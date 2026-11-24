#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/home/shishyan/GitHub/Shishyan/GuruKulaDesam/tools/update_tamildailylife_seo.py
===============================================================================
End-to-End Channel SEO, Video Tags, Hashtags & Community Post Hashtag Updater
for @TamilDailyLife (`தமிழர் பண்பாடு (வாழ்வியல் நெறி) #TamilVirtues` — `UCDdEZ6CPCr6tIzWdDY9mzxg`).

Updates:
1. Channel Customization -> Basic Info -> Channel Description & Discovery Hashtags.
2. Channel Settings -> Channel -> Basic Info (Channel Keywords) & Upload Defaults (Default Tags).
3. All 12 Live Videos on @TamilDailyLife (`2026-11-08` through `2026-11-20`):
   - Populates full ~450-char episode-specific + channel-core YouTube Tags (fixing `tags: 0`).
   - Populates rich Tamil + English SEO Descriptions & 16 targeted Hashtags (fixing `djOaBcVurRk` 15-char description).
4. All 54-day staged video metadata (`tdl_publish_meta/desc_YYYY-MM-DD.txt` & `manifest.json`)
   and all remaining unpublished 3-category Community Posts (`2026-12-11`..`2026-12-31`).
"""

from __future__ import annotations

import json
import re
import sys
import time
from datetime import date, timedelta
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from tdl_astro_panchangam_builder import (  # noqa: E402
    build_cat1_panchangam_post,
    build_cat2_raasi_jothidam_post,
    get_daily_astro_context,
    load_story_meta,
)
from tdl_women_lifestyle_builder import build_cat3_women_lifestyle_post  # noqa: E402

CHANNEL_ID = "UCDdEZ6CPCr6tIzWdDY9mzxg"
CDP_URL = "http://127.0.0.1:9225"
ASSETS_BASE = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life")
META_DIR = ASSETS_BASE / "tdl_publish_meta"
MANIFEST_JSON_PATH = ASSETS_BASE / "TDL_3CATEGORY_COMMUNITY_POSTS_MANIFEST.json"

START_DATE = date(2026, 11, 8)
END_DATE = date(2026, 12, 31)

LIVE_VIDEOS = {
    "2026-11-08": "2C1bAaGDJKE",
    "2026-11-09": "pJUUK0lXylg",
    "2026-11-10": "AXShW9izVt8",
    "2026-11-11": "djOaBcVurRk",
    "2026-11-13": "it2EEgkjHfQ",
    "2026-11-14": "Ia7D4RJ94KM",
    "2026-11-15": "A9SDGW7fb6c",
    "2026-11-16": "ENnzXg9vuxg",
    "2026-11-17": "Izedww_NgWc",
    "2026-11-18": "O2kJx_Wqw-o",
    "2026-11-19": "iYcqEcECAZ4",
    "2026-11-20": "49Td9yK78Po",
}

CHANNEL_SEO_DESCRIPTION = (
    "தமிழர் பண்பாடு (வாழ்வியல் நெறி) | @TamilDailyLife (#TamilVirtues)\n"
    "தினசரி தமிழ் புராணக் கதைகள், ஆன்மீக வாழ்வியல் நெறி, திருக்கோயில் தரிசனம் மற்றும் மகளிர் இல்லற வழிகாட்டி!\n\n"
    "நமது சேனலின் தினசரிப் பதிவுகள்:\n"
    "- தினசரி புராணக் கதைகள் & வாழ்வியல் நீதி (சிவபுராணம், பாகவத புராணம், விஷ்ணு புராணம், கந்த புராணம் & திருக்கோயில் வரலாறு)\n"
    "- தமிழ் பஞ்சாங்கம் & மகளிர் வழிபாட்டு வழிகாட்டி (திதி, நட்சத்திரம், நல்ல நேரம் & வீட்டு பூஜை முறைகள்)\n"
    "- இன்றைய ராசி பலன்கள் & மகளிர் ஜோதிட வழிகாட்டி (12 ராசி பலன்கள், சந்திராஷ்டமம் & வாஸ்து குறிப்புகள்)\n"
    "- இல்லறம், சமையல் & மகளிர் நல வழிகாட்டி (பாரம்பரிய சமையல் குறிப்புகள், இயற்கை ஆரோக்கியம் & குடும்ப நலம்)\n\n"
    "Daily Tamil Purana Stories, Tamil Panchangam, 12-Rasi Palangal, Temple Wisdom & Traditional Women's Lifestyle Guide by Guru Kula Desam.\n"
    "வாழ்க வளமுடன். சிவாயநம!\n\n"
    "#TamilDailyLife #TamilVirtues #புராணக்கதைகள் #தமிழ்பஞ்சாங்கம் #ராசிபலன் #மகளிர்வழிகாட்டி "
    "#ஆன்மீகக்கதைகள் #TamilDevotional #TamilStories #TamilPanchangam #RasiPalan #GuruKulaDesam"
)

CHANNEL_CORE_TAGS = [
    "TamilDailyLife",
    "TamilVirtues",
    "தமிழர் பண்பாடு",
    "வாழ்வியல் நெறி",
    "புராணக் கதைகள்",
    "தமிழ் பஞ்சாங்கம்",
    "இன்றைய ராசி பலன்",
    "மகளிர் வழிகாட்டி",
    "ஆன்மீகக் கதைகள்",
    "சமையல் குறிப்புகள்",
    "Tamil Purana Stories",
    "Tamil Panchangam",
    "Rasi Palan Tamil",
    "Tamil Devotional",
    "Tamil Stories",
    "மகளிர் நலம்",
    "குடும்ப நலம்",
    "தமிழ் ஜோதிடம்",
    "வாஸ்து குறிப்புகள்",
    "Guru Kula Desam",
    "தமிழ் கதைகள்",
]


def detect_episode_specific_tags_and_hashtags(title_ta: str, purana_ta: str, summary_ta: str, m_ta: str) -> tuple[list[str], list[str]]:
    text = f"{title_ta} {purana_ta} {summary_ta}"
    ep_tags: list[str] = []
    ep_hashes: list[str] = []

    # Clean story title root
    clean_title = re.sub(r"[^0-9A-Za-z\u0B80-\u0BFF\s]", " ", title_ta).split()
    if clean_title:
        short_phrase = " ".join(clean_title[:2]).strip()
        if len(short_phrase) >= 4:
            ep_tags.append(short_phrase)

    if purana_ta:
        ep_tags.append(purana_ta)
        h_purana = "#" + re.sub(r"\s+", "", purana_ta)
        ep_hashes.append(h_purana)

    if m_ta == "ஐப்பசி":
        ep_tags.extend(["ஐப்பசி மாதம்", "Aippasi"])
        ep_hashes.append("#ஐப்பசி")
    elif m_ta == "கார்த்திகை":
        ep_tags.extend(["கார்த்திகை தீபம்", "Karthigai Deepam"])
        ep_hashes.append("#கார்த்திகை")
    elif m_ta == "மார்கழி":
        ep_tags.extend(["மார்கழி வழிபாடு", "Margazhi"])
        ep_hashes.append("#மார்கழி")

    if any(k in text for k in ["சிவ", "தட்சிணாமூர்த்தி", "அர்த்த", "நடராஜ", "சங்கர", "லிங்க"]):
        ep_tags.extend(["சிவபுராணம்", "Shiva Purana Tamil", "Om Namah Shivaya"])
        ep_hashes.extend(["#சிவபுராணம்", "#ShivaPurana"])
    if any(k in text for k in ["விஷ்ணு", "கிருஷ்ண", "நரகாசுர", "வாமன", "மத்ஸ்ய", "வராக", "பரசுராம", "கல்கி", "கோவர்த்தன", "திருமகள்", "லட்சுமி"]):
        ep_tags.extend(["பாகவத புராணம்", "பெருமாள் வழிபாடு", "Vishnu Purana Tamil"])
        ep_hashes.extend(["#பாகவதபுராணம்", "#Perumal"])
    if any(k in text for k in ["முருக", "கந்த", "சஷ்டி", "வள்ளி", "தெய்வானை", "வேல்"]):
        ep_tags.extend(["கந்த புராணம்", "முருகன் வழிபாடு", "Kanda Sashti"])
        ep_hashes.extend(["#கந்தபுராணம்", "#Murugan"])
    if any(k in text for k in ["அம்மன்", "சக்தி", "பார்வதி", "காளி", "துர்க்கை", "லலிதா"]):
        ep_tags.extend(["அம்மன் வழிபாடு", "Devi Mahatmyam Tamil"])
        ep_hashes.extend(["#அம்மன்வழிபாடு", "#Sakthi"])

    return ep_tags, ep_hashes[:4]


def fit_youtube_tags(specific_tags: list[str], core_tags: list[str] = CHANNEL_CORE_TAGS, max_chars: int = 455) -> list[str]:
    final: list[str] = []
    seen: set[str] = set()
    total = 0
    for raw in specific_tags + core_tags:
        t = raw.replace("<", "").replace(">", "").replace('"', "").strip()
        if not t or t.lower() in seen:
            continue
        cost = len(t) + (3 if " " in t else 1)
        if total + cost > max_chars:
            continue
        final.append(t)
        seen.add(t.lower())
        total += cost
    return final


def build_episode_seo_package(ds: str) -> dict:
    ctx = get_daily_astro_context(ds)
    sm = load_story_meta(ds)

    title_ta = sm.get("title_ta", "புராணக் கதை").strip()
    purana_ta = sm.get("purana_source", "புராணம்").strip()
    summary_ta = sm.get("story_summary_ta", "").strip()
    moral_ta = sm.get("moral_and_action_ta", "").strip()
    temple_ta = sm.get("temple_where_to_go_ta", "அருகிலுள்ள திருக்கோயில்").strip()

    ep_tags, ep_hashes = detect_episode_specific_tags_and_hashtags(title_ta, purana_ta, summary_ta, ctx["m_ta"])
    tags = fit_youtube_tags(ep_tags, CHANNEL_CORE_TAGS)

    core_hashtags = [
        "#TamilDailyLife",
        "#TamilVirtues",
        "#புராணக்கதைகள்",
        "#தமிழ்பஞ்சாங்கம்",
        "#ராசிபலன்",
        "#மகளிர்வழிகாட்டி",
        "#ஆன்மீகக்கதைகள்",
        "#TamilDevotional",
        "#TamilStories",
        "#TamilPanchangam",
        "#RasiPalan",
        "#GuruKulaDesam",
    ]
    all_hashtags: list[str] = []
    for h in ep_hashes + core_hashtags:
        if h not in all_hashtags:
            all_hashtags.append(h)
    hashtag_line = " ".join(all_hashtags[:15])

    tithi_label = f"{ctx['paksha_ta']} {ctx['tithi_ta']}".strip()
    wd_ext = ctx.get("wd_ext") or {}
    home_pooja = wd_ext.get("deity_ta", "குலதெய்வம் மற்றும் இஷ்ட தெய்வ வழிபாடு")

    desc_lines = [
        f"{ctx['greg_date_ta']} ({ctx['m_ta']} {ctx['tamil_day']}, {ctx['wd_ta']}) — {tithi_label} & {ctx['nak_ta']} நட்சத்திர சிறப்புப் புராண வரலாறு: {title_ta} ({purana_ta})!",
        "",
        f"புராணக் கதைச் சுருக்கம்:",
        f"{summary_ta}",
        "",
        f"வாழ்வியல் நீதி & குடும்ப நலம்:",
        f"{moral_ta}",
        "",
        f"இன்றைய தமிழ் பஞ்சாங்கம் & வழிபாட்டு வழிகாட்டி:",
        f"- நாள்: {ctx['greg_date_ta']} ({ctx['m_ta']} {ctx['tamil_day']}, {ctx['wd_ta']})",
        f"- திதி: {ctx['tithi_span_ta']}",
        f"- நட்சத்திரம்: {ctx['nak_span_ta']} (சந்திர ராசி: {ctx['chandra_rasi_ta']})",
        f"- நல்ல நேரம்: {ctx['nalla_neram_ta']}",
        f"- சிறப்பு வழிபாடு: {home_pooja}",
        f"- ஆலய தரிசனம்: {temple_ta}",
        "",
        "தமிழர் பண்பாடு (வாழ்வியல் நெறி) | @TamilDailyLife (#TamilVirtues):",
        "தினசரி தமிழ் புராணக் கதைகள், தமிழ் பஞ்சாங்கம், பன்னிரு ராசி பலன்கள், வாஸ்து மற்றும் மகளிர் இல்லற சமையல் நல வழிகாட்டி. "
        "Daily Tamil Purana Moral Stories, Authentic Tamil Panchangam, 12-Rasi Astrology & Traditional Tamil Family Wisdom by Guru Kula Desam.",
        "",
        "வாழ்க வளமுடன். சிவாயநம!",
        "",
        hashtag_line,
    ]
    desc = "\n".join(desc_lines).replace("<", "").replace(">", "").strip()

    default_title = f"{title_ta} | {purana_ta} | {ctx['greg_date_ta']} | @TamilDailyLife"
    if len(default_title) > 98:
        default_title = f"{title_ta} | {purana_ta} | @TamilDailyLife"[:98]

    return {
        "date": ds,
        "title": default_title,
        "description": desc,
        "tags": tags,
        "hashtags": all_hashtags[:15],
    }


def stage_all_54_days_metadata_and_unpublished_posts() -> dict[str, dict]:
    META_DIR.mkdir(parents=True, exist_ok=True)
    manifest_file = META_DIR / "manifest.json"
    existing_manifest = json.loads(manifest_file.read_text(encoding="utf-8")) if manifest_file.exists() else {}

    comm_manifest = json.loads(MANIFEST_JSON_PATH.read_text(encoding="utf-8")) if MANIFEST_JSON_PATH.exists() else {"days": {}}
    published_days = comm_manifest.get("days", {})

    packages: dict[str, dict] = {}
    refreshed_comm_posts = 0

    total_days = (END_DATE - START_DATE).days + 1
    for i in range(total_days):
        ds = (START_DATE + timedelta(days=i)).isoformat()
        pkg = build_episode_seo_package(ds)
        # Preserve custom title if already in manifest
        if ds in existing_manifest and existing_manifest[ds].get("title"):
            pkg["title"] = existing_manifest[ds]["title"]
        existing_manifest[ds] = {
            "title": pkg["title"],
            "tags": pkg["tags"],
            "hashtags": pkg["hashtags"],
        }
        (META_DIR / f"desc_{ds}.txt").write_text(pkg["description"], encoding="utf-8")
        (META_DIR / f"tags_{ds}.json").write_text(json.dumps(pkg["tags"], ensure_ascii=False, indent=2), encoding="utf-8")
        packages[ds] = pkg

        # Refresh any unpublished Community Post text files on disk with the new hashtags
        day_comm_dir = ASSETS_BASE / ds / "tdl_community_posts"
        day_comm_dir.mkdir(parents=True, exist_ok=True)
        day_pub_info = published_days.get(ds, {})
        astro_ctx = get_daily_astro_context(ds)
        meta = load_story_meta(ds)

        cat_builders = [
            ("cat1_panchangam", day_comm_dir / f"cat1_panchangam_{ds}.txt", lambda: build_cat1_panchangam_post(ds, meta)),
            ("cat2_raasi_palangal", day_comm_dir / f"cat2_raasi_palangal_{ds}.txt", lambda: build_cat2_raasi_jothidam_post(ds)),
            ("cat3_magalir_illaram", day_comm_dir / f"cat3_magalir_illaram_{ds}.txt", lambda: build_cat3_women_lifestyle_post(ds, astro_ctx.get("header_date_ta"))),
        ]
        for cat_key, fpath, builder_fn in cat_builders:
            is_live = bool(day_pub_info.get(cat_key, {}).get("url"))
            if not is_live or not fpath.exists():
                fpath.write_text(builder_fn(), encoding="utf-8")
                if not is_live:
                    refreshed_comm_posts += 1

    manifest_file.write_text(json.dumps(existing_manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[Staged] 54-day video SEO descriptions & tags in {META_DIR} + refreshed {refreshed_comm_posts} queued Community Posts.")
    return packages


def dismiss_skip_banner(page) -> None:
    skip = page.locator("a:has-text('SKIP TO YOUTUBE STUDIO'), button:has-text('SKIP TO YOUTUBE STUDIO')")
    if skip.count() > 0 and skip.first.is_visible():
        skip.first.click()
        page.wait_for_timeout(4000)


def update_channel_profile_and_settings(page) -> None:
    profile_url = f"https://studio.youtube.com/channel/{CHANNEL_ID}/editing/profile?authuser=0"
    print(f"[Channel SEO] Navigating to {profile_url} ...")
    page.goto(profile_url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(5000)
    dismiss_skip_banner(page)

    # 1. Update Channel Description in Customization -> Profile
    desc_box = page.locator("div#textbox[aria-label*='Tell viewers about your channel']").first
    if desc_box.count() > 0 and desc_box.is_visible():
        desc_box.click()
        page.wait_for_timeout(300)
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        desc_box.fill(CHANNEL_SEO_DESCRIPTION)
        page.wait_for_timeout(1200)
        pub_btn = page.locator("ytcp-button#publish-button").first
        if pub_btn.count() > 0 and not pub_btn.get_attribute("disabled"):
            pub_btn.click()
            page.wait_for_timeout(3500)
            print("[Channel SEO] Published updated Channel Description & Hashtags!")
        else:
            print("[Channel SEO] Channel Description already up to date (Publish button not needed).")

    # 2. Update Channel Keywords & Upload Defaults in Settings Modal
    settings_btn = page.locator("#settings-item, tp-yt-paper-icon-item#settings-item").first
    if settings_btn.count() > 0:
        settings_btn.click()
        page.wait_for_timeout(2500)

        # Click 'Channel' tab in Settings dialog
        page.evaluate(
            """() => {
                const items = Array.from(document.querySelectorAll('ytcp-settings-dialog li, ytcp-settings-dialog tp-yt-paper-item'));
                const ch = items.find(el => (el.innerText || '').trim() === 'Channel');
                if (ch) ch.click();
            }"""
        )
        page.wait_for_timeout(2000)

        # Clear existing chips and enter CHANNEL_CORE_TAGS
        kw_input = page.locator("ytcp-settings-dialog ytcp-chip-bar input#text-input").first
        if kw_input.count() > 0 and kw_input.is_visible():
            kw_input.click()
            page.wait_for_timeout(300)
            for _ in range(30):
                page.keyboard.press("Backspace")
            kw_csv = ", ".join(CHANNEL_CORE_TAGS)
            kw_input.fill(kw_csv)
            page.keyboard.press("Enter")
            page.wait_for_timeout(1200)
            print(f"[Channel SEO] Set {len(CHANNEL_CORE_TAGS)} Channel Keywords ({len(kw_csv)} chars).")

        # Click 'Upload defaults' tab in Settings dialog
        page.evaluate(
            """() => {
                const items = Array.from(document.querySelectorAll('ytcp-settings-dialog li, ytcp-settings-dialog tp-yt-paper-item'));
                const ud = items.find(el => (el.innerText || '').trim() === 'Upload defaults');
                if (ud) ud.click();
            }"""
        )
        page.wait_for_timeout(2000)

        ud_tags_input = page.locator("ytcp-settings-dialog ytcp-form-input-container#tags-container input#text-input").first
        if ud_tags_input.count() > 0 and ud_tags_input.is_visible():
            ud_tags_input.click()
            page.wait_for_timeout(300)
            for _ in range(30):
                page.keyboard.press("Backspace")
            ud_tags_input.fill(", ".join(CHANNEL_CORE_TAGS))
            page.keyboard.press("Enter")
            page.wait_for_timeout(1200)
            print(f"[Channel SEO] Set {len(CHANNEL_CORE_TAGS)} Upload Default Tags.")

        save_btn = page.locator("ytcp-settings-dialog ytcp-button#save-button").first
        if save_btn.count() > 0 and not save_btn.get_attribute("disabled"):
            save_btn.click()
            page.wait_for_timeout(3500)
            print("[Channel SEO] Saved Settings (Channel Keywords + Upload Defaults)!")
        else:
            close_btn = page.locator("ytcp-settings-dialog ytcp-button#close-button, ytcp-settings-dialog ytcp-button#cancel-button").first
            if close_btn.count() > 0:
                close_btn.click()
                page.wait_for_timeout(1000)


def update_all_12_live_videos(page, packages: dict[str, dict]) -> int:
    updated = 0
    for ds, vid in sorted(LIVE_VIDEOS.items()):
        pkg = packages[ds]
        edit_url = f"https://studio.youtube.com/video/{vid}/edit?authuser=0"
        print(f"[Video SEO | {ds} | {vid}] Opening {edit_url} ...")
        page.goto(edit_url, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(4500)
        dismiss_skip_banner(page)

        # Wait for description textbox
        desc_box = page.locator("ytcp-video-description #textbox, #description-textarea #textbox").first
        try:
            desc_box.wait_for(state="visible", timeout=15000)
        except Exception as e:
            print(f"  [WARN] Could not load edit form for {vid}: {e}")
            continue

        # 1. Update Description & Hashtags
        desc_box.click()
        page.wait_for_timeout(300)
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        desc_box.fill(pkg["description"])
        page.wait_for_timeout(800)

        # 2. Expand 'Show more' and populate Tags
        toggle_btn = page.locator("ytcp-button#toggle-button").first
        if toggle_btn.count() > 0 and toggle_btn.is_visible():
            t_txt = (toggle_btn.inner_text() or "").strip().lower()
            if "more" in t_txt:
                toggle_btn.click()
                page.wait_for_timeout(1200)

        tags_input = page.locator("ytcp-form-input-container#tags-container input#text-input, input[aria-label='Tags']").first
        if tags_input.count() > 0 and tags_input.is_visible():
            tags_input.scroll_into_view_if_needed()
            tags_input.click()
            page.wait_for_timeout(300)
            for _ in range(30):
                page.keyboard.press("Backspace")
            tags_csv = ", ".join(pkg["tags"])
            tags_input.fill(tags_csv)
            page.keyboard.press("Enter")
            page.wait_for_timeout(1000)

        # 3. Click Save
        save_btn = page.locator("ytcp-button#save").first
        for _ in range(10):
            if save_btn.count() > 0 and save_btn.get_attribute("disabled") is None:
                break
            page.wait_for_timeout(500)

        if save_btn.count() > 0 and save_btn.get_attribute("disabled") is None:
            save_btn.click()
            page.wait_for_timeout(3500)
            print(f"  [SAVED] {ds} ({vid}) -> desc={len(pkg['description'])} chars, tags={len(pkg['tags'])} ({len(', '.join(pkg['tags']))} chars)")
            updated += 1
        else:
            print(f"  [INFO] {ds} ({vid}) -> Save button disabled (already matching)")
            updated += 1

    return updated


def main() -> None:
    packages = stage_all_54_days_metadata_and_unpublished_posts()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL, timeout=20000)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        try:
            update_channel_profile_and_settings(page)
            updated_count = update_all_12_live_videos(page, packages)
            print(f"\nCOMPLETED: Updated Channel SEO + {updated_count}/{len(LIVE_VIDEOS)} live videos on @TamilDailyLife!")
        finally:
            try:
                page.close()
            except Exception:
                pass
            browser.close()


if __name__ == "__main__":
    main()
