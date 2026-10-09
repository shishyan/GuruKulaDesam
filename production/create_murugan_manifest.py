import os
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "production"))
from google_flow_engine import get_media_duration

releases_dir = ROOT / "renders" / "releases"
files = sorted([f for f in releases_dir.glob("murugan_*_master.mp4")])

manifest = {
    "category": "MURUGAN",
    "playlist_id": "PLcpX3K7ZFYjM",
    "playlist_name": "Lord Murugar Songs",
    "total_tracks": len(files),
    "completed_releases": len(files),
    "releases": []
}

for p in files:
    tid = p.name.replace("murugan_", "").replace("_master.mp4", "")
    sz = p.stat().st_size
    dur = get_media_duration(p)
    manifest["releases"].append({
        "track_id": tid,
        "hymn": "Kandhar Anubhuti: Uruvaai Aruvaai",
        "saint": "Arunagirinathar",
        "master_film": f"renders/releases/{p.name}",
        "file_size_bytes": sz,
        "file_size_mb": round(sz / (1024 * 1024), 2),
        "duration_sec": round(dur, 2),
        "scenes_count": 10,
        "resolution": "1280x720 24fps",
        "status": "READY_TO_UPLOAD"
    })

manifest_path = ROOT / "production" / "murugan_published_manifest.json"
with open(manifest_path, "w", encoding="utf-8") as out:
    json.dump(manifest, out, indent=2, ensure_ascii=False)

print(f"Created murugan_published_manifest.json with {len(manifest['releases'])} releases.")
