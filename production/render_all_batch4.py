# -*- coding: utf-8 -*-
"""
Render all Batch 4 chapters sequentially:
60, 62, 65, 66, 67, 74
Dynamic Enterprise & Heroic Action Suite
"""

import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from production.build_any_chapter_cinematic import render_chapter, CHAPTER_REGISTRY

BATCH4_CHAPTERS = [60, 62, 65, 66, 67, 74]

if __name__ == "__main__":
    targets = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else BATCH4_CHAPTERS
    
    print(f"Target Batch 4 chapters to render: {targets}", flush=True)
    for ch in targets:
        title = CHAPTER_REGISTRY[ch]["title"]
        print(f"\n{'='*75}\nSTARTING RENDER CHAPTER {ch}: {title}\n{'='*75}", flush=True)
        render_chapter(ch)
        print(f"COMPLETED CHAPTER {ch}: {CHAPTER_REGISTRY[ch]['output']}\n", flush=True)
        
    print("\n🎉 ALL BATCH 4 CHAPTER FILMS RENDERED SUCCESSFULLY!", flush=True)
