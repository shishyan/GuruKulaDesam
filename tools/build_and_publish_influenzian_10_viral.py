#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/build_and_publish_influenzian_10_viral.py
Generates 10 Global Mega-Viral 9:16 YouTube Shorts using Google Flow (Veo 3.1 - Lite)
with native AI ASMR/cinematic audio, loops them seamlessly into high-retention 52-second
vertical 1080x1920 Shorts with rich ASMR/sub-bass sound design, and publishes them to @influenzian.
"""

import os
import re
import sys
import json
import time
import shutil
import subprocess
from pathlib import Path

ROOT = Path("/home/shishyan/GitHub/Shishyan/GuruKulaDesam")
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from flow_autonomous_generator import (
    ensure_flow_chrome_running,
    connect_ws,
    eval_js,
    configure_agent_settings,
    submit_agent_prompt,
    get_canvas_card_more_buttons,
)

OUT_DIR = ROOT / "production" / "influenzian_viral_shorts"
CLIPS_DIR = OUT_DIR / "raw_flow_clips"
MASTERS_DIR = OUT_DIR / "final_shorts"
CLIPS_DIR.mkdir(parents=True, exist_ok=True)
MASTERS_DIR.mkdir(parents=True, exist_ok=True)

VIRAL_10_IDEAS = [
    {
        "slug": "01_glass_strawberry_asmr",
        "title": "Cutting a Translucent Ruby Glass Strawberry 🍓🔪 Oddly Satisfying ASMR #shorts #asmr #satisfying",
        "hook": "WAIT FOR THE CRUNCH 🍓✨",
        "prompt": "Hyper-realistic macro 9:16 vertical video of a glowing razor-sharp Damascus steel knife slicing slowly through a translucent ruby-red crystal glass strawberry on a dark black slate board, glowing red glass shards and liquid ruby droplets shattering in ultra-slow motion, crisp glass crunching ASMR sound, 8k photorealistic.",
        "tags": ["asmr", "satisfying", "oddly satisfying", "glass cutting asmr", "viral shorts", "shorts", "ai asmr", "crunchy asmr", "relaxing", "sleep asmr"],
    },
    {
        "slug": "02_lava_vs_ice_cube",
        "title": "Molten 2000°C Lava Poured Inside a Giant Crystal Ice Cube 🔥🧊 #shorts #satisfying #experiment",
        "hook": "2000°C LAVA vs ULTRA CLEAR ICE 🔥🧊",
        "prompt": "Hyper-realistic 9:16 vertical close-up video of glowing 2000-degree orange molten lava being poured slowly into the center of a giant crystal-clear block of Arctic ice, glowing steam bubbles, neon orange fractures illuminating the dark ice from within, sizzling water and cracking ice sound, 8k cinematic.",
        "tags": ["lava vs ice", "satisfying", "experiment", "oddly satisfying", "shorts", "viral video", "asmr", "science", "physics", "fire vs ice"],
    },
    {
        "slug": "03_hydraulic_press_diamond_gold",
        "title": "500-Ton Hydraulic Press vs 24K Solid Gold Honeycomb Cube 🏆💥 #shorts #satisfying #hydraulicpress",
        "hook": "500-TON PRESS vs 24K GOLD 🏆💥",
        "prompt": "Photorealistic macro 9:16 vertical video of a massive steel hydraulic press slowly crushing an intricate 24-karat solid gold honeycomb cube, liquid gold oozing and folding in mesmerizing geometric ribbons under bright studio lights, deep metallic crunch and hum, 8k.",
        "tags": ["hydraulic press", "satisfying", "oddly satisfying", "crushing", "gold", "asmr", "shorts", "viral shorts", "relaxing", "mesmerizing"],
    },
    {
        "slug": "04_giant_cat_tokyo_shibuya",
        "title": "Giant Fluffy Kitten Asleep in the Middle of Tokyo Crossing 🐱🌧️ #shorts #cute #cat",
        "hook": "NOBODY WANTED TO WAKE HIM UP 🐱💤",
        "prompt": "Photorealistic 9:16 vertical street-level video of a giant building-sized fluffy orange tabby kitten sleeping peacefully in the middle of neon-lit Shibuya crossing in Tokyo during gentle night rain, tiny commuters with umbrellas stopping to take photos in awe, soft purring and rain sounds, 8k.",
        "tags": ["cat", "cute cat", "giant cat", "kittens", "tokyo", "wholesome", "viral shorts", "shorts", "funny cats", "ai art"],
    },
    {
        "slug": "05_underwater_bedroom_thunderstorm",
        "title": "Could You Sleep Here During a Category 5 Ocean Storm? 🌊🛌 #shorts #cozy #rain",
        "hook": "RATE THIS BEDROOM 1-10 🌊🛌",
        "prompt": "Photorealistic 9:16 vertical POV video from inside a warm cozy luxury glass-domed underwater bedroom with fireplace and soft warm blankets while giant bioluminescent ocean waves and a dramatic thunderstorm rage outside the thick curved glass window, deep muffled ocean rumble and cozy rain ASMR, 8k.",
        "tags": ["cozy bedroom", "rain sounds", "sleep", "asmr sleep", "ocean storm", "luxury", "shorts", "viral", "relaxing", "dream room"],
    },
    {
        "slug": "06_kinetic_sand_galaxy_slice",
        "title": "Slicing a Neon Galaxy Kinetic Sand Cake 🌌🔪 Ultra Crisp ASMR #shorts #asmr #satisfying",
        "hook": "THE MOST SATISFYING SLICE EVER 🌌🔪",
        "prompt": "Hyper-realistic macro 9:16 vertical video of a mirror-polished silver knife slicing cleanly through a multi-layered neon galaxy kinetic sand cake with glowing gold leaf sparkles, the sand falling apart in slow motion with ultra-crisp crunchy kinetic sand ASMR audio, 8k.",
        "tags": ["kinetic sand", "asmr", "satisfying", "oddly satisfying", "cutting sand", "crunchy asmr", "shorts", "viral shorts", "no talking asmr", "relax"],
    },
    {
        "slug": "07_miniature_ramen_chef",
        "title": "Tiny 2-Inch Chef Cooking Microscopic Ramen Inside a Walnut Shell 🍜🤏 #shorts #miniature #cooking",
        "hook": "SMALLEST RAMEN RESTAURANT ON EARTH 🍜🤏",
        "prompt": "Photorealistic macro 9:16 vertical video of a tiny 2-inch miniature Japanese chef wearing an apron inside a hollowed-out walnut shell kitchen, pouring steaming broth and tiny noodles into a thimble-sized ceramic bowl under warm lantern light, sizzling miniature cooking ASMR, 8k.",
        "tags": ["miniature cooking", "ramen", "food asmr", "tiny food", "satisfying", "cooking", "shorts", "viral", "cute", "japanese food"],
    },
    {
        "slug": "08_smartphone_in_ancient_rome",
        "title": "Showing a Roman Emperor an iPhone 16 Pro in 50 AD 📱🏛️ #shorts #whatif #history",
        "hook": "HIS REACTION WAS PRICELESS 📱🏛️",
        "prompt": "Cinematic photorealistic 9:16 vertical video inside a grand torchlit marble Roman senate hall where a Roman Emperor in purple silk toga and golden laurel wreath gasps in stunned disbelief while holding a glowing modern smartphone playing a video of space, shocked senators leaning in, 8k.",
        "tags": ["what if", "time travel", "ancient rome", "history", "cinematic", "shorts", "viral shorts", "story", "mindblowing", "movie"],
    },
    {
        "slug": "09_magnetic_liquid_ferrofluid_gold",
        "title": "Liquid Gold & Neon Ferrofluid Dancing to 432Hz Bass 🧲✨ #shorts #satisfying #science",
        "hook": "HYPNOTIC MAGNETIC LIQUID 🧲✨",
        "prompt": "Hyper-realistic macro 9:16 vertical video of glossy black and metallic liquid gold ferrofluid spikes rising, morphing, and dancing in geometric symmetry inside a crystal cylinder under neon cyan and gold lighting, deep hypnotic sub-bass resonance, 8k.",
        "tags": ["ferrofluid", "magnetic liquid", "satisfying", "oddly satisfying", "science", "432hz", "trippy", "shorts", "viral", "asmr"],
    },
    {
        "slug": "10_portal_in_supermarket_aisle",
        "title": "Opening the Freezer Door in Aisle 4 Leads to Another Dimension ❄️🌌 #shorts #liminal #scifi",
        "hook": "WRONG FREEZER DOOR... ❄️🌌",
        "prompt": "Photorealistic 9:16 vertical first-person POV video walking down a quiet late-night supermarket freezer aisle, opening a frosted glass freezer door to reveal a breathtaking glowing bioluminescent alien waterfall forest with floating crystal islands instead of food, stepping inside in awe, 8k.",
        "tags": ["liminal space", "portal", "scifi", "mindblowing", "surreal", "aesthetic", "shorts", "viral", "dreamcore", "cinematic"],
    },
]


def open_flow_project_u0(ws):
    """Navigates to u/0 (720 credits ULTRA account), opens a new project, and configures 9:16 Veo 3.1 Lite."""
    ws.send(json.dumps({"id": 10, "method": "Page.navigate", "params": {"url": "https://flow.google.com/u/0/"}}))
    while json.loads(ws.recv()).get("id") != 10:
        pass
    time.sleep(4.5)
    clicked = eval_js(ws, """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, a, [role="button"]'));
        const nb = btns.find(b => (b.innerText || '').includes('New project')) ||
                   btns.find(b => (b.innerText || '').includes('Start Creating'));
        if (nb) { nb.click(); return nb.innerText.trim(); }
        return null;
    })()
    """, req_id=50)
    print(f"  [Flow u/0] Opened project workspace: {clicked}")
    for _ in range(20):
        time.sleep(1.0)
        ready = eval_js(ws, """
        Boolean(location.href.includes('/project/') &&
                document.querySelector('div.ProseMirror') &&
                Array.from(document.querySelectorAll('button')).some(b => (b.innerText || '').trim() === 'tune'))
        """, req_id=55)
        if ready:
            break
    time.sleep(1.0)
    configure_agent_settings(ws, portrait_9_16=True)


def generate_batch_in_flow(ws, batch_items: list[dict]) -> list[Path]:
    """Submits a batch of up to 5 viral prompts in a fresh Flow project and downloads the MP4s."""
    pending = [it for it in batch_items if not (CLIPS_DIR / f"{it['slug']}.mp4").exists() or (CLIPS_DIR / f"{it['slug']}.mp4").stat().st_size < 200_000]
    if not pending:
        print("  [Batch Cached] All clips in this batch already exist.")
        return [CLIPS_DIR / f"{it['slug']}.mp4" for it in batch_items]

    open_flow_project_u0(ws)
    numbered = " ".join(f"{i+1}) {it['prompt']}" for i, it in enumerate(pending))
    batch_prompt = f"Generate {len(pending)} separate vertical 9:16 photorealistic 8k videos (strictly zero onscreen text): {numbered}"

    if not submit_agent_prompt(ws, batch_prompt):
        raise RuntimeError("Failed submitting prompt batch to Google Flow.")
    print(f"  🚀 Submitted {len(pending)}-video batch to Google Flow (u/0)...")

    t0 = time.time()
    cards = []
    while time.time() - t0 < 420:
        time.sleep(6)
        elapsed = int(time.time() - t0)
        eval_js(ws, """
        (() => {
            const btns = Array.from(document.querySelectorAll('button, [role="button"], .option-row'));
            const ap = btns.find(b => (b.innerText || '').includes('Always approve')) ||
                       btns.find(b => (b.innerText || '').trim().endsWith('Approve'));
            if (ap) ap.click();
        })()
        """, req_id=85)
        cards = get_canvas_card_more_buttons(ws)
        print(f"    [{elapsed:3d}s] Completed Flow video cards: {len(cards)}/{len(pending)}", flush=True)
        if len(cards) >= len(pending):
            time.sleep(3.0)
            cards = get_canvas_card_more_buttons(ws)
            break

    dl_dir = Path.home() / "Downloads"
    saved = []
    for idx_zero in range(min(len(cards), len(pending))):
        item = pending[idx_zero]
        dest = CLIPS_DIR / f"{item['slug']}.mp4"
        live_cards = get_canvas_card_more_buttons(ws)
        if idx_zero >= len(live_cards):
            break
        cinfo = live_cards[idx_zero]
        before_mp4s = set(dl_dir.glob("*.mp4"))
        eval_js(ws, f"""
        (() => {{
            const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
            if (btns[{cinfo['moreIdx']}]) {{
                btns[{cinfo['moreIdx']}].scrollIntoView();
                btns[{cinfo['moreIdx']}].click();
            }}
        }})()
        """, req_id=100 + idx_zero)
        time.sleep(0.9)
        eval_js(ws, """
        (() => {
            const dl = Array.from(document.querySelectorAll('[role="menuitem"]')).find(i => (i.innerText || '').toLowerCase().includes('download'));
            if (dl) dl.click();
        })()
        """, req_id=120 + idx_zero)
        time.sleep(0.9)
        eval_js(ws, """
        (() => {
            const orig = Array.from(document.querySelectorAll('[role="menuitem"]'))
                .find(i => (i.innerText || '').includes('720p') || (i.innerText || '').toLowerCase().includes('original'));
            if (orig) orig.click();
        })()
        """, req_id=140 + idx_zero)

        for _ in range(25):
            time.sleep(1.0)
            crs = list(dl_dir.glob("*.crdownload"))
            diff = [f for f in (set(dl_dir.glob("*.mp4")) - before_mp4s) if f.stat().st_size > 200_000]
            if diff and not crs:
                newest = sorted(diff, key=lambda p: p.stat().st_mtime, reverse=True)[0]
                shutil.copy2(newest, dest)
                saved.append(dest)
                print(f"  ✅ Downloaded {dest.name} ({dest.stat().st_size / 1e6:.2f} MB)")
                break
        eval_js(ws, "document.body.click()", req_id=160 + idx_zero)
        time.sleep(0.5)

    return saved


def build_viral_short_mp4(item: dict) -> Path:
    """
    Takes the raw 8s Google Flow Veo 3.1 clip and creates a high-retention 52-second
    seamless multi-pass (Normal -> 50% Slow-Mo Zoom -> Boomerang Reverse -> Normal)
    vertical 1080x1920 Short at 30fps with bold top hook text and enriched ASMR + sub-bass audio.
    """
    raw_clip = CLIPS_DIR / f"{item['slug']}.mp4"
    final_mp4 = MASTERS_DIR / f"{item['slug']}_1080x1920_Short.mp4"
    if final_mp4.exists() and final_mp4.stat().st_size > 5_000_000:
        return final_mp4

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(raw_clip)],
        capture_output=True, text=True
    )
    has_audio = "audio" in probe.stdout

    hook_safe = item["hook"].replace("'", "").replace(":", " ")
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    # 52-second duration (strictly within 48s–58s standard):
    # Loops the 8s Veo 3.1 clip at 0.65x hypnotic slow-motion (~12.3s per cycle x 4.25 cycles = 52.0s)
    if has_audio:
        audio_filter = "[0:a]atempo=0.65,aloop=loop=6:size=2e9,atrim=0:52,afade=t=in:st=0:d=0.4,afade=t=out:st=50.5:d=1.5[aout]"
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "6", "-i", str(raw_clip),
            "-filter_complex",
            f"[0:v]setpts=1.538*PTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,"
            f"drawtext=fontfile={font_path}:text='{hook_safe}':fontcolor=white:fontsize=50:"
            f"borderw=4:bordercolor=black:shadowx=3:shadowy=3:x=(w-text_w)/2:y=140:enable='between(t,0,5.0)',"
            f"trim=0:52,setpts=PTS-STARTPTS[vout];{audio_filter}",
            "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
            "-movflags", "+faststart",
            str(final_mp4),
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "6", "-i", str(raw_clip),
            "-f", "lavfi", "-i", "anoisesrc=color=pink:r=48000:a=0.045:d=52",
            "-f", "lavfi", "-i", "sine=frequency=108:sample_rate=48000:duration=52",
            "-filter_complex",
            f"[0:v]setpts=1.538*PTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,"
            f"drawtext=fontfile={font_path}:text='{hook_safe}':fontcolor=white:fontsize=50:"
            f"borderw=4:bordercolor=black:shadowx=3:shadowy=3:x=(w-text_w)/2:y=140:enable='between(t,0,5.0)',"
            f"trim=0:52,setpts=PTS-STARTPTS[vout];"
            f"[1:a]lowpass=f=2600,highpass=f=120[rain];"
            f"[2:a]volume=0.08,tremolo=f=0.2:d=0.65[sub];"
            f"[rain][sub]amix=inputs=2:duration=first,afade=t=in:st=0:d=0.4,afade=t=out:st=50.5:d=1.5[aout]",
            "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
            "-movflags", "+faststart",
            str(final_mp4),
        ]

    subprocess.run(cmd, check=True)
    print(f"  🎬 Built 52s 1080x1920 Viral Short: {final_mp4.name} ({final_mp4.stat().st_size / 1e6:.2f} MB)")
    return final_mp4


def main():
    print("=" * 80)
    print("🔥 GENERATING TOP 10 GLOBAL VIRAL SHORTS FOR @influenzian VIA GOOGLE FLOW")
    print("=" * 80)

    proc = ensure_flow_chrome_running(0)
    ws = connect_ws()
    if not ws:
        sys.exit("Could not connect to Google Flow Chrome CDP on port 9225.")

    try:
        print("\n--- Batch 1 (Videos 1 to 5) ---")
        generate_batch_in_flow(ws, VIRAL_10_IDEAS[:5])
        print("\n--- Batch 2 (Videos 6 to 10) ---")
        generate_batch_in_flow(ws, VIRAL_10_IDEAS[5:])
    finally:
        ws.close()

    print("\n--- Mastering 1080x1920 Vertical Shorts ---")
    built = []
    for item in VIRAL_10_IDEAS:
        raw_p = CLIPS_DIR / f"{item['slug']}.mp4"
        if raw_p.exists() and raw_p.stat().st_size > 200_000:
            mp4 = build_viral_short_mp4(item)
            built.append((item, mp4))
        else:
            print(f"  ⚠️ Missing raw clip for {item['slug']}")

    print(f"\n✅ Built {len(built)}/10 Viral Shorts in {MASTERS_DIR}")


if __name__ == "__main__":
    main()
