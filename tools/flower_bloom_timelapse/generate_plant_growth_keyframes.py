#!/usr/bin/env python3
"""Generate 5 composition-locked 16:9 Dwarf Golden Sunflower plant-growth keyframes via backward i2i."""

import argparse
import subprocess
import sys
from pathlib import Path

KEYFRAMES_DIR = Path("/home/shishyan/GuruKulaDesam_Local/work/plant_growth_pilot/keyframes")
PROFILE = "nagaraj957"
MODEL = "nano-pro"
ASPECT = "16:9"

STAGE_SPECS = [
    {
        "name": "stage_05_full_bloom",
        "mode": "t2i",
        "ref": None,
        "out": KEYFRAMES_DIR / "stage_05_full_bloom.jpg",
        "prompt": (
            "Wide-medium botanical photograph of a single compact dwarf golden sunflower plant standing "
            "in full bloom on a dark moist forest-soil mound at the bottom of the frame, flanked by two "
            "small mossy stones on the left and right soil edges, sturdy green stem with six lush "
            "serrated green leaves rising vertically in the center and crowned with one radiant "
            "wide-open golden-yellow sunflower blossom with a rich dark-amber spiral center, generous "
            "dark emerald woodland bokeh headroom above the flower, warm golden dawn sunbeams from the "
            "right, tripod-locked composition, pure botanical nature photography with zero text, "
            "watermarks, or UI icons"
        ),
    },
    {
        "name": "stage_04_opening_bud",
        "mode": "i2i",
        "ref": KEYFRAMES_DIR / "stage_05_full_bloom.jpg",
        "out": KEYFRAMES_DIR / "stage_04_opening_bud.jpg",
        "prompt": (
            "Keep the exact same tripod camera framing, exact same dark moist soil mound and two small "
            "mossy stones at the bottom, exact same green stem and six green leaves, and exact same warm "
            "golden dawn woodland bokeh background, but change ONLY the top flower head into a "
            "half-open sunflower bud: pointed green outer bracts peeling back while bright "
            "golden-yellow petals remain cupped upward at a forty-five degree angle partially hiding "
            "the dark center, pure botanical nature photography with zero text, watermarks, or UI icons"
        ),
    },
    {
        "name": "stage_03_green_bud_stem",
        "mode": "i2i",
        "ref": KEYFRAMES_DIR / "stage_04_opening_bud.jpg",
        "out": KEYFRAMES_DIR / "stage_03_green_bud_stem.jpg",
        "prompt": (
            "Keep the exact same tripod camera framing, exact same dark moist soil mound and two small "
            "mossy stones at the bottom, exact same stem base position, and exact same warm golden dawn "
            "woodland bokeh background, but make the sunflower plant slightly shorter at about "
            "three-quarters height with fresh green leaves and a completely closed spiky green "
            "star-shaped flower bud at the top crown with zero yellow petals showing yet, pure "
            "botanical nature photography with zero text, watermarks, or UI icons"
        ),
    },
    {
        "name": "stage_02_young_seedling",
        "mode": "i2i",
        "ref": KEYFRAMES_DIR / "stage_03_green_bud_stem.jpg",
        "out": KEYFRAMES_DIR / "stage_02_young_seedling.jpg",
        "prompt": (
            "Keep the exact same tripod camera framing, exact same dark moist soil mound and two small "
            "mossy stones at the bottom, exact same stem root spot in the center of the soil, and "
            "exact same warm golden dawn woodland bokeh background, but shrink the plant down into a "
            "short young green sunflower seedling only one-third as tall: a slender fuzzy green stem "
            "with just four small bright-green leaves and zero flower bud, wide empty golden-lit forest "
            "bokeh space above the young seedling, pure botanical nature photography with zero text, "
            "watermarks, or UI icons"
        ),
    },
    {
        "name": "stage_01_tiny_sprout",
        "mode": "i2i",
        "ref": KEYFRAMES_DIR / "stage_02_young_seedling.jpg",
        "out": KEYFRAMES_DIR / "stage_01_tiny_sprout.jpg",
        "prompt": (
            "Keep the exact same tripod camera framing, exact same dark moist soil mound and two small "
            "mossy stones at the bottom, exact same center emergence point in the soil, and exact same "
            "warm golden dawn woodland bokeh background, but shrink the seedling all the way down into "
            "a tiny newborn green sprout barely emerging an inch above the moist dark soil with just "
            "two tiny dew-covered baby cotyledon leaves, leaving the entire upper space as empty warm "
            "golden woodland bokeh, pure botanical nature photography with zero text, watermarks, or UI icons"
        ),
    },
]


def run_stage(spec: dict, profile: str) -> None:
    out_path: Path = spec["out"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if spec["mode"] == "t2i":
        cmd = [
            "gflow-headless",
            "image",
            "t2i",
            spec["prompt"],
            "--profile",
            profile,
            "--aspect",
            ASPECT,
            "--model",
            MODEL,
            "--out-file",
            str(out_path),
        ]
    else:
        ref_path: Path = spec["ref"]
        if not ref_path.exists():
            raise FileNotFoundError(f"Missing reference image: {ref_path}")
        cmd = [
            "gflow-headless",
            "image",
            "i2i",
            spec["prompt"],
            "--ref",
            str(ref_path),
            "--profile",
            profile,
            "--aspect",
            ASPECT,
            "--model",
            MODEL,
            "--out-file",
            str(out_path),
        ]

    print(f"=== Generating {spec['name']} ({spec['mode']}) -> {out_path} ===", flush=True)
    res = subprocess.run(cmd, check=False)
    if res.returncode != 0:
        raise RuntimeError(f"gflow-headless failed for {spec['name']} (exit {res.returncode})")
    if not out_path.exists() or out_path.stat().st_size == 0:
        raise RuntimeError(f"Expected output file missing or empty: {out_path}")
    print(f"OK: {out_path} ({out_path.stat().st_size} bytes)", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate backward-i2i plant growth keyframes.")
    parser.add_argument(
        "--stage",
        choices=[s["name"] for s in STAGE_SPECS],
        help="Generate only a single named stage (otherwise generates all 5 in reverse order).",
    )
    parser.add_argument("--profile", default=PROFILE, help="gflow profile name.")
    parser.add_argument("--skip-existing", action="store_true", help="Skip stages whose output JPG already exists.")
    args = parser.parse_args()

    specs = [s for s in STAGE_SPECS if args.stage is None or s["name"] == args.stage]
    for spec in specs:
        if args.skip_existing and spec["out"].exists() and spec["out"].stat().st_size > 0:
            print(f"Skipping existing {spec['out']}", flush=True)
            continue
        run_stage(spec, args.profile)
    return 0


if __name__ == "__main__":
    sys.exit(main())
