#!/usr/bin/env python3
"""
Channel Branding, Watermark, Metadata & 9-Playlist Bootstrapper for @intelligentian (`UCjVbL7GE3cHLOWRYAxZH65A`)

Features:
  1. Strictly enforces target channel ID == `UCjVbL7GE3cHLOWRYAxZH65A` across `data/credentials/token_intelligentian.json`
     and `data/credentials/tokens_intelligentian/token_*.json` — NEVER touches any other channel!
  2. Enforces STRICT ZERO-CTA invariant across channel description, keywords, and playlist descriptions.
  3. Uploads custom 2560x1440 banner via `yt.channelBanners().insert(...)` and applies:
       - `brandingSettings.image.bannerExternalUrl`
       - `brandingSettings.channel.description` (pure mission statement covering the 7 Frontier AI Ecosystems across
         Daily Real-Time AI News & Basics-to-Frontier AI Mastery)
       - `brandingSettings.channel.keywords`
       - `brandingSettings.channel.defaultLanguage = "en"` & `country = "US"`
  4. Uploads custom PNG watermark via `yt.watermarks().set(...)` when `--watermark` is supplied or auto-discovered.
  5. Idempotently audits existing playlists and creates any missing playlists across the **7 Official Company Playlists**
     + **2 Master Track Playlists**, saving canonical IDs to `production/intelligentian_playlists.json`.
  6. Optional `--set-avatar-cdp` helper using Playwright over Chrome DevTools Protocol (`http://127.0.0.1:9222` or custom
     `--cdp-url`) to apply the 800x800 profile avatar in YouTube Studio Customization when a logged-in session is present,
     or outputs clear status instructions (since YouTube Data API v3 supports banner + watermark + playlists + branding
     100% via API, while profile avatars live in Studio / Google Account UI).
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

EXPECTED_CHANNEL_ID = "UCjVbL7GE3cHLOWRYAxZH65A"
CHANNEL_HANDLE = "@intelligentian"

BANNED_CTA_PHRASES = (
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

CHANNEL_DESCRIPTION = (
    "Intelligentian is an independent engineering and research briefing network covering the 7 Frontier AI Ecosystems — "
    "OpenAI, Anthropic, Google & DeepMind, Nvidia, Microsoft, Meta, and xAI.\n\n"
    "Two Structured Tracks:\n"
    "1. Daily AI News Brief: Real-time technical breakdowns of model releases, reasoning benchmarks, compute superclusters, "
    "open-weights checkpoints, and enterprise agent architectures.\n"
    "2. Learn AI From Scratch to Frontier (L1 → L4 Curriculum): First-principles visual engineering guides taking builders "
    "from neural foundations and tokenization (L1), to API workflows and RAG systems (L2), multi-agent orchestration and "
    "evaluation harnesses (L3), and frontier distributed training and inference optimization (L4).\n\n"
    "Pure signal, empirical benchmarks, architecture diagrams, and primary technical citations."
)

CHANNEL_KEYWORDS = (
    'Intelligentian "Artificial Intelligence" "AI News" "Learn AI" OpenAI Anthropic "Google DeepMind" '
    'Gemini Claude GPT Nvidia CUDA Microsoft Copilot "Meta Llama" "xAI Grok" "AI Engineering" "AI Agents" LLM'
)

CANONICAL_PLAYLISTS = [
    {
        "key": "OPENAI",
        "title": "OpenAI · GPT, Agents & Frontier Mastery",
        "description": (
            "Technical briefings, reasoning model architectures, Responses & Agents SDK workflows, "
            "and L1 → L4 mastery across the OpenAI ecosystem."
        ),
    },
    {
        "key": "ANTHROPIC",
        "title": "Anthropic · Claude, Safety & Enterprise AI",
        "description": (
            "Claude frontier model releases, mechanistic interpretability, Model Context Protocol (MCP), "
            "computer-use agents, and L1 → L4 engineering guides."
        ),
    },
    {
        "key": "GOOGLE",
        "title": "Google & DeepMind · Gemini 4, Agents & Science",
        "description": (
            "Gemini multimodal architectures, TPUs, AlphaFold & scientific discovery, Genie world models, "
            "and L1 → L4 technical mastery across Google & DeepMind."
        ),
    },
    {
        "key": "NVIDIA",
        "title": "Nvidia · GPUs, CUDA & AI Infrastructure",
        "description": (
            "Blackwell & Rubin GPU architectures, NVLink interconnects, CUDA kernels, TensorRT-LLM inference, "
            "physical AI robotics, and L1 → L4 infrastructure engineering."
        ),
    },
    {
        "key": "MICROSOFT",
        "title": "Microsoft · Copilot, Azure & Enterprise AI",
        "description": (
            "Azure AI Foundry, Copilot studio orchestration, Phi small language models, enterprise governance, "
            "and L1 → L4 cloud AI systems engineering."
        ),
    },
    {
        "key": "META",
        "title": "Meta · Llama, Open-Source & Local AI",
        "description": (
            "Llama open-weights releases, PyTorch internals, quantization, local edge deployment, "
            "and L1 → L4 open-source AI engineering."
        ),
    },
    {
        "key": "XAI",
        "title": "xAI · Grok, Colossus Superclusters & Real-Time AI",
        "description": (
            "Grok frontier reasoning models, Colossus 100k+ GPU supercluster networking, real-time search synthesis, "
            "and L1 → L4 systems breakdowns."
        ),
    },
    {
        "key": "TRACK_NEWS",
        "title": "Daily AI News Brief · Real-Time Global Updates",
        "description": (
            "Daily real-time technical briefings covering breaking model launches, benchmark shifts, "
            "compute infrastructure, and research papers across all 7 frontier AI labs."
        ),
    },
    {
        "key": "TRACK_LEARNING",
        "title": "Learn AI From Scratch to Frontier (Complete Curriculum)",
        "description": (
            "Complete structured L1 (Foundations) → L2 (Applied Workflows) → L3 (Agentic Systems) → L4 (Frontier Architecture) "
            "curriculum across OpenAI, Anthropic, Google, Nvidia, Microsoft, Meta, and xAI."
        ),
    },
]


def assert_zero_cta(text: str, ctx: str) -> None:
    low = (text or "").lower()
    for phrase in BANNED_CTA_PHRASES:
        if phrase in low:
            raise ValueError(f"STRICT ZERO-CTA VIOLATION in {ctx}: found '{phrase}'")


def sanitize_yt_text(text: str) -> str:
    return (
        (text or "")
        .replace("->", "→")
        .replace("<=", "≤")
        .replace(">=", "≥")
        .replace("<", "under ")
        .replace(">", "over ")
    )


def get_intelligentian_clients(cred_dir: Path) -> list[tuple[str, object]]:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    candidates: list[Path] = []
    seen_keys: set[str] = set()
    raw_paths = [cred_dir / "token_intelligentian.json"]
    sub = cred_dir / "tokens_intelligentian"
    if sub.is_dir():
        raw_paths.extend(sorted(sub.glob("token_*.json")))
        raw_paths.extend(sorted(sub.glob("*.json")))

    for p in raw_paths:
        if not p.exists():
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            dedup_key = data.get("refresh_token") or str(p.resolve())
            if dedup_key in seen_keys:
                continue
            seen_keys.add(dedup_key)
            candidates.append(p)
        except Exception:
            continue

    verified_clients: list[tuple[str, object]] = []
    for tpath in candidates:
        try:
            creds = Credentials.from_authorized_user_file(str(tpath))
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                tpath.write_text(creds.to_json(), encoding="utf-8")
            yt = build("youtube", "v3", credentials=creds)
            resp = yt.channels().list(part="id,snippet", mine=True).execute()
            items = resp.get("items", [])
            if not items:
                print(f"[OAuth Skip] {tpath.name}: no YouTube channel returned.")
                continue
            ch_id = items[0]["id"]
            ch_title = items[0]["snippet"].get("title", "")
            # HARD CHANNEL ISOLATION ASSERTION
            if ch_id != EXPECTED_CHANNEL_ID:
                raise RuntimeError(
                    f"CHANNEL ISOLATION GUARD TRIGGERED on {tpath.name}: "
                    f"resolved channel '{ch_title}' ({ch_id}) != expected @intelligentian ({EXPECTED_CHANNEL_ID})!"
                )
            assert ch_id == EXPECTED_CHANNEL_ID
            print(f"[OAuth Verified] {ch_title} ({ch_id}) via {tpath.name}")
            verified_clients.append((tpath.name, yt))
        except RuntimeError:
            raise
        except Exception as exc:
            print(f"[OAuth Skip] {tpath.name}: {exc}")

    return verified_clients


def call_with_rotation(clients: list[tuple[str, object]], fn, op_name: str):
    last_exc = None
    for idx, (tname, yt) in enumerate(clients):
        try:
            return fn(yt), idx
        except Exception as exc:
            msg = str(exc)
            last_exc = exc
            if any(k in msg for k in ("quotaExceeded", "403", "429", "rateLimitExceeded")):
                print(f"[Quota Rotate] {op_name} hit limit on {tname}, rotating... ({msg[:180]})")
                continue
            raise
    raise RuntimeError(f"All {len(clients)} OAuth tokens exhausted on {op_name}: {last_exc}")


def auto_discover_branding_paths(repo_root: Path, banner_arg: str, watermark_arg: str, avatar_arg: str):
    search_dirs = [
        repo_root / "assets" / "intelligentian" / "branding",
        repo_root / "production" / "intelligentian" / "branding",
        Path("/home/shishyan/GitHub/Influenzian/Utility_Explainer_Studio/public/assets/intelligentian/branding"),
    ]

    def pick(explicit: str, patterns: tuple[str, ...]) -> Path | None:
        if explicit:
            p = Path(explicit)
            return p if p.exists() else None
        for d in search_dirs:
            if not d.is_dir():
                continue
            for pat in patterns:
                matches = sorted(d.glob(pat))
                if matches:
                    return matches[0]
        return None

    banner = pick(banner_arg, ("*banner*2560*.png", "*banner*2560*.jpg", "*banner*.png", "*banner*.jpg"))
    watermark = pick(watermark_arg, ("*watermark*.png", "*watermark*150*.png"))
    avatar = pick(avatar_arg, ("*avatar*800*.png", "*avatar*.png", "logo_800x800.png", "logo_raw.png"))
    return banner, watermark, avatar


def apply_channel_branding(
    clients: list[tuple[str, object]],
    banner_path: Path | None,
    watermark_path: Path | None,
    dry_run: bool = False,
) -> dict:
    from googleapiclient.http import MediaFileUpload

    clean_desc = sanitize_yt_text(CHANNEL_DESCRIPTION)[:990]
    assert_zero_cta(clean_desc, "channel.description")
    assert_zero_cta(CHANNEL_KEYWORDS, "channel.keywords")

    result_summary = {
        "channelId": EXPECTED_CHANNEL_ID,
        "bannerUploaded": False,
        "bannerExternalUrl": None,
        "brandingUpdated": False,
        "watermarkSet": False,
    }

    if dry_run:
        print(f"[Dry-Run] Would configure branding for {EXPECTED_CHANNEL_ID}:")
        print(f"  - Banner file: {banner_path}")
        print(f"  - Watermark file: {watermark_path}")
        print(f"  - Description ({len(clean_desc)} chars): Zero-CTA verified")
        return result_summary

    # Fetch existing channel brandingSettings first and double-assert channel_id
    ch_resp, _ = call_with_rotation(
        clients,
        lambda yt: yt.channels().list(part="id,snippet,brandingSettings", mine=True).execute(),
        "channels.list",
    )
    items = ch_resp.get("items", [])
    if not items or items[0]["id"] != EXPECTED_CHANNEL_ID:
        raise RuntimeError(f"Safety check failed: active channel is not {EXPECTED_CHANNEL_ID}")

    branding = items[0].get("brandingSettings", {})
    ch_settings = branding.get("channel", {})
    img_settings = branding.get("image", {})

    banner_url = None
    if banner_path and banner_path.exists():
        mime = "image/png" if banner_path.suffix.lower() == ".png" else "image/jpeg"
        print(f"[Banner Upload] Uploading {banner_path} ({banner_path.stat().st_size / 1024:.1f} KB)...")
        b_resp, _ = call_with_rotation(
            clients,
            lambda yt: yt.channelBanners().insert(
                body={},
                media_body=MediaFileUpload(str(banner_path), mimetype=mime, resumable=True),
            ).execute(),
            "channelBanners.insert",
        )
        banner_url = b_resp.get("url")
        if banner_url:
            img_settings["bannerExternalUrl"] = banner_url
            result_summary["bannerUploaded"] = True
            result_summary["bannerExternalUrl"] = banner_url
            print(f"[Banner Ready] bannerExternalUrl = {banner_url}")
    else:
        print("[Banner Notice] No banner image file found/supplied; updating text brandingSettings only.")

    ch_settings["description"] = clean_desc
    ch_settings["keywords"] = CHANNEL_KEYWORDS
    ch_settings["defaultLanguage"] = "en"
    ch_settings["country"] = "US"

    update_body = {
        "id": EXPECTED_CHANNEL_ID,
        "brandingSettings": {
            "channel": ch_settings,
        },
    }
    if img_settings.get("bannerExternalUrl"):
        update_body["brandingSettings"]["image"] = {"bannerExternalUrl": img_settings["bannerExternalUrl"]}

    call_with_rotation(
        clients,
        lambda yt: yt.channels().update(part="brandingSettings", body=update_body).execute(),
        "channels.update(brandingSettings)",
    )
    result_summary["brandingUpdated"] = True
    print(f"[Branding Updated] Description, keywords, defaultLanguage='en', country='US' applied to {EXPECTED_CHANNEL_ID}.")

    if watermark_path and watermark_path.exists():
        print(f"[Watermark Upload] Applying channel watermark {watermark_path}...")
        wm_body = {
            "timing": {
                "type": "offsetFromStart",
                "offsetMs": 0,
            },
            "position": {
                "type": "corner",
                "cornerPosition": "bottomRight",
            },
            "targetChannelId": EXPECTED_CHANNEL_ID,
        }
        try:
            call_with_rotation(
                clients,
                lambda yt: yt.watermarks().set(
                    channelId=EXPECTED_CHANNEL_ID,
                    body=wm_body,
                    media_body=MediaFileUpload(str(watermark_path), mimetype="image/png", chunksize=1024 * 256, resumable=True),
                ).execute(),
                "watermarks.set",
            )
            result_summary["watermarkSet"] = True
            print(f"[Watermark Active] Bottom-right watermark applied to {EXPECTED_CHANNEL_ID}.")
        except Exception as wm_exc:
            print(f"[Watermark Notice] Could not apply watermark ({wm_exc})")
    else:
        print("[Watermark Notice] No watermark PNG provided; skipping yt.watermarks().set().")

    return result_summary


def ensure_playlists(
    clients: list[tuple[str, object]],
    out_json: Path,
    privacy: str = "public",
    dry_run: bool = False,
) -> dict:
    for pl in CANONICAL_PLAYLISTS:
        assert_zero_cta(pl["title"], f"playlist.{pl['key']}.title")
        assert_zero_cta(pl["description"], f"playlist.{pl['key']}.description")

    existing_by_title: dict[str, dict] = {}
    if not dry_run:
        page_token = None
        while True:
            resp, _ = call_with_rotation(
                clients,
                lambda yt, pt=page_token: yt.playlists()
                .list(part="id,snippet,status", channelId=EXPECTED_CHANNEL_ID, maxResults=50, pageToken=pt)
                .execute(),
                "playlists.list",
            )
            for item in resp.get("items", []):
                title = item.get("snippet", {}).get("title", "").strip()
                if title and title not in existing_by_title:
                    existing_by_title[title] = {
                        "id": item["id"],
                        "title": title,
                        "privacyStatus": item.get("status", {}).get("privacyStatus", "public"),
                    }
            page_token = resp.get("nextPageToken")
            if not page_token:
                break
        print(f"[Playlist Audit] Found {len(existing_by_title)} existing playlist(s) on {EXPECTED_CHANNEL_ID}.")

    saved_playlists: dict[str, dict] = {}
    for spec in CANONICAL_PLAYLISTS:
        key = spec["key"]
        title = spec["title"]
        desc = sanitize_yt_text(spec["description"])

        if title in existing_by_title:
            pl_id = existing_by_title[title]["id"]
            print(f"  [Exists] {key:14s} -> {pl_id} ({title})")
            saved_playlists[key] = {
                "id": pl_id,
                "title": title,
                "description": desc,
                "url": f"https://www.youtube.com/playlist?list={pl_id}",
            }
            continue

        if dry_run:
            print(f"  [Dry-Run Create] {key:14s} -> {title}")
            saved_playlists[key] = {
                "id": f"DRY_RUN_{key}",
                "title": title,
                "description": desc,
                "url": "",
            }
            continue

        body = {
            "snippet": {
                "title": title,
                "description": desc,
                "defaultLanguage": "en",
            },
            "status": {
                "privacyStatus": privacy,
            },
        }
        created, _ = call_with_rotation(
            clients,
            lambda yt, b=body: yt.playlists().insert(part="snippet,status", body=b).execute(),
            f"playlists.insert({key})",
        )
        pl_id = created["id"]
        print(f"  [Created] {key:14s} -> {pl_id} ({title})")
        saved_playlists[key] = {
            "id": pl_id,
            "title": title,
            "description": desc,
            "url": f"https://www.youtube.com/playlist?list={pl_id}",
        }

    payload = {
        "channelId": EXPECTED_CHANNEL_ID,
        "channelHandle": CHANNEL_HANDLE,
        "updatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "playlists": saved_playlists,
    }
    if not dry_run:
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[Saved] Wrote {len(saved_playlists)} canonical playlist mappings -> {out_json}")
    return payload


def set_avatar_via_cdp(avatar_path: Path | None, cdp_url: str) -> bool:
    """
    Optional Playwright headless CDP helper to upload the 800x800 profile avatar in YouTube Studio
    if an authenticated Studio browser session is reachable on `cdp_url`.
    """
    if not avatar_path or not avatar_path.exists():
        print(
            f"[Avatar Status] No 800x800 avatar PNG found ({avatar_path}). "
            f"Note: YouTube Data API v3 manages banner, watermark, playlists & description 100% via API; "
            f"upload the 800x800 profile avatar in YouTube Studio -> Customization -> Picture: "
            f"https://studio.youtube.com/channel/{EXPECTED_CHANNEL_ID}/editing/images"
        )
        return False

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            f"[Avatar Status] Playwright python package not installed; skipping --set-avatar-cdp. "
            f"Avatar PNG ready at {avatar_path} -> apply at https://studio.youtube.com/channel/{EXPECTED_CHANNEL_ID}/editing/images"
        )
        return False

    studio_url = f"https://studio.youtube.com/channel/{EXPECTED_CHANNEL_ID}/editing/images"
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(cdp_url, timeout=5000)
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            page = context.new_page()
            page.goto(studio_url, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(3500)

            if "accounts.google.com" in page.url:
                print(
                    f"[Avatar CDP Notice] Studio session on {cdp_url} is not signed in. "
                    f"Avatar ready at {avatar_path} -> {studio_url}"
                )
                page.close()
                return False

            # Ensure URL belongs strictly to EXPECTED_CHANNEL_ID
            if EXPECTED_CHANNEL_ID not in page.url:
                raise RuntimeError(
                    f"CDP CHANNEL ISOLATION GUARD: Studio URL {page.url} does not match {EXPECTED_CHANNEL_ID}"
                )

            file_inputs = page.locator("input[type='file']")
            if file_inputs.count() > 0:
                file_inputs.first.set_input_files(str(avatar_path))
                page.wait_for_timeout(2000)
                done_btn = page.get_by_role("button", name="Done")
                if done_btn.count() > 0 and done_btn.first.is_visible():
                    done_btn.first.click()
                    page.wait_for_timeout(1500)
                pub_btn = page.get_by_role("button", name="Publish")
                if pub_btn.count() > 0 and pub_btn.first.is_enabled():
                    pub_btn.first.click()
                    page.wait_for_timeout(3000)
                    print(f"[Avatar Applied via CDP] Uploaded {avatar_path.name} on {studio_url}")
                    page.close()
                    return True

            print(
                f"[Avatar CDP Status] Opened {studio_url}, but direct file input was not exposed automatically. "
                f"Avatar ready at {avatar_path}."
            )
            page.close()
            return False
    except Exception as exc:
        print(
            f"[Avatar Status] CDP session not active at {cdp_url} ({exc}). "
            f"Banner + Watermark + Playlists + Description are 100% API-managed; "
            f"800x800 profile avatar ({avatar_path}) can be set once in YouTube Studio: {studio_url}"
        )
        return False


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description="Setup @intelligentian channel branding, watermark, and 9 playlists.")
    ap.add_argument("--cred-dir", default=str(repo_root / "data" / "credentials"))
    ap.add_argument("--playlists-out", default=str(repo_root / "production" / "intelligentian_playlists.json"))
    ap.add_argument("--banner", default="", help="Path to 2560x1440 channel banner PNG/JPG (< 6MB)")
    ap.add_argument("--watermark", default="", help="Path to square PNG watermark (< 1MB)")
    ap.add_argument("--avatar", default="", help="Path to 800x800 profile avatar PNG")
    ap.add_argument("--set-avatar-cdp", action="store_true", help="Attempt setting 800x800 avatar via headless Chrome CDP")
    ap.add_argument("--cdp-url", default="http://127.0.0.1:9222", help="CDP endpoint for --set-avatar-cdp")
    ap.add_argument("--skip-branding", action="store_true", help="Only create/verify the 9 canonical playlists")
    ap.add_argument("--dry-run", action="store_true", help="Validate Zero-CTA strings, paths, and OAuth without mutating")
    args = ap.parse_args()

    banner_path, watermark_path, avatar_path = auto_discover_branding_paths(
        repo_root, args.banner, args.watermark, args.avatar
    )

    # Always validate Zero-CTA invariants upfront even before checking OAuth
    assert_zero_cta(CHANNEL_DESCRIPTION, "CHANNEL_DESCRIPTION")
    assert_zero_cta(CHANNEL_KEYWORDS, "CHANNEL_KEYWORDS")
    for pl in CANONICAL_PLAYLISTS:
        assert_zero_cta(pl["title"], pl["key"])
        assert_zero_cta(pl["description"], pl["key"])

    clients = get_intelligentian_clients(Path(args.cred_dir))
    if not clients:
        if args.dry_run:
            print(
                f"[Dry-Run Ready] Zero-CTA checks passed for {CHANNEL_HANDLE} ({EXPECTED_CHANNEL_ID}). "
                f"No OAuth token present yet in {args.cred_dir} — authorize token_intelligentian.json to run live."
            )
            ensure_playlists([], Path(args.playlists_out), dry_run=True)
            return
        print(
            f"[Error] No verified OAuth token found for {CHANNEL_HANDLE} ({EXPECTED_CHANNEL_ID}) in {args.cred_dir}.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not args.skip_branding:
        apply_channel_branding(clients, banner_path, watermark_path, dry_run=args.dry_run)

    ensure_playlists(clients, Path(args.playlists_out), dry_run=args.dry_run)

    if args.set_avatar_cdp and not args.dry_run:
        set_avatar_via_cdp(avatar_path, args.cdp_url)
    else:
        print(
            f"[Profile Avatar Info] YouTube Data API v3 configures banner, watermark, description & all 9 playlists via API. "
            f"For the 800x800 profile icon ({avatar_path or 'avatar_800x800.png'}), pass --set-avatar-cdp with an open "
            f"Studio CDP session or upload once at https://studio.youtube.com/channel/{EXPECTED_CHANNEL_ID}/editing/images"
        )


if __name__ == "__main__":
    main()
