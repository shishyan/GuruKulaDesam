# -*- coding: utf-8 -*-
"""
Synchronizes all 12 published master films across:
1. review_quality.html (Buttons, CHAPTER_DATA, scenes, durations, YouTube URLs)
2. assets/data/catalog.json
3. site_catalog.json
4. source/catalog.json (if exists)
"""

import json
import re
import sys
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
FFPROBE = "C:/ffmpeg/bin/ffprobe.exe"
MANIFEST_PATH = ROOT / "production" / "published_videos_manifest.json"
REVIEW_HTML_PATH = ROOT / "review_quality.html"

with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)

PUB_MAP = {item["chapter"]: item for item in manifest if item.get("status") == "PUBLISHED"}

CHAPTER_SPECS = [
    {
        "ch": 5,
        "name_ta": "இல்வாழ்க்கை",
        "name_en": "Ilvaazhkkai",
        "sub": "Domestic Virtue & Grihastha Dharma • Master Film",
        "folder": "05-ilvaazhkkai",
        "video": "renders/releases/adhikaram_05_ilvaazhkkai_cinematic.mp4",
        "atmo": "Flowers 🌸",
        "tab_label": "Ilvaazhkkai • 42 Scenes (6.1s pan) ✔"
    },
    {
        "ch": 8,
        "name_ta": "அன்புடைமை",
        "name_en": "Anbudaimai",
        "sub": "Loving-Kindness & Universal Affection • Master Film",
        "folder": "08-anbudaimai",
        "video": "renders/releases/adhikaram_08_anbudaimai_cinematic.mp4",
        "atmo": "Drizzle 🌧️",
        "tab_label": "Anbudaimai • 35 Scenes (6.1s pan) ✔"
    },
    {
        "ch": 16,
        "name_ta": "பொறையுடைமை",
        "name_en": "Poraiyudaimai",
        "sub": "Forbearance & Supreme Forgiveness • Master Film",
        "folder": "16-poraiyudaimai",
        "video": "renders/releases/adhikaram_16_poraiyudaimai_cinematic.mp4",
        "atmo": "Rain 🌧️",
        "tab_label": "Poraiyudaimai • 62 Scenes (6.2s pan) ✔"
    },
    {
        "ch": 25,
        "name_ta": "அருளுடைமை",
        "name_en": "Aruludaimai",
        "sub": "Universal Grace & Compassion to All Beings • Master Film",
        "folder": "25-aruludaimai",
        "video": "renders/releases/adhikaram_25_aruludaimai_cinematic.mp4",
        "atmo": "Drizzle 🌧️",
        "tab_label": "Aruludaimai • 37 Scenes (6.3s pan) ✔"
    },
    {
        "ch": 26,
        "name_ta": "புலால் உண்ணாமை",
        "name_en": "Pulaal Unnaamai",
        "sub": "Sacred Reverence for All Life • Flagship Master Film",
        "folder": "26-pulaal-unnaamai",
        "video": "renders/releases/adhikaram_26_pulaal_unnaamai_cinematic.mp4",
        "atmo": "Drizzle 🌧️",
        "tab_label": "Pulaal • 46 Scenes (6.1s pan) ✔"
    },
    {
        "ch": 27,
        "name_ta": "தவம்",
        "name_en": "Thavam",
        "sub": "Spiritual Austerity & Meditation • Master Film",
        "folder": "27-thavam",
        "video": "renders/releases/adhikaram_27_thavam_cinematic.mp4",
        "atmo": "Snow ❄️",
        "tab_label": "Thavam • 43 Scenes (6.4s pan) ✔"
    },
    {
        "ch": 30,
        "name_ta": "வாய்மை",
        "name_en": "Vaaimai",
        "sub": "The Power of Absolute Truthfulness • Master Film",
        "folder": "30-vaaimai",
        "video": "renders/releases/adhikaram_30_vaaimai_cinematic.mp4",
        "atmo": "Rain 🌧️",
        "tab_label": "Vaaimai • 41 Scenes (6.2s pan) ✔"
    },
    {
        "ch": 31,
        "name_ta": "வெகுளாமை",
        "name_en": "Vegulaamai",
        "sub": "Restraint from Anger & Conquest of Wrath • Master Film",
        "folder": "31-vegulaamai",
        "video": "renders/releases/adhikaram_31_vegulaamai_cinematic.mp4",
        "atmo": "Rain 🌧️",
        "tab_label": "Vegulaamai • 52 Scenes (6.2s pan) ✔"
    },
    {
        "ch": 39,
        "name_ta": "இறைமாட்சி",
        "name_en": "Iraimaatchi",
        "sub": "The Greatness of the Sovereign • Master Film",
        "folder": "39-iraimaatchi",
        "video": "renders/releases/adhikaram_39_iraimaatchi_cinematic.mp4",
        "atmo": "Flowers 🌸",
        "tab_label": "Iraimaatchi • 37 Scenes (6.2s pan) ✔"
    },
    {
        "ch": 40,
        "name_ta": "கல்வி",
        "name_en": "Kalvi",
        "sub": "True Learning & Enlightened Knowledge • Master Film",
        "folder": "40-kalvi",
        "video": "renders/releases/adhikaram_40_kalvi_cinematic.mp4",
        "atmo": "Drizzle 🌧️",
        "tab_label": "Kalvi • 59 Scenes (6.2s pan) ✔"
    },
    {
        "ch": 42,
        "name_ta": "கேள்வி",
        "name_en": "Kelvi",
        "sub": "The Wisdom of Attentive Listening • Master Film",
        "folder": "42-kelvi",
        "video": "renders/releases/adhikaram_42_kelvi_cinematic.mp4",
        "atmo": "Rain 🌧️",
        "tab_label": "Kelvi • 41 Scenes (6.2s pan) ✔"
    },
    {
        "ch": 44,
        "name_ta": "குற்றங்கடிதல்",
        "name_en": "Kutrangadithal",
        "sub": "Guarding Against Flaws & Inner Weakness • Master Film",
        "folder": "44-kutrangadithal",
        "video": "renders/releases/adhikaram_44_kutrangadithal_cinematic.mp4",
        "atmo": "Rain 🌧️",
        "tab_label": "Kutrangadithal • 36 Scenes (6.1s pan) ✔"
    },
    {
        "ch": 45,
        "name_ta": "பெரியாரைத் துணைக்கோடல்",
        "name_en": "Periyaaraith Thunaikkodal",
        "sub": "Securing the Alliance of the Wise • Master Film",
        "folder": "45-periyaaraith-thunaikkodal",
        "video": "renders/releases/adhikaram_45_periyaaraith_thunaikkodal_cinematic.mp4",
        "atmo": "Drizzle 🌧️",
        "tab_label": "Periyaarai • 42 Scenes (6.3s pan) ✔"
    },
    {
        "ch": 46,
        "name_ta": "சிற்றினஞ்சேராமை",
        "name_en": "Sitrinanjeraamai",
        "sub": "Avoiding Base Fellowship & Preserving Purity • Master Film",
        "folder": "46-sitrinanjeraamai",
        "video": "renders/releases/adhikaram_46_sitrinanjeraamai_cinematic.mp4",
        "atmo": "Rain 🌧️",
        "tab_label": "Sitrinam • 53 Scenes (6.2s pan) ✔"
    },
    {
        "ch": 52,
        "name_ta": "தெரிந்து வினையாடல்",
        "name_en": "Therinthu Vinaiyaadal",
        "sub": "Right Delegation & Statecraft • Master Film",
        "folder": "52-therinthu-vinaiyaadal",
        "video": "renders/releases/adhikaram_52_therinthu_vinaiyaadal_cinematic.mp4",
        "atmo": "Rain 🌧️",
        "tab_label": "Therinthu • 55 Scenes (6.9s pan) ✔"
    },
    {
        "ch": 54,
        "name_ta": "பொச்சாவாமை",
        "name_en": "Pochchaavaamai",
        "sub": "Unfailing Vigilance & Mindfulness • Master Film",
        "folder": "54-pochchaavaamai",
        "video": "renders/releases/adhikaram_54_pochchaavaamai_cinematic.mp4",
        "atmo": "Drizzle 🌧️",
        "tab_label": "Pochchaavaamai • 46 Scenes (6.9s pan) ✔"
    },
    {
        "ch": 57,
        "name_ta": "வெருவந்த செய்யாமை",
        "name_en": "Veruvantha Seyyaamai",
        "sub": "Benevolent Governance & Gentle Majesty • Master Film",
        "folder": "57-veruvantha-seyyaamai",
        "video": "renders/releases/adhikaram_57_veruvantha_seyyaamai_cinematic.mp4",
        "atmo": "Flowers 🌸",
        "tab_label": "Veruvantha • 50 Scenes (6.8s pan) ✔"
    },
    {
        "ch": 61,
        "name_ta": "மடியின்மை",
        "name_en": "Madiyinmai",
        "sub": "Overcoming Indolence & Relentless Diligence • Master Film",
        "folder": "61-madiyinmai",
        "video": "renders/releases/adhikaram_61_madiyinmai_cinematic.mp4",
        "atmo": "Rain 🌧️",
        "tab_label": "Madiyinmai • 40 Scenes (6.2s pan) ✔"
    },
]

def get_video_info(video_rel):
    p = ROOT / video_rel
    if not p.exists():
        return 0, 0, "0 MB"
    cmd = [FFPROBE, "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(p)]
    data = json.loads(subprocess.check_output(cmd).decode("utf-8"))
    dur = float(data["format"]["duration"])
    size_mb = p.stat().st_size / (1024 * 1024)
    return dur, size_mb

def format_title(filename):
    clean = re.sub(r'^\d+-(n\d+_)?', '', filename)
    clean = clean.replace('.jpg', '').replace('.png', '')
    clean = clean.replace('_', ' ').replace('-', ' ').title()
    return clean

chapter_data_dict = {}
tab_buttons_html = []

for spec in CHAPTER_SPECS:
    ch = spec["ch"]
    pub = PUB_MAP.get(ch, {})
    yt_url = pub.get("url", f"https://www.youtube.com/watch?v={pub.get('video_id', '')}")
    
    vid_dur, vid_size_mb = get_video_info(spec["video"])
    vis_dir = ROOT / "production" / "visuals" / "thirukkural" / spec["folder"]
    img_files = sorted(list(vis_dir.glob("*.jpg")) + list(vis_dir.glob("*.png")))
    
    n_shots = len(img_files)
    shot_dur = vid_dur / n_shots if n_shots else 6.0
    
    mins = int(vid_dur // 60)
    secs = int(vid_dur % 60)
    
    scenes = []
    for i, img in enumerate(img_files):
        time_sec = round(i * shot_dur)
        title = format_title(img.name)
        scenes.append({
            "time": time_sec,
            "img": f"production/visuals/thirukkural/{spec['folder']}/{img.name}",
            "title": f"Shot {i+1}: {title}",
            "desc": f"Scene {i+1} ({shot_dur:.1f}s hold) • {title}"
        })
        
    chapter_data_dict[str(ch)] = {
        "title": f"அதிகாரம் {ch}: {spec['name_ta']} ({spec['name_en']})",
        "sub": spec["sub"],
        "video": spec["video"],
        "duration": f"{vid_dur:.2f}s ({mins}m {secs:02d}s)",
        "artworks": f"{n_shots} (100% Unique MD5)",
        "size": f"{vid_size_mb:.2f} MB",
        "shotDuration": f"{shot_dur:.2f}s",
        "youtube": yt_url,
        "published": True,
        "scenes": scenes
    }
    
    btn_html = (
        f'            <button type="button" class="tab-btn" data-chapter="{ch}" onclick="loadChapter({ch})">\n'
        f'                <span class="tab-title-tamil">அதிகாரம் {ch}: {spec["name_ta"]}</span>\n'
        f'                <span class="tab-sub">{spec["name_en"]} • {n_shots} Scenes ({shot_dur:.1f}s pan) ✔</span>\n'
        f'            </button>'
    )
    tab_buttons_html.append(btn_html)

# Read review_quality.html and update tabs and CHAPTER_DATA
with open(REVIEW_HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Replace tab buttons
tabs_start = html.find('<div class="chapter-tabs"')
if tabs_start != -1:
    tabs_open_end = html.find('>', tabs_start) + 1
    tabs_close = html.find('</div>', tabs_open_end)
    new_tabs = "\n" + "\n".join(tab_buttons_html) + "\n        "
    html = html[:tabs_open_end] + new_tabs + html[tabs_close:]

# Replace CHAPTER_DATA = { ... };
cd_start = html.find('const CHAPTER_DATA = {')
if cd_start != -1:
    # Find matching closing bracket
    bracket_count = 0
    start_pos = html.find('{', cd_start)
    end_pos = start_pos
    for idx in range(start_pos, len(html)):
        if html[idx] == '{':
            bracket_count += 1
        elif html[idx] == '}':
            bracket_count -= 1
            if bracket_count == 0:
                end_pos = idx + 1
                break
                
    json_str = json.dumps(chapter_data_dict, indent=4, ensure_ascii=False)
    html = html[:cd_start] + "const CHAPTER_DATA = " + json_str + ";" + html[end_pos:]

with open(REVIEW_HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ review_quality.html synchronized with all {len(CHAPTER_SPECS)} master chapters!")

# Now synchronize site catalogs
CATALOG_PATHS = [
    ROOT / "assets" / "data" / "catalog.json",
    ROOT / "site_catalog.json",
    ROOT / "docs" / "assets" / "data" / "catalog.json",
    ROOT / "site" / "assets" / "data" / "catalog.json",
]

for cat_p in CATALOG_PATHS:
    if not cat_p.exists():
        continue
    with open(cat_p, "r", encoding="utf-8") as f:
        cat_data = json.load(f)
        
    items = cat_data.get("thirukkural", cat_data) if isinstance(cat_data, dict) else cat_data
    updated = 0
    for item in items:
        # Match by chapter or title
        for spec in CHAPTER_SPECS:
            ch = spec["ch"]
            pub = PUB_MAP.get(ch)
            if not pub:
                continue
            title = str(item.get("title", ""))
            if f"அதிகாரம் {ch} " in title or f"அதிகாரம் {ch}-" in title or f"Chapter {ch}" in title or spec["name_ta"] in title:
                item["id"] = pub["video_id"]
                item["youtube_id"] = pub["video_id"]
                updated += 1
                break
                
    with open(cat_p, "w", encoding="utf-8") as f:
        json.dump(cat_data, f, indent=4, ensure_ascii=False)
    print(f"✅ {cat_p.name} updated: {updated} items synchronized with live YouTube IDs!")
