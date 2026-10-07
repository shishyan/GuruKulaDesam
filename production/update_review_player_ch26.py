# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "review_quality.html"
VISUAL_DIR = ROOT / "production" / "visuals" / "thirukkural" / "26-pulaal-unnaamai"

files = sorted(list(VISUAL_DIR.glob("*.jpg")) + list(VISUAL_DIR.glob("*.png")))
dur = 279.27 / len(files)

scene_objs = []
for idx, f in enumerate(files):
    t = int(idx * dur)
    clean_name = f.stem.replace("-", " ").title()
    scene_objs.append(f'                    {{ time: {t}, img: "production/visuals/thirukkural/26-pulaal-unnaamai/{f.name}", title: "Shot {idx+1:02d}: {clean_name}", desc: "Couplet scene {idx+1} ({dur:.1f}s)" }}')

scenes_js = ",\n".join(scene_objs)

ch26_js_replacement = f"""            26: {{
                title: "அதிகாரம் 26: புலால் உண்ணாமை (Pulaal Unnaamai)",
                sub: "46 Cinematic Couplet Shots • Gradual Film Pan Every 6s • Falling Rain & Dhoopam",
                video: "renders/releases/adhikaram_26_pulaal_unnaamai_cinematic.mp4",
                duration: "279.27s (4m 39s)",
                artworks: "46 (100% Unique MD5)",
                size: "Master 46-Shot Film",
                shotDuration: "6.07s",
                scenes: [
{scenes_js}
                ]
            }},"""

content = HTML_PATH.read_text(encoding="utf-8")
import re
pattern = r"26:\s*\{[\s\S]*?\}\s*,\s*27:"
replacement = ch26_js_replacement + "\n            27:"
new_content = re.sub(pattern, replacement, content)

HTML_PATH.write_text(new_content, encoding="utf-8")
print(f"Updated {HTML_PATH.name} with {len(files)} scenes for Chapter 26!")

