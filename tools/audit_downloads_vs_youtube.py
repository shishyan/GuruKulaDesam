#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guru Kula Desam (@guru-kula-desam)
Downloads Audio Library vs. Live YouTube Catalog Deduplication Auditor

Strictly enforces USER DIRECTIVE:
"remember, those songs in downloads folder may already be there in youtube, so dont duplicate it."
"""

import os
import sys
import re
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META_FILE = ROOT / "live_youtube_metadata.json"
REGISTRY_FILE = ROOT / "production" / "youtube_published_registry.json"
DOWNLOADS_DIR = Path(r"C:\Users\Shishyan\Downloads")
REPORT_FILE = ROOT / "production" / "downloads_vs_youtube_audit.json"
FFPROBE = "C:/ffmpeg/bin/ffprobe.exe"

def parse_iso_duration(dur_str: str) -> float:
    if not dur_str:
        return 0.0
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", dur_str)
    if not m:
        return 0.0
    h, m_val, s = m.groups()
    total = 0.0
    if h:
        total += int(h) * 3600
    if m_val:
        total += int(m_val) * 60
    if s:
        total += int(s)
    return total

def get_audio_duration(path: Path) -> float:
    cmd = [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path)
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())
    except Exception:
        return 0.0

def extract_tamil_keywords(text: str) -> set:
    return set(re.findall(r"[\u0B80-\u0BFF]{3,}", text))

def main():
    print("=" * 80)
    print("GURU KULA DESAM — DOWNLOADS vs. YOUTUBE DEDUPLICATION AUDIT")
    print("=" * 80)

    if not META_FILE.exists():
        print(f"[Error] Metadata file not found: {META_FILE}")
        return

    with open(META_FILE, "r", encoding="utf-8") as f:
        meta = json.load(f)

    # Build index of YouTube videos
    yt_index = []
    for yid, data in meta.items():
        dur_str = data.get("duration", "")
        dur_sec = parse_iso_duration(dur_str)
        title = data.get("title", "")
        yt_index.append({
            "youtube_id": yid,
            "title": title,
            "duration_sec": dur_sec,
            "duration_str": dur_str,
            "published_at": data.get("publishedAt", ""),
            "tamil_words": extract_tamil_keywords(title)
        })

    print(f"Loaded {len(yt_index)} existing YouTube videos from live catalog.")

    audio_files = sorted(
        list(DOWNLOADS_DIR.glob("*.wav")) +
        list(DOWNLOADS_DIR.glob("*.mp3")) +
        list(DOWNLOADS_DIR.glob("*.m4a"))
    )
    print(f"Found {len(audio_files)} audio files in {DOWNLOADS_DIR}")
    print("Probing audio durations and cross-referencing against YouTube...")

    exact_matches = []
    same_chapter_diff_cut = []
    completely_novel = []

    for idx, f in enumerate(audio_files, 1):
        stem = f.stem
        dur = get_audio_duration(f)
        words = extract_tamil_keywords(stem)

        # 1. Check for exact title keyword match + duration within +/- 4 seconds
        matched = False
        for y in yt_index:
            common = words.intersection(y["tamil_words"])
            if common:
                diff = abs(y["duration_sec"] - dur)
                if diff <= 4.0:
                    exact_matches.append({
                        "file_name": f.name,
                        "file_path": str(f),
                        "file_duration_sec": round(dur, 2),
                        "matched_youtube_id": y["youtube_id"],
                        "matched_youtube_title": y["title"],
                        "matched_youtube_duration": round(y["duration_sec"], 2),
                        "matched_keywords": list(common),
                        "duration_diff_sec": round(diff, 2),
                        "action": "SKIP_DO_NOT_DUPLICATE"
                    })
                    matched = True
                    break

        if not matched:
            # 2. Check if chapter/keyword exists on YouTube but with different length
            kw_matches = [y for y in yt_index if words.intersection(y["tamil_words"])]
            if kw_matches:
                same_chapter_diff_cut.append({
                    "file_name": f.name,
                    "file_path": str(f),
                    "file_duration_sec": round(dur, 2),
                    "candidate_youtube_matches": [
                        {
                            "youtube_id": y["youtube_id"],
                            "title": y["title"],
                            "duration_sec": round(y["duration_sec"], 2)
                        } for y in kw_matches[:3]
                    ],
                    "action": "REVIEW_OR_ALTERNATE_VERSION"
                })
            else:
                completely_novel.append({
                    "file_name": f.name,
                    "file_path": str(f),
                    "file_duration_sec": round(dur, 2),
                    "action": "SAFE_TO_PRODUCE_NOVEL"
                })

        if idx % 50 == 0 or idx == len(audio_files):
            print(f"  Processed {idx}/{len(audio_files)} files...")

    print("\n" + "=" * 80)
    print("DEDUPLICATION AUDIT SUMMARY:")
    print(f"  Total Audio Files in Downloads : {len(audio_files)}")
    print(f"  1. EXACT MATCHES on YouTube    : {len(exact_matches)} (ALREADY PUBLISHED -> MUST SKIP)")
    print(f"  2. SAME CHAPTER / DIFFERENT CUT: {len(same_chapter_diff_cut)} (Potential remix/alt cuts)")
    print(f"  3. COMPLETELY NOVEL (Not on YT): {len(completely_novel)} (Brand new songs never on YT)")
    print("=" * 80)

    report = {
        "summary": {
            "total_downloads_files": len(audio_files),
            "exact_matches_count": len(exact_matches),
            "same_chapter_diff_cut_count": len(same_chapter_diff_cut),
            "completely_novel_count": len(completely_novel)
        },
        "exact_matches_must_skip": exact_matches,
        "same_chapter_diff_cut": same_chapter_diff_cut,
        "completely_novel_safe_to_produce": completely_novel
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Audit report saved to: {REPORT_FILE}")

if __name__ == "__main__":
    main()
