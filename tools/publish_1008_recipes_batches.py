#!/usr/bin/env python3
"""
Batch-publish the 1,008 categorized South Indian Cooking Recipes to @TamilDailyLife
with 2 `1:1` food photography images per post, tracking progress in published_recipes_batches.json.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import publish_daily_gkd_community_post as gkd_pub
gkd_pub.POSTS_URL = "https://www.youtube.com/channel/UCDdEZ6CPCr6tIzWdDY9mzxg/posts"
from publish_daily_gkd_community_post import publish_via_cdp

OUT_ROOT = Path.home() / "GoogleDrive_GuruKulaDesam" / "Assets" / "south-indian-recipes-1008"
INDEX_JSON = OUT_ROOT / "RECIPES_1008_INDEX.json"
RECEIPTS_JSON = OUT_ROOT / "published_recipes_batches.json"


def ensure_two_images(entry: dict) -> list[Path]:
    num = entry["num"]
    title_en = entry["title_en"]
    img_dir = OUT_ROOT / "images" / f"recipe_{num:04d}"
    img_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["GFLOW_CLI_LEASE_WAIT_SECONDS"] = "300"

    prompts = [
        f"Photorealistic South Indian traditional {title_en} served on a fresh green banana leaf with brass vessels, warm natural morning light, appetizing food photography, pure artwork with zero text or UI icons",
        f"Photorealistic overhead close-up of South Indian {title_en} with traditional spices, curry leaves, and brass katori bowls on a clean granite counter, pure food photography with zero text or UI icons",
    ]
    images: list[Path] = []
    for idx, prompt in enumerate(prompts, start=1):
        out_file = img_dir / f"gflow_{idx:02d}.jpg"
        if out_file.exists() and out_file.stat().st_size > 30_000:
            images.append(out_file)
            continue
        cmd = [
            "gflow-headless", "image", "t2i",
            "--profile", "nagaraj957",
            prompt,
            "--aspect", "1:1",
            "--model", "nano-pro",
            "--out-file", str(out_file),
        ]
        res = subprocess.run(cmd, env=env, capture_output=True, text=True)
        if res.returncode == 0 and out_file.exists() and out_file.stat().st_size > 30_000:
            images.append(out_file)
    return images[:2]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    entries = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    receipts = json.loads(RECEIPTS_JSON.read_text(encoding="utf-8")) if RECEIPTS_JSON.exists() else {}

    posted = 0
    for entry in entries:
        num = entry["num"]
        if str(num) in receipts:
            continue
        post_text = (OUT_ROOT / entry["rel_path"]).read_text(encoding="utf-8").strip()
        images = ensure_two_images(entry)
        if not images:
            continue
        url = publish_via_cdp(post_text, images, dry_run=args.dry_run)
        receipts[str(num)] = {"num": num, "title_ta": entry["title_ta"], "url": url}
        if not args.dry_run:
            RECEIPTS_JSON.write_text(json.dumps(receipts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        posted += 1
        if posted >= args.batch_size:
            break
        time.sleep(5)

    print(f"Batch complete: {posted} recipes published ({len(receipts)}/1008 total).")


if __name__ == "__main__":
    main()
