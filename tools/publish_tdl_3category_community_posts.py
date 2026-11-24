#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/home/shishyan/GitHub/Shishyan/GuruKulaDesam/tools/publish_tdl_3category_community_posts.py
===========================================================================================
Master 3-Category Daily Community Post Generator & Live YouTube Publisher for @TamilDailyLife
(`தமிழர் பண்பாடு (வாழ்வியல் நெறி) #TamilVirtues` — Channel ID: `UCDdEZ6CPCr6tIzWdDY9mzxg`)

Covers all 54 days of 2026 since Diwali (`2026-11-08` through `2026-12-31` = 162 posts):
  1. Category 1 (`cat1_panchangam`): தமிழ் பஞ்சாங்கம் & மகளிர் வழிபாட்டு வழிகாட்டி
  2. Category 2 (`cat2_raasi_palangal`): இன்றைய ராசி பலன்கள் & மகளிர் ஜோதிட வழிகாட்டி
  3. Category 3 (`cat3_magalir_illaram`): இல்லறம், சமையல் & மகளிர் நல வழிகாட்டி
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import date, timedelta
from pathlib import Path
from playwright.sync_api import sync_playwright

TOOLS_DIR = Path(__file__).resolve().parent
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
POSTS_URL = f"https://www.youtube.com/channel/{CHANNEL_ID}/posts"
CDP_PORT = 9225
CDP_URL = f"http://127.0.0.1:{CDP_PORT}"

_LOCAL_DRIVE_ASSETS = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life")
ASSETS_BASE = _LOCAL_DRIVE_ASSETS if _LOCAL_DRIVE_ASSETS.exists() else Path("/tmp/tdl_cloud_assets/tamil-daily-life")
ARTWORKS_DIR = ASSETS_BASE / "tdl_community_artworks"
MASTER_MANIFEST_PATH = ASSETS_BASE / "TDL_3CATEGORY_COMMUNITY_POSTS_MANIFEST.json"


def sync_cloud_assets_from_gdrive() -> None:
    """When running on GitHub Actions (without local workstation mount), hydrate manifest & artworks from Google Drive."""
    if _LOCAL_DRIVE_ASSETS.exists():
        return
    ASSETS_BASE.mkdir(parents=True, exist_ok=True)
    ARTWORKS_DIR.mkdir(parents=True, exist_ok=True)
    print("[Cloud Hydrate] Pulling TDL_3CATEGORY_COMMUNITY_POSTS_MANIFEST.json & artworks from Google Drive...", flush=True)
    subprocess.run(
        [
            "rclone", "copyto",
            "gdrive:GuruKulaDesam/Assets/tamil-daily-life/TDL_3CATEGORY_COMMUNITY_POSTS_MANIFEST.json",
            str(MASTER_MANIFEST_PATH),
        ],
        check=False,
    )
    subprocess.run(
        [
            "rclone", "copy",
            "gdrive:GuruKulaDesam/Assets/tamil-daily-life/tdl_community_artworks/",
            str(ARTWORKS_DIR),
            "--transfers", "8",
        ],
        check=False,
    )
    if MASTER_MANIFEST_PATH.exists():
        try:
            mf = json.loads(MASTER_MANIFEST_PATH.read_text(encoding="utf-8"))
            for ds, cats in (mf.get("days") or {}).items():
                day_pub = {}
                for ck, info in (cats or {}).items():
                    if info.get("url"):
                        day_pub[ck] = {
                            "url": info["url"],
                            "image": Path(info.get("image_file") or "").name,
                            "published_at": info.get("published_at") or "",
                        }
                if day_pub:
                    rp = ASSETS_BASE / ds / "tdl_community_posts" / f"published_{ds}.json"
                    rp.parent.mkdir(parents=True, exist_ok=True)
                    if not rp.exists():
                        rp.write_text(json.dumps(day_pub, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"[Cloud Hydrate] Manifest seed note: {e}", flush=True)

START_DATE = date(2026, 11, 8)
END_DATE = date(2026, 12, 31)

CAT1_BY_WEEKDAY = {
    0: "cat1_mon_somavara_shiva.jpg",
    1: "cat1_tue_murugan_amman.jpg",
    2: "cat1_wed_perumal_tulsi.jpg",
    3: "cat1_thu_guru_dakshinamurthy.jpg",
    4: "cat1_fri_mahalakshmi_velli.jpg",
    5: "cat1_sat_karthigai_margazhi.jpg",
    6: "cat1_sun_surya_shiva.jpg",
}

CAT2_ROTATION = [
    "cat2_rasi_mandala_01.jpg",
    "cat2_navagraha_lamps_02.jpg",
    "cat2_nakshatra_sky_03.jpg",
    "cat2_vastu_nilapadi_04.jpg",
    "cat2_chandra_pournami_05.jpg",
    "cat2_subha_horai_kalasha_06.jpg",
    "cat2_pariharam_gomatha_07.jpg",
]

CAT3_ROTATION = [
    "cat3_kitchen_anjaraipetti_01.jpg",
    "cat3_sattvic_banana_leaf_02.jpg",
    "cat3_herbal_kashayam_03.jpg",
    "cat3_natural_beauty_herbs_04.jpg",
    "cat3_family_lamp_harmony_05.jpg",
    "cat3_savings_mangalam_06.jpg",
    "cat3_margazhi_dawn_kolam_07.jpg",
]


def select_artworks_for_date(day_idx: int, dt: date, astro_ctx: dict) -> dict[str, Path]:
    wd = dt.weekday()
    tithi_ta = astro_ctx.get("tithi_clean_ta", "")
    tamil_month_ta = astro_ctx.get("tamil_month_ta", "")

    # Cat 1: Festival/month overrides + weekday alignment
    if dt == date(2026, 11, 24) or (tamil_month_ta == "கார்த்திகை" and wd == 5):
        c1_name = "cat1_sat_karthigai_margazhi.jpg"
    else:
        c1_name = CAT1_BY_WEEKDAY[wd]

    # Cat 2: Full moon gets Pournami artwork; otherwise deterministic rotation
    if "பௌர்ணமி" in tithi_ta:
        c2_name = "cat2_chandra_pournami_05.jpg"
    else:
        c2_name = CAT2_ROTATION[day_idx % len(CAT2_ROTATION)]

    # Cat 3: Margazhi start highlights Margazhi dawn kolam; otherwise deterministic rotation
    if dt == date(2026, 12, 16):
        c3_name = "cat3_margazhi_dawn_kolam_07.jpg"
    else:
        c3_name = CAT3_ROTATION[day_idx % len(CAT3_ROTATION)]

    return {
        "cat1": ARTWORKS_DIR / c1_name,
        "cat2": ARTWORKS_DIR / c2_name,
        "cat3": ARTWORKS_DIR / c3_name,
    }


LOCAL_ART_CACHE = Path("/tmp/tdl_community_artworks_cache")


def get_cached_artwork(src: Path) -> Path:
    LOCAL_ART_CACHE.mkdir(parents=True, exist_ok=True)
    dst = LOCAL_ART_CACHE / src.name
    if (not dst.exists() or dst.stat().st_size < 15_000) and src.exists():
        import shutil
        shutil.copy2(src, dst)
    return dst if dst.exists() else src


def materialize_all_54_days() -> list[dict]:
    """Generate and persist all 54 days x 3 categories = 162 post text files on disk."""
    total_days = (END_DATE - START_DATE).days + 1
    records = []
    for idx in range(total_days):
        dt = START_DATE + timedelta(days=idx)
        ds = dt.isoformat()
        day_post_dir = ASSETS_BASE / ds / "tdl_community_posts"
        day_post_dir.mkdir(parents=True, exist_ok=True)

        f1 = day_post_dir / f"cat1_panchangam_{ds}.txt"
        f2 = day_post_dir / f"cat2_raasi_palangal_{ds}.txt"
        f3 = day_post_dir / f"cat3_magalir_illaram_{ds}.txt"

        astro_ctx = get_daily_astro_context(ds)
        if (
            f1.exists()
            and f2.exists()
            and f3.exists()
            and "#TamilDailyLife" in f1.read_text(encoding="utf-8")
            and "#TamilDailyLife" in f2.read_text(encoding="utf-8")
            and "#TamilDailyLife" in f3.read_text(encoding="utf-8")
        ):
            cat1_txt = f1.read_text(encoding="utf-8")
            cat2_txt = f2.read_text(encoding="utf-8")
            cat3_txt = f3.read_text(encoding="utf-8")
        else:
            meta = load_story_meta(ds)
            cat1_txt = build_cat1_panchangam_post(ds, meta)
            cat2_txt = build_cat2_raasi_jothidam_post(ds)
            cat3_txt = build_cat3_women_lifestyle_post(ds, astro_ctx.get("header_date_ta"))
            f1.write_text(cat1_txt, encoding="utf-8")
            f2.write_text(cat2_txt, encoding="utf-8")
            f3.write_text(cat3_txt, encoding="utf-8")

        arts = select_artworks_for_date(idx, dt, astro_ctx)
        cached_arts = {k: get_cached_artwork(p) for k, p in arts.items()}

        records.append(
            {
                "date": ds,
                "day_post_dir": day_post_dir,
                "receipt_path": day_post_dir / f"published_{ds}.json",
                "categories": [
                    {
                        "key": "cat1_panchangam",
                        "label_ta": "பஞ்சாங்கம் & மகளிர் வழிபாட்டு வழிகாட்டி",
                        "text_path": f1,
                        "text": cat1_txt,
                        "image_path": cached_arts["cat1"],
                    },
                    {
                        "key": "cat2_raasi_palangal",
                        "label_ta": "இன்றைய ராசி பலன்கள் & மகளிர் ஜோதிட வழிகாட்டி",
                        "text_path": f2,
                        "text": cat2_txt,
                        "image_path": cached_arts["cat2"],
                    },
                    {
                        "key": "cat3_magalir_illaram",
                        "label_ta": "இல்லறம், சமையல் & மகளிர் நல வழிகாட்டி",
                        "text_path": f3,
                        "text": cat3_txt,
                        "image_path": cached_arts["cat3"],
                    },
                ],
            }
        )
    return records


def restart_and_resync_cdp_browser():
    import os
    print("Ensuring desktop keyring environment and launching Chrome 9225...", flush=True)
    os.environ.setdefault("XDG_CURRENT_DESKTOP", "zorin:GNOME")
    os.environ.setdefault("DESKTOP_SESSION", "zorin")
    os.environ.setdefault("DBUS_SESSION_BUS_ADDRESS", f"unix:path=/run/user/{os.getuid()}/bus")
    subprocess.run(["pkill", "-f", "/opt/google/chrome/chrome.*9225"], check=False)
    time.sleep(2.0)
    import flow_autonomous_generator as fg
    fg.sync_flow_chrome_profile(force=True)
    fg.ensure_flow_chrome_running(user_idx=3)
    time.sleep(2.5)


def ensure_cdp_browser():
    import urllib.request
    try:
        urllib.request.urlopen(f"{CDP_URL}/json/version", timeout=2)
        return
    except Exception:
        pass
    restart_and_resync_cdp_browser()


def ensure_tamildailylife_account(page) -> None:
    """Ensure active YouTube Brand Account in Chrome 9225 is the OWNER @TamilDailyLife (UCDdEZ6CPCr6tIzWdDY9mzxg)."""
    if not page.url.startswith(POSTS_URL):
        page.goto(POSTS_URL, wait_until="domcontentloaded", timeout=40000)
        try:
            page.wait_for_selector(
                "#placeholder-area, #simplebox-placeholder, ytd-backstage-post-dialog-renderer, a[aria-label='Sign in']",
                timeout=15000,
            )
        except Exception:
            pass

    # If signed out ("Sign in" visible and no #avatar-btn), raise so outer loop re-syncs Cookies!
    if page.locator("#avatar-btn").count() == 0 and page.locator("a[aria-label='Sign in'], ytd-button-renderer a[href*='ServiceLogin']").count() > 0:
        raise RuntimeError("YOUTUBE_SIGNED_OUT_NEED_RESYNC")

    placeholder = page.locator("#placeholder-area, #simplebox-placeholder").first
    if placeholder.count() > 0 and placeholder.is_visible():
        placeholder.click()
        page.wait_for_timeout(1200)

    has_dlg = page.locator("ytd-backstage-post-dialog-renderer").count() > 0
    dlg_text = page.locator("ytd-backstage-post-dialog-renderer").inner_text() if has_dlg else ""
    if has_dlg and ("தமிழர் பண்பாடு" in dlg_text or "TamilVirtues" in dlg_text or "TamilDailyLife" in dlg_text):
        return

    # Reload POSTS_URL once before attempting account switch
    page.goto(POSTS_URL, wait_until="domcontentloaded", timeout=40000)
    page.wait_for_timeout(4000)
    if page.locator("#avatar-btn").count() == 0:
        raise RuntimeError("YOUTUBE_SIGNED_OUT_NEED_RESYNC")

    placeholder = page.locator("#placeholder-area, #simplebox-placeholder").first
    if placeholder.count() > 0 and placeholder.is_visible():
        placeholder.click()
        page.wait_for_timeout(1200)
    has_dlg = page.locator("ytd-backstage-post-dialog-renderer").count() > 0
    dlg_text = page.locator("ytd-backstage-post-dialog-renderer").inner_text() if has_dlg else ""
    if has_dlg and ("தமிழர் பண்பாடு" in dlg_text or "TamilVirtues" in dlg_text or "TamilDailyLife" in dlg_text):
        return

    print("Switching active Brand Account on port 9225 to OWNER @TamilDailyLife ...", flush=True)
    page.goto("https://www.youtube.com", wait_until="domcontentloaded", timeout=35000)
    page.wait_for_selector("#avatar-btn", timeout=15000)
    page.locator("#avatar-btn").first.click()
    page.wait_for_timeout(1500)
    page.locator(
        'ytd-compact-link-renderer:has-text("Switch account"), tp-yt-paper-item:has-text("Switch account")'
    ).first.click()
    page.wait_for_timeout(2500)
    items = page.locator("ytd-account-item-renderer")
    clicked = False
    for i in range(items.count()):
        txt = " | ".join(x.strip() for x in items.nth(i).inner_text().splitlines() if x.strip())
        if "தமிழர் பண்பாடு" in txt and "manager" not in txt.lower():
            items.nth(i).click()
            clicked = True
            break
    if not clicked:
        page.locator('ytd-account-item-renderer:has-text("தமிழர் பண்பாடு")').last.click()
    page.wait_for_timeout(4500)

    page.goto(POSTS_URL, wait_until="domcontentloaded", timeout=40000)
    page.wait_for_selector(
        "#placeholder-area, #simplebox-placeholder, ytd-backstage-post-dialog-renderer",
        timeout=18000,
    )
    placeholder = page.locator("#placeholder-area, #simplebox-placeholder").first
    if placeholder.count() > 0 and placeholder.is_visible():
        placeholder.click()
        page.wait_for_timeout(1200)


def get_top_post_url(page) -> str:
    el = page.locator('ytd-backstage-post-thread-renderer a[href*="/post/"]').first
    if el.count() == 0:
        return ""
    href = el.get_attribute("href") or ""
    if href.startswith("/"):
        return f"https://www.youtube.com{href}"
    return href


def publish_one_post_on_page(page, post_text: str, image_path: Path) -> tuple[str | None, str | None]:
    """
    Publish a single Community Post with 1:1 image on `@TamilDailyLife`.
    Returns `(new_post_url, error_reason)`.
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
    file_input.set_input_files([str(image_path.resolve())])

    # Wait for image upload preview spinner to complete
    page.wait_for_timeout(4500)
    for _ in range(18):
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
    page.wait_for_timeout(1000)

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
                import re
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

        # Poll for API postId or brand-new DOM post URL
        for _ in range(24):
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

    return None, "Burst cooldown or daily rate limit on create_post"


def write_master_manifest(records: list[dict]) -> dict:
    summary = {
        "channel": "@TamilDailyLife",
        "channel_id": CHANNEL_ID,
        "updated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_days": len(records),
        "total_posts_generated": len(records) * 3,
        "total_posts_published_live": 0,
        "days": {},
    }
    live_count = 0
    for rec in records:
        ds = rec["date"]
        rp = rec["receipt_path"]
        day_pub = json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}
        cats_out = {}
        for c in rec["categories"]:
            ck = c["key"]
            pub_entry = day_pub.get(ck, {})
            if pub_entry.get("url"):
                live_count += 1
            cats_out[ck] = {
                "label_ta": c["label_ta"],
                "text_file": str(c["text_path"]),
                "image_file": str(c["image_path"]),
                "url": pub_entry.get("url"),
                "published_at": pub_entry.get("published_at"),
            }
        summary["days"][ds] = cats_out
    summary["total_posts_published_live"] = live_count
    MASTER_MANIFEST_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start-date", default="2026-11-08")
    ap.add_argument("--end-date", default="2026-12-31")
    ap.add_argument("--generate-only", action="store_true")
    ap.add_argument("--cloud-headless", action="store_true", help="Run standalone headless Chromium in GitHub Actions")
    ap.add_argument("--storage-state", default="", help="Optional Playwright storage_state JSON path for cloud headless")
    ap.add_argument("--delay-sec", type=float, default=50.0)
    ap.add_argument("--max-posts", type=int, default=60, help="Max posts to publish per daily run before yielding")
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    sync_cloud_assets_from_gdrive()
    print("Materializing all 54 days x 3 categories (162 posts) on disk...", flush=True)
    records = materialize_all_54_days()
    summary = write_master_manifest(records)
    print(
        f"Materialized {summary['total_posts_generated']} posts across {summary['total_days']} days "
        f"(already live: {summary['total_posts_published_live']}).",
        flush=True,
    )

    if args.generate_only:
        subprocess.run(
            [
                "rclone", "copyto",
                str(MASTER_MANIFEST_PATH),
                "gdrive:GuruKulaDesam/Assets/tamil-daily-life/TDL_3CATEGORY_COMMUNITY_POSTS_MANIFEST.json",
            ],
            check=False,
        )
        return

    if args.cloud_headless and (not args.storage_state or not Path(args.storage_state).exists()):
        print(
            "NOTICE: Running in --cloud-headless mode without TAMILDAILYLIFE_YT_STORAGE_STATE_B64 configured; "
            "all 162 SEO-hashtagged 3-category posts and manifest are materialized and synced to Google Drive.",
            flush=True,
        )
        subprocess.run(
            [
                "rclone", "copyto",
                str(MASTER_MANIFEST_PATH),
                "gdrive:GuruKulaDesam/Assets/tamil-daily-life/TDL_3CATEGORY_COMMUNITY_POSTS_MANIFEST.json",
            ],
            check=False,
        )
        return

    if not args.cloud_headless:
        ensure_cdp_browser()
    rate_limit_hit = False
    newly_published = 0

    with sync_playwright() as p:
        if args.cloud_headless:
            browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
            ctx = browser.new_context(storage_state=args.storage_state, viewport={"width": 1920, "height": 1080})
        else:
            browser = p.chromium.connect_over_cdp(CDP_URL)
            ctx = browser.contexts[0]
        page = ctx.new_page()
        page.set_default_timeout(25000)
        try:
            for rec in records:
                ds = rec["date"]
                if ds < args.start_date or ds > args.end_date:
                    continue
                rp = rec["receipt_path"]
                day_pub = json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}

                day_changed = False
                for c in rec["categories"]:
                    ck = c["key"]
                    if day_pub.get(ck, {}).get("url"):
                        continue

                    print(f"[{ds} | {ck}] Publishing ({c['image_path'].name}) ...", flush=True)
                    url, err = None, None
                    for attempt in range(5):
                        try:
                            if not args.cloud_headless:
                                ensure_cdp_browser()
                            url, err = publish_one_post_on_page(page, c["text"], c["image_path"])
                            if url:
                                break
                            cooldown = 55 + (35 * attempt)
                            if attempt < 4:
                                print(f"  soft-limit/cooldown retry {attempt+1}/4 in {cooldown}s ({err})...", flush=True)
                                time.sleep(cooldown)
                        except Exception as exc:
                            err = str(exc)
                            print(f"  retry {attempt+1}/5 after exception: {err[:160]}", flush=True)
                            if args.cloud_headless:
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
                            page.set_default_timeout(25000)
                            time.sleep(5)

                    if url:
                        day_pub[ck] = {
                            "url": url,
                            "image": c["image_path"].name,
                            "published_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        }
                        rp.write_text(json.dumps(day_pub, ensure_ascii=False, indent=2), encoding="utf-8")
                        newly_published += 1
                        day_changed = True
                        print(f"  LIVE ({newly_published}) -> {url}", flush=True)
                        if args.max_posts and newly_published >= args.max_posts:
                            print(f"Reached --max-posts={args.max_posts} for this run; saving state cleanly.", flush=True)
                            rate_limit_hit = True
                            break
                        time.sleep(args.delay_sec)
                    else:
                        print(f"  STOP/WARN on {ds} {ck}: {err}", flush=True)
                        rate_limit_hit = True
                        break

                if day_changed and (newly_published % 15 == 0):
                    write_master_manifest(records)

                if rate_limit_hit:
                    print("Rate-limit / cap reached on live feed; saving state cleanly.", flush=True)
                    break
        finally:
            try:
                page.close()
            except Exception:
                pass

    final_summary = write_master_manifest(records)
    print(
        f"\nSyncing artworks & manifest to Google Drive (live={final_summary['total_posts_published_live']}/162)...",
        flush=True,
    )
    subprocess.run(
        [
            "rclone", "copy",
            str(ARTWORKS_DIR),
            "gdrive:GuruKulaDesam/Assets/tamil-daily-life/tdl_community_artworks/",
            "--transfers", "8",
        ],
        check=False,
    )
    subprocess.run(
        [
            "rclone", "copyto",
            str(MASTER_MANIFEST_PATH),
            "gdrive:GuruKulaDesam/Assets/tamil-daily-life/TDL_3CATEGORY_COMMUNITY_POSTS_MANIFEST.json",
        ],
        check=False,
    )
    print("DONE!", flush=True)


if __name__ == "__main__":
    main()
