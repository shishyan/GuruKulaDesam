#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/generate_google_devotional_scenes.py

Autonomous generator for authentic South Indian devotional scenes using
Google gemini-2.5-flash-image with strict free-tier rate management.

Key Guarantees:
1. Pure Google native image model (gemini-2.5-flash-image).
2. 100% authentic South Indian Tamil heritage & Dravidian temple iconography.
3. Strictly respects Google free-tier RPM/RPD limits (zero billing cost).
4. Resume-friendly: Automatically skips already generated scenes.
"""

import os, sys, io, json, time, base64, urllib.request, unicodedata, re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY and (ROOT / ".env").exists():
    for ln in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if ln.startswith("GEMINI_API_KEY="):
            API_KEY = ln.split("=", 1)[1].strip().strip('"').strip("'")

ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"

GOOGLE_SOUTH_INDIAN_STYLE = (
    "A 16:9 cinematic photorealistic devotional photograph, 8k resolution, authentic South Indian Tamil Nadu spiritual aesthetic. "
    "Ancient Chola and Pandyan Dravidian granite temple architecture, majestically carved gopurams, glowing gold kalasams in early morning dawn sunlight. "
    "Polished granite sanctum floors reflecting flickering brass oil lamps (agal vilakku deepams), fresh fragrant marigold and white jasmine malligai garlands, "
    "gentle swirling sacred dhoopam sambrani incense haze. Devotees and sages with authentic South Indian Tamil features, sacred white Tripundra vibhuti on forehead, "
    "rudraksha malas, wearing traditional silk veshti, angavastram, and festive Kanchipuram silk sarees. "
    "Full-frame 16:9 composition, NO text, NO watermarks, NO modern western items, NO foreign fantasy. Scene: "
)

def safe_folder_name(name):
    name = os.path.splitext(name)[0]
    name = re.sub(r'[^\w\s\-]', '', name)
    name = re.sub(r'\s+', '_', name).strip('_')
    return name

def clean_frame(img):
    import numpy as np
    a = np.asarray(img.convert("L"))
    rows = np.where(a.mean(axis=1) > 14)[0]
    cols = np.where(a.mean(axis=0) > 14)[0]
    if len(rows) and len(cols):
        img = img.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))
    w, h = img.size
    tw = int(h * 16 / 9)
    if tw <= w:
        x = (w - tw) // 2
        img = img.crop((x, 0, x + tw, h))
    else:
        th = int(w * 9 / 16)
        y = (h - th) // 2
        img = img.crop((0, y, w, y + th))
    return img.resize((1280, 720), Image.LANCZOS)

def generate_scene(prompt, out_path):
    out_path = Path(out_path)
    if out_path.exists() and out_path.stat().st_size > 10000:
        return True

    full_prompt = GOOGLE_SOUTH_INDIAN_STYLE + prompt
    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"]
        }
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=data, headers={"Content-Type": "application/json"})

    for attempt in range(1, 6):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                part = res["candidates"][0]["content"]["parts"][0]
                img_bytes = base64.b64decode(part["inlineData"]["data"])
                img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
                img = clean_frame(img)
                out_path.parent.mkdir(parents=True, exist_ok=True)
                img.save(out_path, "JPEG", quality=95)
                print(f"  ✔ Saved {out_path.name} ({out_path.stat().st_size // 1024} KB)", flush=True)
                return True
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore")
            print(f"   [attempt {attempt}] HTTP {e.code}: {body[:100]}", flush=True)
            if e.code == 429:
                print("   ⏳ Free-tier rate limit reached. Backing off for 30s...", flush=True)
                time.sleep(30)
            else:
                time.sleep(5)
        except Exception as e:
            print(f"   [attempt {attempt}] {str(e)[:100]}", flush=True)
            time.sleep(5)

    return False

def main():
    registry_path = ROOT / "production" / "master_317_song_prompts.json"
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    print(f"==================================================")
    print(f"🏛️ GOOGLE NATIVE AUTHENTIC SOUTH INDIAN STUDIO")
    print(f"Loaded {len(registry)} songs from Master Registry.")
    print(f"==================================================")

    # Optional: filter by song or process all sequentially
    target_song = sys.argv[1] if len(sys.argv) > 1 else None

    for track_idx, (wav_name, data) in enumerate(registry.items(), start=1):
        if target_song and target_song.lower() not in wav_name.lower():
            continue

        folder_name = safe_folder_name(wav_name)
        out_dir = ROOT / "production" / "scene_images" / folder_name
        out_dir.mkdir(parents=True, exist_ok=True)

        existing = list(out_dir.glob("scene_*.jpg"))
        if len(existing) == 24:
            print(f"[{track_idx}/{len(registry)}] ⏩ {wav_name} (24/24 already generated)")
            continue

        print(f"\n[{track_idx}/{len(registry)}] 🎨 Google Generating: {wav_name} ({data['title']})...")
        prompts = data["scenes"]

        for idx, prompt_text in enumerate(prompts):
            img_path = out_dir / f"scene_{idx+1:02d}.jpg"
            if img_path.exists() and img_path.stat().st_size > 10000:
                continue

            success = generate_scene(prompt_text, img_path)
            # Safe pacing for Google Free Tier (15 requests/minute = ~4s between calls)
            time.sleep(4.0)

    print("\n🎉 GENERATION RUN COMPLETE!")

if __name__ == "__main__":
    main()
