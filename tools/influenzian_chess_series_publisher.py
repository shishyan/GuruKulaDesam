#!/usr/bin/env python3
"""
Autonomous Publisher & Daily Queue Drip Engine for @influenzian Main Channel
(`UCcJFqC7z0f-ARNcJadKiKpQ`) — Magnus Carlsen & Javokhir Sindarov Stickman 3D Chess Series.

Features:
  - Strictly enforces target channel ID == UCcJFqC7z0f-ARNcJadKiKpQ (@influenzian).
  - Strictly enforces ZERO-CTA policy across titles, tags, scripts, and descriptions.
  - Builds rich chapter timestamps + historical PGN source attributions.
  - Pulls rendered 1080p MP4s + verified 16:9 thumbnails from local catalog or
    Google Drive (`gdrive:Influenzian/DailyQueue/CHESS/<EPISODE_ID>/`).
  - Rotates across available `@influenzian` OAuth tokens and exits cleanly on
    quotaExceeded / uploadLimitExceeded while saving progress in
    `production/influenzian_chess_published_registry.json`.
"""
import argparse
import datetime
import json
import subprocess
from pathlib import Path

EXPECTED_CHANNEL_ID = "UCcJFqC7z0f-ARNcJadKiKpQ"

BANNED_CTA_PHRASES = (
    "subscribe",
    "hit the bell",
    "click the bell",
    "smash that like",
    "drop a like",
    "like and share",
    "leave a comment",
    "comment below",
    "follow for more",
)


def assert_zero_cta(text: str, ctx: str) -> None:
    low = (text or "").lower()
    for w in BANNED_CTA_PHRASES:
        if w in low:
            raise ValueError(f"STRICT ZERO-CTA VIOLATION in {ctx}: found '{w}'")


def fmt_mmss(sec: float) -> str:
    s = max(0, int(round(sec)))
    return f"{s // 60:02d}:{s % 60:02d}"


def build_chess_description(manifest: dict) -> str:
    chapters = []
    seen_ch = set()
    for b in manifest.get("beats", []):
        ch = b.get("chapter", "").strip()
        if ch and ch not in seen_ch:
            seen_ch.add(ch)
            chapters.append(f"{fmt_mmss(b.get('startSec', 0))} {ch}")

    wp = manifest.get("whitePlayer", {})
    bp = manifest.get("blackPlayer", {})
    matchup = f"White: {wp.get('name', 'White')} ({wp.get('rating', '')}) vs Black: {bp.get('name', 'Black')} ({bp.get('rating', '')})"
    sources = "\n".join(f"• {s}" for s in manifest.get("sources", []))
    tags = " ".join(manifest.get("hashtags", ["#MagnusCarlsen", "#JavokhirSindarov", "#Chess"]))

    desc = (
        f"{manifest.get('youtubeTitle') or manifest.get('title')}\n"
        f"{manifest.get('eventBadge', '')} — {manifest.get('subHeader', '')}\n"
        f"{matchup}\n\n"
        f"Every chess piece moves in true 3D phase with escalating move-quality sound design and character mind-out banter.\n\n"
        f"Chapters:\n" + "\n".join(chapters) + "\n\n"
        f"Verified Historical Sources:\n{sources}\n\n"
        f"{tags}"
    )
    desc = desc.replace("->", "→").replace("<=", "≤").replace(">=", "≥").replace("<", "under ").replace(">", "over ")
    assert_zero_cta(desc, f"{manifest['episodeId']}.description")
    return desc[:4900]


def get_youtube_clients(cred_dir: Path) -> list:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    candidates = []
    seen = set()
    for p in [cred_dir / "token_influenzian.json"] + sorted((cred_dir / "tokens_influenzian").glob("*.json")):
        if p.exists() and str(p.resolve()) not in seen:
            seen.add(str(p.resolve()))
            candidates.append(p)

    clients = []
    for tpath in candidates:
        try:
            creds = Credentials.from_authorized_user_file(str(tpath))
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                tpath.write_text(creds.to_json(), encoding="utf-8")
            yt = build("youtube", "v3", credentials=creds)
            ch = yt.channels().list(part="id,snippet", mine=True).execute()
            items = ch.get("items", [])
            if not items:
                continue
            ch_id = items[0]["id"]
            if ch_id != EXPECTED_CHANNEL_ID:
                print(f"[Security Guard] Skipping {tpath.name}: resolved to {ch_id} != {EXPECTED_CHANNEL_ID}")
                continue
            print(f"[OAuth Ready] {items[0]['snippet']['title']} ({ch_id}) via {tpath.name}")
            clients.append((tpath.name, yt))
        except Exception as exc:
            print(f"[OAuth Skip] {tpath.name}: {exc}")
    return clients


def pull_from_rclone(remote_dir: str, local_cache: Path) -> list[Path]:
    local_cache.mkdir(parents=True, exist_ok=True)
    res = subprocess.run(["rclone", "lsf", remote_dir, "--dirs-only"], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[Drive Notice] '{remote_dir}' unavailable ({res.stderr.strip()})")
        return []
    ep_dirs = []
    for line in res.stdout.splitlines():
        sub = line.strip().rstrip("/")
        if not sub:
            continue
        dst = local_cache / sub
        dst.mkdir(parents=True, exist_ok=True)
        subprocess.run(["rclone", "copy", f"{remote_dir}/{sub}", str(dst)], check=False)
        if (dst / "manifest.json").exists():
            ep_dirs.append(dst)
    return sorted(ep_dirs)


def find_thumbnail(ep_dir: Path, ep_id: str) -> Path | None:
    for name in (f"{ep_id}_thumb_16x9.jpg", "thumbnail_16x9.jpg"):
        cand = ep_dir / name
        if cand.exists() and cand.stat().st_size < 2 * 1024 * 1024:
            return cand
    return None


def publish_episode(yt, ep_dir: Path, privacy: str) -> str:
    from googleapiclient.http import MediaFileUpload

    manifest = json.loads((ep_dir / "manifest.json").read_text(encoding="utf-8"))
    ep_id = manifest["episodeId"]
    assert_zero_cta(json.dumps(manifest), ep_id)

    mp4s = list(ep_dir.glob("*_1080p.mp4"))
    if not mp4s:
        raise FileNotFoundError(f"No *_1080p.mp4 in {ep_dir}")
    mp4_path = mp4s[0]

    raw_title = (manifest.get("youtubeTitle") or manifest["title"]).replace("<", "").replace(">", "")[:98]
    assert_zero_cta(raw_title, f"{ep_id}.title")
    description = build_chess_description(manifest)

    tags = [
        "Magnus Carlsen",
        "Javokhir Sindarov",
        "Chess",
        "Stickman Animation",
        "Chess Brilliancy",
        "Grandmaster",
        "Influenzian",
    ]
    body = {
        "snippet": {
            "title": raw_title,
            "description": description,
            "tags": tags,
            "categoryId": "24",  # Entertainment / Storytelling
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    req = yt.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(str(mp4_path), chunksize=8 * 1024 * 1024, resumable=True),
    )
    resp = None
    while resp is None:
        _, resp = req.next_chunk()
    vid = resp["id"]
    print(f"[Published LIVE ({privacy})] {ep_id} -> https://youtu.be/{vid}")

    thumb_path = find_thumbnail(ep_dir, ep_id)
    if thumb_path is not None:
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(thumb_path))).execute()
            print(f"[Thumbnail Applied] {thumb_path.name} -> {vid}")
        except Exception as thumb_exc:
            print(f"[Thumbnail Notice] {vid} uploaded, thumbnail skipped: {thumb_exc}")
    return vid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--local-catalog", default="", help="Local episodes/chess_series dir")
    ap.add_argument("--drive-remote", default="gdrive:Influenzian/DailyQueue/CHESS")
    ap.add_argument("--cred-dir", default="data/credentials")
    ap.add_argument("--registry", default="production/influenzian_chess_published_registry.json")
    ap.add_argument("--privacy", choices=["public", "unlisted"], default="public")
    ap.add_argument("--max-uploads", type=int, default=6)
    args = ap.parse_args()

    reg_path = Path(args.registry)
    reg_path.parent.mkdir(parents=True, exist_ok=True)
    registry = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.exists() else {"published": {}}

    if args.local_catalog and Path(args.local_catalog).is_dir():
        ep_dirs = sorted(
            [d for d in Path(args.local_catalog).iterdir() if d.is_dir() and (d / "manifest.json").exists()]
        )
    else:
        ep_dirs = pull_from_rclone(args.drive_remote, Path("/tmp/influenzian_chess_queue"))

    pending = []
    for d in ep_dirs:
        mf = json.loads((d / "manifest.json").read_text(encoding="utf-8"))
        ep_id = mf["episodeId"]
        if ep_id not in registry["published"] and list(d.glob("*_1080p.mp4")):
            pending.append((mf.get("seriesOrder", 99), ep_id, d))
    pending.sort(key=lambda x: x[0])

    if not pending:
        print("[Queue Clean] All staged Carlsen & Sindarov chess episodes are already published!")
        return

    clients = get_youtube_clients(Path(args.cred_dir))
    if not clients:
        print("[Notice] No valid @influenzian OAuth client available; episodes remain staged on Drive.")
        return

    uploaded_count = 0
    client_idx = 0

    for _, ep_id, ep_dir in pending:
        if uploaded_count >= args.max_uploads:
            break
        while client_idx < len(clients):
            tname, yt = clients[client_idx]
            try:
                vid = publish_episode(yt, ep_dir, args.privacy)
                registry["published"][ep_id] = {
                    "youtubeVideoId": vid,
                    "url": f"https://youtu.be/{vid}",
                    "privacyStatus": args.privacy,
                    "channelId": EXPECTED_CHANNEL_ID,
                    "publishedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                }
                reg_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
                uploaded_count += 1
                break
            except Exception as exc:
                msg = str(exc)
                if (
                    "quotaExceeded" in msg
                    or "uploadLimitExceeded" in msg
                    or "exceeded the number of videos" in msg
                    or "403" in msg
                    or "429" in msg
                ):
                    print(f"[Quota/Rate Notice on {tname}] {msg[:220]}")
                    if "exceeded the number of videos" in msg:
                        print("[Channel Daily Cap Reached] Remaining episodes will auto-drip on the next schedule.")
                        client_idx = len(clients)
                        break
                    client_idx += 1
                else:
                    raise
        if client_idx >= len(clients):
            print("[Quota Exhausted Today] Remaining episodes will auto-drip on the next workflow run.")
            break

    print(f"[Summary] Published {uploaded_count} new chess episode(s) in this run; total published={len(registry['published'])}.")


if __name__ == "__main__":
    main()
