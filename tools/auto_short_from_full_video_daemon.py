#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/auto_short_from_full_video_daemon.py

Multi-Channel Autonomous Companion YouTube Short Generator & Scheduler.
Watches all 5 channels for newly posted full-length videos (> 75 seconds, non-live):
  1. @karmicgenie     (UCmixCKV4uTv3wIp634IRLXg) — Deep Sleep, ASMR & 432Hz Meditation
  2. @guru-kula-desam (UCPqB1A_WzpLJec6q69BOO3Q) — Flagship Thirukkural, Devotional & Meditative Films
  3. @gurukuladesam   (UCz4dzcjahGaIb5dZCv32AmA) — Virtuous / Thirukkural / Vallalar Channel
  4. @gurukuladesam2  (UCGUmNzaV_OUFbsNdHJQtaNQ) — Devotional / Panchangam Channel
  5. @influenzian     (UCcJFqC7z0f-ARNcJadKiKpQ) — Sports & Gaming Peak-Action Channel

Whenever a new full-length video is detected on a channel (that does not yet have a
companion Short in `production/shorts_metadata/companion_shorts_registry.json` or in
live channel descriptions):
  - Locates the source video from local master cache (or downloads the 35s–91s slice via `yt-dlp`).
  - Renders a 1080x1920 (9:16, 30fps, 56.0s) Vertical Short starting at 00:00:35
    (peak melody/action, 0s dead-air delay, smooth audio/video fades).
  - Schedules (`status.publishAt` at the next clean slot, or publishes immediately with `--publish-now`)
    the companion Short on that channel with a direct funnel link back to the full-length video!
"""

import os
import re
import sys
import glob
import json
import time
import argparse
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import google.oauth2.credentials
from google.auth.transport.requests import Request
import googleapiclient.discovery
import googleapiclient.http
from googleapiclient.errors import HttpError

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
CREDENTIALS_DIR = ROOT / "data" / "credentials"
REGISTRY_PATH = ROOT / "production" / "shorts_metadata" / "companion_shorts_registry.json"
WORK_DIR = ROOT / "renders" / "companion_shorts"
WORK_DIR.mkdir(parents=True, exist_ok=True)

IST = timezone(timedelta(hours=5, minutes=30))
DAILY_SLOTS_IST = [(6, 0), (11, 0), (16, 0), (20, 0)]

CHANNEL_CONFIGS = {
    "karmicgenie": {
        "handle": "@karmicgenie",
        "channel_id": "UCmixCKV4uTv3wIp634IRLXg",
        "token_paths": [
            CREDENTIALS_DIR / "tokens_karmicgenie" / "token_942198183044.json",
            CREDENTIALS_DIR / "tokens_karmicgenie" / "token_472322435541.json",
            CREDENTIALS_DIR / "token_karmicgenie.json",
        ],
        "niche": "sleep_asmr",
        "default_lang": "en",
    },
    "guru-kula-desam": {
        "handle": "@guru-kula-desam",
        "channel_id": "UCPqB1A_WzpLJec6q69BOO3Q",
        "token_paths": [
            CREDENTIALS_DIR / "token.json",
            CREDENTIALS_DIR / "tokens" / "token_472322435541.json",
        ],
        "niche": "devotional_meditative",
        "default_lang": "ta",
    },
    "gurukuladesam": {
        "handle": "@gurukuladesam",
        "channel_id": "UCz4dzcjahGaIb5dZCv32AmA",
        "token_paths": [
            CREDENTIALS_DIR / "token_gurukuladesam.json",
            CREDENTIALS_DIR / "tokens_gurukuladesam" / "token_472322435541.json",
        ],
        "niche": "virtuous_tamil",
        "default_lang": "ta",
    },
    "gurukuladesam2": {
        "handle": "@gurukuladesam2",
        "channel_id": "UCGUmNzaV_OUFbsNdHJQtaNQ",
        "token_paths": [
            CREDENTIALS_DIR / "token_gurukuladesam2.json",
            CREDENTIALS_DIR / "tokens_gurukuladesam2" / "token_839236964216.json",
            CREDENTIALS_DIR / "tokens_gurukuladesam2" / "token_472322435541.json",
        ],
        "niche": "devotional_tamil",
        "default_lang": "ta",
    },
    "influenzian": {
        "handle": "@influenzian",
        "channel_id": "UCcJFqC7z0f-ARNcJadKiKpQ",
        "token_paths": [
            CREDENTIALS_DIR / "token_influenzian.json",
            CREDENTIALS_DIR / "tokens_influenzian" / "token_942198183044.json",
        ],
        "niche": "sports_gaming",
        "default_lang": "en",
    },
}


def parse_iso8601_duration(dur_str: str) -> int:
    """Converts ISO 8601 duration (e.g. 'PT4M13S', 'PT3H1M5S') into total seconds."""
    if not dur_str:
        return 0
    m = re.match(r"^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$", dur_str)
    if not m:
        return 0
    h = int(m.group(1) or 0)
    mins = int(m.group(2) or 0)
    s = int(m.group(3) or 0)
    return h * 3600 + mins * 60 + s


def load_registry() -> dict:
    if REGISTRY_PATH.exists():
        try:
            return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"channels": {}}


def save_registry(reg: dict):
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")


def seed_registry_from_existing_records(reg: dict) -> dict:
    """Seeds the companion registry with the 30 Shorts already published for @karmicgenie and @guru-kula-desam."""
    kg_long_file = ROOT / "production" / "nanudaimai_instrumental" / "karmicgenie_publish_results.json"
    kg_short_file = ROOT / "production" / "nanudaimai_instrumental" / "karmicgenie_shorts_results.json"

    reg.setdefault("channels", {})
    kg_map = reg["channels"].setdefault("karmicgenie", {})
    gkd_map = reg["channels"].setdefault("guru-kula-desam", {})

    if kg_long_file.exists() and kg_short_file.exists():
        try:
            long_data = json.loads(kg_long_file.read_text(encoding="utf-8"))
            short_data = json.loads(kg_short_file.read_text(encoding="utf-8"))
            for key, s_info in short_data.items():
                if s_info.get("status") != "published":
                    continue
                l_info = long_data.get(key, {})
                full_vid_id = l_info.get("karmicgenie_video_id")
                if full_vid_id and full_vid_id not in kg_map:
                    kg_map[full_vid_id] = {
                        "full_video_id": full_vid_id,
                        "full_title": l_info.get("title", ""),
                        "short_video_id": s_info.get("short_video_id"),
                        "short_url": s_info.get("short_url"),
                        "short_title": s_info.get("short_title"),
                        "status": "published",
                        "published_at": s_info.get("published_at"),
                    }
        except Exception as e:
            print(f"  ℹ️ Note seeding karmicgenie records: {e}")

    save_registry(reg)
    return reg


def get_channel_client(channel_key: str):
    cfg = CHANNEL_CONFIGS[channel_key]
    target_cid = cfg["channel_id"]
    for tpath in cfg["token_paths"]:
        if not tpath.exists():
            continue
        try:
            data = json.loads(tpath.read_text(encoding="utf-8"))
            creds = google.oauth2.credentials.Credentials.from_authorized_user_info(data)
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                tpath.write_text(creds.to_json(), encoding="utf-8")
            yt = googleapiclient.discovery.build("youtube", "v3", credentials=creds, cache_discovery=False)
            ch = yt.channels().list(part="snippet,contentDetails", mine=True).execute()
            items = ch.get("items", [])
            if items and items[0]["id"] == target_cid:
                return yt, items[0]
        except Exception as e:
            print(f"  ⚠️ Token check failed for {tpath.name} ({channel_key}): {e}")
    return None, None


def compute_next_schedule_slot_utc(occupied_slots_ist: set) -> tuple[str, str]:
    """Finds the next open auspicious IST slot (6 AM, 11 AM, 4 PM, 8 PM IST) at least 45 minutes in the future."""
    now_ist = datetime.now(IST)
    for day_offset in range(0, 14):
        day = (now_ist + timedelta(days=day_offset)).date()
        for hr, mn in DAILY_SLOTS_IST:
            slot_ist = datetime(day.year, day.month, day.day, hr, mn, 0, tzinfo=IST)
            if slot_ist <= now_ist + timedelta(minutes=45):
                continue
            slot_key = slot_ist.strftime("%Y-%m-%dT%H:%M")
            if slot_key not in occupied_slots_ist:
                occupied_slots_ist.add(slot_key)
                slot_utc = slot_ist.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                return slot_utc, slot_ist.strftime("%Y-%m-%d %I:%M %p IST")
    fallback_ist = now_ist + timedelta(hours=2)
    return fallback_ist.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), fallback_ist.strftime("%Y-%m-%d %I:%M %p IST")


def download_or_slice_source_video(full_video_id: str, out_short_mp4: Path, start_sec: float = 35.0, duration_sec: float = 56.0) -> bool:
    """
    Downloads the 35s-95s section of `full_video_id` using yt-dlp (or full video fallback)
    and encodes a 9:16 Vertical Short (1080x1920 @ 30fps) with smooth audio/video fades.
    """
    if out_short_mp4.exists() and out_short_mp4.stat().st_size > 2 * 1024 * 1024:
        return True

    temp_src = WORK_DIR / f"temp_src_{full_video_id}.mp4"
    url = f"https://www.youtube.com/watch?v={full_video_id}"

    # Try downloading just the 30s-105s window via yt-dlp --download-sections
    dl_cmd = [
        "yt-dlp",
        "--no-playlist",
        "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
        "--download-sections", f"*{int(max(0, start_sec - 5))}-{int(start_sec + duration_sec + 10)}",
        "--merge-output-format", "mp4",
        "-o", str(temp_src),
        url,
    ]
    res = subprocess.run(dl_cmd, capture_output=True, text=True)
    used_section = True
    if res.returncode != 0 or not temp_src.exists():
        used_section = False
        dl_full_cmd = [
            "yt-dlp",
            "--no-playlist",
            "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
            "--merge-output-format", "mp4",
            "-o", str(temp_src),
            url,
        ]
        res2 = subprocess.run(dl_full_cmd, capture_output=True, text=True)
        if res2.returncode != 0 or not temp_src.exists():
            print(f"  ❌ yt-dlp could not download {url}: {res2.stderr[:200]}")
            return False

    ss_offset = "5.00" if used_section else f"{start_sec:.2f}"
    fade_out_st = duration_sec - 1.5
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-ss", ss_offset,
        "-t", f"{duration_sec:.2f}",
        "-i", str(temp_src),
        "-vf", f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920:(iw-1080)/2:(ih-1920)/2,fps=30,fade=t=in:st=0:d=0.4,fade=t=out:st={fade_out_st:.2f}:d=1.2",
        "-af", f"afade=t=in:st=0:d=0.4,afade=t=out:st={fade_out_st:.2f}:d=1.5",
        "-c:v", "libx264", "-preset", "veryfast", "-profile:v", "high", "-level:v", "4.1",
        "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
        "-movflags", "+faststart",
        str(out_short_mp4),
    ]
    subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
    if temp_src.exists():
        temp_src.unlink()
    return out_short_mp4.exists() and out_short_mp4.stat().st_size > 1024 * 1024


def build_companion_short_metadata(channel_key: str, full_vid_id: str, full_title: str, full_tags: list) -> tuple[str, str, list]:
    cfg = CHANNEL_CONFIGS[channel_key]
    full_url = f"https://youtube.com/watch?v={full_vid_id}"
    niche = cfg["niche"]

    clean_base = full_title.replace("#Shorts", "").replace("#shorts", "").strip()
    if "—" in clean_base:
        lead = clean_base.split("—")[0].strip()
    elif "|" in clean_base:
        lead = clean_base.split("|")[0].strip()
    else:
        lead = clean_base[:48].strip()

    if niche == "sleep_asmr" or ("sleep" in full_title.lower() or "asmr" in full_title.lower() or "432hz" in full_title.lower()):
        short_title = f"{lead[:42]} — 60s Deep Sleep & ASMR 432Hz Calm #Shorts"
        if len(short_title) > 100:
            short_title = f"{lead[:32]} — Deep Sleep & ASMR #Shorts"
        desc = f"""{short_title}

Take a 60-second deep breath and let this 432Hz meditative instrumental and organic ASMR nature soundscape quiet your mind and guide you into Deep Sleep.

🎧 Watch the Full-Length 1080p Deep Sleep & ASMR Soundscape here:
👉 {full_title}
🔗 {full_url}

🔔 Subscribe to {cfg['handle']} for daily Deep Sleep, ASMR & 432Hz Meditative Soundscapes!

#Shorts #DeepSleep #ASMR #SleepMusic #ASMRSleep #432Hz #MeditationMusic #InsomniaRelief #AnxietyRelief #StressRelief #RelaxingMusic #NatureSounds #Zen #Calm"""
        base_tags = [
            "shorts", "youtube shorts", "deep sleep", "asmr", "sleep music",
            "asmr sleep", "432hz sleep music", "insomnia relief", "anxiety relief",
            "stress relief", "meditation music", "relaxing music", "nature sounds",
        ]
    elif niche == "sports_gaming":
        short_title = f"{lead[:62]} — Peak Action Highlight #Shorts"[:100]
        desc = f"""{short_title}

🔥 Watch the Full Video here:
👉 {full_title}
🔗 {full_url}

🔔 Subscribe to {cfg['handle']} for daily high-energy Sports & Gaming highlights!

#Shorts #Sports #Highlights #ViralShorts #Trending #Influenzian"""
        base_tags = ["shorts", "youtube shorts", "sports highlights", "viral shorts", "influenzian"]
    else:
        short_title = f"{lead[:68]} | {cfg['handle']} #Shorts"[:100]
        desc = f"""{short_title}

🎬 முழுப் பாடல் / காணொளியைக் காண (Watch the Full Master Film here):
👉 {full_title}
🔗 {full_url}

🔔 Subscribe to {cfg['handle']} for daily sacred Tamil devotional & Thirukkural master films!

#Shorts #GuruKulaDesam #TamilDevotional #Thirukkural #MuruganSongs #SacredMusic #TamilShorts"""
        base_tags = ["shorts", "youtube shorts", "guru kula desam", "tamil devotional", "thirukkural", "murugan songs"]

    combined_tags = []
    seen = set()
    for t in base_tags + (full_tags or []):
        tc = t.strip()
        if not tc or tc.lower() in seen:
            continue
        seen.add(tc.lower())
        if sum(len(x) + 3 for x in combined_tags) + len(tc) <= 420:
            combined_tags.append(tc)

    return short_title, desc, combined_tags


def process_channel(channel_key: str, reg: dict, max_per_channel: int = 2, publish_now: bool = False, lookback: int = 25) -> int:
    cfg = CHANNEL_CONFIGS[channel_key]
    yt, ch_info = get_channel_client(channel_key)
    if not yt:
        print(f"⏩ [{cfg['handle']}] No active OAuth token available; skipping.")
        return 0

    uploads_playlist = ch_info["contentDetails"]["relatedPlaylists"]["uploads"]
    pl_items = yt.playlistItems().list(
        part="snippet,contentDetails", playlistId=uploads_playlist, maxResults=min(50, max(lookback, 30))
    ).execute().get("items", [])

    if not pl_items:
        print(f"ℹ️ [{cfg['handle']}] No uploads found on channel.")
        return 0

    vid_ids = [it["contentDetails"]["videoId"] for it in pl_items]
    vids_resp = yt.videos().list(
        part="snippet,contentDetails,status,liveStreamingDetails", id=",".join(vid_ids)
    ).execute().get("items", [])

    ch_reg = reg.setdefault("channels", {}).setdefault(channel_key, {})

    # 1. Collect all existing Shorts on the channel & occupied scheduled slots
    occupied_slots_ist = set()
    existing_linked_full_ids = set(ch_reg.keys())

    for v in vids_resp:
        vid_id = v["id"]
        dur_sec = parse_iso8601_duration(v.get("contentDetails", {}).get("duration", ""))
        title = v.get("snippet", {}).get("title", "")
        desc = v.get("snippet", {}).get("description", "")
        pub_at = v.get("status", {}).get("publishAt")
        if pub_at:
            try:
                dt_utc = datetime.fromisoformat(pub_at.replace("Z", "+00:00"))
                occupied_slots_ist.add(dt_utc.astimezone(IST).strftime("%Y-%m-%dT%H:%M"))
            except Exception:
                pass

        # If this video is already a Short, check if its description links to a full video ID
        if dur_sec <= 75 or "#shorts" in title.lower():
            for m in re.findall(r"(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})", desc):
                existing_linked_full_ids.add(m)

    # 2. Find full-length videos (> 75s, non-live, public) that don't have a companion Short yet
    candidates = []
    for v in vids_resp[:lookback]:
        vid_id = v["id"]
        if vid_id in existing_linked_full_ids:
            continue
        if "liveStreamingDetails" in v:
            continue
        status = v.get("status", {}).get("privacyStatus", "")
        if status != "public":
            continue
        dur_sec = parse_iso8601_duration(v.get("contentDetails", {}).get("duration", ""))
        title = v.get("snippet", {}).get("title", "")
        if dur_sec <= 75 or "#shorts" in title.lower():
            continue
        # Skip 3-hour compilations (> 45 mins) in cloud runner to avoid huge downloads
        if dur_sec > 2700:
            continue
        candidates.append((v, dur_sec))

    print(f"🔍 [{cfg['handle']}] Scanned {len(vids_resp)} recent uploads -> {len(candidates)} full-length video(s) needing a companion Short.")

    created_count = 0
    for v, dur_sec in candidates[:max_per_channel]:
        full_vid_id = v["id"]
        full_title = v["snippet"]["title"]
        full_tags = v["snippet"].get("tags", [])

        short_mp4 = WORK_DIR / f"{channel_key}_{full_vid_id}_Short_9x16.mp4"
        start_sec = 35.0 if dur_sec >= 95 else max(0.0, (dur_sec - 56.0) / 2.0)
        clip_dur = min(56.0, max(15.0, dur_sec - 2.0))

        print(f"  🎬 Building Companion Short for [{full_vid_id}] {full_title[:65]}...")
        ok = download_or_slice_source_video(full_vid_id, short_mp4, start_sec=start_sec, duration_sec=clip_dur)
        if not ok:
            continue

        short_title, short_desc, short_tags = build_companion_short_metadata(
            channel_key, full_vid_id, full_title, full_tags
        )

        if publish_now:
            status_body = {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            }
            sched_label = "PUBLIC IMMEDIATELY"
        else:
            slot_utc, slot_ist_label = compute_next_schedule_slot_utc(occupied_slots_ist)
            status_body = {
                "privacyStatus": "private",
                "publishAt": slot_utc,
                "selfDeclaredMadeForKids": False,
            }
            sched_label = f"SCHEDULED for {slot_ist_label} ({slot_utc})"

        body = {
            "snippet": {
                "title": short_title,
                "description": short_desc,
                "tags": short_tags,
                "categoryId": "10",
                "defaultLanguage": cfg["default_lang"],
                "defaultAudioLanguage": cfg["default_lang"],
            },
            "status": status_body,
        }

        try:
            media = googleapiclient.http.MediaFileUpload(
                str(short_mp4), mimetype="video/mp4", chunksize=10 * 1024 * 1024, resumable=True
            )
            req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
            resp = None
            while resp is None:
                _, resp = req.next_chunk()

            short_id = resp.get("id")
            short_url = f"https://youtube.com/shorts/{short_id}"
            print(f"  ✅ [{cfg['handle']}] Companion Short Uploaded ({sched_label}): {short_url}")

            ch_reg[full_vid_id] = {
                "full_video_id": full_vid_id,
                "full_title": full_title,
                "short_video_id": short_id,
                "short_url": short_url,
                "short_title": short_title,
                "schedule_mode": sched_label,
                "status": "published" if publish_now else "scheduled",
                "created_at": datetime.now(IST).isoformat(),
            }
            save_registry(reg)
            created_count += 1
        except HttpError as err:
            print(f"  ⚠️ YouTube API error on {cfg['handle']} ({full_vid_id}): {err}")
            break
        finally:
            if short_mp4.exists():
                short_mp4.unlink()

    return created_count


def main():
    parser = argparse.ArgumentParser(description="Multi-Channel Companion Short Auto-Scheduler")
    parser.add_argument("--channel", default="all", help="Channel key (karmicgenie, guru-kula-desam, gurukuladesam, gurukuladesam2, influenzian, or all)")
    parser.add_argument("--max-per-channel", type=int, default=2, help="Max companion Shorts to create per channel per run")
    parser.add_argument("--lookback", type=int, default=20, help="Number of recent uploads to inspect per channel")
    parser.add_argument("--publish-now", action="store_true", help="Publish immediately as Public instead of scheduling at next slot")
    args = parser.parse_args()

    reg = load_registry()
    reg = seed_registry_from_existing_records(reg)

    target_channels = (
        list(CHANNEL_CONFIGS.keys())
        if args.channel == "all"
        else [c.strip().lstrip("@").lower() for c in args.channel.split(",") if c.strip()]
    )

    total_created = 0
    for ch_key in target_channels:
        if ch_key not in CHANNEL_CONFIGS:
            print(f"⚠️ Unknown channel key: {ch_key}")
            continue
        total_created += process_channel(
            ch_key,
            reg,
            max_per_channel=args.max_per_channel,
            publish_now=args.publish_now,
            lookback=args.lookback,
        )

    print(f"\n✨ Multi-Channel Companion Short Run Complete. New Companion Shorts Scheduled/Published: {total_created}")


if __name__ == "__main__":
    main()
