#!/usr/bin/env python3
"""Generate 4 composition-locked 16:9 Sacred Pink Indian Lotus blooming keyframes via backward i2i."""

import argparse
import subprocess
import sys
from pathlib import Path

KEYFRAMES_DIR = Path("/home/shishyan/GuruKulaDesam_Local/work/lotus_bloom_pilot/keyframes")
PROFILE = "nagaraj957"
MODEL = "nano-pro"
ASPECT = "16:9"

STAGE_SPECS = [
    {
        "name": "stage_04_full_bloom",
        "mode": "t2i",
        "ref": None,
        "out": KEYFRAMES_DIR / "stage_04_full_bloom.jpg",
        "prompt": (
            "Centered macro botanical photograph of a single sacred pink Indian lotus flower in "
            "glorious full bloom rising on a straight green stem above mirror-still dark emerald pond "
            "water at golden dawn, velvety rose-pink outer and inner petals wide open revealing a "
            "glowing golden-yellow stamen crown and seed pod center, tiny crystal morning dew droplets, "
            "warm golden rim lighting against a dreamy dark forest bokeh background, tripod-locked "
            "composition, pure macro botanical photography with zero text, watermarks, or UI icons"
        ),
    },
    {
        "name": "stage_03_half_open",
        "mode": "i2i",
        "ref": KEYFRAMES_DIR / "stage_04_full_bloom.jpg",
        "out": KEYFRAMES_DIR / "stage_03_half_open.jpg",
        "prompt": (
            "Keep the exact same tripod camera angle, exact same centered green stem position, exact "
            "same mirror-still dark emerald pond water, and exact same warm golden dawn bokeh "
            "background, but change ONLY the flower head into a half-open cupped pink lotus blossom: "
            "outer pink petals partially raised at a forty-five degree cup angle and inner pink petals "
            "curving inward loosely around the barely visible golden center, pure macro botanical "
            "photography with zero text, watermarks, or UI icons"
        ),
    },
    {
        "name": "stage_02_cracking_bud",
        "mode": "i2i",
        "ref": KEYFRAMES_DIR / "stage_03_half_open.jpg",
        "out": KEYFRAMES_DIR / "stage_02_cracking_bud.jpg",
        "prompt": (
            "Keep the exact same tripod camera angle, exact same centered green stem position, exact "
            "same mirror-still dark emerald pond water, and exact same warm golden dawn bokeh "
            "background, but change ONLY the flower head into a tall pointed rose-pink lotus bud "
            "just beginning to crack open slightly at the tip: outer green-edged rose sepals loosening "
            "by a few millimeters while all inner petals remain folded upright in a cone, pure macro "
            "botanical photography with zero text, watermarks, or UI icons"
        ),
    },
    {
        "name": "stage_01_tight_bud",
        "mode": "i2i",
        "ref": KEYFRAMES_DIR / "stage_02_cracking_bud.jpg",
        "out": KEYFRAMES_DIR / "stage_01_tight_bud.jpg",
        "prompt": (
            "Keep the exact same tripod camera angle, exact same centered green stem position, exact "
            "same mirror-still dark emerald pond water, and exact same warm golden dawn bokeh "
            "background, but change ONLY the flower head into a completely closed, compact pointed "
            "green-and-deep-rose lotus bud before blooming, tightly sealed tip beaded with tiny crystal "
            "morning dew droplets, zero open petals, pure macro botanical photography with zero text, "
            "watermarks, or UI icons"
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
    parser = argparse.ArgumentParser(description="Generate backward-i2i lotus keyframes.")
    parser.add_argument(
        "--stage",
        choices=[s["name"] for s in STAGE_SPECS],
        help="Generate only a single named stage (otherwise generates all 4 in reverse order).",
    )
    parser.add_argument("--profile", default=PROFILE, help="gflow profile name.")
    parser.add_argument("--skip-existing", action="store_true", help="Skip stages whose output PNG already exists.")
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
