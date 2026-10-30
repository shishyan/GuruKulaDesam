#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/shorts_viral_builder.py
100% Song-Authentic 9:16 Vertical (1080x1920 @ 24fps) Shorts Builder
for @GuruKulaDesam (நற்செய்கை — Virtuous Shorts) & @GuruKulaDesam2 (நற்பண்பு — Devotional Shorts).

STRICT AUTHENTICITY GUARANTEE (ZERO CROSS-TRACK SCENE POOLING):
1. Primary Source (`original_master_clip`):
   Clips the song's TRUE Original Master Film at the exact `[start_sec : start_sec + clip_dur]`
   vocal peak window so both audio AND visuals match the exact verse & storyline being sung:
   - Local clean un-layered 1080p Master MP4s (Google Drive `Videos/`, Windows SSD `renders/releases/`)
   - Published 1080p Master Films on `@Guru-Kula-Desam` (`UCPqB1A_WzpLJec6q69BOO3Q`, auto-fetched via `yt-dlp`).
2. Secondary Source (`google_flow_dedicated`):
   Uses ONLY scenes generated specifically for `track_id` via the Google Flow PRO account
   (`tools/flow_autonomous_generator.py`), verified unique (`hash_count == 1`), or generates
   fresh song-specific clips live via `--use-flow`.
3. NEVER uses scenes from another song or generic nature loops.
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
DEFAULT_SHORT_DURATION = 35.0

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
    """Returns True ONLY if `mp4_path` is strictly unique to its song (not shared/duplicated across tracks)."""
    if not mp4_path.exists() or mp4_path.stat().st_size < 250_000:
        return False
    counts = _get_clip_hash_counts()
    try:
        with open(mp4_path, "rb") as fh:
            h = hashlib.md5(fh.read(65536)).hexdigest()
        # Allow count <= 2 only because Linux & mounted Windows SSD may mirror the exact same track folder
        return counts.get(h, 1) <= 2
    except Exception:
        return False


def get_track_dedicated_flow_clips(track_id: str, require_fresh_flow_short: bool = False) -> list[Path]:
    """
    Returns ONLY Flow video clips created specifically for `track_id` (NEVER from any other song!).
    When `require_fresh_flow_short=True`, strictly requires newly generated `flow_short_*.mp4` clips.
    """
    for base in (FLOW_RENDERS_DIR, WIN_FLOW_RENDERS_DIR):
        tdir = base / track_id
        if not tdir.exists():
            continue
        # 1. Always prefer fresh `flow_short_*.mp4` clips verified by `flow_verified.json`
        verified_clips = [c for c in sorted(tdir.glob("flow_short_*.mp4")) if c.stat().st_size > 250_000]
        if len(verified_clips) >= 3:
            return verified_clips
        if require_fresh_flow_short:
            continue
        if track_id in ("AW4cljBWy2w", "Lki_Y8OSljs"):
            continue
        # 2. Otherwise accept `scene_*.mp4` ONLY if >= 5 scenes are strictly unique to this song
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


def get_ytdlp_cmd() -> list[str]:
    local_bin = Path.home() / ".local" / "bin" / "yt-dlp"
    if local_bin.exists():
        return [str(local_bin)]
    which_yt = shutil.which("yt-dlp")
    if which_yt:
        return [which_yt]
    return [sys.executable, "-m", "yt_dlp"]


def resolve_original_master_video(track_id: str, catalog_entry: dict | None = None) -> tuple[Path | None, bool, str | None]:
    """
    Resolves the song's TRUE Original Master Video (`(video_path, has_burned_bars, youtube_film_id)`):
      1. Clean un-layered local/GDrive/SSD Master MP4 (`has_burned_bars=False`)
      2. Cached 1080p YouTube Master Film (`renders/master_cache/<youtube_film_id>.mp4`)
      3. Local layered GDrive Master MP4 (`has_burned_bars=True`)
      4. Auto-download published 1080p Master Film from `@Guru-Kula-Desam` via `yt-dlp`!
    """
    cat = catalog_entry
    if cat is None:
        master_cat = load_master_catalog()
        cat = master_cat.get(track_id)
        if not cat:
            for entry in master_cat.values():
                if entry.get("legacy_track_id") == track_id or entry.get("youtube_film_id") == track_id:
                    cat = entry
                    break

    yt_film_id = cat.get("youtube_film_id") if cat else None
    has_burned = bool(cat.get("has_burned_bars", False)) if cat else False

    # 1. Already cached on fast local disk (`renders/master_cache/`)
    if yt_film_id:
        cached_mp4 = MASTER_CACHE_DIR / f"{yt_film_id}.mp4"
        if cached_mp4.exists() and cached_mp4.stat().st_size > 5_000_000:
            return cached_mp4, has_burned, yt_film_id

    cache_id = yt_film_id or track_id
    local_cache_mp4 = MASTER_CACHE_DIR / f"{cache_id}.mp4"
    if local_cache_mp4.exists() and local_cache_mp4.stat().st_size > 5_000_000:
        return local_cache_mp4, False, yt_film_id

    # 2. Fast local/mounted SSD (`renders/releases/` or `/media/shishyan/Shishyan/...`)
    if cat and cat.get("local_clean_video") and not str(cat["local_clean_video"]).startswith("/run/user/"):
        p = Path(cat["local_clean_video"])
        if p.exists() and p.stat().st_size > 5_000_000:
            return p, False, yt_film_id

    search_ids = [track_id]
    if cat and cat.get("legacy_track_id") and cat["legacy_track_id"] not in search_ids:
        search_ids.append(cat["legacy_track_id"])
    for rel_dir in (RELEASES_DIR, WIN_RELEASES_DIR):
        if rel_dir.exists():
            if cat and cat.get("chapter_num"):
                for m in sorted(rel_dir.glob(f"adhikaram_0*{cat['chapter_num']}_*_cinematic.mp4")):
                    if m.stat().st_size > 5_000_000:
                        return m, False, yt_film_id
            for sid in search_ids:
                for m in sorted(rel_dir.glob(f"*{sid}*.mp4")):
                    if m.stat().st_size > 5_000_000:
                        return m, False, yt_film_id

    # 3. Clean un-layered Google Drive video — copy once via fast `gio copy` into `MASTER_CACHE_DIR` to avoid FUSE seek stalls!
    if cat and cat.get("local_clean_video") and str(cat["local_clean_video"]).startswith("/run/user/"):
        gvfs_p = Path(cat["local_clean_video"])
        try:
            if gvfs_p.exists():
                print(f"  📂 Caching clean 1080p base video from Google Drive -> {local_cache_mp4.name}...")
                subprocess.run(["gio", "copy", str(gvfs_p), str(local_cache_mp4)], check=True, capture_output=True)
                if local_cache_mp4.exists() and local_cache_mp4.stat().st_size > 5_000_000:
                    return local_cache_mp4, False, yt_film_id
        except Exception:
            pass

    # 4. Auto-download published 1080p Master Film from @Guru-Kula-Desam via yt-dlp!
    if yt_film_id:
        cached_mp4 = MASTER_CACHE_DIR / f"{yt_film_id}.mp4"
        print(f"  📥 Downloading Original 1080p Master Film from @Guru-Kula-Desam ({yt_film_id}) via yt-dlp...")
        ytdlp = get_ytdlp_cmd()
        url = f"https://www.youtube.com/watch?v={yt_film_id}"
        for extra_args in (
            ["--extractor-args", "youtube:player_client=android,web"],
            [],
        ):
            cmd = [
                *ytdlp,
                *extra_args,
                "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
                "--merge-output-format", "mp4",
                "-o", str(cached_mp4),
                url,
            ]
            subprocess.run(cmd, capture_output=True, text=True)
            if cached_mp4.exists() and cached_mp4.stat().st_size > 5_000_000:
                print(f"  ✅ Downloaded Master Film: {cached_mp4.name} ({cached_mp4.stat().st_size / 1e6:.1f} MB)")
                return cached_mp4, has_burned, yt_film_id

    # 5. Fallback: Google Drive layered Master MP4 via `gio copy`
    if cat and cat.get("local_layered_video"):
        gvfs_p = Path(cat["local_layered_video"])
        try:
            if gvfs_p.exists():
                subprocess.run(["gio", "copy", str(gvfs_p), str(local_cache_mp4)], check=True, capture_output=True)
                if local_cache_mp4.exists() and local_cache_mp4.stat().st_size > 5_000_000:
                    return local_cache_mp4, True, yt_film_id
        except Exception:
            pass

    return None, False, yt_film_id


def detect_deity_category(track_id: str, meta_entry: dict, manifest_cat: str = "") -> str:
    title_l = f"{meta_entry.get('title', '')}".lower()
    combined = f"{manifest_cat} {meta_entry.get('genre', '')} {title_l}".lower()
    if any(k in title_l for k in ("திருக்குறள்", "thirukkural", "அதிகாரம்", "adhikaram")):
        return "thirukkural"
    if any(k in title_l for k in ("சுப்ரமணிய", "subramani", "திருப்புகழ்", "thiruppugazh", "ஆறுமுகம்", "arumugam", "கந்த", "kandha", "kandar", "முருக", "murug")):
        return "murugan"
    if any(k in combined for k in ("திருவருட்பா", "thiruvarutpa", "வள்ளலார்", "vallalar", "அருட்பெருஞ்ஜோதி", "அருட்பெருஞ்சோதி", "arutperunjothi", "கொன்றை வேந்தன்", "konrai vendhan")):
        return "vallalar"
    if any(k in combined for k in ("விநாயக", "vinayag", "கணபதி", "ganapathi", "கண நாதா", "gana natha", "கணேச", "ganesha", "கைத்தல நிறைகனி", "kaiththala", "திகட சக்கர", "thigada", "பிடியதன் உருவுமை", "pidiyathan", "நான்மணிமாலை")):
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


def find_audio_peak_window(media_path: Path, window_sec: float = DEFAULT_SHORT_DURATION) -> tuple[float, float]:
    total_dur = get_media_duration(media_path)
    if total_dur <= window_sec + 4.0:
        return 0.0, min(total_dur, window_sec)

    sr = 8000
    cmd = [
        FFMPEG, "-v", "error",
        "-t", "180",
        "-i", str(media_path),
        "-vn", "-ac", "1", "-ar", str(sr),
        "-f", "s16le", "-",
    ]
    try:
        raw_bytes = subprocess.check_output(cmd)
        num_samples = len(raw_bytes) // 2
        samples = struct.unpack(f"<{num_samples}h", raw_bytes[: num_samples * 2])

        sec_energies = []
        for s in range(0, num_samples - sr, sr):
            chunk = samples[s : s + sr]
            mean_sq = sum(x * x for x in chunk) / float(sr)
            sec_energies.append(math.sqrt(mean_sq))

        # Avoid opening title card (first 16s) and closing tail (last 10s) of Master Films
        min_start = min(16, max(0, len(sec_energies) - int(window_sec) - 2))
        max_start = max(min_start + 1, len(sec_energies) - int(window_sec) - 10)

        best_start = min_start
        best_score = -1.0
        win_int = int(window_sec)

        for start_sec in range(min_start, max_start + 1):
            opening_energy = sum(sec_energies[start_sec : start_sec + 8]) * 1.35
            body_energy = sum(sec_energies[start_sec + 8 : start_sec + win_int])
            score = opening_energy + body_energy
            if score > best_score:
                best_score = score
                best_start = start_sec

        return float(best_start), float(window_sec)
    except Exception as e:
        print(f"  [Peak Detector] Fallback to 22.0s due to: {e}")
        start_fallback = min(22.0, max(0.0, total_dur - window_sec))
        return start_fallback, window_sec


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
    Strict 15% Header / 75% Content / 10% Footer layout (1080x1920) using libass (HarfBuzz-ng
    complex Tamil ligature shaping — zero broken vowel signs on Linux, Windows, and GitHub Actions!):
    - Top 15% Header (Y=0..288, 288px):
      * Line 1 (MarginV=88): `@GuruKulaDesam` or `@GuruKulaDesam2` (#FFE040)
      * Line 2 (MarginV=160): One-liner song name (`{sacred_cat['name_ta']} — {short_ta}`)
    - Middle 75% Content (Y=288..1728, 1440px): Pure unobstructed original song video (1080px width)
    - Bottom 10% Footer (Y=1728..1920, 192px): Clean breathing space (zero clutter, zero ads)
    - Zero text background boxes (`BorderStyle=1, Outline=0, Shadow=0`), zero graphic frames.
    """
    cat_ta = sacred_cat["name_ta"]
    short_ta = smart_truncate(clean_song_title_part(song_title_ta.split("|")[0]), 38)
    one_liner = f"{cat_ta} — {short_ta}".replace("{", "(").replace("}", ")")

    ass_path = work_dir / "header_overlay.ass"
    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Brand,Noto Sans Tamil,38,&H0040E0FF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,8,24,24,88,1
Style: SongLine,Noto Sans Tamil,31,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,8,24,24,162,1

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
    cat_entry = master_cat.get(track_id)
    if not cat_entry:
        for ce in master_cat.values():
            if ce.get("legacy_track_id") == track_id or ce.get("youtube_film_id") == track_id:
                cat_entry = ce
                break

    meta_db = json.loads(METADATA_DB.read_text(encoding="utf-8")) if METADATA_DB.exists() else {}
    meta_entry = dict(meta_db.get(track_id, {}))
    if cat_entry:
        meta_entry.setdefault("title", cat_entry["title"])
        # Prefer the newest Master Film title when available
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
        # Only reuse cached Short if it was built with the new authentic Master/Flow pipeline!
        if old_meta.get("brand_handle") == brand_handle and old_meta.get("visual_source_mode") in ("original_master_clip", "google_flow_dedicated"):
            print(f"✅ Authentic Short already rendered for {brand_handle}: {out_mp4.name} ({out_mp4.stat().st_size / 1e6:.2f} MB)")
            viral_meta = build_viral_short_metadata(
                track_id, deity_key, meta_entry, panchangam_info,
                youtube_film_id=cat_entry.get("youtube_film_id") if cat_entry else None
            )
            old_meta.update(viral_meta)
            out_meta_file.write_text(json.dumps(old_meta, indent=2, ensure_ascii=False), encoding="utf-8")
            return old_meta

    # Resolve Song-Specific Visual Source (Priority 1: Original Master Video; Priority 2: Dedicated Google Flow Clips)
    master_vid, has_burned_bars, yt_film_id = (None, False, None)
    if not use_flow:
        master_vid, has_burned_bars, yt_film_id = resolve_original_master_video(track_id, cat_entry)

    work_dir = SHORTS_TEMP_DIR / track_id
    shutil.rmtree(work_dir, ignore_errors=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    is_portrait_source = False
    flow_pts_stretch = 1.0
    visual_source_mode = None
    if master_vid is not None:
        visual_source_mode = "original_master_clip"
        audio_path = master_vid  # Exact frame-locked audio + video from the Master Film itself!
        start_sec, clip_dur = find_audio_peak_window(master_vid, window_sec=duration_sec)
        raw_source_video = master_vid
        video_seek_start = start_sec
        source_desc = f"Original Master Video ({master_vid.name})"
    else:
        dedicated_clips = get_track_dedicated_flow_clips(track_id, require_fresh_flow_short=use_flow)
        if len(dedicated_clips) < 3 and use_flow:
            from tools.flow_autonomous_generator import generate_flow_clips_for_short
            dedicated_clips = generate_flow_clips_for_short(track_id, scene_count=4)

        if len(dedicated_clips) < 3:
            shutil.rmtree(work_dir, ignore_errors=True)
            raise FileNotFoundError(
                f"STRICT AUTHENTICITY GUARD: Track '{track_id}' has neither an Original Master Video "
                f"nor dedicated song-specific Google Flow scenes. Refusing to use unrelated clips! "
                f"(Pass --use-flow to generate dedicated scenes via Google Flow PRO account.)"
            )

        audio_path = find_track_audio(track_id)
        if not audio_path:
            from google_flow_engine import ensure_audio
            audio_path = ensure_audio(track_id)

        visual_source_mode = "google_flow_dedicated"
        start_sec, clip_dur = find_audio_peak_window(audio_path, window_sec=duration_sec)
        raw_source_video = work_dir / "flow_dedicated_timeline.mp4"
        concat_txt = work_dir / "scenes_concat.txt"

        # Probe dimensions & total duration of unique Flow clips
        try:
            probe_wh = subprocess.check_output(
                [FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(dedicated_clips[0])],
                text=True,
            ).strip()
            sw, sh = [int(x) for x in probe_wh.split("x")[:2]]
            is_portrait_source = sw < sh
        except Exception:
            is_portrait_source = False

        unique_total_dur = sum(get_media_duration(c) for c in dedicated_clips)
        if unique_total_dur >= clip_dur:
            selected_scenes = list(dedicated_clips)
            flow_pts_stretch = 1.0
        elif unique_total_dur >= clip_dur * 0.65:
            # Gentle devotional slow-motion (e.g. 28-31.7s -> 35.6s) so ZERO scenes repeat!
            selected_scenes = list(dedicated_clips)
            flow_pts_stretch = min(1.50, (clip_dur + 0.6) / max(1.0, unique_total_dur))
        else:
            selected_scenes = []
            total_s = 0.0
            idx = 0
            while total_s < clip_dur + 4.0:
                c = dedicated_clips[idx % len(dedicated_clips)]
                selected_scenes.append(c)
                total_s += max(4.0, get_media_duration(c))
                idx += 1

        target_w, target_h = (720, 1280) if is_portrait_source else (1280, 720)
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
        has_burned_bars = False
        source_desc = f"Song-Dedicated Google Flow {'9:16 ' if is_portrait_source else ''}Clips ({len(dedicated_clips)} clips for {track_id})"

    print("=" * 80)
    print(f"🔥 BUILDING 100% SONG-AUTHENTIC 9:16 SHORT: {sacred_cat['title']} | [{deity_key.upper()}] {track_id}")
    print(f"🎬 Source Mode: {source_desc}")
    print(f"🗓️  Panchangam : {panchangam_info['onscreen_panchangam_line1']}")
    print(f"🎵 Clip Window: {start_sec:.1f}s -> {start_sec + clip_dur:.1f}s ({clip_dur:.1f}s)")
    print("=" * 80)

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
            f"crop={W}:1440:(iw-{W})/2:(ih-1440)*0.40,"
            f"pad={W}:{H}:0:288:black,{dt_chain},format=yuv420p[v_out]",
        ]
    else:
        if has_burned_bars:
            pre_crop = "crop=iw*0.86:ih*0.778:iw*0.07:ih*0.06"
        else:
            pre_crop = "crop=iw*0.86:ih:iw*0.07:0"
        filter_parts = [
            f"[0:v]{pts_filter}fps={fps_short},{pre_crop},scale=-2:1440,"
            f"crop={W}:1440:'(iw-ow)/2+min((iw-ow)/2,160)*sin(2*PI*t/22.0)':0,"
            f"pad={W}:{H}:0:288:black,{dt_chain},format=yuv420p[v_out]",
        ]

    fade_out_st = max(0.5, clip_dur - 0.8)
    filter_parts.append(f"[{audio_map_in}]afade=t=in:st=0:d=0.35,afade=t=out:st={fade_out_st:.2f}:d=0.8[a_out]")

    cmd_render = [
        FFMPEG, "-y",
        *inputs,
        "-filter_complex", ";".join(filter_parts),
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
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
    print(f"  ⚙️ Encoded 1080x1920 vertical Short in {elapsed:.1f}s")

    size_mb = out_mp4.stat().st_size / (1024 * 1024)
    viral_meta.update({
        "brand_handle": brand_handle,
        "visual_source_mode": visual_source_mode,
        "visual_source_file": master_vid.name if master_vid else f"google_flow_renders/{track_id}",
        "youtube_film_id": yt_film_id,
        "video_path": str(out_mp4.relative_to(ROOT)),
        "duration_sec": round(clip_dur, 2),
        "peak_start_sec": round(start_sec, 2),
        "file_size_mb": round(size_mb, 2),
        "rendered_at": time.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
    })
    out_meta_file.write_text(json.dumps(viral_meta, indent=2, ensure_ascii=False), encoding="utf-8")
    shutil.rmtree(work_dir, ignore_errors=True)

    print(f"🎉 [AUTHENTIC SHORT READY] {out_mp4.name} ({size_mb:.2f} MB) | Mode={visual_source_mode}")
    print(f"   • Sacred Title : {viral_meta['title']}")
    return viral_meta


def list_candidate_tracks(deity_filter: str = None, prioritize_high_energy: bool = True) -> list[dict]:
    """
    Lists ONLY tracks that have a verified 100% song-specific Original Master Film
    in `master_film_sources.json` (or >= 5 strictly unique song-dedicated Google Flow clips).
    Prioritizes newest Oct 2026 1080p Master Films & iconic hymns first!
    """
    master_cat = load_master_catalog()
    meta_db = json.loads(METADATA_DB.read_text(encoding="utf-8")) if METADATA_DB.exists() else {}

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
    seen_ids = set()

    # 1. All verified Original Master Films (primary source!)
    for fid, entry in master_cat.items():
        deity = detect_deity_category(fid, {"title": entry.get("title", fid)}, entry.get("deity", ""))
        if deity_filter and deity != deity_filter.lower():
            continue
        # Ensure accessible either locally or via YouTube yt-dlp
        has_local = False
        for k in ("local_clean_video", "local_layered_video"):
            if entry.get(k):
                try:
                    if Path(entry[k]).exists():
                        has_local = True
                        break
                except OSError:
                    pass
        if not has_local and not entry.get("youtube_film_id"):
            continue

        raw_title = entry.get("title", fid)
        is_iconic = any(k in raw_title.lower() for k in iconic_keywords)
        tier = entry.get("quality_tier", 1)
        priority = tier * 2 + (0 if is_iconic else 1)
        sacred_cat = classify_sacred_category(deity, {"title": raw_title})

        candidates.append({
            "track_id": fid,
            "legacy_track_id": entry.get("legacy_track_id"),
            "deity": deity,
            "sacred_category": sacred_cat["title"],
            "priority": priority,
            "source_type": "MASTER-FILM",
            "published_at": entry.get("published_at", ""),
            "title": raw_title,
        })
        seen_ids.add(fid)
        if entry.get("legacy_track_id"):
            seen_ids.add(entry["legacy_track_id"])

    # 2. Any additional tracks with >= 5 strictly unique song-dedicated Google Flow clips
    for tid, me in meta_db.items():
        if tid in seen_ids:
            continue
        deity = detect_deity_category(tid, me)
        if deity_filter and deity != deity_filter.lower():
            continue
        own_clips = get_track_dedicated_flow_clips(tid)
        if len(own_clips) >= 5 and find_track_audio(tid) is not None:
            raw_title = me.get("title", tid)
            sacred_cat = classify_sacred_category(deity, me)
            candidates.append({
                "track_id": tid,
                "legacy_track_id": tid,
                "deity": deity,
                "sacred_category": sacred_cat["title"],
                "priority": 4,
                "source_type": "DEDICATED-FLOW",
                "published_at": "2026-09-01T00:00:00Z",
                "title": raw_title,
            })

    # Sort highest quality & newest Master Films first!
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
    ap = argparse.ArgumentParser(description="Build 100% Song-Authentic 9:16 Vertical Shorts")
    ap.add_argument("--track", type=str, help="Specific Film/Track ID to build")
    ap.add_argument("--batch", type=int, default=0, help="Build N prioritized Shorts in batch")
    ap.add_argument("--deity", type=str, default=None, help="Filter by deity/pillar")
    ap.add_argument("--duration", type=float, default=DEFAULT_SHORT_DURATION, help="Short duration in seconds (default: 35s)")
    ap.add_argument("--brand", type=str, default="@GuruKulaDesam", help="Brand handle (@GuruKulaDesam or @GuruKulaDesam2)")
    ap.add_argument("--use-flow", action="store_true", help="Generate dedicated song-specific visuals via Google Flow PRO account")
    ap.add_argument("--force", action="store_true", help="Force rebuild even if output MP4 exists")
    ap.add_argument("--list", action="store_true", help="List verified song-authentic tracks")
    args = ap.parse_args()

    if args.list:
        cands = list_candidate_tracks(deity_filter=args.deity)
        print(f"Total Verified Song-Authentic Tracks for 9:16 Shorts: {len(cands)}")
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
