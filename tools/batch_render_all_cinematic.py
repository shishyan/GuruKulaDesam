#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/batch_render_all_cinematic.py
Automated Batch Processor for all 37 Curated Thirukkural Chapters:
- Validates curated audio and image collections.
- Executes build_cinematic_720p_film.py with optional GPU NVENC acceleration.
- Renders 1280x720 24fps cinema-grade videos with 5–7s transitions, 4-way & 3D parabolic pans,
  and 100% upward divine drizzle/vibhuti atmospheric loops.
"""
import sys, os, json, argparse, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURATED_FILE = ROOT / "production" / "curated_37_waiting_adhigarams.json"
BUILD_SCRIPT = ROOT / "tools" / "build_cinematic_720p_film.py"

def main():
    parser = argparse.ArgumentParser(description="Batch Render 720p Cinematic Devotional Films")
    parser.add_argument("--gpu", choices=["none", "nvenc"], default="none", help="Enable NVIDIA GPU NVENC acceleration")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of chapters to process (0 = all 37)")
    parser.add_argument("--start-chapter", type=int, default=1, help="Start from specific chapter number (e.g. 4)")
    parser.add_argument("--parallel-chapters", type=int, default=4, help="Number of entire chapters to render concurrently (e.g. 4 or 6)")
    args = parser.parse_args()

    if not CURATED_FILE.exists():
        print(f"Error: Curated chapters list not found at {CURATED_FILE}")
        sys.exit(1)

    with open(CURATED_FILE, "r", encoding="utf-8") as f:
        chapters = json.load(f)

    # Filter chapters starting from start_chapter
    chapters = [c for c in chapters if c["chapter"] >= args.start_chapter]
    if args.limit > 0:
        chapters = chapters[:args.limit]

    print(f"Starting Multi-Chapter Parallel Render for {len(chapters)} chapters...")
    print(f"Concurrent Chapters: {args.parallel_chapters} | GPU: {args.gpu}")
    print("=" * 60)

    from concurrent.futures import ThreadPoolExecutor

    def process_chapter(item):
        ch_num = item["chapter"]
        ch_name = item.get("name_ta", f"Chapter {ch_num}")
        print(f"▶ [STARTED] Chapter {ch_num}: {ch_name}...", flush=True)
        cmd = [sys.executable, str(BUILD_SCRIPT), "--chapter", str(ch_num), "--gpu", args.gpu]
        try:
            res = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            print(f"✔ [COMPLETED] Chapter {ch_num}: {ch_name}!", flush=True)
            return ch_num, True, ""
        except subprocess.CalledProcessError as e:
            print(f"✖ [FAILED] Chapter {ch_num}: {ch_name} (code {e.returncode})", flush=True)
            return ch_num, False, e.output

    completed = 0
    failed = []

    with ThreadPoolExecutor(max_workers=args.parallel_chapters) as executor:
        for ch_num, success, err_out in executor.map(process_chapter, chapters):
            if success:
                completed += 1
            else:
                failed.append((ch_num, err_out[-300:] if err_out else ""))

    print("\n" + "=" * 60)
    print(f"BATCH RENDER SUMMARY:")
    print(f"Successfully rendered: {completed}/{len(chapters)}")
    if failed:
        print(f"Failed chapters: {[f[0] for f in failed]}")
    print("=" * 60)

if __name__ == "__main__":
    main()
