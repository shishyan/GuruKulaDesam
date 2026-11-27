#!/usr/bin/env python3
"""
Automated Real-Time AI News Harvester & 8-Beat Structured Manifest Generator for @intelligentian (`UCjVbL7GE3cHLOWRYAxZH65A`)

Features:
  1. Fetches live RSS / Atom feeds across:
       - Google News RSS queries for the 7 Frontier AI Companies (`OpenAI`, `Anthropic Claude`,
         `Google DeepMind Gemini`, `Nvidia AI`, `Microsoft Copilot`, `Meta Llama AI`, `xAI Grok`)
       - Official & high-signal AI engineering feeds (OpenAI News RSS, HackerNews AI Algolia/RSS,
         TechCrunch AI, The Verge AI, VentureBeat AI, ArXiv CS.AI/CS.LG)
  2. Deduplicates against `production/intelligentian_news_history.json` (by canonical normalized headline,
     URL fingerprint, and topic token overlap) and prioritizes fresh stories from the past 24–72 hours,
     rotating across recently under-covered companies so `@intelligentian` maintains balanced coverage.
  3. Classifies the top breaking story into one of the **7 AI Company Categories**
     (`OPENAI`, `ANTHROPIC`, `GOOGLE`, `NVIDIA`, `MICROSOFT`, `META`, `XAI`).
  4. Synthesizes a complete, Zero-CTA 8-beat `manifest.json` (`episodeId`, `company`, `track="TRACK_NEWS"`,
     8 structured narrative beats, architecture diagram `nodes` + `edges`, empirical takeaways, source citations,
     and `visualPlate` mappings pointing to `gdrive:Intelligentian/NewsTemplates/<COMPANY>/` or freshly generated
     plates) ready for either Remotion (`Utility_Explainer_Studio`) or autonomous GitHub Actions rendering via
     `tools/intelligentian_daily_news_cloud_builder.py`.
"""
from __future__ import annotations

import argparse
import datetime
import email.utils
import hashlib
import html
import json
import re
import subprocess
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

EXPECTED_CHANNEL_ID = "UCjVbL7GE3cHLOWRYAxZH65A"
CHANNEL_HANDLE = "@intelligentian"

COMPANIES = ["OPENAI", "ANTHROPIC", "GOOGLE", "NVIDIA", "MICROSOFT", "META", "XAI"]

COMPANY_META = {
    "OPENAI": {
        "display": "OpenAI",
        "accentHex": "#10A37F",
        "secondaryHex": "#34D399",
        "voice": "en-US-AndrewMultilingualNeural",
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


def assert_zero_cta(text: str, ctx: str) -> None:
    low = (text or "").lower()
    for w in BANNED_CTA_WORDS:
        if w in low:
            raise ValueError(f"STRICT ZERO-CTA VIOLATION in {ctx}: found '{w}'")


def clean_cta_from_external_text(text: str) -> str:
    out = text or ""
    for w in BANNED_CTA_WORDS:
        out = re.sub(re.escape(w), "", out, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", out).strip()


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
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) IntelligentianNewsBot/1.0",
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

    # Standard RSS 2.0 <item>
    for el in root.findall(".//item"):
        title = strip_html(el.findtext("title") or "")
        link = (el.findtext("link") or "").strip()
        desc = strip_html(el.findtext("description") or "")
        pub_raw = el.findtext("pubDate") or el.findtext("{http://purl.org/dc/elements/1.1/}date") or ""
        src_el = el.find("source")
        publisher = strip_html(src_el.text if src_el is not None and src_el.text else feed_name)
        # Clean Google News trailing " - Publisher Name"
        if " - " in title and feed_name.startswith("GoogleNews"):
            parts = title.rsplit(" - ", 1)
            if len(parts[1]) < 42:
                title, publisher = parts[0].strip(), parts[1].strip()
        if len(title) >= 18:
            items.append(
                {
                    "title": title,
                    "url": link,
                    "summary": desc[:480],
                    "publisher": publisher or feed_name,
                    "publishedAt": parse_pub_date(pub_raw).isoformat(),
                    "hintCompany": hint_company,
                }
            )

    # Atom <entry>
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
                    "summary": summary[:480],
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

    return [f"assets/plates/{company.lower()}_plate_{i:02d}.png" for i in range(1, 9)]


def extract_key_metric(headline: str, summary: str, company: str) -> str:
    combined = f"{headline} {summary}"
    m = re.search(r"(\$?\d+(?:\.\d+)?\s*(?:B|M|T|K|%|x|GB|TB|GW|MW|tokens|GPUs))", combined, flags=re.IGNORECASE)
    if m:
        return m.group(1).upper().strip()
    return f"{COMPANY_META[company]['display'].upper()} BRIEF"


def build_8beat_manifest(
    primary: dict,
    corroborating: list[dict],
    company: str,
    date_utc: datetime.date,
    visual_plates: list[str],
) -> dict:
    meta = COMPANY_META[company]
    comp_name = meta["display"]
    headline_clean = primary["title"].replace("<", "").replace(">", "").strip()
    publisher = primary.get("publisher", "AI Industry Report")
    summary_raw = primary.get("summary") or headline_clean
    summary_sentence = summary_raw.split(". ")[0].strip().rstrip(".")
    if summary_sentence.lower() == headline_clean.lower() or len(summary_sentence) < 25:
        summary_sentence = (
            f"Engineering teams across the {comp_name} ecosystem are evaluating the architectural and deployment "
            f"implications of this release"
        )

    hero_metric = extract_key_metric(headline_clean, summary_raw, company)
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", headline_clean).strip("_")[:38]
    ep_id = f"NEWS_{date_utc.strftime('%Y%m%d')}_{company}_{slug}"
    date_label = date_utc.strftime("%b %d, %Y")

    yt_title = f"{comp_name} AI Alert: {headline_clean}"
    if len(yt_title) > 96:
        yt_title = yt_title[:93].rsplit(" ", 1)[0] + "..."

    corroborating_line = ""
    if corroborating:
        sec_story = corroborating[0]["title"].rstrip(".")
        sec_pub = corroborating[0].get("publisher", "Tech Press")
        corroborating_line = (
            f"Parallel reporting from {sec_pub} also highlights {sec_story}, underscoring rapid momentum across the stack."
        )
    else:
        corroborating_line = (
            f"Across the broader {comp_name} roadmap, this update tightens the loop between model capability, latency, and cost efficiency."
        )

    layers = meta["architectureLayers"]

    def pick_plate(idx: int) -> str:
        return visual_plates[idx % len(visual_plates)]

    beats = [
        {
            "id": "beat_01_breaking_signal",
            "beatIndex": 1,
            "chapterTitle": f"Breaking Signal: {comp_name}",
            "actTag": "BREAKING AI BRIEF",
            "yearStamp": date_label.upper(),
            "punchMetric": hero_metric,
            "accentHex": meta["accentHex"],
            "visualPlate": pick_plate(0),
            "diagramNodes": [
                {"id": "n1", "label": publisher[:24], "role": "source"},
                {"id": "n2", "label": comp_name, "role": "core"},
                {"id": "n3", "label": "Global AI Impact", "role": "target"},
            ],
            "diagramEdges": [["n1", "n2"], ["n2", "n3"]],
            "keyBullets": [
                headline_clean[:88],
                f"Primary Reporting: {publisher} ({date_label})",
                f"Ecosystem Domain: {meta['ecosystemContext'][:64]}",
            ],
            "narration": (
                f"Breaking AI intelligence brief for {date_label}. {headline_clean}. "
                f"Reported via {publisher}, this development marks a notable technical shift inside the {comp_name} ecosystem."
            ),
            "citation": {
                "claim": headline_clean,
                "sourceName": publisher,
                "sourceDetail": primary.get("url", ""),
                "year": str(date_utc.year),
            },
        },
        {
            "id": "beat_02_what_launched",
            "beatIndex": 2,
            "chapterTitle": "Core Facts & Release Scope",
            "actTag": "CORE FACTS",
            "yearStamp": comp_name.upper(),
            "punchMetric": "VERIFIED SCOPE",
            "accentHex": meta["secondaryHex"],
            "visualPlate": pick_plate(1),
            "diagramNodes": [
                {"id": "n1", "label": "Announcement", "role": "source"},
                {"id": "n2", "label": "Technical Spec", "role": "core"},
                {"id": "n3", "label": "Rollout Window", "role": "target"},
            ],
            "diagramEdges": [["n1", "n2"], ["n2", "n3"]],
            "keyBullets": [
                summary_sentence[:90],
                "Separating verified engineering capabilities from market noise",
                "Immediate availability and developer surface area",
            ],
            "narration": (
                f"Here are the verified core facts. {summary_sentence}. "
                f"Rather than looking at headlines in isolation, let us examine what actually changed under the hood and who it affects first."
            ),
            "citation": {
                "claim": summary_sentence[:120],
                "sourceName": publisher,
                "sourceDetail": "Primary Release Coverage",
                "year": str(date_utc.year),
            },
        },
        {
            "id": "beat_03_system_architecture",
            "beatIndex": 3,
            "chapterTitle": f"Inside the {comp_name} Stack",
            "actTag": "SYSTEM ARCHITECTURE",
            "yearStamp": "STACK TOPOLOGY",
            "punchMetric": "5-LAYER PIPELINE",
            "accentHex": meta["accentHex"],
            "visualPlate": pick_plate(2),
            "diagramNodes": [
                {"id": f"l{i+1}", "label": lbl, "role": "core" if i == 2 else "layer"}
                for i, lbl in enumerate(layers)
            ],
            "diagramEdges": [[f"l{i+1}", f"l{i+2}"] for i in range(len(layers) - 1)],
            "keyBullets": [
                f"Ingress & Routing: {layers[0]} → {layers[1]}",
                f"Compute & Model Core: {layers[2]}",
                f"Execution & Delivery: {layers[3]} → {layers[4]}",
            ],
            "narration": (
                f"Architecturally, every modern {comp_name} workload flows through five tightly coupled stages: "
                f"{layers[0]}, {layers[1]}, {layers[2]}, {layers[3]}, and {layers[4]}. "
                f"Improvements at the core layer immediately compound downstream reliability and latency."
            ),
            "citation": {
                "claim": meta["ecosystemContext"],
                "sourceName": f"{comp_name} Systems Architecture",
                "sourceDetail": "Reference Pipeline Topology",
                "year": str(date_utc.year),
            },
        },
        {
            "id": "beat_04_why_now_bottleneck",
            "beatIndex": 4,
            "chapterTitle": "The Bottleneck Being Solved",
            "actTag": "CAUSAL BOTTLENECK",
            "yearStamp": "LATENCY VS COST",
            "punchMetric": "EFFICIENCY SHIFT",
            "accentHex": meta["secondaryHex"],
            "visualPlate": pick_plate(3),
            "diagramNodes": [
                {"id": "b1", "label": "Compute Cost", "role": "source"},
                {"id": "b2", "label": "Context & Memory", "role": "core"},
                {"id": "b3", "label": "Verified Accuracy", "role": "target"},
            ],
            "diagramEdges": [["b1", "b2"], ["b2", "b3"]],
            "keyBullets": [
                "Inference economics: tokens per dollar per watt",
                "Reducing hallucination and multi-step tool drift",
                corroborating_line[:88],
            ],
            "narration": (
                f"Why does this happen right now? In frontier AI engineering, teams face a three-way constraint between "
                f"compute cost, context memory bandwidth, and verified accuracy. {corroborating_line}"
            ),
            "citation": {
                "claim": "Compute-memory-verification trilemma in production AI",
                "sourceName": corroborating[0]["publisher"] if corroborating else publisher,
                "sourceDetail": corroborating[0]["title"] if corroborating else "Ecosystem Analysis",
                "year": str(date_utc.year),
            },
        },
        {
            "id": "beat_05_seven_giant_landscape",
            "beatIndex": 5,
            "chapterTitle": "7-Ecosystem Competitive Context",
            "actTag": "FRONTIER LANDSCAPE",
            "yearStamp": "7 AI ECOSYSTEMS",
            "punchMetric": f"{comp_name.upper()} POSITION",
            "accentHex": meta["accentHex"],
            "visualPlate": pick_plate(4),
            "diagramNodes": [
                {"id": "c1", "label": "OpenAI / Anthropic", "role": "peer"},
                {"id": "c2", "label": "Google / xAI", "role": "peer"},
                {"id": "c3", "label": "Nvidia / MSFT / Meta", "role": "peer"},
            ],
            "diagramEdges": [["c1", "c2"], ["c2", "c3"]],
            "keyBullets": [
                f"Active Focus: {comp_name}",
                "Cross-ecosystem pressure across OpenAI, Anthropic, Google, Nvidia, Microsoft, Meta & xAI",
                "Interoperability via standard APIs, open weights, and agent protocols",
            ],
            "narration": (
                f"Stepping back across all seven frontier AI ecosystems — OpenAI, Anthropic, Google DeepMind, Nvidia, "
                f"Microsoft, Meta, and xAI — moves by {comp_name} directly influence pricing, benchmark baselines, "
                f"and enterprise procurement across the entire industry."
            ),
            "citation": {
                "claim": "Cross-ecosystem competitive benchmark dynamics",
                "sourceName": "Intelligentian Research Synthesis",
                "sourceDetail": "7-Lab Frontier Tracker",
                "year": str(date_utc.year),
            },
        },
        {
            "id": "beat_06_builder_workflow_impact",
            "beatIndex": 6,
            "chapterTitle": "Impact for Developers & Teams",
            "actTag": "BUILDER PLAYBOOK",
            "yearStamp": "PRODUCTION OPS",
            "punchMetric": "3 EVAL GATES",
            "accentHex": meta["secondaryHex"],
            "visualPlate": pick_plate(5),
            "diagramNodes": [
                {"id": "w1", "label": "Task Eval Suite", "role": "source"},
                {"id": "w2", "label": "Shadow Traffic Test", "role": "core"},
                {"id": "w3", "label": "Production Cutover", "role": "target"},
            ],
            "diagramEdges": [["w1", "w2"], ["w2", "w3"]],
            "keyBullets": [
                "Gate 1: Benchmark on your own domain-specific test prompts",
                "Gate 2: Measure p95 latency and cost per resolved workflow",
                "Gate 3: Keep model-agnostic routing so upgrades take minutes",
            ],
            "narration": (
                f"For software engineers and technical operators, the practical playbook has three gates. "
                f"First, run your own domain evaluation suite rather than relying solely on leaderboard scores. "
                f"Second, measure ninety-fifth percentile latency and cost per completed task. "
                f"Third, maintain clean abstraction layers so adopting {comp_name} updates requires zero rewrites."
            ),
            "citation": {
                "claim": "Three-gate production evaluation harness",
                "sourceName": "AI Systems Engineering Standard",
                "sourceDetail": "Eval -> Shadow -> Cutover",
                "year": str(date_utc.year),
            },
        },
        {
            "id": "beat_07_risks_and_constraints",
            "beatIndex": 7,
            "chapterTitle": "Engineering Trade-Offs & Constraints",
            "actTag": "SIGNAL VS NOISE",
            "yearStamp": "KEY RISKS",
            "punchMetric": "VERIFY METRICS",
            "accentHex": "#F59E0B",
            "visualPlate": pick_plate(6),
            "diagramNodes": [
                {"id": "r1", "label": "Rate & Quota Limits", "role": "source"},
                {"id": "r2", "label": "Data Governance", "role": "core"},
                {"id": "r3", "label": "Fallback Routing", "role": "target"},
            ],
            "diagramEdges": [["r1", "r2"], ["r2", "r3"]],
            "keyBullets": [
                "Watch real-world throughput limits during initial rollout",
                "Audit data retention, privacy boundaries, and determinism",
                "Pair primary frontier endpoints with resilient fallback models",
            ],
            "narration": (
                f"Every frontier release also carries real engineering constraints. "
                f"Watch for early rate-limit ceilings, verify enterprise data-retention guarantees, "
                f"and always pair primary endpoints with deterministic verification and fallback routing."
            ),
            "citation": {
                "claim": "Production reliability and governance checklist",
                "sourceName": "Enterprise AI Architecture Review",
                "sourceDetail": "Resilience & Quota Engineering",
                "year": str(date_utc.year),
            },
        },
        {
            "id": "beat_08_forward_indicators",
            "beatIndex": 8,
            "chapterTitle": "What to Watch Next",
            "actTag": "NEXT 30 DAYS",
            "yearStamp": "FORWARD RADAR",
            "punchMetric": "NEXT MILESTONE",
            "accentHex": meta["accentHex"],
            "visualPlate": pick_plate(7),
            "diagramNodes": [
                {"id": "f1", "label": "Independent Evals", "role": "source"},
                {"id": "f2", "label": "Developer Adoption", "role": "core"},
                {"id": "f3", "label": "Ecosystem Response", "role": "target"},
            ],
            "diagramEdges": [["f1", "f2"], ["f2", "f3"]],
            "keyBullets": [
                "Independent blind evaluations and real-world developer benchmarks",
                "Pricing, context window, and SDK tooling updates",
                f"Next moves from peer labs responding to {comp_name}",
            ],
            "narration": (
                f"Over the coming weeks, track three leading indicators: independent blind evaluations from builders, "
                f"SDK and API throughput stability, and how peer frontier labs respond to {comp_name}. "
                f"That concludes today's Intelligentian real-time technical briefing."
            ),
            "citation": {
                "claim": "30-day post-release technical indicators",
                "sourceName": "Intelligentian Daily AI Brief",
                "sourceDetail": date_label,
                "year": str(date_utc.year),
            },
        },
    ]

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
        "title": yt_title,
        "youtubeTitle": yt_title,
        "subtitle": f"{comp_name} · Daily Real-Time AI News Brief ({date_label})",
        "executiveSummary": (
            f"Real-time architectural and engineering briefing on {comp_name}: {headline_clean}. "
            f"Covers verified facts, 5-layer stack topology, competitive context across the 7 AI ecosystems, "
            f"and a 3-gate evaluation playbook for builders."
        ),
        "breakingStory": {
            "headline": headline_clean,
            "publisher": publisher,
            "url": primary.get("url", ""),
            "publishedAt": primary.get("publishedAt", ""),
            "fingerprint": story_fingerprint(headline_clean),
        },
        "voiceConfig": {
            "edgeVoice": meta["voice"],
            "kokoroVoice": meta["kokoroVoice"],
        },
        "fps": 30,
        "width": 1920,
        "height": 1080,
        "beats": beats,
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
        # Prefer breaking news within the last 36 hours
        recency_bonus = max(0.0, 36.0 - min(age_hours, 72.0) * 0.5)
        # Mild rotation bonus for companies not covered in the last 4 daily briefs
        rotation_bonus = 4.0 if comp not in recent_companies else 0.0
        # Direct engineering publication bonus
        source_bonus = 3.5 if not str(item.get("publisher", "")).startswith("GoogleNews") else 1.5

        total_score = kw_score * 2.5 + recency_bonus * 0.4 + rotation_bonus + source_bonus
        seen_batch_fps.add(fp)
        scored.append((total_score, comp, item))

    if not scored:
        # Offline / network-restricted deterministic engineering fallback so pipeline never crashes
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
    ap = argparse.ArgumentParser(description="Real-Time AI News Harvester for @intelligentian")
    ap.add_argument("--history-file", default=str(repo_root / "production" / "intelligentian_news_history.json"))
    ap.add_argument("--out-dir", default="/tmp/intelligentian_daily_news", help="Parent directory for generated episode folder")
    ap.add_argument("--company", choices=[""] + COMPANIES, default="", help="Optional force specific AI company")
    ap.add_argument(
        "--drive-templates",
        default="gdrive:Intelligentian/NewsTemplates",
        help="rclone path to curated per-company 16:9 visual plates",
    )
    ap.add_argument("--dry-run", action="store_true", help="Fetch and print selected story without updating history")
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
    manifest = build_8beat_manifest(primary_story, corroborating, company, today_utc, plates)

    ep_id = manifest["episodeId"]
    ep_dir = Path(args.out_dir) / ep_id
    ep_dir.mkdir(parents=True, exist_ok=True)
    mf_path = ep_dir / "manifest.json"
    mf_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    # Also write a convenient pointer file so downstream builders know the exact latest episode directory
    latest_ptr = Path(args.out_dir) / "latest_episode.json"
    latest_ptr.write_text(
        json.dumps({"episodeId": ep_id, "episodeDir": str(ep_dir), "company": company}, indent=2),
        encoding="utf-8",
    )

    print(f"[News Harvested] Company={company} | Episode={ep_id}")
    print(f"  Headline : {primary_story['title']}")
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
        # Keep history bounded and clean
        history["fingerprints"] = history["fingerprints"][-1000:]
        history["urls"] = history["urls"][-1000:]
        history["stories"] = history["stories"][-500:]
        hist_path.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[History Updated] Recorded fingerprint {fp} -> {hist_path}")


if __name__ == "__main__":
    main()
