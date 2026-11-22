#!/usr/bin/env python3
"""
Publish all 24 Canonical Tamil Mantras (Deities, Daily Life, Life Events, Navagraha, Siddhar/Sanmarga)
to @Guru-Kula-Desam Community Posts with fresh 1:1 `gflow-headless` sacred artworks.
======================================================================================================
- Zero emojis, zero decorative Unicode, zero Panchangam/diary lines, zero comment-begging tactics.
- Clean literary Tamil editorial format:
    <Mantra Title> | <Source Tradition>
    <Category>
    தமிழ் மந்திரம்: <4-line canonical Tamil verse>
    மந்திரப் பொருள்: <meaning paragraph>
    ஓதும் முறையும் தருணமும்: `- ` bullets
    வாழ்வியல் மற்றும் ஆன்மிகப் பலன்கள்: `- ` bullets
    <Closing Blessing> + <Sign-off>
- Uses both `nagaraj957` and `nagaraj97` gflow profiles in parallel (2 workers) to generate all 24 1:1 artworks rapidly,
  and publishes each post sequentially to `https://www.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q/posts` via CDP 9225.
"""
import concurrent.futures
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, "/home/shishyan/GitHub/Shishyan/GuruKulaDesam/tools")
from publish_daily_gkd_community_post import strip_decorative_unicode, POSTS_URL, CDP_URL

MANTRAS_DIR = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-mantras")
CATALOG_PATH = MANTRAS_DIR / "TAMIL_MANTRAS_MASTER_CATALOG.json"


def format_mantra_editorial_post(m: dict) -> str:
    when_bullets = "\n".join(f"- {b.strip().lstrip('-• ').strip()}" for b in m["when_and_how_bullets_ta"] if b.strip())
    ben_bullets = "\n".join(f"- {b.strip().lstrip('-• ').strip()}" for b in m["benefits_bullets_ta"] if b.strip())

    parts = [
        f"{m['title_ta'].strip()} | {m['source_tradition_ta'].strip()}",
        f"வகைப்பாடு: {m['category_ta'].strip()}",
        f"தமிழ் மந்திரம்:\n{m['mantra_text_ta'].strip()}",
        f"மந்திரப் பொருள்:\n{m['meaning_ta'].strip()}",
        f"ஓதும் முறையும் தருணமும்:\n{when_bullets}",
        f"வாழ்வியல் மற்றும் ஆன்மிகப் பலன்கள்:\n{ben_bullets}",
        m["closing_blessing_ta"].strip(),
        m["signoff_ta"].strip(),
    ]
    raw = "\n\n".join(parts)
    # Replace em-dash if any with clean hyphen/pipe and strip any decorative unicode
    return strip_decorative_unicode(raw).strip()


def generate_single_gflow_image(idx: int, m: dict, profile: str) -> Path:
    slug_dir = MANTRAS_DIR / f"{idx:02d}_{m['slug']}"
    slug_dir.mkdir(parents=True, exist_ok=True)
    out_file = slug_dir / f"{m['slug']}.jpg"
    if out_file.exists() and out_file.stat().st_size > 30_000:
        return out_file

    env = os.environ.copy()
    env["GFLOW_CLI_LEASE_WAIT_SECONDS"] = "300"
    other_prof = "nagaraj97" if profile == "nagaraj957" else "nagaraj957"
    for model_name in ["nano-pro", "imagen4", "nano2"]:
        for prof in [profile, other_prof]:
            clean_prompt = m["gflow_prompt_en"].replace("1:1 square composition,", "").replace("1:1", "square")
            cmd = [
                "gflow-headless", "image", "t2i",
                "--profile", prof,
                "--project", "f895ba67-e26c-460f-ab5e-efc4ed11bf4b",
                clean_prompt,
                "--aspect", "1:1",
                "--model", model_name,
                "--out-file", str(out_file),
            ]
            print(f"  [Artwork #{idx:02d}] Generating ({model_name}) via {prof} -> {m['slug']}.jpg ...", flush=True)
            res = subprocess.run(cmd, env=env, capture_output=True, text=True)
            if res.returncode == 0 and out_file.exists() and out_file.stat().st_size > 30_000:
                print(f"  [Artwork #{idx:02d}] Ready ({out_file.stat().st_size // 1024} KB)", flush=True)
                return out_file
            print(f"    warn #{idx:02d} ({model_name}/{prof}): rc={res.returncode}", flush=True)
    raise RuntimeError(f"Failed to generate artwork for #{idx:02d} {m['slug']}")


def ensure_headless_chrome_cdp():
    import urllib.request
    try:
        urllib.request.urlopen(f"{CDP_URL}/json/version", timeout=2)
        return
    except Exception:
        pass
    print("Starting persistent headless Chrome on port 9225...", flush=True)
    import flow_autonomous_generator as fg
    fg.sync_flow_chrome_profile(force=True)
    fg.ensure_flow_chrome_running(user_idx=3)


def publish_single_image_post_cdp(post_text: str, image_path: Path) -> str:
    ensure_headless_chrome_cdp()
    str_path = str(image_path.resolve())
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.new_page()
        try:
            page.goto(POSTS_URL, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(4000)

            placeholder = page.locator("#placeholder-area, #simplebox-placeholder").first
            if placeholder.is_visible():
                placeholder.click()
                page.wait_for_timeout(1500)

            has_dialog = page.locator("ytd-backstage-post-dialog-renderer").count() > 0
            dialog_text = page.locator("ytd-backstage-post-dialog-renderer").inner_text() if has_dialog else ""
            if not has_dialog or ("குரு குல தேசம்" not in dialog_text and "Guru Kula Desam" not in dialog_text):
                page.goto("https://www.youtube.com/account_switcher", wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(3500)
                acct = page.locator("ytd-account-item-renderer:has-text('குரு குல தேசம்')").first
                if acct.is_visible():
                    acct.click()
                    page.wait_for_timeout(4500)
                page.goto(POSTS_URL, wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(4500)
                placeholder = page.locator("#placeholder-area, #simplebox-placeholder").first
                if placeholder.is_visible():
                    placeholder.click()
                    page.wait_for_timeout(1500)

            img_btn = page.locator("button:has-text('Image'):visible, button[aria-label='Add an image']:visible").first
            if not img_btn.is_visible():
                page.evaluate("""() => {
                    const btns = Array.from(document.querySelectorAll('ytd-backstage-post-dialog-renderer button, button'));
                    const b = btns.find(el => el.offsetParent !== null && ((el.innerText || '').trim() === 'Image' || (el.getAttribute('aria-label') || '').includes('image')));
                    if (b) b.click();
                }""")
            else:
                img_btn.click()
            page.wait_for_timeout(2000)

            file_input = page.locator('input[type="file"][multiple]').first
            file_input.set_input_files([str_path])

            page.wait_for_timeout(6500)
            for _ in range(15):
                spinners = page.locator("ytd-backstage-image-upload-renderer tp-yt-paper-spinner-lite[active]").count()
                if spinners == 0:
                    break
                page.wait_for_timeout(1200)

            editor = page.locator("ytd-backstage-post-dialog-renderer #contenteditable-root").first
            editor.click()
            page.wait_for_timeout(400)
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
            page.wait_for_timeout(1500)

            post_btn = page.locator("ytd-backstage-post-dialog-renderer #submit-button button").first
            for _ in range(12):
                if post_btn.is_enabled():
                    break
                page.wait_for_timeout(1000)

            assert post_btn.is_enabled(), "Post button disabled"
            post_btn.click()
            page.wait_for_timeout(6000)

            post_link_el = page.locator('ytd-backstage-post-thread-renderer a[href*="/post/"]').first
            post_url = POSTS_URL
            if post_link_el.count() > 0:
                href = post_link_el.get_attribute("href") or ""
                if href.startswith("/"):
                    post_url = f"https://www.youtube.com{href}"
                elif href.startswith("http"):
                    post_url = href
            return post_url
        finally:
            page.close()


def main():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    print(f"Loaded {len(catalog)} Tamil Mantras from {CATALOG_PATH}", flush=True)

def main():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    print(f"Loaded {len(catalog)} Tamil Mantras from {CATALOG_PATH}", flush=True)

    # Sequential generation + cooldown retry on WAF/rate-limit (rc=7)
    prepared = {}
    for idx, m in enumerate(catalog, 1):
        slug_dir = MANTRAS_DIR / f"{idx:02d}_{m['slug']}"
        slug_dir.mkdir(parents=True, exist_ok=True)
        post_txt = format_mantra_editorial_post(m)
        (slug_dir / "post.txt").write_text(post_txt, encoding="utf-8")
        out_file = slug_dir / f"{m['slug']}.jpg"
        if out_file.exists() and out_file.stat().st_size > 30_000:
            prepared[idx] = (post_txt, out_file)
            continue
        for attempt in range(3):
            try:
                prof = "nagaraj957" if attempt % 2 == 0 else "nagaraj97"
                img_path = generate_single_gflow_image(idx, m, prof)
                prepared[idx] = (post_txt, img_path)
                time.sleep(8)
                break
            except Exception as e:
                print(f"  Retry {attempt+1}/3 for #{idx:02d} after 25s cooldown ({e})...", flush=True)
                time.sleep(25)
        if idx not in prepared:
            raise RuntimeError(f"Could not generate artwork for #{idx:02d}")

    print(f"\nAll {len(prepared)} Tamil Mantra artworks generated! Publishing sequentially to @Guru-Kula-Desam ...", flush=True)

    published_summary = []
    for idx, m in enumerate(catalog, 1):
        slug_dir = MANTRAS_DIR / f"{idx:02d}_{m['slug']}"
        receipt = slug_dir / "published.json"
        if receipt.exists():
            info = json.loads(receipt.read_text(encoding="utf-8"))
            print(f"[{idx:02d}/24] Already live -> {info['url']} ({m['title_ta']})", flush=True)
            published_summary.append((idx, m["title_ta"], m["category_ta"], info["url"]))
            continue

        post_txt, img_path = prepared[idx]
        url = publish_single_image_post_cdp(post_txt, img_path)
        receipt.write_text(
            json.dumps({
                "index": idx,
                "slug": m["slug"],
                "title_ta": m["title_ta"],
                "category_ta": m["category_ta"],
                "url": url,
                "published_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"[{idx:02d}/24] LIVE -> {url} | {m['title_ta']}", flush=True)
        published_summary.append((idx, m["title_ta"], m["category_ta"], url))
        time.sleep(10)

    # Sync entire tamil-mantras master folder to Google Drive
    subprocess.run(
        ["rclone", "copy", str(MANTRAS_DIR), "gdrive:GuruKulaDesam/Assets/tamil-mantras/", "--transfers", "8"],
        check=False,
    )

    print("\n=== ALL 24 TAMIL MANTRAS PUBLISHED ===", flush=True)
    for idx, title, cat_ta, url in published_summary:
        print(f"{idx:02d}. {title} ({cat_ta}) -> {url}", flush=True)


if __name__ == "__main__":
    main()
