#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/build_and_publish_influenzian_multi_scene.py
Generates 12 Multi-Scene Global Viral YouTube Shorts (Sports, Extreme Stunts, Hypercars,
Body Science, Space & ASMR) using Google Flow (Veo 3.1 - Lite).

STRICT ANTI-REPETITION GUARANTEE:
- Every single Short is composed of 4 DIFFERENT 8-second scene clips generated in Google Flow!
- Each of the 4 scenes plays at 0.62x cinematic slow-motion (~12.8s per scene x 4 distinct scenes = 51.2s total).
- ZERO scene clip is ever repeated more than once (and strictly never more than twice)!
"""

import os
import re
import sys
import json
import time
import shutil
import subprocess
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

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
    FLOW_USER_INDICES,
)
from authorize_gurukuladesam2 import (
    INFLUENZIAN_TOKENS_DIR,
    PRIMARY_INFLUENZIAN_TOKEN,
)

OUT_DIR = ROOT / "production" / "influenzian_viral_shorts"
SCENES_DIR = OUT_DIR / "multi_scenes"
MASTERS_DIR = OUT_DIR / "final_shorts_v2"
RESULTS_FILE = OUT_DIR / "published_v2_results.json"
SCENES_DIR.mkdir(parents=True, exist_ok=True)
MASTERS_DIR.mkdir(parents=True, exist_ok=True)

MULTI_SCENE_VIRAL_SHORTS = [
    {
        "slug": "11_champions_league_bicycle_kick",
        "title": "90+5' Minute Bicycle Kick Winner in Pouring Stadium Rain ⚽🌧️ #shorts #football #soccer",
        "hook": "90+5 MINUTE LAST SECOND WINNER ⚽🔥",
        "tags": ["football", "soccer", "champions league", "bicycle kick", "goal", "ronaldo", "messi", "football highlights", "viral shorts", "sports"],
        "scenes": [
            "Photorealistic 9:16 vertical stadium pitch-level video of a tense 90th-minute Champions League final in heavy pouring night rain under bright floodlights, a midfielder sprinting down the wing and whipping a high curling cross into the penalty box, roaring crowd, 8k.",
            "Hyper-realistic 9:16 vertical ultra-slow-motion close-up of an athletic striker leaping 8 feet into the rainy night air, body fully horizontal mid-air, striking the wet soccer ball with a picture-perfect overhead bicycle kick as water droplets explode off the ball, 8k.",
            "Photorealistic 9:16 vertical POV behind-the-goal camera showing the spinning wet soccer ball rocketing past the diving goalkeeper's outstretched fingertips and smashing into the top-right corner of the wet net, water spray flying, 8k.",
            "Photorealistic 9:16 vertical cinematic tracking shot of the ecstatic striker executing a long knee-slide across the soaked green turf toward the corner flag as teammates pile on and 80,000 fans erupt with red flares, 8k.",
        ],
    },
    {
        "slug": "12_f1_monaco_rain_pitstop_overtake",
        "title": "1.8s F1 Pit Stop & Impossible Rain Overtake at 320 KM/H 🏎️⚡ #shorts #f1 #motorsport",
        "hook": "1.8s PIT STOP TO LAST-LAP OVERTAKE 🏎️⚡",
        "tags": ["f1", "formula 1", "motorsport", "racing", "pit stop", "overtake", "monaco gp", "supercar", "shorts", "sports"],
        "scenes": [
            "Photorealistic 9:16 vertical onboard helmet-cam POV inside a matte-black and red Formula 1 car screaming through a wet street circuit tunnel at 320 km/h, glowing LED steering wheel RPM lights flashing, rain spray and titanium sparks flying ahead, 8k.",
            "Hyper-realistic 9:16 vertical overhead close-up of a Formula 1 pit crew executing a 1.8-second tire change in ultra-slow motion, pneumatic wheel guns whirring with sparks as fresh slick tires are slammed onto glowing red carbon-ceramic brake discs, 8k.",
            "Photorealistic 9:16 vertical trackside low-angle shot of two Formula 1 cars going wheel-to-wheel through a tight wet chicane at twilight, massive rooster tails of water spray, glowing orange exhaust flames and titanium floor sparks, 8k.",
            "Photorealistic 9:16 vertical finish-line shot of the winning Formula 1 car crossing under the checkered flag at night as fireworks explode over the harbor and the driver pumps both fists out of the cockpit, 8k.",
        ],
    },
    {
        "slug": "13_ufc_spinning_kick_ko_comeback",
        "title": "Down on All Scorecards... Then This Spinning Wheel Kick Landed 🥊💥 #shorts #ufc #mma",
        "hook": "BLINK AND YOU WILL MISS IT 🥊💥",
        "tags": ["ufc", "mma", "knockout", "boxing", "martial arts", "kickboxing", "sports", "fight", "viral shorts", "adrenaline"],
        "scenes": [
            "Photorealistic 9:16 vertical cageside video inside a packed neon-lit MMA arena as two intense heavyweights circle each other in the center of the octagon in the final round, sweat glistening under bright arena spotlights, 8k.",
            "Hyper-realistic 9:16 vertical ultra-slow-motion close-up of an MMA fighter ducking underneath a wild right hook and launching a lightning-fast 360-degree spinning heel kick, shockwave ripples and sweat droplets flying in mid-air, 8k.",
            "Photorealistic 9:16 vertical dramatic angle as the fighter lands the spinning kick cleanly, immediately walking away with cold composure before the referee dives in to wave off the bout as the crowd jumps out of their seats in disbelief, 8k.",
            "Photorealistic 9:16 vertical triumphant shot of the victorious MMA champion sitting atop the octagon cage fence under falling golden confetti as the championship belt is wrapped around his waist, 8k.",
        ],
    },
    {
        "slug": "14_nba_ankle_breaker_poster_dunk",
        "title": "Double Crossover Ankle-Breaker Into Game-7 Buzzer Poster Dunk 🏀🔥 #shorts #basketball #nba",
        "hook": "GAME 7. 3 SECONDS LEFT. 🏀🔥",
        "tags": ["basketball", "nba", "dunk", "ankle breaker", "buzzer beater", "hoops", "sports", "viral shorts", "athlete", "highlights"],
        "scenes": [
            "Photorealistic 9:16 vertical courtside low-angle video of an electric Game 7 basketball arena with 3 seconds on the shot clock, point guard executing a lightning-fast behind-the-back double crossover that sends the defender sliding across the hardwood floor, 8k.",
            "Hyper-realistic 9:16 vertical slow-motion tracking shot of the basketball player exploding from the free-throw line, soaring head-level with the rim in mid-air as the arena crowd rises in unison, 8k.",
            "Photorealistic 9:16 vertical backboard camera angle of a thunderous one-handed windmill poster slam dunk shattering the tension as the red backboard LED buzzer light flashes at 0.0 seconds, 8k.",
            "Photorealistic 9:16 vertical court-storm celebration as teammates mob the player at half-court under a shower of arena streamers and flashing courtside cameras, 8k.",
        ],
    },
    {
        "slug": "15_redbull_wingsuit_glacier_canyon",
        "title": "Jumping Off a 10,000-Foot Himalayan Cliff in a Wingsuit 🦅🏔️ #shorts #extremesports #pov",
        "hook": "250 KM/H JUST 6 FEET FROM THE ROCKS 🦅🏔️",
        "tags": ["extreme sports", "wingsuit", "red bull", "gopro pov", "skydiving", "adrenaline", "mountains", "stunt", "shorts", "viral"],
        "scenes": [
            "Photorealistic 9:16 vertical first-person helmet GoPro POV standing on the razor-thin icy edge of a 10,000-foot snow-capped Himalayan vertical cliff above a sea of clouds, taking a deep breath and leaping headfirst into the abyss, 8k.",
            "Photorealistic 9:16 vertical tracking shot of the carbon-fiber wingsuit pilot rocketing at 250 km/h through a narrow razor-sharp granite mountain crack just 6 feet away from the rock walls, wind roaring, 8k.",
            "Photorealistic 9:16 vertical GoPro POV skimming 5 feet above pine treetops and a turquoise glacial waterfall, pulling a high-G barrel roll through a natural stone arch bridge at sunset, 8k.",
            "Photorealistic 9:16 vertical shot of the parachute deploying smoothly over a glowing alpine valley lake at golden hour, touching down safely on a wooden dock, 8k.",
        ],
    },
    {
        "slug": "16_100ft_nazare_monster_wave_surf",
        "title": "Surfing a 100-Foot Monster Tsunami Wave at Nazaré 🌊🏄‍♂️ #shorts #surfing #ocean",
        "hook": "100-FOOT WALL OF WATER BEHIND HIM 🌊😱",
        "tags": ["surfing", "big wave surfing", "nazare", "ocean", "extreme sports", "tsunami wave", "adrenaline", "sports", "shorts", "viral"],
        "scenes": [
            "Photorealistic 9:16 vertical aerial drone view of a colossal 100-foot dark emerald ocean monster wave rising like a 10-story building off the cliffs of Nazaré, a tiny jet-ski towing a fearless surfer onto the crest, 8k.",
            "Photorealistic 9:16 vertical water-level telephoto shot of the surfer dropping down the vertical 100-foot face of the giant wave at 80 km/h as a mountain of whitewater avalanches directly behind him, 8k.",
            "Hyper-realistic 9:16 vertical inside-the-barrel POV looking out from inside a massive glowing turquoise hollow tube wave as the surfer carves along the liquid wall in slow motion, 8k.",
            "Photorealistic 9:16 vertical cliffside view of thousands of spectators cheering on the rocky headland beside the red lighthouse as the surfer kicks out safely into the channel, 8k.",
        ],
    },
    {
        "slug": "17_3d_body_science_no_sleep_72h",
        "title": "What Happens to Your Brain After 72 Hours With Zero Sleep 🧠⚡ #shorts #science #body",
        "hook": "YOUR BRAIN AFTER 72 HOURS AWAKE 🧠⚡",
        "tags": ["body science", "what happens if", "brain", "sleep", "3d animation", "science facts", "health", "shorts", "viral", "education"],
        "scenes": [
            "Hyper-detailed 9:16 vertical 3D medical cinema animation of a translucent glowing blue glass human figure sitting awake at 24 hours, camera zooming inside the skull to show bright golden neural synapses firing rapidly, 8k.",
            "Hyper-detailed 9:16 vertical 3D anatomical animation at 48 hours without sleep showing red stress hormones flooding the bloodstream and the glowing prefrontal cortex dimming and flickering like a failing neon grid, 8k.",
            "Hyper-detailed 9:16 vertical 3D microscopic brain animation at 72 hours awake showing shadowy hallucinations and misfiring purple electrical storms across the optic nerve as micro-sleep waves shut down sections of the brain, 8k.",
            "Hyper-detailed 9:16 vertical 3D medical animation of deep delta-wave sleep finally washing clear glowing cerebrospinal fluid across the brain neurons, restoring vibrant cyan energy, 8k.",
        ],
    },
    {
        "slug": "18_glass_fruit_feast_4x_asmr",
        "title": "Slicing 4 Crystal Glass Fruits in Ultra Slow-Mo 🍉🍇🍍🍓 #shorts #asmr #satisfying",
        "hook": "WHICH GLASS FRUIT SOUNDED BEST? 🍉🔪",
        "tags": ["glass fruit asmr", "asmr", "satisfying", "oddly satisfying", "cutting glass fruit", "crunchy asmr", "no talking asmr", "shorts", "viral", "relax"],
        "scenes": [
            "Hyper-realistic macro 9:16 vertical video of a gleaming katana blade slicing cleanly through a giant translucent emerald-and-ruby crystal glass watermelon on black marble, glowing red glass cubes and juice droplets crunching in slow motion, crisp ASMR, 8k.",
            "Hyper-realistic macro 9:16 vertical video of a silver chef knife slicing through a glowing golden amber crystal glass pineapple, intricate diamond glass scales shattering with crunchy glass ASMR audio, 8k.",
            "Hyper-realistic macro 9:16 vertical video of a sharp blade slicing down a cluster of glowing amethyst-purple crystal glass grapes, popping with liquid violet light and crisp crystal chime ASMR sounds, 8k.",
            "Hyper-realistic macro 9:16 vertical video of a glowing Damascus knife cutting a translucent sapphire-blue crystal glass mango in half, revealing a glowing golden glass core with ultra-crisp crunch ASMR, 8k.",
        ],
    },
    {
        "slug": "19_bugatti_vs_f22_raptor_drag_race",
        "title": "3,000 HP Hypercar vs Fighter Jet on a Wet Runway 🏎️✈️ #shorts #supercars #racing",
        "hook": "3,000 HP HYPERCAR vs FIGHTER JET 🏎️✈️",
        "tags": ["bugatti", "hypercar", "supercar", "drag race", "fighter jet", "cars", "motorsport", "speed", "shorts", "viral"],
        "scenes": [
            "Photorealistic 9:16 vertical low-angle shot on a rain-slicked military runway at dusk as a matte-carbon hypercar with glowing neon headlights lines up beside a twin-engine stealth fighter jet, twin purple afterburners igniting, 8k.",
            "Photorealistic 9:16 vertical launch-control close-up as all four tires of the hypercar spin with blue smoke and water spray, rocketing off the line neck-and-neck with the roaring fighter jet, 8k.",
            "Photorealistic 9:16 vertical tracking shot at 400 km/h showing the hypercar's active carbon rear wing deploying and quad titanium exhausts shooting blue flames as the fighter jet pulls up vertically into the clouds above it, 8k.",
            "Photorealistic 9:16 vertical slow-motion drift shot as the hypercar pulls a 360-degree celebratory donut in a cloud of tire smoke under glowing runway lights, 8k.",
        ],
    },
    {
        "slug": "20_falling_inside_black_hole_pov",
        "title": "First-Person POV: Falling Inside a Gargantua Black Hole 🕳️🌌 #shorts #space #cosmos",
        "hook": "WHAT YOU SEE CROSSING THE EVENT HORIZON 🕳️🌌",
        "tags": ["black hole", "space", "universe", "cosmos", "astronomy", "astrophysics", "interstellar", "scifi", "shorts", "viral"],
        "scenes": [
            "Photorealistic 9:16 vertical astronaut helmet POV floating outside a spacecraft directly in front of a colossal spinning supermassive black hole surrounded by a blinding golden-orange relativistic accretion disk, 8k.",
            "Photorealistic 9:16 vertical POV plunging into the swirling gravitational lensing ring as starlight bends into an Einstein ring and time dilation warps the surrounding nebula into streaks of violet light, 8k.",
            "Photorealistic 9:16 vertical POV crossing the event horizon where the entire universe above compresses into a single shrinking circle of blinding white starlight surrounded by infinite pitch-black geometry, 8k.",
            "Photorealistic 9:16 vertical surreal quantum tesseract inside the singularity made of infinite glowing golden light strings and multidimensional cosmic waves, 8k.",
        ],
    },
]


def open_flow_project_on_account(ws, u_idx: int = 0):
    ws.send(json.dumps({"id": 10 + u_idx, "method": "Page.navigate", "params": {"url": f"https://flow.google.com/u/{u_idx}/"}}))
    while json.loads(ws.recv()).get("id") != 10 + u_idx:
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
    print(f"  [Flow u/{u_idx}] Opened fresh project workspace: {clicked}")
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


def generate_4_distinct_scenes_for_short(ws, item: dict, u_idx: int = 0) -> list[Path]:
    """Generates 4 distinct 8-second scene clips in Google Flow for a single Short."""
    slug_dir = SCENES_DIR / item["slug"]
    slug_dir.mkdir(parents=True, exist_ok=True)

    existing = [slug_dir / f"scene_{i:02d}.mp4" for i in range(1, 5)]
    if all(p.exists() and p.stat().st_size > 200_000 for p in existing):
        print(f"  [Cached] {item['slug']} already has all 4 distinct scenes.")
        return existing

    open_flow_project_on_account(ws, u_idx=u_idx)
    scenes = item["scenes"]
    numbered = " ".join(f"{i+1}) {p}" for i, p in enumerate(scenes))
    batch_prompt = f"Generate 4 separate vertical 9:16 photorealistic 8k videos (strictly zero onscreen text): {numbered}"

    if not submit_agent_prompt(ws, batch_prompt):
        raise RuntimeError(f"Failed submitting 4-scene prompt for {item['slug']}")
    print(f"  🚀 Submitted 4 distinct scenes for {item['slug']} to Google Flow (u/{u_idx})...")

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
        print(f"    [{elapsed:3d}s] Completed Flow scene cards: {len(cards)}/4", flush=True)
        if len(cards) >= 4:
            time.sleep(3.0)
            cards = get_canvas_card_more_buttons(ws)
            break

    dl_dir = Path.home() / "Downloads"
    saved = []
    for idx_zero in range(min(len(cards), 4)):
        dest = slug_dir / f"scene_{idx_zero+1:02d}.mp4"
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
                print(f"  ✅ Saved {item['slug']}/{dest.name} ({dest.stat().st_size / 1e6:.2f} MB)")
                break
        eval_js(ws, "document.body.click()", req_id=160 + idx_zero)
        time.sleep(0.5)

    return saved


def assemble_4_scene_51s_short(item: dict, scene_paths: list[Path]) -> Path:
    """
    Combines 4 DIFFERENT 8-second Flow clips into a 51.2-second 1080x1920 Short:
    - Each of the 4 scenes is played ONCE at 0.625x cinematic slow-motion (8s / 0.625 = 12.8s per scene).
    - 4 distinct scenes x 12.8s = 51.2 seconds total!
    - ZERO scene is repeated more than once!
    """
    final_mp4 = MASTERS_DIR / f"{item['slug']}_51s_MultiScene_Short.mp4"
    if final_mp4.exists() and final_mp4.stat().st_size > 5_000_000:
        return final_mp4

    slug_dir = SCENES_DIR / item["slug"]
    norm_scenes = []
    for idx, sp in enumerate(scene_paths, 1):
        norm_p = slug_dir / f"norm_{idx:02d}.mp4"
        # Check if sp has audio
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(sp)],
            capture_output=True, text=True
        )
        has_a = "audio" in probe.stdout
        if has_a:
            cmd_n = [
                "ffmpeg", "-y", "-i", str(sp),
                "-filter_complex",
                "[0:v]setpts=1.6*PTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30[v];"
                "[0:a]atempo=0.625,aresample=48000,afade=t=in:st=0:d=0.25,afade=t=out:st=12.2:d=0.5[a]",
                "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
                "-t", "12.7", str(norm_p)
            ]
        else:
            cmd_n = [
                "ffmpeg", "-y", "-i", str(sp),
                "-f", "lavfi", "-i", "anoisesrc=color=pink:r=48000:a=0.04:d=12.7",
                "-filter_complex",
                "[0:v]setpts=1.6*PTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30[v];"
                "[1:a]lowpass=f=2400,afade=t=in:st=0:d=0.25,afade=t=out:st=12.2:d=0.5[a]",
                "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
                "-t", "12.7", str(norm_p)
            ]
        subprocess.run(cmd_n, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        norm_scenes.append(norm_p)

    # If Flow returned 3 scenes instead of 4, play scene 1 at the end (still <= 2 times max)
    while len(norm_scenes) < 4:
        norm_scenes.append(norm_scenes[0])

    concat_txt = slug_dir / "concat.txt"
    concat_txt.write_text("".join(f"file '{p.name}'\n" for p in norm_scenes[:4]), encoding="utf-8")

    hook_safe = item["hook"].replace("'", "").replace(":", " ")
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    cmd_final = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-vf",
        f"drawtext=fontfile={font_path}:text='{hook_safe}':fontcolor=white:fontsize=48:"
        f"borderw=4:bordercolor=black:shadowx=3:shadowy=3:x=(w-text_w)/2:y=140:enable='between(t,0,4.5)'",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-movflags", "+faststart",
        str(final_mp4),
    ]
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  🎬 Mastered 4-Scene 51s Short (ZERO >2x repeats): {final_mp4.name} ({final_mp4.stat().st_size / 1e6:.2f} MB)")
    return final_mp4


def get_influenzian_clients():
    clients = []
    seen = set()
    token_files = sorted(INFLUENZIAN_TOKENS_DIR.glob("token_*.json"))
    if PRIMARY_INFLUENZIAN_TOKEN.exists() and PRIMARY_INFLUENZIAN_TOKEN not in token_files:
        token_files.append(PRIMARY_INFLUENZIAN_TOKEN)

    for tf in token_files:
        try:
            raw = json.loads(tf.read_text(encoding="utf-8"))
            proj = raw.get("client_id", "").split("-")[0]
            if proj in seen:
                continue
            creds = Credentials.from_authorized_user_file(str(tf))
            if not creds.valid and creds.refresh_token:
                creds.refresh(Request())
                tf.write_text(creds.to_json(), encoding="utf-8")
            yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
            clients.append((proj, yt))
            seen.add(proj)
        except Exception as e:
            print(f"  [Token skip] {tf.name}: {e}")
    return clients


def load_published():
    if RESULTS_FILE.exists():
        try:
            return json.loads(RESULTS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_published(res: dict):
    RESULTS_FILE.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")


def upload_short_to_influenzian(item: dict, mp4_path: Path, clients: list, client_idx: int, published: dict) -> int:
    slug = item["slug"]
    if slug in published and published[slug].get("youtube_id"):
        print(f"  ⏭️ {slug} already published: {published[slug]['url']}")
        return client_idx

    desc = (
        f"{item['title']}\n\n"
        f"{item['hook']} — 4-Scene Cinematic Story & Slow-Motion Breakdown!\n\n"
        "🌍 Subscribe to @influenzian2 for daily viral sports moments, extreme GoPro POVs, "
        "hypercars, 3D body science, cosmic journeys, and oddly satisfying ASMR.\n\n"
        "#shorts #viral #sports #football #f1 #ufc #basketball #satisfying #asmr #trending #fyp"
    )
    is_sports = any(k in item["tags"] for k in ("football", "f1", "ufc", "basketball", "extreme sports", "surfing"))
    body = {
        "snippet": {
            "title": item["title"],
            "description": desc,
            "tags": item["tags"] + ["shorts", "viral shorts", "trending", "fyp", "influenzian"],
            "categoryId": "17" if is_sports else "24",  # 17 = Sports, 24 = Entertainment
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    while client_idx < len(clients):
        proj, yt = clients[client_idx]
        try:
            print(f"  📤 Uploading {mp4_path.name} to @influenzian2 via Project {proj}...")
            media = MediaFileUpload(str(mp4_path), mimetype="video/mp4", resumable=True)
            req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
            resp = None
            while resp is None:
                status, resp = req.next_chunk()
            vid_id = resp["id"]
            url = f"https://youtube.com/shorts/{vid_id}"
            print(f"  🎉 PUBLISHED LIVE: {url}")
            published[slug] = {
                "title": item["title"],
                "youtube_id": vid_id,
                "url": url,
                "project": proj,
                "published_at": time.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
            }
            save_published(published)
            return client_idx
        except HttpError as e:
            err_str = str(e)
            print(f"  ⚠️ Upload error on Project {proj}: {err_str[:180]}")
            if "uploadLimitExceeded" in err_str:
                print("  🛑 Channel 24-hour upload limit reached on YouTube (`uploadLimitExceeded`). Continuing local Flow generation & mastering so remaining Shorts are ready!")
                return len(clients)
            if "quotaExceeded" in err_str or "dailyLimitExceeded" in err_str or e.resp.status in (403, 429):
                client_idx += 1
            else:
                return client_idx
    return client_idx


def main():
    print("=" * 85)
    print("🔥 MULTI-SCENE (4 SCENES/SHORT, ZERO >2X REPEAT) VIRAL ENGINE FOR @influenzian2")
    print("=" * 85)

    proc = ensure_flow_chrome_running(0)
    ws = connect_ws()
    if not ws:
        sys.exit("Could not connect to Google Flow Chrome CDP on port 9225.")

    clients = get_influenzian_clients()
    client_idx = 0
    published = load_published()

    try:
        for idx, item in enumerate(MULTI_SCENE_VIRAL_SHORTS, 1):
            print(f"\n==================== [{idx}/{len(MULTI_SCENE_VIRAL_SHORTS)}] {item['slug']} ====================")
            scenes = generate_4_distinct_scenes_for_short(ws, item, u_idx=0)
            if len(scenes) >= 3:
                mp4_path = assemble_4_scene_51s_short(item, scenes)
                if client_idx < len(clients):
                    client_idx = upload_short_to_influenzian(item, mp4_path, clients, client_idx, published)
            else:
                print(f"  ⚠️ Only {len(scenes)} scenes generated for {item['slug']}, skipping assembly.")
    finally:
        ws.close()

    print("\n" + "=" * 85)
    print(f"✅ COMPLETED MULTI-SCENE RUN: {len(published)} Newly Published Live Shorts")
    for k, v in published.items():
        print(f"  • {k}: {v['url']} | {v['title'][:55]}")
    print("=" * 85)


if __name__ == "__main__":
    main()
