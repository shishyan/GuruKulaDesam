# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from build_chapter_film import render_chapter_film, ROOT, RENDERS_DIR

REMAINING = [
    (54, "O0hASl4BS2c", ROOT / "production" / "visuals" / "thirukkural" / "54-pochchaavaamai", RENDERS_DIR / "adhikaram_54_pochchaavaamai_cinematic.mp4"),
    (57, "hjcH8zbEleE", ROOT / "production" / "visuals" / "thirukkural" / "57-veruvantha-seyyaamai", RENDERS_DIR / "adhikaram_57_veruvantha_seyyaamai_cinematic.mp4"),
    (61, "GfGlO3RQuik", ROOT / "production" / "visuals" / "thirukkural" / "61-madiyinmai", RENDERS_DIR / "adhikaram_61_madiyinmai_cinematic.mp4"),
]

def main():
    for ch, aid, vdir, out in REMAINING:
        print(f"\n{'='*70}\n[BATCH] Rendering Chapter {ch}\n{'='*70}", flush=True)
        render_chapter_film(ch, aid, vdir, out, shot_duration=6.0)
    print("\n[BATCH] Chapters 54, 57, 61 completed successfully!", flush=True)

if __name__ == "__main__":
    main()

