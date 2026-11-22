#!/usr/bin/env python3
"""
Cloud-Native Daily Editorial Community Post Stager (`@Guru-Kula-Desam` & `@TamilDailyLife`).

Runs daily at 00:00 UTC (05:30 AM IST) via GitHub Actions (`.github/workflows/daily-community-posts-cloud.yml`)
completely independent of the local Linux workstation:

1. Pulls upcoming `TamilDailyLife_YYYY-MM-DD_Script.md` + `STORY_METADATA.json` files from Google Drive
   via `rclone` (`GURUKULADESAM_RCLONE_CONF`) for the next `N` days (default: 7 days ahead).
2. Synthesizes zero-emoji, zero-Panchangam, dignified literary Tamil editorial blog posts (`editorial_post_YYYY-MM-DD.txt`)
   and 3 context-matched `1:1` sacred artwork prompts (`gflow_prompts_YYYY-MM-DD.json`) via Gemini API
   (`GEMINI_API_KEY` if set, or deterministic literary Tamil builder).
3. Materializes `@TamilDailyLife` 3-category daily posts (Panchangam, 12-Rasi Palangal, Women's Wellness/Kitchen)
   and syncs all staged texts + manifests back to Google Drive (`gdrive:GuruKulaDesam/Assets/tamil-daily-life/`).
"""
import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from publish_daily_gkd_community_post import strip_decorative_unicode, to_editorial_literary_tamil
from tdl_astro_panchangam_builder import (
    build_cat1_panchangam_post,
    build_cat2_raasi_jothidam_post,
    get_daily_astro_context,
)
from tdl_women_lifestyle_builder import build_cat3_women_lifestyle_post

TMP_ASSETS = Path("/tmp/gkd_cloud_community_stage")


def stage_one_date(ds: str, gdrive_base: str, dry_run: bool = False) -> dict:
    day_dir = TMP_ASSETS / ds
    day_dir.mkdir(parents=True, exist_ok=True)
    script_file = day_dir / f"TamilDailyLife_{ds}_Script.md"
    meta_file = day_dir / "STORY_METADATA.json"

    subprocess.run(
        ["rclone", "copyto", f"{gdrive_base}/{ds}/TamilDailyLife_{ds}_Script.md", str(script_file)],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        ["rclone", "copyto", f"{gdrive_base}/{ds}/STORY_METADATA.json", str(meta_file)],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    result = {"date": ds, "gkd_editorial_staged": False, "tdl_3cat_staged": False}

    # 1. Stage @Guru-Kula-Desam Editorial Blog Post
    post_dir = day_dir / "community_post"
    post_dir.mkdir(parents=True, exist_ok=True)
    ed_file = post_dir / f"editorial_post_{ds}.txt"
    prompts_file = post_dir / f"gflow_prompts_{ds}.json"

    subprocess.run(
        ["rclone", "copyto", f"{gdrive_base}/{ds}/community_post/editorial_post_{ds}.txt", str(ed_file)],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if ed_file.exists() and ed_file.stat().st_size > 120:
        print(f"[{ds}] @Guru-Kula-Desam editorial post already staged on Drive ({ed_file.stat().st_size} bytes).")
        result["gkd_editorial_staged"] = True
    elif script_file.exists():
        script_text = script_file.read_text(encoding="utf-8")
        meta = json.loads(meta_file.read_text(encoding="utf-8")) if meta_file.exists() else {}
        post_text, prompts = to_editorial_literary_tamil(script_text, meta)
        post_text = strip_decorative_unicode(post_text).strip()
        ed_file.write_text(post_text, encoding="utf-8")
        prompts_file.write_text(json.dumps({"date": ds, "prompts": prompts}, ensure_ascii=False, indent=2), encoding="utf-8")
        if not dry_run:
            subprocess.run(
                ["rclone", "copy", str(post_dir), f"{gdrive_base}/{ds}/community_post/"],
                check=False,
            )
        print(f"[{ds}] Synthesized & synced @Guru-Kula-Desam editorial post to Google Drive.")
        result["gkd_editorial_staged"] = True
    else:
        print(f"[{ds}] No source script found at {gdrive_base}/{ds}/ — skipping @Guru-Kula-Desam stage.")

    # 2. Stage @TamilDailyLife 3-Category Posts
    try:
        astro_ctx = get_daily_astro_context(ds)
        tdl_dir = day_dir / "tdl_community_posts"
        tdl_dir.mkdir(parents=True, exist_ok=True)
        f1 = tdl_dir / f"cat1_panchangam_{ds}.txt"
        f2 = tdl_dir / f"cat2_raasi_palangal_{ds}.txt"
        f3 = tdl_dir / f"cat3_magalir_illaram_{ds}.txt"

        subprocess.run(
            ["rclone", "copy", f"{gdrive_base}/{ds}/tdl_community_posts/", str(tdl_dir)],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if not (f1.exists() and f2.exists() and f3.exists()):
            meta = json.loads(meta_file.read_text(encoding="utf-8")) if meta_file.exists() else {}
            f1.write_text(build_cat1_panchangam_post(ds, meta), encoding="utf-8")
            f2.write_text(build_cat2_raasi_jothidam_post(ds), encoding="utf-8")
            f3.write_text(build_cat3_women_lifestyle_post(ds, astro_ctx.get("header_date_ta")), encoding="utf-8")
            if not dry_run:
                subprocess.run(
                    ["rclone", "copy", str(tdl_dir), f"{gdrive_base}/{ds}/tdl_community_posts/"],
                    check=False,
                )
            print(f"[{ds}] Synthesized & synced @TamilDailyLife 3-category posts to Google Drive.")
        else:
            print(f"[{ds}] @TamilDailyLife 3-category posts already staged on Drive.")
        result["tdl_3cat_staged"] = True
    except Exception as e:
        print(f"[{ds}] @TamilDailyLife 3-category stage note: {e}")

    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start-date", default="", help="YYYY-MM-DD (defaults to today IST)")
    ap.add_argument("--days-ahead", type=int, default=7, help="Number of upcoming days to stage on Google Drive")
    ap.add_argument("--gdrive-base", default="gdrive:GuruKulaDesam/Assets/tamil-daily-life")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.start_date:
        start_dt = datetime.date.fromisoformat(args.start_date)
    else:
        ist_now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=5, minutes=30)
        start_dt = ist_now.date()

    TMP_ASSETS.mkdir(parents=True, exist_ok=True)
    results = []
    for offset in range(max(1, args.days_ahead)):
        ds = (start_dt + datetime.timedelta(days=offset)).isoformat()
        results.append(stage_one_date(ds, args.gdrive_base, dry_run=args.dry_run))

    print(f"Cloud staging summary ({len(results)} days checked): {json.dumps(results, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
