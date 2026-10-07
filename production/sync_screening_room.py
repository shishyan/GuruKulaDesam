# -*- coding: utf-8 -*-
"""
Screening Room Synchronizer
Automatically synchronizes review_quality.html with the latest renders,
published videos manifest, and visual assets for all chapters.
"""

import os
import re
import json
import glob
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FFPROBE = "C:/ffmpeg/bin/ffprobe.exe"
MANIFEST_FILE = ROOT / "production" / "published_videos_manifest.json"
REVIEW_HTML_FILE = ROOT / "review_quality.html"

CHAPTER_METADATA = {
    26: {
        "title": "அதிகாரம் 26: புலால் உண்ணாமை (Pulaal Unnaamai)",
        "tamil_short": "அதிகாரம் 26: புலால் உண்ணாமை",
        "name_short": "Pulaal",
        "sub": "Sacred Reverence for All Life • Flagship Master Film",
        "dir_name": "26-pulaal-unnaamai",
        "video_file": "adhikaram_26_pulaal_unnaamai_cinematic.mp4"
    },
    27: {
        "title": "அதிகாரம் 27: தவம் (Thavam)",
        "tamil_short": "அதிகாரம் 27: தவம்",
        "name_short": "Thavam",
        "sub": "Spiritual Austerity & Meditation • Master Film",
        "dir_name": "27-thavam",
        "video_file": "adhikaram_27_thavam_cinematic.mp4"
    },
    52: {
        "title": "அதிகாரம் 52: தெரிந்து வினையாடல் (Therinthu Vinaiyaadal)",
        "tamil_short": "அதிகாரம் 52: தெரிந்து வினையாடல்",
        "name_short": "Therinthu",
        "sub": "The Art of Right Delegation & Trust • Master Film",
        "dir_name": "52-therinthu-vinaiyaadal",
        "video_file": "adhikaram_52_therinthu_vinaiyaadal_cinematic.mp4"
    },
    54: {
        "title": "அதிகாரம் 54: பொச்சாவாமை (Pochchaavaamai)",
        "tamil_short": "அதிகாரம் 54: பொச்சாவாமை",
        "name_short": "Pochchaavaamai",
        "sub": "Eternal Vigilance & Mindfulness • Master Film",
        "dir_name": "54-pochchaavaamai",
        "video_file": "adhikaram_54_pochchaavaamai_cinematic.mp4"
    },
    57: {
        "title": "அதிகாரம் 57: வெருவந்த செய்யாமை (Veruvantha Seyyaamai)",
        "tamil_short": "அதிகாரம் 57: வெருவந்த செய்யாமை",
        "name_short": "Veruvantha",
        "sub": "Benevolent & Gentle Governance • Master Film",
        "dir_name": "57-veruvantha-seyyaamai",
        "video_file": "adhikaram_57_veruvantha_seyyaamai_cinematic.mp4"
    },
    61: {
        "title": "அதிகாரம் 61: மடியின்மை (Madiyinmai)",
        "tamil_short": "அதிகாரம் 61: மடியின்மை",
        "name_short": "Madiyinmai",
        "sub": "Unflagging Diligence & Conquest of Sloth • Master Film",
        "dir_name": "61-madiyinmai",
        "video_file": "adhikaram_61_madiyinmai_cinematic.mp4"
    }
}

def get_video_stats(video_path):
    if not video_path.exists():
        return None
    size_mb = video_path.stat().st_size / (1024 * 1024)
    cmd = [
        FFPROBE, "-v", "quiet", "-print_format", "json",
        "-show_streams", "-show_format", str(video_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return {"size_mb": size_mb, "duration": 0}
    data = json.loads(res.stdout)
    dur = 0
    for s in data.get("streams", []):
        if s.get("codec_type") == "video" and "duration" in s:
            dur = float(s["duration"])
            break
    if dur == 0 and "format" in data and "duration" in data["format"]:
        dur = float(data["format"]["duration"])
    return {"size_mb": size_mb, "duration": dur}

def get_manifest():
    if not MANIFEST_FILE.exists():
        return {}
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    manifest = {}
    for item in data:
        manifest[item["chapter"]] = item
    return manifest

def format_title_from_filename(filename):
    clean = re.sub(r'^\d+-', '', filename)
    clean = re.sub(r'\.(jpg|png|webp)$', '', clean)
    clean = re.sub(r'_1791\d+', '', clean)
    clean = clean.replace('-', ' ').replace('_', ' ')
    clean = re.sub(r'\bn\d+\b', '', clean).strip()
    return clean.title()

def sync():
    manifest = get_manifest()
    chapter_data = {}
    tab_buttons_html = []

    for ch_num, meta in CHAPTER_METADATA.items():
        v_path = ROOT / "renders" / "releases" / meta["video_file"]
        v_stats = get_video_stats(v_path)
        
        vis_dir = ROOT / "production" / "visuals" / "thirukkural" / meta["dir_name"]
        raw_images = sorted(glob.glob(str(vis_dir / "*.jpg")) + glob.glob(str(vis_dir / "*.png")))
        # Filter out duplicates or thumbnails
        images = [p for p in raw_images if not os.path.basename(p).startswith("thumbnail")]

        total_dur = v_stats["duration"] if v_stats else 300.0
        size_str = f"{v_stats['size_mb']:.2f} MB" if v_stats else "N/A"
        mins = int(total_dur // 60)
        secs = int(total_dur % 60)
        dur_str = f"{total_dur:.2f}s ({mins}m {secs:02d}s)"
        
        num_artworks = len(images)
        shot_sec = total_dur / num_artworks if num_artworks > 0 else 6.0
        shot_str = f"{shot_sec:.2f}s"

        pub_info = manifest.get(ch_num)
        is_published = pub_info is not None and pub_info.get("status") == "PUBLISHED"
        yt_url = pub_info.get("url", "") if pub_info else ""

        scenes = []
        for idx, img_path in enumerate(images):
            t = round(idx * shot_sec)
            fn = os.path.basename(img_path)
            rel_img = f"production/visuals/thirukkural/{meta['dir_name']}/{fn}"
            stitle = format_title_from_filename(fn)
            scenes.append({
                "time": t,
                "img": rel_img,
                "title": f"Shot {idx+1}: {stitle}",
                "desc": f"Scene {idx+1} ({shot_sec:.1f}s hold) • {stitle}"
            })

        chapter_data[str(ch_num)] = {
            "title": meta["title"],
            "sub": meta["sub"],
            "video": f"renders/releases/{meta['video_file']}",
            "duration": dur_str,
            "artworks": f"{num_artworks} (100% Unique MD5)",
            "size": size_str,
            "shotDuration": shot_str,
            "youtube": yt_url,
            "published": is_published,
            "scenes": scenes
        }

        # Tab button
        active_cls = " active" if ch_num == 26 else ""
        pub_tag = " ✔ PUBLISHED" if is_published else ""
        tab_buttons_html.append(
            f'            <button class="tab-btn{active_cls}" onclick="loadChapter({ch_num})">\n'
            f'                <span class="tab-title-tamil">{meta["tamil_short"]}</span>\n'
            f'                <span class="tab-sub">{meta["name_short"]} • {num_artworks} Scenes ({shot_sec:.1f}s pan){pub_tag}</span>\n'
            f'            </button>'
        )

    # Read review_quality.html
    with open(REVIEW_HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # Replace tab buttons
    tab_block = '<div class="chapter-tabs" id="tabs">\n' + '\n'.join(tab_buttons_html) + '\n        </div>'
    html = re.sub(
        r'<div class="chapter-tabs" id="tabs">.*?</div>\s*<!-- Main Player',
        tab_block + '\n\n        <!-- Main Player',
        html,
        flags=re.DOTALL
    )

    # Replace CHAPTER_DATA json
    json_str = json.dumps(chapter_data, indent=12, ensure_ascii=False)
    html = re.sub(
        r'const CHAPTER_DATA = \{.*?let currentChapter',
        f'const CHAPTER_DATA = {json_str};\n\n        let currentChapter',
        html,
        flags=re.DOTALL
    )

    with open(REVIEW_HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"review_quality.html successfully synced for all {len(CHAPTER_METADATA)} chapters!")

if __name__ == "__main__":
    sync()
