import sys
import json

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/youtube_backup/videos.json', encoding='utf-8') as f:
    videos = json.load(f)

missing_lyrics_section = []
for v in videos:
    vid = v['id']
    title = v['snippet']['title']
    desc = v['snippet']['description']
    
    # Check if this is an art track or normal upload
    if "provided to youtube by distrokid" in desc.lower():
        continue
        
    if "பாடல் வரிகள்" not in desc and "lyrics" not in desc.lower():
        missing_lyrics_section.append({
            'id': vid,
            'title': title,
            'desc_len': len(desc),
            'desc_snippet': desc[:100].replace('\n', ' ')
        })

print(f"Total videos missing explicit lyrics section: {len(missing_lyrics_section)}")
for item in missing_lyrics_section:
    print(f"[{item['id']}] {item['title']} (Desc len: {item['desc_len']})")
    print(f"   Snippet: {item['desc_snippet']}")
