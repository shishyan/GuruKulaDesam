import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('master_all_598_songs_catalog.json', encoding='utf-8') as f:
    catalog = {s['video_id']: s for s in json.load(f)}

try:
    with open('production/youtube_backup/videos.json', encoding='utf-8') as f:
        yt_videos = {v['id']: v for v in json.load(f)}
except Exception:
    yt_videos = {}

with open('production/youtube_lyrics_overrides.json', encoding='utf-8') as f:
    overrides = json.load(f)

works = overrides.get('_works', {})

print(f"Auditing {len(yt_videos)} videos from YouTube backup...")

errors = []

for vid, ytv in yt_videos.items():
    title = ytv['snippet'].get('title', '')
    desc = ytv['snippet'].get('description', '')
    cat = catalog.get(vid, {})
    
    # 1. Check title containing prompt text
    if 'create album cover' in title.lower() or 'prompt' in title.lower():
        errors.append({
            'video_id': vid,
            'title': title,
            'issue': 'Title contains raw generation prompt string instead of song title',
            'severity': 'HIGH'
        })
        
    # 2. Check Thigada vs Gananatha
    if 'திகட' in title and ('கணநாதா' in desc or 'gana natha' in desc.lower()):
        errors.append({
            'video_id': vid,
            'title': title,
            'issue': "Title says 'திகட சக்கர விநாயகர்' (Kandapuranam), but lyrics in description are 'Gana Natha Om'",
            'severity': 'HIGH'
        })
        
    # 3. Check Kandhar Anubhuti vs Skanda Mantram
    ov_ref = overrides.get(vid, {}).get('ref')
    if ('அநுபூதி' in title or 'anuboothi' in title.lower()) and ov_ref == 'skandamantram':
        errors.append({
            'video_id': vid,
            'title': title,
            'issue': "Title says 'கந்தர் அநுபூதி: உருவாய் அருவாய்', but audio/lyrics attached are Skanda Mantram",
            'severity': 'HIGH'
        })

    # 4. Check Thirukkural chapter title vs description chapter
    tm = re.search(r'அதிகாரம்\s*(\d+)', title)
    if tm:
        ch_title = int(tm.group(1))
        # Find chapter in description
        dm = re.findall(r'அதிகாரம்\s*(\d+)', desc)
        for dch in dm:
            if int(dch) != ch_title:
                errors.append({
                    'video_id': vid,
                    'title': title,
                    'issue': f"Title specifies Chapter {ch_title}, but description contains lyrics for Chapter {dch}",
                    'severity': 'CRITICAL'
                })
                break
                
    # 5. Check if lyrics in description belong to a different scripture
    if 'திருப்பாவை' in title and 'திருவெம்பாவை' in desc and 'திருப்பாவை' not in desc:
        errors.append({
            'video_id': vid,
            'title': title,
            'issue': "Title specifies Thiruppavai (Andal/Vishnu), but description has Thiruvempavai (Manikkavasagar/Shiva)",
            'severity': 'CRITICAL'
        })
        
    if 'திருவெம்பாவை' in title and 'திருப்பாவை' in desc and 'திருவெம்பாவை' not in desc:
        errors.append({
            'video_id': vid,
            'title': title,
            'issue': "Title specifies Thiruvempavai (Shiva), but description has Thiruppavai (Vishnu)",
            'severity': 'CRITICAL'
        })

print(f"\nTotal identified errors: {len(errors)}")
for idx, e in enumerate(errors, 1):
    print(f"\n{idx}. [{e['video_id']}] ({e['severity']}) {e['title']}")
    print(f"   --> {e['issue']}")

with open('production/wrong_lyrics_identified.json', 'w', encoding='utf-8') as f:
    json.dump(errors, f, indent=2, ensure_ascii=False)
