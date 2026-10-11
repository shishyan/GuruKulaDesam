#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
enrich_missing_thirukkural_lyrics.py
Enriches all missing Thirukkural tracks in production/metadata/all_songs_lyrics_and_meanings.json
using canonical Kurals from production/thirukkural_all.json.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LYRICS_DB_FILE = ROOT / "production" / "metadata" / "all_songs_lyrics_and_meanings.json"
THIRUKKURAL_ALL_FILE = ROOT / "production" / "thirukkural_all.json"
AUDIT_REPORT_FILE = ROOT / "production" / "lyrics_audit_report.json"

def main():
    with open(THIRUKKURAL_ALL_FILE, "r", encoding="utf-8") as f:
        tk_data = json.load(f)
    kurals_by_num = {item["Number"]: item for item in tk_data["kural"]}

    with open(LYRICS_DB_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)

    with open(AUDIT_REPORT_FILE, "r", encoding="utf-8") as f:
        audit = json.load(f)

    missing_tracks = audit.get("missing", [])
    print(f"Found {len(missing_tracks)} missing tracks to evaluate.")

    enriched_count = 0
    for item in missing_tracks:
        tid = item["track_id"]
        title = item["title"]

        # Extract chapter number
        match = re.search(r"அதிகாரம்\s*(\d+)", title)
        if not match:
            continue
        ch_num = int(match.group(1))
        start_kural = (ch_num - 1) * 10 + 1
        end_kural = ch_num * 10

        lyrics_lines = []
        meanings_lines = []
        english_lines = []

        for kn in range(start_kural, end_kural + 1):
            kd = kurals_by_num.get(kn)
            if kd:
                lyrics_lines.append(f"குறள் {kn}:")
                lyrics_lines.append(kd["Line1"])
                lyrics_lines.append(kd["Line2"])
                lyrics_lines.append("")

                meanings_lines.append(f"குறள் {kn}: {kd.get('mv') or kd.get('mk') or kd.get('sp')}")
                english_lines.append(f"Kural {kn}: {kd.get('couplet', '')}\n  Meaning: {kd.get('explanation', '')}")

        tamil_lyrics = "\n".join(lyrics_lines).strip()
        tamil_meaning = "\n\n".join(meanings_lines).strip()
        english_meaning = "\n\n".join(english_lines).strip()

        if tid not in db:
            db[tid] = {
                "video_id": tid,
                "title": title,
                "author": "திருவள்ளுவர் (Thiruvalluvar)",
                "genre": "திருக்குறள் (Thirukkural)",
            }

        db[tid]["tamil_lyrics"] = tamil_lyrics
        db[tid]["tamil_meaning"] = tamil_meaning
        db[tid]["english_meaning"] = english_meaning
        db[tid]["author"] = "திருவள்ளுவர் (Thiruvalluvar)"
        db[tid]["genre"] = "திருக்குறள் (Thirukkural)"

        print(f"Enriched {tid} (Chapter {ch_num}): Kurals {start_kural}-{end_kural}")
        enriched_count += 1

    with open(LYRICS_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    print(f"\nSuccessfully enriched {enriched_count} Thirukkural tracks in {LYRICS_DB_FILE}!")

if __name__ == "__main__":
    main()
