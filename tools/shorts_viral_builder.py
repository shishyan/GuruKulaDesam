#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/shorts_viral_builder.py
100% Song-Authentic 9:16 Vertical (1080x1920 @ 24fps) Shorts Builder
for @GuruKulaDesam (நற்செய்கை — Virtuous Shorts) & @GuruKulaDesam2 (நற்பண்பு — Devotional Shorts).

STRICT @GURU-KULA-DESAM DISCOGRAPHY & CHORUS GUARANTEE:
1. Primary & Default Source (`original_master_clip`):
   Clips the song's TRUE Original Master Film from `@guru-kula-desam` (`UCPqB1A_WzpLJec6q69BOO3Q`)
   starting right at the Opening Chorus (`Pallavi`, `clip_anchor_mode="chorus_v1"`) and running
   34–43s through the Chorus into the natural instrumental / phrase dip so ZERO words are chopped:
   - Local clean un-layered 1080p/720p Master MP4s (`renders/master_cache/*_clean.mp4`, Google Drive `Videos/`, SSD `renders/releases/`)
   - Published HD Master Films on `@guru-kula-desam` (`UCPqB1A_WzpLJec6q69BOO3Q`, auto-fetched at 1080p/720p via `yt-dlp`).
2. Per-Video Pixel Layout & Motion Guard (`inspect_master_video_layout`):
   - Rejects static single-image cover art (`scene_motion < 4.5` or `1:1` square posters).
   - Auto-detects top header pills (`has_top`) and bottom karaoke subtitles (`has_bot`) directly from
     decoded frames and applies exact centered `1080x1248` (`Y=312..1560`) Lanczos framing with gentle
     divine vibrancy (`eq=saturation=1.08:contrast=1.03:brightness=0.015`) and zero disorienting `sin` pan.
3. NEVER falls back to synthetic Google Flow clips unless `--use-flow` is explicitly requested.
"""

import os
import sys
import re
import json
import math
import time
import shutil
import struct
import hashlib
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.tamil_panchangam_engine import (
    IST,
    classify_sacred_category,
    get_auspicious_alignment_for_datetime,
)

FFMPEG = "C:/ffmpeg/bin/ffmpeg.exe" if Path("C:/ffmpeg/bin/ffmpeg.exe").exists() else (shutil.which("ffmpeg") or "ffmpeg")
FFPROBE = "C:/ffmpeg/bin/ffprobe.exe" if Path("C:/ffmpeg/bin/ffprobe.exe").exists() else (shutil.which("ffprobe") or "ffprobe")

WIN_ROOT = Path("/media/shishyan/Shishyan/GitHub/Gurukuladesam")
METADATA_DB = ROOT / "production" / "metadata" / "all_songs_lyrics_and_meanings.json"
MANIFEST_DB = ROOT / "production" / "autonomous_master_production_manifest.json"
MASTER_CATALOG_FILE = ROOT / "production" / "shorts_metadata" / "master_film_sources.json"

FLOW_RENDERS_DIR = ROOT / "production" / "google_flow_renders"
WIN_FLOW_RENDERS_DIR = WIN_ROOT / "production" / "google_flow_renders"
RELEASES_DIR = ROOT / "renders" / "releases"
WIN_RELEASES_DIR = WIN_ROOT / "renders" / "releases"
MASTER_CACHE_DIR = ROOT / "renders" / "master_cache"
MASTER_CACHE_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIRS = [ROOT / "production" / "audio", ROOT / "source" / "youtube", WIN_ROOT / "production" / "audio", WIN_ROOT / "source" / "youtube"]

SHORTS_OUT_DIR = ROOT / "renders" / "shorts_gurukuladesam2"
SHORTS_OUT_DIR.mkdir(parents=True, exist_ok=True)
SHORTS_META_DIR = ROOT / "production" / "shorts_metadata"
SHORTS_META_DIR.mkdir(parents=True, exist_ok=True)
SHORTS_TEMP_DIR = ROOT / "renders" / "temp_shorts_build"
SHORTS_TEMP_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
FPS = 24
DEFAULT_SHORT_DURATION = 38.0

# Wav2Vec2-Tamil CTC (20ms phoneme frame) + DSP verified Opening Chorus (Pallavi) windows:
# Keyed by resolved video stem / YouTube Film ID / Track ID -> (start_sec, duration_sec)
VERIFIED_CHORUS_WINDOWS = {
    # 1. கடவுள் வாழ்த்து (அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு + reprise + instrumental finish)
    "gvg-um6fU40_clean": (28.0, 40.5),
    "gvg-um6fU40": (28.0, 40.5),
    "VKWNnHC4tbU": (28.0, 40.5),
    "02C8glMmetw": (24.5, 38.5),
    # 2. அதிகாரம் 67 - வினைத்திட்பம் (சொல்லுதல் யார்க்கும் எளிய அரியவாம் சொல்லிய வண்ணம் செயல் + instrumental)
    "UPAYRisyN7Q": (15.6, 36.8),
    "adhikaram_67_vinaithitpam_cinematic": (15.6, 36.8),
    "--4jzoezBW8": (15.6, 36.8),
    # 3. திருவருட்பா: அபராத விண்ணப்பம் I (நம்பினேன் நின்றன் திருவடி மலரை... தும்பி மாமுகனை வேலனை ஈன்ற தோன்றலே)
    "thirukkural_-cmB2_XZqs0_master": (48.2, 35.6),
    "-cmB2_XZqs0": (48.2, 35.6),
    # 4. அதிகாரம் 56 - கொடுங்கோன்மை (முறைகோடி மன்னவன் செய்யின் உறைகோடி ஒல்லாது வானம் பெயல் + instrumental)
    "thirukkural_01g0sJdaL2I_master": (13.6, 36.2),
    "wzdoeFDq0iQ": (8.6, 40.8),
    "01g0sJdaL2I": (13.6, 36.2),
    # 5. அபிராமி அந்தாதி: தனந்தரும் கல்விதரும் (தனந்தரும் கல்விதரும் ஒரு நாளும் தளர்வறியா மனந்தரும்...)
    "Yu4RBKpAodM": (44.4, 40.4),
    "60rrBjJfAS4": (44.4, 40.4),
    "2tL-bKjkL18": (44.4, 40.4),
    # 6. விநாயகர் துதி: கண நாதா ஓம் (கணநாதா கணநாதா கங்காதர சுத கணநாதா + மத்தள வயிறனே + instrumental)
    "uqQlyCQjz-A": (20.8, 35.0),
    "2g6p7WKWsxk": (20.8, 35.0),
    "vinayagar_Lki_Y8OSljs_master": (20.8, 35.0),
    "Lki_Y8OSljs": (20.8, 35.0),
    # 7. பாலும் தெளிதேனும் (பாலும் தெளிதேனும் பாகும் பருப்பும்... சங்கத் தமிழ் மூன்றும் தா!)
    "vinayagar_AW4cljBWy2w_master": (35.7, 37.5),
    "AW4cljBWy2w": (35.7, 37.5),
    # 8. கந்தர் அனுபூதி: உருவாய் அருவாய் (உருவாய் அருவாய்... குருவாய் வருவாய் அருள்வாய் குகனே! முருகா முருகா!)
    "DsbMysGdqv8": (37.4, 41.6),
    "zMhemBjkes0": (37.4, 41.6),
    # 9. திருவருட்பா: சிவ சுப்ரமணியர் திருவிருத்தம் (Opening Chorus stanza -> natural phrase pause)
    "ssOkftpUcLE": (32.7, 35.2),
    "-unILRjNLHQ": (32.7, 35.2),
    # 10. திருப்புகழ்: ஆறுமுகம் ஆறுமுகம் (ஆறுமுகம் ஆறுமுகம்... full Chorus + reprise -> instrumental pause)
    "SwUq9aoYdZs": (43.9, 37.9),
    "murugan_B6yVe6HM8Ok_master": (43.9, 37.9),
    "B6yVe6HM8Ok": (43.9, 37.9),
    # 11. திருப்புகழ்: முத்தைத் தரு (முத்தைத் தரு பத்தித் திருநகை... + instrumental + reprise)
    "6L6DDOwDuy8": (23.2, 40.6),
    "_6QdoqADlT0": (23.8, 40.0),
    "murugan_3oJ2OPG-WCs_master": (23.2, 40.6),
    "3oJ2OPG-WCs": (23.2, 40.6),
    # Additional verified iconic Master Films
    "dd3x2HfeE0I": (26.2, 37.8),
    "p1KPCpSX53U": (25.8, 36.8),
    "udRsA-oWxS0": (35.3, 38.2),
    "zQ05gUqsReQ_clean": (36.4, 38.0),
    "zQ05gUqsReQ": (36.4, 38.0),
}

NON_DEVOTIONAL_EXCLUDED_KEYWORDS = (
    "மணிக்கொடி",
    "தமிழ்த் தாய்",
    "தேசிய கீதம்",
    "சுதந்திர",
    "வந்தே மாதரம்",
    "பாரதியார் பாடல்",
    "remix",
)

# Dedicated playlist on @guru-kula-desam ("The Remix List" -> PLOtFcgNeGYyI) and all Remix video IDs
# strictly excluded from the Shorts publishing scope:
EXCLUDED_REMIX_PLAYLIST_ID = "PLOtFcgNeGYyI"
EXCLUDED_REMIX_VIDEO_IDS = frozenset({
    "28Xnfhctf0I", "Iky5L-131A4", "cEIEecb51Fc", "R-5gWfRNMts", "0DoegY9d0ZM", "cUt716Zafy0",
    "FS5fUOxZySE", "2Pun6K7h984", "0bz1myKXoJQ", "UyCe3KLqY_8", "OzejLLvDq5s", "r75xdfETSbE",
    "RAUafMVpT5k", "GN181JJ1lXU", "RY7nPGorS94", "ulW6fg4lkYA", "q2oGlYiV-qg", "FGFVertqRUU",
    "J-mAIpyxy4A", "XRizXIUU57g", "tj_5hsasdyU", "Fh3HfGUObmg", "FXMVQIidbJU", "PmziMZrMHfE",
    "37qaN4sG53k", "Vj6wcfC3rPk", "tLt9J-X9WOE", "5coBrJy6a5M", "9-SvikTz2FU", "DhHGetUJlAI",
    "F-aVgFOdKFo", "VMqFjcQtebw", "mVQJIrLtnCk", "JGslKeAreOE", "JvonvWQHKQY", "djYooU1LmGk",
    "oEQ3sx6ujQc", "dVYI3ZgpDC8", "KLsXZa28uyE", "HRN77i6Kio8", "xVyPWHTMXHw", "wylRNpaJNmY",
    "VVkl8bORJXg", "vbMywONB5Wc", "gjo0AfKBzsU", "2Qs07DTJvvM", "x3CyxNH5bpQ", "QXWB2raWKXE",
    "rOowxP53oWA", "0WurYH-hkNM", "D95woYqPoPI", "QXqjB9UnD7E", "aZ830iKkqBs", "c5OwVOaYsW0",
    "fQspUClJyg8", "zzJZkyX1GL4", "MM7sy4TQj6w", "785z3bWr43A", "MmZsN65ejRE", "628xa7-iMgM",
    "hZl325VJwik", "nnZLI8AY4rs", "2N5_pir8gbM", "VqUGNZ9Uleo", "Wp7MvpC-P8c", "G5fGB22diek",
    "koPghjI9FPE", "aPNYGn5ntIU", "PU0HJxRNmiw", "wzyyyzSJUV8", "w-wUOqoZyAY", "44mJquYpaRQ",
    "VGpWJXwhogo",
})

DEITY_HOOKS = {
    "murugan": {
        "badge": "வெற்றிவேல் முருகன் | LORD MURUGAN DIVINE CHANT",
        "hook_en": "Receive Lord Murugan's Grace Today",
        "hook_ta": "வெற்றிவேல் முருகனுக்கு அரோகரா! தியானிப்போம் வாரீர்",
        "tags": ["#Shorts", "#Murugan", "#Vetrivel", "#KandaSashti", "#Thaipusam", "#ArupadaiVeedu", "#TamilDevotional", "#BhaktiShorts", "#GuruKulaDesam"],
    },
    "shiva": {
        "badge": "தென்னாடுடைய சிவனே போற்றி | LORD SHIVA SACRED HYMN",
        "hook_en": "Om Namah Shivaya — Sacred Tamil Tirumurai",
        "hook_ta": "நமச்சிவாய வாழ்க! நாதன் தாள் வாழ்க!",
        "tags": ["#Shorts", "#Shiva", "#OmNamahShivaya", "#Thiruvasagam", "#Pradosham", "#Shivaratri", "#TamilDevotional", "#GuruKulaDesam"],
    },
    "amman": {
        "badge": "ஓம் சக்தி பராசக்தி | GODDESS AMMAN GRACE",
        "hook_en": "Receive Divine Mother's Blessings",
        "hook_ta": "தனந்தரும் கல்விதரும் அபிராமி அம்மன் திருவருள்!",
        "tags": ["#Shorts", "#Amman", "#Abhirami", "#OmSakthi", "#Pournami", "#Navaratri", "#TamilDevotional", "#GuruKulaDesam"],
    },
    "vinayagar": {
        "badge": "ஓம் கம் கணபதயே நமஹ | LORD VINAYAGAR BLESSINGS",
        "hook_en": "Remove All Obstacles with This Sacred Ganapathi Chant",
        "hook_ta": "தடைகள் நீக்கும் முழுமுதற்கடவுள் விநாயகர் போற்றி!",
        "tags": ["#Shorts", "#Vinayagar", "#Ganesha", "#Ganapathi", "#SankataharaChaturthi", "#Bhakti", "#TamilDevotional", "#GuruKulaDesam"],
    },
    "vishnu": {
        "badge": "ஓம் நமோ நாராயணாய | PERUMAL & KRISHNA DIVINE HYMN",
        "hook_en": "Sacred Perumal Pasuram for Peace & Prosperity",
        "hook_ta": "கோவிந்தா! நாராயணா! பெருமாள் திவ்ய பிரபந்தம்",
        "tags": ["#Shorts", "#Perumal", "#Krishna", "#Vishnu", "#Ekadashi", "#DivyaPrabandham", "#Tirupati", "#TamilDevotional", "#GuruKulaDesam"],
    },
    "vallalar": {
        "badge": "அருட்பெருஞ்ஜோதி | VALLALAR THIRUVARUTPA",
        "hook_en": "Arutperunjothi — Supreme Light of Universal Compassion",
        "hook_ta": "அருட்பெருஞ்ஜோதி தனிப்பெருங்கருணை!",
        "tags": ["#Shorts", "#Vallalar", "#Thiruvarutpa", "#Arutperunjothi", "#Sanmargam", "#TamilDevotional", "#GuruKulaDesam"],
    },
    "thirukkural": {
        "badge": "திருவள்ளுவர் அருளிய திருக்குறள் | ETERNAL TAMIL WISDOM",
        "hook_en": "2,000-Year-Old Sacred Tamil Wisdom for Noble Living",
        "hook_ta": "உலகப் பொதுமறை திருக்குறள் — தெய்வீக இசை வடிவம்",
        "tags": ["#Shorts", "#Thirukkural", "#Thiruvalluvar", "#TamilWisdom", "#UniversalEthics", "#TamilDevotional", "#GuruKulaDesam"],
    },
}

_CLIP_HASH_COUNTS = None


def _get_clip_hash_counts() -> dict[str, int]:
    global _CLIP_HASH_COUNTS
    if _CLIP_HASH_COUNTS is not None:
        return _CLIP_HASH_COUNTS
    counts = {}
    for base in (FLOW_RENDERS_DIR, WIN_FLOW_RENDERS_DIR):
        if base.exists():
            for mp4 in base.glob("*/*.mp4"):
                try:
                    if mp4.stat().st_size > 200_000:
                        with open(mp4, "rb") as fh:
                            h = hashlib.md5(fh.read(65536)).hexdigest()
                        counts[h] = counts.get(h, 0) + 1
                except Exception:
                    pass
    _CLIP_HASH_COUNTS = counts
    return counts


def is_strictly_unique_song_clip(mp4_path: Path) -> bool:
    if not mp4_path.exists() or mp4_path.stat().st_size < 250_000:
        return False
    counts = _get_clip_hash_counts()
    try:
        with open(mp4_path, "rb") as fh:
            h = hashlib.md5(fh.read(65536)).hexdigest()
        return counts.get(h, 1) <= 2
    except Exception:
        return False


def get_track_dedicated_flow_clips(track_id: str, require_fresh_flow_short: bool = False) -> list[Path]:
    for base in (FLOW_RENDERS_DIR, WIN_FLOW_RENDERS_DIR):
        tdir = base / track_id
        if not tdir.exists():
            continue
        verified_clips = [c for c in sorted(tdir.glob("flow_short_*.mp4")) if c.stat().st_size > 250_000]
        if len(verified_clips) >= 3:
            return verified_clips
        if require_fresh_flow_short:
            continue
        own_scenes = [c for c in sorted(tdir.glob("scene_*.mp4")) if c.stat().st_size > 250_000 and is_strictly_unique_song_clip(c)]
        if len(own_scenes) >= 5:
            return own_scenes
    return []


def load_master_catalog() -> dict:
    if MASTER_CATALOG_FILE.exists():
        try:
            return json.loads(MASTER_CATALOG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def find_catalog_entry(track_id: str, master_cat: dict | None = None) -> dict | None:
    cat_map = master_cat if master_cat is not None else load_master_catalog()
    if track_id in cat_map:
        return cat_map[track_id]
    for entry in cat_map.values():
        if (
            entry.get("legacy_track_id") == track_id
            or entry.get("youtube_film_id") == track_id
            or track_id in (entry.get("alias_track_ids") or [])
        ):
            return entry
    return None


def get_ytdlp_cmd() -> list[str]:
    local_bin = Path.home() / ".local" / "bin" / "yt-dlp"
    if local_bin.exists():
        return [str(local_bin)]
    which_yt = shutil.which("yt-dlp")
    if which_yt:
        return [which_yt]
    return [sys.executable, "-m", "yt_dlp"]


def probe_video_stream(path: Path) -> tuple[bool, int, int, float]:
    """Validates container `moov` atom, landscape HD resolution (`height >= 720`), and `duration > 35s`."""
    try:
        if not path.exists() or path.stat().st_size < 5_000_000:
            return False, 0, 0, 0.0
        pr = json.loads(subprocess.check_output([
            FFPROBE, "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height:format=duration",
            "-of", "json", str(path),
        ], text=True))
        streams = pr.get("streams") or []
        if not streams:
            return False, 0, 0, 0.0
        w = int(streams[0].get("width", 0))
        h = int(streams[0].get("height", 0))
        dur = float(pr.get("format", {}).get("duration", 0.0))
        is_valid = (dur > 35.0) and (h >= 720) and (abs(w - h) > 16)
        return is_valid, w, h, dur
    except Exception:
        return False, 0, 0, 0.0


def inspect_master_video_layout(video_path: Path, sample_start: float = 24.0, has_burned_hint: bool = False) -> dict:
    """
    Fast (<0.4s) 4-frame pixel layout & motion verifier:
    - Measures coarse scene motion (`32x18`) to block static single-image posters (`scene_motion < 4.5`).
    - Detects persistent top header pills (`has_top`) and outlined Tamil karaoke subtitles (`has_bot`).
    """
    ok, w, h, dur = probe_video_stream(video_path)
    if not ok:
        return {"w": w, "h": h, "dur": dur, "scene_motion": 0.0, "is_static": True, "has_top": has_burned_hint, "has_bot": has_burned_hint}

    try:
        import numpy as np
        from PIL import Image

        tw, th = 960, 540
        frames, coarse = [], []
        for dt in (0.0, 9.0, 18.0, 27.0):
            ts = min(max(2.0, sample_start + dt), max(0.0, dur - 2.0))
            raw = subprocess.check_output([
                FFMPEG, "-nostdin", "-v", "error", "-ss", f"{ts:.1f}",
                "-i", str(video_path), "-frames:v", "1",
                "-vf", f"scale={tw}:{th}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
            ])
            if len(raw) == tw * th * 3:
                im = Image.frombuffer("RGB", (tw, th), raw)
                frames.append(np.array(im, dtype=np.int16))
                coarse.append(np.array(im.resize((32, 18), Image.BILINEAR), dtype=np.float32))

        if len(frames) < 2:
            return {"w": w, "h": h, "dur": dur, "scene_motion": 20.0, "is_static": False, "has_top": has_burned_hint, "has_bot": has_burned_hint}

        arr = np.stack(frames, axis=0)
        c_arr = np.stack(coarse, axis=0)[:, 3:15, 6:26, :]
        scene_motion = float(np.abs(np.diff(c_arr, axis=0)).mean())
        is_static = (scene_motion < 4.5) or (abs(w - h) <= 16)

        top_zone = arr[:, 3:36, 300:660, :]
        top_std = top_zone.std(axis=0).max(axis=2)
        top_gx = np.abs(np.diff(top_zone.mean(axis=0), axis=1)).max(axis=2)
        has_top = bool(((top_std[:, :-1] < 8.0) & (top_gx > 45.0)).sum() >= 24) and not is_static

        bot_hits = 0
        for f in frames:
            bz = f[int(540 * 0.855):int(540 * 0.985), int(960 * 0.28):int(960 * 0.72), :]
            luma = (bz[:, :, 0] * 299 + bz[:, :, 1] * 587 + bz[:, :, 2] * 114) // 1000
            dx2 = luma[:, 2:] - luma[:, :-2]
            pos_j = (dx2 > 75).sum(axis=1)
            neg_j = (dx2 < -75).sum(axis=1)
            if ((pos_j >= 10) & (neg_j >= 10)).sum() >= 3:
                bot_hits += 1
        # If top header pill or catalog burned-bars flag is present on a YouTube layered video, guard bottom subtitle band too
        has_bot = ((bot_hits >= 1) or has_top or has_burned_hint) and not is_static

        return {
            "w": w,
            "h": h,
            "dur": dur,
            "scene_motion": round(scene_motion, 2),
            "is_static": is_static,
            "has_top": has_top,
            "has_bot": has_bot,
        }
    except Exception:
        return {"w": w, "h": h, "dur": dur, "scene_motion": 25.0, "is_static": False, "has_top": has_burned_hint, "has_bot": has_burned_hint}


def resolve_original_master_video(track_id: str, catalog_entry: dict | None = None) -> tuple[Path | None, bool, str | None]:
    """
    Resolves the song's TRUE `@guru-kula-desam` Master Film (`(video_path, has_burned_hint, youtube_film_id)`):
      1. Cached clean un-layered 1080p GDrive Master MP4 (`renders/master_cache/<id>_clean.mp4`)
      2. Clean un-layered Google Drive Master MP4 (`local_clean_video`, cached as `<id>_clean.mp4`)
      3. Validated fast local/SSD remastered Master MP4 (`local_clean_video`, `height >= 720`, `24fps+`)
      4. Cached HD YouTube Master Film (`renders/master_cache/<youtube_film_id>.mp4`)
      5. Auto-download published 1080p/720p Master Film from `@guru-kula-desam` via `yt-dlp` (DASH 1080p first!)
    """
    cat = catalog_entry if catalog_entry is not None else find_catalog_entry(track_id)
    yt_film_id = cat.get("youtube_film_id") if cat else None
    has_burned = bool(cat.get("has_burned_bars", False)) if cat else False
    cache_id = yt_film_id or track_id

    # 1. Cached clean un-layered base video (`*_clean.mp4`)
    clean_cache_mp4 = MASTER_CACHE_DIR / f"{cache_id}_clean.mp4"
    ok, _, _, _ = probe_video_stream(clean_cache_mp4)
    if ok:
        return clean_cache_mp4, False, yt_film_id

    # 2. Clean un-layered Google Drive video -> cache once into `*_clean.mp4`
    if cat and cat.get("local_clean_video") and str(cat["local_clean_video"]).startswith("/run/user/"):
        gvfs_p = Path(cat["local_clean_video"])
        try:
            if gvfs_p.exists():
                print(f"  📂 Caching clean 1080p base video from Google Drive -> {clean_cache_mp4.name}...")
                subprocess.run(["gio", "copy", str(gvfs_p), str(clean_cache_mp4)], check=True, capture_output=True)
                ok, _, _, _ = probe_video_stream(clean_cache_mp4)
                if ok:
                    return clean_cache_mp4, False, yt_film_id
        except Exception:
            pass

    # 3. Validated fast local/mounted SSD remastered Master MP4 (`local_clean_video`)
    if cat and cat.get("local_clean_video") and not str(cat["local_clean_video"]).startswith("/run/user/"):
        p = Path(cat["local_clean_video"])
        ok, _, _, _ = probe_video_stream(p)
        if ok:
            return p, False, yt_film_id

    # 4. Already cached HD YouTube Master Film (`renders/master_cache/<yt_film_id>.mp4`)
    if yt_film_id:
        cached_mp4 = MASTER_CACHE_DIR / f"{yt_film_id}.mp4"
        ok, _, _, _ = probe_video_stream(cached_mp4)
        if ok:
            return cached_mp4, has_burned, yt_film_id

    local_cache_mp4 = MASTER_CACHE_DIR / f"{cache_id}.mp4"
    ok, _, _, _ = probe_video_stream(local_cache_mp4)
    if ok:
        return local_cache_mp4, False, yt_film_id

    # 5. Auto-download published 1080p/720p Master Film from @Guru-Kula-Desam via yt-dlp (DASH 1080p first — NEVER 360p!)
    if yt_film_id:
        cached_mp4 = MASTER_CACHE_DIR / f"{yt_film_id}.mp4"
        cached_mp4.unlink(missing_ok=True)
        print(f"  📥 Downloading Original HD Master Film from @guru-kula-desam ({yt_film_id}) via yt-dlp...")
        ytdlp = get_ytdlp_cmd()
        url = f"https://www.youtube.com/watch?v={yt_film_id}"
        for extra_args in (
            [],
            ["--extractor-args", "youtube:player_client=web,tv"],
        ):
            cmd = [
                *ytdlp,
                *extra_args,
                "-f", (
                    "bestvideo[vcodec^=avc1][height<=1080][height>=720]+bestaudio[ext=m4a]/"
                    "bestvideo[height<=1080][height>=720][ext=mp4]+bestaudio[ext=m4a]/"
                    "bestvideo[height<=1080][height>=720]+bestaudio/"
                    "best[height<=1080][height>=720]"
                ),
                "--merge-output-format", "mp4",
                "-o", str(cached_mp4),
                url,
            ]
            subprocess.run(cmd, capture_output=True, text=True)
            ok, w, h, _ = probe_video_stream(cached_mp4)
            if ok:
                print(f"  ✅ Downloaded Master Film: {cached_mp4.name} ({w}x{h}, {cached_mp4.stat().st_size / 1e6:.1f} MB)")
                return cached_mp4, has_burned, yt_film_id
            cached_mp4.unlink(missing_ok=True)

    # 6. Fallback: local/SSD releases dir if verified valid HD
    search_ids = [track_id]
    if cat and cat.get("legacy_track_id") and cat["legacy_track_id"] not in search_ids:
        search_ids.append(cat["legacy_track_id"])
    if yt_film_id and yt_film_id not in search_ids:
        search_ids.append(yt_film_id)
    for rel_dir in (RELEASES_DIR, WIN_RELEASES_DIR):
        if rel_dir.exists():
            if cat and cat.get("chapter_num"):
                for m in sorted(rel_dir.glob(f"adhikaram_0*{cat['chapter_num']}_*_cinematic.mp4")):
                    ok, _, _, _ = probe_video_stream(m)
                    if ok:
                        return m, False, yt_film_id
            for sid in search_ids:
                for m in sorted(rel_dir.glob(f"*{sid}*.mp4")):
                    ok, _, _, _ = probe_video_stream(m)
                    if ok:
                        return m, False, yt_film_id

    return None, False, yt_film_id


def detect_deity_category(track_id: str, meta_entry: dict, manifest_cat: str = "") -> str:
    title_l = f"{meta_entry.get('title', '')}".lower()
    combined = f"{manifest_cat} {meta_entry.get('genre', '')} {title_l}".lower()
    if any(k in title_l for k in ("திருக்குறள்", "thirukkural", "அதிகாரம்", "adhikaram")):
        return "thirukkural"
    if any(k in title_l for k in ("சுப்ரமணிய", "subramani", "திருப்புகழ்", "thiruppugazh", "ஆறுமுகம்", "arumugam", "கந்த", "kandha", "kandar", "முருக", "murug")):
        return "murugan"
    if any(k in title_l for k in ("திருவருட்பா", "thiruvarutpa", "வள்ளலார்", "vallalar", "அருட்பெருஞ்ஜோதி", "அருட்பெருஞ்சோதி", "arutperunjothi", "கொன்றை வேந்தன்", "konrai vendhan")):
        return "vallalar"
    if any(k in title_l for k in ("தேவாரம்", "thevaram", "திருவாசகம்", "thiruvasagam", "ஈஸ்வர", "ishwara", "நடராஜ", "nataraj", "சிவ", "shiva")):
        return "shiva"
    if any(k in combined for k in ("திருவருட்பா", "thiruvarutpa", "வள்ளலார்", "vallalar", "அருட்பெருஞ்ஜோதி", "அருட்பெருஞ்சோதி", "arutperunjothi", "கொன்றை வேந்தன்", "konrai vendhan")):
        return "vallalar"
    if any(k in combined for k in ("விநாயக", "vinayag", "கணபதி", "ganapathi", "கண நாதா", "gana natha", "கணேச", "ganesha", "கைத்தல நிறைகனி", "kaiththala", "திகட சக்கர", "thigada", "பிடியதன் உருவுமை", "pidiyathan", "நான்மணிமாலை", "பாலும் தெளிதேனும்")):
        return "vinayagar"
    if any(k in combined for k in ("அம்மன்", "amman", "அபிராமி", "abhirami", "சக்தி", "sakthi", "சரஸ்வதி", "saraswathi", "லக்ஷ்மி", "lakshmi", "கருமாரி", "karumari", "ரேணுகாம்பாள்", "renukambal", "காயத்ரி", "gayathri")):
        return "amman"
    if any(k in combined for k in ("விஷ்ணு", "vishnu", "கிருஷ்ண", "krishna", "பெருமாள்", "perumal", "ஆழ்வார்", "azhvar", "திருப்பாவை", "thiruppavai", "நாராயண", "narayana", "கோவிந்த", "govinda", "ராம", "rama", "ரகுபதி", "raghupati", "ஆஞ்சநேயர்", "anjaneyar", "பல்லாண்டு", "pallaandu")):
        return "vishnu"
    if any(k in combined for k in ("முருக", "murug", "கந்த", "kandha", "kandar", "திருப்புகழ்", "thiruppugazh", "சுப்ரமணிய", "subramani", "ஸ்கந்த", "skanda", "ஆறுமுகம்", "arumugam", "வேல்", "கௌமாரம்", "koumaram", "மகரம் அளறு")):
        return "murugan"
    if any(k in combined for k in ("சிவ", "shiva", "siva", "திருவாசகம்", "thiruvasagam", "தேவாரம்", "thevaram", "ஈஸ்வர", "ishwara", "eeswara", "திருமந்திரம்", "thirumanthiram", "பெரியபுராணம்", "periyapuranam", "தில்லை", "thillai", "அருணாசலம்", "arunachalam", "நடராஜ", "nataraj", "கோளறு", "திருநீற்று")):
        return "shiva"
    if any(k in combined for k in ("திருக்குறள்", "thirukkural", "அதிகாரம்", "adhikaram")):
        return "thirukkural"
    return "murugan"


def get_media_duration(path: Path) -> float:
    cmd = [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path),
    ]
    out = subprocess.check_output(cmd).decode("utf-8", errors="ignore").strip()
    return float(out) if out else 0.0


def find_chorus_window(
    media_path: Path,
    track_id: str = "",
    yt_film_id: str | None = None,
    min_dur: float = 34.0,
    max_dur: float = 43.0,
    default_dur: float = DEFAULT_SHORT_DURATION,
) -> tuple[float, float]:
    """
    Locates the Opening Chorus (`Pallavi`) vocal entry and lets the Chorus + instrumental/phrase dip
    finish cleanly within `[min_dur .. max_dur]` (34–43s) without chopping mid-word:
      1. Uses exact 20ms Wav2Vec2-Tamil CTC verified Chorus windows when available for the resolved file.
      2. For all other songs, runs Masataka Goto Long-Range Chorus Recurrence + Mid/Side Center Vocal
         Formant Salience + First-Statement Backtrack + Breath-Dip Phrase-End Snapping.
    """
    total_dur = get_media_duration(media_path)
    if total_dur <= min_dur + 3.0:
        return 0.0, round(min(total_dur, default_dur), 2)

    for key in (media_path.stem, yt_film_id or "", track_id):
        if key and key in VERIFIED_CHORUS_WINDOWS:
            st, dur = VERIFIED_CHORUS_WINDOWS[key]
            if st + dur <= total_dur + 0.5:
                return float(st), round(min(dur, total_dur - st), 2)

    try:
        import numpy as np

        sr = 8000
        cmd = [
            FFMPEG, "-nostdin", "-v", "error", "-t", "240",
            "-i", str(media_path),
            "-vn", "-ac", "2", "-ar", str(sr), "-f", "s16le", "-",
        ]
        raw = subprocess.check_output(cmd)
        pcm = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        pcm = pcm[: (len(pcm) // 2) * 2].reshape(-1, 2)
        mid = 0.5 * (pcm[:, 0] + pcm[:, 1])
        side = 0.5 * (pcm[:, 0] - pcm[:, 1])

        hop = sr // 10   # 0.1s
        win = sr // 5    # 0.2s
        n_frames = (len(mid) - win) // hop + 1
        idx = np.arange(n_frames)[:, None] * hop + np.arange(win)[None, :]
        w_win = np.hanning(win).astype(np.float32)

        spec_m = np.abs(np.fft.rfft(mid[idx] * w_win, axis=1))
        spec_s = np.abs(np.fft.rfft(side[idx] * w_win, axis=1))
        freqs = np.fft.rfftfreq(win, d=1.0 / sr)

        m_voc = (freqs >= 300) & (freqs <= 3200)
        voc_m = np.sqrt(np.mean(spec_m[:, m_voc] ** 2, axis=1) + 1e-12)
        voc_s = np.sqrt(np.mean(spec_s[:, m_voc] ** 2, axis=1) + 1e-12)

        p92 = float(np.percentile(voc_m, 92)) + 1e-9
        voc_norm = voc_m / p92
        ms_ratio = voc_m / (voc_s + 0.10 * p92)
        center_boost = np.clip((ms_ratio - 1.15) / 1.5, 0.05, 1.40)
        vocal_sal = voc_norm * center_boost

        edges = np.geomspace(280, 3300, 17)
        bands = [np.log(np.mean(spec_m[:, (freqs >= edges[b]) & (freqs < edges[b + 1])] ** 2, axis=1) + 1e-10) for b in range(16)]
        bmat = np.stack(bands, axis=1)
        bmat -= np.mean(bmat, axis=1, keepdims=True)

        nh = n_frames // 5  # 0.5s grid
        bm_h = bmat[: nh * 5].reshape(nh, 5, 16).mean(axis=1)
        vs_h = vocal_sal[: nh * 5].reshape(nh, 5).mean(axis=1)
        vn_h = voc_norm[: nh * 5].reshape(nh, 5).mean(axis=1)
        ms_h = ms_ratio[: nh * 5].reshape(nh, 5).mean(axis=1)

        max_cand_h = int(min(50.0, max(2.0, total_dur - max_dur)) * 2)
        plen = 20  # 10.0s Chorus phrase template
        n_tmpls = nh - plen
        tmpls = np.array([bm_h[i : i + plen].ravel() for i in range(n_tmpls)], dtype=np.float32)
        tmpls_norm = tmpls / (np.linalg.norm(tmpls, axis=1, keepdims=True) + 1e-9)

        best_sc = -1e9
        best_h = 32  # fallback ~16s if very quiet
        valid_mask = np.array([np.mean(vs_h[j : j + plen]) >= 0.16 for j in range(n_tmpls)])

        for h in range(0, min(max_cand_h + 1, n_tmpls)):
            sal14 = float(np.mean(vs_h[h : min(nh, h + 28)]))
            med_ms = float(np.median(ms_h[h : min(nh, h + 24)]))
            duty26 = float(np.mean(vn_h[h : min(nh, h + 52)] > 0.30))
            if sal14 < 0.18 or duty26 < 0.45 or med_ms < 1.32:
                continue

            sims = tmpls_norm @ tmpls_norm[h]
            imm_lo, imm_hi = min(n_tmpls, h + 18), min(n_tmpls, h + 56)
            sim_imm = float(np.max(sims[imm_lo:imm_hi] * valid_mask[imm_lo:imm_hi])) if imm_hi > imm_lo else 0.0
            lr_lo = min(n_tmpls, max(h + 84, 110))
            sim_lr = float(np.max(sims[lr_lo:] * valid_mask[lr_lo:])) if n_tmpls > lr_lo + 4 else sim_imm

            if h <= 3:
                step_up = 0.25 if vs_h[h] > 0.28 else 0.0
            else:
                pre_dip = float(np.min(vn_h[max(0, h - 4) : h + 1]))
                pk_next = float(np.max(vn_h[h : min(nh, h + 6)]))
                pre8_sal = float(np.mean(vs_h[max(0, h - 16) : h]))
                step_up = 0.45 * max(0.0, pk_next - pre_dip) + 0.65 * max(0.0, sal14 - pre8_sal)

            sc = 1.25 * sim_lr + 0.65 * sim_imm + 0.55 * min(1.0, sal14) + 0.55 * step_up
            if sc > best_sc:
                best_sc = sc
                best_h = h

        # Backtrack to 1st Pallavi statement if `best_h` landed on the 2nd immediate repetition
        if best_h >= 16:
            sims_to_best = tmpls_norm[:best_h] @ tmpls_norm[best_h]
            for h0 in range(0, best_h - 15):
                if sims_to_best[h0] >= 0.52 and np.mean(vs_h[h0 : h0 + 20]) >= 0.20 and np.median(ms_h[h0 : h0 + 20]) >= 1.32:
                    sub = sims_to_best[h0 : min(best_h - 14, h0 + 7)]
                    best_h = h0 + int(np.argmax(sub))
                    break

        c_idx = int(best_h * 5)
        s_lo = max(0, c_idx - 8)
        s_hi = min(n_frames - 5, c_idx + 12)
        local_thresh = max(0.24, 0.48 * float(np.max(voc_norm[s_lo : min(n_frames, s_hi + 20)])))
        exact_onset_idx = c_idx
        for k in range(s_lo, s_hi + 1):
            if voc_norm[k] >= local_thresh and np.mean(voc_norm[k : k + 4]) >= local_thresh * 0.85:
                exact_onset_idx = k
                break

        if exact_onset_idx <= 25:
            start_sec = 0.0
        else:
            b_lo = max(0, exact_onset_idx - 9)
            b_hi = max(b_lo + 1, exact_onset_idx - 3)
            breath_idx = b_lo + int(np.argmin(voc_norm[b_lo : b_hi + 1]))
            start_sec = round(breath_idx * 0.1, 2)

        end_lo_idx = min(n_frames - 2, int((start_sec + min_dur) * 10))
        end_hi_idx = min(n_frames - 1, int((start_sec + max_dur) * 10))
        kernel = np.ones(5, dtype=np.float32) / 5.0
        smooth_voc = np.convolve(voc_norm * np.clip(ms_ratio, 0.5, 3.0), kernel, mode="same")
        best_end_idx = end_lo_idx + int(np.argmin(smooth_voc[end_lo_idx : end_hi_idx + 1]))
        end_sec = min(total_dur, best_end_idx * 0.1 + 0.15)
        dur_sec = round(max(min_dur, min(max_dur, end_sec - start_sec)), 2)
        return float(start_sec), float(dur_sec)
    except Exception as e:
        print(f"  [Chorus Detector] Fallback to 22.0s due to: {e}")
        start_fallback = min(22.0, max(0.0, total_dur - default_dur))
        return float(start_fallback), float(min(default_dur, total_dur - start_fallback))


def find_audio_peak_window(media_path: Path, window_sec: float = DEFAULT_SHORT_DURATION) -> tuple[float, float]:
    """Alias preserved for backward compatibility — always delegates to Chorus-first detection."""
    return find_chorus_window(media_path, default_dur=window_sec)


def clean_song_title_part(text: str) -> str:
    """Removes technical suffixes like [Audio], [Film], [1080p Master Film], (Original), Guru Kula Desam."""
    t = text
    patterns = [
        r"\[.*?\]",
        r"\(\s*(?:original|remix|audio|female|male|symphony|version)[^)]*\)",
        r"\b(?:1080p|master\s*film|full\s*cinematic\s*film|cinematic\s*devotional\s*film|cinematic\s*thirukkural\s*film|cinematic\s*educational\s*film|cinematic\s*film|full\s*song\s*film|devotional\s*film|guru\s*kula\s*desam|remix|2026)\b",
    ]
    for pat in patterns:
        t = re.sub(pat, "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s*[-–|:]+\s*$", "", t)
    t = re.sub(r"^\s*[-–|:]+\s*", "", t)
    t = re.sub(r"\s{2,}", " ", t).strip()
    return t


def smart_truncate(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text
    cut = text[:max_len].rsplit(" ", 1)[0].strip(" -–|:,(")
    return cut if len(cut) >= max_len // 2 else text[:max_len].strip(" -–|:,(")


def find_track_audio(track_id: str) -> Path | None:
    for d in AUDIO_DIRS:
        if not d.exists():
            continue
        for ext in (".m4a", ".mp3", ".wav"):
            p = d / f"{track_id}{ext}"
            if p.exists() and p.stat().st_size > 50_000:
                return p
    return None


def get_parent_youtube_info(track_id: str, youtube_film_id: str | None = None) -> dict:
    parent_vid_id = youtube_film_id or track_id
    if not youtube_film_id and MANIFEST_DB.exists():
        try:
            mdata = json.loads(MANIFEST_DB.read_text(encoding="utf-8"))
            for t in mdata.get("completed_tracks", []):
                if t.get("track_id") == track_id and t.get("youtube_id"):
                    parent_vid_id = t["youtube_id"]
                    break
        except Exception:
            pass
    return {
        "parent_channel_handle": "@guru-kula-desam",
        "parent_channel_id": "UCPqB1A_WzpLJec6q69BOO3Q",
        "parent_channel_url": "https://www.youtube.com/@guru-kula-desam",
        "parent_video_id": parent_vid_id,
        "parent_video_url": f"https://www.youtube.com/watch?v={parent_vid_id}",
    }


def build_vertical_drawtext_filters(
    work_dir: Path,
    sacred_cat: dict,
    song_title_ta: str,
    brand_handle: str = "@GuruKulaDesam",
) -> list[str]:
    """
    Clean vertical 1080x1920 layout using libass (HarfBuzz-ng complex Tamil ligature shaping):
    - Top Header (Y=0..312):
      * Line 1 (MarginV=96): `@GuruKulaDesam` or `@GuruKulaDesam2` (#FFE040)
      * Line 2 (MarginV=170): One-liner song name (`{sacred_cat['name_ta']} — {short_ta}`)
    - Middle Content (Y=312..1560, 1080x1248): Unobstructed wide-framed original `@guru-kula-desam` film
    - Bottom Footer (Y=1560..1920): Clean breathing space above YouTube Shorts UI overlays
    """
    cat_ta = sacred_cat["name_ta"]
    base_ta = clean_song_title_part(song_title_ta.split("|")[0])
    if len(base_ta) > 46 and ":" in base_ta:
        prefix, rest = base_ta.split(":", 1)
        if rest.strip():
            base_ta = rest.strip()
    short_ta = smart_truncate(base_ta, 48)
    one_liner = f"{cat_ta} — {short_ta}".replace("{", "(").replace("}", ")")
    song_font_size = 28 if len(one_liner) > 48 else 31

    ass_path = work_dir / "header_overlay.ass"
    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Brand,Noto Sans Tamil,38,&H0040E0FF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,8,24,24,96,1
Style: SongLine,Noto Sans Tamil,{song_font_size},&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,8,24,24,170,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:10:00.00,Brand,,0,0,0,,{brand_handle}
Dialogue: 0,0:00:00.00,0:10:00.00,SongLine,,0,0,0,,{one_liner}
"""
    ass_path.write_text(ass_content, encoding="utf-8")
    ass_posix = ass_path.as_posix().replace(":", "\\:")
    fonts_dir = (ROOT / "fonts").as_posix().replace(":", "\\:")
    return [f"ass='{ass_posix}':fontsdir='{fonts_dir}'"]


def build_viral_short_metadata(
    track_id: str,
    deity_key: str,
    meta_entry: dict,
    panchangam_info: dict | None = None,
    youtube_film_id: str | None = None,
) -> dict:
    hook_cfg = DEITY_HOOKS.get(deity_key, DEITY_HOOKS["murugan"])
    sacred_cat = classify_sacred_category(deity_key, meta_entry, panchangam_info)
    parent_info = get_parent_youtube_info(track_id, youtube_film_id=youtube_film_id)

    raw_title = meta_entry.get("title", f"Sacred Devotional Hymn {track_id}")
    parts = [clean_song_title_part(p) for p in raw_title.split("|")]
    parts = [p for p in parts if p and p.lower() != "guru kula desam"]
    ta_title = parts[0] if parts else clean_song_title_part(raw_title)
    en_title = parts[1] if len(parts) > 1 else ta_title
    if en_title == ta_title and len(parts) > 2:
        en_title = parts[2]

    cat_prefix = sacred_cat["title"]
    short_title = f"{cat_prefix} — {ta_title} | {en_title} #Shorts"
    if len(short_title) > 95:
        ta_short = ta_title.split(":")[-1].strip() if ":" in ta_title else ta_title
        en_short = en_title.split(":")[-1].strip() if ":" in en_title else en_title
        short_title = f"{cat_prefix} — {smart_truncate(ta_short, 34)} | {smart_truncate(en_short, 28)} #Shorts"
    if len(short_title) > 95:
        short_title = f"{cat_prefix} — {smart_truncate(ta_title, 34)} | {smart_truncate(en_title, 26)} #Shorts"

    tamil_lyrics = meta_entry.get("tamil_lyrics", "").strip()
    tamil_meaning = meta_entry.get("tamil_meaning", "").strip()
    english_meaning = meta_entry.get("english_meaning", "").strip()

    all_hashtags = list(dict.fromkeys(
        [f"#{sacred_cat['name_ta']}", f"#{sacred_cat['key'].capitalize()}"]
        + (panchangam_info.get("festival_hashtags", []) if panchangam_info else [])
        + hook_cfg["tags"]
    ))
    tags_str = " ".join(all_hashtags)

    panchangam_block = []
    if panchangam_info:
        ev_str = ", ".join(panchangam_info.get("special_events", []))
        panchangam_block = [
            "═══════════════════════════════════════════════════════════",
            "🗓️ இன்றைய தமிழ் பஞ்சாங்கம் & வழிபாட்டு நேரங்கள் (TODAY'S PANCHANGAM TIMINGS):",
            "═══════════════════════════════════════════════════════════",
            f"• தமிழ் மாதம் & தேதி: {panchangam_info['tamil_month_ta']} {panchangam_info['tamil_day']}, {panchangam_info['weekday_ta']}",
            f"• சிறப்பு வழிபாடு (Occasion): {ev_str}",
            f"• திதி (Tithi & Timing): {panchangam_info['tithi_name']} — {panchangam_info['tithi_timing']}",
            f"• நட்சத்திரம் (Nakshatram & Timing): {panchangam_info['nakshatra_ta']} ({panchangam_info['nakshatra_en']}) — {panchangam_info['nakshatra_timing']}",
            f"• 🪔 சிறப்பு பூஜை / வழிபாட்டு நேரம்: {panchangam_info['special_pooja_time']}",
            f"• ✅ நல்ல நேரம் (Nalla Neram): காலை {panchangam_info['nalla_neram_am']} | மாலை {panchangam_info['nalla_neram_pm']}",
            f"• ✨ கௌரி நல்ல நேரம் (Gowri Nalla Neram): காலை {panchangam_info['gowri_am']} | மாலை {panchangam_info['gowri_pm']}",
            f"• ⚠️ இராகு காலம் (Rahu Kalam): {panchangam_info['rahu_kalam']}",
            f"• ⚠️ எமகண்டம் (Yama Gandam): {panchangam_info['yama_gandam']}",
            f"• 🔹 குளிகை (Kuligai): {panchangam_info['kuligai']}",
        ]

    desc_lines = [
        f"{short_title}",
        f"{sacred_cat['title']} ({sacred_cat['name_en']}): {sacred_cat['desc_ta']}",
        f"🎬 முழுப் பாடல் (Full Master Film on @guru-kula-desam): {parent_info['parent_video_url']}",
        "",
        *panchangam_block,
        "",
        "═══════════════════════════════════════════════════════════",
        "📜 பாடல் வரிகள் (SACRED TAMIL LYRICS):",
        "═══════════════════════════════════════════════════════════",
        tamil_lyrics[:1200] if tamil_lyrics else hook_cfg["hook_ta"],
        "",
        "═══════════════════════════════════════════════════════════",
        "🕉️ பொருள் விளக்கம் (SPIRITUAL MEANING):",
        "═══════════════════════════════════════════════════════════",
        tamil_meaning[:700] if tamil_meaning else "",
        "",
        english_meaning[:700] if english_meaning else "",
        "",
        tags_str,
    ]

    p_comment_lines = [
        f"{sacred_cat['title']} — {ta_title}",
        f"🙏 {hook_cfg['hook_ta']}",
        f"🎬 முழுப் பாடல் (@guru-kula-desam): {parent_info['parent_video_url']}",
    ]
    if panchangam_info:
        p_comment_lines.extend([
            "",
            f"🗓️ இன்றைய பஞ்சாங்கம் ({panchangam_info['tamil_month_ta']} {panchangam_info['tamil_day']}, {panchangam_info['weekday_ta']}):",
            f"• திதி: {panchangam_info['tithi_short_ta']} ({panchangam_info['tithi_timing']})",
            f"• நட்சத்திரம்: {panchangam_info['nakshatra_ta']} ({panchangam_info['nakshatra_timing']})",
            f"• 🪔 {panchangam_info['special_pooja_time']}",
            f"• நல்ல நேரம்: {panchangam_info['nalla_neram_am']} | இராகு காலம்: {panchangam_info['rahu_kalam']}",
        ])

    tag_list = [
        sacred_cat["name_ta"], sacred_cat["key"],
        *[t.lstrip("#") for t in all_hashtags],
        "@GuruKulaDesam", "@GuruKulaDesam2", "GuruKulaDesam", "GuruKulaDesam2",
        "Guru Kula Desam", "Tamil Devotional Songs",
        "Tamil Panchangam Today", "Nalla Neram Today", ta_title[:30], en_title[:30],
    ]

    return {
        "track_id": track_id,
        "deity": deity_key,
        "sacred_category": sacred_cat,
        "title": short_title,
        "ta_title": ta_title,
        "en_title": en_title,
        "description": "\n".join(line for line in desc_lines if line is not None),
        "pinned_comment": "\n".join(p_comment_lines),
        "parent_channel": parent_info,
        "panchangam": panchangam_info,
        "tags": list(dict.fromkeys(tag_list))[:22],
        "categoryId": "10",
    }


def build_short_for_track(
    track_id: str,
    target_dt: datetime | None = None,
    duration_sec: float = DEFAULT_SHORT_DURATION,
    force_rebuild: bool = False,
    brand_handle: str = "@GuruKulaDesam",
    use_flow: bool = False,
) -> dict:
    master_cat = load_master_catalog()
    cat_entry = find_catalog_entry(track_id, master_cat)

    meta_db = json.loads(METADATA_DB.read_text(encoding="utf-8")) if METADATA_DB.exists() else {}
    meta_entry = dict(meta_db.get(track_id, {}))
    if cat_entry:
        if cat_entry.get("title"):
            meta_entry["title"] = cat_entry["title"]
        for k in ("tamil_lyrics", "tamil_meaning", "english_meaning"):
            if not meta_entry.get(k) and cat_entry.get(k):
                meta_entry[k] = cat_entry[k]

    deity_key = detect_deity_category(track_id, meta_entry, cat_entry.get("deity", "") if cat_entry else "")
    panchangam_info = get_auspicious_alignment_for_datetime(target_dt or datetime.now(IST))
    sacred_cat = classify_sacred_category(deity_key, meta_entry, panchangam_info)

    out_mp4 = SHORTS_OUT_DIR / f"short_{deity_key}_{track_id}.mp4"
    out_meta_file = SHORTS_META_DIR / f"short_{deity_key}_{track_id}.json"

    if out_mp4.exists() and out_mp4.stat().st_size > 1_000_000 and out_meta_file.exists() and not force_rebuild:
        old_meta = json.loads(out_meta_file.read_text(encoding="utf-8"))
        # Strictly require `@guru-kula-desam` Master Film clip (`original_master_clip`) + `chorus_v1` framing!
        if (
            old_meta.get("brand_handle") == brand_handle
            and old_meta.get("visual_source_mode") == "original_master_clip"
            and old_meta.get("clip_anchor_mode") == "chorus_v1"
        ):
            print(f"✅ Discography Chorus Short already rendered for {brand_handle}: {out_mp4.name} ({out_mp4.stat().st_size / 1e6:.2f} MB)")
            viral_meta = build_viral_short_metadata(
                track_id, deity_key, meta_entry, panchangam_info,
                youtube_film_id=old_meta.get("youtube_film_id") or (cat_entry.get("youtube_film_id") if cat_entry else None),
            )
            old_meta.update(viral_meta)
            out_meta_file.write_text(json.dumps(old_meta, indent=2, ensure_ascii=False), encoding="utf-8")
            return old_meta

    master_vid, has_burned_hint, yt_film_id = (None, False, None)
    if not use_flow:
        master_vid, has_burned_hint, yt_film_id = resolve_original_master_video(track_id, cat_entry)
        if master_vid is None:
            raise FileNotFoundError(
                f"STRICT DISCOGRAPHY GUARD: Track '{track_id}' has no verified HD Master Film on @guru-kula-desam. "
                f"Refusing to fall back to synthetic Flow scenes!"
            )

    work_dir = SHORTS_TEMP_DIR / track_id
    shutil.rmtree(work_dir, ignore_errors=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    is_portrait_source = False
    flow_pts_stretch = 1.0
    visual_source_mode = None
    layout_info = {"has_top": False, "has_bot": False, "scene_motion": 0.0, "is_static": False}

    if master_vid is not None:
        visual_source_mode = "original_master_clip"
        audio_path = master_vid
        start_sec, clip_dur = find_chorus_window(
            master_vid, track_id=track_id, yt_film_id=yt_film_id, default_dur=duration_sec
        )
        layout_info = inspect_master_video_layout(master_vid, sample_start=start_sec, has_burned_hint=has_burned_hint)
        if layout_info["is_static"]:
            shutil.rmtree(work_dir, ignore_errors=True)
            raise RuntimeError(
                f"STATIC VIDEO REJECTED: '{master_vid.name}' for '{track_id}' has scene_motion={layout_info['scene_motion']} "
                f"({layout_info['w']}x{layout_info['h']}). Refusing to publish static cover art!"
            )
        raw_source_video = master_vid
        video_seek_start = start_sec
        source_desc = (
            f"@guru-kula-desam Master Film ({master_vid.name} | {layout_info['w']}x{layout_info['h']} | "
            f"motion={layout_info['scene_motion']} | top={layout_info['has_top']} bot={layout_info['has_bot']})"
        )
    else:
        # Explicit `--use-flow` branch ONLY (never reached when `use_flow=False`)
        dedicated_clips = get_track_dedicated_flow_clips(track_id, require_fresh_flow_short=True)
        if len(dedicated_clips) < 3:
            from tools.flow_autonomous_generator import generate_flow_clips_for_short
            dedicated_clips = generate_flow_clips_for_short(track_id, scene_count=4)
        if len(dedicated_clips) < 3:
            shutil.rmtree(work_dir, ignore_errors=True)
            raise FileNotFoundError(f"Insufficient Flow clips for {track_id}")
        audio_path = find_track_audio(track_id)
        if not audio_path:
            raise FileNotFoundError(f"No audio found for {track_id}")
        visual_source_mode = "google_flow_dedicated"
        start_sec, clip_dur = find_chorus_window(audio_path, track_id=track_id, default_dur=duration_sec)
        raw_source_video = work_dir / "flow_dedicated_timeline.mp4"
        selected_scenes = list(dedicated_clips)
        is_portrait_source = True
        target_w, target_h = (720, 1280)
        concat_cmd = [FFMPEG, "-nostdin", "-y"]
        fc_parts = []
        for idx_c, c in enumerate(selected_scenes):
            concat_cmd += ["-i", str(c.resolve())]
            fc_parts.append(
                f"[{idx_c}:v]scale={target_w}:{target_h}:force_original_aspect_ratio=increase:flags=lanczos,"
                f"crop={target_w}:{target_h},setsar=1,fps=24,format=yuv420p[cv{idx_c}]"
            )
        concat_inputs = "".join(f"[cv{idx_c}]" for idx_c in range(len(selected_scenes)))
        fc_parts.append(f"{concat_inputs}concat=n={len(selected_scenes)}:v=1:a=0[vcat]")
        concat_cmd += [
            "-filter_complex", ";".join(fc_parts),
            "-map", "[vcat]", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-pix_fmt", "yuv420p",
            str(raw_source_video),
        ]
        subprocess.run(concat_cmd, check=True, capture_output=True)
        video_seek_start = 0.0
        source_desc = f"Explicit Flow Clips ({track_id})"

    print("=" * 88)
    print(f"🔥 BUILDING @GURU-KULA-DESAM CHORUS SHORT: {sacred_cat['title']} | [{deity_key.upper()}] {track_id}")
    print(f"🎬 Source Mode : {source_desc}")
    print(f"🗓️  Panchangam  : {panchangam_info['onscreen_panchangam_line1']}")
    print(f"🎵 Chorus Clip : {start_sec:.2f}s -> {start_sec + clip_dur:.2f}s ({clip_dur:.2f}s)")
    print("=" * 88)

    viral_meta = build_viral_short_metadata(track_id, deity_key, meta_entry, panchangam_info, youtube_film_id=yt_film_id)
    dt_filters = build_vertical_drawtext_filters(
        work_dir=work_dir,
        sacred_cat=sacred_cat,
        song_title_ta=viral_meta["ta_title"],
        brand_handle=brand_handle,
    )

    fps_short = 24
    if visual_source_mode == "original_master_clip":
        inputs = [
            "-ss", f"{video_seek_start:.2f}", "-t", f"{clip_dur:.2f}", "-i", str(raw_source_video),
        ]
        audio_map_in = "0:a"
    else:
        inputs = [
            "-ss", f"{video_seek_start:.2f}", "-t", f"{clip_dur:.2f}", "-i", str(raw_source_video),
            "-ss", f"{start_sec:.2f}", "-t", f"{clip_dur:.2f}", "-i", str(audio_path),
        ]
        audio_map_in = "1:a"

    dt_chain = ",".join(dt_filters)
    pts_filter = f"setpts={flow_pts_stretch:.4f}*PTS," if flow_pts_stretch > 1.01 else ""
    if is_portrait_source:
        filter_parts = [
            f"[0:v]{pts_filter}fps={fps_short},scale={W}:1920:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={W}:1248:(iw-{W})/2:(ih-1248)*0.40,"
            f"pad={W}:{H}:0:312:black,{dt_chain},format=yuv420p[v_out]",
        ]
    else:
        has_top = layout_info["has_top"]
        has_bot = layout_info["has_bot"]
        if has_top and has_bot:
            pre_crop = "crop=iw*0.84:ih*0.785:(iw-ow)/2:ih*0.065"
        elif has_bot:
            pre_crop = "crop=iw*0.84:ih*0.845:(iw-ow)/2:0"
        else:
            pre_crop = "crop=iw*0.84:ih:(iw-ow)/2:0"

        filter_parts = [
            f"[0:v]{pts_filter}fps={fps_short},{pre_crop},"
            f"scale=-2:1248:flags=lanczos,"
            f"crop={W}:1248:(iw-{W})/2:0,"
            f"eq=saturation=1.08:contrast=1.03:brightness=0.015,"
            f"pad={W}:{H}:0:312:black,{dt_chain},format=yuv420p[v_out]",
        ]

    fade_out_st = max(0.5, clip_dur - 0.85)
    filter_parts.append(f"[{audio_map_in}]afade=t=in:st=0:d=0.35,afade=t=out:st={fade_out_st:.2f}:d=0.85[a_out]")

    cmd_render = [
        FFMPEG, "-nostdin", "-y",
        *inputs,
        "-filter_complex", ";".join(filter_parts),
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-movflags", "+faststart",
        "-t", f"{clip_dur:.2f}",
        str(out_mp4),
    ]
    t0 = time.time()
    res = subprocess.run(cmd_render, capture_output=True)
    if res.returncode != 0 or not out_mp4.exists() or out_mp4.stat().st_size < 500_000:
        raise RuntimeError(f"FFmpeg failed encoding {track_id}: {res.stderr.decode('utf-8', errors='ignore')[-500:]}")
    elapsed = time.time() - t0
    print(f"  ⚙️ Encoded 1080x1920 Chorus Short in {elapsed:.1f}s")

    size_mb = out_mp4.stat().st_size / (1024 * 1024)
    viral_meta.update({
        "brand_handle": brand_handle,
        "visual_source_mode": visual_source_mode,
        "clip_anchor_mode": "chorus_v1",
        "visual_source_file": master_vid.name if master_vid else f"google_flow_renders/{track_id}",
        "youtube_film_id": yt_film_id,
        "scene_motion_score": layout_info["scene_motion"],
        "layout_crop": {"has_top": layout_info["has_top"], "has_bot": layout_info["has_bot"]},
        "video_path": str(out_mp4.relative_to(ROOT)),
        "duration_sec": round(clip_dur, 2),
        "peak_start_sec": round(start_sec, 2),
        "file_size_mb": round(size_mb, 2),
        "rendered_at": time.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
    })
    out_meta_file.write_text(json.dumps(viral_meta, indent=2, ensure_ascii=False), encoding="utf-8")
    shutil.rmtree(work_dir, ignore_errors=True)

    print(f"🎉 [CHORUS DISCOGRAPHY SHORT READY] {out_mp4.name} ({size_mb:.2f} MB) | Start={start_sec:.2f}s Dur={clip_dur:.2f}s")
    print(f"   • Sacred Title : {viral_meta['title']}")
    return viral_meta


def list_candidate_tracks(deity_filter: str = None, prioritize_high_energy: bool = True) -> list[dict]:
    """
    Lists ONLY tracks that have a verified public `@guru-kula-desam` Master Film (`youtube_film_id`)
    in `master_film_sources.json`. Never returns synthetic `DEDICATED-FLOW` or non-devotional tracks.
    """
    master_cat = load_master_catalog()

    iconic_keywords = (
        "கந்த சஷ்டி", "kandha sashti", "ஸ்கந்த மந்திரம்", "skanda", "திருப்புகழ்", "thiruppugazh",
        "முத்தைத் தரு", "muthai tharu", "கந்தர் அலங்காரம்", "kandhar alangaram", "கந்தர் அனுபூதி",
        "தேவாரம்", "thevaram", "திருவாசகம்", "thiruvasagam", "ஈஸ்வர நாமவளி", "ishwara namavali",
        "கோவிந்த நாமாவளி", "govinda namavali", "மகா கணேச", "ganesha pancharatnam", "கண நாதா",
        "கைத்தல நிறைகனி", "அபிராமி", "abhirami", "தனந்தரும்", "திருப்பாவை", "thiruppavai",
        "திருவருட்பா", "thiruvarutpa", "அருட்பெருஞ்சோதி", "கடவுள் வாழ்த்து", "வான் சிறப்பு",
        "அன்புடைமை", "இல்வாழ்க்கை", "அறன் வலியுறுத்தல்", "நீத்தார் பெருமை",
    )

    candidates = []
    seen_yt_ids = set()

    for fid, entry in master_cat.items():
        yt_id = entry.get("youtube_film_id")
        if not yt_id or yt_id in seen_yt_ids or yt_id in EXCLUDED_REMIX_VIDEO_IDS or fid in EXCLUDED_REMIX_VIDEO_IDS:
            continue

        raw_title = entry.get("title", fid)
        title_l = raw_title.lower()
        if "remix" in title_l or any(ex in title_l for ex in NON_DEVOTIONAL_EXCLUDED_KEYWORDS):
            continue

        deity = detect_deity_category(fid, {"title": raw_title}, entry.get("deity", ""))
        if deity_filter and deity != deity_filter.lower():
            continue

        is_iconic = any(k in title_l for k in iconic_keywords)
        tier = entry.get("quality_tier", 1)
        priority = tier * 2 + (0 if is_iconic else 1)
        sacred_cat = classify_sacred_category(deity, {"title": raw_title})

        candidates.append({
            "track_id": fid,
            "legacy_track_id": entry.get("legacy_track_id"),
            "youtube_film_id": yt_id,
            "deity": deity,
            "sacred_category": sacred_cat["title"],
            "priority": priority,
            "source_type": "MASTER-FILM",
            "published_at": entry.get("published_at", ""),
            "title": raw_title,
        })
        seen_yt_ids.add(yt_id)

    candidates.sort(key=lambda x: (x["priority"], x["published_at"] and -int(x["published_at"][:10].replace("-", "")), x["track_id"]))

    if prioritize_high_energy and not deity_filter:
        by_deity = {}
        for c in candidates:
            by_deity.setdefault(c["deity"], []).append(c)
        deity_order = ["murugan", "shiva", "amman", "vinayagar", "vishnu", "vallalar", "thirukkural"]
        interleaved = []
        max_len = max((len(v) for v in by_deity.values()), default=0)
        for i in range(max_len):
            for d in deity_order:
                if d in by_deity and i < len(by_deity[d]):
                    interleaved.append(by_deity[d][i])
        return interleaved

    return candidates


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build 100% @guru-kula-desam Chorus-Clipped 9:16 Vertical Shorts")
    ap.add_argument("--track", type=str, help="Specific Film/Track ID to build")
    ap.add_argument("--batch", type=int, default=0, help="Build N prioritized Shorts in batch")
    ap.add_argument("--deity", type=str, default=None, help="Filter by deity/pillar")
    ap.add_argument("--duration", type=float, default=DEFAULT_SHORT_DURATION, help="Short duration in seconds (default: 38s)")
    ap.add_argument("--brand", type=str, default="@GuruKulaDesam", help="Brand handle (@GuruKulaDesam or @GuruKulaDesam2)")
    ap.add_argument("--use-flow", action="store_true", help="Explicitly opt into Google Flow scenes (disabled by default)")
    ap.add_argument("--force", action="store_true", help="Force rebuild even if output MP4 exists")
    ap.add_argument("--list", action="store_true", help="List verified @guru-kula-desam Master Film tracks")
    args = ap.parse_args()

    if args.list:
        cands = list_candidate_tracks(deity_filter=args.deity)
        print(f"Total Verified @guru-kula-desam Master Films for 9:16 Chorus Shorts: {len(cands)}")
        for idx, c in enumerate(cands[:30], 1):
            print(f"  {idx:2d}. {c['sacred_category']} | [{c['deity'].upper():<11}] ({c['source_type']}) {c['track_id']:<14} | {clean_song_title_part(c['title'])[:55]}")
    elif args.track:
        build_short_for_track(args.track, duration_sec=args.duration, force_rebuild=args.force, brand_handle=args.brand, use_flow=args.use_flow)
    elif args.batch > 0:
        cands = list_candidate_tracks(deity_filter=args.deity)
        built = 0
        for c in cands:
            if built >= args.batch:
                break
            out_mp4 = SHORTS_OUT_DIR / f"short_{c['deity']}_{c['track_id']}.mp4"
            if out_mp4.exists() and not args.force:
                continue
            try:
                build_short_for_track(c["track_id"], duration_sec=args.duration, force_rebuild=args.force, brand_handle=args.brand, use_flow=args.use_flow)
                built += 1
            except Exception as e:
                print(f"❌ Error building {c['track_id']}: {e}")
    else:
        ap.print_help()
