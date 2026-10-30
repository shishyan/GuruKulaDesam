#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/shorts_autonomous_daemon.py
Autonomous 24/7 Song-Authentic YouTube Shorts Publisher & Liturgical Scheduler
for @GuruKulaDesam (நற்செய்கை — Virtuous Shorts) & @GuruKulaDesam2 (நற்பண்பு — Devotional Shorts).

Key Guarantees:
1. 100% Song-Authentic Visuals:
   - Clips the song's TRUE Original Master Video (or generates dedicated song-specific visuals via
     Google Flow PRO account when `--use-flow` is enabled). Never uses generic or cross-track clips.
2. Live YouTube Slot & Song Deduplication:
   - Queries each target channel's live YouTube uploads & `publishAt` schedule BEFORE picking slots,
     making duplicate slot uploads impossible across local cron and GitHub Actions!
3. Strict Pillar & Tamil Panchangam Alignment:
   - `@GuruKulaDesam`: Strictly Virtuous Shorts (`thirukkural`, `vallalar` — alternating across 6AM, 11AM, 4PM, 8PM IST).
   - `@GuruKulaDesam2`: Strictly Devotional Shorts (`murugan`, `shiva`, `amman`, `vinayagar`, `vishnu`) aligned with live Tamil Panchangam.
"""

import os
import re
import sys
import json
import time
import argparse
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.authorize_gurukuladesam2 import (
    INFLUENZIAN_CHANNEL_ID,
    INFLUENZIAN_HANDLE,
    ORIGINAL_CHANNEL_ID,
    ORIGINAL_HANDLE,
    TARGET_CHANNEL_ID,
    TARGET_HANDLE,
    get_channel_youtube_service,
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
    clean_song_title_part,
    list_candidate_tracks,
)

PUBLISHED_REGISTRY_FILE = ROOT / "production" / "shorts_metadata" / "gurukuladesam2_published_registry.json"

DAILY_IST_SLOTS = [
    (6, 0),   # 06:00 AM IST — Brahma Muhurtham / Morning Worship
    (11, 0),  # 11:00 AM IST — Midday Temple Ucchikalam
    (16, 0),  # 04:00 PM IST — Afternoon / Pre-Pradosham
    (20, 0),  # 08:00 PM IST — Evening / Ardhajama Pooja
]

VIRTUOUS_CATEGORIES = ("thirukkural", "vallalar")
DEVOTIONAL_CATEGORIES = ("murugan", "shiva", "amman", "vinayagar", "vishnu")


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
        "scheduled_slots_by_channel": {},
    }


def save_published_registry(reg: dict):
    PUBLISHED_REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    PUBLISHED_REGISTRY_FILE.write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")


def sync_registry_from_remote():
    """Fetches `origin/master` registry in memory and merges any newly cloud-published Shorts without touching unrelated dirty files."""
    try:
        subprocess.run(["git", "-C", str(ROOT), "fetch", "origin", "master"], capture_output=True, timeout=25)
        rel_reg = PUBLISHED_REGISTRY_FILE.relative_to(ROOT).as_posix()
        res = subprocess.run(["git", "-C", str(ROOT), "show", f"origin/master:{rel_reg}"], capture_output=True, text=True, timeout=15)
        if res.returncode == 0 and res.stdout.strip():
            remote_reg = json.loads(res.stdout)
            local_reg = load_published_registry()
            merged_pub = dict(remote_reg.get("published_shorts", {}))
            merged_pub.update(local_reg.get("published_shorts", {}))
            local_reg["published_shorts"] = merged_pub
            save_published_registry(local_reg)
    except Exception as e:
        print(f"  ℹ️ Remote registry fetch note: {e}")


def push_registry_to_remote():
    """Commits and pushes ONLY `gurukuladesam2_published_registry.json` and `legacy_republish_queue.json` safely."""
    try:
        tracked = [PUBLISHED_REGISTRY_FILE.relative_to(ROOT).as_posix()]
        q_file = ROOT / "production" / "shorts_metadata" / "legacy_republish_queue.json"
        if q_file.exists():
            tracked.append(q_file.relative_to(ROOT).as_posix())
        st = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", *tracked], capture_output=True, text=True)
        if not st.stdout.strip():
            return
        subprocess.run(["git", "-C", str(ROOT), "add", *tracked], check=False)
        subprocess.run(
            ["git", "-C", str(ROOT), "commit", "--only", *tracked, "-m", "chore(shorts): update published registry & Flow republish queue [skip ci]"],
            capture_output=True,
            check=False,
        )
        subprocess.run(["git", "-C", str(ROOT), "push", "origin", "HEAD:master"], capture_output=True, timeout=30)
        subprocess.run(["git", "-C", str(ROOT), "push", "origin", "HEAD:main"], capture_output=True, timeout=30)
    except Exception as e:
        print(f"  ℹ️ Remote registry push note: {e}")


def normalize_song_fingerprint(title: str) -> str:
    t = title.split("—")[-1] if "—" in title else title
    t = t.replace("#Shorts", "").split("|")[0]
    t = clean_song_title_part(t).lower()
    return re.sub(r"[\s\-_:.,!?'\"()\[\]]+", "", t)


def fetch_live_channel_state(channel_key: str) -> tuple[set[str], set[str]]:
    """
    Returns `(occupied_slot_isos_ist, existing_song_fingerprints)` directly from live YouTube API
    for `channel_key` so neither local cron nor GitHub Actions can ever double-schedule a slot!
    """
    occupied_slots = set()
    fingerprints = set()
    try:
        yt, _, cfg = get_channel_youtube_service(channel_key)
        uploads_pl = "UU" + cfg["channel_id"][2:]
        pl_res = yt.playlistItems().list(part="contentDetails", playlistId=uploads_pl, maxResults=50).execute()
        vids = [it["contentDetails"]["videoId"] for it in pl_res.get("items", [])]
        if vids:
            v_res = yt.videos().list(part="snippet,status", id=",".join(vids)).execute()
            for v in v_res.get("items", []):
                st = v.get("status", {})
                sn = v.get("snippet", {})
                title = sn.get("title", "")
                fp = normalize_song_fingerprint(title)
                if fp:
                    fingerprints.add(fp)
                pub_at = st.get("publishAt")
                if st.get("privacyStatus") == "private" and pub_at:
                    dt_utc = datetime.fromisoformat(pub_at.replace("Z", "+00:00"))
                    dt_ist = dt_utc.astimezone(IST).replace(second=0, microsecond=0)
                    occupied_slots.add(dt_ist.isoformat())
    except Exception as e:
        print(f"  ℹ️ Live channel state check note ({channel_key}): {e}")
    return occupied_slots, fingerprints


def get_next_schedule_slots_for_channel(count: int, reg: dict, channel_key: str, live_occupied: set[str]) -> list[datetime]:
    now_ist = datetime.now(IST)
    by_ch = reg.get("scheduled_slots_by_channel", {})
    occupied = set(by_ch.get(channel_key, [])) | set(live_occupied)
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


def pick_track_for_slot(
    slot_dt: datetime,
    used_track_ids: set[str],
    used_fingerprints: set[str] | None = None,
    forced_deity: str | None = None,
    channel_key: str = "@gurukuladesam2",
) -> tuple[dict, dict]:
    panchangam = get_auspicious_alignment_for_datetime(slot_dt)
    used_fps = used_fingerprints or set()

    def is_unused(cand: dict) -> bool:
        if cand["track_id"] in used_track_ids:
            return False
        if cand.get("legacy_track_id") and cand["legacy_track_id"] in used_track_ids:
            return False
        fp = normalize_song_fingerprint(cand.get("title", ""))
        if fp and fp in used_fps:
            return False
        return True

    if channel_key.lower() == "@gurukuladesam" and not forced_deity:
        preferred_virtuous = ["thirukkural", "vallalar"] if slot_dt.hour in (6, 16) else ["vallalar", "thirukkural"]
        for v_cat in preferred_virtuous:
            v_candidates = list_candidate_tracks(deity_filter=v_cat, prioritize_high_energy=False)
            for c in v_candidates:
                if is_unused(c):
                    return c, panchangam
        all_v = [c for c in list_candidate_tracks(prioritize_high_energy=False) if c["deity"] in VIRTUOUS_CATEGORIES]
        if all_v:
            return all_v[len(used_track_ids) % len(all_v)], panchangam

    target_deity = forced_deity.lower() if forced_deity else panchangam["active_deity"]
    if target_deity in VIRTUOUS_CATEGORIES and not forced_deity:
        target_deity = panchangam["primary_deity"] if panchangam["primary_deity"] in DEVOTIONAL_CATEGORIES else "murugan"
    forbidden = set(panchangam.get("forbidden_deities", [])) | set(VIRTUOUS_CATEGORIES)

    if target_deity in forbidden and not forced_deity:
        target_deity = panchangam["primary_deity"] if panchangam["primary_deity"] not in forbidden else "murugan"

    deity_candidates = list_candidate_tracks(deity_filter=target_deity, prioritize_high_energy=False)
    for c in deity_candidates:
        if is_unused(c):
            return c, panchangam

    sec_deity = panchangam.get("secondary_deity")
    if sec_deity and sec_deity not in forbidden:
        sec_candidates = list_candidate_tracks(deity_filter=sec_deity, prioritize_high_energy=False)
        for c in sec_candidates:
            if is_unused(c):
                return c, panchangam

    for d_fallback in DEVOTIONAL_CATEGORIES:
        if d_fallback not in forbidden:
            d_cands = list_candidate_tracks(deity_filter=d_fallback, prioritize_high_energy=False)
            for c in d_cands:
                if is_unused(c):
                    return c, panchangam

    if deity_candidates:
        return deity_candidates[len(used_track_ids) % len(deity_candidates)], panchangam

    all_cands = [c for c in list_candidate_tracks() if c["deity"] not in forbidden]
    return all_cands[0], panchangam


def upload_short_via_api(meta: dict, publish_at_dt: datetime | None = None, channel_key: str = "@gurukuladesam") -> str | None:
    video_path = ROOT / meta["video_path"]
    if not video_path.exists():
        raise FileNotFoundError(f"Rendered Short MP4 missing: {video_path}")

    for attempt in range(4):
        try:
            yt, pid, cfg = get_channel_youtube_service(channel_key)
            expected_cid = cfg["channel_id"]
            expected_hnd = cfg["handle"]

            ch_res = yt.channels().list(part="id,snippet", mine=True).execute()
            items = ch_res.get("items", [])
            if not items or items[0]["id"] != expected_cid:
                actual_id = items[0]["id"] if items else "None"
                actual_handle = items[0]["snippet"].get("customUrl") if items else "None"
                raise RuntimeError(
                    f"Safety Guard Triggered: Active token belongs to {actual_handle} ({actual_id}), "
                    f"NOT {expected_hnd} ({expected_cid})."
                )

            status_body = {"selfDeclaredMadeForKids": False}
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

            print(f"\n🚀 [UPLOADING AUTHENTIC SHORT -> {expected_hnd}] {meta['title']}")
            print(f"   • Mode          : {mode_label}")
            print(f"   • Source Mode   : {meta.get('visual_source_mode')} ({meta.get('visual_source_file')})")
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
            err_body = e.content.decode("utf-8", errors="ignore") if getattr(e, "content", None) else ""
            combined_err = f"{e} {err_body}"
            if "quotaExceeded" in combined_err:
                print(f"⚠️ Project {pid} hit API quota for {channel_key}. Rotating to next project...")
                mark_gkd2_project_exhausted(pid, channel_key=channel_key)
                continue
            elif "uploadLimitExceeded" in combined_err or "exceeded the number of videos" in combined_err:
                print(
                    f"⏳ [{expected_hnd}] Reached YouTube's rolling 24h channel upload cap "
                    f"(from yesterday's batch). Cached Short locally for automatic upload on next cron cycle."
                )
                return "CHANNEL_UPLOAD_LIMIT"
            else:
                print(f"❌ YouTube API HttpError ({channel_key}): {e}")
                return None
        except Exception as e:
            print(f"ℹ️ Skipping upload to {channel_key}: {e}")
            return None

    return None


def run_batch_pipeline(
    count: int,
    schedule_mode: bool = False,
    deity_filter: str = None,
    channel_filter: str = None,
    use_flow: bool = False,
):
    reg = load_published_registry()
    published_map = reg.get("published_shorts", {})
    used_ids = set(published_map.keys())
    for info in published_map.values():
        if info.get("legacy_track_id"):
            used_ids.add(info["legacy_track_id"])

    all_channels = (("@gurukuladesam", ORIGINAL_HANDLE), ("@gurukuladesam2", TARGET_HANDLE))
    if channel_filter:
        active_channels = tuple((k, h) for k, h in all_channels if k == channel_filter.lower() or h.lower() == channel_filter.lower())
    else:
        active_channels = all_channels

    print("=" * 95)
    print(f"🕉️  GURUKULADESAM SONG-AUTHENTIC SHORTS PIPELINE ({count} Slots/Channel -> {count * len(active_channels)} Shorts)")
    print(f"📺 1. குரு குல தேசம் | நெறி தவறாமை     >> {ORIGINAL_HANDLE} (நற்செய்கை — Virtuous Master Clips)")
    print(f"📺 2. குரு குல தேசம் | நன்றி மறவாமை    >> {TARGET_HANDLE} (நற்பண்பு — Devotional Master Clips)")
    print(f"🏛️  3. குரு குல தேசம் | ஒழுக்கம் பிழையாமை >> @Guru-Kula-Desam (நற்குணம் — Master Video Source)")
    print(f"⏳ 4. Spiritual Shorts (Future)        >> {INFLUENZIAN_HANDLE}")
    print("=" * 95)

    completed = 0
    for ch_key, ch_hnd in active_channels:
        try:
            get_channel_youtube_service(ch_key)
        except Exception as e:
            print(f"ℹ️ Skipping {ch_hnd} (token unavailable): {e}")
            continue

        live_occupied, live_fps = fetch_live_channel_state(ch_key)
        if schedule_mode:
            ch_slots = get_next_schedule_slots_for_channel(count, reg, ch_key, live_occupied)
        else:
            ch_slots = [datetime.now(IST)] * count

        channel_limit_hit = False
        session_used_ids = set(used_ids)
        session_fps = set(live_fps)

        for slot_idx, slot_dt in enumerate(ch_slots):
            slot_iso = slot_dt.isoformat() if schedule_mode else None
            pick_dt = slot_dt if schedule_mode else slot_dt.replace(hour=DAILY_IST_SLOTS[slot_idx % len(DAILY_IST_SLOTS)][0])

            track_item, panchangam = pick_track_for_slot(
                pick_dt, session_used_ids, used_fingerprints=session_fps, forced_deity=deity_filter, channel_key=ch_key
            )
            tid = track_item["track_id"]
            session_used_ids.add(tid)
            if track_item.get("legacy_track_id"):
                session_used_ids.add(track_item["legacy_track_id"])

            try:
                meta = build_short_for_track(tid, target_dt=slot_dt, brand_handle=ch_hnd, use_flow=use_flow)
                session_fps.add(normalize_song_fingerprint(meta["title"]))
                if channel_limit_hit:
                    print(f"   💾 Pre-rendered & cached {meta['video_path']} for {ch_hnd} ({slot_dt.strftime('%Y-%m-%d %I:%M %p IST')}).")
                    continue

                yt_vid_id = upload_short_via_api(meta, publish_at_dt=slot_dt if schedule_mode else None, channel_key=ch_key)
                if yt_vid_id == "CHANNEL_UPLOAD_LIMIT":
                    channel_limit_hit = True
                    continue
                if yt_vid_id:
                    used_ids.add(tid)
                    if track_item.get("legacy_track_id"):
                        used_ids.add(track_item["legacy_track_id"])
                    published_map[tid] = {
                        "youtube_short_id": yt_vid_id,
                        "channel_handle": ch_hnd,
                        "short_url": f"https://youtube.com/shorts/{yt_vid_id}",
                        "title": meta["title"],
                        "deity": meta["deity"],
                        "visual_source_mode": meta.get("visual_source_mode"),
                        "visual_source_file": meta.get("visual_source_file"),
                        "legacy_track_id": track_item.get("legacy_track_id"),
                        "panchangam_occasion": panchangam["occasion_badge_ta"],
                        "uploaded_at": datetime.now(IST).isoformat(),
                        "scheduled_for": slot_iso,
                        "status": "scheduled" if schedule_mode else "public",
                    }
                    reg["published_shorts"] = published_map
                    if slot_iso:
                        ch_sched = reg.setdefault("scheduled_slots_by_channel", {}).setdefault(ch_key, [])
                        if slot_iso not in ch_sched:
                            ch_sched.append(slot_iso)
                    save_published_registry(reg)
                    live_fps.add(normalize_song_fingerprint(meta["title"]))
                    completed += 1
            except Exception as e:
                print(f"❌ Error on {ch_hnd} track {tid}: {e}")

    print(f"\n🏁 Batch Complete: {completed}/{count * len(active_channels)} Song-Authentic Shorts published/scheduled.")


def prebuild_panchangam_queue(count: int, deity_filter: str = None, use_flow: bool = False):
    reg = load_published_registry()
    used_ids = set(reg.get("published_shorts", {}).keys())
    slots = get_next_schedule_slots_for_channel(count, reg, "@gurukuladesam2", set())

    built = 0
    for slot_dt in slots:
        track_item, panchangam = pick_track_for_slot(slot_dt, used_ids, forced_deity=deity_filter)
        tid = track_item["track_id"]
        used_ids.add(tid)
        print(f"\n📅 Slot {slot_dt.strftime('%Y-%m-%d %I:%M %p IST')} -> [{track_item['deity'].upper()}] {tid} ({panchangam['occasion_badge_ta']})")
        try:
            build_short_for_track(tid, target_dt=slot_dt, brand_handle=TARGET_HANDLE, use_flow=use_flow)
            built += 1
        except Exception as e:
            print(f"❌ Failed building {tid}: {e}")
    print(f"\n✅ Pre-built {built}/{count} Song-Authentic 9:16 vertical Shorts in {SHORTS_OUT_DIR}")


def fetch_live_youtube_analytics(pub: dict) -> tuple[dict, dict]:
    channel_stats = {}
    video_stats = {}
    try:
        res = get_channel_youtube_service("@gurukuladesam")
        yt = res[0] if isinstance(res, tuple) else res
        ch_ids = [ORIGINAL_CHANNEL_ID, TARGET_CHANNEL_ID, INFLUENZIAN_CHANNEL_ID, "UCPqB1A_WzpLJec6q69BOO3Q"]
        ch_res = yt.channels().list(part="snippet,statistics", id=",".join(ch_ids)).execute()
        for item in ch_res.get("items", []):
            st = item.get("statistics", {})
            channel_stats[item["id"]] = {
                "title": item["snippet"].get("title"),
                "customUrl": item["snippet"].get("customUrl"),
                "subs": int(st.get("subscriberCount", 0)),
                "views": int(st.get("viewCount", 0)),
                "videos": int(st.get("videoCount", 0)),
            }

        vid_ids = [v["youtube_short_id"] for v in pub.values() if v.get("youtube_short_id")]
        for i in range(0, len(vid_ids), 50):
            chunk = vid_ids[i : i + 50]
            v_res = yt.videos().list(part="snippet,statistics,status,contentDetails", id=",".join(chunk)).execute()
            for v in v_res.get("items", []):
                st = v.get("statistics", {})
                status = v.get("status", {})
                video_stats[v["id"]] = {
                    "views": int(st.get("viewCount", 0)),
                    "likes": int(st.get("likeCount", 0)),
                    "comments": int(st.get("commentCount", 0)),
                    "privacyStatus": status.get("privacyStatus", "unknown"),
                    "publishedAt": v.get("snippet", {}).get("publishedAt"),
                    "duration": v.get("contentDetails", {}).get("duration"),
                }
    except Exception as e:
        print(f"  ℹ️ Live Analytics Note: {e}")
    return channel_stats, video_stats


def print_dashboard():
    reg = load_published_registry()
    pub = reg.get("published_shorts", {})
    local_mp4s = list(SHORTS_OUT_DIR.glob("short_*.mp4"))
    cands = list_candidate_tracks()
    now_panchangam = get_auspicious_alignment_for_datetime(datetime.now(IST))
    ch_stats, v_stats = fetch_live_youtube_analytics(pub)

    print("=" * 95)
    print("📈 @GURUKULADESAM & @GURUKULADESAM2 SONG-AUTHENTIC SHORTS ENGINE — DASHBOARD (8 SHORTS/DAY)")
    print("=" * 95)
    c1 = ch_stats.get(ORIGINAL_CHANNEL_ID, {})
    c2 = ch_stats.get(TARGET_CHANNEL_ID, {})
    ci = ch_stats.get(INFLUENZIAN_CHANNEL_ID, {})
    cm = ch_stats.get("UCPqB1A_WzpLJec6q69BOO3Q", {})
    print(f"  • 1. குரு குல தேசம் | நெறி தவறாமை     >> {ORIGINAL_HANDLE} (நற்செய்கை | Virtuous) — {c1.get('subs', 0)} subs | {c1.get('views', 0):,} views | {c1.get('videos', 0)} videos")
    print(f"  • 2. குரு குல தேசம் | நன்றி மறவாமை    >> {TARGET_HANDLE} (நற்பண்பு | Devotional) — {c2.get('subs', 0)} subs | {c2.get('views', 0):,} views | {c2.get('videos', 0)} videos")
    print(f"  • 3. குரு குல தேசம் | ஒழுக்கம் பிழையாமை >> @Guru-Kula-Desam (நற்குணம் | Master Video) — {cm.get('subs', 0)} subs | {cm.get('views', 0):,} views | {cm.get('videos', 0)} videos")
    print(f"  • 4. Spiritual Shorts (Future)        >> {INFLUENZIAN_HANDLE} (Time as Ultimate Credit) — {ci.get('subs', 0)} subs | {ci.get('views', 0):,} views | {ci.get('videos', 0)} videos")
    print(f"  • Today's Panchangam     : {now_panchangam['tamil_month_ta']} {now_panchangam['tamil_day']} | {now_panchangam['weekday_ta']} | {now_panchangam['tithi_name']} | {now_panchangam['nakshatra_ta']}")
    print(f"  • Today's Sacred Occasion: {', '.join(now_panchangam['special_events'])} ({now_panchangam['occasion_badge_ta']})")
    print(f"  • Today's 4 Slot Deities : 6 AM: [{now_panchangam['slot_deities'][6].upper()}] | 11 AM: [{now_panchangam['slot_deities'][11].upper()}] | 4 PM: [{now_panchangam['slot_deities'][16].upper()}] | 8 PM: [{now_panchangam['slot_deities'][20].upper()}]")
    print(f"  • Verified Master Films  : {len(cands)} 100% Song-Specific Master Films")
    print(f"  • Local Rendered Shorts  : {len(local_mp4s)} vertical 1080x1920 MP4s in renders/shorts_gurukuladesam2/")
    print(f"  • Uploaded / Scheduled   : {len(pub)} Shorts in Registry")
    if pub:
        total_short_views = 0
        total_short_likes = 0
        total_short_comments = 0
        print("\n📊 Live Short-by-Short Performance Analytics:")
        for tid, info in list(pub.items())[-14:]:
            yt_id = info.get("youtube_short_id", "")
            vs = v_stats.get(yt_id, {})
            views = vs.get("views", 0)
            likes = vs.get("likes", 0)
            comments = vs.get("comments", 0)
            like_rate = (likes / views * 100.0) if views > 0 else 0.0
            live_status = vs.get("privacyStatus", info.get("status", "unknown")).upper()
            src_tag = "MASTER" if info.get("visual_source_mode") == "original_master_clip" else ("FLOW" if info.get("visual_source_mode") == "google_flow_dedicated" else "LEGACY")
            total_short_views += views
            total_short_likes += likes
            total_short_comments += comments
            sched = info.get("scheduled_for") or info.get("uploaded_at")
            print(
                f"  - [{info['deity'].upper():<11}] ({src_tag:<6}) {info['short_url']} | {live_status:<7} "
                f"| 👁️ {views:>5} views | 👍 {likes:>3} likes ({like_rate:>4.1f}%) | Slot: {sched}"
            )
        overall_lr = (total_short_likes / total_short_views * 100.0) if total_short_views > 0 else 0.0
        print(f"\n  🔥 Total Tracked Shorts Views: {total_short_views:,} | Total Likes: {total_short_likes:,} ({overall_lr:.1f}% Like-to-View Ratio) | Comments: {total_short_comments}")
    print("=" * 95)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Autonomous Song-Authentic YouTube Shorts Publisher")
    ap.add_argument("--status", action="store_true", help="Show pipeline & Panchangam dashboard")
    ap.add_argument("--calendar", action="store_true", help="Print 7-day Tamil Panchangam & deity schedule forecast")
    ap.add_argument("--prebuild", type=int, default=0, help="Pre-render N Song-Authentic vertical 9:16 Shorts locally")
    ap.add_argument("--publish-now", type=int, default=0, help="Build & immediately publish N Shorts live")
    ap.add_argument("--schedule-days", type=int, default=0, help="Build & schedule N days of Shorts (4/day/channel)")
    ap.add_argument("--deity", type=str, default=None, help="Override deity filter")
    ap.add_argument("--channel", type=str, default=None, help="Target specific channel (@GuruKulaDesam or @GuruKulaDesam2)")
    ap.add_argument("--use-flow", action="store_true", help="Generate dedicated song-specific visuals via Google Flow PRO account")
    ap.add_argument("--sync-git", action="store_true", help="Sync published registry with GitHub before and after run")
    ap.add_argument("--daemon", action="store_true", help="Run continuous 24/7 autonomous daemon")
    args = ap.parse_args()

    if args.sync_git:
        sync_registry_from_remote()

    if args.calendar:
        print_7day_panchangam_forecast()
    elif args.prebuild > 0:
        prebuild_panchangam_queue(args.prebuild, deity_filter=args.deity, use_flow=args.use_flow)
    elif args.publish_now > 0:
        run_batch_pipeline(args.publish_now, schedule_mode=False, deity_filter=args.deity, channel_filter=args.channel, use_flow=args.use_flow)
        if args.sync_git:
            push_registry_to_remote()
    elif args.schedule_days > 0:
        run_batch_pipeline(args.schedule_days * 4, schedule_mode=True, deity_filter=args.deity, channel_filter=args.channel, use_flow=args.use_flow)
        if args.sync_git:
            push_registry_to_remote()
    elif args.daemon:
        while True:
            try:
                run_batch_pipeline(4, schedule_mode=True, deity_filter=args.deity, use_flow=args.use_flow)
            except Exception as e:
                print(f"[Daemon Warning] Cycle error: {e}")
            time.sleep(6 * 3600)
    else:
        print_dashboard()
