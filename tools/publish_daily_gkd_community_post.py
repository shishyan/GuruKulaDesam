#!/usr/bin/env python3
"""
Daily @Guru-Kula-Desam Editorial Community Post Publisher
=========================================================
Reads `/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life/YYYY-MM-DD/TamilDailyLife_YYYY-MM-DD_Script.md`,
distills the day's sacred Purana story, modern family reflection, and simple home/temple practice
into a clean, zero-emoji, zero-gimmick, zero-panchangam professional Tamil editorial blog post,
generates 3 context-matched 1:1 photorealistic sacred artworks via `gflow-headless`,
and publishes directly to `https://www.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q/posts`
via the local headless Chrome CDP session (`127.0.0.1:9225`).
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

CHANNEL_ID = "UCPqB1A_WzpLJec6q69BOO3Q"
POSTS_URL = f"https://www.youtube.com/channel/{CHANNEL_ID}/posts"
CDP_URL = "http://127.0.0.1:9225"
ASSETS_BASE = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life")


def strip_decorative_unicode(text: str) -> str:
    """Remove all emojis, pictographs, dingbats, and decorative symbols while preserving Tamil, ASCII, and clean punctuation."""
    cleaned = []
    for ch in text:
        cp = ord(ch)
        if ch in ("\n", "\t") or (0x20 <= cp <= 0x7E) or (0x0B80 <= cp <= 0x0BFF) or cp in (0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D):
            cleaned.append(ch)
    return "".join(cleaned)


def to_editorial_literary_tamil(script_text: str, meta: dict) -> tuple[str, list[str]]:
    """
    Use Gemini API (if GEMINI_API_KEY / GOOGLE_API_KEY is available) or clean deterministic rules
    to transform the spoken `TamilDailyLife_YYYY-MM-DD_Script.md` into a crisp, dignified,
    written literary Tamil (செந்தமிழ் / உரைநடை) editorial blog post:
    - Zero emojis or Unicode symbols (uses standard `- ` markdown dashes for bullets)
    - Zero Panchangam / date / tithi / nakshatra / diary greetings ("இன்று", "காலையில எழுந்ததும்...")
    - Zero clickbait or comment-begging tactics
    - Concise, timeless Story + Bullet-pointed Moral + timeless Spiritual Reflection.
    """
    # Check if an LLM key exists in GuruKulaDesam_Local/.env or environment
    env_vars = dict(os.environ)
    env_file = Path("/home/shishyan/GuruKulaDesam_Local/.env")
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                env_vars.setdefault(k.strip(), v.strip().strip('"').strip("'"))

    gemini_key = env_vars.get("GEMINI_API_KEY") or env_vars.get("GOOGLE_API_KEY")
    if gemini_key:
        import urllib.request
        prompt = f"""Transform the following spoken Tamil Purana storytelling script into a concise, dignified, professional Tamil editorial blog post (தூய எளிய உரைநடைத் தமிழ் — NOT colloquial spoken slang like 'கடைஞ்சாங்க/குடிச்சிட்டார்', NOT diary style, NO 'இன்று/நாளை', NO Panchangam/tithi/nakshatra/date details, NO emojis or decorative Unicode symbols, NO comment-begging/engagement bait).

Structure strictly as:
1. Clean Title Line: <புராணத் தலைப்பு> | <புராண நூல் பெயர்>
2. Two concise, vivid paragraphs narrating the sacred Purana story in dignified written Tamil prose (around 90–130 words total).
3. Section heading `வாழ்வியல் அறம்:` followed by 3 crisp bullet points starting with `- ` (ASCII hyphen + space) distilling the timeless psychological & family wisdom from the story.
4. Section heading `வழிபாட்டு மரபு:` followed by 2 crisp `- ` bullet points explaining the timeless spiritual/temple significance connected to this Purana (no daily schedule/diary commands).
5. One-sentence timeless closing reflection, followed on a new line by `சிவாயநம.`

Also return 3 English `gflow` image prompts (1:1 square, photorealistic South Indian sacred realism, zero text/UI icons) matching the 3 key visual moments of this specific Purana story.

Respond ONLY in valid JSON:
{{"post_ta": "...", "image_prompts": ["...", "...", "..."]}}

SOURCE SCRIPT:
{script_text}
"""
        body = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.3},
        }).encode("utf-8")
        for model_name in ["gemini-2.5-flash", "gemini-2.0-flash"]:
            try:
                req = urllib.request.Request(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={gemini_key}",
                    data=body,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=45) as resp:
                    res_json = json.loads(resp.read().decode("utf-8"))
                raw_txt = res_json["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(raw_txt)
                post_ta = strip_decorative_unicode(parsed["post_ta"]).strip()
                prompts = [p for p in parsed.get("image_prompts", []) if isinstance(p, str)][:3]
                if post_ta and len(prompts) >= 3:
                    return post_ta, prompts
            except Exception as e:
                print(f"Gemini {model_name} fallback notice: {e}")

    # Deterministic fallback if no API key is configured
    return build_editorial_post_fallback(script_text, meta)


def build_editorial_post_fallback(script_text: str, meta: dict) -> tuple[str, list[str]]:
    """
    Parse the canonical `TamilDailyLife_YYYY-MM-DD_Script.md` and construct a clean,
    professional editorial blog post (Story + Moral + Practice — zero Panchangam, zero diary greetings, zero clickbait).
    """
    paras = [p.strip() for p in script_text.split("\n\n") if p.strip()]

    # Filter out conversational diary greetings, Panchangam date/tithi headers, and sign-offs:
    # Usually:
    #   paras[0]: "சிவாயநம! அன்பான சகோதர, சகோதரிகளே!..." (skip diary greeting)
    #   paras[1]: Date / Tamil Month / Tithi / Nakshatra (skip panchangam)
    #   paras[2]: Story lead-in ("இந்தப் புனிதமான... கதை இருக்கு") (skip conversational bridge)
    #   paras[3..k]: Purana Story narrative ("முன்னொரு காலத்துல...")
    #   Moral paragraph: ("நம்ம குடும்ப வாழ்க்கையிலயும்..." or "இந்தக் கதை...")
    #   Transition: "சரி, நம்ம வீட்டுல இன்னைக்கு செய்ய வேண்டியதை பார்க்கலாம்."
    #   Home practice paragraph
    #   Transition: "அப்புறம், ... எங்க போனா மனசுக்கு ரொம்ப நிறைவா இருக்கும்?"
    #   Temple darshan paragraph
    #   Closing summary + tomorrow teaser + சிவாயநம

    story_paras = []
    moral_para = ""
    home_para = ""
    temple_para = ""
    closing_thought = ""

    mode = "scan"
    for p in paras:
        if p.startswith("சிவாயநம") and len(p) < 120:
            continue
        if any(k in p for k in ["நட்சத்திரமும்", "பக்ஷ", "திதியும்"]) and len(story_paras) == 0:
            continue
        if p.endswith("கதை இருக்கு.") or p.endswith("வரலாறு இருக்கு."):
            continue
        if "திரும்பவும் உங்களைப் பார்க்கிறேன்" in p:
            continue
        if "செய்ய வேண்டியதை பார்க்கலாம்" in p or "செய்ய வேண்டியதைப் பார்க்கலாம்" in p:
            mode = "home"
            continue
        if "மனசுக்கு ரொம்ப நிறைவா இருக்கும்" in p:
            mode = "temple"
            continue

        if mode == "scan":
            if "குடும்ப வாழ்க்கையிலயும்" in p or "பாடத்தைச் சொல்லுது" in p or "உண்மையைச் சொல்லுது" in p:
                moral_para = p
                mode = "after_moral"
            elif p.startswith("முன்னொரு") or len(story_paras) > 0:
                story_paras.append(p)
        elif mode == "after_moral":
            story_paras.append(p)
        elif mode == "home" and not home_para:
            home_para = p
            mode = "after_home"
        elif mode == "temple" and not temple_para:
            temple_para = p
            mode = "closing"
        elif mode == "closing" and not closing_thought:
            closing_thought = p

    # Clean conversational filler phrases into polished editorial Tamil prose
    def polish_prose(t: str) -> str:
        t = re.sub(r"நம்ம குடும்ப வாழ்க்கையிலயும் இந்தக் கதை எவ்வளவு பெரிய (உண்மையைச்|பாடத்தைச்) சொல்லுது பார்த்தீங்களா\?\s*", "", t)
        return t.strip()

    moral_clean = polish_prose(moral_para)

    title_ta = meta.get("title_ta", "").strip()
    purana_ta = meta.get("purana_source", "").strip()

    # Infer accurate title from story if STORY_METADATA has a mismatched title
    if "திருநீலகண்டர்" in script_text and "திருநீலகண்டர்" not in title_ta:
        headline = "திருநீலகண்டர் வரலாறும் பிரதோஷத் தத்துவமும் | சிவபுராணம்"
    elif title_ta and purana_ta:
        headline = f"{title_ta} | {purana_ta}"
    elif title_ta:
        headline = title_ta
    else:
        headline = "இன்றைய புராண வரலாறும் வாழ்வியல் நீதியும்"

    sections = [headline]

    if story_paras:
        sections.append("\n\n".join(story_paras))

    if moral_clean:
        sentences = [s.strip() for s in re.split(r"(?<=[.!])\s+", moral_clean) if s.strip()]
        bullets = "\n".join(f"- {s}" for s in sentences)
        sections.append(f"வாழ்வியல் அறம்:\n{bullets}")

    practice_bullets = []
    if home_para:
        hp = re.sub(r"[^.!]*நட்சத்திரம்[^.!]*[.!]\s*", "", home_para).strip()
        if hp:
            practice_bullets.append(f"- இல்லற வழிபாடு: {hp}")
    if temple_para:
        practice_bullets.append(f"- ஆலய வழிபாடு: {temple_para}")

    if practice_bullets:
        sections.append("வழிபாட்டு மரபு:\n" + "\n".join(practice_bullets))

    if closing_thought:
        sections.append(f"{closing_thought}\n\nசிவாயநம.")
    else:
        sections.append("சிவாயநம.")

    full_post = strip_decorative_unicode("\n\n".join(sections))

    # Build 3 context-specific gflow prompts from the story
    prompts = [
        f"Photorealistic South Indian sacred realism depicting the opening scene of {headline}: ancient Vedic Purana divine epic setting, warm golden temple lamp lighting, dramatic sacred atmosphere, pure artwork with zero text or UI icons",
        f"Photorealistic South Indian sacred realism depicting the divine spiritual climax of {headline}: radiant deity grace in classical Chola temple iconography, warm golden rim lighting, pure artwork with zero text or UI icons",
        f"Photorealistic South Indian sacred realism depicting serene twilight darshan and lamp worship at an ancient Chola granite temple sanctum with brass oil lamps and sacred flowers, pure artwork with zero text or UI icons",
    ]
    return full_post, prompts


def ensure_gflow_images(post_dir: Path, prompts: list[str]) -> list[Path]:
    """Ensure at least 3 1:1 gflow images exist in post_dir."""
    existing = sorted(post_dir.glob("gflow_0*.jpg")) + sorted(post_dir.glob("gflow_0*.png"))
    if len(existing) >= 3:
        return existing[:5]

    generated = []
    env = os.environ.copy()
    env["GFLOW_CLI_LEASE_WAIT_SECONDS"] = "180"
    for idx, prompt in enumerate(prompts, start=1):
        out_file = post_dir / f"gflow_{idx:02d}.jpg"
        if out_file.exists() and out_file.stat().st_size > 20_000:
            generated.append(out_file)
            continue
        for prof in ["nagaraj957", "nagaraj97"]:
            cmd = [
                "gflow-headless", "image", "t2i",
                "--profile", prof,
                prompt,
                "--aspect", "1:1",
                "--model", "nano-pro",
                "--out-file", str(out_file),
            ]
            res = subprocess.run(cmd, env=env, capture_output=True, text=True)
            if res.returncode == 0 and out_file.exists() and out_file.stat().st_size > 20_000:
                generated.append(out_file)
                break
    return generated


def ensure_headless_chrome_cdp():
    import urllib.request
    try:
        urllib.request.urlopen(f"{CDP_URL}/json/version", timeout=2)
        return
    except Exception:
        pass
    sys.path.insert(0, "/home/shishyan/GitHub/Shishyan/GuruKulaDesam/tools")
    import flow_autonomous_generator as fg
    fg.sync_flow_chrome_profile(force=True)
    fg.ensure_flow_chrome_running(user_idx=3)


def publish_via_cdp(post_text: str, image_paths: list[Path], dry_run: bool = False) -> str:
    """Publish the multi-image editorial Community Post directly via headless Chrome CDP (127.0.0.1:9225)."""
    ensure_headless_chrome_cdp()
    assert len(image_paths) >= 2, f"Need at least 2 images, got {len(image_paths)}"
    str_paths = [str(p.resolve()) for p in image_paths]

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.new_page()
        try:
            print(f"Navigating to {POSTS_URL} ...")
            page.goto(POSTS_URL, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(4000)

            # Ensure active channel is @Guru-Kula-Desam (UCPqB1A_WzpLJec6q69BOO3Q)
            # Check if Image button is visible on this channel's post box
            img_btn = page.locator("ytd-backstage-post-dialog-renderer button:has-text('Image'), #image-button button, button[aria-label*='Image']").first
            if not img_btn.is_visible():
                # Click placeholder first if collapsed
                placeholder = page.locator("#placeholder-area, #simplebox-placeholder").first
                if placeholder.is_visible():
                    placeholder.click()
                    page.wait_for_timeout(1500)

            has_dialog = page.locator("ytd-backstage-post-dialog-renderer").count() > 0
            dialog_text = page.locator("ytd-backstage-post-dialog-renderer").inner_text() if has_dialog else ""
            if not has_dialog or "குரு குல தேசம் (Guru Kula Desam)" not in dialog_text:
                print("Switching active brand account to குரு குல தேசம் (Guru Kula Desam)...")
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

            # Attach all 1:1 gflow images via <input type="file" multiple>
            file_input = page.locator('input[type="file"][multiple]').first
            print(f"Uploading {len(str_paths)} images: {[p.name for p in image_paths]} ...")
            file_input.set_input_files(str_paths)

            # Wait for all image previews to finish uploading
            page.wait_for_timeout(8000)
            for _ in range(15):
                spinners = page.locator("ytd-backstage-image-upload-renderer tp-yt-paper-spinner-lite[active]").count()
                if spinners == 0:
                    break
                page.wait_for_timeout(1500)

            # Enter editorial post text into #contenteditable-root
            editor = page.locator("ytd-backstage-post-dialog-renderer #contenteditable-root").first
            editor.click()
            page.wait_for_timeout(500)
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
            page.wait_for_timeout(2000)

            if dry_run:
                shot = "/tmp/gkd_community_post_dryrun.png"
                page.screenshot(path=shot, full_page=False)
                print(f"DRY RUN ready screenshot saved to {shot}")
                return shot

            # Click Post button
            post_btn = page.locator("ytd-backstage-post-dialog-renderer #submit-button button").first
            for _ in range(10):
                if post_btn.is_enabled():
                    break
                page.wait_for_timeout(1000)

            assert post_btn.is_enabled(), "Post submit button is still disabled after uploading images and text"
            print("Clicking Post...")
            post_btn.click()
            page.wait_for_timeout(6000)

            # Extract published post link
            post_link_el = page.locator('ytd-backstage-post-thread-renderer a[href*="/post/"]').first
            post_url = POSTS_URL
            if post_link_el.count() > 0:
                href = post_link_el.get_attribute("href") or ""
                if href.startswith("/"):
                    post_url = f"https://www.youtube.com{href}"
                elif href.startswith("http"):
                    post_url = href

            print(f"PUBLISHED_COMMUNITY_POST_URL={post_url}")
            return post_url
        finally:
            page.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default="", help="YYYY-MM-DD (defaults to today IST)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.date:
        date_str = args.date
    else:
        ist_now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=5, minutes=30)
        date_str = ist_now.strftime("%Y-%m-%d")

    day_dir = ASSETS_BASE / date_str
    script_file = day_dir / f"TamilDailyLife_{date_str}_Script.md"
    meta_file = day_dir / "STORY_METADATA.json"

    if not script_file.exists():
        subprocess.run(
            ["rclone", "copy", f"gdrive:GuruKulaDesam/Assets/tamil-daily-life/{date_str}/", str(day_dir)],
            check=False,
        )

    if not script_file.exists():
        raise FileNotFoundError(f"Missing daily script: {script_file}")

    script_text = script_file.read_text(encoding="utf-8")
    meta = json.loads(meta_file.read_text(encoding="utf-8")) if meta_file.exists() else {}

    post_dir = day_dir / "community_post"
    post_dir.mkdir(parents=True, exist_ok=True)
    published_receipt = post_dir / f"published_{date_str}.json"
    if published_receipt.exists() and not args.dry_run:
        info = json.loads(published_receipt.read_text(encoding="utf-8"))
        print(f"Already published for {date_str}: {info.get('url')} — skipping duplicate post.")
        return

    post_file = post_dir / f"editorial_post_{date_str}.txt"
    if post_file.exists() and post_file.stat().st_size > 100 and os.environ.get("USE_EXISTING_EDITORIAL") == "1":
        post_text = strip_decorative_unicode(post_file.read_text(encoding="utf-8")).strip()
        _, prompts = to_editorial_literary_tamil(script_text, meta)
    else:
        post_text, prompts = to_editorial_literary_tamil(script_text, meta)
        post_file.write_text(post_text, encoding="utf-8")
    print("=== EDITORIAL POST TEXT ===")
    print(post_text)
    print("===========================")

    images = ensure_gflow_images(post_dir, prompts)
    print(f"Ready gflow images ({len(images)}): {[p.name for p in images]}")

    url = publish_via_cdp(post_text, images, dry_run=args.dry_run)
    if not args.dry_run:
        published_receipt.write_text(
            json.dumps({"date": date_str, "url": url, "published_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}, indent=2),
            encoding="utf-8",
        )
    subprocess.run(
        ["rclone", "copy", str(post_dir), f"gdrive:GuruKulaDesam/Assets/tamil-daily-life/{date_str}/community_post/"],
        check=False,
    )
    print(f"Done: {url}")


if __name__ == "__main__":
    main()
