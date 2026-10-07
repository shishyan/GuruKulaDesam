# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from build_true_motion_film import render_stable_film, CHAPTERS

def main():
    target_chapters = [27, 52, 54, 57, 61]
    for ch in target_chapters:
        aid, vdir, out = CHAPTERS[ch]
        print(f"\n{'='*70}\n[BATCH PRODUCTION] Rendering Chapter {ch} True Motion Film\n{'='*70}", flush=True)
        render_stable_film(ch, aid, vdir, out)
        
    print("\n[BATCH PRODUCTION] All True Motion films rendered successfully!", flush=True)

if __name__ == "__main__":
    main()
