#!/usr/bin/env python3
"""
Automated Real-Time AI News Harvester & 7-Beat Interactive NotebookLM + Live Audience Q&A Manifest Generator
for @intelligentian (`UCjVbL7GE3cHLOWRYAxZH65A`)

Features:
  1. Fetches live RSS / Atom feeds across:
       - Google News RSS queries for the 7 Frontier AI Companies (`OpenAI`, `Anthropic Claude`,
         `Google DeepMind Gemini`, `Nvidia AI`, `Microsoft Copilot`, `Meta Llama AI`, `xAI Grok`)
       - Official & high-signal AI engineering feeds (OpenAI News RSS, HackerNews AI Algolia/RSS,
         TechCrunch AI, The Verge AI, VentureBeat AI)
  2. Deduplicates against `production/intelligentian_news_history.json` (by canonical normalized headline,
     URL fingerprint, and topic token overlap) and prioritizes fresh stories from the past 24–72 hours,
     rotating across recently under-covered companies so `@intelligentian` maintains balanced coverage.
  3. Classifies the top breaking story into one of the **7 AI Company Categories**
     (`OPENAI`, `ANTHROPIC`, `GOOGLE`, `NVIDIA`, `MICROSOFT`, `META`, `XAI`).
  4. When `GEMINI_API_KEY` is present, calls **`gemini-4-hydrogen`** via the Gemini Interactions API
     (`POST https://generativelanguage.googleapis.com/v1beta/interactions` with JSON Schema `response_format`
     and `store: false`) to synthesize a **7-Beat Interactive NotebookLM Male/Female Co-Host Show (`Maya` & `Alex`)
     + 2 Simulated Live Audience Call-In Questions**:
       - Beats 1, 2, 4, 6, 7 (`speakerRole: "COHOST_DUO"`): Witty, sharp back-and-forth banter between
         Maya (`voice: "Aoede"`, curious/energetic co-host) and Alex (`voice: "Puck"`, razor-sharp AI systems
         architect) breaking down what happened, why it matters, and the technical stack (`diagramNodes`),
         explicitly answering each audience caller by name in Beats 4 and 6!
       - Beats 3 & 5 (`speakerRole: "AUDIENCE_Q"`): 2 Simulated Live Audience Call-In Questions with realistic
         names + roles (e.g., `"Priya · Backend Developer"`, `"David · Small Business Owner"`) voiced by distinct
         prebuilt Gemini TTS voices (`"Leda"`, `"Fenrir"`, `"Charon"`, `"Callirrhoe"`).
  5. Enforces strict `assert_zero_cta` (`subscribe`, `hit the bell`, `smash that like`, `like and share`,
     `leave a comment`, `follow for more` banned) and falls back cleanly to a deterministic 7-beat interactive
     NotebookLM + Audience Q&A template if `GEMINI_API_KEY` is unavailable or rate-limited.
"""
from __future__ import annotations

import argparse
import datetime
import email.utils
import hashlib
import html
import json
import os
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

EXPECTED_CHANNEL_ID = "UCjVbL7GE3cHLOWRYAxZH65A"
CHANNEL_HANDLE = "@intelligentian"

GEMINI_INTERACTIONS_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
GEMINI_SCRIPT_MODEL = "gemini-4-hydrogen"

AUDIENCE_VOICES = ("Leda", "Fenrir", "Charon", "Callirrhoe")

COMPANIES = ["OPENAI", "ANTHROPIC", "GOOGLE", "NVIDIA", "MICROSOFT", "META", "XAI"]

COMPANY_META = {
    "OPENAI": {
        "display": "OpenAI",
        "accentHex": "#10A37F",
        "secondaryHex": "#34D399",
        "voice": "en-US-AndrewMultilingualNeural",
        "femaleEdgeVoice": "en-US-AvaMultilingualNeural",
        "kokoroVoice": "am_michael",
        "keywords": (
            "openai",
            "chatgpt",
            "gpt-5",
            "gpt-4",
            "gpt5",
            "o3",
            "o4",
            "sora",
            "sam altman",
            "responses api",
            "codex",
        ),
        "ecosystemContext": "OpenAI Frontier Reasoning, Responses API & Agentic Orchestration Stack",
        "architectureLayers": ["Client Request", "Router & Policy", "Reasoning Core", "Tool Sandbox", "Verified Output"],
    },
    "ANTHROPIC": {
        "display": "Anthropic",
        "accentHex": "#D97757",
        "secondaryHex": "#FBBF24",
        "voice": "en-US-BrianMultilingualNeural",
        "femaleEdgeVoice": "en-US-AvaMultilingualNeural",
        "kokoroVoice": "am_adam",
        "keywords": (
            "anthropic",
            "claude",
            "sonnet",
            "opus",
            "haiku",
            "model context protocol",
            "mcp",
            "dario amodei",
            "constitutional ai",
            "claude code",
        ),
        "ecosystemContext": "Anthropic Claude Frontier Models, Mechanistic Safety & MCP Tooling",
        "architectureLayers": ["Prompt Context", "Constitutional Guard", "Claude Extended Thinking", "MCP Server Bus", "Artifact Output"],
    },
    "GOOGLE": {
        "display": "Google & DeepMind",
        "accentHex": "#4285F4",
        "secondaryHex": "#38BDF8",
        "voice": "en-US-AndrewMultilingualNeural",
        "femaleEdgeVoice": "en-US-AvaMultilingualNeural",
        "kokoroVoice": "am_michael",
        "keywords": (
            "deepmind",
            "gemini",
            "google ai",
            "alphafold",
            "genie",
            "veo",
            "tpu",
            "demis hassabis",
            "vertex ai",
            "notebooklm",
        ),
        "ecosystemContext": "Google DeepMind Gemini Multimodal Architecture, TPU Pods & Scientific AI",
        "architectureLayers": ["Multimodal Input", "Long-Context KV Cache", "Gemini MoE Core", "TPU v6e Fabric", "Grounded Action"],
    },
    "NVIDIA": {
        "display": "Nvidia",
        "accentHex": "#76B900",
        "secondaryHex": "#A3E635",
        "voice": "en-US-ChristopherNeural",
        "femaleEdgeVoice": "en-US-AvaMultilingualNeural",
        "kokoroVoice": "am_fenrir",
        "keywords": (
            "nvidia",
            "blackwell",
            "rubin",
            "cuda",
            "nvlink",
            "tensorrt",
            "dgx",
            "jensen huang",
            "nim",
            "omniverse",
            "cosmos",
            "h100",
            "h200",
            "gb200",
        ),
        "ecosystemContext": "Nvidia Accelerated Compute, NVLink Rack-Scale Fabrics & TensorRT Inference",
        "architectureLayers": ["HBM3e / HBM4", "Tensor Cores", "NVLink Switch", "CUDA / TensorRT-LLM", "Token Throughput"],
    },
    "MICROSOFT": {
        "display": "Microsoft",
        "accentHex": "#00A4EF",
        "secondaryHex": "#60A5FA",
        "voice": "en-US-BrianMultilingualNeural",
        "femaleEdgeVoice": "en-US-AvaMultilingualNeural",
        "kokoroVoice": "am_adam",
        "keywords": (
            "microsoft",
            "copilot",
            "azure ai",
            "azure openai",
            "phi-4",
            "phi-3",
            "satya nadella",
            "foundry",
            "autogen",
            "semantic kernel",
        ),
        "ecosystemContext": "Microsoft Azure AI Foundry, Copilot Enterprise Graph & Small Language Models",
        "architectureLayers": ["Enterprise Graph", "Azure AI Foundry", "Model Router", "Agent Governance", "Workflow Execution"],
    },
    "META": {
        "display": "Meta AI",
        "accentHex": "#0668E1",
        "secondaryHex": "#818CF8",
        "voice": "en-US-AndrewMultilingualNeural",
        "femaleEdgeVoice": "en-US-AvaMultilingualNeural",
        "kokoroVoice": "am_michael",
        "keywords": (
            "meta ai",
            "llama",
            "open-weights",
            "open source ai",
            "pytorch",
            "yann lecun",
            "fair",
            "mark zuckerberg",
            "vllm",
        ),
        "ecosystemContext": "Meta Llama Open-Weights Ecosystem, PyTorch Stack & Local Quantized Inference",
        "architectureLayers": ["Open Weights", "Quantization (FP8/INT4)", "PyTorch / vLLM", "Local GPU Node", "Private Deployment"],
    },
    "XAI": {
        "display": "xAI",
        "accentHex": "#E2E8F0",
        "secondaryHex": "#38BDF8",
        "voice": "en-US-ChristopherNeural",
        "femaleEdgeVoice": "en-US-AvaMultilingualNeural",
        "kokoroVoice": "am_fenrir",
        "keywords": (
            "xai",
            "grok",
            "colossus",
            "memphis supercluster",
            "deepsearch",
            "aurora",
        ),
        "ecosystemContext": "xAI Grok Reasoning Stack, Colossus 100k+ GPU Fabric & Real-Time Retrieval",
        "architectureLayers": ["Live Telemetry", "Colossus RDMA Fabric", "Grok Reasoning", "DeepSearch Verifier", "Synthesis Brief"],
    },
}

GOOGLE_NEWS_QUERIES = [
    ("OPENAI", "OpenAI GPT OR ChatGPT OR OpenAI Agents when:2d"),
    ("ANTHROPIC", "Anthropic Claude OR Model Context Protocol AI when:2d"),
    ("GOOGLE", "Google DeepMind Gemini OR Google TPU AI when:2d"),
    ("NVIDIA", "Nvidia Blackwell OR Rubin OR CUDA AI infrastructure when:2d"),
    ("MICROSOFT", "Microsoft Copilot OR Azure AI Foundry when:2d"),
    ("META", "Meta Llama AI OR PyTorch open weights when:2d"),
    ("XAI", "xAI Grok OR Colossus supercluster AI when:2d"),
]

DIRECT_TECH_FEEDS = [
    ("OpenAI Official Blog", "https://openai.com/news/rss.xml"),
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("The Verge AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
    ("VentureBeat AI", "https://venturebeat.com/category/ai/feed/"),
    ("HackerNews AI Frontpage", "https://hnrss.org/newest?q=OpenAI+OR+Anthropic+OR+Gemini+OR+Nvidia+OR+Llama+OR+Grok&points=50"),
]

BANNED_CTA_WORDS = (
    "subscribe",
    "hit the bell",
    "click the bell",
    "smash that like",
    "drop a like",
    "like and share",
    "leave a comment",
    "comment below",
    "follow for more",
)


def resolve_gemini_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key
    repo_env = Path(__file__).resolve().parent.parent / ".env"
    if repo_env.exists():
        for ln in repo_env.read_text(encoding="utf-8", errors="ignore").splitlines():
            s = ln.strip()
            if s.startswith("GEMINI_API_KEY="):
                return s.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def assert_zero_cta(text: str, ctx: str) -> None:
    low = (text or "").lower()
    for w in BANNED_CTA_WORDS:
        if w in low:
            raise ValueError(f"STRICT ZERO-CTA VIOLATION in {ctx}: found '{w}'")


def clean_cta_from_external_text(text: str) -> str:
    out = text or ""
    # Replace word-level "subscribe" variants safely with "enroll" / "opt-in" or strip CTA phrases
    for w in BANNED_CTA_WORDS:
        if w == "subscribe":
            out = re.sub(r"\bsubscribe(d|r|rs|s)?\b", "enterprise-plan", out, flags=re.IGNORECASE)
        else:
            out = re.sub(re.escape(w), "", out, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", out).strip()


def strip_inline_tts_tags(text: str) -> str:
    """Removes inline Gemini TTS vocal tags (`<laugh>`, `<short pause>`, etc.) for clean readable narration/captions."""
    cleaned = re.sub(r"<[^>]+>", " ", text or "")
    cleaned = re.sub(r"\|[^|]+\|", " ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def strip_html(raw: str) -> str:
    txt = html.unescape(raw or "")
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return clean_cta_from_external_text(txt)


def parse_pub_date(raw_date: str) -> datetime.datetime:
    now = datetime.datetime.now(datetime.timezone.utc)
    if not raw_date:
        return now
    raw_date = raw_date.strip()
    try:
        dt = email.utils.parsedate_to_datetime(raw_date)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        return dt.astimezone(datetime.timezone.utc)
    except Exception:
        pass
    try:
        dt = datetime.datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        return dt.astimezone(datetime.timezone.utc)
    except Exception:
        return now


def fetch_xml_items(feed_name: str, url: str, hint_company: str | None = None, timeout: int = 12) -> list[dict]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) IntelligentianNewsBot/2.0",
            "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
        },
    )
    items: list[dict] = []
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw_bytes = resp.read()
        root = ET.fromstring(raw_bytes)
    except Exception as exc:
        print(f"[RSS Skip] {feed_name}: {exc}")
        return items

    for el in root.findall(".//item"):
        title = strip_html(el.findtext("title") or "")
        link = (el.findtext("link") or "").strip()
        desc = strip_html(el.findtext("description") or "")
        pub_raw = el.findtext("pubDate") or el.findtext("{http://purl.org/dc/elements/1.1/}date") or ""
        src_el = el.find("source")
        publisher = strip_html(src_el.text if src_el is not None and src_el.text else feed_name)
        if " - " in title and feed_name.startswith("GoogleNews"):
            parts = title.rsplit(" - ", 1)
            if len(parts[1]) < 42:
                title, publisher = parts[0].strip(), parts[1].strip()
        if len(title) >= 18:
            items.append(
                {
                    "title": title,
                    "url": link,
                    "summary": desc[:520],
                    "publisher": publisher or feed_name,
                    "publishedAt": parse_pub_date(pub_raw).isoformat(),
                    "hintCompany": hint_company,
                }
            )

    atom_ns = "{http://www.w3.org/2005/Atom}"
    for el in root.findall(f".//{atom_ns}entry"):
        title = strip_html(el.findtext(f"{atom_ns}title") or "")
        link_el = el.find(f"{atom_ns}link")
        link = (link_el.attrib.get("href", "") if link_el is not None else "").strip()
        summary = strip_html(el.findtext(f"{atom_ns}summary") or el.findtext(f"{atom_ns}content") or "")
        pub_raw = el.findtext(f"{atom_ns}published") or el.findtext(f"{atom_ns}updated") or ""
        if len(title) >= 18:
            items.append(
                {
                    "title": title,
                    "url": link,
                    "summary": summary[:520],
                    "publisher": feed_name,
                    "publishedAt": parse_pub_date(pub_raw).isoformat(),
                    "hintCompany": hint_company,
                }
            )
    return items


def classify_company(item: dict) -> tuple[str, int]:
    text = f"{item.get('title', '')} {item.get('summary', '')}".lower()
    title_low = item.get("title", "").lower()
    best_comp = item.get("hintCompany") or ""
    best_score = 0

    for comp, meta in COMPANY_META.items():
        score = 0
        for kw in meta["keywords"]:
            if kw in title_low:
                score += 6
            elif kw in text:
                score += 2
        if item.get("hintCompany") == comp and score > 0:
            score += 2
        if score > best_score:
            best_score = score
            best_comp = comp

    if best_score == 0 and item.get("hintCompany") in COMPANIES:
        return item["hintCompany"], 1
    return (best_comp if best_comp in COMPANIES else "OPENAI"), best_score


def story_fingerprint(title: str) -> str:
    norm = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()
    tokens = [t for t in norm.split() if len(t) > 2][:10]
    return hashlib.sha1(" ".join(tokens).encode("utf-8")).hexdigest()[:16]


def token_set(title: str) -> set[str]:
    stop = {"the", "and", "for", "with", "from", "into", "that", "this", "new", "how", "why", "its", "over", "after"}
    words = re.findall(r"[a-z0-9]{3,}", title.lower())
    return {w for w in words if w not in stop}


def is_duplicate_story(item: dict, history: dict) -> bool:
    fp = story_fingerprint(item["title"])
    seen_fps = set(history.get("fingerprints", []))
    seen_urls = set(history.get("urls", []))
    if fp in seen_fps or (item.get("url") and item["url"] in seen_urls):
        return True

    cand_tokens = token_set(item["title"])
    if not cand_tokens:
        return False
    for prev in history.get("stories", [])[-120:]:
        prev_tokens = token_set(prev.get("title", ""))
        if not prev_tokens:
            continue
        overlap = len(cand_tokens & prev_tokens) / max(1, min(len(cand_tokens), len(prev_tokens)))
        if overlap >= 0.72:
            return True
    return False


def discover_visual_plates(company: str, drive_templates_remote: str, local_plate_cache: Path) -> list[str]:
    """
    Checks `gdrive:Intelligentian/NewsTemplates/<COMPANY>/` (if rclone is configured) so curated
    16:9 visual plates are reused seamlessly, or returns deterministic plate filenames that
    `intelligentian_daily_news_cloud_builder.py` renders at 1920x1080 if absent.
    """
    comp_dir = local_plate_cache / company
    comp_dir.mkdir(parents=True, exist_ok=True)

    if drive_templates_remote:
        remote_path = f"{drive_templates_remote.rstrip('/')}/{company}"
        res = subprocess.run(["rclone", "lsf", remote_path, "--files-only"], capture_output=True, text=True)
        if res.returncode == 0:
            imgs = [
                ln.strip()
                for ln in res.stdout.splitlines()
                if ln.strip().lower().endswith((".jpg", ".jpeg", ".png"))
            ]
            if imgs:
                subprocess.run(["rclone", "copy", remote_path, str(comp_dir)], check=False)
                downloaded = sorted(str(p) for p in comp_dir.glob("*") if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
                if downloaded:
                    return downloaded

    return [f"assets/plates/{company.lower()}_plate_{i:02d}.png" for i in range(1, 8)]


def extract_key_metric(headline: str, summary: str, company: str) -> str:
    combined = f"{headline} {summary}"
    m = re.search(r"(\$?\d+(?:\.\d+)?\s*(?:B|M|T|K|%|x|GB|TB|GW|MW|tokens|GPUs))", combined, flags=re.IGNORECASE)
    if m:
        return m.group(1).upper().strip()
    return f"{COMPANY_META[company]['display'].upper()} BRIEF"


INTERACTIVE_PODCAST_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "youtubeTitle": {
            "type": "string",
            "description": "Punchy, high-clarity YouTube title (<= 92 chars) on the breaking AI story. Zero clickbait, zero CTAs.",
        },
        "executiveSummary": {
            "type": "string",
            "description": "2-3 sentence technical executive summary of the breaking news and why it matters to builders.",
        },
        "beats": {
            "type": "array",
            "description": "Exactly 7 beats: Beats 1, 2, 4, 6, 7 are COHOST_DUO (Maya & Alex banter); Beats 3 and 5 are AUDIENCE_Q (live viewer call-in questions).",
            "items": {
                "type": "object",
                "properties": {
                    "beatIndex": {"type": "integer"},
                    "speakerRole": {
                        "type": "string",
                        "enum": ["COHOST_DUO", "AUDIENCE_Q"],
                    },
                    "chapterTitle": {
                        "type": "string",
                        "description": "Short chapter headline (<= 48 chars).",
                    },
                    "actTag": {
                        "type": "string",
                        "description": "Short uppercase badge (e.g., BREAKING SIGNAL, STACK TOPOLOGY, LIVE CALLER Q1, ARCHITECT ANSWER, LIVE CALLER Q2, BUILDER PLAYBOOK, FORWARD RADAR).",
                    },
                    "punchMetric": {
                        "type": "string",
                        "description": "Crisp 2-4 word metric or callout stamp (<= 22 chars).",
                    },
                    "diagramNodeLabels": {
                        "type": "array",
                        "description": "3 to 5 short architecture/concept flow node labels (<= 20 chars each).",
                        "items": {"type": "string"},
                    },
                    "keyBullets": {
                        "type": "array",
                        "description": "Exactly 3 concise, high-signal technical bullet points (<= 88 chars each).",
                        "items": {"type": "string"},
                    },
                    "audienceCaller": {
                        "type": "object",
                        "description": "Required when speakerRole is AUDIENCE_Q (Beats 3 and 5); omit or leave empty on COHOST_DUO.",
                        "properties": {
                            "name": {"type": "string", "description": "Realistic first name, e.g., Priya, David, Marcus, Elena."},
                            "roleTitle": {"type": "string", "description": "Realistic job role, e.g., Backend Developer, Small Business Owner, FinTech Lead."},
                            "voice": {
                                "type": "string",
                                "enum": ["Leda", "Fenrir", "Charon", "Callirrhoe"],
                            },
                            "questionSummary": {
                                "type": "string",
                                "description": "Clean 1-sentence summary of the viewer's skeptical or practical question (<= 115 chars).",
                            },
                        },
                        "required": ["name", "roleTitle", "voice", "questionSummary"],
                    },
                    "dialogueTurns": {
                        "type": "array",
                        "description": "Spoken dialogue turns. For COHOST_DUO: 2-3 rapid back-and-forth turns between Maya (voice Aoede) and Alex (voice Puck). For AUDIENCE_Q: 1 turn by the caller.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "speaker": {"type": "string"},
                                "role": {"type": "string", "enum": ["HOST_F", "HOST_M", "AUDIENCE_Q"]},
                                "voice": {
                                    "type": "string",
                                    "enum": ["Aoede", "Puck", "Leda", "Fenrir", "Charon", "Callirrhoe"],
                                },
                                "style": {
                                    "type": "string",
                                    "description": "Delivery style for Gemini 3.8 TTS speech_metadata (e.g., 'curious, energetic co-host' or 'sharp, clear AI systems architect').",
                                },
                                "text": {
                                    "type": "string",
                                    "description": "Verbatim spoken transcript. Optional subtle inline Gemini TTS tags allowed: <short pause>, <laugh>.",
                                },
                            },
                            "required": ["speaker", "role", "voice", "style", "text"],
                        },
                    },
                },
                "required": [
                    "beatIndex",
                    "speakerRole",
                    "chapterTitle",
                    "actTag",
                    "punchMetric",
                    "diagramNodeLabels",
                    "keyBullets",
                    "dialogueTurns",
                ],
            },
        },
    },
    "required": ["youtubeTitle", "executiveSummary", "beats"],
}


def generate_gemini_interactive_script(
    api_key: str,
    primary: dict,
    corroborating: list[dict],
    company: str,
    date_utc: datetime.date,
) -> dict | None:
    """
    Calls `gemini-4-hydrogen` (`POST /v1beta/interactions` with `response_format` JSON schema and `store: false`)
    to author a 7-beat Interactive NotebookLM Male/Female Co-Host Show (`Maya` & `Alex`) + 2 Live Audience Questions.
    """
    meta = COMPANY_META[company]
    comp_name = meta["display"]
    date_label = date_utc.strftime("%b %d, %Y")
    corr_blob = "\n".join(
        f"- {c.get('publisher', 'Tech Press')}: {c.get('title', '')} — {c.get('summary', '')[:220]}"
        for c in corroborating[:3]
    ) or "- Corroborating ecosystem context: rapid latency, cost, and agentic verification competition."

    prompt = f"""You are the executive showrunner for @intelligentian's daily flagship AI engineering show:
"MAYA & ALEX · INTERACTIVE AI BRIEFING DESK" (NotebookLM-style dual-host technical podcast + simulated live viewer call-ins).

Transform today's real breaking AI story ({date_label}) into a 7-beat interactive show JSON strictly matching the schema.

PRIMARY BREAKING STORY:
- Company Ecosystem: {comp_name} ({meta['ecosystemContext']})
- Reference Stack Layers: {', '.join(meta['architectureLayers'])}
- Headline: {primary['title']}
- Source Publisher: {primary.get('publisher', 'AI Industry Report')}
- Summary: {primary.get('summary', '')}

CORROBORATING SIGNALS:
{corr_blob}

EXACT 7-BEAT SHOW STRUCTURE (MANDATORY):
- Beat 1 (`beatIndex: 1`, `speakerRole: "COHOST_DUO"`): Immediate hook! Maya (`voice: "Aoede"`, `role: "HOST_F"`, bright/curious/energetic co-host) & Alex (`voice: "Puck"`, `role: "HOST_M"`, razor-sharp AI systems architect) break what just happened at {comp_name} and why engineers stopped scrolling. (2-3 rapid turns).
- Beat 2 (`beatIndex: 2`, `speakerRole: "COHOST_DUO"`): Under-the-hood technical architecture! Maya asks how it actually works; Alex breaks down the exact system topology (`diagramNodeLabels` with 4-5 crisp stages) and concrete engineering shift.
- Beat 3 (`beatIndex: 3`, `speakerRole: "AUDIENCE_Q"`): First Simulated Live Viewer Call-In! Pick a realistic caller (`audienceCaller` with first `name` + `roleTitle` like `"Priya"` / `"Backend Developer"`, using voice `"Leda"` or `"Callirrhoe"`). One crisp spoken turn (`18-32` words) asking the exact skeptical architectural or reliability question a sharp engineer is thinking right now.
- Beat 4 (`beatIndex: 4`, `speakerRole: "COHOST_DUO"`): Direct Answer to Caller #1! Maya and Alex BOTH address Caller #1 **by first name**, answering their skepticism with clear mechanics, trade-offs, and benchmarks.
- Beat 5 (`beatIndex: 5`, `speakerRole: "AUDIENCE_Q"`): Second Simulated Live Viewer Call-In! Pick a DIFFERENT caller (`name` + `roleTitle` like `"David"` / `"Small Business Owner"` or `"Marcus"` / `"Engineering Manager"`, using a DIFFERENT voice `"Fenrir"` or `"Charon"`). One crisp spoken turn (`18-32` words) asking a practical cost, migration, privacy, or workflow question.
- Beat 6 (`beatIndex: 6`, `speakerRole: "COHOST_DUO"`): Direct Answer to Caller #2! Alex and Maya answer Caller #2 **by first name** with a concrete 3-step builder/operator playbook.
- Beat 7 (`beatIndex: 7`, `speakerRole: "COHOST_DUO"`): Forward Radar & Closing Insight! Witty, memorable closing synthesis from Maya & Alex on what to watch over the next 30 days across the 7 frontier AI labs. End cleanly on pure insight.

HARD RULES (STRICTLY ENFORCED):
1. STRICT ZERO-CTA POLICY: NEVER use any call-to-action words anywhere in spoken dialogue, bullets, or titles. The words/phrases `subscribe`, `hit the bell`, `click the bell`, `smash that like`, `drop a like`, `like and share`, `leave a comment`, `comment below`, and `follow for more` are STRICTLY BANNED (even referring to "software subscriptions" — say "paid tier" or "monthly plan" instead of "subscribe"!).
2. Keep spoken dialogue natural, crisp, and brisk (~35–55 words total on COHOST_DUO beats across 2-3 turns; ~18–32 words on AUDIENCE_Q beats) so total episode runtime is ~95–135 seconds.
3. `text` inside `dialogueTurns` is passed verbatim to `gemini-3.8-flash-tts`: NEVER put speaker prefixes like `Maya:` inside `text`, and use only subtle optional `<short pause>` or `<laugh>` tags (never sound-effect tags).
4. Ensure Beat 3 and Beat 5 callers use two distinct voices from `["Leda", "Fenrir", "Charon", "Callirrhoe"]` (and matching gender-natural voice pairing: `Leda`/`Callirrhoe` for female callers, `Fenrir`/`Charon` for male callers).
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
    except urllib.error.HTTPError as hexc:
        err_txt = hexc.read().decode("utf-8", errors="ignore")[:320]
        print(f"[Gemini-4-Hydrogen Fallback] HTTP {hexc.code}: {err_txt}")
        return None
    except Exception as exc:
        print(f"[Gemini-4-Hydrogen Fallback] Request error: {exc}")
        return None

    out_chunks: list[str] = []
    for step in body.get("steps", []):
        if step.get("type") == "model_output":
            for part in step.get("content", []):
                if part.get("type") == "text" and part.get("text"):
                    out_chunks.append(part["text"])
    raw_json = "".join(out_chunks).strip()
    if not raw_json and isinstance(body.get("output_text"), str):
        raw_json = body["output_text"].strip()
    if not raw_json:
        print("[Gemini-4-Hydrogen Fallback] Empty model_output text")
        return None

    try:
        parsed = json.loads(raw_json)
        beats = parsed.get("beats", [])
        if len(beats) != 7:
            print(f"[Gemini-4-Hydrogen Fallback] Expected 7 beats, got {len(beats)}")
            return None
        return parsed
    except Exception as exc:
        print(f"[Gemini-4-Hydrogen Fallback] JSON parse/validation error: {exc}")
        return None


def build_deterministic_7beat_script(
    primary: dict,
    corroborating: list[dict],
    company: str,
    date_utc: datetime.date,
) -> dict:
    """Deterministic 7-beat Interactive NotebookLM + 2 Audience Call-Ins fallback when GEMINI_API_KEY is absent."""
    meta = COMPANY_META[company]
    comp_name = meta["display"]
    headline_clean = clean_cta_from_external_text(primary["title"].replace("<", "").replace(">", "").strip())
    publisher = primary.get("publisher", "AI Industry Report")
    summary_raw = clean_cta_from_external_text(primary.get("summary") or headline_clean)
    summary_sentence = summary_raw.split(". ")[0].strip().rstrip(".")
    if summary_sentence.lower() == headline_clean.lower() or len(summary_sentence) < 25:
        summary_sentence = (
            f"Engineering teams across the {comp_name} ecosystem are evaluating the architectural and deployment "
            f"implications of this update"
        )
    hero_metric = extract_key_metric(headline_clean, summary_raw, company)
    layers = meta["architectureLayers"]

    yt_title = f"{comp_name} AI Briefing: {headline_clean}"
    if len(yt_title) > 92:
        yt_title = yt_title[:89].rsplit(" ", 1)[0] + "..."

    corr_note = (
        f"Parallel coverage from {corroborating[0].get('publisher', 'tech press')} highlights {corroborating[0]['title'].rstrip('.')}."
        if corroborating
        else f"Across the {comp_name} stack, latency, memory bandwidth, and verification accuracy remain tightly linked."
    )
    corr_note = clean_cta_from_external_text(corr_note)

    return {
        "youtubeTitle": yt_title,
        "executiveSummary": (
            f"Interactive AI systems briefing with Maya and Alex on {comp_name}: {headline_clean}. "
            f"Includes 5-layer stack architecture plus two live viewer Q&A breakdowns on production reliability and cost."
        ),
        "beats": [
            {
                "beatIndex": 1,
                "speakerRole": "COHOST_DUO",
                "chapterTitle": f"Breaking Signal: {comp_name}",
                "actTag": "BREAKING SIGNAL",
                "punchMetric": hero_metric[:22],
                "diagramNodeLabels": [publisher[:18], comp_name[:18], "Developer Impact"],
                "keyBullets": [
                    headline_clean[:86],
                    f"Reported via {publisher} ({date_utc.strftime('%b %d, %Y')})",
                    f"Domain: {meta['ecosystemContext'][:68]}",
                ],
                "dialogueTurns": [
                    {
                        "speaker": "Maya",
                        "role": "HOST_F",
                        "voice": "Aoede",
                        "style": "bright, curious, energetic podcast host",
                        "text": f"Good morning builders! Big signal out of {comp_name} today: {headline_clean}. <short pause> Alex, why is every systems team talking about this?",
                    },
                    {
                        "speaker": "Alex",
                        "role": "HOST_M",
                        "voice": "Puck",
                        "style": "sharp, warm AI systems architect",
                        "text": f"Because this is more than a headline, Maya. Reported via {publisher}, it directly shifts how {comp_name} balances model capability, latency, and real-world deployment.",
                    },
                ],
            },
            {
                "beatIndex": 2,
                "speakerRole": "COHOST_DUO",
                "chapterTitle": f"Inside the {comp_name} Stack",
                "actTag": "STACK TOPOLOGY",
                "punchMetric": "5-LAYER PIPELINE",
                "diagramNodeLabels": [lbl[:20] for lbl in layers],
                "keyBullets": [
                    summary_sentence[:86],
                    f"Ingress & Routing: {layers[0]} -> {layers[1]}",
                    f"Core & Execution: {layers[2]} -> {layers[3]} -> {layers[4]}",
                ],
                "dialogueTurns": [
                    {
                        "speaker": "Maya",
                        "role": "HOST_F",
                        "voice": "Aoede",
                        "style": "curious, analytical co-host",
                        "text": f"Let's pop the hood! Where does this actually sit inside the {comp_name} architecture?",
                    },
                    {
                        "speaker": "Alex",
                        "role": "HOST_M",
                        "voice": "Puck",
                        "style": "clear, structured technical architect",
                        "text": f"{summary_sentence}. Every request flows from {layers[0]} and {layers[1]} straight into {layers[2]}, compounding reliability all the way to {layers[4]}.",
                    },
                ],
            },
            {
                "beatIndex": 3,
                "speakerRole": "AUDIENCE_Q",
                "chapterTitle": "Live Viewer Call-In #1: Reliability",
                "actTag": "LIVE CALLER Q1",
                "punchMetric": "CALLER QUESTION",
                "diagramNodeLabels": ["Headline Spec", "Edge Cases", "Verified Eval"],
                "keyBullets": [
                    "Caller: Priya · Backend Developer",
                    "Question: Does this hold up under real production traffic or drift on multi-step tool calls?",
                    "Evaluating p95 latency and deterministic guardrails",
                ],
                "audienceCaller": {
                    "name": "Priya",
                    "roleTitle": "Backend Developer",
                    "voice": "Leda",
                    "questionSummary": f"Does this {comp_name} update hold up under real multi-step production traffic without tool drift?",
                },
                "dialogueTurns": [
                    {
                        "speaker": "Priya",
                        "role": "AUDIENCE_Q",
                        "voice": "Leda",
                        "style": "skeptical, practical backend developer calling in",
                        "text": f"Hey Maya and Alex, Priya here, backend developer! Benchmarks always look great on launch day, <short pause> does this actually hold up on messy multi-step production workflows?",
                    }
                ],
            },
            {
                "beatIndex": 4,
                "speakerRole": "COHOST_DUO",
                "chapterTitle": "Answering Priya: Production Guardrails",
                "actTag": "ARCHITECT ANSWER",
                "punchMetric": "SHADOW EVALS",
                "diagramNodeLabels": ["Domain Prompts", "Shadow Traffic", "Fallback Router"],
                "keyBullets": [
                    "Run domain-specific regression suites before switching traffic",
                    "Pair frontier reasoning with schema validation and fallback routing",
                    corr_note[:86],
                ],
                "dialogueTurns": [
                    {
                        "speaker": "Maya",
                        "role": "HOST_F",
                        "voice": "Aoede",
                        "style": "warm, validating co-host",
                        "text": "Spot-on question, Priya! Launch benchmarks never tell the whole story until your own edge cases hit the API.",
                    },
                    {
                        "speaker": "Alex",
                        "role": "HOST_M",
                        "voice": "Puck",
                        "style": "precise, practical AI architect",
                        "text": f"Here is the rule, Priya: shadow-test {comp_name} on fifty of your hardest real traces first, enforce strict JSON schema checks, and keep an automatic fallback router ready.",
                    },
                ],
            },
            {
                "beatIndex": 5,
                "speakerRole": "AUDIENCE_Q",
                "chapterTitle": "Live Viewer Call-In #2: Cost & Lock-In",
                "actTag": "LIVE CALLER Q2",
                "punchMetric": "COST & ROI",
                "diagramNodeLabels": ["Token Budget", "Model Router", "Zero Lock-In"],
                "keyBullets": [
                    "Caller: David · Small Business Owner",
                    "Question: How do smaller teams adopt this without blowing up monthly inference budgets or vendor lock-in?",
                    "Routing routine tasks vs complex reasoning turns",
                ],
                "audienceCaller": {
                    "name": "David",
                    "roleTitle": "Small Business Owner",
                    "voice": "Fenrir",
                    "questionSummary": "How can a lean team adopt these capabilities without runaway inference costs or vendor lock-in?",
                },
                "dialogueTurns": [
                    {
                        "speaker": "David",
                        "role": "AUDIENCE_Q",
                        "voice": "Fenrir",
                        "style": "earnest, cost-conscious small business owner calling in",
                        "text": "Hi team, this is David, I run a small software shop! How do lean teams use this without blowing up our monthly token bill or getting locked in?",
                    }
                ],
            },
            {
                "beatIndex": 6,
                "speakerRole": "COHOST_DUO",
                "chapterTitle": "Answering David: Lean Builder Playbook",
                "actTag": "BUILDER PLAYBOOK",
                "punchMetric": "TIERED ROUTING",
                "diagramNodeLabels": ["Fast Lite Tier", "Frontier Core", "Clean Adapter"],
                "keyBullets": [
                    "Step 1: Route 80% of routine classification to lightweight models",
                    f"Step 2: Reserve heavy {comp_name} reasoning for high-value steps",
                    "Step 3: Keep a thin provider-agnostic adapter so switching takes minutes",
                ],
                "dialogueTurns": [
                    {
                        "speaker": "Alex",
                        "role": "HOST_M",
                        "voice": "Puck",
                        "style": "encouraging, actionable systems advisor",
                        "text": f"Great call, David! Never send every prompt to the biggest model—route eighty percent of routine work to fast lite tiers and save {comp_name}'s heavy reasoning for the hardest twenty percent.",
                    },
                    {
                        "speaker": "Maya",
                        "role": "HOST_F",
                        "voice": "Aoede",
                        "style": "energetic, crisp co-host",
                        "text": "And wrap your model calls behind one clean interface, David, <short pause> so swapping across OpenAI, Anthropic, Google, or open weights takes five minutes, zero lock-in!",
                    },
                ],
            },
            {
                "beatIndex": 7,
                "speakerRole": "COHOST_DUO",
                "chapterTitle": "30-Day Frontier Radar",
                "actTag": "FORWARD RADAR",
                "punchMetric": "NEXT 30 DAYS",
                "diagramNodeLabels": ["Blind Evals", "p95 Latency", "7-Lab Response"],
                "keyBullets": [
                    "Watch independent developer evaluations over the next 30 days",
                    "Track real-world API throughput, rate limits, and pricing moves",
                    f"Monitor counter-moves across all 7 frontier ecosystems after {comp_name}",
                ],
                "dialogueTurns": [
                    {
                        "speaker": "Maya",
                        "role": "HOST_F",
                        "voice": "Aoede",
                        "style": "bright, forward-looking",
                        "text": f"Over the next thirty days, watch independent blind evaluations and see how peer labs respond to {comp_name}.",
                    },
                    {
                        "speaker": "Alex",
                        "role": "HOST_M",
                        "voice": "Puck",
                        "style": "warm, decisive sign-off",
                        "text": "Measure real latency, keep your architecture modular, and build with verified signal. See you on tomorrow's Intelligentian briefing desk!",
                    },
                ],
            },
        ],
    }


def build_7beat_interactive_manifest(
    primary: dict,
    corroborating: list[dict],
    company: str,
    date_utc: datetime.date,
    visual_plates: list[str],
    api_key: str = "",
) -> dict:
    meta = COMPANY_META[company]
    comp_name = meta["display"]
    headline_clean = clean_cta_from_external_text(primary["title"].replace("<", "").replace(">", "").strip())
    publisher = primary.get("publisher", "AI Industry Report")
    date_label = date_utc.strftime("%b %d, %Y")

    slug = re.sub(r"[^a-zA-Z0-9]+", "_", headline_clean).strip("_")[:38]
    ep_id = f"NEWS_{date_utc.strftime('%Y%m%d')}_{company}_{slug}"

    script_data: dict | None = None
    script_engine = "deterministic_template"
    if api_key:
        candidate = generate_gemini_interactive_script(api_key, primary, corroborating, company, date_utc)
        if candidate is not None:
            try:
                assert_zero_cta(json.dumps(candidate), f"{ep_id}.gemini_candidate")
                script_data = candidate
                script_engine = GEMINI_SCRIPT_MODEL
                print(f"[Gemini-4-Hydrogen] Synthesized 7-beat Interactive Maya & Alex + 2 Audience Q&A script for {ep_id}")
            except ValueError as cta_err:
                print(f"[Gemini-4-Hydrogen Sanitizer] Cleaning CTA phrase ({cta_err}) and re-validating...")
                cleaned_str = clean_cta_from_external_text(json.dumps(candidate))
                candidate = json.loads(cleaned_str)
                assert_zero_cta(json.dumps(candidate), f"{ep_id}.gemini_sanitized")
                script_data = candidate
                script_engine = GEMINI_SCRIPT_MODEL

    if script_data is None:
        script_data = build_deterministic_7beat_script(primary, corroborating, company, date_utc)

    yt_title = clean_cta_from_external_text(script_data.get("youtubeTitle") or f"{comp_name} AI Briefing: {headline_clean}")
    if len(yt_title) > 96:
        yt_title = yt_title[:93].rsplit(" ", 1)[0] + "..."

    exec_summary = clean_cta_from_external_text(
        script_data.get("executiveSummary")
        or f"Interactive technical briefing with Maya & Alex on {comp_name}: {headline_clean}, featuring two live viewer Q&A breakdowns."
    )

    def pick_plate(idx: int) -> str:
        return visual_plates[idx % len(visual_plates)]

    normalized_beats: list[dict] = []
    caller_voice_cursor = 0

    for idx, raw_b in enumerate(script_data["beats"][:7], 1):
        expected_role = "AUDIENCE_Q" if idx in (3, 5) else "COHOST_DUO"
        speaker_role = raw_b.get("speakerRole") if raw_b.get("speakerRole") in ("COHOST_DUO", "AUDIENCE_Q") else expected_role
        # Enforce strict Beat 3 & 5 = AUDIENCE_Q and Beats 1,2,4,6,7 = COHOST_DUO
        speaker_role = expected_role

        node_labels = [clean_cta_from_external_text(str(lbl))[:24] for lbl in (raw_b.get("diagramNodeLabels") or []) if str(lbl).strip()][:5]
        if len(node_labels) < 3:
            node_labels = [lbl[:22] for lbl in meta["architectureLayers"][:4]]

        diagram_nodes = [
            {
                "id": f"n{i+1}",
                "label": lbl,
                "role": "core" if i == len(node_labels) // 2 else ("source" if i == 0 else "target"),
            }
            for i, lbl in enumerate(node_labels)
        ]
        diagram_edges = [[f"n{i+1}", f"n{i+2}"] for i in range(len(node_labels) - 1)]

        raw_turns = raw_b.get("dialogueTurns") or []
        turns: list[dict] = []
        audience_caller: dict | None = None

        if speaker_role == "AUDIENCE_Q":
            ac = raw_b.get("audienceCaller") or {}
            c_name = clean_cta_from_external_text(str(ac.get("name") or ("Priya" if idx == 3 else "David"))).strip()
            c_role = clean_cta_from_external_text(str(ac.get("roleTitle") or ("Backend Developer" if idx == 3 else "Small Business Owner"))).strip()
            c_voice = str(ac.get("voice") or "").strip()
            if c_voice not in AUDIENCE_VOICES:
                c_voice = AUDIENCE_VOICES[caller_voice_cursor % len(AUDIENCE_VOICES)]
            caller_voice_cursor += 1

            first_turn_txt = clean_cta_from_external_text(str(raw_turns[0].get("text", ""))) if raw_turns else ""
            if not first_turn_txt:
                first_turn_txt = str(ac.get("questionSummary") or f"Hi Maya and Alex, {c_name} here! How does this {comp_name} update impact real-world reliability and cost?")
            # Strip any accidental leading "Name:" prefix
            first_turn_txt = re.sub(rf"^{re.escape(c_name)}\s*:\s*", "", first_turn_txt, flags=re.IGNORECASE).strip()

            q_summary = clean_cta_from_external_text(str(ac.get("questionSummary") or strip_inline_tts_tags(first_turn_txt)))[:130]
            audience_caller = {
                "name": c_name,
                "roleTitle": c_role,
                "displayLabel": f"{c_name} · {c_role}",
                "voice": c_voice,
                "questionSummary": q_summary,
            }
            turns.append(
                {
                    "speaker": c_name,
                    "role": "AUDIENCE_Q",
                    "voice": c_voice,
                    "style": clean_cta_from_external_text(str(raw_turns[0].get("style") if raw_turns else f"curious, earnest {c_role.lower()} calling in live")),
                    "text": first_turn_txt,
                }
            )
        else:
            for t_i, rt in enumerate(raw_turns[:4]):
                sp_raw = str(rt.get("speaker", "")).strip()
                is_maya = sp_raw.lower().startswith("maya") or (sp_raw.lower() not in ("alex",) and t_i % 2 == 0)
                sp_name = "Maya" if is_maya else "Alex"
                sp_role = "HOST_F" if is_maya else "HOST_M"
                sp_voice = "Aoede" if is_maya else "Puck"
                t_txt = clean_cta_from_external_text(str(rt.get("text", ""))).strip()
                t_txt = re.sub(r"^(Maya|Alex)\s*:\s*", "", t_txt, flags=re.IGNORECASE).strip()
                if t_txt:
                    turns.append(
                        {
                            "speaker": sp_name,
                            "role": sp_role,
                            "voice": sp_voice,
                            "style": clean_cta_from_external_text(
                                str(rt.get("style") or ("curious, energetic co-host" if is_maya else "sharp, clear AI systems architect"))
                            ),
                            "text": t_txt,
                        }
                    )
            # Ensure both Maya and Alex participate on COHOST_DUO beats
            speakers_present = {t["speaker"] for t in turns}
            if len(turns) < 2 or len(speakers_present) < 2:
                fallback_script = build_deterministic_7beat_script(primary, corroborating, company, date_utc)
                turns = fallback_script["beats"][idx - 1]["dialogueTurns"]

        plain_narration = " ".join(strip_inline_tts_tags(t["text"]) for t in turns).strip()
        bullets = [clean_cta_from_external_text(str(b))[:90] for b in (raw_b.get("keyBullets") or []) if str(b).strip()][:3]
        while len(bullets) < 3:
            bullets.append(f"{comp_name} ecosystem: {meta['ecosystemContext'][:68]}")

        accent = "#34D399" if idx == 3 else ("#FACC15" if idx == 5 else (meta["accentHex"] if idx % 2 == 1 else meta["secondaryHex"]))

        beat_obj: dict = {
            "id": f"beat_{idx:02d}_{speaker_role.lower()}",
            "beatIndex": idx,
            "speakerRole": speaker_role,
            "deskBanner": (
                f"LIVE VIEWER CALL-IN · {audience_caller['name']} ({audience_caller['roleTitle']})"
                if audience_caller
                else "MAYA & ALEX · AI BRIEFING DESK"
            ),
            "chapterTitle": clean_cta_from_external_text(str(raw_b.get("chapterTitle") or f"Section {idx}"))[:54],
            "actTag": clean_cta_from_external_text(str(raw_b.get("actTag") or ("LIVE CALL-IN" if audience_caller else "AI BRIEFING"))).upper()[:26],
            "yearStamp": date_label.upper(),
            "punchMetric": clean_cta_from_external_text(str(raw_b.get("punchMetric") or comp_name.upper())).upper()[:22],
            "accentHex": accent,
            "visualPlate": pick_plate(idx - 1),
            "diagramNodes": diagram_nodes,
            "diagramEdges": diagram_edges,
            "keyBullets": bullets,
            "dialogueTurns": turns,
            "narration": plain_narration,
            "citation": {
                "claim": audience_caller["questionSummary"] if audience_caller else headline_clean[:110],
                "sourceName": f"Live Viewer Q&A ({audience_caller['displayLabel']})" if audience_caller else publisher,
                "sourceDetail": primary.get("url", "") if idx == 1 else f"{comp_name} Technical Briefing",
                "year": str(date_utc.year),
            },
        }
        if audience_caller:
            beat_obj["audienceCaller"] = audience_caller

        normalized_beats.append(beat_obj)

    sources_list = [f"{publisher} ({date_label}) — {headline_clean}: {primary.get('url', '')}".strip(": ")]
    for corr in corroborating[:3]:
        sources_list.append(
            f"{corr.get('publisher', 'Source')} — {corr['title']}: {corr.get('url', '')}".strip(": ")
        )

    manifest = {
        "episodeId": ep_id,
        "channelId": EXPECTED_CHANNEL_ID,
        "channelHandle": CHANNEL_HANDLE,
        "company": company,
        "companyDisplayName": comp_name,
        "track": "TRACK_NEWS",
        "showFormat": "NOTEBOOKLM_INTERACTIVE_DUO_PLUS_AUDIENCE_QA",
        "scriptEngine": script_engine,
        "title": yt_title,
        "youtubeTitle": yt_title,
        "subtitle": f"Maya & Alex · Interactive {comp_name} AI Briefing + Live Viewer Q&A ({date_label})",
        "executiveSummary": exec_summary,
        "coHosts": [
            {"speaker": "Maya", "role": "HOST_F", "voice": "Aoede", "persona": "Curious, energetic co-host"},
            {"speaker": "Alex", "role": "HOST_M", "voice": "Puck", "persona": "Sharp AI systems architect"},
        ],
        "breakingStory": {
            "headline": headline_clean,
            "publisher": publisher,
            "url": primary.get("url", ""),
            "publishedAt": primary.get("publishedAt", ""),
            "fingerprint": story_fingerprint(headline_clean),
        },
        "voiceConfig": {
            "ttsPrimaryModel": "gemini-3.8-flash-tts",
            "ttsFallbackModel": "gemini-3.8-flash-lite-tts",
            "coHostVoices": {"Maya": "Aoede", "Alex": "Puck"},
            "audienceVoices": list(AUDIENCE_VOICES),
            "edgeVoice": meta["voice"],
            "femaleEdgeVoice": meta["femaleEdgeVoice"],
            "kokoroVoice": meta["kokoroVoice"],
        },
        "fps": 30,
        "width": 1920,
        "height": 1080,
        "beats": normalized_beats,
        "sources": sources_list,
        "hashtags": [
            f"#{comp_name.replace(' ', '').replace('&', '')}",
            "#AINews",
            "#AIEngineering",
            "#ArtificialIntelligence",
            "#Intelligentian",
        ],
    }

    assert_zero_cta(json.dumps(manifest), ep_id)
    return manifest


def harvest_and_select(
    history: dict,
    force_company: str = "",
) -> tuple[str, dict, list[dict]]:
    all_candidates: list[dict] = []

    for comp, query in GOOGLE_NEWS_QUERIES:
        if force_company and comp != force_company:
            continue
        encoded_q = urllib.parse.quote(query)
        gnews_url = f"https://news.google.com/rss/search?q={encoded_q}&hl=en-US&gl=US&ceid=US:en"
        all_candidates.extend(fetch_xml_items(f"GoogleNews-{comp}", gnews_url, hint_company=comp))

    for feed_name, feed_url in DIRECT_TECH_FEEDS:
        all_candidates.extend(fetch_xml_items(feed_name, feed_url, hint_company=None))

    now_utc = datetime.datetime.now(datetime.timezone.utc)
    recent_companies = [s.get("company") for s in history.get("stories", [])[-4:]]

    scored: list[tuple[float, str, dict]] = []
    seen_batch_fps: set[str] = set()

    for item in all_candidates:
        fp = story_fingerprint(item["title"])
        if fp in seen_batch_fps or is_duplicate_story(item, history):
            continue
        comp, kw_score = classify_company(item)
        if force_company and comp != force_company:
            continue
        if kw_score <= 0:
            continue

        pub_dt = parse_pub_date(item.get("publishedAt", ""))
        age_hours = max(0.0, (now_utc - pub_dt).total_seconds() / 3600.0)
        recency_bonus = max(0.0, 36.0 - min(age_hours, 72.0) * 0.5)
        rotation_bonus = 4.0 if comp not in recent_companies else 0.0
        source_bonus = 3.5 if not str(item.get("publisher", "")).startswith("GoogleNews") else 1.5

        total_score = kw_score * 2.5 + recency_bonus * 0.4 + rotation_bonus + source_bonus
        seen_batch_fps.add(fp)
        scored.append((total_score, comp, item))

    if not scored:
        target_comp = force_company if force_company in COMPANIES else COMPANIES[now_utc.timetuple().tm_yday % len(COMPANIES)]
        disp = COMPANY_META[target_comp]["display"]
        fallback_item = {
            "title": f"{disp} Advances Frontier Reasoning Efficiency and Enterprise Agent Reliability",
            "url": "https://news.ycombinator.com/",
            "summary": (
                f"Engineering teams deploying {disp} models are adopting structured verification harnesses, "
                f"KV-cache compression, and low-latency tool routing for production AI systems."
            ),
            "publisher": "AI Systems Engineering Brief",
            "publishedAt": now_utc.isoformat(),
            "hintCompany": target_comp,
        }
        return target_comp, fallback_item, []

    scored.sort(key=lambda x: x[0], reverse=True)
    _, top_comp, top_item = scored[0]
    corroborating = [it for _, c, it in scored[1:12] if c == top_comp and it["title"] != top_item["title"]][:3]
    return top_comp, top_item, corroborating


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description="Real-Time AI News Harvester & Interactive Maya/Alex Podcast Generator for @intelligentian")
    ap.add_argument("--history-file", default=str(repo_root / "production" / "intelligentian_news_history.json"))
    ap.add_argument("--out-dir", default="/tmp/intelligentian_daily_news", help="Parent directory for generated episode folder")
    ap.add_argument("--company", choices=[""] + COMPANIES, default="", help="Optional force specific AI company")
    ap.add_argument(
        "--drive-templates",
        default="gdrive:Intelligentian/NewsTemplates",
        help="rclone path to curated per-company 16:9 visual plates",
    )
    ap.add_argument("--dry-run", action="store_true", help="Fetch and generate manifest without updating history")
    args = ap.parse_args()

    hist_path = Path(args.history_file)
    hist_path.parent.mkdir(parents=True, exist_ok=True)
    history = (
        json.loads(hist_path.read_text(encoding="utf-8"))
        if hist_path.exists()
        else {"channelId": EXPECTED_CHANNEL_ID, "fingerprints": [], "urls": [], "stories": []}
    )

    company, primary_story, corroborating = harvest_and_select(history, force_company=args.company)
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()

    plate_cache = Path(args.out_dir) / "_plate_cache"
    plates = discover_visual_plates(company, "" if args.dry_run else args.drive_templates, plate_cache)
    api_key = resolve_gemini_api_key()
    manifest = build_7beat_interactive_manifest(
        primary_story,
        corroborating,
        company,
        today_utc,
        plates,
        api_key=api_key,
    )

    ep_id = manifest["episodeId"]
    ep_dir = Path(args.out_dir) / ep_id
    ep_dir.mkdir(parents=True, exist_ok=True)
    mf_path = ep_dir / "manifest.json"
    mf_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    latest_ptr = Path(args.out_dir) / "latest_episode.json"
    latest_ptr.write_text(
        json.dumps(
            {
                "episodeId": ep_id,
                "episodeDir": str(ep_dir),
                "company": company,
                "scriptEngine": manifest.get("scriptEngine"),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"[News Harvested] Company={company} | Engine={manifest.get('scriptEngine')} | Episode={ep_id}")
    print(f"  Headline : {primary_story['title']}")
    print(f"  YT Title : {manifest['youtubeTitle']}")
    print(f"  Source   : {primary_story.get('publisher')} ({primary_story.get('publishedAt')})")
    print(f"  Manifest : {mf_path}")

    if not args.dry_run:
        fp = story_fingerprint(primary_story["title"])
        history.setdefault("fingerprints", []).append(fp)
        if primary_story.get("url"):
            history.setdefault("urls", []).append(primary_story["url"])
        history.setdefault("stories", []).append(
            {
                "episodeId": ep_id,
                "company": company,
                "title": primary_story["title"],
                "publisher": primary_story.get("publisher", ""),
                "url": primary_story.get("url", ""),
                "publishedAt": primary_story.get("publishedAt", ""),
                "harvestedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "fingerprint": fp,
            }
        )
        history["fingerprints"] = history["fingerprints"][-1000:]
        history["urls"] = history["urls"][-1000:]
        history["stories"] = history["stories"][-500:]
        hist_path.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[History Updated] Recorded fingerprint {fp} -> {hist_path}")


if __name__ == "__main__":
    main()
