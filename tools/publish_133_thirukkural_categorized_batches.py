#!/usr/bin/env python3
"""
Batch-publish the 133 categorized Thirukkural Adhikaram posts (10 kurals each)
to @guru-kula-desam via Chrome CDP (127.0.0.1:9225), ensuring 2 images per post.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, "/home/shishyan/GitHub/Shishyan/GuruKulaDesam/tools")
from publish_daily_gkd_community_post import publish_via_cdp

OUT_ROOT = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/thirukkural-1330-categorized")
INDEX_JSON = OUT_ROOT / "THIRUKKURAL_1330_INDEX.json"
RECEIPTS_JSON = OUT_ROOT / "published_batches.json"
LEGACY_POSTS_ROOT = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/thirukkural-133-posts")


def ensure_two_images(entry: dict) -> list[Path]:
    ch = entry["ch"]
    ch_name = entry["chName"]
    paal = entry["paal"]
    img_dir = OUT_ROOT / "images" / f"ch_{ch:03d}"
    img_dir.mkdir(parents=True, exist_ok=True)

    images: list[Path] = []
    legacy_img = LEGACY_POSTS_ROOT / f"ch_{ch:03d}" / f"thirukkural_ch_{ch:03d}.jpg"
    if legacy_img.exists() and legacy_img.stat().st_size > 30_000:
        images.append(legacy_img)

    env = os.environ.copy()
    env["GFLOW_CLI_LEASE_WAIT_SECONDS"] = "300"

    prompts = [
        f"Photorealistic South Indian classical Tamil temple and sage Thiruvalluvar meditating by palm-leaf manuscripts, representing Thirukkural chapter {ch} ({ch_name} in {paal}), warm golden morning light, pure artwork with zero text or UI icons",
        f"Photorealistic serene South Indian courtyard with glowing brass oil lamps, lotus flowers, and ancient stone carvings symbolizing {ch_name} ({paal}), rich sacred atmosphere, pure artwork with zero text or UI icons",
    ]

    for idx, prompt in enumerate(prompts, start=1):
        if len(images) >= 2:
            break
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
        else:
            print(f"  [Warn Ch {ch:03d}] gflow image {idx} failed: {res.stderr[:200]}", flush=True)

    return images[:2]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--start-ch", type=int, default=1)
    parser.add_argument("--end-ch", type=int, default=133)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    entries = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    receipts = json.loads(RECEIPTS_JSON.read_text(encoding="utf-8")) if RECEIPTS_JSON.exists() else {}

    posted_this_run = 0
    for entry in entries:
        ch = entry["ch"]
        if ch < args.start_ch or ch > args.end_ch:
            continue
        if str(ch) in receipts:
            continue

        post_path = OUT_ROOT / entry["rel_path"]
        post_text = post_path.read_text(encoding="utf-8").strip()
        images = ensure_two_images(entry)
        if not images:
            print(f"[Skip Ch {ch:03d}] No images available", flush=True)
            continue

        print(f"[Ch {ch:03d}/133] Publishing with {len(images)} images...", flush=True)
        url = publish_via_cdp(post_text, images, dry_run=args.dry_run)
        receipts[str(ch)] = {
            "ch": ch,
            "chName": entry["chName"],
            "url": url,
            "images": [str(p) for p in images],
        }
        if not args.dry_run:
            RECEIPTS_JSON.write_text(json.dumps(receipts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        posted_this_run += 1
        print(f"  -> Published Ch {ch:03d}: {url}", flush=True)
        if posted_this_run >= args.batch_size:
            break
        time.sleep(5)

    print(f"Batch complete: {posted_this_run} posts published this run ({len(receipts)}/133 total).")


if __name__ == "__main__":
    main()
