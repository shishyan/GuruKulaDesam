import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    meta = json.load(f)

print(f"Total videos in live_youtube_metadata.json: {len(meta)}")

# Let's check production/channel_all_videos_full_audit.json if it exists
full_audit = {}
if os.path.exists('production/channel_all_videos_full_audit.json'):
    with open('production/channel_all_videos_full_audit.json', 'r', encoding='utf-8') as f:
        full_audit = json.load(f)
    print(f"Total videos in production/channel_all_videos_full_audit.json: {len(full_audit)}")

# Let's inspect production/youtube_backup/videos.json
backup_videos = []
if os.path.exists('production/youtube_backup/videos.json'):
    with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
        backup_videos = json.load(f)
    print(f"Total videos in production/youtube_backup/videos.json: {len(backup_videos)}")

# Let's analyze types of videos in meta:
kurals = 0
devotional = 0
shorts = 0
audio_releases = 0
others = 0

for vid, item in meta.items():
    title = item.get('title', '')
    desc = item.get('description', '')
    dur = item.get('duration', '')
    
    if "குறள்" in title or "Thirukkural" in title or "Kural" in title:
        kurals += 1
    elif any(w in title for w in ["திருப்புகழ்", "திருப்பாவை", "திருவெம்பாவை", "திருவாசகம்", "திருவருட்பா", "விநாயகர்", "கந்தபுராணம்", "சிவன்", "பக்தி"]):
        devotional += 1
    else:
        others += 1

print("\n--- Content Breakdown ---")
print(f"Thirukkural Videos (Kurals / Athikarams): {kurals}")
print(f"Devotional Songs / Hymns: {devotional}")
print(f"Other Tracks: {others}")

# Let's check production/subtitles/ and production/thumbnails/ coverage
sub_count = 0
thumb_count = 0
for vid in meta.keys():
    if os.path.exists(f"production/subtitles/{vid}.srt"):
        sub_count += 1
    if os.path.exists(f"production/thumbnails/{vid}.png"):
        thumb_count += 1

print(f"\nCoverage across ALL {len(meta)} videos:")
print(f"SRT files in production/subtitles/: {sub_count} / {len(meta)}")
print(f"Thumbnail PNGs in production/thumbnails/: {thumb_count} / {len(meta)}")
