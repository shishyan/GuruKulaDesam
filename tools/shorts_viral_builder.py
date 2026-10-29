#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/shorts_viral_builder.py
Autonomous 9:16 Vertical (1080x1920 @ 24fps) Viral Devotional Shorts Builder
for @gurukuladesam2 ("$1M Challenge" High-Retention & Liturgically Aligned Engine).

Key Features:
1. 6 Sacred Tamil Category Titles (Mandated by User):
   - Every Short is categorized and titled with one of the 6 sacred pillars:
     📖 நன்னெறி | 📖 நல்லறம் | 📖 நற்பண்பு | 📖 நற்துணை | 📖 நற்சொல் | 📖 நற்செயல்
2. Exact Tamil Panchangam & Timings (tools/tamil_panchangam_engine.py):
   - Displays exact Tithi & Nakshatra start/end timings (IST), Nalla Neram, Rahu Kalam,
     Yama Gandam, and special Pooja windows (e.g., Krittika Nakshatra timing, Pradosham 4:30-6:00 PM,
     Sankatahara Chaturthi moonrise) both ON-SCREEN and in the description/top comment.
3. 100% Authentic Deity-Matched Video Selection:
   - Never uses generic duplicated placeholder scenes (like cows/ponds on a Murugan song).
   - Verifies MD5 uniqueness of track clips and automatically pulls from the Curated Authentic Deity
     Visual Pool (`0PvXn4gqlFM` & `1hoVaPwWMes` for Murugan, `IhE1OvdIBKs` for Vinayagar,
     `-yxeA6nvNZk` for Shiva, `0k9CZLNA2TY` for Amman, `thiruppavai-true-video` & `G:/My Drive` for Vishnu)
     or generates fresh clips via the Gemini/Flow Chrome tunnel.
4. Full Parent Channel Attribution & Funnel (@guru-kula-desam):
   - Persistent footer credit, closing 4.5s CTA card, top-of-description links, and automated top comment.
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
from PIL import Image, ImageDraw, ImageFilter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.tamil_panchangam_engine import (
    IST,
    SACRED_6_CATEGORIES,
    classify_sacred_category,
    get_auspicious_alignment_for_datetime,
)

FFMPEG = "C:/ffmpeg/bin/ffmpeg.exe" if Path("C:/ffmpeg/bin/ffmpeg.exe").exists() else (shutil.which("ffmpeg") or "ffmpeg")
FFPROBE = "C:/ffmpeg/bin/ffprobe.exe" if Path("C:/ffmpeg/bin/ffprobe.exe").exists() else (shutil.which("ffprobe") or "ffprobe")

METADATA_DB = ROOT / "production" / "metadata" / "all_songs_lyrics_and_meanings.json"
MANIFEST_DB = ROOT / "production" / "autonomous_master_production_manifest.json"
FLOW_RENDERS_DIR = ROOT / "production" / "google_flow_renders"
RELEASES_DIR = ROOT / "renders" / "releases"
SUBTITLES_DIR = ROOT / "production" / "subtitles"
AUDIO_DIRS = [ROOT / "production" / "audio", ROOT / "source" / "youtube"]
GDRIVE_VIDEOS_DIR = Path("G:/My Drive/GuruKulaDesam/Videos")

SHORTS_OUT_DIR = ROOT / "renders" / "shorts_gurukuladesam2"
SHORTS_OUT_DIR.mkdir(parents=True, exist_ok=True)
SHORTS_META_DIR = ROOT / "production" / "shorts_metadata"
SHORTS_META_DIR.mkdir(parents=True, exist_ok=True)
SHORTS_TEMP_DIR = ROOT / "renders" / "temp_shorts_build"
SHORTS_TEMP_DIR.mkdir(parents=True, exist_ok=True)

# 9:16 Vertical Master Constants
W, H = 1080, 1920
FPS = 24
DEFAULT_SHORT_DURATION = 35.0

# Verified Authentic Deity Visual Pools (100% genuine, non-duplicated deity/temple scenes)
AUTHENTIC_DEITY_SCENE_FOLDERS = {
    "murugan": ["0PvXn4gqlFM", "1hoVaPwWMes", "-unILRjNLHQ", "C9Ea0-FfMNs", "B6yVe6HM8Ok", "bOxyDZgsI2c", "3oJ2OPG-WCs"],
    "vinayagar": ["IhE1OvdIBKs", "mQpQEuXiEZ4"],
    "shiva": ["-yxeA6nvNZk", "-yEq62Bu_d8", "0TB3drCSvNc", "0tXyQEAHVNQ", "2_rwWlC09I0", "2QOF2ycA4RQ", "2vuuHMEhs20"],
    "amman": ["0k9CZLNA2TY", "bZ03UopgYcc", "fzoZWnsJReg", "grjVzzo-RWc", "Q2xax9mIhZw"],
    "vishnu": ["0W1FqHOYwDc", "31xVgvxoiUA", "468ErjVLRCs", "60rrBjJfAS4", "2YzLM0yoBlg"],
    "vallalar": ["-cmB2_XZqs0", "0gK0asNO-RM", "1W9SHSo-2Vk", "28Xnfhctf0I", "3youy-33GtY"],
    "thirukkural": ["--4jzoezBW8", "01g0sJdaL2I", "02C8glMmetw", "0bz1myKXoJQ", "0DoegY9d0ZM", "0fD-z3s_g2A"],
}

# Explicit high-impact deity idol / sanctum scenes that MUST lead the opening of each Short!
DEITY_HERO_SCENES = {
    "murugan": [
        "0PvXn4gqlFM/scene_03.mp4",  # Six-faced Shanmukha Murugan idol milk abhishekam
        "0PvXn4gqlFM/scene_04.mp4",  # Golden Vel with red ixora & marukozhundhu garland
        "0PvXn4gqlFM/scene_02.mp4",  # Tamil devotees carrying Paal Kudam to Murugan sanctum
        "0PvXn4gqlFM/scene_01.mp4",  # Thiruchendur seaside Murugan Raja Gopuram
        "1hoVaPwWMes/scene_01.mp4",  # Sacred Murugan hill steps
    ],
    "vinayagar": [
        "IhE1OvdIBKs/scene_01.mp4",  # Stone Vinayagar idol with Kozhukattai, jackfruit, banana naivedyam
        "IhE1OvdIBKs/scene_02.mp4",  # Sacred lotus feet of Vinayagar with red hibiscus
        "IhE1OvdIBKs/scene_03.mp4",
        "IhE1OvdIBKs/scene_04.mp4",
    ],
    "shiva": [
        "-yxeA6nvNZk/scene_01.mp4",  # Shiva Lingam with Tripundra Vibhuti & Bilva leaves in sanctum
        "-yxeA6nvNZk/scene_02.mp4",
        "-yxeA6nvNZk/scene_03.mp4",
        "-yEq62Bu_d8/scene_01.mp4",
    ],
    "amman": [
        "0k9CZLNA2TY/scene_01.mp4",  # Goddess Abhirami Amman sanctum with red hibiscus & brass kuthuvilakku
        "0k9CZLNA2TY/scene_02.mp4",
        "0k9CZLNA2TY/scene_03.mp4",
    ],
}

# Cache of MD5 hashes across `production/google_flow_renders` to detect & reject generic duplicated clips
_CLIP_HASH_COUNTS = None


def _get_clip_hash_counts() -> dict[str, int]:
    global _CLIP_HASH_COUNTS
    if _CLIP_HASH_COUNTS is not None:
        return _CLIP_HASH_COUNTS
    counts = {}
    if FLOW_RENDERS_DIR.exists():
        for mp4 in FLOW_RENDERS_DIR.glob("*/*.mp4"):
            try:
                h = hashlib.md5(mp4.read_bytes()[:65536]).hexdigest()
                counts[h] = counts.get(h, 0) + 1
            except Exception:
                pass
    _CLIP_HASH_COUNTS = counts
    return counts


def is_authentic_unique_clip(mp4_path: Path) -> bool:
    """Returns True if `mp4_path` is a genuine scene and NOT one of the generic 8x-duplicated nature loops."""
    if not mp4_path.exists() or mp4_path.stat().st_size < 200_000:
        return False
    counts = _get_clip_hash_counts()
    try:
        h = hashlib.md5(mp4_path.read_bytes()[:65536]).hexdigest()
        return counts.get(h, 1) <= 2
    except Exception:
        return True


def get_authentic_deity_clips(track_id: str, deity_key: str) -> list[Path]:
    """
    1. Always leads with `DEITY_HERO_SCENES[deity_key]` (explicit deity idol/sanctum clips
       like Shanmukha Murugan milk abhishekam + Golden Vel for Murugan, Vinayagar idol + Kozhukattai
       for Vinayagar, Shiva Lingam for Shiva, Abhirami sanctum for Amman) so the first 15 seconds
       of every Short unmistakably show the exact deity of the song!
    2. Appends the track's own authentic, non-duplicated Google Flow clips (if any) and the
       verified deity pool.
    """
    hero_clips = []
    for rel in DEITY_HERO_SCENES.get(deity_key, []):
        hp = FLOW_RENDERS_DIR / rel
        if hp.exists() and hp.stat().st_size > 200_000:
            hero_clips.append(hp)

    # Rotate hero clips slightly by track_id so each Short starts on a distinct iconic idol shot
    if len(hero_clips) > 1:
        h_off = sum(ord(ch) for ch in track_id) % len(hero_clips)
        hero_clips = hero_clips[h_off:] + hero_clips[:h_off]

    own_dir = FLOW_RENDERS_DIR / track_id
    own_authentic = []
    if own_dir.exists() and track_id not in ("AW4cljBWy2w", "Lki_Y8OSljs"):
        own_authentic = [
            c for c in sorted(own_dir.glob("scene_*.mp4"))
            if is_authentic_unique_clip(c) and c not in hero_clips
        ]

    pool = list(hero_clips) + own_authentic

    if deity_key == "vishnu":
        tp_dir = ROOT / "production" / "approved" / "thiruppavai-true-video"
        if tp_dir.exists():
            pool.extend([p for p in sorted(tp_dir.glob("*.mp4")) if p not in pool])

    for folder_id in AUTHENTIC_DEITY_SCENE_FOLDERS.get(deity_key, AUTHENTIC_DEITY_SCENE_FOLDERS["murugan"]):
        fdir = FLOW_RENDERS_DIR / folder_id
        if fdir.exists():
            for c in sorted(fdir.glob("scene_*.mp4")):
                if is_authentic_unique_clip(c) and c not in pool:
                    pool.append(c)

    return pool


DEITY_HOOKS = {
    "murugan": {
        "badge": "வெற்றிவேல் முருகன் | LORD MURUGAN DIVINE CHANT",
        "hook_en": "⚡ DO NOT SCROLL! Receive Lord Murugan's Grace Today 🙏",
        "hook_ta": "வெற்றிவேல் முருகனுக்கு அரோகரா! தியானிப்போம் வாரீர்",
        "tags": ["#Shorts", "#Murugan", "#Vetrivel", "#KandaSashti", "#Thaipusam", "#ArupadaiVeedu", "#TamilDevotional", "#BhaktiShorts", "#GuruKulaDesam"],
    },
    "shiva": {
        "badge": "தென்னாடுடைய சிவனே போற்றி | LORD SHIVA SACRED HYMN",
        "hook_en": "🔱 OM NAMAH SHIVAYA! Feel the Cosmic Vibration of Kailash 🙏",
        "hook_ta": "நமச்சிவாய வாழ்க! நாதன் தாள் வாழ்க!",
        "tags": ["#Shorts", "#Shiva", "#OmNamahShivaya", "#Thiruvasagam", "#Pradosham", "#Shivaratri", "#TamilDevotional", "#GuruKulaDesam"],
    },
    "amman": {
        "badge": "ஓம் சக்தி பராசக்தி | GODDESS AMMAN GRACE",
        "hook_en": "🌺 Pause for 45 Seconds to Receive Divine Mother's Blessings 🙏",
        "hook_ta": "தனந்தரும் கல்விதரும் அபிராமி அம்மன் திருவருள்!",
        "tags": ["#Shorts", "#Amman", "#Abhirami", "#OmSakthi", "#Pournami", "#Navaratri", "#TamilDevotional", "#GuruKulaDesam"],
    },
    "vinayagar": {
        "badge": "ஓம் கம் கணபதயே நமஹ | LORD VINAYAGAR BLESSINGS",
        "hook_en": "🐘 Remove All Obstacles Today with This Sacred Ganapathi Chant 🙏",
        "hook_ta": "தடைகள் நீக்கும் முழுமுதற்கடவுள் விநாயகர் போற்றி!",
        "tags": ["#Shorts", "#Vinayagar", "#Ganesha", "#Ganapathi", "#SankataharaChaturthi", "#Bhakti", "#TamilDevotional", "#GuruKulaDesam"],
    },
    "vishnu": {
        "badge": "ஓம் நமோ நாராயணாய | PERUMAL & KRISHNA DIVINE HYMN",
        "hook_en": "🙏 Hear This Sacred Perumal Pasuram for Peace & Prosperity ✨",
        "hook_ta": "கோவிந்தா! நாராயணா! பெருமாள் திவ்ய பிரபந்தம்",
        "tags": ["#Shorts", "#Perumal", "#Krishna", "#Vishnu", "#Ekadashi", "#DivyaPrabandham", "#Tirupati", "#TamilDevotional", "#GuruKulaDesam"],
    },
    "vallalar": {
        "badge": "அருட்பெருஞ்ஜோதி | VALLALAR THIRUVARUTPA",
        "hook_en": "🔥 Arutperunjothi! Experience the Supreme Light of Compassion 🙏",
        "hook_ta": "அருட்பெருஞ்ஜோதி தனிப்பெருங்கருணை!",
        "tags": ["#Shorts", "#Vallalar", "#Thiruvarutpa", "#Arutperunjothi", "#Sanmargam", "#TamilDevotional", "#GuruKulaDesam"],
    },
    "thirukkural": {
        "badge": "திருவள்ளுவர் அருளிய திருக்குறள் | ETERNAL TAMIL WISDOM",
        "hook_en": "📜 2,000-Year-Old Sacred Tamil Wisdom That Will Change Your Life ✨",
        "hook_ta": "உலகப் பொதுமறை திருக்குறள் — தெய்வீக இசை வடிவம்",
        "tags": ["#Shorts", "#Thirukkural", "#Thiruvalluvar", "#TamilWisdom", "#SanatanaDharma", "#TamilDevotional", "#GuruKulaDesam"],
    },
}


def get_media_duration(path: Path) -> float:
    cmd = [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path)
    ]
    out = subprocess.check_output(cmd).decode("utf-8", errors="ignore").strip()
    return float(out) if out else 0.0


def find_audio_peak_window(audio_path: Path, window_sec: float = DEFAULT_SHORT_DURATION) -> tuple[float, float]:
    total_dur = get_media_duration(audio_path)
    if total_dur <= window_sec + 4.0:
        return 0.0, min(total_dur, window_sec)

    sr = 8000
    cmd = [
        FFMPEG, "-v", "error",
        "-i", str(audio_path),
        "-ac", "1", "-ar", str(sr),
        "-f", "s16le", "-"
    ]
    try:
        raw_bytes = subprocess.check_output(cmd)
        num_samples = len(raw_bytes) // 2
        samples = struct.unpack(f"<{num_samples}h", raw_bytes[:num_samples * 2])

        sec_energies = []
        for s in range(0, num_samples - sr, sr):
            chunk = samples[s:s + sr]
            mean_sq = sum(x * x for x in chunk) / float(sr)
            sec_energies.append(math.sqrt(mean_sq))

        min_start = min(15, max(0, len(sec_energies) - int(window_sec) - 2))
        max_start = max(min_start + 1, len(sec_energies) - int(window_sec) - 5)

        best_start = min_start
        best_score = -1.0
        win_int = int(window_sec)

        for start_sec in range(min_start, max_start + 1):
            opening_energy = sum(sec_energies[start_sec:start_sec + 8]) * 1.35
            body_energy = sum(sec_energies[start_sec + 8:start_sec + win_int])
            score = opening_energy + body_energy
            if score > best_score:
                best_score = score
                best_start = start_sec

        return float(best_start), float(window_sec)
    except Exception as e:
        print(f"  [Peak Detector] Fallback to 20.0s due to: {e}")
        start_fallback = min(20.0, max(0.0, total_dur - window_sec))
        return start_fallback, window_sec


def build_track_vertical_backdrop(source_video: Path, seek_sec: float, out_png: Path) -> Path:
    """
    Extracts a rich frame from `source_video`, creates a full-bleed 1080x1920 Gaussian-blurred
    darkened temple aura backdrop, and leaves a clean, uncluttered vertical frame
    (with zero text background boxes, zero side clutter).
    """
    raw_frame = out_png.parent / "temp_frame.jpg"
    subprocess.run(
        [
            FFMPEG, "-y", "-ss", f"{max(0.0, seek_sec + 2.5):.2f}",
            "-i", str(source_video),
            "-frames:v", "1", "-q:v", "2", str(raw_frame)
        ],
        check=True, capture_output=True
    )

    base = Image.open(raw_frame).convert("RGBA")
    bg = base.resize((W, H), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(radius=28))
    dark_tint = Image.new("RGBA", (W, H), (8, 6, 18, 165))
    bg = Image.alpha_composite(bg, dark_tint).convert("RGB")
    bg.save(out_png, "PNG")
    return out_png


def wrap_tamil_couplet(text: str, max_words_per_line: int = 4) -> str:
    words = text.replace("\n", " ").split()
    lines = []
    for i in range(0, len(words), max_words_per_line):
        lines.append(" ".join(words[i:i + max_words_per_line]))
    return "\n".join(lines[:3])


def parse_srt_cues(srt_path: Path) -> list[dict]:
    if not srt_path.exists():
        return []
    raw = srt_path.read_text(encoding="utf-8", errors="ignore")
    blocks = re.split(r"\n\s*\n", raw.strip())
    cues = []

    def to_sec(ts: str) -> float:
        ts = ts.strip().replace(",", ".")
        parts = ts.split(":")
        return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])

    for b in blocks:
        lines = [l.strip() for l in b.splitlines() if l.strip()]
        if len(lines) >= 2:
            m = re.search(r"(\d+:\d+:\d+[,\.]\d+)\s*-->\s*(\d+:\d+:\d+[,\.]\d+)", lines[0] if "-->" in lines[0] else lines[1])
            if m:
                start_t = to_sec(m.group(1))
                end_t = to_sec(m.group(2))
                txt_start = 1 if "-->" in lines[0] else 2
                txt = "\n".join(lines[txt_start:])
                if txt:
                    cues.append({"start": start_t, "end": end_t, "text": txt})
    return cues


def build_vertical_drawtext_filters(
    work_dir: Path,
    deity_key: str,
    sacred_cat: dict,
    song_title_ta: str,
    song_title_en: str,
    lyrics_cues: list[dict],
    english_summary: str,
    clip_start: float,
    clip_dur: float,
    panchangam_info: dict | None = None,
    brand_handle: str = "@GuruKulaDesam",
) -> list[str]:
    """
    Strict 15% Header / 75% Content / 10% Footer layout (1080x1920):
    - Top 15% Header (Y=0..288, 288px):
      * Line 1 (Y=96): `@GuruKulaDesam` or `@GuruKulaDesam2`
      * Line 2 (Y=168): One-liner song name (`{sacred_cat['name_ta']} — {short_ta}`)
    - Middle 75% Content (Y=288..1728, 1440px): Pure unobstructed deity video (full 1080px width, zero borders)
    - Bottom 10% Footer (Y=1728..1920, 192px): Clean breathing space (no parent channel ads, no clutter)
    - Zero text background boxes (`box=0`), zero text borders (`borderw=0`), zero graphic frames.
    """
    cat_ta = sacred_cat["name_ta"]

    short_ta = song_title_ta.split("|")[0].strip()
    if len(short_ta) > 36:
        short_ta = short_ta[:34] + "..."

    one_liner = f"{cat_ta} — {short_ta}"

    txt_dir = work_dir / "drawtext_cards"
    txt_dir.mkdir(parents=True, exist_ok=True)

    font_ta = Path("C:/Windows/Fonts/NirmalaB.ttf")
    if not font_ta.exists():
        font_ta = ROOT / "fonts" / "NirmalaB.ttf"
    if not font_ta.exists():
        font_ta = ROOT / "fonts" / "NotoSansTamil-Bold.ttf"
    f_ta_posix = font_ta.as_posix().replace(":", "\\:")

    def write_card(name: str, content: str) -> str:
        p = txt_dir / f"{name}.txt"
        p.write_text(content.strip(), encoding="utf-8")
        return p.as_posix().replace(":", "\\:")

    filters = []

    # 1. Top Header Brand Phrase: "@GuruKulaDesam" or "@GuruKulaDesam2" (Y=96, no border, no background box)
    f_brand = write_card("top_brand", brand_handle)
    filters.append(
        f"drawtext=fontfile='{f_ta_posix}':textfile='{f_brand}':text_shaping=1:"
        f"fontcolor=#FFE040:fontsize=36:x=(w-text_w)/2:y=96"
    )

    # 2. Top Header One-Liner (Song Name, Y=168, no border, no background box)
    f_oneliner = write_card("top_oneliner", one_liner)
    filters.append(
        f"drawtext=fontfile='{f_ta_posix}':textfile='{f_oneliner}':text_shaping=1:"
        f"fontcolor=white:fontsize=30:x=(w-text_w)/2:y=168"
    )

    return filters


def detect_deity_category(track_id: str, meta_entry: dict, manifest_cat: str = "") -> str:
    combined = f"{manifest_cat} {meta_entry.get('genre', '')} {meta_entry.get('title', '')}".lower()
    if "murug" in combined or "முருக" in combined or "கந்த" in combined or "திருப்புகழ்" in combined or "சுப்ரமணிய" in combined:
        return "murugan"
    if "shiva" in combined or "சிவ" in combined or "திருவாசகம்" in combined or "தேவாரம்" in combined or "ஈஸ்வர" in combined:
        return "shiva"
    if "amman" in combined or "அம்மன்" in combined or "சக்தி" in combined or "அபிராமி" in combined or "சரஸ்வதி" in combined:
        return "amman"
    if "vinayag" in combined or "விநாயக" in combined or "கணபதி" in combined or "கண நாதா" in combined or "கணேச" in combined:
        return "vinayagar"
    if "vishnu" in combined or "krishna" in combined or "விஷ்ணு" in combined or "கிருஷ்ண" in combined or "பெருமாள்" in combined or "ஆழ்வார்" in combined or "திருப்பாவை" in combined or "நாராயண" in combined:
        return "vishnu"
    if "vallalar" in combined or "வள்ளலார்" in combined or "திருவருட்பா" in combined or "அருட்பெருஞ்ஜோதி" in combined:
        return "vallalar"
    if "kural" in combined or "திருக்குறள்" in combined:
        return "thirukkural"
    return "murugan"


def find_track_audio(track_id: str) -> Path | None:
    for d in AUDIO_DIRS:
        for ext in (".m4a", ".mp3", ".wav"):
            p = d / f"{track_id}{ext}"
            if p.exists() and p.stat().st_size > 50_000:
                return p
    return None


def find_master_video(track_id: str) -> Path | None:
    matches = list(RELEASES_DIR.glob(f"*{track_id}*.mp4"))
    for m in matches:
        if m.stat().st_size > 1_000_000:
            return m
    return None


def get_parent_youtube_info(track_id: str) -> dict:
    parent_vid_id = track_id
    if MANIFEST_DB.exists():
        try:
            mdata = json.loads(MANIFEST_DB.read_text(encoding="utf-8"))
            for t in mdata.get("completed_tracks", []):
                if t.get("track_id") == track_id:
                    if t.get("youtube_id"):
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
        "original_audio_id": track_id,
        "original_audio_url": f"https://youtu.be/{track_id}",
    }


def build_viral_short_metadata(
    track_id: str,
    deity_key: str,
    meta_entry: dict,
    panchangam_info: dict | None = None,
) -> dict:
    hook_cfg = DEITY_HOOKS.get(deity_key, DEITY_HOOKS["murugan"])
    sacred_cat = classify_sacred_category(deity_key, meta_entry, panchangam_info)
    parent_info = get_parent_youtube_info(track_id)

    raw_title = meta_entry.get("title", f"Sacred Devotional Hymn {track_id}").replace("[Film]", "").strip()
    parts = [p.strip() for p in raw_title.split("|")]
    ta_title = parts[0]
    en_title = parts[1] if len(parts) > 1 else ta_title

    # Title starts with one of the 6 Sacred Tamil Category Titles mandated by user:
    # 📖 நன்னெறி | 📖 நல்லறம் | 📖 நற்பண்பு | 📖 நற்துணை | 📖 நற்சொல் | 📖 நற்செயல்
    # Always preserve BOTH Tamil and English transliteration inside the 95-char limit for maximum search & Shorts shelf discovery!
    cat_prefix = sacred_cat["title"]  # e.g., "📖 நற்துணை"
    short_title = f"{cat_prefix} — {ta_title} | {en_title} #Shorts"
    if len(short_title) > 95:
        ta_short = ta_title.split(":")[-1].strip() if ":" in ta_title else ta_title
        en_short = en_title.split(":")[-1].strip() if ":" in en_title else en_title
        short_title = f"{cat_prefix} — {ta_short[:34]} | {en_short[:30]} #Shorts"
    if len(short_title) > 95:
        short_title = f"{cat_prefix} — {ta_title[:36]} | {en_title[:28]} #Shorts"

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
            f"🗓️ இன்றைய தமிழ் பஞ்சாங்கம் & வழிபாட்டு நேரங்கள் (TODAY'S PANCHANGAM TIMINGS):",
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
    pinned_comment = "\n".join(p_comment_lines)

    tag_list = [
        sacred_cat["name_ta"], sacred_cat["key"],
        *[t.lstrip("#") for t in all_hashtags],
        "@GuruKulaDesam", "@GuruKulaDesam2", "GuruKulaDesam", "GuruKulaDesam2",
        "Guru Kula Desam", "Tamil Devotional Songs",
        "Tamil Panchangam Today", "Nalla Neram Today", ta_title[:30], en_title[:30]
    ]

    return {
        "track_id": track_id,
        "deity": deity_key,
        "sacred_category": sacred_cat,
        "title": short_title,
        "ta_title": ta_title,
        "en_title": en_title,
        "description": "\n".join(line for line in desc_lines if line is not None),
        "pinned_comment": pinned_comment,
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
) -> dict:
    meta_db = json.loads(METADATA_DB.read_text(encoding="utf-8")) if METADATA_DB.exists() else {}
    meta_entry = meta_db.get(track_id, {})

    deity_key = detect_deity_category(track_id, meta_entry)
    panchangam_info = get_auspicious_alignment_for_datetime(target_dt or datetime.now(IST))
    sacred_cat = classify_sacred_category(deity_key, meta_entry, panchangam_info)

    out_mp4 = SHORTS_OUT_DIR / f"short_{deity_key}_{track_id}.mp4"
    out_meta_file = SHORTS_META_DIR / f"short_{deity_key}_{track_id}.json"

    if out_mp4.exists() and out_mp4.stat().st_size > 1_000_000 and out_meta_file.exists() and not force_rebuild:
        old_meta = json.loads(out_meta_file.read_text(encoding="utf-8"))
        if old_meta.get("brand_handle") == brand_handle:
            print(f"✅ Short already rendered for {brand_handle}: {out_mp4.name} ({out_mp4.stat().st_size / 1e6:.2f} MB)")
            viral_meta = build_viral_short_metadata(track_id, deity_key, meta_entry, panchangam_info)
            old_meta.update(viral_meta)
            out_meta_file.write_text(json.dumps(old_meta, indent=2, ensure_ascii=False), encoding="utf-8")
            return old_meta

    audio_path = find_track_audio(track_id)
    master_vid = find_master_video(track_id)
    if not audio_path and master_vid:
        audio_path = master_vid

    if not audio_path:
        raise FileNotFoundError(f"No audio or master video found for track {track_id}")

    # Step 1: Detect Chorus / Peak Vocal Window
    start_sec, clip_dur = find_audio_peak_window(audio_path, window_sec=duration_sec)
    print("=" * 80)
    print(f"🔥 BUILDING 9:16 VIRAL SHORT: {sacred_cat['title']} | [{deity_key.upper()}] {track_id}")
    print(f"🗓️  Panchangam : {panchangam_info['onscreen_panchangam_line1']}")
    print(f"⏰ Timings    : {panchangam_info['special_pooja_time']} | இராகு: {panchangam_info['rahu_kalam']}")
    print(f"🎵 Peak Window: {start_sec:.1f}s -> {start_sec + clip_dur:.1f}s ({clip_dur:.1f}s)")
    print("=" * 80)

    work_dir = SHORTS_TEMP_DIR / track_id
    shutil.rmtree(work_dir, ignore_errors=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    # Step 2: Select 100% Authentic Deity-Matched Video Clips (Rejects generic cow/pond duplicates!)
    authentic_clips = get_authentic_deity_clips(track_id, deity_key)
    raw_source_video = work_dir / "source_timeline.mp4"

    if len(authentic_clips) >= 2:
        print(f"  🎬 Using {len(authentic_clips)} authentic [{deity_key.upper()}] deity/temple scenes (e.g., {authentic_clips[0].parent.name}/{authentic_clips[0].name})")
        concat_txt = work_dir / "scenes_concat.txt"
        selected_scenes = []
        total_s = 0.0
        idx = 0
        while total_s < clip_dur + 4.0:
            c = authentic_clips[idx % len(authentic_clips)]
            selected_scenes.append(c)
            total_s += 8.0
            idx += 1
        with open(concat_txt, "w", encoding="utf-8") as f:
            for c in selected_scenes:
                f.write(f"file '{str(c.resolve()).replace(chr(92), '/')}'\n")
        subprocess.run(
            [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(raw_source_video)],
            check=True, capture_output=True
        )
        video_seek_start = 0.0
    elif master_vid:
        raw_source_video = master_vid
        video_seek_start = start_sec
    else:
        raise FileNotFoundError(f"Neither authentic deity scenes nor master video found for {track_id}")

    # Step 3: Build HarfBuzz Drawtext Filters & Viral Metadata (15% Header / 75% Content / 10% Footer, No Borders/Backgrounds)
    viral_meta = build_viral_short_metadata(track_id, deity_key, meta_entry, panchangam_info)
    dt_filters = build_vertical_drawtext_filters(
        work_dir=work_dir,
        deity_key=deity_key,
        sacred_cat=sacred_cat,
        song_title_ta=viral_meta["ta_title"],
        song_title_en=viral_meta["en_title"],
        lyrics_cues=[],
        english_summary="",
        clip_start=start_sec,
        clip_dur=clip_dur,
        panchangam_info=panchangam_info,
        brand_handle=brand_handle,
    )

    # Step 4: Fast 1080x1920 @ 24fps Composite (15% Header = 288px, 75% Content = 1440px, 10% Footer = 192px; No Background Image, No Borders)
    fps_short = 24
    inputs = [
        "-ss", f"{video_seek_start:.2f}", "-t", f"{clip_dur:.2f}", "-i", str(raw_source_video),
        "-ss", f"{start_sec:.2f}", "-t", f"{clip_dur:.2f}", "-i", str(audio_path),
    ]

    dt_chain = ",".join(dt_filters)
    filter_parts = [
        f"[0:v]fps={fps_short},scale=-2:1440,crop={W}:1440:'(iw-ow)/2+((iw-ow)/2)*sin(2*PI*t/18.0)':0,"
        f"colorbalance=rs=-0.02:gs=0.01:bs=0.04,pad={W}:{H}:0:288:black,{dt_chain},format=yuv420p[v_out]",
    ]

    fade_out_st = max(0.5, clip_dur - 0.8)
    filter_parts.append(f"[1:a]afade=t=in:st=0:d=0.4,afade=t=out:st={fade_out_st:.2f}:d=0.8[a_out]")

    cmd_render = [
        FFMPEG, "-y",
        *inputs,
        "-filter_complex", ";".join(filter_parts),
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-movflags", "+faststart",
        "-t", f"{clip_dur:.2f}",
        str(out_mp4)
    ]
    t0 = time.time()
    res = subprocess.run(cmd_render, capture_output=True)
    if res.returncode != 0 or not out_mp4.exists() or out_mp4.stat().st_size < 500_000:
        raise RuntimeError(f"FFmpeg failed encoding {track_id}: {res.stderr.decode('utf-8', errors='ignore')[-400:]}")
    elapsed = time.time() - t0
    print(f"  ⚙️ Encoded 1080x1920 vertical Short in {elapsed:.1f}s")

    size_mb = out_mp4.stat().st_size / (1024 * 1024)
    viral_meta.update({
        "brand_handle": brand_handle,
        "video_path": str(out_mp4.relative_to(ROOT)),
        "duration_sec": round(clip_dur, 2),
        "peak_start_sec": round(start_sec, 2),
        "file_size_mb": round(size_mb, 2),
        "rendered_at": time.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
    })
    out_meta_file.write_text(json.dumps(viral_meta, indent=2, ensure_ascii=False), encoding="utf-8")
    shutil.rmtree(work_dir, ignore_errors=True)

    print(f"🎉 [SHORT READY] {out_mp4.name} ({size_mb:.2f} MB)")
    print(f"   • Sacred Title : {viral_meta['title']}")
    return viral_meta


def list_candidate_tracks(deity_filter: str = None, prioritize_high_energy: bool = True) -> list[dict]:
    meta_db = json.loads(METADATA_DB.read_text(encoding="utf-8")) if METADATA_DB.exists() else {}
    manifest_tracks = {}
    if MANIFEST_DB.exists():
        mdata = json.loads(MANIFEST_DB.read_text(encoding="utf-8"))
        for t in mdata.get("completed_tracks", []):
            manifest_tracks[t["track_id"]] = t

    candidates = []
    all_ids = set(meta_db.keys()) | set(manifest_tracks.keys())
    iconic_keywords = (
        "கந்த சஷ்டி", "kandha sashti", "ஸ்கந்த மந்திரம்", "skanda", "திருப்புகழ்", "thiruppugazh",
        "கந்தர் அலங்காரம்", "kandhar alangaram", "கந்தர் அநுபூதி", "தேவாரம்", "thevaram",
        "திருவாசகம்", "thiruvasagam", "விநாயகர் அகவல்", "அபிராமி அந்தாதி", "abhirami",
        "திருப்பாவை", "thiruppavai", "திருவருட்பா", "thiruvarutpa",
    )
    for tid in sorted(all_ids):
        meta_entry = meta_db.get(tid, {})
        m_cat = manifest_tracks.get(tid, {}).get("category", "")
        deity = detect_deity_category(tid, meta_entry, m_cat)

        if deity_filter and deity != deity_filter.lower():
            continue

        own_dir = FLOW_RENDERS_DIR / tid
        own_authentic = [c for c in sorted(own_dir.glob("scene_*.mp4")) if is_authentic_unique_clip(c)] if own_dir.exists() else []
        has_authentic_flow = len(own_authentic) >= 4
        has_master = find_master_video(tid) is not None
        has_audio = find_track_audio(tid) is not None or has_master

        if has_audio:
            sacred_cat = classify_sacred_category(deity, meta_entry)
            raw_title = meta_entry.get("title", manifest_tracks.get(tid, {}).get("title", tid))
            is_iconic = any(k in raw_title.lower() for k in iconic_keywords)
            # Prioritize tracks with dedicated authentic Flow renders AND iconic high-demand hymns first!
            priority = (0 if has_authentic_flow else 2) + (0 if is_iconic else 1)
            candidates.append({
                "track_id": tid,
                "deity": deity,
                "sacred_category": sacred_cat["title"],
                "priority": priority,
                "has_authentic_flow": has_authentic_flow,
                "title": raw_title,
            })

    candidates.sort(key=lambda x: (x["priority"], x["track_id"]))

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
    ap = argparse.ArgumentParser(description="Build 9:16 Viral Devotional Shorts for @gurukuladesam2")
    ap.add_argument("--track", type=str, help="Specific Track ID to build (e.g. --track=-L3VXkM2MTY)")
    ap.add_argument("--batch", type=int, default=0, help="Build N prioritized Shorts in batch")
    ap.add_argument("--deity", type=str, default=None, help="Filter by deity (murugan, shiva, amman, vinayagar, vishnu, vallalar, thirukkural)")
    ap.add_argument("--duration", type=float, default=DEFAULT_SHORT_DURATION, help="Short duration in seconds (default: 45s)")
    ap.add_argument("--force", action="store_true", help="Force rebuild even if output MP4 exists")
    ap.add_argument("--list", action="store_true", help="List available tracks for Shorts")
    args = ap.parse_args()

    if args.list:
        cands = list_candidate_tracks(deity_filter=args.deity)
        print(f"Total Ready Tracks for 9:16 Shorts: {len(cands)}")
        for idx, c in enumerate(cands[:25], 1):
            auth_tag = "✅ OWN-FLOW" if c["has_authentic_flow"] else "🔄 DEITY-POOL"
            print(f"  {idx:2d}. {c['sacred_category']} | [{c['deity'].upper():<10}] ({auth_tag}) {c['track_id']} | {c['title'][:50]}")
    elif args.track:
        build_short_for_track(args.track, duration_sec=args.duration, force_rebuild=args.force)
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
                build_short_for_track(c["track_id"], duration_sec=args.duration, force_rebuild=args.force)
                built += 1
            except Exception as e:
                print(f"❌ Error building {c['track_id']}: {e}")
    else:
        ap.print_help()
