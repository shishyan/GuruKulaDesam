# -*- coding: utf-8 -*-
"""
Run 46-Shot Cinematic True Film Build for Chapter 26 (Pulaal Unnaamai)
"""
import sys
from pathlib import Path
from build_cinematic_46_film import render_film

ROOT = Path(__file__).resolve().parents[1]
VISUAL_DIR = ROOT / "production" / "visuals" / "thirukkural" / "26-pulaal-unnaamai"
AUDIO_ID = "h2q-ADrbBc4"
OUTPUT = ROOT / "renders" / "releases" / "adhikaram_26_pulaal_unnaamai_cinematic.mp4"

def main():
    images = sorted(list(VISUAL_DIR.glob("*.jpg")) + list(VISUAL_DIR.glob("*.png")))
    print(f"Found {len(images)} unique images for Chapter 26.")
    assert len(images) == 46, f"Expected 46 images, found {len(images)}"
    
    render_film(images, AUDIO_ID, OUTPUT)
    print("\n[CH26 MASTER PRODUCTION COMPLETED SUCCESSFULLY!]")

if __name__ == "__main__":
    main()

