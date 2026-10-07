# -*- coding: utf-8 -*-
"""
Render all Batch 3 chapters sequentially:
39, 40, 42, 44, 45, 46
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from production.build_any_chapter_cinematic import render_chapter, CHAPTER_REGISTRY

BATCH3_CHAPTERS = [39, 40, 42, 44, 45, 46]

if __name__ == "__main__":
    targets = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else BATCH3_CHAPTERS
    
    print(f"Target chapters to render: {targets}", flush=True)
    for ch in targets:
        title = CHAPTER_REGISTRY[ch]["title"]
        print(f"\n{'='*70}\nSTARTING RENDER CHAPTER {ch}: {title}\n{'='*70}", flush=True)
        render_chapter(ch)
        print(f"COMPLETED CHAPTER {ch}: {CHAPTER_REGISTRY[ch]['output']}\n", flush=True)
        
    print("\n🎉 ALL BATCH 3 CHAPTER FILMS RENDERED SUCCESSFULLY!", flush=True)
