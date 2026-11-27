#!/usr/bin/env python3
"""
Multi-Project Quota-Rotating Publisher for @intelligentian (`UCjVbL7GE3cHLOWRYAxZH65A`)

Features:
  1. Hard Channel Isolation Guard: Strictly verifies `channel_id == "UCjVbL7GE3cHLOWRYAxZH65A"` across every
     token (`data/credentials/token_intelligentian.json` and `data/credentials/tokens_intelligentian/token_*.json`
     mapped from `INTELLIGENTIAN_OAUTH_TOKEN`..`_4`) — NEVER touches any other YouTube channel.
  2. Strict Zero-CTA Policy (`assert_zero_cta`): Bans `subscribe`, `hit the bell`, `smash that like`,
     `like and share`, `leave a comment`, `follow for more` across manifests, titles, tags, and descriptions,
     and sanitizes `<` / `>` so YouTube Data API v3 never rejects descriptions (`invalidDescription`).
  3. Dual Publishing Modes:
       - `--mode immediate-batch`: Publishes all ready unpublished episodes in `--local-dir` or
         `--drive-remote gdrive:Intelligentian/Queue` immediately as `public` (or `--privacy`), sets custom
         16:9 thumbnail (`< 2 MB`), inserts into BOTH the Company Playlist (`OPENAI`..`XAI`) AND the Master
         Track Playlist (`TRACK_NEWS` or `TRACK_LEARNING`), and records in
         `production/intelligentian_published_registry.json`.
       - `--mode daily-curriculum`: Deterministically selects the next unpublished Learning episode in strict
         curriculum order (`L1 -> L2 -> L3 -> L4` rotating across the 7 Frontier AI Companies:
         `OPENAI -> ANTHROPIC -> GOOGLE -> NVIDIA -> MICROSOFT -> META -> XAI`) from `--local-dir` or
         `--drive-remote gdrive:Intelligentian/CurriculumQueue` and publishes it `public`.
  4. Automatic Playlist Bootstrap Fallback: Reads `production/intelligentian_playlists.json`, and if missing or
     incomplete, queries/creates the canonical playlists on `@intelligentian` via `setup_intelligentian_channel`.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

EXPECTED_CHANNEL_ID = "UCjVbL7GE3cHLOWRYAxZH65A"
CHANNEL_HANDLE = "@intelligentian"

COMPANIES_ROTATION = [
    "OPENAI",
    "ANTHROPIC",
    "GOOGLE",
    "NVIDIA",
    "MICROSOFT",
    "META",
    "XAI",
]

LEVEL_ORDER = {"L1": 1, "L2": 2, "L3": 3, "L4": 4}

COMPANY_DISPLAY_NAMES = {
    "OPENAI": "OpenAI",
    "ANTHROPIC": "Anthropic",
    "GOOGLE": "Google & DeepMind",
    "NVIDIA": "Nvidia",
    "MICROSOFT": "Microsoft",
    "META": "Meta AI",
    "XAI": "xAI",
}

COMPANY_HASHTAGS = {
    "OPENAI": "#OpenAI #GPT #AIAgents #AIEngineering #Intelligentian",
    "ANTHROPIC": "#Anthropic #ClaudeAI #AISafety #MCP #Intelligentian",
    "GOOGLE": "#GoogleDeepMind #GeminiAI #AIResearch #TPUs #Intelligentian",
    "NVIDIA": "#Nvidia #CUDA #Blackwell #AIInfrastructure #Intelligentian",
    "MICROSOFT": "#MicrosoftAI #Copilot #AzureAI #EnterpriseAI #Intelligentian",
    "META": "#MetaAI #Llama #OpenSourceAI #LocalLLM #Intelligentian",
    "XAI": "#xAI #Grok #ColossusCluster #RealTimeAI #Intelligentian",
}

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


def assert_zero_cta(text: str, context: str) -> None:
    low = (text or "").lower()
    for phrase in BANNED_CTA_WORDS:
        if phrase in low:
            raise ValueError(f"STRICT ZERO-CTA VIOLATION in {context}: found '{phrase}'")


def sanitize_yt_text(text: str) -> str:
    return (
        (text or "")
        .replace("->", "→")
        .replace("<=", "≤")
        .replace(">=", "≥")
        .replace("<", "under ")
        .replace(">", "over ")
    )


def fmt_mmss(sec: float) -> str:
    s = max(0, int(round(sec)))
    return f"{s // 60:02d}:{s % 60:02d}"


def infer_company(manifest: dict, ep_id: str) -> str:
    explicit = str(manifest.get("company") or manifest.get("companyCategory") or manifest.get("category") or "").upper()
    if explicit in COMPANIES_ROTATION:
        return explicit
    blob = f"{ep_id} {manifest.get('title', '')} {manifest.get('subtitle', '')}".upper()
    keyword_map = [
        ("OPENAI", ("OPENAI", "CHATGPT", "GPT-", "GPT5", "GPT4", "O3", "O4", "SORA")),
        ("ANTHROPIC", ("ANTHROPIC", "CLAUDE", "SONNET", "OPUS", "HAIKU", "MCP")),
        ("GOOGLE", ("GOOGLE", "DEEPMIND", "GEMINI", "ALPHAFOLD", "GENIE", "TPU")),
        ("NVIDIA", ("NVIDIA", "CUDA", "BLACKWELL", "RUBIN", "TENSORRT", "NVLINK", "DGX")),
        ("MICROSOFT", ("MICROSOFT", "COPILOT", "AZURE", "PHI-")),
        ("META", ("META", "LLAMA", "PYTORCH")),
        ("XAI", ("XAI", "GROK", "COLOSSUS")),
    ]
    for comp, keys in keyword_map:
        if any(k in blob for k in keys):
            return comp
    return "OPENAI"


def infer_track(manifest: dict, ep_id: str, mode: str) -> str:
    explicit = str(manifest.get("track") or manifest.get("trackPlaylist") or "").upper()
    if explicit in ("TRACK_NEWS", "NEWS", "DAILY_NEWS"):
        return "TRACK_NEWS"
    if explicit in ("TRACK_LEARNING", "LEARNING", "CURRICULUM"):
        return "TRACK_LEARNING"
    upper_id = ep_id.upper()
    if mode == "daily-curriculum" or re.search(r"(^|[_\-])L[1-4]([_\-]|$)", upper_id) or manifest.get("level"):
        return "TRACK_LEARNING"
    if "NEWS" in upper_id or "BRIEF" in upper_id:
        return "TRACK_NEWS"
    return "TRACK_LEARNING" if manifest.get("curriculumLevel") else "TRACK_NEWS"


def infer_curriculum_sort_key(manifest: dict, ep_id: str) -> tuple[int, int, int, str]:
    """
    Sorts Learning episodes strictly as L1 -> L2 -> L3 -> L4, and within each level
    rotates across the 7 AI companies (`OPENAI -> ANTHROPIC -> GOOGLE -> NVIDIA -> MICROSOFT -> META -> XAI`).
    """
    lvl_str = str(manifest.get("level") or manifest.get("curriculumLevel") or "").upper()
    if lvl_str not in LEVEL_ORDER:
        m = re.search(r"(?:^|[_\-])(L[1-4])(?:[_\-]|$)", ep_id.upper())
        lvl_str = m.group(1) if m else "L1"
    lvl_rank = LEVEL_ORDER.get(lvl_str, 9)
    comp = infer_company(manifest, ep_id)
    comp_rank = COMPANIES_ROTATION.index(comp) if comp in COMPANIES_ROTATION else 99
    seq_order = int(manifest.get("curriculumOrder", manifest.get("seriesOrder", 999)))
    return (lvl_rank, comp_rank, seq_order, ep_id)


def build_intelligentian_description(manifest: dict, ep_id: str, company: str, track: str) -> str:
    title = manifest.get("youtubeTitle") or manifest.get("title") or ep_id
    subtitle = manifest.get("subtitle") or (
        f"{COMPANY_DISPLAY_NAMES.get(company, company)} · Daily Real-Time AI Technical Briefing"
        if track == "TRACK_NEWS"
        else f"{COMPANY_DISPLAY_NAMES.get(company, company)} · From Scratch to Frontier Curriculum"
    )

    chapters: list[str] = []
    citations: list[str] = []

    items = manifest.get("beats") or manifest.get("scenes") or []
    for idx, sc in enumerate(items):
        ts = fmt_mmss(sc.get("startSec", idx * 15))
        ch_title = (
            sc.get("chapterTitle")
            or sc.get("beatTitle")
            or sc.get("actTag")
            or sc.get("yearStamp")
            or f"Section {idx + 1:02d}"
        )
        chapters.append(f"{ts} {ch_title}")
        cit = sc.get("citation")
        if isinstance(cit, dict) and (cit.get("sourceName") or cit.get("claim")):
            src_name = cit.get("sourceName", "Technical Source")
            src_yr = cit.get("year", "")
            src_det = cit.get("sourceDetail") or cit.get("claim") or ""
            yr_part = f" ({src_yr})" if src_yr else ""
            citations.append(f"• [{ts}] {src_name}{yr_part} — {src_det}")

    for src in manifest.get("sources", []):
        if isinstance(src, str) and src.strip():
            citations.append(f"• {src.strip()}")
        elif isinstance(src, dict):
            lbl = src.get("title") or src.get("sourceName") or "Source"
            url = src.get("url", "")
            citations.append(f"• {lbl}" + (f": {url}" if url else ""))

    if not chapters or not chapters[0].startswith("00:00"):
        chapters.insert(0, "00:00 Executive Architecture Overview")

    summary_block = manifest.get("executiveSummary") or manifest.get("summary") or (
        f"Technical engineering breakdown covering {COMPANY_DISPLAY_NAMES.get(company, company)} architecture, "
        f"empirical benchmarks, system trade-offs, and practical implementation patterns."
    )

    hashtags = " ".join(manifest.get("hashtags", [])) or COMPANY_HASHTAGS.get(company, "#AIEngineering #Intelligentian")
    if "#AI" not in hashtags:
        hashtags = f"{hashtags} #AI #ArtificialIntelligence"

    parts = [
        f"{title}",
        f"{subtitle}",
        "",
        summary_block,
        "",
        "Chapters:",
        "\n".join(chapters),
    ]
    if citations:
        parts.extend(["", "Primary Sources & Technical References:", "\n".join(citations[:12])])
    parts.extend(["", hashtags])

    desc = sanitize_yt_text("\n".join(parts)).strip()
    assert_zero_cta(desc, f"{ep_id}.description")
    return desc[:4900]


def build_intelligentian_tags(manifest: dict, company: str, track: str) -> list[str]:
    comp_label = COMPANY_DISPLAY_NAMES.get(company, company)
    base = list(manifest.get("tags", []))
    defaults = [
        comp_label,
        f"{comp_label} AI",
        "AI News" if track == "TRACK_NEWS" else "Learn AI",
        "Artificial Intelligence",
        "AI Engineering",
        "Large Language Models",
        "AI Agents",
        "Frontier AI",
        "Intelligentian",
    ]
    out: list[str] = []
    for t in base + defaults:
        clean = sanitize_yt_text(str(t)).strip()
        if clean and clean not in out:
            assert_zero_cta(clean, f"tag:{clean}")
            out.append(clean)
    return out[:15]


def get_youtube_clients(cred_dir: Path) -> list[tuple[str, object]]:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    candidates: list[Path] = []
    seen_refresh: set[str] = set()
    raw_paths = [cred_dir / "token_intelligentian.json"]
    tok_dir = cred_dir / "tokens_intelligentian"
    if tok_dir.is_dir():
        raw_paths.extend(sorted(tok_dir.glob("token_*.json")))
        raw_paths.extend(sorted(tok_dir.glob("*.json")))

    for p in raw_paths:
        if not p.exists():
            continue
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
            key = raw.get("refresh_token") or str(p.resolve())
            if key in seen_refresh:
                continue
            seen_refresh.add(key)
            candidates.append(p)
        except Exception:
            continue

    clients: list[tuple[str, object]] = []
    for tpath in candidates:
        try:
            creds = Credentials.from_authorized_user_file(str(tpath))
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                tpath.write_text(creds.to_json(), encoding="utf-8")
            yt = build("youtube", "v3", credentials=creds)
            ch = yt.channels().list(part="id,snippet", mine=True).execute()
            items = ch.get("items", [])
            if not items:
                continue
            ch_id = items[0]["id"]
            ch_title = items[0]["snippet"].get("title", "")
            if ch_id != EXPECTED_CHANNEL_ID:
                raise RuntimeError(
                    f"CHANNEL ISOLATION GUARD TRIGGERED on {tpath.name}: "
                    f"resolved {ch_title} ({ch_id}) != expected @intelligentian ({EXPECTED_CHANNEL_ID})!"
                )
            assert ch_id == EXPECTED_CHANNEL_ID
            print(f"[OAuth Ready] {ch_title} ({ch_id}) via {tpath.name}")
            clients.append((tpath.name, yt))
        except RuntimeError:
            raise
        except Exception as exc:
            print(f"[OAuth Skip] {tpath.name}: {exc}")
    return clients


def load_or_bootstrap_playlists(playlists_path: Path, clients: list[tuple[str, object]]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    if playlists_path.exists():
        try:
            data = json.loads(playlists_path.read_text(encoding="utf-8"))
            for k, v in data.get("playlists", {}).items():
                pid = v.get("id", "") if isinstance(v, dict) else str(v)
                if pid and not pid.startswith("DRY_RUN_"):
                    mapping[k] = pid
        except Exception:
            pass

    required_keys = set(COMPANIES_ROTATION) | {"TRACK_NEWS", "TRACK_LEARNING"}
    if required_keys.issubset(mapping.keys()) or not clients:
        return mapping

    # Auto-bootstrap missing playlists idempotently
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import setup_intelligentian_channel as setup_mod

        payload = setup_mod.ensure_playlists(clients, playlists_path, dry_run=False)
        for k, v in payload.get("playlists", {}).items():
            if isinstance(v, dict) and v.get("id"):
                mapping[k] = v["id"]
    except Exception as exc:
        print(f"[Playlist Bootstrap Notice] Could not auto-sync playlists ({exc})")
    return mapping


def find_mp4(ep_dir: Path) -> Path | None:
    for pattern in ("*_1080p.mp4", "master_1080p.mp4", "*.mp4"):
        matches = sorted(ep_dir.glob(pattern))
        if matches:
            return matches[0]
    return None


def find_thumbnail(ep_dir: Path, ep_id: str) -> Path | None:
    candidates = [
        ep_dir / f"{ep_id}_thumb_16x9.jpg",
        ep_dir / "thumbnail_16x9.jpg",
        ep_dir / "poster_16x9.jpg",
        ep_dir / "thumbnail.jpg",
        ep_dir / "thumbnail_16x9.png",
    ]
    for p in candidates:
        if p.exists() and p.stat().st_size < 2 * 1024 * 1024:
            return p
    for p in sorted(ep_dir.glob("*thumb*.jpg")):
        if p.stat().st_size < 2 * 1024 * 1024:
            return p
    return None


def discover_local_episodes(local_dir: Path, published_ids: set[str]) -> list[tuple[str, dict, Path]]:
    found: list[tuple[str, dict, Path]] = []
    if not local_dir.is_dir():
        return found

    # Support either `local_dir/manifest.json` directly or `local_dir/<EPISODE_ID>/manifest.json`
    candidate_dirs = [local_dir] if (local_dir / "manifest.json").exists() else sorted(local_dir.iterdir())
    for d in candidate_dirs:
        if not d.is_dir() or not (d / "manifest.json").exists():
            continue
        mf = json.loads((d / "manifest.json").read_text(encoding="utf-8"))
        ep_id = mf.get("episodeId") or d.name
        if ep_id in published_ids:
            continue
        if find_mp4(d) is not None:
            found.append((ep_id, mf, d))
    return found


def discover_drive_episodes(remote_dir: str, cache_dir: Path, published_ids: set[str]) -> list[tuple[str, dict, Path]]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    res = subprocess.run(["rclone", "lsf", remote_dir, "--dirs-only"], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[Drive Queue Notice] '{remote_dir}' not accessible or empty ({res.stderr.strip()})")
        return []

    found: list[tuple[str, dict, Path]] = []
    for line in sorted(res.stdout.splitlines()):
        sub = line.strip().rstrip("/")
        if not sub or sub in published_ids:
            continue
        dst = cache_dir / sub
        dst.mkdir(parents=True, exist_ok=True)
        subprocess.run(["rclone", "copy", f"{remote_dir}/{sub}/manifest.json", str(dst)], check=False)
        mf_path = dst / "manifest.json"
        if not mf_path.exists():
            continue
        mf = json.loads(mf_path.read_text(encoding="utf-8"))
        ep_id = mf.get("episodeId") or sub
        if ep_id in published_ids:
            continue
        found.append((ep_id, mf, dst))
    return found


def ensure_drive_media(remote_dir: str, folder_name: str, ep_dir: Path) -> bool:
    if find_mp4(ep_dir) is not None:
        return True
    print(f"[Drive Pull] Downloading rendered 1080p package from {remote_dir}/{folder_name} ...")
    subprocess.run(["rclone", "copy", f"{remote_dir}/{folder_name}", str(ep_dir)], check=False)
    return find_mp4(ep_dir) is not None


def insert_into_playlist_idempotent(clients: list[tuple[str, object]], start_idx: int, playlist_id: str, video_id: str, label: str) -> None:
    if not playlist_id:
        return
    for offset in range(len(clients)):
        idx = (start_idx + offset) % len(clients)
        tname, yt = clients[idx]
        try:
            # Quick duplicate check in playlist (1 quota unit)
            chk = yt.playlistItems().list(part="id", playlistId=playlist_id, videoId=video_id, maxResults=1).execute()
            if chk.get("items"):
                print(f"  [Playlist Exists] {video_id} already in {label} ({playlist_id})")
                return
            yt.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id,
                        },
                    }
                },
            ).execute()
            print(f"  [Playlist Added] {video_id} -> {label} ({playlist_id}) via {tname}")
            return
        except Exception as exc:
            msg = str(exc)
            if any(k in msg for k in ("quotaExceeded", "403", "429", "rateLimitExceeded")):
                print(f"  [Playlist Rotate] {tname} quota reached on {label}, trying next token...")
                continue
            print(f"  [Playlist Notice] Could not insert {video_id} into {label} ({playlist_id}): {msg[:180]}")
            return


def upload_single_episode(
    yt,
    ep_id: str,
    manifest: dict,
    ep_dir: Path,
    company: str,
    track: str,
    privacy: str,
) -> tuple[str, bool]:
    from googleapiclient.http import MediaFileUpload

    # Validate entire manifest + metadata against Zero-CTA policy before uploading a single byte
    assert_zero_cta(json.dumps(manifest), f"{ep_id}.manifest")

    mp4_path = find_mp4(ep_dir)
    if mp4_path is None:
        raise FileNotFoundError(f"No MP4 found inside {ep_dir}")

    raw_title = sanitize_yt_text(manifest.get("youtubeTitle") or manifest.get("title") or ep_id).strip()[:98]
    assert_zero_cta(raw_title, f"{ep_id}.title")
    description = build_intelligentian_description(manifest, ep_id, company, track)
    tags = build_intelligentian_tags(manifest, company, track)

    # Category 28 = Science & Technology (or 27 = Education for curriculum)
    category_id = "27" if track == "TRACK_LEARNING" else "28"

    body = {
        "snippet": {
            "title": raw_title,
            "description": description,
            "tags": tags,
            "categoryId": category_id,
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en",
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    req = yt.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(str(mp4_path), chunksize=8 * 1024 * 1024, resumable=True),
    )
    resp = None
    while resp is None:
        _, resp = req.next_chunk()

    vid = resp["id"]
    print(f"[Published -> @intelligentian ({privacy})] {ep_id} -> https://youtu.be/{vid}")

    thumb_path = find_thumbnail(ep_dir, ep_id)
    thumb_applied = False
    if thumb_path is not None:
        mime = "image/png" if thumb_path.suffix.lower() == ".png" else "image/jpeg"
        try:
            yt.thumbnails().set(
                videoId=vid,
                media_body=MediaFileUpload(str(thumb_path), mimetype=mime),
            ).execute()
            thumb_applied = True
            print(f"  [Thumbnail Applied] {thumb_path.name} ({thumb_path.stat().st_size // 1024} KB) -> {vid}")
        except Exception as thumb_exc:
            print(f"  [Thumbnail Notice] Video {vid} is LIVE; custom thumbnail skipped: {thumb_exc}")
    else:
        print(f"  [Thumbnail Notice] No <2MB 16:9 thumbnail found in {ep_dir}")

    return vid, thumb_applied


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description="Multi-token Zero-CTA YouTube Publisher for @intelligentian")
    ap.add_argument(
        "--mode",
        choices=["immediate-batch", "daily-curriculum"],
        default="immediate-batch",
        help="Publishing mode: immediate-batch (all ready episodes) or daily-curriculum (next L1->L4 episode)",
    )
    ap.add_argument("--local-dir", default="", help="Local directory containing rendered episode subfolder(s)")
    ap.add_argument(
        "--drive-remote",
        default="",
        help="rclone remote path (defaults to gdrive:Intelligentian/Queue or gdrive:Intelligentian/CurriculumQueue)",
    )
    ap.add_argument("--cred-dir", default=str(repo_root / "data" / "credentials"))
    ap.add_argument("--playlists-file", default=str(repo_root / "production" / "intelligentian_playlists.json"))
    ap.add_argument("--registry", default=str(repo_root / "production" / "intelligentian_published_registry.json"))
    ap.add_argument("--privacy", choices=["public", "unlisted", "private"], default="public")
    ap.add_argument("--max-uploads", type=int, default=24, help="Maximum episodes to publish in immediate-batch mode")
    ap.add_argument("--only-episode", default="", help="Optional exact episodeId filter")
    ap.add_argument("--dry-run", action="store_true", help="Verify queue order, Zero-CTA, and OAuth without uploading")
    args = ap.parse_args()

    default_remote = (
        "gdrive:Intelligentian/CurriculumQueue"
        if args.mode == "daily-curriculum"
        else "gdrive:Intelligentian/Queue"
    )
    drive_remote = args.drive_remote or default_remote

    reg_path = Path(args.registry)
    reg_path.parent.mkdir(parents=True, exist_ok=True)
    registry = (
        json.loads(reg_path.read_text(encoding="utf-8"))
        if reg_path.exists()
        else {"channelId": EXPECTED_CHANNEL_ID, "channelHandle": CHANNEL_HANDLE, "published": {}}
    )
    published_ids = set(registry.get("published", {}).keys())

    use_local = bool(args.local_dir and Path(args.local_dir).exists())
    if use_local:
        candidates = discover_local_episodes(Path(args.local_dir), published_ids)
    else:
        cache_sub = "curriculum" if args.mode == "daily-curriculum" else "batch"
        candidates = discover_drive_episodes(drive_remote, Path("/tmp/intelligentian_queue") / cache_sub, published_ids)

    if args.only_episode:
        candidates = [c for c in candidates if c[0] == args.only_episode]

    if args.mode == "daily-curriculum":
        # Filter to Learning episodes (or all in CurriculumQueue) and sort L1 -> L2 -> L3 -> L4 across the 7 companies
        learning_cands = [
            c for c in candidates if infer_track(c[1], c[0], args.mode) == "TRACK_LEARNING"
        ] or candidates
        learning_cands.sort(key=lambda c: infer_curriculum_sort_key(c[1], c[0]))
        batch = learning_cands[:1]
    else:
        candidates.sort(key=lambda c: (int(c[1].get("priorityOrder", 50)), c[0]))
        batch = candidates[: max(1, args.max_uploads)]

    if not batch:
        print(f"[{args.mode}] Queue clean — no unpublished @intelligentian episodes pending.")
        return

    print(f"[{args.mode}] Selected {len(batch)} episode(s) for {CHANNEL_HANDLE} ({EXPECTED_CHANNEL_ID}):")
    for idx, (ep_id, mf, _) in enumerate(batch, 1):
        comp = infer_company(mf, ep_id)
        trk = infer_track(mf, ep_id, args.mode)
        assert_zero_cta(json.dumps(mf), ep_id)
        print(f"  {idx:02d}. {ep_id}  [Company={comp} | Track={trk} | Privacy={args.privacy}]")

    clients = get_youtube_clients(Path(args.cred_dir))
    if args.dry_run:
        print(
            f"[Dry-Run Complete] Zero-CTA verified on {len(batch)} episode(s); "
            f"verified @intelligentian OAuth clients={len(clients)}."
        )
        return

    if not clients:
        print(
            f"[OAuth Notice] No active OAuth token found for {EXPECTED_CHANNEL_ID} in {args.cred_dir}. "
            f"Episodes remain staged and ready."
        )
        return

    playlist_map = load_or_bootstrap_playlists(Path(args.playlists_file), clients)

    client_idx = 0
    uploaded_total = 0

    for ep_id, mf, ep_dir in batch:
        if not use_local and not ensure_drive_media(drive_remote, ep_dir.name, ep_dir):
            print(f"[Skip] {ep_id} media not yet available on {drive_remote}/{ep_dir.name}")
            continue

        company = infer_company(mf, ep_id)
        track = infer_track(mf, ep_id, args.mode)

        while client_idx < len(clients):
            tname, yt = clients[client_idx]
            try:
                vid, thumb_ok = upload_single_episode(yt, ep_id, mf, ep_dir, company, track, args.privacy)
                company_pl = playlist_map.get(company, "")
                track_pl = playlist_map.get(track, "")
                insert_into_playlist_idempotent(clients, client_idx, company_pl, vid, company)
                insert_into_playlist_idempotent(clients, client_idx, track_pl, vid, track)

                registry.setdefault("published", {})[ep_id] = {
                    "youtubeVideoId": vid,
                    "url": f"https://youtu.be/{vid}",
                    "title": sanitize_yt_text(mf.get("youtubeTitle") or mf.get("title") or ep_id)[:98],
                    "company": company,
                    "track": track,
                    "companyPlaylistId": company_pl,
                    "trackPlaylistId": track_pl,
                    "privacyStatus": args.privacy,
                    "channelId": EXPECTED_CHANNEL_ID,
                    "oauthTokenUsed": tname,
                    "thumbnailApplied": thumb_ok,
                    "publishedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                }
                reg_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
                uploaded_total += 1
                break
            except Exception as exc:
                msg = str(exc)
                if any(
                    k in msg
                    for k in (
                        "quotaExceeded",
                        "uploadLimitExceeded",
                        "exceeded the number of videos",
                        "403",
                        "429",
                    )
                ):
                    print(f"[Quota Rotation on {tname}] {msg[:200]}")
                    if "exceeded the number of videos" in msg:
                        print("[Channel Rolling-24h Cap Reached] Remaining episodes will publish on next cycle.")
                        client_idx = len(clients)
                        break
                    client_idx += 1
                else:
                    raise

        if client_idx >= len(clients):
            print("[All OAuth Quotas Exhausted] Remaining queued episodes preserved for next window.")
            break

    print(
        f"[Done] Published {uploaded_total}/{len(batch)} episode(s) to {CHANNEL_HANDLE} ({EXPECTED_CHANNEL_ID}); "
        f"registry total={len(registry.get('published', {}))}."
    )


if __name__ == "__main__":
    main()
