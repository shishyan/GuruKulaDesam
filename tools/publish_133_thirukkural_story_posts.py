#!/usr/bin/env python3
"""
Generate 133 Story-Matched 1:1 Artworks via `gflow-headless` (2 Parallel Profile Lanes)
& Publish All 133 Thirukkural Chapters as Editorial Story Community Posts on @Guru-Kula-Desam
=================================================================================================
- Zero emojis, zero decorative Unicode, zero Panchangam/diary lines, zero comment-begging tactics.
- Clean literary Tamil editorial story structure:
    திருக்குறள் அதிகாரம் <N>: <chName> | <paal> - <iyal>
    <story_title_ta>

    குறள் <kural_num>:
    <kural_line1>
    <kural_line2>

    <story_para_1>

    <story_para_2>

    வாழ்வியல் அறம்:
    - <bullet_1>
    - <bullet_2>
    - <bullet_3>

    <closing_reflection_ta>
- Streams publishing while generating: a background publisher thread posts each chapter to `@Guru-Kula-Desam`
  as soon as its `1:1` `gflow` artwork is ready, saving `published.json` receipts per chapter for 100% crash-resumability!
"""
import concurrent.futures
import json
import os
import re
import subprocess
import sys
import threading
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, "/home/shishyan/GitHub/Shishyan/GuruKulaDesam/tools")
from publish_daily_gkd_community_post import strip_decorative_unicode, POSTS_URL, CDP_URL
import flow_autonomous_generator as fg

OUT_ROOT = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/thirukkural-133-posts")
CATALOG_PATH = OUT_ROOT / "THIRUKKURAL_133_STORIES_MASTER_CATALOG.json"
FLOW_PROJECT_ID = "f895ba67-e26c-460f-ab5e-efc4ed11bf4b"


def format_kural_story_post(item: dict) -> str:
    ch = item["ch"]
    bullets = "\n".join(f"- {b.strip().lstrip('-• ').strip()}" for b in item["moral_bullets_ta"] if b.strip())
    p1, p2 = item["story_paras_ta"][0].strip(), item["story_paras_ta"][1].strip()

    sections = [
        f"திருக்குறள் அதிகாரம் {ch}: {item['chName'].strip()} | {item['paal'].strip()} - {item['iyal'].strip()}",
        item["story_title_ta"].strip(),
        f"குறள் {item['kural_num']}:\n{item['kural_line1'].strip()}\n{item['kural_line2'].strip()}",
        p1,
        p2,
        f"வாழ்வியல் அறம்:\n{bullets}",
        item["closing_reflection_ta"].strip(),
    ]
    return strip_decorative_unicode("\n\n".join(sections)).strip()


def generate_chapter_artwork(item: dict, preferred_profile: str) -> Path:
    ch = item["ch"]
    ch_dir = OUT_ROOT / f"ch_{ch:03d}"
    ch_dir.mkdir(parents=True, exist_ok=True)
    out_file = ch_dir / f"thirukkural_ch_{ch:03d}.jpg"
    if out_file.exists() and out_file.stat().st_size > 30_000:
        return out_file

    clean_prompt = (
        item["gflow_prompt_en"]
        .replace("1:1 square composition,", "")
        .replace("1:1", "square")
        .replace("16:9", "square")
        .replace("24K", "solid gold")
    )
    env = os.environ.copy()
    env["GFLOW_CLI_LEASE_WAIT_SECONDS"] = "300"
    other_prof = "nagaraj97" if preferred_profile == "nagaraj957" else "nagaraj957"

    for attempt in range(4):
        for model_name in ["nano2", "nano-pro", "nano2-lite"]:
            for prof in [preferred_profile, other_prof]:
                for use_proj in [False, True]:
                    cmd = ["gflow-headless", "image", "t2i", "--profile", prof]
                    if use_proj:
                        cmd.extend(["--project", FLOW_PROJECT_ID])
                    cmd.extend([clean_prompt, "--aspect", "1:1", "--model", model_name, "--out-file", str(out_file)])
                    res = subprocess.run(cmd, env=env, capture_output=True, text=True)
                    if res.returncode == 0 and out_file.exists() and out_file.stat().st_size > 30_000:
                        print(f"  [Art Ch {ch:03d}/133] Ready ({out_file.stat().st_size // 1024} KB via {prof}/{model_name})", flush=True)
                        return out_file
        print(f"  [Art Ch {ch:03d}] Cooldown 20s (attempt {attempt+1}/4)...", flush=True)
        time.sleep(20)

    raise RuntimeError(f"Failed to generate artwork for Chapter {ch:03d}")


def ensure_cdp_alive():
    import urllib.request
    try:
        urllib.request.urlopen(f"{CDP_URL}/json/version", timeout=2)
        return
    except Exception:
        pass
    fg.sync_flow_chrome_profile(force=True)
    fg.ensure_flow_chrome_running(user_idx=3)


def publish_chapter_cdp(page, post_text: str, image_path: Path, expected_prefix: str) -> str:
    str_path = str(image_path.resolve())
    page.goto(POSTS_URL, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(3500)

    prev_top_href = ""
    top_el_before = page.locator('ytd-backstage-post-thread-renderer a[href*="/post/"]').first
    if top_el_before.count() > 0:
        prev_top_href = top_el_before.get_attribute("href") or ""

    placeholder = page.locator("#placeholder-area, #simplebox-placeholder").first
    if placeholder.is_visible():
        placeholder.click()
        page.wait_for_timeout(1200)

    has_dialog = page.locator("ytd-backstage-post-dialog-renderer").count() > 0
    dialog_text = page.locator("ytd-backstage-post-dialog-renderer").inner_text() if has_dialog else ""
    if not has_dialog or "குரு குல தேசம் (Guru Kula Desam)" not in dialog_text:
        page.locator("button[aria-label='Account menu']").click()
        page.wait_for_timeout(1800)
        page.locator("ytd-compact-link-renderer:has-text('Switch account')").click()
        page.wait_for_timeout(2500)
        acct = page.locator("ytd-account-item-renderer:has-text('குரு குல தேசம் (Guru Kula Desam)')").first
        acct.click()
        page.wait_for_timeout(4500)
        page.goto(POSTS_URL, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(4500)
        placeholder = page.locator("#placeholder-area, #simplebox-placeholder").first
        if placeholder.is_visible():
            placeholder.click()
            page.wait_for_timeout(1200)

    img_btn = page.locator("button:has-text('Image'):visible, button[aria-label='Add an image']:visible").first
    if img_btn.is_visible():
        img_btn.click()
    else:
        page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('ytd-backstage-post-dialog-renderer button, button'));
            const b = btns.find(el => el.offsetParent !== null && ((el.innerText || '').trim() === 'Image' || (el.getAttribute('aria-label') || '').includes('image')));
            if (b) b.click();
        }""")
    page.wait_for_timeout(1800)

    file_input = page.locator('input[type="file"][multiple]').first
    file_input.set_input_files([str_path])

    page.wait_for_timeout(5500)
    for _ in range(15):
        spinners = page.locator("ytd-backstage-image-upload-renderer tp-yt-paper-spinner-lite[active]").count()
        if spinners == 0:
            break
        page.wait_for_timeout(1000)

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

    post_btn = page.locator("ytd-backstage-post-dialog-renderer #submit-button button").first
    for _ in range(15):
        if post_btn.is_enabled():
            break
        page.wait_for_timeout(1000)

    assert post_btn.is_enabled(), "Post submit button remained disabled"
    post_btn.click()

    # Verify a BRAND-NEW post URL + matching chapter title appears at top of feed
    post_url = ""
    for _ in range(15):
        page.wait_for_timeout(1000)
        top_thread = page.locator("ytd-backstage-post-thread-renderer").first
        if top_thread.count() > 0:
            link_el = top_thread.locator('a[href*="/post/"]').first
            href = (link_el.get_attribute("href") or "") if link_el.count() > 0 else ""
            top_txt = (top_thread.locator("#content-text").first.inner_text() or "").strip() if top_thread.locator("#content-text").count() > 0 else ""
            if href and href != prev_top_href and expected_prefix in top_txt:
                post_url = f"https://www.youtube.com{href}" if href.startswith("/") else href
                break

    if not post_url:
        toast_txt = page.locator("tp-yt-paper-toast").first.inner_text().strip() if page.locator("tp-yt-paper-toast").count() > 0 else "YouTube rolling Community Post rate-limit active"
        raise RuntimeError(f"RATE_LIMITED: {toast_txt}")
    return post_url


def main():
    stories = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    assert len(stories) == 133, f"Expected 133 chapters, got {len(stories)}"
    print(f"Loaded all 133 Thirukkural chapter stories!", flush=True)

    # Pre-write all 133 formatted editorial text files
    post_texts = {}
    for item in stories:
        ch = item["ch"]
        ch_dir = OUT_ROOT / f"ch_{ch:03d}"
        ch_dir.mkdir(parents=True, exist_ok=True)
        txt = format_kural_story_post(item)
        (ch_dir / "post.txt").write_text(txt, encoding="utf-8")
        post_texts[ch] = txt

    ready_art = {}
    art_error = []

    odd_items = [s for s in stories if s["ch"] % 2 == 1]
    even_items = [s for s in stories if s["ch"] % 2 == 0]

    def art_worker(items, prof_name):
        try:
            for item in items:
                ch = item["ch"]
                receipt = OUT_ROOT / f"ch_{ch:03d}" / "published.json"
                if receipt.exists():
                    ready_art[ch] = OUT_ROOT / f"ch_{ch:03d}" / f"thirukkural_ch_{ch:03d}.jpg"
                    continue
                img = generate_chapter_artwork(item, prof_name)
                ready_art[ch] = img
        except Exception as e:
            art_error.append(str(e))
            print(f"[ART WORKER ERROR {prof_name}]: {e}", flush=True)

    t_odd = threading.Thread(target=art_worker, args=(odd_items, "nagaraj957"), daemon=True)
    t_even = threading.Thread(target=art_worker, args=(even_items, "nagaraj97"), daemon=True)
    t_odd.start()
    t_even.start()

    # Stream publishing in exact chapter order 1..133 as soon as each chapter's artwork is ready!
    ensure_cdp_alive()
    published_all = []

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.new_page()
        try:
            for item in stories:
                ch = item["ch"]
                ch_dir = OUT_ROOT / f"ch_{ch:03d}"
                receipt = ch_dir / "published.json"
                if receipt.exists():
                    info = json.loads(receipt.read_text(encoding="utf-8"))
                    published_all.append(info)
                    print(f"[Ch {ch:03d}/133] Already live -> {info['url']} ({item['chName']})", flush=True)
                    continue

                # Wait for this chapter's artwork to finish generating
                while ch not in ready_art:
                    if art_error and not t_odd.is_alive() and not t_even.is_alive():
                        raise RuntimeError(f"Artwork workers stopped with error: {art_error}")
                    time.sleep(2)

                img_path = ready_art[ch]
                expected_prefix = f"திருக்குறள் அதிகாரம் {ch}:"
                # Retry publishing up to 2 times; if YouTube rolling rate-limit is active, finish all 133 artworks cleanly and exit for drip queue
                rate_limited_stop = False
                last_err = None
                for pub_try in range(2):
                    try:
                        url = publish_chapter_cdp(page, post_texts[ch], img_path, expected_prefix)
                        info = {
                            "ch": ch,
                            "chName": item["chName"],
                            "paal": item["paal"],
                            "iyal": item["iyal"],
                            "story_title_ta": item["story_title_ta"],
                            "kural_num": item["kural_num"],
                            "url": url,
                            "published_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        }
                        receipt.write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
                        published_all.append(info)
                        print(f"[Ch {ch:03d}/133] LIVE -> {url} | அதிகாரம் {ch}: {item['chName']} ({item['story_title_ta']})", flush=True)
                        last_err = None
                        break
                    except Exception as e:
                        last_err = e
                        print(f"  [Pub Notice Ch {ch:03d} try {pub_try+1}/2] {e}", flush=True)
                        if "RATE_LIMITED" in str(e) and pub_try == 1:
                            rate_limited_stop = True
                            break
                        try:
                            page.close()
                        except Exception:
                            pass
                        ensure_cdp_alive()
                        browser = p.chromium.connect_over_cdp(CDP_URL)
                        context = browser.contexts[0]
                        page = context.new_page()
                        time.sleep(6)

                if rate_limited_stop:
                    print(f"\n[YouTube Rolling Cap Reached at Ch {ch:03d}] Waiting for artwork workers to finish all 133/133 artworks so remaining chapters auto-drip cleanly!", flush=True)
                    break

                if last_err is not None:
                    raise RuntimeError(f"Failed publishing Ch {ch:03d}: {last_err}")

                # Polite spacing between YouTube Community Posts
                time.sleep(10)
        finally:
            try:
                page.close()
            except Exception:
                pass

    print("Waiting for artwork workers to complete all 133/133 artworks...", flush=True)
    t_odd.join()
    t_even.join()

    (OUT_ROOT / "PUBLISHED_133_INDEX.json").write_text(
        json.dumps(published_all, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    subprocess.run(
        ["rclone", "copy", str(OUT_ROOT), "gdrive:GuruKulaDesam/Assets/thirukkural-133-posts/", "--transfers", "12"],
        check=False,
    )
    print(f"\n=== ALL {len(published_all)}/133 THIRUKKURAL CHAPTER STORY POSTS LIVE ===", flush=True)


if __name__ == "__main__":
    main()
