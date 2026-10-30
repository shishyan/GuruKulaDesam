#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/flow_autonomous_generator.py
Google Flow Multi-Account (`shishyan@gmail.com` PRO, `nagaraj957@gmail.com` ULTRA,
`gurukuladesam@gmail.com`, `sashanaga@gmail.com` PRO on `https://flow.google.com/`)
Autonomous Song-Specific Native 9:16 & 16:9 Video Generator for Shorts & Master Films.

Capabilities:
1. Auto-syncs Chrome `Default` multi-account session (`u/3` PRO 755+ credits, `u/0` ULTRA,
   `u/2`, `u/1` PRO) into `~/.config/google-chrome-flow-multi` on CDP port `9225`.
2. Automatically configures Flow Agent settings (`Confirm before generating = Never`,
   native `9:16` vertical video output, `Veo 3.1 - Lite`) and submits song-specific
   parallel scene batches anchored strictly to each hymn's Tamil verses & meaning.
3. Downloads generated native `9:16` MP4s via `Browser.setDownloadBehavior` into
   `production/google_flow_renders/<track_id>/flow_short_01..04.mp4` + `flow_verified.json`.
"""

import os
import re
import sys
import time
import json
import shutil
import zipfile
import argparse
import subprocess
import urllib.request
from pathlib import Path

import websocket

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "production"))

from google_flow_engine import (
    FLOW_RENDERS_DIR,
    PROMPTS_DIR,
    RENDERS_DIR,
    build_master_film,
    ensure_audio,
    parse_blueprint,
)

METADATA_DB = ROOT / "production" / "metadata" / "all_songs_lyrics_and_meanings.json"
CDP_PORT = 9225
CHROME_BIN = "/opt/google/chrome/chrome" if Path("/opt/google/chrome/chrome").exists() else (shutil.which("google-chrome") or "google-chrome")
FLOW_CDP_PROFILE_DIR = Path.home() / ".config" / "google-chrome-flow-multi"

# Multi-account priority order in Chrome Default profile:
# u/3 = shishyan@gmail.com (PRO, 755+ credits)
# u/0 = nagaraj957@gmail.com (ULTRA, 52+ credits)
# u/2 = gurukuladesam@gmail.com (50 daily credits)
# u/1 = sashanaga@gmail.com (PRO, 50 daily credits)
FLOW_USER_INDICES = [3, 0, 2, 1]

CURATED_LEGACY_PROMPTS = {
    "01g0sJdaL2I": [
        "Stern tyrannical ancient Tamil king on an ornate dark stone throne gesturing harshly as distressed villagers plead in a dim torchlit Chola palace hall, illustrating cruel unjust rule (Thirukkural Kodungonmai, Kural 551).",
        "Armed ancient royal guard holding an iron spear demanding tribute from a humble Tamil farmer beside parched fields under dramatic overcast skies (Velodu Nindran Iduvendrathu Polum, Kural 552).",
        "Sorrowful Tamil mother and elderly villager looking at dry leafless trees and cracked earth symbolizing the tears of oppressed citizens eroding royal wealth (Allarpattu Aatradhu Azhudha Kanneer, Kural 555).",
        "Wise elder Tamil minister in white veshti holding a palm-leaf Aram scroll counseling righteous justice beside a glowing brass kuthuvilakku oil lamp in a stone Chola mandapam.",
    ],
    "-cmB2_XZqs0": [
        "Elderly Tamil saint Vallalar draped completely from head to toe in a single seamless pure white cotton shawl covering his head, shoulders, and chest, sacred horizontal white ash on forehead, bowing with folded hands before a golden temple oil lamp.",
        "Sacred close-up of the radiant eternal golden Arutperunjothi oil lamp glowing behind translucent curtains at Vadalur Sathya Gnana Sabai as gentle incense smoke rises.",
        "Compassionate Tamil devotees wearing modest pure white cotton shirts and white veshtis gently serving warm steamed rice on green banana leaves to humble elderly villagers at twilight.",
        "Peaceful golden dawn sunlight streaming into a quiet whitewashed Tamil meditation hall as devotees in modest white cotton attire pray with folded hands before a glowing brass kuthuvilakku oil lamp.",
    ],
    "--4jzoezBW8": [
        "Resolute ancient Chola master stone sculptor chiseling a massive granite temple pillar with unwavering mental focus amidst stone dust in warm golden morning light (Thirukkural Vinaithitpam, Kural 661).",
        "Determined ancient Tamil engineer examining palm-leaf plans beside a mighty granite stone dam holding back rushing monsoon river waters (Oororaal Utrapin Olkaamai, Kural 662).",
        "Strong wooden temple chariot wheel and forged iron axle steadily carrying massive granite blocks along an ancient palm-lined Tamil road at sunrise (Achchaani, Kural 667).",
        "Completed towering Chola granite temple gopuram gleaming in triumphant golden sunrise light as the resolute master builder stands calmly with folded hands.",
    ],
    "02C8glMmetw": [
        "Revered Tamil sage Thiruvalluvar in white cotton robe with rudraksha beads inscribing Agara Muthala on a palm-leaf manuscript with an iron stylus beside a glowing brass kuthuvilakku lamp at dawn.",
        "Golden sunrise rays breaking through morning mist over a grand ancient Chola granite temple gopuram reflected in a blooming pink lotus pond.",
        "Devout Tamil scholar bowing in humble reverence inside a lamp-lit Chola stone sanctum adorned with fresh lotus blossoms (Katrathanal Aaya Payan, Kural 2).",
        "Serene Tamil elders and young students seated beneath a sacred temple banyan tree listening to palm-leaf recitation in warm golden morning light.",
    ],
    "2tL-bKjkL18": [
        "Sanctum close-up of black-granite Chola Goddess Abhirami Amman with sacred horizontal vibhuti stripes and red kumkum tilak on forehead, lotus garland, warm brass kuthuvilakku oil lamps in Thirukkadaiyur shrine.",
        "Young Tamil girl and elder grandmother studying ancient palm-leaf Tamil manuscripts beside a glowing brass oil lamp in a Chola stone courtyard, symbolizing divine wisdom (Kalvi Tharum).",
        "Temple priest with vibhuti stripes performing sacred golden camphor deeparadhana aarti before Goddess Abhirami sanctum as Tamil devotees bow with folded hands.",
        "Radiant golden lotus blossoms and brass kuthuvilakku lamps illuminating Goddess Abhirami Amman in magenta Kanchipuram silk saree inside an ancient Chola sanctum.",
    ],
    "-L3VXkM2MTY": [
        "Saint Arunagirinathar with rudraksha malas and horizontal white vibhuti stripes meditating in ecstatic devotion as a beam of golden divine light illuminates a carved granite Chola mandapam.",
        "Black-granite Chola sanctum idol of youthful South Indian deity Kartikeya Murugan wearing jasmine and red rose garlands with an emerald peacock beside brass kuthuvilakku oil lamps, strictly no trident.",
        "Youthful divine Guru Lord Murugan radiating a warm golden aura inside a serene Chola hill-temple sanctum blessing a bowing Tamil devotee beside an emerald peacock.",
        "Sacred close-up of a single-pointed leaf-shaped golden spearhead (single teardrop blade, strictly NOT a three-pronged trident) anointed with sandalwood, horizontal white ash stripes, red kumkum, and pink lotus blossoms beside a camphor flame.",
    ],
    "B6yVe6HM8Ok": [
        "Barefoot Tamil devotees carrying floral kavadi and brass milk pots ascending the misty ancient stone steps of Palani hill temple at golden sunrise.",
        "Devout Tamil Saiva bhaktar with closed eyes reverently applying three horizontal stripes of sacred white Vibhuthi ash on his forehead in warm morning temple oil-lamp light.",
        "Youthful South Indian deity Lord Murugan wearing a golden crown and fragrant jasmine garlands beside an emerald peacock in a lamp-lit Chola granite sanctum as a priest waves golden camphor aarti, strictly no trident.",
        "Sacred close-up of a single-pointed teardrop leaf-shaped golden spearhead (single blade only, NOT a trident) adorned with jasmine flowers, sandalwood paste, and glowing brass kuthuvilakku oil lamps.",
    ],
    "3oJ2OPG-WCs": [
        "Saint Arunagirinathar singing Thiruppugazh with small brass hand-cymbals and rudraksha beads in a pillared Chola temple hall lit by hundreds of brass lamps.",
        "Magnificent emerald-blue peacock standing gracefully before a towering Chola granite gopuram bathed in golden dawn mist and flickering temple oil lamps.",
        "Sacred Swamimalai scene of young Guru Murugan seated on a carved stone pedestal gently imparting the Pranava Mantra to attentive Lord Shiva with crescent moon and matted locks.",
        "Compassionate smiling youthful South Indian deity Lord Murugan adorned with fragrant white jasmine garlands and golden ornaments inside a warm oil-lamp-lit Chola stone sanctum, strictly no trident.",
    ],
    "Lki_Y8OSljs": [
        "Saiva temple priest performing sacred milk and honey abhishekam over a consecrated black-stone elephant-headed Ganesha idol with curved elephant trunk as brass oil lamps shimmer.",
        "Ancient Chola black-granite elephant-headed Ganesha murti with curved trunk adorned with fresh jasmine garlands and glowing multi-tiered brass kuthuvilakku oil lamps.",
        "Sacred close-up of benevolent elephant-headed Lord Ganesha stone idol with a clearly visible curved elephant trunk, large elephant ears, horizontal white vibhuti stripes, red kumkum, and green arugampul grass garland.",
        "Tamil devotees lighting golden camphor before an ancient banyan-tree elephant-headed stone Ganesha shrine at dawn, symbolizing removal of all obstacles.",
    ],
    "-unILRjNLHQ": [
        "Elderly Tamil saint Vallalar draped completely from head to shoulder in pure seamless white cotton cloth praying with folded hands inside a lamp-lit Chola granite temple hall.",
        "White-clad Tamil saint praying with folded hands in a radiant golden beam of divine temple light inside an ancient carved Chola stone mandapam.",
        "Rows of brass kuthuvilakku oil lamps glowing warmly along a carved granite corridor of an ancient Tamil Murugan temple at dusk.",
        "Youthful South Indian deity Lord Subramaniyar Murugan adorned with white jasmine garlands beside an emerald peacock bathed in warm golden temple oil-lamp light, strictly no trident.",
    ],
    "AW4cljBWy2w": [
        "Traditional green banana leaf offering of fresh milk in a brass tumbler, clear golden honey, palm jaggery, and lentils placed lovingly before Chola stone Lord Vinayagar (Paalum Thelithenum Paagum Paruppum).",
        "Elderly Tamil poetess Avvaiyar in white cotton saree with rudraksha beads and vibhuti stripes offering palm-leaf Sangam Tamil verses before elephant-faced Karpaga Vinayagar (Sangath Tamil Moondrum Thaa).",
        "Close-up of benevolent Chola black-granite Lord Vinayagar adorned with red hibiscus flowers, jasmine garland, horizontal vibhuti stripes, and glowing brass lamps.",
        "Temple priest performing golden camphor harathi before Lord Vinayagar while young Tamil students hold palm-leaf manuscripts seeking blessings for Tamil wisdom.",
    ],
}


def sync_flow_chrome_profile(force: bool = False):
    """Syncs Chrome Default multi-account session into isolated CDP profile dir."""
    src_root = Path.home() / ".config" / "google-chrome"
    if not src_root.exists():
        return
    if not force and (FLOW_CDP_PROFILE_DIR / "Default" / "Cookies").exists():
        return
    (FLOW_CDP_PROFILE_DIR / "Default").mkdir(parents=True, exist_ok=True)
    local_state = src_root / "Local State"
    if local_state.exists():
        shutil.copy2(local_state, FLOW_CDP_PROFILE_DIR / "Local State")

    src_prof = src_root / "Default"
    if not src_prof.exists():
        src_prof = src_root / "Profile 3"
    for item in ("Cookies", "Preferences", "Secure Preferences", "Login Data", "Web Data", "Network"):
        s = src_prof / item
        d = FLOW_CDP_PROFILE_DIR / "Default" / item
        if s.exists():
            try:
                if s.is_dir():
                    shutil.rmtree(d, ignore_errors=True)
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
            except Exception:
                pass


def ensure_flow_chrome_running(user_idx: int = 3) -> subprocess.Popen | None:
    """Ensures CDP port 9225 is active with a completely hidden Google Flow tab."""
    try:
        tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/list", timeout=2).read())
        if any("flow.google" in t.get("url", "") or "labs.google" in t.get("url", "") for t in tabs):
            return None
    except Exception:
        pass

    print(f"[Flow] Launching hidden headless Google Flow session (u/{user_idx}) on CDP port {CDP_PORT}...")
    sync_flow_chrome_profile(force=False)
    env = os.environ.copy()
    ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36"
    proc = subprocess.Popen(
        [
            CHROME_BIN,
            "--headless=new",
            f"--user-agent={ua}",
            "--disable-blink-features=AutomationControlled",
            "--hide-scrollbars",
            "--mute-audio",
            "--disable-notifications",
            f"--user-data-dir={FLOW_CDP_PROFILE_DIR}",
            f"--remote-debugging-port={CDP_PORT}",
            "--window-size=1920,1080",
            "--no-first-run",
            "--no-default-browser-check",
            f"https://flow.google.com/u/{user_idx}/",
        ],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    for _ in range(18):
        time.sleep(1)
        try:
            tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/list", timeout=2).read())
            if any("flow.google" in t.get("url", "") for t in tabs):
                time.sleep(3)
                return proc
        except Exception:
            pass
    return proc


def get_flow_tab():
    try:
        tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/list", timeout=3).read())
    except Exception as e:
        print(f"[CDP Error] Could not connect to Chrome on port {CDP_PORT}: {e}")
        return None
    flow_tabs = [t for t in tabs if ("flow.google" in t.get("url", "") or "labs.google" in t.get("url", "")) and t.get("type") == "page"]
    return flow_tabs[0] if flow_tabs else None


def connect_ws():
    tab = get_flow_tab()
    if not tab:
        return None
    ws = websocket.create_connection(tab["webSocketDebuggerUrl"], suppress_origin=True)
    dl_path = str(Path.home() / "Downloads")
    ws.send(json.dumps({
        "id": 1,
        "method": "Browser.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": dl_path, "eventsEnabled": True},
    }))
    ws.recv()
    return ws


def eval_js(ws, js_code: str, req_id: int = 2):
    ws.send(json.dumps({
        "id": req_id,
        "method": "Runtime.evaluate",
        "params": {"expression": js_code, "returnByValue": True},
    }))
    while True:
        msg = json.loads(ws.recv())
        if msg.get("id") == req_id:
            return msg.get("result", {}).get("result", {}).get("value")


def select_active_flow_account_and_open_project(ws, needed_credits: int = 40) -> tuple[int, int]:
    """Finds a signed-in Google Flow account with >= `needed_credits` and opens a fresh project workspace."""
    for u_idx in FLOW_USER_INDICES:
        ws.send(json.dumps({"id": 10 + u_idx, "method": "Page.navigate", "params": {"url": f"https://flow.google.com/u/{u_idx}/"}}))
        while True:
            if json.loads(ws.recv()).get("id") == 10 + u_idx:
                break
        time.sleep(4.5)
        for ob_step in range(8):
            clicked_ob = eval_js(ws, """
            (() => {
                document.querySelectorAll('[role="dialog"] *, .mat-mdc-dialog-content, div').forEach(el => {
                    if (el.scrollHeight > el.clientHeight + 20) el.scrollTop = el.scrollHeight;
                });
                const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
                const b = btns.find(x => !x.disabled && ['Next', 'Agree', 'Accept', 'Continue', 'Got it', 'I agree'].includes((x.innerText || '').trim()));
                if (b) { b.click(); return (b.innerText || '').trim(); }
                return null;
            })()
            """, req_id=15 + ob_step)
            if not clicked_ob:
                break
            time.sleep(1.0)
        eval_js(ws, """
        (() => {
            const acc = document.querySelector('[aria-label="Account details"], [aria-label*="Google Account"]');
            if (acc) acc.click();
        })()
        """, req_id=20 + u_idx)
        time.sleep(1.5)
        body_txt = eval_js(ws, "document.body.innerText", req_id=30 + u_idx) or ""
        m = re.search(r"(\d+)\s+Google Flow credits", body_txt)
        credits = int(m.group(1)) if m else 0
        print(f"  [Flow Account u/{u_idx}] Available credits: {credits}")
        if credits >= needed_credits:
            # Close account popup cleanly via Escape + body click
            ws.send(json.dumps({"id": 35 + u_idx, "method": "Input.dispatchKeyEvent", "params": {"type": "keyDown", "key": "Escape", "code": "Escape", "windowsVirtualKeyCode": 27}}))
            while json.loads(ws.recv()).get("id") != 35 + u_idx:
                pass
            ws.send(json.dumps({"id": 36 + u_idx, "method": "Input.dispatchKeyEvent", "params": {"type": "keyUp", "key": "Escape", "code": "Escape", "windowsVirtualKeyCode": 27}}))
            while json.loads(ws.recv()).get("id") != 36 + u_idx:
                pass
            eval_js(ws, "document.body.click()", req_id=40 + u_idx)
            time.sleep(0.8)
            clicked = eval_js(ws, """
            (() => {
                const btns = Array.from(document.querySelectorAll('button, a, [role="button"]'));
                const nb = btns.find(b => (b.innerText || '').includes('New project')) ||
                           btns.find(b => (b.innerText || '').includes('Start Creating'));
                if (nb) { nb.click(); return nb.innerText.trim(); }
                return null;
            })()
            """, req_id=50 + u_idx)
            print(f"  [Flow Account u/{u_idx}] Opened new project workspace ({clicked})")
            # Poll until project canvas + ProseMirror editor + tune button are mounted
            for _ in range(20):
                time.sleep(1.0)
                ready = eval_js(ws, """
                Boolean(location.href.includes('/project/') &&
                        document.querySelector('div.ProseMirror') &&
                        Array.from(document.querySelectorAll('button')).some(b => (b.innerText || '').trim() === 'tune'))
                """, req_id=55 + u_idx)
                if ready:
                    break
            time.sleep(1.0)
            for ob_step in range(6):
                clicked_ob = eval_js(ws, """
                (() => {
                    document.querySelectorAll('[role="dialog"] *, .mat-mdc-dialog-content, div').forEach(el => {
                        if (el.scrollHeight > el.clientHeight + 20) el.scrollTop = el.scrollHeight;
                    });
                    const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
                    const b = btns.find(x => !x.disabled && ['Next', 'Agree', 'Accept', 'Continue', 'Got it', 'I agree'].includes((x.innerText || '').trim()));
                    if (b) { b.click(); return (b.innerText || '').trim(); }
                    return null;
                })()
                """, req_id=56 + ob_step)
                if not clicked_ob:
                    break
                time.sleep(0.8)
            configure_agent_settings(ws, portrait_9_16=True)
            return u_idx, credits
    raise RuntimeError(f"No signed-in Google Flow account has >= {needed_credits} credits right now.")


def configure_agent_settings(ws, portrait_9_16: bool = True):
    """Sets Confirm before generating = Never, Video = 9:16 (or 16:9), x1, Veo 3.1 - Lite."""
    eval_js(ws, """
    (() => {
        const tune = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').trim() === 'tune');
        if (tune) tune.click();
    })()
    """, req_id=60)
    time.sleep(1.0)
    # Open Video model dropdown and select Veo 3.1 - Lite
    eval_js(ws, """
    (() => {
        const dd = Array.from(document.querySelectorAll('button, [role="combobox"]')).find(b => ['Omni', 'Veo'].some(w => (b.innerText || '').includes(w)));
        if (dd) dd.click();
    })()
    """, req_id=61)
    time.sleep(0.7)
    eval_js(ws, """
    (() => {
        const opt = Array.from(document.querySelectorAll('[role="option"], [role="menuitem"], mat-option, button'))
            .find(e => (e.innerText || '').trim() === 'Veo 3.1 - Lite');
        if (opt) opt.click();
    })()
    """, req_id=62)
    time.sleep(0.6)
    ratio_str = "9:16" if portrait_9_16 else "16:9"
    eval_js(ws, f"""
    (() => {{
        const els = Array.from(document.querySelectorAll('div, label, span, mat-radio-button, [role="radio"], button'));
        const neverEl = els.find(e => (e.innerText || '').trim().startsWith('Never'));
        if (neverEl) neverEl.click();
        const ratioBtns = Array.from(document.querySelectorAll('button[role="radio"], button')).filter(b => (b.innerText || '').includes({json.dumps(ratio_str)}));
        if (ratioBtns.length > 0) ratioBtns[ratioBtns.length - 1].click();
        const saveBtn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').trim() === 'Save');
        if (saveBtn) saveBtn.click();
    }})()
    """, req_id=63)
    time.sleep(1.2)


def get_canvas_card_more_buttons(ws) -> list[dict]:
    return eval_js(ws, """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
        const out = [];
        for (let i = 0; i < btns.length - 1; i++) {
            if (btns[i].getAttribute('aria-label') === 'Reuse prompt' &&
                !(btns[i].innerText || '').includes('keyboard_return') &&
                btns[i+1].getAttribute('aria-label') === 'More options') {
                out.push({moreIdx: i + 1, label: btns[i+2] ? (btns[i+2].getAttribute('aria-label') || '') : ''});
            }
        }
        return out;
    })()
    """, req_id=70) or []


def submit_agent_prompt(ws, prompt_text: str) -> bool:
    for attempt in range(2):
        ok = eval_js(ws, f"""
        (() => {{
            const el = document.querySelector('div.ProseMirror');
            if (!el) return false;
            el.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);
            document.execCommand('insertText', false, {json.dumps(prompt_text)});
            return true;
        }})()
        """, req_id=75)
        if not ok:
            time.sleep(1.0)
            continue
        time.sleep(0.5)
        ws.send(json.dumps({"id": 76, "method": "Input.insertText", "params": {"text": " "}}))
        while json.loads(ws.recv()).get("id") != 76:
            pass
        time.sleep(0.5)
        rect = eval_js(ws, """
        (() => {
            const b = document.querySelector('button[aria-label="Start generation"]');
            if (!b || b.disabled) return null;
            const r = b.getBoundingClientRect();
            return {left: r.left, top: r.top, w: r.width, h: r.height};
        })()
        """, req_id=77)
        if not rect:
            time.sleep(1.0)
            continue
        # Click left side of circular Start generation button (+6px) to avoid right-edge floating badge
        x_click = rect["left"] + (6 if attempt == 0 else rect["w"] / 2)
        for idx_ev, ev in enumerate(("mousePressed", "mouseReleased")):
            ws.send(json.dumps({
                "id": 78 + idx_ev,
                "method": "Input.dispatchMouseEvent",
                "params": {"type": ev, "x": x_click, "y": rect["top"] + rect["h"] / 2, "button": "left", "clickCount": 1},
            }))
            while json.loads(ws.recv()).get("id") != 78 + idx_ev:
                pass
        time.sleep(2.5)
        started = eval_js(ws, """
        (() => {
            const b = document.querySelector('button[aria-label="Start generation"]');
            const txt = (document.querySelector('div.ProseMirror')?.innerText || '').trim();
            return (!b || b.disabled || txt.length < 15);
        })()
        """, req_id=81)
        if started:
            return True
    return False


def build_song_specific_short_prompts(track_id: str, count: int = 4) -> tuple[str, list[str]]:
    """Crafts `count` hyper-specific scene prompts strictly anchored to THIS song's verses & meaning."""
    meta_db = json.loads(METADATA_DB.read_text(encoding="utf-8")) if METADATA_DB.exists() else {}
    entry = meta_db.get(track_id, {})
    title = entry.get("title", track_id)

    if track_id in CURATED_LEGACY_PROMPTS:
        return title, CURATED_LEGACY_PROMPTS[track_id][:count]

    bp_matches = list(PROMPTS_DIR.glob(f"*/{track_id}*.md"))
    if bp_matches:
        bp = parse_blueprint(bp_matches[0])
        if len(bp.get("scenes", [])) >= count:
            excl = bp.get("continuity", {}).get("Hard Exclusions", "No text, no watermarks, no modern clothes.")
            prompts = [
                f"Photorealistic South Indian Chola-era devotional cinema, 9:16 vertical framing, centered subject: {sc['prompt']} Exclusions: {sc.get('exclusions', '')} {excl}"
                for sc in bp["scenes"][:count]
            ]
            return bp["title"], prompts

    en_meaning = re.sub(r"\s+", " ", entry.get("english_meaning", "")).strip()
    ta_meaning = re.sub(r"\s+", " ", entry.get("tamil_meaning", "")).strip()
    ta_lyrics = [l.strip() for l in entry.get("tamil_lyrics", "").splitlines() if l.strip()]

    story_context = en_meaning[:320] if en_meaning else (ta_meaning[:260] if ta_meaning else title)
    camera_beats = [
        "Opening sacred close-up establishing the exact divine subject and emotional essence",
        "Medium cinematic devotional tableau illustrating the core verse action in warm temple lamp-light",
        "Intimate expressive shot of sincere Tamil devotion and sacred ritual offering matching the hymn",
        "Radiant golden-hour culmination shot of divine grace and inner peace in an ancient Chola sanctum",
    ]
    prompts = []
    for idx in range(count):
        lyric_ref = ta_lyrics[idx % len(ta_lyrics)] if ta_lyrics else title
        prompts.append(
            f"Photorealistic South Indian Chola-era sacred cinema for the Tamil hymn '{title}' "
            f"(verse theme: '{lyric_ref}'; meaning: {story_context}). "
            f"{camera_beats[idx % len(camera_beats)]}. "
            f"Warm brass kuthuvilakku oil-lamp glow, authentic Tamil cultural attire, zero onscreen text, zero watermarks."
        )
    return title, prompts


def generate_flow_clips_for_short(track_id: str, scene_count: int = 4, force_regenerate: bool = False) -> list[Path]:
    """
    Generates `scene_count` dedicated native 9:16 song-specific clips via Google Flow
    and saves `flow_short_01..0N.mp4` + `flow_verified.json` in `production/google_flow_renders/<track_id>/`.
    """
    track_dir = FLOW_RENDERS_DIR / track_id
    track_dir.mkdir(parents=True, exist_ok=True)

    existing = [p for p in sorted(track_dir.glob("flow_short_*.mp4")) if p.stat().st_size > 300_000]
    if len(existing) >= min(3, scene_count) and not force_regenerate:
        print(f"  [Flow Cached] {track_id} already has {len(existing)} verified native 9:16 Flow clips.")
        return existing

    title, prompts = build_song_specific_short_prompts(track_id, count=scene_count)
    print("\n" + "=" * 85)
    print(f"✨ GOOGLE FLOW NATIVE 9:16 GENERATOR: {title} ({track_id}) — {len(prompts)} Scenes")
    print("=" * 85)

    proc = ensure_flow_chrome_running(user_idx=FLOW_USER_INDICES[0])
    ws = connect_ws()
    if not ws:
        if proc:
            proc.terminate()
        raise RuntimeError("Could not connect to Google Flow Chrome CDP session on port 9225.")

    dl_dir = Path.home() / "Downloads"
    saved_paths: list[Path] = []
    try:
        u_idx, credits = select_active_flow_account_and_open_project(ws, needed_credits=len(prompts) * 10)
        numbered = " ".join(f"{i+1}) {p}" for i, p in enumerate(prompts))
        batch_prompt = (
            f"Generate {len(prompts)} separate vertical 9:16 photorealistic South Indian Chola-era sacred video clips "
            f"(strictly zero onscreen text, zero subtitles, zero modern objects): {numbered}"
        )

        if not submit_agent_prompt(ws, batch_prompt):
            raise RuntimeError(f"Failed submitting Flow batch prompt for {track_id}")
        print(f"  🚀 Submitted {len(prompts)}-scene parallel batch to Google Flow (u/{u_idx})...")

        # Poll canvas until all `len(prompts)` video cards finish rendering (up to 420s during peak demand)
        t0 = time.time()
        cards = []
        while time.time() - t0 < 420:
            time.sleep(6)
            elapsed = int(time.time() - t0)
            # Click Approve automatically just in case confirmation ever appears
            eval_js(ws, """
            (() => {
                const btns = Array.from(document.querySelectorAll('button, [role="button"], .option-row'));
                const ap = btns.find(b => (b.innerText || '').includes('Always approve')) ||
                           btns.find(b => (b.innerText || '').trim().endsWith('Approve'));
                if (ap) ap.click();
            })()
            """, req_id=85)
            cards = get_canvas_card_more_buttons(ws)
            print(f"    [{elapsed:3d}s] Completed Flow video cards on canvas: {len(cards)}/{len(prompts)}", flush=True)
            if len(cards) >= len(prompts):
                time.sleep(2.5)
                cards = get_canvas_card_more_buttons(ws)
                break

        if len(cards) < 3:
            raise RuntimeError(f"Only {len(cards)} Flow clips completed for {track_id} within timeout.")

        # Download each completed card MP4 (re-query live DOM button indices before each card click)
        for idx_zero in range(min(len(cards), len(prompts))):
            idx = idx_zero + 1
            live_cards = get_canvas_card_more_buttons(ws)
            if idx_zero >= len(live_cards):
                break
            cinfo = live_cards[idx_zero]
            dest = track_dir / f"flow_short_{idx:02d}.mp4"
            before_mp4s = set(dl_dir.glob("*.mp4"))
            eval_js(ws, f"""
            (() => {{
                const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
                if (btns[{cinfo['moreIdx']}]) {{
                    btns[{cinfo['moreIdx']}].scrollIntoView();
                    btns[{cinfo['moreIdx']}].click();
                }}
            }})()
            """, req_id=100 + idx)
            time.sleep(0.9)
            eval_js(ws, """
            (() => {
                const dl = Array.from(document.querySelectorAll('[role="menuitem"]')).find(i => (i.innerText || '').toLowerCase().includes('download'));
                if (dl) dl.click();
            })()
            """, req_id=120 + idx)
            time.sleep(0.9)
            eval_js(ws, """
            (() => {
                const orig = Array.from(document.querySelectorAll('[role="menuitem"]'))
                    .find(i => (i.innerText || '').includes('720p') || (i.innerText || '').toLowerCase().includes('original'));
                if (orig) orig.click();
            })()
            """, req_id=140 + idx)

            for _ in range(25):
                time.sleep(1.0)
                crs = list(dl_dir.glob("*.crdownload"))
                diff = [f for f in (set(dl_dir.glob("*.mp4")) - before_mp4s) if f.stat().st_size > 300_000]
                if diff and not crs:
                    newest = sorted(diff, key=lambda p: p.stat().st_mtime, reverse=True)[0]
                    shutil.copy2(newest, dest)
                    saved_paths.append(dest)
                    print(f"  ✅ Saved {dest.name} ({dest.stat().st_size / 1e6:.2f} MB) <- {cinfo.get('label', '')}")
                    break
            eval_js(ws, "document.body.click()", req_id=160 + idx)
            time.sleep(0.5)

    finally:
        ws.close()

    if len(saved_paths) >= 3:
        (track_dir / "flow_verified.json").write_text(
            json.dumps({
                "track_id": track_id,
                "title": title,
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
                "aspect_ratio": "9:16",
                "clips": [p.name for p in saved_paths],
            }, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return saved_paths


def generate_track_scenes(track_id: str, target_scene_count: int = 4) -> bool:
    clips = generate_flow_clips_for_short(track_id, scene_count=target_scene_count)
    return len(clips) >= 3


def main():
    parser = argparse.ArgumentParser(description="Google Flow Autonomous Song-Specific Video Generator")
    parser.add_argument("--track", type=str, required=True, help="Track ID to generate song-specific Flow visuals for")
    parser.add_argument("--scenes", type=int, default=4, help="Number of song-specific scenes (default: 4)")
    parser.add_argument("--for-short", action="store_true", help="Generate song-specific clips and build 9:16 Short")
    parser.add_argument("--force", action="store_true", help="Force regenerate Flow clips even if cached")
    parser.add_argument("--push", action="store_true", help="Upload built Short directly to YouTube")
    parser.add_argument("--channel", type=str, default="@GuruKulaDesam2", help="Target channel (@GuruKulaDesam or @GuruKulaDesam2)")
    args = parser.parse_args()

    if args.for_short:
        clips = generate_flow_clips_for_short(args.track, scene_count=args.scenes, force_regenerate=args.force)
        if len(clips) < 3:
            sys.exit(f"❌ Flow generated only {len(clips)} clips for {args.track}; aborting Short build.")
        from tools.shorts_viral_builder import build_short_for_track
        meta = build_short_for_track(args.track, force_rebuild=True, brand_handle=args.channel, use_flow=True)
        if args.push:
            from tools.shorts_autonomous_daemon import upload_short_via_api
            upload_short_via_api(meta, publish_at_dt=None, channel_key=args.channel.lower())
    else:
        generate_track_scenes(args.track, target_scene_count=args.scenes)


if __name__ == "__main__":
    main()
