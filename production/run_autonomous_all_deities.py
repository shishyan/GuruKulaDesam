#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guru Kula Desam (@guru-kula-desam)
Autonomous Multi-Deity Master Film Production Engine
Continuously renders 720p HD master films across all deities on Google Flow
until Flow credits are exhausted.

Features:
- Multi-deity round-robin (Shiva, Vallalar, Vishnu/Krishna, Amman, Thirukkural, Murugan).
- Strict <= 8-minute duration ceiling.
- Fast-anchor base clips (no-extend) retimed to 75% devotional pacing.
- Max 3 scenes per track for maximum efficiency.
- Auto-resolves master audio using authenticated cookies and Node.js challenge solver.
- Persists master release records to production/autonomous_master_production_manifest.json.
- Consecutive failure and credit-exhaustion safeguard.
"""

import os
import sys
import time
import json
import re
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "production"))

from flow_browser_bridge import generate_track_on_flow
from google_flow_engine import RENDERS_DIR, FLOW_RENDERS_DIR

MANIFEST_FILE = ROOT / "production" / "autonomous_master_production_manifest.json"
PENDING_MANIFEST = ROOT / "production" / "pending_google_flow_manifest.json"
METADATA_FILE = ROOT / "live_youtube_metadata.json"

MAX_DURATION_SECONDS = 480  # Strict 8-minute ceiling

def parse_iso8601_duration(d_str: str) -> int:
    if not d_str:
        return 0
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d_str)
    if not m:
        return 0
    h = int(m.group(1) or 0)
    mins = int(m.group(2) or 0)
    s = int(m.group(3) or 0)
    return h * 3600 + mins * 60 + s

def load_manifest() -> dict:
    if MANIFEST_FILE.exists():
        try:
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "title": "Guru Kula Desam - Autonomous Multi-Deity Master Films Production",
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "total_completed": 0,
        "completed_tracks": [],
    }

def save_manifest(manifest: dict):
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

def get_existing_master_ids() -> set:
    existing = set()
    if MANIFEST_FILE.exists():
        try:
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data.get("completed_tracks", []):
                    tid = item.get("track_id")
                    if tid:
                        existing.add(tid)
        except Exception:
            pass
    for f in RENDERS_DIR.glob("*_master.mp4"):
        m = re.search(r"([0-9A-Za-z_-]{11})_master\.mp4$", f.name)
        if m:
            existing.add(m.group(1))
    return existing

def get_candidate_tracks(selected_category: str = None) -> list:
    if not PENDING_MANIFEST.exists():
        print(f"Error: {PENDING_MANIFEST} not found.", flush=True)
        return []

    with open(PENDING_MANIFEST, "r", encoding="utf-8") as f:
        p_data = json.load(f)

    ready = p_data.get("ready_to_generate", []) or p_data.get("pending_tracks", [])
    
    meta = {}
    if METADATA_FILE.exists():
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            meta = json.load(f)

    existing_masters = get_existing_master_ids()
    print(f"Total existing master films detected in renders/releases/: {len(existing_masters)}", flush=True)

    by_category = {}
    for item in ready:
        tid = item.get("video_id") or item.get("track_id")
        if not tid or tid in existing_masters:
            continue

        cat = (item.get("category") or "unknown").lower()
        if selected_category and cat != selected_category.lower():
            continue

        # Check duration
        dur_iso = meta.get(tid, {}).get("duration", "")
        dur_sec = parse_iso8601_duration(dur_iso)
        if dur_sec > MAX_DURATION_SECONDS or dur_sec <= 0:
            continue

        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append({
            "track_id": tid,
            "title": item.get("title", ""),
            "category": cat,
            "duration_sec": dur_sec,
            "blueprint_file": item.get("blueprint_file", "")
        })

    # Interleave tracks across categories for balanced round-robin
    categories = sorted(by_category.keys())
    for c in categories:
        print(f"  Category '{c}': {len(by_category[c])} eligible tracks (<= 8 min)", flush=True)

    interleaved = []
    max_len = max([len(by_category[c]) for c in categories]) if categories else 0
    for idx in range(max_len):
        for c in categories:
            if idx < len(by_category[c]):
                interleaved.append(by_category[c][idx])

    return interleaved

def main():
    parser = argparse.ArgumentParser(description="Autonomous Multi-Deity Master Production Engine")
    parser.add_argument("--category", type=str, default=None, help="Specific deity category")
    parser.add_argument("--limit", type=int, default=100, help="Maximum tracks to render in this session")
    args = parser.parse_args()

    print("=" * 80, flush=True)
    print("GURU KULA DESAM — AUTONOMOUS MULTI-DEITY PRODUCTION ENGINE", flush=True)
    print(f"Workflow: Fast-Anchor Base Scenes (--no-extend, max 3 scenes) | 720p HD @ 24fps | Ceiling: <= {MAX_DURATION_SECONDS}s", flush=True)
    print("=" * 80, flush=True)

    candidates = get_candidate_tracks(args.category)
    total_to_process = min(args.limit, len(candidates))
    print(f"\nTotal queued tracks for processing: {total_to_process}", flush=True)

    manifest = load_manifest()
    completed_in_run = 0
    consecutive_failures = 0

    for i, track in enumerate(candidates[:total_to_process], 1):
        tid = track["track_id"]
        cat = track["category"]
        title = track["title"]
        dur = track["duration_sec"]

        print(f"\n{'=' * 80}", flush=True)
        print(f"[{i}/{total_to_process}] PROCESSING: {cat.upper()} — {title} ({tid})", flush=True)
        print(f"Duration: {dur}s ({dur/60:.1f} mins) | Category: {cat}", flush=True)
        print(f"{'=' * 80}", flush=True)

        try:
            ok = generate_track_on_flow(tid, extend=False)
            if ok:
                consecutive_failures = 0
                completed_in_run += 1
                master_candidates = list(RENDERS_DIR.glob(f"*_{tid}_master.mp4"))
                master_file = master_candidates[0] if master_candidates else RENDERS_DIR / f"{cat.lower()}_{tid}_master.mp4"
                file_size_mb = master_file.stat().st_size / (1024 * 1024) if master_file.exists() else 0
                
                manifest = load_manifest()
                existing_ids = {t.get("track_id") for t in manifest.get("completed_tracks", [])}
                if tid not in existing_ids:
                    manifest["completed_tracks"].append({
                        "track_id": tid,
                        "title": title,
                        "category": cat,
                        "duration_sec": dur,
                        "master_film": str(master_file.relative_to(ROOT)),
                        "file_size_mb": round(file_size_mb, 2),
                        "completed_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")
                    })
                    manifest["total_completed"] = len(manifest["completed_tracks"])
                    save_manifest(manifest)
                print(f"\n>>> [SUCCESS] Master Film Generated: {master_file.name} ({file_size_mb:.2f} MB)", flush=True)
            else:
                consecutive_failures += 1
                print(f"\n>>> [Warning] Track {tid} returned False from generation engine. (Consecutive failures: {consecutive_failures})", flush=True)
                if consecutive_failures >= 5:
                    print("\n[Flow ALERT] 5 consecutive tracks failed. Possible credit exhaustion or session issue. Stopping runner.", flush=True)
                    break
        except Exception as e:
            consecutive_failures += 1
            print(f"\n>>> [Error] Failed processing track {tid}: {e}. (Consecutive failures: {consecutive_failures})", flush=True)
            if consecutive_failures >= 5:
                print("\n[Flow ALERT] 5 consecutive tracks failed. Possible credit exhaustion or session issue. Stopping runner.", flush=True)
                break

        time.sleep(3)

    print("\n" + "=" * 80, flush=True)
    print(f"RUN FINISHED: Completed {completed_in_run} master films in this run. Total in manifest: {manifest['total_completed']}", flush=True)
    print("=" * 80, flush=True)

if __name__ == "__main__":
    main()
