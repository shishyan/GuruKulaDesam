# -*- coding: utf-8 -*-
import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "production"))

from build_any_chapter_cinematic import render_chapter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BATCH2_CHAPTERS = [42, 44, 45, 46]

def main():
    print("=" * 70)
    print("STARTING BATCH 2 VEDIC MASTER RENDERS (Chapters 42, 44, 45, 46)")
    print("=" * 70)
    for ch in BATCH2_CHAPTERS:
        # Wipe temp directory to ensure fresh render of new Vedic images
        temp_dir = ROOT / "renders" / f"temp_ch{ch}_cinematic"
        if temp_dir.exists():
            print(f"Clearing temp directory: {temp_dir.name}...")
            shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"\n--- RENDERING CHAPTER {ch} ---")
        render_chapter(ch)
        print(f"--- CHAPTER {ch} COMPLETE ---\n")

    print("=" * 70)
    print("ALL BATCH 2 CHAPTERS (42, 44, 45, 46) RENDERED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    main()
