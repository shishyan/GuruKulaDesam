# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Batch 4 Master Film Rendering Engine
Renders Chapters 60, 62, 65, 66, 67, 74:
- 60: ஊக்கமுடைமை (Ookkamudaimai)
- 62: ஆள்வினையுடைமை (Aalvinaiyudaimai)
- 65: சொல்வன்மை (Solvanmai)
- 66: வினைத்தூய்மை (Vinaithooymai)
- 67: வினைத்திட்பம் (Vinaithitpam)
- 74: நாடு (Naadu)

Features:
- Scene-aware selective drizzle (auspicious on positive scenes, dry on negative scenes)
- Consecrated corner framing: Sacred Dhoopa Kalasam (bottom-left) & Kuthuvilakku (bottom-right)
- 2x oversampled cinematic camera motion with cosine easing
- Master A/V synchronization (< 0.005s drift) + faststart moov atom
"""

import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "production"))

from build_any_chapter_cinematic import render_chapter, CHAPTER_REGISTRY

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BATCH4_CHAPTERS = [60, 62, 65, 66, 67, 74]

def main():
    print("=" * 75)
    print("STARTING BATCH 4 VEDIC MASTER RENDERS (Chapters 60, 62, 65, 66, 67, 74)")
    print("=" * 75)
    for ch in BATCH4_CHAPTERS:
        cfg = CHAPTER_REGISTRY[ch]
        out_file = cfg["output"]

        # Check if already rendered and valid
        if out_file.exists() and out_file.stat().st_size > 5_000_000:
            print(f"\n[Exists & Valid] Chapter {ch}: {out_file.name} ({out_file.stat().st_size / 1024 / 1024:.2f} MB)")
            continue

        temp_dir = ROOT / "renders" / f"temp_ch{ch}_cinematic"
        if temp_dir.exists():
            print(f"Clearing temp directory: {temp_dir.name}...")
            shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"\n--- RENDERING CHAPTER {ch}: {cfg['title']} ---")
        render_chapter(ch)
        print(f"--- CHAPTER {ch} COMPLETE ---\n")

    print("=" * 75)
    print("ALL BATCH 4 CHAPTERS (60, 62, 65, 66, 67, 74) RENDERED SUCCESSFULLY!")
    print("=" * 75)

if __name__ == "__main__":
    main()
