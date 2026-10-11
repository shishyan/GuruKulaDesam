import sys
import json

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/youtube_backup/videos.json', encoding='utf-8') as f:
    videos = json.load(f)

with open('production/youtube_lyrics_overrides.json', encoding='utf-8') as f:
    overrides = json.load(f)

works = overrides.get('_works', {})

# Mapping keywords in title to works key
KEYWORD_TO_WORK = [
    (['கருமாரி', 'karumari'], 'karumari'),
    (['அவிநாசி', 'avinasi'], 'avinasi'),
    (['சமயபுரம்', 'samayapura', 'சமயபுரத்தாயே'], 'mariamman'),
    (['ரேணுகாம்பாள்', 'renukambal'], 'renukambal'),
    (['வேதஸார', 'வேதசார்', 'vedasar'], 'vedasara'),
    (['திருவையாறு', 'thiruvaiyaru'], 'thiruvaiyaru'),
    (['திருப்புலம்பல்', 'thirupulambal'], 'thirupulambal'),
    (['தென்னாடுடைய', 'thennadudaiya'], 'thennadudaiya'),
    (['ரகுபதி', 'raghupati'], 'raghupati'),
    (['சுப்ரமணியர்', 'sivasubramaniyar'], 'sivasubramaniyar'),
    (['கோளறு', 'kolaru'], 'kolaru'),
    (['கணேச பஞ்சரத்னம்', 'pancharatnam'], 'pancharatnam'),
    (['திகட சக்கர', 'thigada'], 'thigada')
]

matched = []
unmatched = []

for v in videos:
    vid = v['id']
    title = v['snippet']['title']
    desc = v['snippet']['description']
    
    if "provided to youtube by distrokid" in desc.lower():
        continue
        
    has_full_lyrics = "பாடல் வரிகள்" in desc and len(desc) > 500
    
    # Check if matched to a known work
    target_work = None
    for kw_list, w_key in KEYWORD_TO_WORK:
        if any(kw in title.lower() for kw in kw_list):
            target_work = w_key
            break
            
    if target_work:
        # Check if already has proper lyrics or needs update
        work_data = works.get(target_work, {})
        first_line = work_data.get('lyrics', '').split('\n')[0][:20]
        
        needs_update = False
        reason = ""
        if len(desc) < 300:
            needs_update = True
            reason = f"Description too short ({len(desc)} chars)"
        elif first_line and first_line not in desc:
            needs_update = True
            reason = f"Missing canonical verse '{first_line}'"
        elif target_work == 'pancharatnam' and 'நதேதராதி' not in desc:
            needs_update = True
            reason = "Pancharatnam missing verses 2-5"
            
        if needs_update:
            matched.append({
                'id': vid,
                'title': title,
                'work': target_work,
                'reason': reason,
                'canonical_lyrics': work_data.get('lyrics', ''),
                'canonical_meaning': work_data.get('meaning', '')
            })
    else:
        if len(desc) < 200:
            unmatched.append({
                'id': vid,
                'title': title,
                'desc_len': len(desc)
            })

print(f"=== MATCHED VIDEOS NEEDING CANONICAL LYRICS FIXES: {len(matched)} ===")
for m in matched:
    print(f"\n[{m['id']}] {m['title']}")
    print(f"  Work: {m['work']} | Reason: {m['reason']}")

print(f"\n=== UNMATCHED SHORT VIDEOS: {len(unmatched)} ===")
for u in unmatched:
    print(f"[{u['id']}] {u['title']} ({u['desc_len']} chars)")

with open('production/verified_videos_needing_lyrics.json', 'w', encoding='utf-8') as f:
    json.dump({'matched': matched, 'unmatched': unmatched}, f, indent=2, ensure_ascii=False)
