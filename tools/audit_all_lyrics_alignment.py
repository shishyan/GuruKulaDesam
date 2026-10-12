#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_all_lyrics_alignment.py
Performs a comprehensive audit of all tracks across catalog, manifest, and DB:
1. Resolved lyrics via get_track_lyrics(track_id)
2. Empty or missing lyrics
3. Cross-deity mismatches (e.g. Vinayagar lyrics on Murugan/Shiva/Amman tracks)
4. Title vs lyric alignment (e.g. 'Natha Vinthugal' having Ganesha lyrics or 'Gana Natha' having Murugan lyrics)
5. Overrides vs DB consistency
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LYRICS_DB_FILE = ROOT / "production" / "metadata" / "all_songs_lyrics_and_meanings.json"
LYRICS_OVERRIDE_FILE = ROOT / "production" / "youtube_lyrics_overrides.json"
CATALOG_FILE = ROOT / "assets" / "data" / "catalog.json"
MANIFEST_FILE = ROOT / "production" / "autonomous_master_production_manifest.json"

def get_resolved_lyrics(track_id: str, overrides: dict, lyrics_db: dict) -> tuple[str, str]:
    """Returns (lyrics, source_type)."""
    if track_id in overrides:
        entry = overrides[track_id]
        if isinstance(entry, dict):
            if entry.get("lyrics"):
                return entry["lyrics"].strip(), "override_direct"
            if entry.get("ref") and "_works" in overrides and entry["ref"] in overrides["_works"]:
                return overrides["_works"][entry["ref"]].get("lyrics", "").strip(), f"override_ref:{entry['ref']}"

    if track_id in lyrics_db and isinstance(lyrics_db[track_id], dict) and lyrics_db[track_id].get("tamil_lyrics"):
        return lyrics_db[track_id]["tamil_lyrics"].strip(), "lyrics_db"

    return "", "missing"

def main():
    overrides = json.load(open(LYRICS_OVERRIDE_FILE, "r", encoding="utf-8")) if LYRICS_OVERRIDE_FILE.exists() else {}
    lyrics_db = json.load(open(LYRICS_DB_FILE, "r", encoding="utf-8")) if LYRICS_DB_FILE.exists() else {}
    catalog_raw = json.load(open(CATALOG_FILE, "r", encoding="utf-8")) if CATALOG_FILE.exists() else {}
    manifest_raw = json.load(open(MANIFEST_FILE, "r", encoding="utf-8")) if MANIFEST_FILE.exists() else {}

    # Flatten catalog
    all_tracks = {}
    if isinstance(catalog_raw, dict):
        for cat_name, items in catalog_raw.items():
            if isinstance(items, list):
                for item in items:
                    tid = item.get("id") or item.get("track_id") or item.get("youtube_id")
                    if tid:
                        item["catalog_category"] = cat_name
                        all_tracks[tid] = item
    elif isinstance(catalog_raw, list):
        for item in catalog_raw:
            tid = item.get("id") or item.get("track_id") or item.get("youtube_id")
            if tid:
                all_tracks[tid] = item

    # Flatten manifest
    manifest_tracks = {}
    if isinstance(manifest_raw, dict) and "completed_tracks" in manifest_raw:
        for ct in manifest_raw["completed_tracks"]:
            tid = ct.get("track_id")
            if tid:
                manifest_tracks[tid] = ct

    print(f"Loaded: Overrides={len(overrides)}, DB={len(lyrics_db)}, Catalog={len(all_tracks)}, Manifest={len(manifest_tracks)}")

    # Deity signature keywords
    KEYWORD_CHECKS = [
        # (pattern, expected_deity, forbidden_deities, label)
        (r"கைத்தல\s*நிறைகனி|முதாகராத்த|மோதகம்|கணபதி|விகட\s*சக்கரன்|கண\s*நாதா", "vinayagar", ["murugan", "shiva", "amman", "vishnu", "thirukkural"], "Vinayagar Hymn"),
        (r"நாத\s*விந்து|முத்தைத்\s*தரு|சீர்\s*உலாவிய|கந்தர்|சரவண|முருக|ஆறுமுக|வேலவ|குமரா", "murugan", ["vinayagar", "amman", "vishnu", "thirukkural"], "Murugan Hymn"),
        (r"நமச்சிவாய|பொன்னார்\s*மேனியனே|மாசில்\s*வீணையும்|சிவ\s*சிவ|ஈஸ்வர|தில்லை|திருவெம்பாவை|ஆடலமுத", "shiva", ["vinayagar", "amman", "vishnu", "thirukkural"], "Shiva Hymn"),
        (r"அபிராமி|சமயபுர|மாரியம்மன்|காளி|துர்க்கை|ரேணுகா|தாயே", "amman", ["vinayagar", "murugan", "thirukkural"], "Amman Hymn"),
        (r"நாராயண|கிருஷ்ண|ராமா|கோவிந்த|மாதவா|திருப்பாவை|ஆண்டாள்|பெரியாழ்வார்", "vishnu", ["vinayagar", "murugan", "shiva", "thirukkural"], "Vishnu Hymn"),
        (r"அருட்பெருஞ்சோதி|வள்ளலார்|ராமலிங்க|திருவருட்பா", "vallalar", ["vinayagar", "murugan", "amman", "vishnu", "thirukkural"], "Vallalar Hymn"),
        (r"அகர\s*முதல|குறள்|துப்பார்க்குத்|கற்க\s*கசடற", "thirukkural", ["vinayagar", "murugan", "shiva", "amman", "vishnu", "vallalar"], "Thirukkural"),
    ]

    missing_lyrics = []
    suspicious_mismatches = []
    audited_ok = []

    track_ids_to_audit = set(manifest_tracks.keys()) | set(all_tracks.keys()) | set(lyrics_db.keys())

    for tid in sorted(track_ids_to_audit):
        cat_info = all_tracks.get(tid, {})
        db_info = lyrics_db.get(tid, {})
        man_info = manifest_tracks.get(tid, {})

        title = cat_info.get("title") or db_info.get("title") or man_info.get("title") or "Unknown"
        deity = (cat_info.get("category") or cat_info.get("catalog_category") or man_info.get("category") or "").lower()

        lyrics, source = get_resolved_lyrics(tid, overrides, lyrics_db)

        if not lyrics:
            missing_lyrics.append({"track_id": tid, "title": title, "deity": deity})
            continue

        first_couplet = " ".join([l.strip() for l in lyrics.splitlines() if l.strip()][:2])
        mismatch_found = False

        # 1. Title vs Lyric checks
        if ("நாத விந்து" in title or "natha vindhu" in title.lower() or "naadha" in title.lower()) and "நாத விந்து" not in lyrics:
            suspicious_mismatches.append({
                "track_id": tid, "title": title, "deity": deity, "source": source,
                "reason": "Title is 'Natha Vinthugal' but lyrics do not contain 'நாத விந்து'!",
                "first_couplet": first_couplet
            })
            mismatch_found = True

        if ("கைத்தல" in title or "kaithala" in title.lower()) and "கைத்தல" not in lyrics:
            suspicious_mismatches.append({
                "track_id": tid, "title": title, "deity": deity, "source": source,
                "reason": "Title is 'Kaithala Nirai Kani' but lyrics do not contain 'கைத்தல'!",
                "first_couplet": first_couplet
            })
            mismatch_found = True

        if ("சீர் உலாவிய" in title or "seer ulaaviya" in title.lower()) and "சீர் உலா" not in lyrics:
            suspicious_mismatches.append({
                "track_id": tid, "title": title, "deity": deity, "source": source,
                "reason": "Title is 'Seer Ulaaviya' but lyrics do not contain 'சீர் உலா'!",
                "first_couplet": first_couplet
            })
            mismatch_found = True

        if ("முத்தைத் தரு" in title or "muthaith" in title.lower()) and "முத்தைத்" not in lyrics:
            suspicious_mismatches.append({
                "track_id": tid, "title": title, "deity": deity, "source": source,
                "reason": "Title is 'Muthaith Tharu' but lyrics do not contain 'முத்தைத்'!",
                "first_couplet": first_couplet
            })
            mismatch_found = True

        if ("அகர முதல" in title or "agara mudhala" in title.lower()) and "அகர முதல" not in lyrics:
            suspicious_mismatches.append({
                "track_id": tid, "title": title, "deity": deity, "source": source,
                "reason": "Title is 'Agara Mudhala' but lyrics mismatch!",
                "first_couplet": first_couplet
            })
            mismatch_found = True

        # 2. Deity vs Lyric checks
        if deity:
            # Check specifically for Vinayagar lyrics mistakenly placed on Murugan / Shiva songs
            if deity == "murugan" and ("கைத்தல நிறைகனி" in lyrics or "முதாகராத்த" in lyrics):
                if "கைத்தல" not in title and "kaithala" not in title.lower():
                    suspicious_mismatches.append({
                        "track_id": tid, "title": title, "deity": deity, "source": source,
                        "reason": "Murugan track bound to Vinayagar lyrics (கைத்தல நிறைகனி / முதாகராத்த)!",
                        "first_couplet": first_couplet
                    })
                    mismatch_found = True
            elif deity == "shiva" and ("கைத்தல நிறைகனி" in lyrics or "முதாகராத்த" in lyrics):
                suspicious_mismatches.append({
                    "track_id": tid, "title": title, "deity": deity, "source": source,
                    "reason": "Shiva track bound to Vinayagar lyrics!",
                    "first_couplet": first_couplet
                })
                mismatch_found = True
            elif deity == "amman" and ("கைத்தல நிறைகனி" in lyrics or "முதாகராத்த" in lyrics):
                suspicious_mismatches.append({
                    "track_id": tid, "title": title, "deity": deity, "source": source,
                    "reason": "Amman track bound to Vinayagar lyrics!",
                    "first_couplet": first_couplet
                })
                mismatch_found = True
            elif deity == "thirukkural" and not any(kw in lyrics for kw in ["குறள்", "அகர", "என்ப", "செயற்கரிய", "துப்பார்க்கு"]):
                suspicious_mismatches.append({
                    "track_id": tid, "title": title, "deity": deity, "source": source,
                    "reason": "Thirukkural track bound to non-Thirukkural lyrics!",
                    "first_couplet": first_couplet
                })
                mismatch_found = True

        if not mismatch_found:
            audited_ok.append({"track_id": tid, "title": title, "deity": deity, "source": source})

    print(f"\n==========================================")
    print(f"AUDIT SUMMARY:")
    print(f"Total Unique Tracks Audited: {len(track_ids_to_audit)}")
    print(f"Clean & Aligned: {len(audited_ok)}")
    print(f"Suspicious Mismatches: {len(suspicious_mismatches)}")
    print(f"Missing Lyrics: {len(missing_lyrics)}")
    print(f"==========================================\n")

    if suspicious_mismatches:
        print(f"--- {len(suspicious_mismatches)} MISMATCHES DETECTED ---")
        for idx, item in enumerate(suspicious_mismatches, 1):
            print(f"[{idx}] Track ID: {item['track_id']} | Deity: {item['deity']}")
            print(f"    Title: {item['title']}")
            print(f"    Reason: {item['reason']}")
            print(f"    Source: {item['source']}")
            print(f"    First Couplet: {item['first_couplet'][:80]}...")
            print("-" * 60)

    # Dump full report
    report = {
        "summary": {
            "total": len(track_ids_to_audit),
            "ok": len(audited_ok),
            "mismatches": len(suspicious_mismatches),
            "missing": len(missing_lyrics)
        },
        "mismatches": suspicious_mismatches,
        "missing": missing_lyrics,
        "ok": audited_ok
    }
    out_file = ROOT / "production" / "lyrics_audit_report.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\nWrote full report to {out_file}")

if __name__ == "__main__":
    main()
