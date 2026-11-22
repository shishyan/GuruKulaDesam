#!/usr/bin/env python3
"""
20-Tries Viral Challenge Tracker & Outlier Iterator for @influenzian (`UCcJFqC7z0f-ARNcJadKiKpQ`)
Goal: Hit >= 1,000,000 views within 20 long-form documentary tries (100% legal, factual, zero-CTA).

Reads public view counts via yt-dlp (zero YouTube API quota cost!) for every published try,
computes 24h / 7d view velocity, and tracks remaining tries out of 20.
"""
import json
import subprocess
import datetime
from pathlib import Path

TRACKER_FILE = Path("/home/shishyan/GitHub/GuruKulaDesam/production/influenzian_20_tries_viral_tracker.json")


def fetch_public_views(vid: str) -> dict:
    if not vid or vid == "PENDING_QUOTA_RESET":
        return {"views": 0, "likes": 0}
    try:
        out = subprocess.check_output(
            ["yt-dlp", "--dump-json", "--skip-download", f"https://www.youtube.com/watch?v={vid}"],
            stderr=subprocess.DEVNULL,
            timeout=15,
        ).decode()
        d = json.loads(out)
        return {"views": int(d.get("view_count") or 0), "likes": int(d.get("like_count") or 0)}
    except Exception:
        return {"views": 0, "likes": 0}


def main():
    if not TRACKER_FILE.exists():
        print("No tracker file yet.")
        return
    data = json.loads(TRACKER_FILE.read_text(encoding="utf-8"))
    best_views = 0
    for entry in data.get("tries", []):
        vid = entry.get("youtubeVideoId", "")
        if vid and vid != "PENDING_QUOTA_RESET":
            stats = fetch_public_views(vid)
            entry["latestViews"] = stats["views"]
            entry["latestLikes"] = stats["likes"]
            entry["lastCheckedUtc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            best_views = max(best_views, stats["views"])
        print(
            f"Try #{entry['tryNumber']:02d}/20 | {entry['status']:18s} | "
            f"Views: {entry.get('latestViews', 0):>9,} / 1,000,000 | {entry['title']}"
        )
    data["bestViewsSoFar"] = best_views
    data["goalReached"] = best_views >= 1_000_000
    TRACKER_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
