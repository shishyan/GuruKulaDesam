import sys
import os
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('production/channel_sync_progress.json', 'r', encoding='utf-8') as f:
    synced = json.load(f)

print(f"Total synced: {len(synced)}")

# Check some recently synced videos
sample_vids = ['NK2PqzKz3aI', 'XErAOEtZdAU', '2tL-bKjkL18', 'kFmUrNPXsso', 'MTvDDAQCFmk', 'nuSx1NgiCuo']
for vid in sample_vids:
    path = f"production/subtitles/{vid}.srt"
    if os.path.exists(path):
        print(f"\n==================== {vid} ====================")
        with open(path, 'r', encoding='utf-8') as f:
            print(f.read()[:500])
