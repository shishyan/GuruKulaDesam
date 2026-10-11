import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/youtube_backup/videos.json', encoding='utf-8') as f:
    videos = json.load(f)

deity_keywords = {
    'krishna_rama': ['கிருஷ்ண', 'ராமா', 'ராமர்', 'hare rama', 'hare krishna', 'raghupati', 'ரகுபதி'],
    'murugan': ['முருக', 'சுப்ரமணிய', 'கந்த', 'சண்முக', 'சரவணபவ', 'வேல்', 'muruga', 'karthikeya'],
    'vinayagar': ['விநாயக', 'கணேச', 'கணபதி', 'பிள்ளையார்', 'மோதகம்', 'ganesha', 'vinayaga'],
    'shiva': ['சிவன்', 'சிவபெருமான்', 'நமச்சிவாய', 'ஈஸ்வர', 'shiva', 'நடராஜர்', 'தில்லை', 'அம்பல'],
    'amman': ['மாரியம்மன்', 'அபிராமி', 'கருமாரி', 'ரேணுகாம்பாள்', 'பராசக்தி', 'துர்க்கை', 'amman']
}

mismatches = []

for v in videos:
    vid = v['id']
    title = v['snippet']['title'].lower()
    desc = v['snippet']['description']
    
    if "provided to youtube by distrokid" in desc.lower():
        continue
        
    # Detect deity of title
    title_deity = None
    if any(k in title for k in ['சுப்ரமணியர்', 'முருகர்', 'கந்தர்', 'திருப்புகழ்', 'வேல் விருத்தம்']):
        title_deity = 'murugan'
    elif any(k in title for k in ['விநாயகர்', 'கணேச', 'கணபதி', 'திகட சக்கர']):
        title_deity = 'vinayagar'
    elif any(k in title for k in ['சிவன்', 'சிவபெருமான்', 'நடராஜர்', 'தேவாரம்', 'திருவாசகம்', 'திருமந்திரம்']):
        title_deity = 'shiva'
    elif any(k in title for k in ['கருமாரி', 'சமயபுரம்', 'ரேணுகாம்பாள்', 'அபிராமி']):
        title_deity = 'amman'
    elif any(k in title for k in ['ராம', 'கிருஷ்ண', 'நாராயண', 'விஷ்ணு']):
        title_deity = 'krishna_rama'

    if not title_deity:
        continue
        
    # Check lyrics text inside description
    lyrics_part = ""
    if "பாடல் வரிகள்" in desc:
        lyrics_part = desc.split("பாடல் வரிகள்")[1]
    elif "lyrics" in desc.lower():
        lyrics_part = desc.split("yrics")[1]
        
    if lyrics_part:
        lyrics_lower = lyrics_part.lower()
        
        # Check if Murugan video has Krishna/Rama lyrics
        if title_deity == 'murugan' and any(k in lyrics_lower for k in ['கிருஷ்ண', 'ஹரே ராம', 'கஸ்தூரீ']):
            mismatches.append({
                'id': vid,
                'title': v['snippet']['title'],
                'title_deity': 'Murugan',
                'lyrics_deity': 'Krishna/Rama',
                'sample': lyrics_part[:150].replace('\n', ' ')
            })
            
        # Check if Vinayagar video has Gana Natha when title is Thigada
        if 'திகட சக்கர' in title and 'கண நாதா ஓம்' in lyrics_lower and 'திகட சக்கர' not in lyrics_lower:
            mismatches.append({
                'id': vid,
                'title': v['snippet']['title'],
                'title_deity': 'Vinayagar (Thigada Sakkara)',
                'lyrics_deity': 'Generic Gana Natha chant',
                'sample': lyrics_part[:150].replace('\n', ' ')
            })
            
        # Check if Shiva video has Krishna/Rama lyrics
        if title_deity == 'shiva' and any(k in lyrics_lower for k in ['கிருஷ்ண', 'ஹரே ராம', 'ரகுபதி']):
            mismatches.append({
                'id': vid,
                'title': v['snippet']['title'],
                'title_deity': 'Shiva',
                'lyrics_deity': 'Krishna/Rama',
                'sample': lyrics_part[:150].replace('\n', ' ')
            })

print(f"Total Cross-Deity / Content Mismatches found: {len(mismatches)}")
for m in mismatches:
    print(f"\n[{m['id']}] {m['title']}")
    print(f"   Expected Deity: {m['title_deity']} | Found Lyrics Deity: {m['lyrics_deity']}")
    print(f"   Sample: {m['sample']}")
