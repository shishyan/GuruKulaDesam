import json
import sys

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

# Update youtube_backup/videos.json and master_all_598_songs_catalog.json
with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    backup_videos = json.load(f)

# Load canonical overrides
with open('production/youtube_lyrics_overrides.json', 'r', encoding='utf-8') as f:
    overrides = json.load(f)

works = overrides.get('_works', {})

UPDATES = {
    "uPk4dyag74Y": ("thigada", "திகட சக்கரச் செம்முக மைந்துளான்..."),
    "_eG3rWRIvJo": ("thigada", "திகட சக்கரச் செம்முக மைந்துளான்..."),
    "udRsA-oWxS0": ("pancharatnam", "முதாகராத்த மோதகம்... (5 Verses Complete)"),
    "iXHNzqOrxzw": ("pancharatnam", "முதாகராத்த மோதகம்... (5 Verses Complete)"),
    "qPjurMK6xpI": ("pancharatnam", "முதாகராத்த மோதகம்... (5 Verses Complete)"),
    "mPypwIgdo-E": ("thirupulambal", "பூங்கமலத் தயனொடுமால்..."),
    "g42Pg2sg_gg": ("vedasara", "பசூநாம் பதிம் பாபநாசம்..."),
    "rRoJfeRQiaM": ("thiruvaiyaru", "மாதர்ப் பிறைக் கண்ணியானை..."),
    "jZFTlpJwn6A": ("thiyaga_vanna_pathigam", "காரார் குழலாள் உமையோ..."),
    "FGeahfpAbiw": ("anbu_maalai", "அற்புதப் பொன் அம்பலத்தே...")
}

count = 0
for v in backup_videos:
    vid = v.get('id')
    if vid in UPDATES:
        work_key, snippet = UPDATES[vid]
        w = works.get(work_key, {})
        v['snippet']['canonical_verified'] = True
        v['snippet']['canonical_work'] = work_key
        count += 1

with open('production/youtube_backup/videos.json', 'w', encoding='utf-8') as f:
    json.dump(backup_videos, f, indent=2, ensure_ascii=False)

print(f"Updated {count} records in production/youtube_backup/videos.json")
