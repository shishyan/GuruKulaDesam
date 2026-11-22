#!/usr/bin/env python3
"""
Autonomous Daily 3-Category Publisher & Queue Drip Engine for @influenzian (`UCcJFqC7z0f-ARNcJadKiKpQ`)
Runs daily via GitHub Actions (`.github/workflows/influenzian-daily-3category.yml`) or locally:

3 Categories -> 3 Distinct Audiences (3 Daily Slots or Sequential Rotation):
  1. `MIND`        -> Audience A: Knowledge Workers, Students & Strategic Thinkers  (06:30 UTC / 12:00 IST)
  2. `AI_WORKFLOW` -> Audience B: Engineers, Builders & Technical AI Operators      (13:30 UTC / 19:00 IST)
  3. `MONEY`       -> Audience C: Working Professionals, Families & Investors       (19:30 UTC / 01:00 IST)

STRICT ZERO-CTA INVARIANT:
  - Descriptions, titles, tags, and transcripts NEVER ask viewers to subscribe, like, comment, share, or hit the bell.
  - Pure research citations, chapter timestamps, and practical operating frameworks only.

Storage & Quota Resilience:
  - Reads rendered 1080p MP4s + verified 16:9 thumbnails from Google Drive (`gdrive:Influenzian/DailyQueue/<CATEGORY>/<EPISODE_ID>/`)
    when running inside GitHub Actions (zero binaries stored in Git).
  - Rotates across available `@influenzian` OAuth tokens (`token_influenzian.json`, `tokens_influenzian/token_*.json`).
  - Records published YouTube IDs in `production/influenzian_daily_published_registry.json` so episodes never duplicate.
"""
import argparse
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

BANNED_CTA_WORDS = (
    "subscribe",
    "hit the bell",
    "smash that like",
    "like and share",
    "leave a comment",
    "follow for more",
)

CATEGORIES = ["MIND", "AI_WORKFLOW", "MONEY"]

CATEGORY_HASHTAGS = {
    "MIND": "#CognitiveScience #MentalModels #Neuroscience #DecisionMaking #DeepWork",
    "AI_WORKFLOW": "#AIEngineering #AgentWorkflows #SystemsDesign #LLMVerification #Automation",
    "MONEY": "#BehavioralFinance #IndexInvesting #Compounding #PersonalFinance #WealthMath",
}


def assert_zero_cta(text: str, context: str):
    low = text.lower()
    for w in BANNED_CTA_WORDS:
        if w in low:
            raise ValueError(f"ZERO-CTA POLICY VIOLATION in {context}: found '{w}'")


def fmt_mmss(sec: float) -> str:
    s = max(0, int(round(sec)))
    return f"{s // 60:02d}:{s % 60:02d}"


def build_pure_utility_description(manifest: dict) -> str:
    chapters = []
    citations = []
    if "beats" in manifest:
        for beat in manifest.get("beats", []):
            if beat.get("yearStamp"):
                ts = fmt_mmss(beat.get("startSec", 0))
                chapters.append(f"{ts} {beat['yearStamp']}")
        aud = manifest.get("audience", "Future Builders, Families & Visionary Leaders")
        cat = manifest.get("category", "MIND")
        desc = (
            f"{manifest['title']}\n\n"
            f"Year-by-Year Timeline:\n" + "\n".join(chapters) + "\n\n"
            f"{CATEGORY_HASHTAGS.get(cat, '#FutureTimeline #2026to2050 #Leadership #Abundance')}"
        )
    else:
        for sc in manifest.get("scenes", []):
            ts = fmt_mmss(sc.get("startSec", 0))
            chapters.append(f"{ts} {sc['chapterTitle']}")
            cit = sc.get("citation", {})
            citations.append(
                f"• [{ts}] {cit.get('sourceName', '')} ({cit.get('year', '')}) — {cit.get('sourceDetail', '')}"
            )
        cat = manifest.get("category", "MIND")
        aud = manifest.get("audience", "Practitioners & Decision Makers")
        desc = (
            f"{manifest['title']}\n"
            f"Target Operating Brief · {aud}\n\n"
            f"Chapters:\n" + "\n".join(chapters) + "\n\n"
            f"Primary Research & Empirical Citations:\n" + "\n".join(citations) + "\n\n"
            f"{CATEGORY_HASHTAGS.get(cat, '#MentalModels #SystemsThinking')}"
        )
    # Sanitize literal '<' and '>' which YouTube Data API v3 rejects with HTTP 400 invalidDescription
    desc = desc.replace("->", "→").replace("<=", "≤").replace(">=", "≥").replace("<", "under ").replace(">", "over ")
    assert_zero_cta(desc, manifest["episodeId"])
    return desc[:4900]


def get_youtube_client(cred_dir: Path):
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    candidates = [cred_dir / "token_influenzian.json"]
    tok_sub = cred_dir / "tokens_influenzian"
    if tok_sub.is_dir():
        candidates.extend(sorted(tok_sub.glob("*.json")))

    for tpath in candidates:
        if not tpath.exists():
            continue
        try:
            creds = Credentials.from_authorized_user_file(str(tpath))
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                tpath.write_text(creds.to_json(), encoding="utf-8")
            yt = build("youtube", "v3", credentials=creds)
            ch = yt.channels().list(part="id,snippet", mine=True).execute()
            items = ch.get("items", [])
            if items:
                print(f"[OAuth Active] Connected to {items[0]['snippet']['title']} ({items[0]['id']}) via {tpath.name}")
                return yt
        except Exception as exc:
            print(f"[OAuth Skip] {tpath.name}: {exc}")
    return None


def pull_from_rclone_if_needed(remote_dir: str, local_cache: Path) -> list[Path]:
    local_cache.mkdir(parents=True, exist_ok=True)
    res = subprocess.run(["rclone", "lsf", remote_dir, "--dirs-only"], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[Drive Queue Notice] rclone remote '{remote_dir}' unavailable ({res.stderr.strip()})")
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


def publish_episode(yt, ep_dir: Path, privacy: str) -> str | None:
    from googleapiclient.http import MediaFileUpload

    manifest = json.loads((ep_dir / "manifest.json").read_text(encoding="utf-8"))
    assert_zero_cta(json.dumps(manifest), manifest["episodeId"])
    mp4s = list(ep_dir.glob("*_1080p.mp4"))
    if not mp4s:
        print(f"[Skip] No rendered 1080p MP4 found in {ep_dir}")
        return None
    mp4_path = mp4s[0]
    thumb_path = ep_dir / "thumbnail_16x9.jpg"

    title = manifest["title"].replace("<", "").replace(">", "")[:98]
    assert_zero_cta(title, "title")
    description = build_pure_utility_description(manifest)

    is_paper_story = "beats" in manifest
    tags = (
        [
            "Future Timeline",
            "2026 to 2050",
            "Future Leaders",
            "Abundance Economics",
            "Technological Singularity",
            "Systems Thinking",
        ]
        if is_paper_story
        else [
            manifest.get("category", "MIND"),
            "Operating Manual",
            "Cognitive Science",
            "Systems Thinking",
            "Behavioral Finance",
            "AI Engineering",
        ]
    )
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "27",  # Education
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
    print(f"[Published -> YouTube ({privacy})] {manifest['episodeId']} -> https://youtu.be/{vid}")
    if thumb_path.exists() and thumb_path.stat().st_size < 2 * 1024 * 1024:
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(thumb_path))).execute()
            print(f"[Thumbnail Set] Custom 16:9 poster applied to {vid}")
        except Exception as thumb_exc:
            print(f"[Thumbnail Notice] Video {vid} is LIVE, custom thumbnail skipped until YouTube Studio phone verification is enabled: {thumb_exc}")
    return vid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", choices=["ALL", "MIND", "AI_WORKFLOW", "MONEY"], default="ALL")
    ap.add_argument("--local-catalog", default="", help="Optional local daily_catalog path")
    ap.add_argument("--drive-remote", default="gdrive:Influenzian/DailyQueue")
    ap.add_argument("--cred-dir", default="data/credentials")
    ap.add_argument("--registry", default="production/influenzian_daily_published_registry.json")
    ap.add_argument("--privacy", choices=["public", "unlisted"], default="public")
    args = ap.parse_args()

    reg_path = Path(args.registry)
    reg_path.parent.mkdir(parents=True, exist_ok=True)
    registry = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.exists() else {"published": {}}

    target_cats = CATEGORIES if args.category == "ALL" else [args.category]
    yt = get_youtube_client(Path(args.cred_dir))

    for cat in target_cats:
        candidate_dirs = []
        if args.local_catalog and Path(args.local_catalog).is_dir():
            for d in sorted(Path(args.local_catalog).iterdir()):
                mf = d / "manifest.json"
                if mf.exists() and json.loads(mf.read_text()).get("category") == cat:
                    candidate_dirs.append(d)
        else:
            candidate_dirs = pull_from_rclone_if_needed(f"{args.drive_remote}/{cat}", Path("/tmp/influenzian_queue") / cat)

        next_ep = None
        for d in candidate_dirs:
            ep_id = json.loads((d / "manifest.json").read_text())["episodeId"]
            if ep_id not in registry["published"]:
                next_ep = (ep_id, d)
                break

        if not next_ep:
            print(f"[{cat}] Queue clean — no unpublished episode pending.")
            continue

        ep_id, ep_dir = next_ep
        print(f"[{cat}] Selected next autonomous episode: {ep_id}")
        if yt is None:
            print(f"[{cat}] Waiting on valid INFLUENZIAN_OAUTH_TOKEN to push {ep_id} to YouTube (staged & ready on Drive).")
            continue

        vid = publish_episode(yt, ep_dir, args.privacy)
        if vid:
            registry["published"][ep_id] = {
                "youtubeVideoId": vid,
                "url": f"https://youtu.be/{vid}",
                "category": cat,
                "privacyStatus": args.privacy,
                "publishedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
            reg_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
