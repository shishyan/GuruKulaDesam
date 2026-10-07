# -*- coding: utf-8 -*-
"""
Render Batch 2 chapters sequentially:
8, 16, 25, 30, 31
"""

import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from production.build_any_chapter_cinematic import render_chapter, CHAPTER_REGISTRY

BATCH2_CHAPTERS = [8, 16, 25, 30, 31]

if __name__ == "__main__":
    targets = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else BATCH2_CHAPTERS
    
    print(f"Target chapters to render: {targets}", flush=True)
    for ch in targets:
        title = CHAPTER_REGISTRY[ch]["title"]
        print(f"\n{'='*70}\nSTARTING RENDER CHAPTER {ch}: {title}\n{'='*70}", flush=True)
        render_chapter(ch)
        print(f"COMPLETED CHAPTER {ch}: {CHAPTER_REGISTRY[ch]['output']}\n", flush=True)
        
    print("\n🎉 ALL REQUESTED CHAPTER FILMS RENDERED SUCCESSFULLY!", flush=True)
