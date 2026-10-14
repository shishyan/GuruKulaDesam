# -*- coding: utf-8 -*-
"""
Continuous Automated Master Film Batch Assembler
Iterates through all pre-staged tracks with >= 7 consecrated scenes in production/google_flow_renders/
and builds complete, lossless release films with 75% devotional retiming.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

REPO_ROOT = Path(".")
QUEUE_FILE = REPO_ROOT / "production" / "colab_handoff" / "local_assembly_queue.json"
ASSEMBLER = REPO_ROOT / "production" / "colab_handoff" / "colab_master_assembler.py"

def run_batch():
    if not QUEUE_FILE.exists():
        print(f"Queue file {QUEUE_FILE} not found!")
        return

    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)

    print(f"🚀 Starting Continuous Master Film Assembly for {len(queue)} pending tracks...")
    
    completed = []
    failed = []

    for idx, track_id in enumerate(queue, 1):
        master_file = REPO_ROOT / "renders" / "releases" / f"thirukkural_{track_id}_master.mp4"
        if master_file.exists() and master_file.stat().st_size > 10_000_000:
            print(f"[{idx}/{len(queue)}] Track {track_id} already assembled ({master_file.stat().st_size / 1024 / 1024:.2f} MB). Skipping.")
            completed.append(track_id)
            continue

        print(f"\n=======================================================")
        print(f"[{idx}/{len(queue)}] 🎬 Assembling Release Master for Track: {track_id}")
        print(f"=======================================================")
        
        t0 = time.time()
        cmd = [
            sys.executable,
            str(ASSEMBLER),
            f"--track={track_id}",
            f"--repo-root={str(REPO_ROOT)}"
        ]
        
        try:
            res = subprocess.run(cmd, check=True)
            dur = time.time() - t0
            print(f"✅ Master Film built successfully in {dur/60:.2f} min -> {master_file.name}")
            completed.append(track_id)
        except Exception as e:
            print(f"❌ Error assembling {track_id}: {e}")
            failed.append(track_id)

    print(f"\n🎉 Batch Complete! Successfully assembled: {len(completed)} | Failed: {len(failed)}")

if __name__ == "__main__":
    run_batch()
