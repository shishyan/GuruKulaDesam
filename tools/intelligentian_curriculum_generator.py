#!/usr/bin/env python3
"""
Autonomous Daily Interactive Curriculum Generator for @intelligentian (`UCjVbL7GE3cHLOWRYAxZH65A`)

Used by Slot 2 (`07:00 PM IST` / `13:30 UTC`) in `.github/workflows/intelligentian-daily-auto.yml`:
  1. Checks if `gdrive:Intelligentian/CurriculumQueue` already has a pre-rendered unpublished Learning MP4.
     If one exists, exits cleanly (`needsBuild=false`) so `intelligentian_publisher.py --mode daily-curriculum`
     publishes that pre-rendered episode first.
  2. Otherwise, selects the next unpublished lesson from `production/intelligentian_curriculum_roadmap.json`
     (`L1_BASICS -> L2_APPLIED -> L3_SYSTEMS -> L4_FRONTIER` across `OPENAI`, `ANTHROPIC`, `GOOGLE`, `NVIDIA`,
     `MICROSOFT`, `META`, `XAI`) — and once all 25 roadmap lessons complete, seamlessly continues into endless
     evergreen progressive cycles!
  3. Uses **`gemini-4-hydrogen`** (`POST https://generativelanguage.googleapis.com/v1beta/interactions`, JSON schema,
     `store: false`) to author a **7-Beat Interactive NotebookLM Male/Female Co-Host Show (`Maya` & `Alex`)
     + 2 Simulated Live Viewer Call-In Questions (`AUDIENCE_Q`)** tailored to the lesson's exact complexity tier
     (`L1` beginner intuition -> `L4` deep frontier math/silicon), with a deterministic 7-beat fallback.
  4. Writes `/tmp/intelligentian_daily_curriculum/<EP_ID>/manifest.json` + `latest_episode.json` ready for
     `intelligentian_daily_news_cloud_builder.py` (`gemini-3.8-flash-tts` Multi-Speaker + 1080p render).
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from intelligentian_live_news_harvester import (
    AUDIENCE_VOICES,
    COMPANIES,
    COMPANY_META,
    EXPECTED_CHANNEL_ID,
    CHANNEL_HANDLE,
    GEMINI_INTERACTIONS_URL,
    GEMINI_SCRIPT_MODEL,
    INTERACTIVE_PODCAST_JSON_SCHEMA,
    assert_zero_cta,
    clean_cta_from_external_text,
    discover_visual_plates,
    resolve_gemini_api_key,
    strip_inline_tts_tags,
)

LEVEL_LABELS = {
    "L1_BASICS": ("L1", "Level 1 · Intuitive Foundations (Zero Math)"),
    "L2_APPLIED": ("L2", "Level 2 · Applied AI Engineering & Agent Workflows"),
    "L3_SYSTEMS": ("L3", "Level 3 · Production Systems, RAG & Distributed Serving"),
    "L4_FRONTIER": ("L4", "Level 4 · Frontier Transformer Math, Kernels & Silicon"),
}


def has_unpublished_drive_curriculum_mp4(drive_remote: str, published_ids: set[str]) -> str | None:
    if not drive_remote:
        return None
    try:
        res = subprocess.run(
            ["rclone", "lsf", "--dirs-only", drive_remote],
            capture_output=True,
            text=True,
            timeout=25,
            check=False,
        )
        if res.returncode != 0:
            return None
        dirs = [d.strip().rstrip("/") for d in res.stdout.splitlines() if d.strip()]
        for d in sorted(dirs):
            if d in published_ids:
                continue
            f_res = subprocess.run(
                ["rclone", "lsf", f"{drive_remote.rstrip('/')}/{d}"],
                capture_output=True,
                text=True,
                timeout=20,
                check=False,
            )
            files = [x.strip() for x in f_res.stdout.splitlines() if x.strip()]
            has_mf = "manifest.json" in files
            has_mp4 = any(x.lower().endswith(".mp4") for x in files)
            if has_mf and has_mp4:
                return d
    except Exception:
        return None
    return None


def select_next_curriculum_item(roadmap: dict, published_ids: set[str], force_company: str = "") -> dict:
    queue = list(roadmap.get("futureQueueEP11toEP35", []))
    for item in queue:
        ep_id = str(item.get("episodeId", "")).strip()
        comp = str(item.get("companyCategory", "OPENAI")).upper()
        if not ep_id or ep_id in published_ids:
            continue
        if force_company and comp != force_company:
            continue
        return item

    # Endless evergreen cycle once EP11..EP35 are all published
    cycle_num = len(published_ids) + 1
    base = queue[cycle_num % len(queue)] if queue else {
        "companyCategory": force_company or "OPENAI",
        "complexityLevel": "L2_APPLIED",
        "audienceBadge": "BUILDERS & OPERATORS",
        "title": "Frontier AI Systems Architecture: Context, Verification & Latency Mastery",
        "hookPayoff7Sec": "Reliable AI products win not by bigger prompts, but by pairing clean context windows with deterministic verification loops.",
        "coreMentalModels": [
            "Context Window Signal-to-Noise Discipline",
            "Structured Tool Verification & Schema Guardrails",
            "Tiered Latency-Cost Model Routing",
        ],
        "thumbnailText": "AI ARCHITECTURE",
    }
    today_tag = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d")
    comp = force_company or str(base.get("companyCategory", "OPENAI")).upper()
    lvl_full = str(base.get("complexityLevel", "L2_APPLIED")).upper()
    lvl_short = LEVEL_LABELS.get(lvl_full, ("L2", ""))[0]
    ep_id = f"LEARN_{today_tag}_{lvl_short}_{comp}_CYCLE{cycle_num}"
    cloned = dict(base)
    cloned["episodeId"] = ep_id
    cloned["companyCategory"] = comp
    return cloned


def generate_gemini_curriculum_script(api_key: str, item: dict) -> dict | None:
    comp = str(item.get("companyCategory", "OPENAI")).upper()
    meta = COMPANY_META.get(comp, COMPANY_META["OPENAI"])
    comp_name = meta["display"]
    lvl_full = str(item.get("complexityLevel", "L1_BASICS")).upper()
    lvl_short, lvl_desc = LEVEL_LABELS.get(lvl_full, ("L1", "Progressive AI Curriculum"))
    audience_badge = str(item.get("audienceBadge", "ALL LEARNERS"))
    models_blob = "\n".join(f"- {m}" for m in item.get("coreMentalModels", []))

    prompt = f"""You are the executive showrunner for @intelligentian's flagship daily AI Learning Show:
"MAYA & ALEX · INTERACTIVE AI MASTERY STUDIO" (NotebookLM-style dual-host educational deep dive + simulated live learner call-ins).

Author a 7-beat interactive educational episode JSON strictly matching the schema.

LESSON SPECIFICATION:
- Episode ID: {item.get('episodeId')}
- Frontier Ecosystem Focus: {comp_name} ({meta['ecosystemContext']})
- Complexity Tier: {lvl_short} — {lvl_desc} (Target Audience: {audience_badge})
- Lesson Title: {item.get('title')}
- 7-Second Core Payoff: {item.get('hookPayoff7Sec')}
- Core Mental Models to Teach:
{models_blob}

EXACT 7-BEAT INTERACTIVE LESSON STRUCTURE (MANDATORY):
- Beat 1 (`beatIndex: 1`, `speakerRole: "COHOST_DUO"`): 7-Second Hook! Maya (`voice: "Aoede"`, `role: "HOST_F"`, curious/energetic co-host) & Alex (`voice: "Puck"`, `role: "HOST_M"`, crystal-clear AI systems architect) hook the viewer immediately with the core mental shift: {item.get('hookPayoff7Sec')}
- Beat 2 (`beatIndex: 2`, `speakerRole: "COHOST_DUO"`): Mental Model #1 & Visual Stack! Maya asks how it works from first principles; Alex teaches the core mechanism clearly using vivid analogies and a 4-stage `diagramNodeLabels` pipeline.
- Beat 3 (`beatIndex: 3`, `speakerRole: "AUDIENCE_Q"`): First Simulated Live Learner Call-In! A realistic viewer (`audienceCaller` with `name` + `roleTitle` matching {audience_badge}, voice `"Leda"` or `"Callirrhoe"`) asks the #1 confusing question or misconception viewers have in their heads right now (`18-30` words).
- Beat 4 (`beatIndex: 4`, `speakerRole: "COHOST_DUO"`): Direct Answer to Caller #1! Maya and Alex address Caller #1 **by first name**, clearing up the misconception with a crisp real-world {comp_name} example.
- Beat 5 (`beatIndex: 5`, `speakerRole: "AUDIENCE_Q"`): Second Simulated Live Learner Call-In! A DIFFERENT viewer (`name` + `roleTitle`, voice `"Fenrir"` or `"Charon"`) asks a practical "How do I apply this in my own projects or daily workflow?" question (`18-30` words).
- Beat 6 (`beatIndex: 6`, `speakerRole: "COHOST_DUO"`): Direct Answer to Caller #2! Alex and Maya address Caller #2 **by first name** and give a concrete 3-step hands-on blueprint.
- Beat 7 (`beatIndex: 7`, `speakerRole: "COHOST_DUO"`): Synthesis & Mastery Takeaway! Memorable closing mental model recap from Maya & Alex. End cleanly on pure insight.

HARD RULES:
1. STRICT ZERO-CTA POLICY: NEVER use `subscribe`, `hit the bell`, `click the bell`, `smash that like`, `drop a like`, `like and share`, `leave a comment`, `comment below`, or `follow for more` anywhere (say "monthly plan" instead of "subscription").
2. Keep dialogue natural, warm, and brisk (~38–55 words on COHOST_DUO beats across 2-3 turns; ~18–30 words on AUDIENCE_Q beats).
3. `text` inside `dialogueTurns` goes directly to `gemini-3.8-flash-tts`: NEVER include `Maya:` or `Alex:` speaker prefixes inside `text`; subtle `<short pause>` or `<laugh>` tags are welcome.
"""

    payload = {
        "model": GEMINI_SCRIPT_MODEL,
        "input": prompt,
        "store": False,
        "generation_config": {
            "thinking_level": "medium",
            "max_output_tokens": 32768,
        },
        "response_format": {
            "type": "text",
            "mime_type": "application/json",
            "schema": INTERACTIVE_PODCAST_JSON_SCHEMA,
        },
    }
    req = urllib.request.Request(
        GEMINI_INTERACTIONS_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "x-goog-api-key": api_key,
            "Content-Type": "application/json",
            "Api-Revision": "2026-05-20",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=95) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        print(f"[Curriculum Gemini Fallback] {exc}")
        return None

    chunks: list[str] = []
    for step in body.get("steps", []):
        if step.get("type") == "model_output":
            for part in step.get("content", []):
                if part.get("type") == "text" and part.get("text"):
                    chunks.append(part["text"])
    raw_json = "".join(chunks).strip() or str(body.get("output_text") or "").strip()
    if not raw_json:
        return None
    try:
        parsed = json.loads(raw_json)
        if len(parsed.get("beats", [])) == 7:
            return parsed
    except Exception as exc:
        print(f"[Curriculum JSON Fallback] {exc}")
    return None


def build_deterministic_curriculum_script(item: dict) -> dict:
    comp = str(item.get("companyCategory", "OPENAI")).upper()
    meta = COMPANY_META.get(comp, COMPANY_META["OPENAI"])
    comp_name = meta["display"]
    title = clean_cta_from_external_text(str(item.get("title", f"{comp_name} AI Systems Deep Dive")))
    payoff = clean_cta_from_external_text(str(item.get("hookPayoff7Sec", f"Understanding {comp_name} architecture from first principles.")))
    models = [clean_cta_from_external_text(str(m)) for m in item.get("coreMentalModels", [])]
    while len(models) < 3:
        models.append(f"{comp_name} production architecture discipline")
    layers = meta["architectureLayers"]

    return {
        "youtubeTitle": title[:92],
        "executiveSummary": f"{payoff} Interactive {comp_name} AI Mastery episode with Maya & Alex plus two live learner Q&A breakdowns.",
        "beats": [
            {
                "beatIndex": 1,
                "speakerRole": "COHOST_DUO",
                "chapterTitle": "The Core Mental Shift",
                "actTag": "CORE INTUITION",
                "punchMetric": str(item.get("thumbnailText") or comp_name)[:22],
                "diagramNodeLabels": ["Old Assumption", f"{comp_name} Core", "Real Breakthrough"],
                "keyBullets": [payoff[:86], models[0][:86], f"Focus: {comp_name} AI Mastery"],
                "dialogueTurns": [
                    {
                        "speaker": "Maya",
                        "role": "HOST_F",
                        "voice": "Aoede",
                        "style": "bright, curious podcast co-host",
                        "text": f"Welcome back to Intelligentian! Today we are unlocking one of my favorite {comp_name} concepts: {title}. <short pause> Alex, give us the core intuition in one sentence!",
                    },
                    {
                        "speaker": "Alex",
                        "role": "HOST_M",
                        "voice": "Puck",
                        "style": "clear, warm AI systems architect",
                        "text": payoff,
                    },
                ],
            },
            {
                "beatIndex": 2,
                "speakerRole": "COHOST_DUO",
                "chapterTitle": models[0][:48],
                "actTag": "FIRST PRINCIPLES",
                "punchMetric": "UNDER THE HOOD",
                "diagramNodeLabels": [l[:20] for l in layers[:4]],
                "keyBullets": [models[0][:86], models[1][:86], f"Pipeline: {layers[0]} -> {layers[2]}"],
                "dialogueTurns": [
                    {
                        "speaker": "Maya",
                        "role": "HOST_F",
                        "voice": "Aoede",
                        "style": "inquisitive co-host",
                        "text": "Walk us under the hood—what actually happens step by step when a request hits this stack?",
                    },
                    {
                        "speaker": "Alex",
                        "role": "HOST_M",
                        "voice": "Puck",
                        "style": "precise educator",
                        "text": f"Think of it in stages, Maya: {models[0]}. Data moves cleanly from {layers[0]} into {layers[2]}, which is why {models[1].lower()}.",
                    },
                ],
            },
            {
                "beatIndex": 3,
                "speakerRole": "AUDIENCE_Q",
                "chapterTitle": "Live Learner Call-In #1",
                "actTag": "VIEWER QUESTION",
                "punchMetric": "COMMON TRAP",
                "diagramNodeLabels": ["Misconception", "Reality Check", "Clean Mental Model"],
                "keyBullets": [
                    "Caller: Nina · Full-Stack Engineer",
                    f"Clarifying how {models[1][:55]} works in practice",
                    "Avoiding the #1 beginner & builder pitfall",
                ],
                "audienceCaller": {
                    "name": "Nina",
                    "roleTitle": "Full-Stack Engineer",
                    "voice": "Leda",
                    "questionSummary": f"Where do teams usually get tripped up when applying {models[1][:65]}?",
                },
                "dialogueTurns": [
                    {
                        "speaker": "Nina",
                        "role": "AUDIENCE_Q",
                        "voice": "Leda",
                        "style": "curious full-stack engineer calling in",
                        "text": f"Hey Maya and Alex, Nina here! Where do engineers usually get tripped up first when they try applying this in a real {comp_name} workflow?",
                    }
                ],
            },
            {
                "beatIndex": 4,
                "speakerRole": "COHOST_DUO",
                "chapterTitle": "Answering Nina: Avoiding the Trap",
                "actTag": "ARCHITECT ANSWER",
                "punchMetric": "SIGNAL VS NOISE",
                "diagramNodeLabels": ["Noisy Input", "Clean Boundary", "Verified Output"],
                "keyBullets": [models[1][:86], "Measure latency, token cost, and accuracy separately", "Start with clean evaluation traces"],
                "dialogueTurns": [
                    {
                        "speaker": "Maya",
                        "role": "HOST_F",
                        "voice": "Aoede",
                        "style": "warm, encouraging co-host",
                        "text": "Such a great question, Nina—almost everyone hits that exact wall in week one!",
                    },
                    {
                        "speaker": "Alex",
                        "role": "HOST_M",
                        "voice": "Puck",
                        "style": "sharp technical mentor",
                        "text": f"The biggest trap, Nina, is treating the model like magic instead of systems engineering. Anchor on {models[1].lower()}, and verify every boundary with real test cases.",
                    },
                ],
            },
            {
                "beatIndex": 5,
                "speakerRole": "AUDIENCE_Q",
                "chapterTitle": "Live Learner Call-In #2",
                "actTag": "PRACTICAL ROI",
                "punchMetric": "HANDS-ON BUILD",
                "diagramNodeLabels": ["Today's Stack", "First Prototype", "Production Scale"],
                "keyBullets": [
                    "Caller: Sam · Product Builder",
                    "How to apply this mental model in a weekend prototype",
                    models[2][:86],
                ],
                "audienceCaller": {
                    "name": "Sam",
                    "roleTitle": "Product Builder",
                    "voice": "Fenrir",
                    "questionSummary": "What is the fastest practical way to test and apply this concept this week?",
                },
                "dialogueTurns": [
                    {
                        "speaker": "Sam",
                        "role": "AUDIENCE_Q",
                        "voice": "Fenrir",
                        "style": "practical product builder calling in",
                        "text": "Hi both, Sam calling in! If I want to put this into practice on a real project this weekend, <short pause> what is the cleanest starting blueprint?",
                    }
                ],
            },
            {
                "beatIndex": 6,
                "speakerRole": "COHOST_DUO",
                "chapterTitle": "Answering Sam: 3-Step Blueprint",
                "actTag": "BUILDER PLAYBOOK",
                "punchMetric": "3-STEP PLAYBOOK",
                "diagramNodeLabels": ["Baseline Eval", "Focused Build", "Ship & Measure"],
                "keyBullets": [models[2][:86], "Benchmark 20 real examples before optimizing", f"Leverage {comp_name} native tooling"],
                "dialogueTurns": [
                    {
                        "speaker": "Alex",
                        "role": "HOST_M",
                        "voice": "Puck",
                        "style": "actionable systems coach",
                        "text": f"Love the builder mindset, Sam! First, write twenty real test inputs. Second, apply {models[2].lower()}. Third, compare latency and accuracy side by side.",
                    },
                    {
                        "speaker": "Maya",
                        "role": "HOST_F",
                        "voice": "Aoede",
                        "style": "energetic co-host",
                        "text": "Once you see that side-by-side diff on your own data, Sam, the whole architecture clicks for life!",
                    },
                ],
            },
            {
                "beatIndex": 7,
                "speakerRole": "COHOST_DUO",
                "chapterTitle": "Mastery Recap",
                "actTag": "KEY TAKEAWAY",
                "punchMetric": "MASTERY UNLOCKED",
                "diagramNodeLabels": [models[0][:18], models[1][:18], models[2][:18]],
                "keyBullets": [models[0][:86], models[1][:86], models[2][:86]],
                "dialogueTurns": [
                    {
                        "speaker": "Maya",
                        "role": "HOST_F",
                        "voice": "Aoede",
                        "style": "warm, memorable wrap-up",
                        "text": f"Three mental models to keep in your toolkit: {models[0]}, {models[1]}, and {models[2]}.",
                    },
                    {
                        "speaker": "Alex",
                        "role": "HOST_M",
                        "voice": "Puck",
                        "style": "confident sign-off",
                        "text": "Keep building from first principles, test everything against real workloads, and we will see you in the next Intelligentian mastery session!",
                    },
                ],
            },
        ],
    }


def build_curriculum_manifest(item: dict, plates: list[str], api_key: str) -> dict:
    ep_id = str(item["episodeId"])
    comp = str(item.get("companyCategory", "OPENAI")).upper()
    meta = COMPANY_META.get(comp, COMPANY_META["OPENAI"])
    comp_name = meta["display"]
    lvl_full = str(item.get("complexityLevel", "L1_BASICS")).upper()
    lvl_short, lvl_desc = LEVEL_LABELS.get(lvl_full, ("L1", "AI Mastery Curriculum"))

    script_data = None
    script_engine = "deterministic_curriculum_template"
    if api_key:
        cand = generate_gemini_curriculum_script(api_key, item)
        if cand is not None:
            cleaned = json.loads(clean_cta_from_external_text(json.dumps(cand)))
            assert_zero_cta(json.dumps(cleaned), f"{ep_id}.gemini")
            script_data = cleaned
            script_engine = GEMINI_SCRIPT_MODEL
            print(f"[Gemini-4-Hydrogen] Authored interactive curriculum episode {ep_id} ({lvl_short} · {comp_name})")

    if script_data is None:
        script_data = build_deterministic_curriculum_script(item)

    yt_title = clean_cta_from_external_text(str(item.get("title") or script_data.get("youtubeTitle") or ep_id))[:95]
    exec_summary = clean_cta_from_external_text(str(script_data.get("executiveSummary") or item.get("hookPayoff7Sec") or yt_title))

    normalized_beats: list[dict] = []
    caller_cursor = 0
    for idx, raw_b in enumerate(script_data["beats"][:7], 1):
        role = "AUDIENCE_Q" if idx in (3, 5) else "COHOST_DUO"
        node_labels = [clean_cta_from_external_text(str(x))[:22] for x in (raw_b.get("diagramNodeLabels") or []) if str(x).strip()][:5]
        if len(node_labels) < 3:
            node_labels = [x[:20] for x in meta["architectureLayers"][:4]]
        diagram_nodes = [
            {"id": f"n{i+1}", "label": lbl, "role": "core" if i == len(node_labels) // 2 else ("source" if i == 0 else "target")}
            for i, lbl in enumerate(node_labels)
        ]
        diagram_edges = [[f"n{i+1}", f"n{i+2}"] for i in range(len(node_labels) - 1)]

        raw_turns = raw_b.get("dialogueTurns") or []
        turns: list[dict] = []
        audience_caller = None

        if role == "AUDIENCE_Q":
            ac = raw_b.get("audienceCaller") or {}
            c_name = clean_cta_from_external_text(str(ac.get("name") or ("Nina" if idx == 3 else "Sam"))).strip()
            c_role = clean_cta_from_external_text(str(ac.get("roleTitle") or ("Full-Stack Engineer" if idx == 3 else "Product Builder"))).strip()
            c_voice = str(ac.get("voice") or "").strip()
            if c_voice not in AUDIENCE_VOICES:
                c_voice = AUDIENCE_VOICES[caller_cursor % len(AUDIENCE_VOICES)]
            caller_cursor += 1
            t_txt = clean_cta_from_external_text(str(raw_turns[0].get("text", ""))) if raw_turns else ""
            t_txt = re.sub(rf"^{re.escape(c_name)}\s*:\s*", "", t_txt, flags=re.IGNORECASE).strip()
            if not t_txt:
                t_txt = f"Hi Maya and Alex, {c_name} here! How do we apply this {comp_name} mental model cleanly in real projects?"
            q_sum = clean_cta_from_external_text(str(ac.get("questionSummary") or strip_inline_tts_tags(t_txt)))[:125]
            audience_caller = {
                "name": c_name,
                "roleTitle": c_role,
                "displayLabel": f"{c_name} · {c_role}",
                "voice": c_voice,
                "questionSummary": q_sum,
            }
            turns.append(
                {
                    "speaker": c_name,
                    "role": "AUDIENCE_Q",
                    "voice": c_voice,
                    "style": f"curious {c_role.lower()} calling in live",
                    "text": t_txt,
                }
            )
        else:
            for t_i, rt in enumerate(raw_turns[:4]):
                sp_raw = str(rt.get("speaker", "")).strip()
                is_maya = sp_raw.lower().startswith("maya") or (sp_raw.lower() not in ("alex",) and t_i % 2 == 0)
                sp_name = "Maya" if is_maya else "Alex"
                t_txt = clean_cta_from_external_text(str(rt.get("text", ""))).strip()
                t_txt = re.sub(r"^(Maya|Alex)\s*:\s*", "", t_txt, flags=re.IGNORECASE).strip()
                if t_txt:
                    turns.append(
                        {
                            "speaker": sp_name,
                            "role": "HOST_F" if is_maya else "HOST_M",
                            "voice": "Aoede" if is_maya else "Puck",
                            "style": "curious, energetic co-host" if is_maya else "sharp, clear AI systems architect",
                            "text": t_txt,
                        }
                    )
            if len({t["speaker"] for t in turns}) < 2:
                turns = build_deterministic_curriculum_script(item)["beats"][idx - 1]["dialogueTurns"]

        bullets = [clean_cta_from_external_text(str(b))[:90] for b in (raw_b.get("keyBullets") or []) if str(b).strip()][:3]
        while len(bullets) < 3:
            bullets.append(f"{comp_name} · {lvl_desc[:68]}")

        beat_obj: dict = {
            "id": f"beat_{idx:02d}_{role.lower()}",
            "beatIndex": idx,
            "speakerRole": role,
            "deskBanner": (
                f"LIVE VIEWER CALL-IN · {audience_caller['name']} ({audience_caller['roleTitle']})"
                if audience_caller
                else f"MAYA & ALEX · AI MASTERY ({lvl_short})"
            ),
            "chapterTitle": clean_cta_from_external_text(str(raw_b.get("chapterTitle") or f"Part {idx}"))[:54],
            "actTag": clean_cta_from_external_text(str(raw_b.get("actTag") or lvl_short)).upper()[:26],
            "yearStamp": f"{lvl_short} · {item.get('audienceBadge', 'AI MASTERY')}"[:26],
            "punchMetric": clean_cta_from_external_text(str(raw_b.get("punchMetric") or item.get("thumbnailText") or comp_name)).upper()[:22],
            "accentHex": "#34D399" if idx == 3 else ("#FACC15" if idx == 5 else (meta["accentHex"] if idx % 2 == 1 else meta["secondaryHex"])),
            "visualPlate": plates[(idx - 1) % len(plates)],
            "diagramNodes": diagram_nodes,
            "diagramEdges": diagram_edges,
            "keyBullets": bullets,
            "dialogueTurns": turns,
            "narration": " ".join(strip_inline_tts_tags(t["text"]) for t in turns).strip(),
            "citation": {
                "claim": audience_caller["questionSummary"] if audience_caller else clean_cta_from_external_text(str(item.get("hookPayoff7Sec", yt_title)))[:110],
                "sourceName": f"Live Learner Q&A ({audience_caller['displayLabel']})" if audience_caller else f"{comp_name} Engineering Curriculum",
                "sourceDetail": lvl_desc,
                "year": "2026",
            },
        }
        if audience_caller:
            beat_obj["audienceCaller"] = audience_caller
        normalized_beats.append(beat_obj)

    manifest = {
        "episodeId": ep_id,
        "channelId": EXPECTED_CHANNEL_ID,
        "channelHandle": CHANNEL_HANDLE,
        "company": comp,
        "companyCategory": comp,
        "companyDisplayName": comp_name,
        "track": "TRACK_LEARNING",
        "level": lvl_short,
        "complexityLevel": lvl_full,
        "curriculumOrder": int(item.get("episodeNumber", 99)),
        "showFormat": "NOTEBOOKLM_INTERACTIVE_DUO_PLUS_AUDIENCE_QA",
        "scriptEngine": script_engine,
        "title": yt_title,
        "youtubeTitle": yt_title,
        "thumbnailHeadline": str(item.get("thumbnailText") or comp_name)[:22],
        "subtitle": f"Maya & Alex · {lvl_desc} ({comp_name} Interactive Mastery + Viewer Q&A)",
        "executiveSummary": exec_summary,
        "breakingStory": {
            "headline": str(item.get("thumbnailText") or yt_title),
            "publisher": f"{comp_name} · {lvl_short} AI Mastery",
        },
        "voiceConfig": {
            "ttsPrimaryModel": "gemini-3.8-flash-tts",
            "ttsFallbackModel": "gemini-3.8-flash-lite-tts",
            "coHostVoices": {"Maya": "Aoede", "Alex": "Puck"},
            "audienceVoices": list(AUDIENCE_VOICES),
            "edgeVoice": meta["voice"],
            "femaleEdgeVoice": meta["femaleEdgeVoice"],
        },
        "fps": 30,
        "width": 1920,
        "height": 1080,
        "beats": normalized_beats,
        "sources": [
            f"{comp_name} Technical Documentation & Engineering Guides — {yt_title}",
            f"@intelligentian Progressive AI Mastery Curriculum ({lvl_desc})",
        ],
        "hashtags": [
            f"#{comp_name.replace(' ', '').replace('&', '')}",
            "#LearnAI",
            "#AIEngineering",
            "#ArtificialIntelligence",
            "#Intelligentian",
        ],
    }
    assert_zero_cta(json.dumps(manifest), ep_id)
    return manifest


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description="Autonomous Daily Interactive Curriculum Generator for @intelligentian")
    ap.add_argument("--roadmap", default=str(repo_root / "production" / "intelligentian_curriculum_roadmap.json"))
    ap.add_argument("--registry", default=str(repo_root / "production" / "intelligentian_published_registry.json"))
    ap.add_argument("--out-dir", default="/tmp/intelligentian_daily_curriculum")
    ap.add_argument("--drive-queue", default="gdrive:Intelligentian/CurriculumQueue")
    ap.add_argument("--drive-templates", default="gdrive:Intelligentian/NewsTemplates")
    ap.add_argument("--company", choices=[""] + COMPANIES, default="")
    ap.add_argument("--force-generate", action="store_true", help="Generate from roadmap even if CurriculumQueue has MP4s")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    reg = json.loads(Path(args.registry).read_text(encoding="utf-8")) if Path(args.registry).exists() else {"published": {}}
    published_ids = set(reg.get("published", {}).keys())

    out_root = Path(args.out_dir)
    out_root.mkdir(parents=True, exist_ok=True)
    status_ptr = out_root / "latest_episode.json"

    if not args.force_generate and not args.dry_run:
        queued_ep = has_unpublished_drive_curriculum_mp4(args.drive_queue, published_ids)
        if queued_ep:
            status_ptr.write_text(
                json.dumps({"needsBuild": False, "queuedDriveEpisode": queued_ep}, indent=2),
                encoding="utf-8",
            )
            print(f"[Curriculum Queue Ready] Found pre-rendered Drive episode `{queued_ep}` -> delegating directly to publisher.")
            return

    roadmap = json.loads(Path(args.roadmap).read_text(encoding="utf-8")) if Path(args.roadmap).exists() else {}
    item = select_next_curriculum_item(roadmap, published_ids, force_company=args.company)
    comp = str(item.get("companyCategory", "OPENAI")).upper()

    plates = discover_visual_plates(comp, "" if args.dry_run else args.drive_templates, out_root / "_plate_cache")
    api_key = resolve_gemini_api_key()
    manifest = build_curriculum_manifest(item, plates, api_key)

    ep_id = manifest["episodeId"]
    ep_dir = out_root / ep_id
    ep_dir.mkdir(parents=True, exist_ok=True)
    (ep_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    status_ptr.write_text(
        json.dumps(
            {
                "needsBuild": True,
                "episodeId": ep_id,
                "episodeDir": str(ep_dir),
                "company": comp,
                "level": manifest.get("level"),
                "scriptEngine": manifest.get("scriptEngine"),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"[Curriculum Generated] {ep_id} | Level={manifest.get('level')} | Company={comp} | Engine={manifest.get('scriptEngine')}")


if __name__ == "__main__":
    main()
