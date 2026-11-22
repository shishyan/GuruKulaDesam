#!/usr/bin/env python3
"""
Pre-Schedule Future YouTube Community Posts onto YouTube's Native Cloud Scheduler (`Schedule post` -> `SCHEDULED` tab).
====================================================================================================================
Why this guarantees 100% zero-PC-uptime delivery:
- YouTube Data API v3 has no REST endpoint for Community Posts.
- However, YouTube's Community Post composer (`ytd-backstage-post-dialog-renderer`) includes a native
  first-party **`Schedule post`** action (`Action menu` -> `Schedule post` -> Date + Time + `(GMT+0530) Local Time` -> `Schedule`).
- Once queued into YouTube's `SCHEDULED` tab, **YouTube's own Google servers** publish every post automatically
  at `05:30 AM IST` (`@Guru-Kula-Desam`) and `06:00 AM / 06:15 AM / 06:30 AM IST` (`@TamilDailyLife`) even when
  the Linux PC is completely powered off or unplugged for weeks!

Supported Modes:
  1. `--channel gkd`  : Pre-schedules upcoming daily Purana editorial posts (`5:30 AM IST`) on `@Guru-Kula-Desam` (`UCPqB1A_WzpLJec6q69BOO3Q`).
  2. `--channel tdl`  : Pre-schedules upcoming 3-category daily posts (`6:00 AM`, `6:15 AM`, `6:30 AM IST`) on `@TamilDailyLife` (`UCDdEZ6CPCr6tIzWdDY9mzxg`).
  3. `--channel both` : Tops up YouTube's native Cloud `SCHEDULED` queue for both channels (default: next 14 days).
"""
import argparse
import datetime
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from publish_daily_gkd_community_post import (
    ASSETS_BASE,
    ensure_gflow_images,
    strip_decorative_unicode,
    to_editorial_literary_tamil,
)
from publish_tdl_3category_community_posts import (
    ensure_tamildailylife_account,
    materialize_all_54_days,
)

GKD_CHANNEL_ID = "UCPqB1A_WzpLJec6q69BOO3Q"
TDL_CHANNEL_ID = "UCDdEZ6CPCr6tIzWdDY9mzxg"
DEFAULT_CDP_URL = os.environ.get("YT_CDP_URL", "http://127.0.0.1:9225")


def ensure_gkd_account(page, posts_url: str) -> None:
    page.goto(posts_url, wait_until="domcontentloaded", timeout=40000)
    page.wait_for_timeout(3500)
    placeholder = page.locator("#placeholder-area, #simplebox-placeholder").first
    if placeholder.count() > 0 and placeholder.is_visible():
        placeholder.click()
        page.wait_for_timeout(1200)

    has_dialog = page.locator("ytd-backstage-post-dialog-renderer").count() > 0
    dialog_text = page.locator("ytd-backstage-post-dialog-renderer").inner_text() if has_dialog else ""
    if not has_dialog or "குரு குல தேசம் (Guru Kula Desam)" not in dialog_text:
        page.locator("button[aria-label='Account menu'], #avatar-btn").first.click()
        page.wait_for_timeout(1500)
        page.locator("ytd-compact-link-renderer:has-text('Switch account'), tp-yt-paper-item:has-text('Switch account')").first.click()
        page.wait_for_timeout(2500)
        page.locator("ytd-account-item-renderer:has-text('குரு குல தேசம் (Guru Kula Desam)')").first.click()
        page.wait_for_timeout(4500)
        page.goto(posts_url, wait_until="domcontentloaded", timeout=40000)
        page.wait_for_timeout(4000)
        placeholder = page.locator("#placeholder-area, #simplebox-placeholder").first
        if placeholder.count() > 0 and placeholder.is_visible():
            placeholder.click()
            page.wait_for_timeout(1200)


def schedule_post_on_youtube_cloud(
    page,
    channel_mode: str,
    post_text: str,
    image_paths: list[Path],
    target_dt: datetime.date,
    time_label_12h: str,
    dry_run: bool = False,
) -> bool:
    """
    Uploads `image_paths` + `post_text`, opens YouTube's native `Schedule post` picker,
    sets `target_dt` (e.g., `Nov 23, 2026`) and `time_label_12h` (e.g., `5:30 AM`),
    and clicks `Schedule` so YouTube's own servers publish it when the PC is off!
    """
    if channel_mode == "gkd":
        ensure_gkd_account(page, f"https://www.youtube.com/channel/{GKD_CHANNEL_ID}/posts")
    else:
        ensure_tamildailylife_account(page)

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
    page.wait_for_timeout(5000)
    for _ in range(18):
        if page.locator("ytd-backstage-image-upload-renderer tp-yt-paper-spinner-lite[active]").count() == 0:
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

    # Open the Action menu chevron right next to Post -> click "Schedule post"
    action_btn = page.locator("ytd-backstage-post-dialog-renderer button[aria-label='Action menu']:visible").last
    for _ in range(10):
        if action_btn.is_enabled():
            break
        page.wait_for_timeout(800)
    if not action_btn.is_enabled():
        raise RuntimeError("Schedule Action menu button remained disabled")

    action_btn.click()
    page.wait_for_timeout(1200)
    page.locator("tp-yt-paper-item:has-text('Schedule post'), ytd-menu-service-item-renderer:has-text('Schedule post')").first.click()
    page.wait_for_timeout(1800)

    # Format date string like "Nov 23, 2026"
    date_label = target_dt.strftime("%b %-d, %Y")
    date_input = page.locator("ytd-backstage-post-dialog-renderer input#textbox:visible").first
    if date_input.count() > 0:
        date_input.click()
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        date_input.fill(date_label)
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)

    # Select time in the Schedule time dropdown (e.g. "5:30 AM" or "6:00 AM")
    time_trigger = page.locator("ytd-backstage-post-dialog-renderer tp-yt-paper-dropdown-menu:visible, ytd-backstage-post-dialog-renderer #time-of-day-trigger:visible").first
    if time_trigger.count() > 0 and time_trigger.is_visible():
        time_trigger.click()
        page.wait_for_timeout(1000)
        t_opt = page.locator(f"tp-yt-paper-item:has-text('{time_label_12h}')").first
        if t_opt.count() > 0:
            t_opt.scroll_into_view_if_needed()
            t_opt.click()
            page.wait_for_timeout(800)

    if dry_run:
        shot = f"/tmp/yt_cloud_schedule_dryrun_{channel_mode}_{target_dt.isoformat()}.png"
        page.screenshot(path=shot)
        print(f"[DRY RUN] Ready to schedule {channel_mode} for {date_label} @ {time_label_12h} IST -> {shot}")
        return True

    sched_btn = page.locator("ytd-backstage-post-dialog-renderer button[aria-label='Schedule']:visible, ytd-backstage-post-dialog-renderer button:has-text('Schedule'):visible").last
    for _ in range(10):
        if sched_btn.is_enabled():
            break
        page.wait_for_timeout(800)
    if not sched_btn.is_enabled():
        raise RuntimeError("Schedule submit button remained disabled")

    sched_btn.click()
    page.wait_for_timeout(5000)

    # Check if YouTube showed a rolling rate-limit toast
    toast = page.locator("tp-yt-paper-toast:visible")
    if toast.count() > 0:
        t_txt = (toast.first.inner_text() or "").strip()
        if any(k in t_txt.lower() for k in ("limit", "try again", "too many", "couldn't", "error")):
            raise RuntimeError(f"RATE_LIMITED: {t_txt}")

    return True


def queue_gkd_days(page, start_dt: datetime.date, days_ahead: int, dry_run: bool) -> int:
    scheduled_count = 0
    for offset in range(1, days_ahead + 1):
        dt = start_dt + datetime.timedelta(days=offset)
        ds = dt.isoformat()
        day_dir = ASSETS_BASE / ds
        post_dir = day_dir / "community_post"
        post_dir.mkdir(parents=True, exist_ok=True)
        pub_receipt = post_dir / f"published_{ds}.json"
        sched_receipt = post_dir / f"scheduled_{ds}.json"
        if pub_receipt.exists() or sched_receipt.exists():
            continue

        script_file = day_dir / f"TamilDailyLife_{ds}_Script.md"
        meta_file = day_dir / "STORY_METADATA.json"
        if not script_file.exists():
            subprocess.run(["rclone", "copy", f"gdrive:GuruKulaDesam/Assets/tamil-daily-life/{ds}/", str(day_dir)], check=False)
        if not script_file.exists():
            continue

        script_text = script_file.read_text(encoding="utf-8")
        meta = json.loads(meta_file.read_text(encoding="utf-8")) if meta_file.exists() else {}
        ed_file = post_dir / f"editorial_post_{ds}.txt"
        if ed_file.exists() and ed_file.stat().st_size > 120:
            post_text = strip_decorative_unicode(ed_file.read_text(encoding="utf-8")).strip()
            _, prompts = to_editorial_literary_tamil(script_text, meta)
        else:
            post_text, prompts = to_editorial_literary_tamil(script_text, meta)
            ed_file.write_text(post_text, encoding="utf-8")

        images = ensure_gflow_images(post_dir, prompts)
        if len(images) < 2:
            print(f"[GKD {ds}] Needed >=2 gflow artworks, got {len(images)} — skipping for now.")
            continue

        print(f"[GKD {ds}] Pre-scheduling onto YouTube Cloud Scheduler for {ds} @ 5:30 AM IST...")
        ok = schedule_post_on_youtube_cloud(page, "gkd", post_text, images, dt, "5:30\u202fAM", dry_run=dry_run)
        if ok and not dry_run:
            sched_receipt.write_text(
                json.dumps({"date": ds, "scheduled_for_ist": f"{ds}T05:30:00+05:30", "scheduled_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}, indent=2),
                encoding="utf-8",
            )
            subprocess.run(["rclone", "copy", str(post_dir), f"gdrive:GuruKulaDesam/Assets/tamil-daily-life/{ds}/community_post/"], check=False)
            scheduled_count += 1
            time.sleep(12)
    return scheduled_count


def queue_tdl_days(page, start_dt: datetime.date, days_ahead: int, dry_run: bool) -> int:
    records = {r["date"]: r for r in materialize_all_54_days()}
    slot_times = {
        "cat1_panchangam": "6:00\u202fAM",
        "cat2_raasi_palangal": "6:15\u202fAM",
        "cat3_magalir_illaram": "6:30\u202fAM",
    }
    scheduled_count = 0
    for offset in range(1, days_ahead + 1):
        dt = start_dt + datetime.timedelta(days=offset)
        ds = dt.isoformat()
        if ds not in records:
            continue
        rec = records[ds]
        rp = rec["receipt_path"]
        day_pub = json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}
        changed = False
        for c in rec["categories"]:
            ck = c["key"]
            if day_pub.get(ck, {}).get("url") or day_pub.get(ck, {}).get("scheduled_for_ist"):
                continue
            t_str = slot_times.get(ck, "6:00\u202fAM")
            print(f"[TDL {ds} | {ck}] Pre-scheduling onto YouTube Cloud Scheduler for {ds} @ {t_str} IST...")
            ok = schedule_post_on_youtube_cloud(page, "tdl", c["text"], [c["image_path"]], dt, t_str, dry_run=dry_run)
            if ok and not dry_run:
                day_pub[ck] = {
                    "scheduled_for_ist": f"{ds} {t_str} IST",
                    "image": c["image_path"].name,
                    "scheduled_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                }
                rp.write_text(json.dumps(day_pub, ensure_ascii=False, indent=2), encoding="utf-8")
                changed = True
                scheduled_count += 1
                time.sleep(15)
        if changed:
            subprocess.run(["rclone", "copy", str(rec["day_post_dir"]), f"gdrive:GuruKulaDesam/Assets/tamil-daily-life/{ds}/tdl_community_posts/"], check=False)
    return scheduled_count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", choices=["gkd", "tdl", "both"], default="both")
    ap.add_argument("--days-ahead", type=int, default=14)
    ap.add_argument("--cdp-url", default=DEFAULT_CDP_URL)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ist_today = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=5, minutes=30)).date()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(args.cdp_url)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        try:
            total = 0
            if args.channel in ("gkd", "both"):
                try:
                    total += queue_gkd_days(page, ist_today, args.days_ahead, args.dry_run)
                except Exception as e:
                    print(f"[GKD Cloud Pre-Schedule Notice] {e}")
            if args.channel in ("tdl", "both"):
                try:
                    total += queue_tdl_days(page, ist_today, args.days_ahead, args.dry_run)
                except Exception as e:
                    print(f"[TDL Cloud Pre-Schedule Notice] {e}")
            print(f"Pre-scheduled {total} upcoming Community Posts onto YouTube's Cloud Scheduler.")
        finally:
            page.close()


if __name__ == "__main__":
    main()
