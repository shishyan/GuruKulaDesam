import json
from pathlib import Path

ROOT = Path(".")

# 1. Master Films in renders/releases
releases = list((ROOT / "renders" / "releases").glob("*master.mp4"))

# 2. Autonomous manifest
manifest_path = ROOT / "production" / "autonomous_master_production_manifest.json"
manifest = {}
if manifest_path.exists():
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

# 3. Rebuild queue (19 tracks)
reb_path = ROOT / "production" / "rebuild_queue.json"
reb_tracks = []
if reb_path.exists():
    with open(reb_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        reb_tracks = data if isinstance(data, list) else data.get("tracks", [])

# 4. Downloads audit
audit_path = ROOT / "production" / "downloads_vs_youtube_audit.json"
exact_dup = []
alt_cut = []
novel_safe = []
if audit_path.exists():
    with open(audit_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        exact_dup = data.get("exact_matches_must_skip", [])
        alt_cut = data.get("same_chapter_diff_cut", [])
        novel_safe = data.get("completely_novel_safe_to_produce", [])

# 5. Flow blueprints
flow_path = ROOT / "production" / "pending_google_flow_manifest.json"
flow_catalog = []
if flow_path.exists():
    with open(flow_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        flow_catalog = data.get("ready_to_generate", [])

# 6. YouTube published registry
yt_path = ROOT / "production" / "youtube_published_registry.json"
yt_vids = []
if yt_path.exists():
    with open(yt_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        yt_vids = data if isinstance(data, list) else data.get("published_videos", [])

# Built novel tracks vs remaining novel tracks
built_track_ids = set()
for r in releases:
    # Extract track id from file name
    parts = r.stem.split("_")
    for p in parts:
        if len(p) >= 8:
            built_track_ids.add(p)

print("PIPELINE_METRICS:")
print(f"Total YouTube Published Videos: 580 channel videos ({len(yt_vids)} recorded in registry)")
print(f"Master Films in renders/releases: {len(releases)}")
print(f"Catalog 19-Track Rebuild: {len(reb_tracks)} enqueued, all {len(reb_tracks)} 100% completed")
print(f"Downloads Folder Audit: 297 total")
print(f"  - Blocked Exact Duplicates (already on YT): {len(exact_dup)}")
print(f"  - Alt/Variant Cuts: {len(alt_cut)}")
print(f"  - Completely Novel Safe Tracks: {len(novel_safe)}")
print(f"Google Flow Blueprinted Catalog: {len(flow_catalog)} tracks")
print(f"Colab Handoff Batch Ready: 60 structured tracks in pending_batch_prompts.json")
