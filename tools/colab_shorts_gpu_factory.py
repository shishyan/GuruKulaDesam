#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/colab_shorts_gpu_factory.py
Google Colab NVIDIA L4 / A100 High-Speed GPU Factory for @gurukuladesam2
("$1M Challenge" Autonomous Multi-Deity 9:16 Vertical Shorts & Revenue Engine).

What this script does when executed in Google Colab (or locally):
1. Auto-mounts Google Drive (`/content/drive/MyDrive/GuruKulaDesam`) or uses local workspace.
2. Uses NVIDIA `h264_nvenc` hardware acceleration + `ProcessPoolExecutor` multi-worker parallelization
   to render 60 to 193 Panchangam-aligned 9:16 vertical Shorts (`1080x1920 @ 30fps`) with:
   - True Upward Chromatic Divine Rain + Sambrani Temple Smoke
   - Complex HarfBuzz `Noto Sans Tamil Bold` Tri-Color Glowing Subtitles
   - Tamil Panchangam Tithi / Nakshatra / Festival Top Badges
   - Full Parent Channel Attribution & Funnel (`@guru-kula-desam` + clickable links)
3. Automatically schedules & uploads the rendered Shorts to `@gurukuladesam2` (`UCGUmNzaV_OUFbsNdHJQtaNQ`)
   at 6:00 AM, 12:00 PM, and 6:00 PM IST across your multi-project YouTube API quota pool!
"""

import os
import sys
import json
import time
import shutil
import subprocess
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.tamil_panchangam_engine import (
    IST,
    get_auspicious_alignment_for_datetime,
    print_7day_panchangam_forecast,
)
from tools.shorts_viral_builder import (
    build_short_for_track,
    list_candidate_tracks,
    SHORTS_OUT_DIR,
)
from tools.shorts_autonomous_daemon import (
    get_next_schedule_slots,
    load_published_registry,
    pick_track_for_slot,
     run_batch_pipeline,
)


def detect_colab_environment() -> dict:
    in_colab = Path("/content").exists()
    has_nvidia = False
    gpu_name = "CPU (Multi-Core)"
    try:
        out = subprocess.check_output(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"], text=True).strip()
        if out:
            has_nvidia = True
            gpu_name = out.splitlines()[0]
    except Exception:
        pass
    return {
        "in_colab": in_colab,
        "has_nvidia": has_nvidia,
        "gpu_name": gpu_name,
        "cpu_cores": os.cpu_count() or 4,
    }


def _worker_build_short(task_dict: dict) -> dict:
    tid = task_dict["track_id"]
    slot_iso = task_dict["slot_iso"]
    from datetime import datetime
    slot_dt = datetime.fromisoformat(slot_iso)
    t0 = time.time()
    meta = build_short_for_track(tid, target_dt=slot_dt, force_rebuild=task_dict.get("force", False))
    return {
        "track_id": tid,
        "deity": meta["deity"],
        "title": meta["title"],
        "video_path": meta["video_path"],
        "elapsed_sec": round(time.time() - t0, 1),
    }


def run_parallel_gpu_factory(days: int = 7, workers: int = 2, auto_upload: bool = False, force: bool = False):
    env = detect_colab_environment()
    total_shorts = days * 3

    print("=" * 85)
    print("🚀 GURUKULADESAM2 — GOOGLE COLAB / L4 GPU AUTONOMOUS SHORTS FACTORY")
    print("=" * 85)
    print(f"  • Environment : {'Google Colab Cloud' if env['in_colab'] else 'Local Workstation'}")
    print(f"  • Accelerator : {env['gpu_name']} ({env['cpu_cores']} CPU threads)")
    print(f"  • Batch Target: {total_shorts} Panchangam-Aligned Shorts ({days} Days @ 3/day)")
    print(f"  • Parent Link : @guru-kula-desam (Full Song & Gurukulam Funnel)")
    print("=" * 85)

    reg = load_published_registry()
    used_ids = set(reg.get("published_shorts", {}).keys())
    slots = get_next_schedule_slots(total_shorts, reg)

    tasks = []
    for slot_dt in slots:
        track_item, panchangam = pick_track_for_slot(slot_dt, used_ids)
        tid = track_item["track_id"]
        used_ids.add(tid)
        tasks.append({
            "track_id": tid,
            "deity": track_item["deity"],
            "slot_iso": slot_dt.isoformat(),
            "occasion": panchangam["occasion_badge_ta"],
            "force": force,
        })

    print("\n📋 Scheduled Production Queue:")
    for i, t in enumerate(tasks, 1):
        print(f"  {i:2d}. {t['slot_iso'][:16]} IST -> [{t['deity'].upper():<9}] {t['track_id']} | {t['occasion']}")

    print(f"\n⚡ Rendering {len(tasks)} Shorts using {workers} parallel worker(s)...")
    t_start = time.time()
    completed = []

    if workers <= 1:
        for t in tasks:
            try:
                res = _worker_build_short(t)
                completed.append(res)
            except Exception as e:
                print(f"❌ Error on {t['track_id']}: {e}")
    else:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            future_map = {ex.submit(_worker_build_short, t): t for t in tasks}
            for fut in as_completed(future_map):
                t = future_map[fut]
                try:
                    res = fut.result()
                    completed.append(res)
                    print(f"  ✅ Completed [{res['deity'].upper()}] {res['track_id']} in {res['elapsed_sec']}s")
                except Exception as e:
                    print(f"  ❌ Worker error on {t['track_id']}: {e}")

    total_elapsed = time.time() - t_start
    print(f"\n🎉 Factory Render Complete: {len(completed)}/{len(tasks)} Shorts built in {total_elapsed:.1f}s!")

    if auto_upload:
        print("\n📡 Launching Autonomous YouTube API Scheduler for @gurukuladesam2...")
        run_batch_pipeline(total_shorts, schedule_mode=True)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Colab L4 GPU Parallel Shorts Factory for @gurukuladesam2")
    ap.add_argument("--days", type=int, default=3, help="Number of days of Shorts to build (3 Shorts/day)")
    ap.add_argument("--workers", type=int, default=2, help="Parallel FFmpeg workers (use 4 on Colab L4)")
    ap.add_argument("--upload", action="store_true", help="Automatically upload & schedule to @gurukuladesam2 after rendering")
    ap.add_argument("--force", action="store_true", help="Force re-render existing files")
    args = ap.parse_args()

    run_parallel_gpu_factory(days=args.days, workers=args.workers, auto_upload=args.upload, force=args.force)
