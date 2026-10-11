import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# Load files
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

print(f"Total videos in YouTube backup: {len(yt_videos)}")

flagged = []

for vid, ytv in yt_videos.items():
    sn = ytv.get('snippet', {})
    title = sn.get('title', '')
    desc = sn.get('description', '')
    cat_entry = catalog.get(vid, {})
    genre = cat_entry.get('genre', '')
    
    ov_ref = overrides.get(vid, {}).get('ref')
    ov_work = works.get(ov_ref, {}) if ov_ref else None
    
    # Check overrides status
    if ov_work and ov_work.get('status') == 'needs_audio_check':
        # Check source notes
        src_note = ov_work.get('source', '')
        if 'wrongly held' in src_note or 'Catalog had verse 1 only' in src_note:
            flagged.append({
                'video_id': vid,
                'title': title,
                'type': 'KNOWN_OVERRIDE_FLAG',
                'issue': f"Work '{ov_ref}' has note: {src_note}",
                'lyrics_sample': ov_work.get('lyrics', '')[:80].replace('\n', ' ')
            })

    # 1. Check Kandhar Anubhuti titled videos having Skanda Mantram lyrics
    if 'அநுபூதி' in title or 'anuboothi' in title.lower() or 'anubhuti' in title.lower():
        if ov_ref == 'skandamantram' or ('காயத்ரி' in desc and 'உருவாய்' not in desc):
            flagged.append({
                'video_id': vid,
                'title': title,
                'type': 'WRONG_WORK_ATTACHED',
                'issue': "Video is titled Kandhar Anubhuti (உருவாய் அருவாய்), but lyrics/override is Skanda Mantram (காயத்ரி மந்திரம்)",
                'lyrics_sample': desc[:100].replace('\n', ' ')
            })

    # 2. Check Vinayagar Thigada Chakkara holding Gana Natha Om
    if 'திகட' in title or 'thigada' in title.lower():
        if 'கணநாதா' in desc or 'gana natha' in desc.lower():
            flagged.append({
                'video_id': vid,
                'title': title,
                'type': 'WRONG_WORK_ATTACHED',
                'issue': "Video is titled Thigada Chakkara (திகட சக்கரம்), but description/lyrics contain 'Gana Natha Om'",
                'lyrics_sample': desc[:100].replace('\n', ' ')
            })

    # 3. Check Deity mismatch: Murugan title with Shiva lyrics, or vice versa
    if 'விநாயக' in title or 'vinayagar' in title.lower() or 'ganesha' in title.lower():
        if 'முருக' in desc and 'விநாயக' not in desc and len(desc) > 100:
            flagged.append({
                'video_id': vid,
                'title': title,
                'type': 'DEITY_MISMATCH',
                'issue': "Vinayagar video has Murugan lyrics in description",
                'lyrics_sample': desc[:100].replace('\n', ' ')
            })
            
    if 'கிருஷ்ண' in title or 'krishna' in title.lower():
        if 'சிவ' in desc and 'கிருஷ்ண' not in desc and len(desc) > 100:
            flagged.append({
                'video_id': vid,
                'title': title,
                'type': 'DEITY_MISMATCH',
                'issue': "Krishna video has Shiva lyrics in description",
                'lyrics_sample': desc[:100].replace('\n', ' ')
            })

    # 4. Thirukkural Chapter mismatch check across all videos
    ch_m = re.search(r'அதிகாரம்\s*(\d+)', title)
    if ch_m:
        ch_num = int(ch_m.group(1))
        # Look for Chapter number in description
        desc_ch_m = re.findall(r'அதிகாரம்\s*(\d+)', desc)
        if desc_ch_m:
            for dch in desc_ch_m:
                if int(dch) != ch_num:
                    flagged.append({
                        'video_id': vid,
                        'title': title,
                        'type': 'THIRUKKURAL_CHAPTER_MISMATCH',
                        'issue': f"Video title is Chapter {ch_num}, but description mentions Chapter {dch}",
                        'lyrics_sample': desc[:120].replace('\n', ' ')
                    })
                    break

print(f"\n========================================================")
print(f"FLAGGED VIDEOS WITH WRONG OR MISMATCHED LYRICS: {len(flagged)}")
print(f"========================================================")

for idx, item in enumerate(flagged, 1):
    print(f"\n{idx}. [{item['video_id']}] {item['title']}")
    print(f"   Category: {item['type']}")
    print(f"   Problem : {item['issue']}")
    if item['lyrics_sample']:
        print(f"   Snippet : {item['lyrics_sample'][:90]}")

with open('production/wrong_lyrics_full_report.json', 'w', encoding='utf-8') as f:
    json.dump(flagged, f, indent=2, ensure_ascii=False)
