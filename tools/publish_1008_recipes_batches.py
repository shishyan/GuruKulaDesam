#!/usr/bin/env python3
"""
Batch-publish the 1,008 categorized South Indian Cooking Recipes to @TamilDailyLife
(`தமிழர் பண்பாடு (வாழ்வியல் நெறி) #TamilVirtues` — Channel ID: `UCDdEZ6CPCr6tIzWdDY9mzxg`)
with 2 `1:1` food photography images per post, strict `backstage/create_post` XHR + DOM
verification against YouTube's rolling-24h cap, and automatic Google Drive receipt sync.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from publish_tdl_3category_community_posts import (
    CDP_URL,
    POSTS_URL,
    ensure_cdp_browser,
    ensure_tamildailylife_account,
    get_top_post_url,
    restart_and_resync_cdp_browser,
)

OUT_ROOT = Path.home() / "GoogleDrive_GuruKulaDesam" / "Assets" / "south-indian-recipes-1008"
INDEX_JSON = OUT_ROOT / "RECIPES_1008_INDEX.json"
RECEIPTS_JSON = OUT_ROOT / "published_recipes_batches.json"
GDRIVE_REMOTE = "gdrive:GuruKulaDesam/Assets/south-indian-recipes-1008"


def existing_recipe_images(img_dir: Path) -> list[Path]:
    found = sorted(
        p for p in list(img_dir.glob("gflow_0*.jpg")) + list(img_dir.glob("gflow_0*.png"))
        if p.is_file() and p.stat().st_size > 25_000
    )
    return found[:2]


def ensure_two_images(entry: dict) -> list[Path]:
    num = entry["num"]
    title_en = entry["title_en"]
    img_dir = OUT_ROOT / "images" / f"recipe_{num:04d}"
    img_dir.mkdir(parents=True, exist_ok=True)

    ready = existing_recipe_images(img_dir)
    if len(ready) >= 2 or not shutil.which("gflow-headless"):
        return ready

    env = os.environ.copy()
    env["GFLOW_CLI_LEASE_WAIT_SECONDS"] = "300"

    prompts = [
        f"Photorealistic South Indian traditional {title_en} served hot on a fresh green banana leaf with brass vessels, warm natural morning light, appetizing authentic food photography, pure photography with zero text or UI icons",
        f"Photorealistic overhead close-up of South Indian {title_en} garnished with fresh curry leaves and traditional spices alongside brass katori bowls on a clean dark granite counter, pure food photography with zero text or UI icons",
    ]

    # Try generating both prompts in a single gflow-headless session into a temp staging dir
    if len(ready) == 0:
        with tempfile.TemporaryDirectory(prefix=f"recipe_{num:04d}_") as tmpd:
            cmd = [
                "gflow-headless", "image", "t2i",
                "--profile", "nagaraj957",
                prompts[0],
                prompts[1],
                "--aspect", "1:1",
                "--model", "nano2",
                "--out", tmpd,
            ]
            res = subprocess.run(cmd, env=env, capture_output=True, text=True)
            staged = sorted(
                p for p in Path(tmpd).iterdir()
                if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png") and p.stat().st_size > 25_000
            )
            for idx, sp in enumerate(staged[:2], start=1):
                dest = img_dir / f"gflow_{idx:02d}{sp.suffix.lower()}"
                shutil.copy2(sp, dest)

    ready = existing_recipe_images(img_dir)
    if len(ready) >= 2:
        return ready

    # Fallback: generate any missing slot individually
    for idx, prompt in enumerate(prompts, start=1):
        out_file = img_dir / f"gflow_{idx:02d}.jpg"
        if out_file.exists() and out_file.stat().st_size > 25_000:
            continue
        for model_name in ["nano2", "nano-pro"]:
            cmd = [
                "gflow-headless", "image", "t2i",
                "--profile", "nagaraj957",
                prompt,
                "--aspect", "1:1",
                "--model", model_name,
                "--out-file", str(out_file),
            ]
            res = subprocess.run(cmd, env=env, capture_output=True, text=True)
            if res.returncode == 0 and out_file.exists() and out_file.stat().st_size > 25_000:
                break

    return existing_recipe_images(img_dir)


def publish_recipe_on_page(
    page, post_text: str, image_paths: list[Path], dry_run: bool = False
) -> tuple[str | None, str | None]:
    """
    Publish a single recipe Community Post with 2 `1:1` images on `@TamilDailyLife`.
    Strictly verifies a brand-new `Ugk...` post ID via `backstage/create_post` XHR or DOM top-feed change.
    """
    ensure_tamildailylife_account(page)
    prev_top = get_top_post_url(page)

    placeholder = page.locator("#placeholder-area, #simplebox-placeholder").first
    if placeholder.count() > 0 and placeholder.is_visible():
        placeholder.click()
        page.wait_for_timeout(1000)

    img_btn = page.locator("button:has-text('Image'):visible, button[aria-label='Add an image']:visible").first
    if img_btn.count() > 0 and img_btn.is_visible():
        img_btn.click()
    else:
        page.evaluate(
            """() => {
                const btns = Array.from(document.querySelectorAll('ytd-backstage-post-dialog-renderer button, button'));
                const b = btns.find(el => el.offsetParent !== null && ((el.innerText || '').trim() === 'Image' || (el.getAttribute('aria-label') || '').includes('image')));
                if (b) b.click();
            }"""
        )
    page.wait_for_timeout(1500)

    file_input = page.locator('input[type="file"][multiple]').first
    file_input.set_input_files([str(p.resolve()) for p in image_paths])

    page.wait_for_timeout(5500)
    for _ in range(18):
        spinners = page.locator("ytd-backstage-image-upload-renderer tp-yt-paper-spinner-lite[active]").count()
        if spinners == 0:
            break
        page.wait_for_timeout(1200)

    editor = page.locator("ytd-backstage-post-dialog-renderer #contenteditable-root").first
    editor.click()
    page.wait_for_timeout(300)
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.evaluate(
        """({text}) => {
            const el = document.querySelector('ytd-backstage-post-dialog-renderer #contenteditable-root');
            el.focus();
            document.execCommand('insertText', false, text);
        }""",
        {"text": post_text},
    )
    page.wait_for_timeout(1200)

    if dry_run:
        return f"{POSTS_URL}#dry-run", None

    post_btn = page.locator("ytd-backstage-post-dialog-renderer #submit-button button").first
    for _ in range(12):
        if post_btn.is_enabled():
            break
        page.wait_for_timeout(800)

    if not post_btn.is_enabled():
        return None, "Post submit button remained disabled"

    captured_api = {"post_id": None, "err": None}

    def _on_create_resp(resp):
        if "backstage/create_post" in resp.url:
            try:
                body = resp.text()
                m = re.search(r'"postId"\s*:\s*"(Ugk[A-Za-z0-9_-]+)"', body)
                if m:
                    captured_api["post_id"] = m.group(1)
                elif "error" in body.lower() or "limit" in body.lower():
                    captured_api["err"] = body[:300]
            except Exception:
                pass

    page.on("response", _on_create_resp)
    try:
        post_btn.click()
        for _ in range(26):
            page.wait_for_timeout(600)
            if captured_api["post_id"]:
                return f"https://www.youtube.com/post/{captured_api['post_id']}", None
            if captured_api["err"]:
                return None, f"create_post API error: {captured_api['err']}"
            toast_loc = page.locator("tp-yt-paper-toast, yt-upsell-dialog-renderer")
            if toast_loc.count() > 0:
                for t_idx in range(toast_loc.count()):
                    if toast_loc.nth(t_idx).is_visible():
                        t_txt = (toast_loc.nth(t_idx).inner_text() or "").strip()
                        if any(k in t_txt.lower() for k in ("limit", "try again", "too many", "couldn't", "error")):
                            return None, f"YouTube toast: {t_txt}"
            cur_top = get_top_post_url(page)
            if cur_top and cur_top != prev_top:
                return cur_top, None
    finally:
        try:
            page.remove_listener("response", _on_create_resp)
        except Exception:
            pass

    return None, "Burst cooldown or rolling-24h rate limit on create_post"


def sync_receipts_to_gdrive() -> None:
    if not shutil.which("rclone"):
        return
    if RECEIPTS_JSON.exists():
        subprocess.run(
            ["rclone", "copyto", str(RECEIPTS_JSON), f"{GDRIVE_REMOTE}/published_recipes_batches.json"],
            check=False,
        )
    img_root = OUT_ROOT / "images"
    if img_root.exists():
        subprocess.run(
            ["rclone", "copy", str(img_root), f"{GDRIVE_REMOTE}/images", "--transfers", "8"],
            check=False,
        )


def resolve_cloud_storage_state() -> str | None:
    raw_json = os.environ.get("YT_STORAGE_STATE_JSON", "").strip()
    b64_json = os.environ.get("TAMILDAILYLIFE_YT_STORAGE_STATE_B64", "").strip()
    if not raw_json and b64_json:
        try:
            raw_json = base64.b64decode(b64_json).decode("utf-8")
        except Exception:
            raw_json = ""
    if not raw_json:
        return None
    tf = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    tf.write(raw_json)
    tf.close()
    return tf.name


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--delay-sec", type=float, default=35.0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

    if not INDEX_JSON.exists():
        print(f"Missing {INDEX_JSON}; nothing to publish.")
        return

    entries = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    receipts = json.loads(RECEIPTS_JSON.read_text(encoding="utf-8")) if RECEIPTS_JSON.exists() else {}

    in_ci = os.environ.get("GITHUB_ACTIONS") == "true"
    tmp_state_path = resolve_cloud_storage_state() if in_ci else None
    if in_ci and not tmp_state_path:
        print(
            f"Cloud runner verified {len(entries)} indexed recipes ({len(receipts)}/1008 published); "
            "no YT storage state secret configured, skipping browser post step cleanly."
        )
        return

    if not in_ci:
        ensure_cdp_browser()

    posted = 0
    with sync_playwright() as p:
        if tmp_state_path:
            browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
            ctx = browser.new_context(storage_state=tmp_state_path, viewport={"width": 1920, "height": 1080})
        else:
            browser = p.chromium.connect_over_cdp(CDP_URL)
            ctx = browser.contexts[0]
        page = ctx.new_page()
        page.set_default_timeout(30000)
        try:
            for entry in entries:
                num = entry["num"]
                if str(num) in receipts:
                    continue

                post_path = OUT_ROOT / entry["rel_path"]
                if not post_path.exists():
                    continue
                post_text = post_path.read_text(encoding="utf-8").strip()

                print(f"[Recipe #{num:04d}/1008 | {entry['title_ta']}] Preparing 2 `1:1` images...", flush=True)
                images = ensure_two_images(entry)
                if len(images) < 2:
                    print(f"  [Skip #{num:04d}] Only {len(images)} image(s) ready; need 2.", flush=True)
                    continue

                print(f"  Publishing to @TamilDailyLife with {[im.name for im in images]}...", flush=True)
                url, err = None, None
                for attempt in range(4):
                    try:
                        if not in_ci:
                            ensure_cdp_browser()
                        url, err = publish_recipe_on_page(page, post_text, images, dry_run=args.dry_run)
                        if url:
                            break
                        cooldown = 55 + (35 * attempt)
                        if attempt < 3:
                            print(f"  Cooldown retry {attempt+1}/3 in {cooldown}s ({err})...", flush=True)
                            time.sleep(cooldown)
                    except Exception as exc:
                        err = str(exc)
                        print(f"  Exception retry {attempt+1}/4: {err[:160]}", flush=True)
                        if in_ci:
                            time.sleep(5)
                            continue
                        try:
                            page.close()
                        except Exception:
                            pass
                        if "YOUTUBE_SIGNED_OUT" in err:
                            restart_and_resync_cdp_browser()
                        else:
                            ensure_cdp_browser()
                        browser = p.chromium.connect_over_cdp(CDP_URL)
                        ctx = browser.contexts[0]
                        page = ctx.new_page()
                        page.set_default_timeout(30000)
                        time.sleep(5)

                if not url:
                    print(f"  [Rate-Limit/Stop] Recipe #{num:04d} halted ({err}); saving progress cleanly.", flush=True)
                    break

                receipts[str(num)] = {
                    "num": num,
                    "category_ta": entry["category_ta"],
                    "title_ta": entry["title_ta"],
                    "title_en": entry["title_en"],
                    "url": url,
                    "images": [im.name for im in images],
                    "published_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                }
                if not args.dry_run:
                    RECEIPTS_JSON.write_text(json.dumps(receipts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

                posted += 1
                print(f"  LIVE ({posted}/{args.batch_size} this batch | {len(receipts)}/1008 total) -> {url}", flush=True)

                if posted % 5 == 0 and not args.dry_run:
                    sync_receipts_to_gdrive()

                if posted >= args.batch_size:
                    break
                time.sleep(args.delay_sec)
        finally:
            try:
                page.close()
            except Exception:
                pass
            if tmp_state_path and os.path.exists(tmp_state_path):
                os.unlink(tmp_state_path)

    if posted > 0 and not args.dry_run:
        sync_receipts_to_gdrive()
    print(f"Batch complete: {posted} recipes published ({len(receipts)}/1008 total).", flush=True)


if __name__ == "__main__":
    main()
