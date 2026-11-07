#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/gkd_jukebox_and_live_broadcaster.py
=========================================
Guru Kula Desam: Zero-Render 1-Hour Jukebox Builder & 24/7 YouTube Live Radio Engine

Intercepts the Top Global YouTube Search Clusters:
  • Cluster #3: Music Mix / Jukebox / Relaxing & Temple Music (3.1M searches/day)
  • Cluster #8: 24/7 Live Stream / Non-Stop Bhakti Radio (1.5M searches/day)
  • Cluster #10: Songs with Synchronized Lyrics / Paarayanam (1.3M searches/day)
  • Cluster #25: Meditation / Brahma Muhurtham / Deep Peace (600K searches/day)

Capabilities:
  1. `--list`: Audits all 287 Master Films in `master_film_sources.json` by deity/category,
     duration, and local/Drive availability.
  2. `--build-jukebox --deity <deity> --minutes 60`: Zero-render lossless concatenation
     (`ffmpeg -f concat -safe 0 -c copy`) of 1080p Master Films into a 1-Hour+ Mega-Mix MP4,
     plus automatic YouTube Chapter Timestamps (`00:00`, `04:32`, ...) & SEO metadata JSON.
  3. `--create-live --deity <deity>`: Uses YouTube Live Streaming API (`liveBroadcasts` +
     `liveStreams`) to provision a 24/7 Live Broadcast and print the exact RTMP Ingestion URL
     & Stream Key.
  4. `--start-radio --deity <deity> --stream-key <KEY>`: Launches an infinite, zero-GPU
     24/7 `ffmpeg -stream_loop -1 -c copy -f flv` RTMP radio broadcast to YouTube Live.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parent.parent
MASTER_SOURCES_PATH = ROOT / "production" / "shorts_metadata" / "master_film_sources.json"
JUKEBOX_OUT_DIR = Path("/home/shishyan/GuruKulaDesam_Local/jukeboxes")
JUKEBOX_OUT_DIR.mkdir(parents=True, exist_ok=True)

DEITY_JUKEBOX_THEMES = {
    "murugan": {
        "title": "🕉️ முருகன் திருப்புகழ் & கந்தர் அனுபூதி 1 மணி நேர இசைத் தொகுப்பு | Non-Stop Lord Murugan Songs Jukebox 1080p",
        "live_title": "🔴 LIVE 24/7: முருகன் திருப்புகழ் & கந்தர் அனுபூதி இடைவிடாத தெய்வீக இசை | Lord Murugan Bhakti Radio",
        "cluster_hooks": "Lord Murugan Devotional Songs | Thiruppugazh With Lyrics | Morning Pooja Music | Sashti & Krittika Special",
        "tags": [
            "முருகன் பாடல்கள்", "திருப்புகழ்", "கந்தர் அனுபூதி", "Murugan Songs",
            "Thiruppugazh Jukebox", "Lord Murugan Non Stop Songs", "Tamil Devotional Songs",
            "Morning Pooja Songs Tamil", "Murugan Songs With Lyrics", "Guru Kula Desam",
        ],
    },
    "shiva": {
        "title": "🕉️ சிவபெருமான் தேவாரம், திருவாசகம் & திருமந்திரம் 1 மணி நேர இசை | Non-Stop Lord Shiva Songs Jukebox 1080p",
        "live_title": "🔴 LIVE 24/7: சிவபெருமான் தேவாரம், திருவாசகம் & நமச்சிவாய தியான இசை | Non-Stop Shiva Meditation Radio",
        "cluster_hooks": "Lord Shiva Devotional Songs | Thiruvasagam & Thevaram With Lyrics | Pradosham & Meditation Music",
        "tags": [
            "சிவன் பாடல்கள்", "திருவாசகம்", "தேவாரம்", "திருமந்திரம்", "Shiva Songs Tamil",
            "Thiruvasagam Jukebox", "Om Namah Shivaya Meditation", "Pradosham Songs",
            "Tamil Devotional Jukebox", "Guru Kula Desam",
        ],
    },
    "vallalar": {
        "title": "🔥 வள்ளலார் திருவருட்பா அருட்பெருஞ்சோதி 1 மணி நேர தியான இசை | Vallalar Thiruvarutpa Meditation Jukebox",
        "live_title": "🔴 LIVE 24/7: அருட்பெருஞ்சோதி வள்ளலார் திருவருட்பா ஆழ்ந்த அமைதி & தியான இசை | Deep Peace & Sleep Radio",
        "cluster_hooks": "Vallalar Thiruvarutpa Songs | Arutperunjothi Meditation & Sleep Music | Deep Peace Temple Ambience",
        "tags": [
            "வள்ளலார் பாடல்கள்", "திருவருட்பா", "அருட்பெருஞ்சோதி", "Vallalar Songs",
            "Thiruvarutpa Jukebox", "Tamil Meditation Music", "Relaxing Spiritual Music",
            "Sanmargam", "Guru Kula Desam",
        ],
    },
    "thirukkural": {
        "title": "📖 திருக்குறள் இன்னிசைக் காவியம் 1 மணி நேர மெகா தொகுப்பு (வரிகளுடன்) | Non-Stop Thirukkural Songs With Lyrics",
        "live_title": "🔴 LIVE 24/7: திருக்குறள் 1330 இன்னிசைக் காவியம் & நன்னெறி இசை | Non-Stop Thirukkural Wisdom & Study Radio",
        "cluster_hooks": "Thirukkural Songs With Synchronized Tamil Lyrics | Study & Focus Music | Ancient Tamil Wisdom",
        "tags": [
            "திருக்குறள்", "திருக்குறள் பாடல்கள்", "Thirukkural Songs", "Thirukkural With Lyrics",
            "Thiruvalluvar", "Tamil Wisdom Songs", "Tamil Literature Music", "Guru Kula Desam",
        ],
    },
    "vinayagar": {
        "title": "🐘 விநாயகர் அகவல் & நான்மணிமாலை 1 மணி நேர காலை வழிபாட்டு இசை | Non-Stop Vinayagar Devotional Jukebox",
        "live_title": "🔴 LIVE 24/7: விநாயகர் காலை வழிபாட்டுப் பாடல்கள் & மங்கள இசை | Morning Pooja Vinayagar Radio",
        "cluster_hooks": "Vinayagar Morning Pooja Songs | Vinayagar Agaval With Lyrics | Auspicious Tamil Bhakti Music",
        "tags": [
            "விநாயகர் பாடல்கள்", "விநாயகர் அகவல்", "Vinayagar Songs Tamil", "Morning Pooja Songs",
            "Pillaiyar Devotional Songs", "Ganesha Bhakti Jukebox", "Guru Kula Desam",
        ],
    },
    "amman": {
        "title": "🔱 அபிராமி அந்தாதி & அம்மன் பக்திப் பாடல்கள் 1 மணி நேர தொகுப்பு | Non-Stop Amman Songs Jukebox",
        "live_title": "🔴 LIVE 24/7: அபிராமி அந்தாதி, மகாலக்ஷ்மி & அம்மன் அருள் இசை | Non-Stop Goddess Amman Bhakti Radio",
        "cluster_hooks": "Abhirami Anthadhi With Lyrics | Friday Amman Pooja Songs | Mahalakshmi & Saraswathi Devotional Jukebox",
        "tags": [
            "அபிராமி அந்தாதி", "அம்மன் பாடல்கள்", "Abhirami Anthadhi", "Amman Songs Tamil",
            "Friday Pooja Songs", "Mahalakshmi Songs Tamil", "Guru Kula Desam",
        ],
    },
    "vishnu": {
        "title": "🙏 திருப்பாவை & பெருமாள் திவ்ய பிரபந்தம் 1 மணி நேர இசைத் தொகுப்பு | Non-Stop Perumal Songs Jukebox",
        "live_title": "🔴 LIVE 24/7: ஆண்டாள் திருப்பாவை & பெருமாள் மங்கள இசை | Non-Stop Lord Perumal Devotional Radio",
        "cluster_hooks": "Andal Thiruppavai With Lyrics | Perumal Morning Suprabhatam & Divya Prabandham Jukebox",
        "tags": [
            "திருப்பாவை", "பெருமாள் பாடல்கள்", "Thiruppavai Songs", "Perumal Songs Tamil",
            "Andal Thiruppavai", "Divya Prabandham", "Morning Bhakti Songs", "Guru Kula Desam",
        ],
    },
}


def format_timestamp(seconds: float) -> str:
    s = int(round(seconds))
    hrs = s // 3600
    mins = (s % 3600) // 60
    secs = s % 60
    if hrs > 0:
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"


def load_master_catalog() -> dict:
    if not MASTER_SOURCES_PATH.exists():
        raise FileNotFoundError(f"Master film catalog missing: {MASTER_SOURCES_PATH}")
    return json.loads(MASTER_SOURCES_PATH.read_text(encoding="utf-8"))


def get_tracks_for_deity(deity: str, require_local: bool = True) -> list[dict]:
    catalog = load_master_catalog()
    tracks = []
    for fid, info in catalog.items():
        if deity != "all" and info.get("deity", "").lower() != deity.lower():
            continue
        vid_path = info.get("local_layered_video") or info.get("local_clean_video")
        if require_local and (not vid_path or not os.path.exists(vid_path)):
            continue
        tracks.append({
            "film_id": fid,
            "title": info.get("title", fid),
            "deity": info.get("deity", "devotional"),
            "duration_sec": int(info.get("duration_sec") or 240),
            "views": int(info.get("views") or 0),
            "video_path": vid_path,
            "youtube_url": info.get("youtube_url", f"https://www.youtube.com/watch?v={fid}"),
        })
    # Sort by views descending so the strongest viral hooks play first in every Jukebox!
    tracks.sort(key=lambda x: x["views"], reverse=True)
    return tracks


def audit_catalog():
    catalog = load_master_catalog()
    print("=" * 95)
    print("🎵 GURU KULA DESAM — JUKEBOX & 24/7 LIVE STREAM CATALOG READINESS AUDIT")
    print("=" * 95)
    for deity in DEITY_JUKEBOX_THEMES:
        all_t = get_tracks_for_deity(deity, require_local=False)
        loc_t = get_tracks_for_deity(deity, require_local=True)
        tot_min = sum(t["duration_sec"] for t in all_t) / 60.0
        loc_min = sum(t["duration_sec"] for t in loc_t) / 60.0
        print(
            f"  • {deity.upper():<12} | {len(all_t):>3} Master Films ({tot_min:>5.1f} mins total) | "
            f"Mounted Ready Now: {len(loc_t):>3} films ({loc_min:>5.1f} mins)"
        )
    print("=" * 95)


def build_jukebox(deity: str, target_minutes: int = 60, dry_run: bool = False) -> dict:
    tracks = get_tracks_for_deity(deity, require_local=True)
    if not tracks:
        raise RuntimeError(f"No locally accessible MP4 files found for deity '{deity}'.")

    target_sec = target_minutes * 60
    selected = []
    accum_sec = 0

    # Loop through sorted tracks until target_minutes is reached
    idx = 0
    while accum_sec < target_sec and len(selected) < 40:
        t = tracks[idx % len(tracks)]
        selected.append(t)
        accum_sec += t["duration_sec"]
        idx += 1
        if idx >= len(tracks) and accum_sec >= target_sec * 0.7:
            break

    theme = DEITY_JUKEBOX_THEMES.get(deity.lower(), DEITY_JUKEBOX_THEMES["murugan"])
    concat_file = JUKEBOX_OUT_DIR / f"concat_{deity}_{target_minutes}m.txt"
    out_mp4 = JUKEBOX_OUT_DIR / f"GKD_Jukebox_{deity.capitalize()}_{target_minutes}Min_1080p.mp4"
    meta_json = JUKEBOX_OUT_DIR / f"GKD_Jukebox_{deity.capitalize()}_{target_minutes}Min_metadata.json"

    chapters = []
    concat_lines = []
    cursor_sec = 0.0

    for i, t in enumerate(selected, 1):
        ts_str = format_timestamp(cursor_sec)
        clean_title = t["title"].split("|")[0].strip()
        chapters.append(f"{ts_str} - {i:02d}. {clean_title}")
        escaped_path = str(t["video_path"]).replace("'", "'\\''")
        concat_lines.append(f"file '{escaped_path}'")
        cursor_sec += t["duration_sec"]

    concat_file.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")

    description = (
        f"{theme['title']}\n"
        f"Guru Kula Desam (@guru-kula-desam)\n\n"
        f"🎧 {theme['cluster_hooks']}\n\n"
        f"⏱️ CHAPTER TIMESTAMPS (NON-STOP JUKEBOX):\n"
        + "\n".join(chapters)
        + "\n\n🔔 Subscribe to Guru Kula Desam (@guru-kula-desam) for daily Tamil Devotional Symphonies, "
        "1330 Thirukkural Master Films & 24/7 Sacred Radio!\n"
        "#GuruKulaDesam #TamilDevotional #Jukebox #TamilSongsWithLyrics #MorningPoojaSongs"
    )

    meta_payload = {
        "deity": deity,
        "title": theme["title"],
        "live_title": theme["live_title"],
        "total_tracks": len(selected),
        "estimated_duration_minutes": round(cursor_sec / 60.0, 1),
        "concat_list_path": str(concat_file),
        "output_mp4_path": str(out_mp4),
        "description": description,
        "tags": theme["tags"],
        "chapters": chapters,
    }
    meta_json.write_text(json.dumps(meta_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ Jukebox Manifest & Chapter Timestamps Ready: {meta_json}")
    print(f"   • Tracks Included : {len(selected)} Master Films (~{cursor_sec / 60.0:.1f} mins)")
    print(f"   • Concat List     : {concat_file}")

    if not dry_run:
        print(f"🚀 Running Zero-Render Lossless FFmpeg Concat -> {out_mp4} ...")
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            "-movflags", "+faststart",
            str(out_mp4),
        ]
        subprocess.run(cmd, check=True)
        print(f"🎉 Jukebox MP4 Created: {out_mp4} ({out_mp4.stat().st_size / (1024*1024):.1f} MB)")

    return meta_payload


def create_youtube_live_broadcast(deity: str = "murugan") -> dict:
    """
    Uses the YouTube Live Streaming API (`liveBroadcasts` + `liveStreams`) on `@guru-kula-desam`
    to create a ready-to-stream 24/7 Live Radio broadcast and returns the RTMP URL & Stream Key.
    """
    tok_path = ROOT / "data" / "credentials" / "tokens" / "token_472322435541.json"
    if not tok_path.exists():
        tok_path = ROOT / "data" / "credentials" / "token.json"

    creds = Credentials.from_authorized_user_file(str(tok_path))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    yt = build("youtube", "v3", credentials=creds, cache_discovery=False)

    theme = DEITY_JUKEBOX_THEMES.get(deity.lower(), DEITY_JUKEBOX_THEMES["murugan"])
    start_iso = (datetime.now(timezone.utc) + timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%SZ")

    broadcast_res = yt.liveBroadcasts().insert(
        part="snippet,status,contentDetails",
        body={
            "snippet": {
                "title": theme["live_title"],
                "description": (
                    f"{theme['live_title']}\n\n"
                    f"🎧 {theme['cluster_hooks']}\n"
                    "24/7 Non-Stop Sacred Tamil Devotional & Meditation Radio by Guru Kula Desam (@guru-kula-desam).\n"
                    "🙏 Subscribe & keep this stream playing in your home or workplace for continuous auspicious vibrations."
                ),
                "scheduledStartTime": start_iso,
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            },
            "contentDetails": {
                "enableAutoStart": True,
                "enableAutoStop": False,
                "enableDvr": True,
                "latencyPreference": "normal",
            },
        },
    ).execute()

    stream_res = yt.liveStreams().insert(
        part="snippet,cdn,contentDetails",
        body={
            "snippet": {
                "title": f"GKD 24x7 {deity.capitalize()} Stream 1080p",
            },
            "cdn": {
                "frameRate": "30fps",
                "ingestionType": "rtmp",
                "resolution": "1080p",
            },
            "contentDetails": {
                "isReusable": True,
            },
        },
    ).execute()

    yt.liveBroadcasts().bind(
        part="id,contentDetails",
        id=broadcast_res["id"],
        streamId=stream_res["id"],
    ).execute()

    ingestion = stream_res["cdn"]["ingestionInfo"]
    rtmp_url = f"{ingestion['ingestionAddress']}/{ingestion['streamName']}"
    info = {
        "broadcast_id": broadcast_res["id"],
        "watch_url": f"https://www.youtube.com/watch?v={broadcast_res['id']}",
        "stream_id": stream_res["id"],
        "ingestion_address": ingestion["ingestionAddress"],
        "stream_key": ingestion["streamName"],
        "full_rtmp_url": rtmp_url,
    }
    print(json.dumps(info, ensure_ascii=False, indent=2))
    return info


def build_pure_radio_station_assets(deity: str) -> dict:
    """
    Builds a TRUE 24/7 Audio Radio Station package (like Lofi Girl / Bhakti FM):
      1. Extracts pure 192kbps M4A/AAC audio tracks from the deity's catalog into a local
         concat playlist (`radio_audio_<deity>.txt`) — zero video stream from the clips!
      2. Renders a single, serene 1920x1080 Sacred Radio Station Canvas (`radio_canvas_<deity>.png`)
         featuring the Guru Kula Desam temple banyan/sanctum backdrop, circular emblem,
         and '24/7 LIVE SACRED RADIO — குரு குல தேசம்' station header.
    """
    from PIL import Image, ImageDraw, ImageFont

    radio_dir = JUKEBOX_OUT_DIR / "radio_station" / deity.lower()
    radio_dir.mkdir(parents=True, exist_ok=True)

    tracks = get_tracks_for_deity(deity, require_local=True)
    if not tracks:
        raise RuntimeError(f"No accessible tracks found for deity '{deity}'.")

    theme = DEITY_JUKEBOX_THEMES.get(deity.lower(), DEITY_JUKEBOX_THEMES["murugan"])
    audio_concat_lines = []
    extracted_audios = []

    print(f"🎙️ Preparing Pure Audio Radio Tracks for '{deity}' ({len(tracks)} tracks)...")
    for idx, t in enumerate(tracks, 1):
        out_m4a = radio_dir / f"{idx:02d}_{t['film_id']}.m4a"
        if not out_m4a.exists() or out_m4a.stat().st_size < 10000:
            cmd = [
                "ffmpeg", "-y", "-v", "error",
                "-i", str(t["video_path"]),
                "-vn", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                str(out_m4a),
            ]
            subprocess.run(cmd, check=True)
        escaped_m4a = str(out_m4a).replace("'", "'\\''")
        audio_concat_lines.append(f"file '{escaped_m4a}'")
        extracted_audios.append(str(out_m4a))

    audio_concat_path = radio_dir / f"radio_audio_{deity.lower()}.txt"
    audio_concat_path.write_text("\n".join(audio_concat_lines) + "\n", encoding="utf-8")

    # Render 1920x1080 Sacred Radio Canvas
    canvas_path = radio_dir / f"radio_canvas_{deity.lower()}_1080p.png"
    bg_path = ROOT / "assets" / "images" / "gurukula-banyan-tree-bg.jpg"
    logo_path = ROOT / "production" / "gurukuladesam_shorts_logo.png"

    canvas = Image.new("RGBA", (1920, 1080), (14, 10, 24, 255))
    if bg_path.exists():
        bg = Image.open(bg_path).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)
        # Darken slightly for serene radio studio aesthetic
        dark_overlay = Image.new("RGBA", (1920, 1080), (10, 6, 20, 155))
        canvas = Image.alpha_composite(bg, dark_overlay)

    if logo_path.exists():
        logo = Image.open(logo_path).convert("RGBA").resize((220, 220), Image.Resampling.LANCZOS)
        canvas.paste(logo, (850, 160), logo)

    draw = ImageDraw.Draw(canvas)
    font_paths = [
        "/usr/share/fonts/truetype/noto/NotoSansTamil-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    font_lg = font_md = font_sm = ImageFont.load_default()
    for fp in font_paths:
        if os.path.exists(fp):
            font_lg = ImageFont.truetype(fp, 54)
            font_md = ImageFont.truetype(fp, 36)
            font_sm = ImageFont.truetype(fp, 28)
            break

    draw.text((960, 440), "குரு குல தேசம் | GURU KULA DESAM", fill=(255, 215, 100, 255), font=font_lg, anchor="mm")
    draw.text((960, 520), "🔴 24/7 LIVE SACRED DEVOTIONAL & MEDITATION RADIO", fill=(255, 255, 255, 255), font=font_md, anchor="mm")
    draw.text((960, 590), theme["cluster_hooks"], fill=(200, 230, 255, 255), font=font_sm, anchor="mm")
    draw.text((960, 980), "Non-Stop 24/7 Audio Broadcast • Subscribe: @guru-kula-desam", fill=(220, 200, 160, 230), font=font_sm, anchor="mm")

    canvas.convert("RGB").save(canvas_path, "PNG")
    print(f"🖼️ Sacred 1080p Radio Canvas Generated: {canvas_path}")
    print(f"🎵 Pure Audio Playlist Ready ({len(extracted_audios)} M4A tracks): {audio_concat_path}")

    return {
        "deity": deity,
        "canvas_path": str(canvas_path),
        "audio_concat_path": str(audio_concat_path),
        "tracks_count": len(extracted_audios),
    }


def start_24x7_ffmpeg_radio(deity: str, stream_key: str, mode: str = "pure-audio-radio"):
    """
    Streams 24/7 to YouTube Live RTMP (`rtmp://a.rtmp.youtube.com/live2/<stream_key>`).
    Defaults to `pure-audio-radio` mode:
      • Loops pure 192kbps stereo audio tracks infinitely (`-stream_loop -1`)
      • Pairs them with a single 1080p Sacred Radio Station Canvas + live golden audio waveform
        (`showwaves`) so listeners get a true 24/7 FM/Lofi-style Audio Radio experience!
    """
    rtmp_target = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

    if mode == "pure-audio-radio":
        radio_dir = JUKEBOX_OUT_DIR / "radio_station" / deity.lower()
        canvas_path = str(radio_dir / f"radio_canvas_{deity.lower()}_1080p.png")
        audio_concat = str(radio_dir / f"radio_audio_{deity.lower()}.txt")
        if not os.path.exists(canvas_path) or not os.path.exists(audio_concat):
            assets = build_pure_radio_station_assets(deity)
            canvas_path = assets["canvas_path"]
            audio_concat = assets["audio_concat_path"]

        # Overlay a live golden audio visualizer wave at y=720 on the 1080p Radio Station Canvas
        filter_complex = (
            "[1:a]showwaves=s=1200x140:mode=cline:rate=24:colors=0xFFD700@0.85|0xFF8C00@0.65[wave];"
            "[0:v][wave]overlay=x=360:y=720:shortest=0[outv]"
        )
        cmd = [
            "ffmpeg",
            "-re",
            "-loop", "1", "-framerate", "24", "-i", canvas_path,
            "-f", "concat", "-safe", "0", "-stream_loop", "-1", "-i", audio_concat,
            "-filter_complex", filter_complex,
            "-map", "[outv]", "-map", "1:a",
            "-c:v", "libx264", "-preset", "ultrafast", "-tune", "stillimage",
            "-pix_fmt", "yuv420p", "-b:v", "1800k", "-maxrate", "2000k", "-bufsize", "4000k", "-g", "48",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-f", "flv",
            rtmp_target,
        ]
        print(f"📻 Starting 24/7 PURE AUDIO RADIO STATION ({deity}) with Live Audio Waveform -> {rtmp_target}")
        print("   Command:", " ".join(cmd))
        subprocess.run(cmd, check=True)
    else:
        meta = build_jukebox(deity, target_minutes=180, dry_run=True)
        concat_path = meta["concat_list_path"]
        cmd = [
            "ffmpeg",
            "-re",
            "-stream_loop", "-1",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_path,
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-f", "flv",
            rtmp_target,
        ]
        print(f"🔴 Starting 24/7 Video Loop Stream ({deity}) -> {rtmp_target}")
        subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(description="GKD Zero-Render Jukebox Builder & 24/7 Live Broadcaster")
    parser.add_argument("--list", action="store_true", help="Audit Master Film catalog for Jukebox & Live readiness")
    parser.add_argument("--build-jukebox", action="store_true", help="Build 1-Hour+ Jukebox concat list, chapters & MP4")
    parser.add_argument("--dry-run", action="store_true", help="Generate concat list and chapter metadata without writing MP4")
    parser.add_argument("--deity", type=str, default="murugan", help="murugan, shiva, vallalar, thirukkural, vinayagar, amman, vishnu")
    parser.add_argument("--minutes", type=int, default=60, help="Target Jukebox duration in minutes (default 60)")
    parser.add_argument("--create-live", action="store_true", help="Create YouTube Live Broadcast & Stream Key via API")
    parser.add_argument("--prepare-radio", action="store_true", help="Extract pure M4A audio tracks & build 1080p Sacred Radio Station Canvas")
    parser.add_argument("--start-radio", action="store_true", help="Launch 24/7 FFmpeg RTMP Live Radio stream (Pure Audio + Radio Canvas + Waveform)")
    parser.add_argument("--mode", type=str, default="pure-audio-radio", choices=["pure-audio-radio", "video-loop"], help="Radio mode (default: pure-audio-radio)")
    parser.add_argument("--stream-key", type=str, help="YouTube Live RTMP Stream Key")
    args = parser.parse_args()

    if args.list:
        audit_catalog()
        return

    if args.prepare_radio:
        build_pure_radio_station_assets(args.deity)
        return

    if args.build_jukebox:
        build_jukebox(args.deity, target_minutes=args.minutes, dry_run=args.dry_run)
        return

    if args.create_live:
        create_youtube_live_broadcast(args.deity)
        return

    if args.start_radio:
        if not args.stream_key:
            raise ValueError("--stream-key is required with --start-radio")
        start_24x7_ffmpeg_radio(args.deity, args.stream_key, mode=args.mode)
        return

    audit_catalog()


if __name__ == "__main__":
    main()
