#!/usr/bin/env python3
"""
Autonomous Priority-First Publisher & YouTube Native Release Scheduler for @influenzian
(`UCcJFqC7z0f-ARNcJadKiKpQ`) — World Chess Championship 2026 (Sindarov & Gukesh) -> Magnus Series -> Pragg Series.

Features:
  - Strictly enforces target channel ID == UCcJFqC7z0f-ARNcJadKiKpQ (@influenzian).
  - Strictly enforces ZERO-CTA policy across titles, tags, scripts, and descriptions.
  - Priority-First Queue Ordering:
      * Wave 0 (priority 0): Any newly completed 2026 World Championship Geneva games (Game 2..14)
      * Wave 1 (priority 1..14): Ongoing World Championship Game 1 + All Sindarov & Gukesh matches
      * Wave 2 (priority 21..26): Resume Magnus Carlsen Rating-Climb Series (Ep07..Ep12)
      * Wave 3 (priority 31..34): Praggnanandhaa Series (Ep20..Ep23)
  - Quota-Maximizing Batch Native Scheduling (`status.publishAt`):
      * Uploads up to 6 episodes per daily quota cycle (6 * 1600 = 9600 / 10000 units).
      * Publishes the first episode immediately (`public`) if no episode went live in the last 3 hours,
        and schedules the remaining uploaded episodes onto YouTube's native release calendar
        (`privacyStatus="private"` + `publishAt` at 08:30, 13:30, 18:00, 21:30 IST daily).
  - Lean rclone fetching: skips already-published episodes and downloads MP4s only for the current upload batch.
"""
import argparse
import datetime
import json
import subprocess
from pathlib import Path

EXPECTED_CHANNEL_ID = "UCcJFqC7z0f-ARNcJadKiKpQ"
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))

# 4 daily World Championship release slots in IST: 08:30 AM, 01:30 PM, 06:00 PM, 09:30 PM IST
DAILY_SLOTS_IST = [
    (8, 30),
    (13, 30),
    (18, 0),
    (21, 30),
]

# Explicit Wave Priority Map:
#   Wave 1 (1..14): World Championship 2026 + Sindarov & Gukesh matches FIRST
#   Wave 2 (21..26): Resume Magnus Carlsen series (Ep07..Ep12)
#   Wave 3 (31..34): Praggnanandhaa series (Ep20..Ep23)
PRIORITY_ORDER_MAP = {
    # Wave 1A: 2026 World Championship Geneva & Direct Sindarov-Gukesh Rivalry + Qualification
    "Ep25_WCh2026_Game1_Sindarov_Gukesh": 1,
    "Ep26_Sindarov_Gukesh_2026_TataSteel_QueenSac": 2,
    "Ep27_Sindarov_Gukesh_2022_Sharjah_H2H": 3,
    "Ep18_Gukesh_Ding_2024_WCh_Crown": 4,
    "Ep28_WeiYi_Sindarov_2025_WorldCup_Crown": 5,
    "Ep29_Sindarov_Caruana_2026_Candidates": 6,
    "Ep30_Nakamura_Sindarov_2026_Candidates": 7,
    # Wave 1B: Gukesh & Sindarov Signature Super-GM Climbs
    "Ep19_Gukesh_Carlsen_2025_Norway": 8,
    "Ep13_Sindarov_Firouzja_2021_WorldCup": 9,
    "Ep14_Carlsen_Sindarov_2024_Summit": 10,
    "Ep15_Gukesh_Abdusattorov_2022_Biel": 11,
    "Ep16_Gukesh_Firouzja_2023_Norway": 12,
    "Ep17_Gukesh_Maghsoodloo_2024_Olympiad": 13,
    "Ep24_Pragg_Gukesh_2025_Sinquefield": 14,
    # Wave 2: Resume Magnus Carlsen Rating-Climb Series
    "Ep07_Carlsen_Kramnik_2009_London": 21,
    "Ep08_Carlsen_Topalov_2010_Nanjing": 22,
    "Ep09_Carlsen_Aronian_2012_London": 23,
    "Ep10_Carlsen_Nakamura_2013_TataSteel": 24,
    "Ep11_Anand_Carlsen_2013_Chennai_WCh": 25,
    "Ep12_Carlsen_Caruana_2014_Shamkir_Peak2882": 26,
    # Wave 3: Praggnanandhaa Series
    "Ep20_Pragg_Topalov_2020_Gibraltar": 31,
    "Ep21_Pragg_Nakamura_2023_WorldCup": 32,
    "Ep22_Pragg_Ding_2024_TataSteel": 33,
    "Ep23_Pragg_Carlsen_2024_Norway": 34,
}

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


def resolve_priority(ep_id: str, manifest: dict) -> tuple[int, int]:
    if ep_id in PRIORITY_ORDER_MAP:
        return (PRIORITY_ORDER_MAP[ep_id], manifest.get("seriesOrder", 99))
    if "WCh2026" in ep_id or "Sindarov" in ep_id or "Gukesh" in ep_id:
        return (int(manifest.get("priorityOrder", 0)), manifest.get("seriesOrder", 99))
    return (int(manifest.get("priorityOrder", 50)), manifest.get("seriesOrder", 99))


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

    ep_id = manifest.get("episodeId", "")
    is_wch_era = any(k in ep_id for k in ("WCh2026", "Sindarov", "Gukesh"))
    default_tags = (
        [
            "#WorldChessChampionship",
            "#Gukesh",
            "#Sindarov",
            "#GukeshVsSindarov",
            "#Chess",
            "#Grandmaster",
            "#ChessBrilliancy",
            "#ChessTactics",
            "#StickmanChess",
        ]
        if is_wch_era
        else [
            "#Magnus",
            "#MagnusCarlsen",
            "#Chess",
            "#Grandmaster",
            "#ChessBrilliancy",
            "#ChessTactics",
            "#Checkmate",
            "#ChessGame",
            "#StickmanChess",
        ]
    )
    raw_tags = list(manifest.get("hashtags", []))
    for t in default_tags:
        if t not in raw_tags:
            raw_tags.append(t)
    tags_str = " ".join(raw_tags)

    series_num = manifest.get("seriesOrder", 1)
    prefix = manifest.get("descriptionPrefix") or f"Chess Masterpiece {series_num:03d}"

    desc = (
        f"{prefix} — {manifest.get('youtubeTitle') or manifest.get('title')}\n"
        f"{manifest.get('eventBadge', '')} — {manifest.get('subHeader', '')}\n"
        f"{matchup}\n\n"
        f"Zen Storyteller Chess: calm handholding narration, colorful 2D pieces on a divided board, a summoned stickman performing critical moves, snare drum-roll sacrifices, and escalating move-quality sound design.\n\n"
        f"Chapters:\n" + "\n".join(chapters) + "\n\n"
        f"Verified Historical Sources:\n{sources}\n\n"
        f"{tags_str}"
    )
    desc = desc.replace("->", "→").replace("<=", "≤").replace(">=", "≥").replace("<", "under ").replace(">", "over ")
    assert_zero_cta(desc, f"{ep_id}.description")
    return desc[:4900]


def build_seo_tags(manifest: dict) -> list[str]:
    wp_name = manifest.get("whitePlayer", {}).get("name", "").replace("GM ", "").replace("IM ", "").strip()
    bp_name = manifest.get("blackPlayer", {}).get("name", "").replace("GM ", "").replace("IM ", "").strip()
    ep_id = manifest.get("episodeId", "")
    tags = []
    for cand in [
        wp_name,
        bp_name,
        f"{wp_name} vs {bp_name}" if wp_name and bp_name else "",
        "World Chess Championship 2026" if ("Sindarov" in ep_id or "Gukesh" in ep_id) else "",
        "Gukesh vs Sindarov" if ("Sindarov" in ep_id or "Gukesh" in ep_id) else "",
        "Geneva World Chess Championship" if "WCh2026" in ep_id else "",
        "D Gukesh" if "Gukesh" in ep_id else "",
        "Javokhir Sindarov" if "Sindarov" in ep_id else "",
        "Magnus Carlsen" if "Carlsen" in ep_id else "",
        "Chess",
        "Chess Brilliancy",
        "Grandmaster Chess",
        "Stickman Chess",
        "Chess Analysis",
        "Influenzian",
    ]:
        if cand and cand not in tags:
            tags.append(cand)
    return tags[:15]


def get_youtube_clients(cred_dir: Path) -> list:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    candidates = []
    seen_refresh = set()
    all_paths = [cred_dir / "token_influenzian.json"]
    if (cred_dir / "tokens_influenzian").is_dir():
        all_paths.extend(sorted((cred_dir / "tokens_influenzian").glob("*.json")))

    for p in all_paths:
        if not p.exists():
            continue
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
            key = raw.get("refresh_token") or str(p.resolve())
            if key in seen_refresh:
                continue
            seen_refresh.add(key)
            candidates.append(p)
        except Exception:
            continue

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


def discover_pending_from_rclone(remote_dir: str, local_cache: Path, published_ids: set[str]) -> list[tuple[tuple[int, int], str, Path]]:
    """Lists Drive folders, skips already-published IDs, fetches manifest.json only first, and returns sorted pending list."""
    local_cache.mkdir(parents=True, exist_ok=True)
    res = subprocess.run(["rclone", "lsf", remote_dir, "--dirs-only"], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[Drive Notice] '{remote_dir}' unavailable ({res.stderr.strip()})")
        return []
    pending = []
    for line in res.stdout.splitlines():
        sub = line.strip().rstrip("/")
        if not sub or sub in published_ids:
            continue
        dst = local_cache / sub
        dst.mkdir(parents=True, exist_ok=True)
        subprocess.run(["rclone", "copy", f"{remote_dir}/{sub}/manifest.json", str(dst)], check=False)
        mf_path = dst / "manifest.json"
        if not mf_path.exists():
            continue
        mf = json.loads(mf_path.read_text(encoding="utf-8"))
        ep_id = mf["episodeId"]
        if ep_id in published_ids:
            continue
        pending.append((resolve_priority(ep_id, mf), ep_id, dst))
    pending.sort(key=lambda x: x[0])
    return pending


def ensure_episode_media(remote_dir: str, ep_id: str, ep_dir: Path) -> bool:
    if list(ep_dir.glob("*_1080p.mp4")):
        return True
    print(f"[Drive Pull] Downloading {ep_id} media from {remote_dir}/{ep_id} ...")
    subprocess.run(["rclone", "copy", f"{remote_dir}/{ep_id}", str(ep_dir)], check=False)
    return bool(list(ep_dir.glob("*_1080p.mp4")))


def compute_next_schedule_slots(registry: dict, count: int, immediate_first: bool) -> list[tuple[str, str | None]]:
    """
    Returns `count` tuples of (privacyStatus, publishAt_iso_utc_or_None).
    Books deterministic 4x/day IST slots (08:30, 13:30, 18:00, 21:30 IST) without colliding
    with already-scheduled episodes in `registry['published']`.
    """
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    booked_utc = set()
    recent_live = False

    for info in registry.get("published", {}).values():
        sched_s = info.get("scheduledPublishAt")
        pub_s = info.get("publishedAt")
        if sched_s:
            try:
                dt = datetime.datetime.fromisoformat(sched_s.replace("Z", "+00:00"))
                booked_utc.add(dt.strftime("%Y-%m-%dT%H:%M"))
                if abs((dt - now_utc).total_seconds()) < 2.5 * 3600:
                    recent_live = True
            except Exception:
                pass
        elif pub_s:
            try:
                dt = datetime.datetime.fromisoformat(pub_s.replace("Z", "+00:00"))
                if 0 <= (now_utc - dt).total_seconds() < 3.0 * 3600:
                    recent_live = True
            except Exception:
                pass

    plan: list[tuple[str, str | None]] = []
    if immediate_first and not recent_live and count > 0:
        plan.append(("public", None))

    now_ist = now_utc.astimezone(IST)
    min_future_utc = now_utc + datetime.timedelta(minutes=25)
    day_offset = 0
    while len(plan) < count and day_offset < 45:
        base_date = (now_ist + datetime.timedelta(days=day_offset)).date()
        for hh, mm in DAILY_SLOTS_IST:
            slot_ist = datetime.datetime(
                base_date.year, base_date.month, base_date.day, hh, mm, 0, tzinfo=IST
            )
            slot_utc = slot_ist.astimezone(datetime.timezone.utc)
            if slot_utc <= min_future_utc:
                continue
            key = slot_utc.strftime("%Y-%m-%dT%H:%M")
            if key in booked_utc:
                continue
            booked_utc.add(key)
            iso_z = slot_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
            plan.append(("private", iso_z))
            if len(plan) >= count:
                break
        day_offset += 1

    return plan


def find_thumbnail(ep_dir: Path, ep_id: str) -> Path | None:
    for name in (f"{ep_id}_thumb_16x9.jpg", "thumbnail_16x9.jpg"):
        cand = ep_dir / name
        if cand.exists() and cand.stat().st_size < 2 * 1024 * 1024:
            return cand
    return None


def publish_episode(yt, ep_dir: Path, privacy: str, publish_at_utc: str | None = None) -> str:
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
    tags = build_seo_tags(manifest)

    status_body: dict = {
        "privacyStatus": "private" if publish_at_utc else privacy,
        "selfDeclaredMadeForKids": False,
    }
    if publish_at_utc:
        status_body["publishAt"] = publish_at_utc

    body = {
        "snippet": {
            "title": raw_title,
            "description": description,
            "tags": tags,
            "categoryId": "24",
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en",
        },
        "status": status_body,
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
    if publish_at_utc:
        print(f"[Scheduled on YouTube -> {publish_at_utc}] {ep_id} -> https://youtu.be/{vid}")
    else:
        print(f"[Published LIVE ({privacy})] {ep_id} -> https://youtu.be/{vid}")

    thumb_path = find_thumbnail(ep_dir, ep_id)
    if thumb_path is not None:
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(thumb_path))).execute()
            print(f"[Thumbnail Applied] {thumb_path.name} -> {vid}")
        except Exception as thumb_exc:
            print(f"[Thumbnail Notice] {vid} uploaded, custom thumbnail skipped: {thumb_exc}")
    return vid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--local-catalog", default="", help="Local episodes/chess_series dir")
    ap.add_argument("--drive-remote", default="gdrive:Influenzian/DailyQueue/CHESS")
    ap.add_argument("--cred-dir", default="data/credentials")
    ap.add_argument("--registry", default="production/influenzian_chess_published_registry.json")
    ap.add_argument("--privacy", choices=["public", "unlisted", "scheduled"], default="scheduled")
    ap.add_argument("--max-uploads", type=int, default=6)
    ap.add_argument("--only-episode", default="", help="Publish only this exact episodeId")
    ap.add_argument("--dry-run", action="store_true", help="Print priority queue and target schedule slots without uploading")
    args = ap.parse_args()

    reg_path = Path(args.registry)
    reg_path.parent.mkdir(parents=True, exist_ok=True)
    registry = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.exists() else {"published": {}}
    published_ids = set(registry.get("published", {}).keys())

    pending: list[tuple[tuple[int, int], str, Path]] = []
    use_local = bool(args.local_catalog and Path(args.local_catalog).is_dir())
    if use_local:
        for d in sorted(Path(args.local_catalog).iterdir()):
            if not d.is_dir() or not (d / "manifest.json").exists():
                continue
            mf = json.loads((d / "manifest.json").read_text(encoding="utf-8"))
            ep_id = mf["episodeId"]
            if args.only_episode and ep_id != args.only_episode:
                continue
            if ep_id not in published_ids and list(d.glob("*_1080p.mp4")):
                pending.append((resolve_priority(ep_id, mf), ep_id, d))
        pending.sort(key=lambda x: x[0])
    else:
        pending = discover_pending_from_rclone(args.drive_remote, Path("/tmp/influenzian_chess_queue"), published_ids)
        if args.only_episode:
            pending = [x for x in pending if x[1] == args.only_episode]

    if not pending:
        print("[Queue Clean] All staged Chess episodes are already published/scheduled on YouTube!")
        return

    batch = pending[: args.max_uploads]
    if args.privacy == "scheduled":
        slot_plan = compute_next_schedule_slots(registry, len(batch), immediate_first=True)
    else:
        slot_plan = [(args.privacy, None) for _ in batch]

    print(f"[Priority Queue] {len(pending)} pending chess episode(s); batch={len(batch)}:")
    for idx, ((prio, s_ord), ep_id, _) in enumerate(batch):
        priv_mode, pub_at = slot_plan[idx]
        when_lbl = f"SCHEDULED {pub_at}" if pub_at else f"IMMEDIATE {priv_mode.upper()}"
        print(f"  {idx+1:02d}. [prio={prio:02d} #{s_ord:02d}] {ep_id} -> {when_lbl}")

    if args.dry_run:
        return

    clients = get_youtube_clients(Path(args.cred_dir))
    if not clients:
        print("[Notice] No valid @influenzian OAuth client available right now (quota resets 08:00 UTC / 13:30 IST); episodes remain staged & ready.")
        return

    uploaded_count = 0
    client_idx = 0

    for idx, (_, ep_id, ep_dir) in enumerate(batch):
        if not use_local and not ensure_episode_media(args.drive_remote, ep_id, ep_dir):
            print(f"[Skip] {ep_id} MP4 not yet on Drive.")
            continue
        priv_mode, pub_at = slot_plan[idx]
        while client_idx < len(clients):
            tname, yt = clients[client_idx]
            try:
                vid = publish_episode(yt, ep_dir, priv_mode, publish_at_utc=pub_at)
                entry = {
                    "youtubeVideoId": vid,
                    "url": f"https://youtu.be/{vid}",
                    "privacyStatus": "scheduled" if pub_at else priv_mode,
                    "channelId": EXPECTED_CHANNEL_ID,
                    "publishedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                }
                if pub_at:
                    entry["scheduledPublishAt"] = pub_at
                registry["published"][ep_id] = entry
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
                        print("[Channel Daily Cap Reached] Remaining episodes will auto-schedule on the next cycle.")
                        client_idx = len(clients)
                        break
                    client_idx += 1
                else:
                    raise
        if client_idx >= len(clients):
            print("[Quota Exhausted Today] Remaining episodes will auto-schedule at next quota reset (08:00 UTC / 13:30 IST).")
            break

    print(f"[Summary] Uploaded/Scheduled {uploaded_count} chess episode(s) in this run; total in YouTube pipeline={len(registry['published'])}.")


if __name__ == "__main__":
    main()
