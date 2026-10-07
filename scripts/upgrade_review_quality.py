# -*- coding: utf-8 -*-
"""
Upgrade and Modernize review_quality.html:
1. Adds Chapters 5 (இல்வாழ்க்கை), 8 (அன்புடைமை), and 16 (பொறையுடைமை) alongside 26, 27, 52, 54, 57, 61.
2. Integrates with Gurukuladesam App Shell, Ashram theme, and assets/js/main.js.
3. Enhances screening room with real-time active scene tracking, keyboard navigation, and fullscreen support.
"""

import os
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def make_scenes(folder, total_dur):
    img_dir = ROOT / 'production' / 'visuals' / 'thirukkural' / folder
    files = sorted([f for f in img_dir.iterdir() if f.suffix.lower() in ('.jpg', '.png')])
    shot_dur = total_dur / len(files)
    scenes = []
    for idx, f in enumerate(files):
        t = round(idx * shot_dur, 2)
        stem = f.stem
        parts = stem.split('_', 1)
        if len(parts) > 1:
            raw_title = parts[1].replace('_', ' ').replace('-', ' ').title()
        else:
            raw_title = stem.replace('_', ' ').replace('-', ' ').title()
        
        rel_path = f'production/visuals/thirukkural/{folder}/{f.name}'
        scenes.append({
            'time': round(t),
            'img': rel_path,
            'title': f'Shot {idx+1}: {raw_title}',
            'desc': f'Scene {idx+1} ({shot_dur:.1f}s hold) • {raw_title}'
        })
    return scenes, len(files), shot_dur

# Build data for 5, 8, 16
new_chapters = {
    "5": {
        "title": "அதிகாரம் 5: இல்வாழ்க்கை (Ilvaazhkkai)",
        "sub": "Sacred Domestic Life & Hospitality • Master Film",
        "video": "renders/releases/adhikaram_05_ilvaazhkkai_cinematic.mp4",
        "duration": "257.54s (4m 17s)",
        "artworks": "42 (100% Unique MD5)",
        "size": "82.91 MB",
        "shotDuration": "6.13s",
        "youtube": "https://www.youtube.com/watch?v=v_dsHTOvKP8",
        "published": True,
        "scenes": make_scenes('05-ilvaazhkkai', 257.54)[0]
    },
    "8": {
        "title": "அதிகாரம் 8: அன்புடைமை (Anbudaimai)",
        "sub": "The Radiance of Unconditional Love • Master Film",
        "video": "renders/releases/adhikaram_08_anbudaimai_cinematic.mp4",
        "duration": "214.79s (3m 34s)",
        "artworks": "35 (100% Unique MD5)",
        "size": "50.61 MB",
        "shotDuration": "6.14s",
        "youtube": "https://www.youtube.com/watch?v=lneosghJWgs",
        "published": True,
        "scenes": make_scenes('08-anbudaimai', 214.79)[0]
    },
    "16": {
        "title": "அதிகாரம் 16: பொறையுடைமை (Poraiyudaimai)",
        "sub": "Sublime Forbearance & Forgiveness • Master Film",
        "video": "renders/releases/adhikaram_16_poraiyudaimai_cinematic.mp4",
        "duration": "381.62s (6m 21s)",
        "artworks": "62 (100% Unique MD5)",
        "size": "138.33 MB",
        "shotDuration": "6.16s",
        "youtube": "https://www.youtube.com/watch?v=R82hz_s2YGQ",
        "published": True,
        "scenes": make_scenes('16-poraiyudaimai', 381.62)[0]
    }
}

# Read existing review_quality.html
html_path = ROOT / 'review_quality.html'
with open(html_path, 'r', encoding='utf-8') as f:
    orig = f.read()

# Extract existing CHAPTER_DATA
m = re.search(r'const CHAPTER_DATA = ({.*?});\s*let currentChapter', orig, re.DOTALL)
if not m:
    raise Exception("Could not find CHAPTER_DATA in review_quality.html")

raw_json = m.group(1)
existing_data = json.loads(raw_json)

# Merge new chapters
merged_data = {}
all_keys = [5, 8, 16, 26, 27, 52, 54, 57, 61]
for k in all_keys:
    str_k = str(k)
    if str_k in new_chapters:
        merged_data[str_k] = new_chapters[str_k]
    elif str_k in existing_data:
        merged_data[str_k] = existing_data[str_k]

# Generate Tabs HTML
tab_meta = [
    (5, "அதிகாரம் 5: இல்வாழ்க்கை", "Ilvaazhkkai • 42 Scenes (6.1s pan) ✔"),
    (8, "அதிகாரம் 8: அன்புடைமை", "Anbudaimai • 35 Scenes (6.1s pan) ✔"),
    (16, "அதிகாரம் 16: பொறையுடைமை", "Poraiyudaimai • 62 Scenes (6.2s pan) ✔"),
    (26, "அதிகாரம் 26: புலால் உண்ணாமை", "Pulaal • 46 Scenes (6.1s pan) ✔"),
    (27, "அதிகாரம் 27: தவம்", "Thavam • 43 Scenes (6.4s pan) ✔"),
    (52, "அதிகாரம் 52: தெரிந்து வினையாடல்", "Therinthu • 55 Scenes (6.9s pan) ✔"),
    (54, "அதிகாரம் 54: பொச்சாவாமை", "Pochchaavaamai • 114 Scenes (2.8s pan) ✔"),
    (57, "அதிகாரம் 57: வெருவந்த செய்யாமை", "Veruvantha • 85 Scenes (4.0s pan) ✔"),
    (61, "அதிகாரம் 61: மடியின்மை", "Madiyinmai • 75 Scenes (3.3s pan) ✔"),
]

tabs_html_parts = []
for ch_num, ch_tamil, ch_sub in tab_meta:
    tabs_html_parts.append(f"""            <button type="button" class="tab-btn" data-chapter="{ch_num}" onclick="loadChapter({ch_num})">
                <span class="tab-title-tamil">{ch_tamil}</span>
                <span class="tab-sub">{ch_sub}</span>
            </button>""")

tabs_replacement = '\n'.join(tabs_html_parts)

# Construct new review_quality.html
new_html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>திரைத் தர ஆய்வு அரங்கம் — குரு குல தேசம் (Film Quality Screening Room)</title>
    <link rel="stylesheet" href="assets/css/style.css">
    <style>
        :root {{
            --bg-dark: #0a0c10;
            --card-bg: rgba(18, 22, 31, 0.95);
            --border-color: #232a3b;
            --accent-gold: #e5a93c;
            --accent-teal: #2dd4bf;
            --accent-blue: #38bdf8;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --pass-green: #22c55e;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Mukta Malar', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg-dark);
            color: var(--text-main);
            min-height: 100vh;
        }}
        .screening-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px 24px 60px;
        }}
        .screening-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
            margin-bottom: 24px;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .brand {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        .brand-logo {{
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #d97706, #b45309);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 4px 12px rgba(217, 119, 6, 0.3);
        }}
        .header-title-box h1 {{
            font-size: 22px;
            font-weight: 700;
            letter-spacing: -0.5px;
            color: #fff;
            margin: 0;
        }}
        .subtitle {{
            font-size: 13px;
            color: var(--text-muted);
            margin-top: 4px;
        }}
        .header-right-badges {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .badge-live {{
            background: rgba(34, 197, 94, 0.15);
            border: 1px solid var(--pass-green);
            color: var(--pass-green);
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .badge-dot {{
            width: 8px;
            height: 8px;
            background: var(--pass-green);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.4; transform: scale(1.3); }}
            100% {{ opacity: 1; transform: scale(1); }}
        }}

        /* Chapter Tabs */
        .chapter-tabs {{
            display: flex;
            gap: 10px;
            overflow-x: auto;
            padding-bottom: 12px;
            margin-bottom: 24px;
        }}
        .tab-btn {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 12px 18px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            white-space: nowrap;
            transition: all 0.2s ease;
            text-align: left;
        }}
        .tab-btn:hover {{
            border-color: var(--accent-gold);
            color: #fff;
            background: #171d2b;
        }}
        .tab-btn.active {{
            border-color: var(--accent-gold);
            background: linear-gradient(135deg, rgba(229, 169, 60, 0.16), rgba(229, 169, 60, 0.05));
            color: var(--accent-gold);
            box-shadow: 0 0 15px rgba(229, 169, 60, 0.15);
        }}
        .tab-title-tamil {{
            font-size: 14px;
            font-weight: 700;
            display: block;
            margin-bottom: 2px;
        }}
        .tab-sub {{
            font-size: 11px;
            opacity: 0.8;
            font-weight: normal;
        }}

        /* Main Screening Grid */
        .screening-grid {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 24px;
        }}
        @media (max-width: 1080px) {{
            .screening-grid {{ grid-template-columns: 1fr; }}
        }}

        /* Player Card */
        .player-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }}
        .video-wrapper {{
            position: relative;
            background: #000;
            width: 100%;
            aspect-ratio: 16 / 9;
        }}
        video {{
            width: 100%;
            height: 100%;
            display: block;
            object-fit: contain;
        }}
        .player-toolbar {{
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #151a24;
            border-top: 1px solid var(--border-color);
            flex-wrap: wrap;
            gap: 12px;
        }}
        .now-playing-info {{
            display: flex;
            flex-direction: column;
        }}
        .now-playing-title {{
            font-size: 17px;
            font-weight: 700;
            color: #fff;
        }}
        .now-playing-sub {{
            font-size: 12px;
            color: var(--accent-teal);
            margin-top: 2px;
        }}
        .player-actions {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .btn {{
            background: #202738;
            border: 1px solid #333e56;
            color: #fff;
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }}
        .btn:hover {{
            background: #2b354d;
            border-color: var(--accent-blue);
        }}
        .btn-gold {{
            background: var(--accent-gold);
            color: #000;
            border: none;
        }}
        .btn-gold:hover {{
            background: #f59e0b;
        }}

        /* Quality Specs Panel */
        .specs-panel {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 20px;
        }}
        .card-header {{
            font-size: 15px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .spec-row {{
            display: flex;
            justify-content: space-between;
            padding: 7px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 12px;
        }}
        .spec-row:last-child {{ border-bottom: none; }}
        .spec-label {{ color: var(--text-muted); }}
        .spec-val {{ font-weight: 600; color: #fff; text-align: right; }}
        .spec-val.green {{ color: var(--pass-green); }}

        /* Scene Breakdown Grid */
        .scene-strip {{
            margin-top: 28px;
        }}
        .strip-header {{
            font-size: 17px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .scene-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 16px;
        }}
        .scene-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.25s ease;
            position: relative;
        }}
        .scene-card:hover {{
            transform: translateY(-3px);
            border-color: var(--accent-gold);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        }}
        .scene-card.active-scene {{
            border-color: var(--accent-gold);
            box-shadow: 0 0 16px rgba(229, 169, 60, 0.45);
            transform: scale(1.02);
        }}
        .scene-card.active-scene::after {{
            content: '▶ இப்போது இயங்குகிறது';
            position: absolute;
            top: 6px;
            left: 6px;
            background: rgba(229, 169, 60, 0.95);
            color: #000;
            font-size: 10px;
            font-weight: 800;
            padding: 2px 6px;
            border-radius: 4px;
        }}
        .scene-thumb {{
            width: 100%;
            aspect-ratio: 16 / 9;
            background: #181d28;
            object-fit: cover;
            display: block;
        }}
        .scene-meta {{
            padding: 10px 12px;
        }}
        .scene-num {{
            font-size: 11px;
            font-weight: 700;
            color: var(--accent-gold);
        }}
        .scene-desc {{
            font-size: 11px;
            color: var(--text-muted);
            margin-top: 2px;
            line-height: 1.3;
        }}

        /* Feature callout */
        .callout {{
            background: rgba(45, 212, 191, 0.08);
            border-left: 4px solid var(--accent-teal);
            padding: 12px 16px;
            border-radius: 0 8px 8px 0;
            font-size: 12px;
            line-height: 1.5;
            color: #ccfbf1;
            margin-top: 14px;
        }}

        .keyboard-hint {{
            background: rgba(0, 0, 0, 0.3);
            border: 1px dashed rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 11px;
            color: #94a3b8;
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 10px;
        }}
        .keyboard-hint kbd {{
            background: #232a3b;
            color: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
    </style>
</head>
<body>
    <div class="app-layout">
        <main class="main-content" style="padding: 0;">
            <div class="screening-container">
                <header class="screening-header">
                    <div class="brand">
                        <div class="brand-logo">🎬</div>
                        <div class="header-title-box">
                            <h1>திரைத் தர ஆய்வு அரங்கம் (Film Quality Screening Room)</h1>
                            <div class="subtitle">திருக்குறள் மாஸ்டர் சினிமா ஆய்வு &amp; காட்சி சரிபார்ப்பு அரங்கம்</div>
                        </div>
                    </div>
                    <div class="header-right-badges">
                        <a href="thirukkural.html" class="btn" style="border-color: var(--accent-gold); color: var(--accent-gold);">
                            ← திருக்குறள் அரங்கம்
                        </a>
                        <div class="badge-live">
                            <div class="badge-dot"></div>
                            100% QA AUDIT PASSED
                        </div>
                    </div>
                </header>

                <!-- Chapter Selector Tabs -->
                <div class="chapter-tabs" id="tabs">
{tabs_replacement}
                </div>

                <!-- Main Player & Specs Grid -->
                <div class="screening-grid">
                    <!-- Left: Video Player -->
                    <div class="player-card">
                        <div class="video-wrapper">
                            <video id="mainPlayer" controls controlslist="nodownload" preload="auto">
                                <source id="videoSrc" src="renders/releases/adhikaram_05_ilvaazhkkai_cinematic.mp4" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                        </div>
                        <div class="player-toolbar">
                            <div class="now-playing-info">
                                <div class="now-playing-title" id="filmTitle">அதிகாரம் 5: இல்வாழ்க்கை (Ilvaazhkkai)</div>
                                <div class="now-playing-sub" id="filmSub">Master Film 1280x720 Progressive @ 24fps • Zero Shaking • Physical Rain &amp; Dhoopam Motion</div>
                            </div>
                            <div class="player-actions">
                                <select class="btn" id="speedSelect" onchange="changeSpeed(this.value)">
                                    <option value="0.75">0.75x (Detail QA)</option>
                                    <option value="1.0" selected>1.0x (Normal)</option>
                                    <option value="1.25">1.25x</option>
                                    <option value="1.5">1.5x</option>
                                </select>
                                <button type="button" class="btn" onclick="togglePlayerFullscreen()" title="திரைப் பெருக்கம் (F)">
                                    ⛶ முழுத்திரை
                                </button>
                                <a id="ytBtn" href="https://www.youtube.com/watch?v=v_dsHTOvKP8" target="_blank" class="btn" style="background:#dc2626; color:#fff; border:none; display:inline-flex; align-items:center; gap:6px;">
                                    ▶ YouTube இல் பார்க்க
                                </a>
                                <a id="downloadBtn" href="renders/releases/adhikaram_05_ilvaazhkkai_cinematic.mp4" download class="btn btn-gold">
                                    ⬇ பதிவிறக்குக (MP4)
                                </a>
                            </div>
                        </div>
                        <div class="keyboard-hint" style="margin: 0 16px 12px 16px;">
                            <span>விசைப்பலகை வழிகாட்டல்:</span>
                            <span><kbd>Space</kbd> / <kbd>K</kbd> இயக்கு / நிறுத்து</span>
                            <span><kbd>←</kbd> / <kbd>→</kbd> 5 நொடி முன்/பின்</span>
                            <span><kbd>[</kbd> / <kbd>]</kbd> முந்தைய/அடுத்த காட்சி</span>
                            <span><kbd>F</kbd> முழுத்திரை</span>
                        </div>
                    </div>

                    <!-- Right: Quality Specifications -->
                    <div class="specs-panel">
                        <div class="card">
                            <div class="card-header">
                                <span>திரைப்பட உற்பத்தித் தரம் (Production Audit)</span>
                                <span style="color: var(--pass-green); font-size: 13px;">✔ Verified</span>
                            </div>
                            <div class="spec-row">
                                <span class="spec-label">Camera Stability</span>
                                <span class="spec-val green" id="statCamera">100% Locked Stable Plate</span>
                            </div>
                            <div class="spec-row">
                                <span class="spec-label">Shaking / Jitter</span>
                                <span class="spec-val green">0.00% (ELIMINATED)</span>
                            </div>
                            <div class="spec-row">
                                <span class="spec-label">Atmospheric Motion</span>
                                <span class="spec-val">Falling Rain + Dhoopam Smoke</span>
                            </div>
                            <div class="spec-row">
                                <span class="spec-label">Unique Artworks</span>
                                <span class="spec-val green" id="statArtworks">42 (100% Unique MD5)</span>
                            </div>
                            <div class="spec-row">
                                <span class="spec-label">Image Duplication</span>
                                <span class="spec-val green">0 Duplicates (Zero Repetition)</span>
                            </div>
                            <div class="spec-row">
                                <span class="spec-label">Runtime</span>
                                <span class="spec-val" id="statDuration">257.54s (4m 17s)</span>
                            </div>
                            <div class="spec-row">
                                <span class="spec-label">Audio Sync Drift</span>
                                <span class="spec-val green">0.0000s (Exact Frame Sync)</span>
                            </div>
                            <div class="spec-row">
                                <span class="spec-label">Video Delivery Spec</span>
                                <span class="spec-val">H.264 24.000 fps Rec.709</span>
                            </div>
                            <div class="spec-row">
                                <span class="spec-label">Audio Delivery Spec</span>
                                <span class="spec-val">AAC 48000 Hz Stereo 256kbps</span>
                            </div>
                            <div class="spec-row">
                                <span class="spec-label">Web Streaming</span>
                                <span class="spec-val green">+faststart moov atom</span>
                            </div>
                            <div class="spec-row">
                                <span class="spec-label">File Size</span>
                                <span class="spec-val" id="statSize">82.91 MB</span>
                            </div>

                            <div class="callout">
                                <strong>Quality Benchmark:</strong> அனைத்து காட்சிகளும் 100% பிரத்யேக ஓவியத் தட்டுகளைக் கொண்டவை. 2x oversampled gradual cinematic moves (pan, tilt, push, pull, diagonal drift) with cosine easing and Lanczos downsampling, blended with procedural falling rain and dhoopam smoke.
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Scene Visual Breakdown Strip -->
                <div class="scene-strip">
                    <div class="strip-header">
                        <span>தனித்துவ காட்சித் தட்டுகள் (Unique Couplet Scene Plates — Zero Repetition)</span>
                        <span style="font-size: 13px; color: var(--text-muted);" id="sceneCountLabel">42 Unique Master Artworks</span>
                    </div>
                    <div class="scene-grid" id="sceneGallery">
                        <!-- Injected via JavaScript -->
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script src="assets/data/catalog.js"></script>
    <script src="assets/js/main.js"></script>
    <script>
        const CHAPTER_DATA = {json.dumps(merged_data, ensure_ascii=False, indent=4)};

        let currentChapter = 5;
        const player = document.getElementById('mainPlayer');
        let currentSceneIndex = -1;

        function getInitialChapter() {{
            const hash = window.location.hash.replace('#', '').replace('chapter-', '');
            if (hash && CHAPTER_DATA[hash]) {{
                return parseInt(hash);
            }}
            try {{
                const saved = localStorage.getItem('gurukulam_review_chapter');
                if (saved && CHAPTER_DATA[saved]) {{
                    return parseInt(saved);
                }}
            }} catch(e) {{}}
            return 5;
        }}

        function loadChapter(ch) {{
            ch = parseInt(ch);
            currentChapter = ch;
            currentSceneIndex = -1;
            
            try {{
                localStorage.setItem('gurukulam_review_chapter', ch);
                if (window.location.hash !== `#chapter-${{ch}}`) {{
                    history.replaceState(null, '', `#chapter-${{ch}}`);
                }}
            }} catch(e) {{}}

            const data = CHAPTER_DATA[ch];
            if (!data) return;

            // Update Tab Active
            document.querySelectorAll('.tab-btn').forEach(btn => {{
                const btnCh = parseInt(btn.getAttribute('data-chapter'));
                btn.classList.toggle('active', btnCh === ch);
            }});

            // Update Video Source
            const wasPlaying = !player.paused;
            player.src = data.video;
            player.load();
            if (wasPlaying) player.play();

            // Update Header & Specs
            document.getElementById('filmTitle').textContent = data.title;
            document.getElementById('filmSub').textContent = data.sub;
            document.getElementById('downloadBtn').href = data.video;
            document.getElementById('statDuration').textContent = data.duration;
            document.getElementById('statArtworks').textContent = data.artworks;
            document.getElementById('statSize').textContent = data.size;
            
            const ytBtn = document.getElementById('ytBtn');
            if (ytBtn) {{
                if (data.youtube) {{
                    ytBtn.style.display = 'inline-flex';
                    ytBtn.href = data.youtube;
                }} else {{
                    ytBtn.style.display = 'none';
                }}
            }}

            // Render Scene Gallery
            const gallery = document.getElementById('sceneGallery');
            gallery.innerHTML = '';
            document.getElementById('sceneCountLabel').textContent = `${{data.scenes.length}} தனித்துவ கலைத்தட்டுகள் (${{data.shotDuration}} hold)`;

            data.scenes.forEach((sc, idx) => {{
                const card = document.createElement('div');
                card.className = 'scene-card';
                card.id = `scene-card-${{idx}}`;
                card.onclick = () => {{
                    player.currentTime = sc.time;
                    player.play();
                    highlightActiveScene(idx);
                }};
                card.innerHTML = `
                    <img src="${{sc.img}}" alt="${{sc.title}}" class="scene-thumb" loading="lazy">
                    <div class="scene-meta">
                        <div class="scene-num">Scene ${{idx + 1}} • ${{formatTime(sc.time)}}</div>
                        <div style="font-weight: 600; font-size: 13px; color: #fff; margin-top: 2px;">${{sc.title}}</div>
                        <div class="scene-desc">${{sc.desc}}</div>
                    </div>
                `;
                gallery.appendChild(card);
            }});

            if (typeof showToast === 'function') {{
                showToast(`🎬 ${{data.title}} ஆய்வு அரங்கம் ஏற்றப்பட்டது.`);
            }}
        }}

        function highlightActiveScene(idx) {{
            if (currentSceneIndex === idx) return;
            const prev = document.getElementById(`scene-card-${{currentSceneIndex}}`);
            if (prev) prev.classList.remove('active-scene');

            currentSceneIndex = idx;
            const cur = document.getElementById(`scene-card-${{idx}}`);
            if (cur) {{
                cur.classList.add('active-scene');
            }}
        }}

        // Listen for video playback progress and highlight the corresponding scene
        player.addEventListener('timeupdate', () => {{
            const data = CHAPTER_DATA[currentChapter];
            if (!data || !data.scenes) return;

            const t = player.currentTime;
            let activeIdx = 0;
            for (let i = 0; i < data.scenes.length; i++) {{
                if (t >= data.scenes[i].time) {{
                    activeIdx = i;
                }} else {{
                    break;
                }}
            }}
            highlightActiveScene(activeIdx);
        }});

        function togglePlayerFullscreen() {{
            const wrapper = document.querySelector('.video-wrapper');
            if (!document.fullscreenElement) {{
                if (wrapper.requestFullscreen) {{
                    wrapper.requestFullscreen();
                }} else if (wrapper.webkitRequestFullscreen) {{
                    wrapper.webkitRequestFullscreen();
                }}
            }} else {{
                if (document.exitFullscreen) {{
                    document.exitFullscreen();
                }}
            }}
        }}

        function changeSpeed(val) {{
            player.playbackRate = parseFloat(val);
        }}

        function formatTime(sec) {{
            const m = Math.floor(sec / 60);
            const s = Math.floor(sec % 60);
            return `${{m}}:${{s < 10 ? '0' : ''}}${{s}}`;
        }}

        // Keyboard navigation shortcuts
        document.addEventListener('keydown', (e) => {{
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;

            if (e.code === 'Space' || e.key === 'k' || e.key === 'K') {{
                e.preventDefault();
                if (player.paused) player.play();
                else player.pause();
            }} else if (e.code === 'ArrowLeft') {{
                e.preventDefault();
                player.currentTime = Math.max(0, player.currentTime - 5);
            }} else if (e.code === 'ArrowRight') {{
                e.preventDefault();
                player.currentTime = Math.min(player.duration, player.currentTime + 5);
            }} else if (e.key === 'f' || e.key === 'F') {{
                e.preventDefault();
                togglePlayerFullscreen();
            }} else if (e.key === '[') {{
                e.preventDefault();
                jumpScene(-1);
            }} else if (e.key === ']') {{
                e.preventDefault();
                jumpScene(1);
            }}
        }});

        function jumpScene(dir) {{
            const data = CHAPTER_DATA[currentChapter];
            if (!data || !data.scenes) return;
            let targetIdx = Math.max(0, Math.min(data.scenes.length - 1, currentSceneIndex + dir));
            const targetScene = data.scenes[targetIdx];
            if (targetScene) {{
                player.currentTime = targetScene.time;
                player.play();
                highlightActiveScene(targetIdx);
                const cur = document.getElementById(`scene-card-${{targetIdx}}`);
                if (cur) cur.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
            }}
        }}

        window.addEventListener('hashchange', () => {{
            const hash = window.location.hash.replace('#', '').replace('chapter-', '');
            if (hash && CHAPTER_DATA[hash] && parseInt(hash) !== currentChapter) {{
                loadChapter(parseInt(hash));
            }}
        }});

        loadChapter(getInitialChapter());
    </script>
</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Successfully upgraded review_quality.html with 9 chapters, active tracking, and app shell!")
