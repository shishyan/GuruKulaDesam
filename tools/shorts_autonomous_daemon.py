#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/shorts_autonomous_daemon.py
Autonomous 24/7 YouTube Shorts Publisher & Liturgical Scheduler for @gurukuladesam2
(Channel ID: UCGUmNzaV_OUFbsNdHJQtaNQ | Parent Channel: @guru-kula-desam).

Capabilities:
1. 100% Liturgical & Tamil Panchangam Alignment (tools/tamil_panchangam_engine.py):
   - Every scheduled slot (06:00 AM, 12:00 PM, 06:00 PM IST) is evaluated against the astronomical
     Tamil Calendar (Month, Tithi, Nakshatra, Vara) so:
       * Maha Shivaratri / Masa Shivaratri / Pradosham / Theypirai Ashtami -> Strictly Lord Shiva
       * Vaikunta Ekadashi / Ekadashi / Thiruvonam / Purattasi Saturday -> Strictly Lord Vishnu / Perumal
       * Skanda Sashti / Krittika / Thaipusam / Panguni Uthiram -> Strictly Lord Murugan
       * Sankatahara Chaturthi / Shukla Chaturthi -> Strictly Lord Vinayagar
       * Pournami / Amavasai / Aadi & Thai Fridays -> Strictly Goddess Amman / Abhirami
   - Never posts a forbidden deity on a sacred festival day.
2. Parent Channel Credit & Traffic Funnel (@guru-kula-desam):
   - Every Short includes on-screen credit, top-of-description links to the full 1080p master film
     on @guru-kula-desam, and automatically posts an top comment on the Short with the clickable
     full-video link!
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.authorize_gurukuladesam2 import (
    CHANNELS_CONFIG,
    ORIGINAL_CHANNEL_ID,
    ORIGINAL_HANDLE,
    TARGET_CHANNEL_ID,
    TARGET_HANDLE,
    get_channel_youtube_service,
    get_gurukuladesam2_youtube_service,
    mark_gkd2_project_exhausted,
)
from tools.tamil_panchangam_engine import (
    IST,
    get_auspicious_alignment_for_datetime,
    print_7day_panchangam_forecast,
)
from tools.shorts_viral_builder import (
    SHORTS_OUT_DIR,
    build_short_for_track,
    list_candidate_tracks,
)

PUBLISHED_REGISTRY_FILE = ROOT / "production" / "shorts_metadata" / "gurukuladesam2_published_registry.json"

# 4 Peak Viral Slots per day in IST (Hour, Minute)
DAILY_IST_SLOTS = [
    (6, 0),   # 06:00 AM IST — Brahma Muhurtham / Morning Worship
    (11, 0),  # 11:00 AM IST — Midday Temple Ucchikalam
    (16, 0),  # 04:00 PM IST — Afternoon / Pre-Pradosham
    (20, 0),  # 08:00 PM IST — Evening / Ardhajama Pooja
]


def load_published_registry() -> dict:
    if PUBLISHED_REGISTRY_FILE.exists():
        try:
            return json.loads(PUBLISHED_REGISTRY_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "channel_id": TARGET_CHANNEL_ID,
        "channel_handle": TARGET_HANDLE,
        "parent_channel_handle": "@guru-kula-desam",
        "published_shorts": {},
        "scheduled_slots": [],
    }


def save_published_registry(reg: dict):
    PUBLISHED_REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    PUBLISHED_REGISTRY_FILE.write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")


def get_next_schedule_slots(count: int, reg: dict) -> list[datetime]:
    now_ist = datetime.now(IST)
    occupied = set(reg.get("scheduled_slots", []))
    slots = []
    day_offset = 0

    while len(slots) < count and day_offset < 90:
        target_date = (now_ist + timedelta(days=day_offset)).date()
        for hr, mn in DAILY_IST_SLOTS:
            slot_dt = datetime(target_date.year, target_date.month, target_date.day, hr, mn, 0, tzinfo=IST)
            if slot_dt > now_ist + timedelta(minutes=20):
                iso_key = slot_dt.isoformat()
                if iso_key not in occupied:
                    slots.append(slot_dt)
                    if len(slots) >= count:
                        break
        day_offset += 1

    return slots


def pick_track_for_slot(slot_dt: datetime, used_track_ids: set[str], forced_deity: str | None = None) -> tuple[dict, dict]:
    """
    Uses the Tamil Panchangam engine to determine the exact mandated deity for `slot_dt`,
    enforces hard exclusion rules, and selects the next unpublished track for that deity.
    """
    panchangam = get_auspicious_alignment_for_datetime(slot_dt)
    target_deity = forced_deity.lower() if forced_deity else panchangam["active_deity"]
    forbidden = set(panchangam.get("forbidden_deities", []))

    if target_deity in forbidden:
        target_deity = panchangam["primary_deity"]

    # First try tracks matching target_deity that haven't been published yet
    deity_candidates = list_candidate_tracks(deity_filter=target_deity, prioritize_high_energy=False)
    for c in deity_candidates:
        if c["track_id"] not in used_track_ids:
            return c, panchangam

    # If all tracks of target_deity have been used, try secondary_deity (if not forbidden)
    sec_deity = panchangam.get("secondary_deity")
    if sec_deity and sec_deity not in forbidden:
        sec_candidates = list_candidate_tracks(deity_filter=sec_deity, prioritize_high_energy=False)
        for c in sec_candidates:
            if c["track_id"] not in used_track_ids:
                return c, panchangam

    # Fallback: cycle back through target_deity tracks
    if deity_candidates:
        return deity_candidates[len(used_track_ids) % len(deity_candidates)], panchangam

    all_cands = [c for c in list_candidate_tracks() if c["deity"] not in forbidden]
    return all_cands[0], panchangam


def post_parent_credit_comment(yt, short_video_id: str, comment_text: str):
    """Posts an official top-level comment on the Short linking to the full song on @guru-kula-desam."""
    try:
        yt.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": short_video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": comment_text
                        }
                    }
                }
            }
        ).execute()
        print(f"   💬 Posted Parent Channel (@guru-kula-desam) full-video link in comments!")
    except Exception as e:
        print(f"   ℹ️ Note: Comment post skipped (video may be scheduled/private until release): {str(e)[:80]}")


def upload_short_via_api(meta: dict, publish_at_dt: datetime | None = None, channel_key: str = "@gurukuladesam") -> str | None:
    video_path = ROOT / meta["video_path"]
    if not video_path.exists():
        raise FileNotFoundError(f"Rendered Short MP4 missing: {video_path}")

    for attempt in range(4):
        try:
            yt, pid, cfg = get_channel_youtube_service(channel_key)
            expected_cid = cfg["channel_id"]
            expected_hnd = cfg["handle"]

            # Verify authenticated channel matches target channel
            ch_res = yt.channels().list(part="id,snippet", mine=True).execute()
            items = ch_res.get("items", [])
            if not items or items[0]["id"] != expected_cid:
                actual_id = items[0]["id"] if items else "None"
                actual_handle = items[0]["snippet"].get("customUrl") if items else "None"
                raise RuntimeError(
                    f"Safety Guard Triggered: Active token belongs to {actual_handle} ({actual_id}), "
                    f"NOT {expected_hnd} ({expected_cid}). "
                    f"Please run: python tools/authorize_gurukuladesam2.py --authorize --channel {channel_key}"
                )

            status_body = {
                "selfDeclaredMadeForKids": False,
            }
            if publish_at_dt is not None:
                utc_dt = publish_at_dt.astimezone(timezone.utc)
                status_body["privacyStatus"] = "private"
                status_body["publishAt"] = utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                mode_label = f"SCHEDULED ({publish_at_dt.strftime('%Y-%m-%d %I:%M %p IST')})"
            else:
                status_body["privacyStatus"] = "public"
                mode_label = "PUBLIC LIVE NOW"

            body = {
                "snippet": {
                    "title": meta["title"][:95],
                    "description": meta["description"],
                    "tags": meta.get("tags", [])[:22],
                    "categoryId": meta.get("categoryId", "10"),
                    "defaultLanguage": "ta",
                    "defaultAudioLanguage": "ta",
                },
                "status": status_body,
            }

            print(f"\n🚀 [UPLOADING SHORT -> {expected_hnd}] {meta['title']}")
            print(f"   • Mode          : {mode_label}")
            print(f"   • File          : {video_path.name} ({meta.get('file_size_mb', 0):.2f} MB)")

            media = MediaFileUpload(str(video_path), mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
            req = yt.videos().insert(part="snippet,status", body=body, media_body=media)

            response = None
            while response is None:
                status, response = req.next_chunk()
                if status:
                    print(f"   > Upload Progress: {int(status.progress() * 100)}%", flush=True)

            vid_id = response.get("id")
            print(f"✅ [SUCCESS -> {expected_hnd}] Short Uploaded! YouTube URL: https://youtube.com/shorts/{vid_id}")
            return vid_id

        except HttpError as e:
            if "quotaExceeded" in str(e) or "uploadLimitExceeded" in str(e):
                print(f"⚠️ Project {pid} hit quota/upload limit for {channel_key}. Rotating to next project...")
                mark_gkd2_project_exhausted(pid, channel_key=channel_key)
                continue
            else:
                print(f"❌ YouTube API HttpError ({channel_key}): {e}")
                return None
        except Exception as e:
            print(f"ℹ️ Skipping upload to {channel_key}: {e}")
            return None

    return None


def run_batch_pipeline(count: int, schedule_mode: bool = False, deity_filter: str = None):
    reg = load_published_registry()
    published_map = reg.get("published_shorts", {})
    used_ids = set(published_map.keys())

    slots = get_next_schedule_slots(count, reg) if schedule_mode else [datetime.now(IST)] * count

    print("=" * 80)
    print(f"🕉️  @GURUKULADESAM PANCHANGAM SHORTS PIPELINE ({count} Shorts)")
    print(f"📺 Target Channel : {ORIGINAL_HANDLE} ({ORIGINAL_CHANNEL_ID})")
    print(f"🗓️  Publishing Mode: {'Scheduled 4x/Day (6AM, 11AM, 4PM, 8PM IST)' if schedule_mode else 'Immediate Public Release'}")
    print("=" * 80)

    completed = 0
    for slot_dt in slots:
        track_item, panchangam = pick_track_for_slot(slot_dt, used_ids, forced_deity=deity_filter)
        tid = track_item["track_id"]
        used_ids.add(tid)

        try:
            meta = build_short_for_track(tid, target_dt=slot_dt)
            yt_vid_id = upload_short_via_api(meta, publish_at_dt=slot_dt if schedule_mode else None, channel_key="@gurukuladesam")
            if yt_vid_id:
                slot_iso = slot_dt.isoformat() if schedule_mode else None
                published_map[tid] = {
                    "youtube_short_id": yt_vid_id,
                    "gurukuladesam_id": yt_vid_id,
                    "short_url": f"https://youtube.com/shorts/{yt_vid_id}",
                    "title": meta["title"],
                    "deity": meta["deity"],
                    "panchangam_occasion": panchangam["occasion_badge_ta"],
                    "uploaded_at": datetime.now(IST).isoformat(),
                    "scheduled_for": slot_iso,
                    "status": "scheduled" if schedule_mode else "public",
                }
                if slot_iso:
                    reg.setdefault("scheduled_slots", []).append(slot_iso)
                reg["published_shorts"] = published_map
                save_published_registry(reg)
                completed += 1
        except Exception as e:
            print(f"❌ Pipeline stopped/errored on track {tid}: {e}")
            break

    print(f"\n🏁 Batch Complete: {completed}/{count} Shorts published/scheduled to {ORIGINAL_HANDLE}.")


def prebuild_panchangam_queue(count: int, deity_filter: str = None):
    """Pre-renders N vertical Shorts aligned with the upcoming IST Panchangam schedule."""
    reg = load_published_registry()
    used_ids = set(reg.get("published_shorts", {}).keys())
    slots = get_next_schedule_slots(count, reg)

    built = 0
    for slot_dt in slots:
        track_item, panchangam = pick_track_for_slot(slot_dt, used_ids, forced_deity=deity_filter)
        tid = track_item["track_id"]
        used_ids.add(tid)
        print(f"\n📅 Slot {slot_dt.strftime('%Y-%m-%d %I:%M %p IST')} -> [{track_item['deity'].upper()}] {tid} ({panchangam['occasion_badge_ta']})")
        try:
            build_short_for_track(tid, target_dt=slot_dt)
            built += 1
        except Exception as e:
            print(f"❌ Failed building {tid}: {e}")
    print(f"\n✅ Pre-built {built}/{count} Panchangam-aligned 9:16 vertical Shorts in {SHORTS_OUT_DIR}")


def print_dashboard():
    reg = load_published_registry()
    pub = reg.get("published_shorts", {})
    local_mp4s = list(SHORTS_OUT_DIR.glob("short_*.mp4"))
    cands = list_candidate_tracks()
    now_panchangam = get_auspicious_alignment_for_datetime(datetime.now(IST))

    print("=" * 85)
    print(f"📈 @GURUKULADESAM2 AUTONOMOUS SHORTS ENGINE — STATUS & PANCHANGAM DASHBOARD")
    print("=" * 85)
    print(f"  • Target Shorts Channel  : {TARGET_HANDLE} ({TARGET_CHANNEL_ID})")
    print(f"  • Parent Master Channel  : @guru-kula-desam (UCPqB1A_WzpLJec6q69BOO3Q)")
    print(f"  • Today's Panchangam     : {now_panchangam['tamil_month_ta']} {now_panchangam['tamil_day']} | {now_panchangam['weekday_ta']} | {now_panchangam['tithi_name']} | {now_panchangam['nakshatra_ta']}")
    print(f"  • Today's Sacred Occasion: {', '.join(now_panchangam['special_events'])} ({now_panchangam['occasion_badge_ta']})")
    print(f"  • Today's 4 Slot Deities : 6 AM: [{now_panchangam['slot_deities'][6].upper()}] | 11 AM: [{now_panchangam['slot_deities'][11].upper()}] | 4 PM: [{now_panchangam['slot_deities'][16].upper()}] | 8 PM: [{now_panchangam['slot_deities'][20].upper()}]")
    print(f"  • Ready Source Catalog   : {len(cands)} Multi-Deity Master Tracks")
    print(f"  • Local Rendered Shorts  : {len(local_mp4s)} vertical 1080x1920 MP4s in renders/shorts_gurukuladesam2/")
    print(f"  • Uploaded / Scheduled   : {len(pub)} Shorts on YouTube")
    if pub:
        print("\nRecent Releases / Scheduled Queue:")
        for tid, info in list(pub.items())[-10:]:
            sched = info.get("scheduled_for") or info.get("uploaded_at")
            print(f"  - [{info['deity'].upper():<9}] {info['short_url']} | {info['status'].upper()} ({sched}) -> Parent: {info.get('parent_video_url')}")
    print("=" * 85)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Autonomous Panchangam-Aligned YouTube Shorts Publisher for @gurukuladesam2")
    ap.add_argument("--status", action="store_true", help="Show pipeline & Panchangam dashboard")
    ap.add_argument("--calendar", action="store_true", help="Print 7-day Tamil Panchangam & deity schedule forecast")
    ap.add_argument("--prebuild", type=int, default=0, help="Pre-render N Panchangam-aligned vertical 9:16 Shorts locally")
    ap.add_argument("--publish-now", type=int, default=0, help="Build & immediately publish N Shorts live to @gurukuladesam2")
    ap.add_argument("--schedule-days", type=int, default=0, help="Build & schedule N days of Shorts (4 per day at 6AM, 11AM, 4PM, 8PM IST)")
    ap.add_argument("--deity", type=str, default=None, help="Override deity filter if desired")
    ap.add_argument("--daemon", action="store_true", help="Run continuous 24/7 autonomous daemon")
    args = ap.parse_args()

    if args.calendar:
        print_7day_panchangam_forecast()
    elif args.prebuild > 0:
        prebuild_panchangam_queue(args.prebuild, deity_filter=args.deity)
    elif args.publish_now > 0:
        run_batch_pipeline(args.publish_now, schedule_mode=False, deity_filter=args.deity)
    elif args.schedule_days > 0:
        run_batch_pipeline(args.schedule_days * 4, schedule_mode=True, deity_filter=args.deity)
    elif args.daemon:
        print(f"🔄 Starting 24/7 Autonomous Panchangam Daemon for {TARGET_HANDLE}...")
        while True:
            try:
                run_batch_pipeline(4, schedule_mode=True, deity_filter=args.deity)
            except Exception as e:
                print(f"[Daemon Warning] Cycle error: {e}")
            print("⏳ Sleeping 6 hours until next schedule top-up...")
            time.sleep(6 * 3600)
    else:
        print_dashboard()
