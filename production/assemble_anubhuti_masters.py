import os
import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "production"))

from google_flow_engine import parse_blueprint, build_master_film, FLOW_RENDERS_DIR, PROMPTS_DIR, RENDERS_DIR

SOURCE_ID = "DsbMysGdqv8"
source_dir = FLOW_RENDERS_DIR / SOURCE_ID

if not source_dir.exists():
    print(f"Error: {source_dir} not found")
    sys.exit(1)

source_clips = sorted([f for f in source_dir.glob("scene_*.mp4") if f.stat().st_size > 500_000])
print(f"Found {len(source_clips)} source clips in {SOURCE_ID}:")
for c in source_clips:
    print(f"  {c.name} ({c.stat().st_size} bytes)")

sister_tracks = [
    "-L3VXkM2MTY", "8jLZHiozGxw", "N8MOVChJwPQ", "PVcmqZuROSU", "QRSRyYEacMs",
    "VMqFjcQtebw", "XErAOEtZdAU", "XqDL5bZgW9c", "cEIEecb51Fc", "iJ-3SHR2MKw",
    "qRqkS1Kf8lA", "qr5jAhLRLUE", "x355fpndpTI", "yPfkP_EjTyc"
]

print(f"\nAssembling master films for {len(sister_tracks)} sister tracks...")

results = []
for i, tid in enumerate(sister_tracks, 1):
    print(f"\n[{i}/{len(sister_tracks)}] Processing sister track: {tid}")
    
    # 1. Copy clips to track folder
    target_dir = FLOW_RENDERS_DIR / tid
    target_dir.mkdir(parents=True, exist_ok=True)
    for c in source_clips:
        dest_c = target_dir / c.name
        if not dest_c.exists() or dest_c.stat().st_size != c.stat().st_size:
            shutil.copy2(c, dest_c)
    
    # 2. Find blueprint
    bps = list(PROMPTS_DIR.glob(f"*/{tid}*.md"))
    if not bps:
        print(f"  Warning: No blueprint for {tid}")
        continue
    
    bp = parse_blueprint(bps[0])
    
    # 3. Build master film
    out_master = RENDERS_DIR / f"murugan_{tid}_master.mp4"
    if out_master.exists() and out_master.stat().st_size > 10_000_000:
        print(f"  [Cached] Master film already exists: {out_master.name} ({out_master.stat().st_size / (1024*1024):.2f} MB)")
        results.append((tid, out_master, True))
        continue
        
    try:
        from google_flow_engine import ensure_audio
        audio_path = ensure_audio(tid)
        existing_clips = sorted(target_dir.glob("scene_*.mp4"))
        success = build_master_film(bp, existing_clips, audio_path, out_master)
        if out_master.exists():
            size_mb = out_master.stat().st_size / (1024 * 1024)
            print(f"  SUCCESS: Built {out_master.name} ({size_mb:.2f} MB)")
            results.append((tid, out_master, True))
        else:
            print(f"  FAILED: Master film assembly failed for {tid}")
            results.append((tid, out_master, False))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append((tid, out_master, False))

print("\n" + "=" * 80)
print(f"KANDHAR ANUBHUTI MASTER RELEASES COMPLETED: {sum(1 for r in results if r[2])}/{len(sister_tracks)}")
print("=" * 80)
