import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/youtube_backup/videos.json', encoding='utf-8') as f:
    videos = json.load(f)

print(f"Total videos in backup: {len(videos)}")

# Key devotional works signatures:
WORKS = {
    'thirukkural': {
        'keywords': ['திருக்குறள்', 'thirukkural', 'அதிகாரம்', 'குறள்'],
        'expected_lyrics_terms': ['அகர', 'துப்பார்க்கு', 'இல்வாழ்க்கை', 'குறள்', 'அதிகாரம்']
    },
    'thiruppugazh_muthai': {
        'keywords': ['முத்தைத் தரு', 'muthai tharu', 'muthai'],
        'expected_lyrics_terms': ['முத்தைத் தரு', 'அத்திக்கு']
    },
    'anubhuti': {
        'keywords': ['கந்தர் அநுபூதி', 'கந்தர் அனுபூதி', 'kandhar anuboot', 'உருவாய் அருவாய்'],
        'expected_lyrics_terms': ['உருவாய் அருவாய்', 'மருவாய் മലராய்']
    },
    'skanda_gayatri': {
        'keywords': ['ஸ்கந்த', 'skanda', 'காயத்ரி', 'சரவணபவ'],
        'expected_lyrics_terms': ['சரவணபவ', 'தத்புருஷாய', 'ஷண்முக']
    },
    'pancharatnam': {
        'keywords': ['பஞ்சரத்னம்', 'pancharatnam', 'கணேச'],
        'expected_lyrics_terms': ['முதாகராத்த', 'மோதகம்']
    },
    'thigada': {
        'keywords': ['திகட சக்கர', 'thigada'],
        'expected_lyrics_terms': ['திகட சக்கர', 'செம்முக']
    },
    'thevaram_maasil': {
        'keywords': ['மாசில் வீணை', 'maasil veenai', 'மாசில்'],
        'expected_lyrics_terms': ['மாசில் வீணை', 'மாலை மதியமும்']
    },
    'thiruvasagam_sivapuranam': {
        'keywords': ['சிவபுராணம்', 'sivapuranam'],
        'expected_lyrics_terms': ['நமச்சிவாய வாழ்க', 'நாதன் தாள் வாழ்க']
    },
    'thirupallaandu': {
        'keywords': ['திருப்பல்லாண்டு', 'thiru pallaandu', 'பல்லாண்டு'],
        'expected_lyrics_terms': ['மன்னுக தில்லை', 'பல்லாண்டு']
    },
    'vel_virutham': {
        'keywords': ['வேல் விருத்தம்', 'vel virutham', 'மகரம் அளறிடை'],
        'expected_lyrics_terms': ['மகரம் அளறிடை', 'அறுமுகனாய்']
    },
    'abirami_anthadhi': {
        'keywords': ['அபிராமி அந்தாதி', 'abirami anthadhi', 'தனந்தரும் கல்விதரும்'],
        'expected_lyrics_terms': ['தனம் தரும்', 'கல்வி தரும்', 'உதிக்கின்ற செங்கதிர்']
    },
    'kolaru': {
        'keywords': ['கோளறு', 'kolaru'],
        'expected_lyrics_terms': ['வேயுறு தோளி', 'நல்லநல்ல அவைநல்ல நல்ல']
    },
    'kandhasashti': {
        'keywords': ['சஷ்டி கவசம்', 'sashti kavasam'],
        'expected_lyrics_terms': ['துதிப்போர்க்கு வல்வினைபோம்', 'சஷ்டியை நோக்க']
    }
}

flagged = []

for v in videos:
    vid = v['id']
    snip = v.get('snippet', {})
    title = snip.get('title', '')
    desc = snip.get('description', '')
    
    issues = []
    
    # 1. Prompt leakage in title / description
    if any(p in title.lower() for p in ['create album', 'generate', 'prompt:', 'album cover for']):
        issues.append(f"Prompt leakage in title: '{title}'")
    if 'create album cover' in desc.lower():
        issues.append("Prompt leakage in description")
        
    # 2. Check for Kandhar Anubhuti title but Skanda Mantram lyrics
    title_lower = title.lower()
    if ('அநுபூதி' in title or 'anuboothi' in title_lower or 'anubhuti' in title_lower) and ('உருவாய் அருவாய்' in title):
        if 'சரவணபவ' in desc and 'உருவாய் அருவாய்' not in desc:
            issues.append("Title says Kandhar Anubhuti (உருவாய் அருவாய்) but lyrics are Skanda Mantram (சரவணபவ)")
            
    # 3. Check for Thigada Sakkara title but Gana Natha Om lyrics
    if 'திகட சக்கர' in title or 'thigada' in title_lower:
        if 'கண நாதா ஓம்' in desc and 'திகட சக்கர' not in desc:
            issues.append("Title says Thigada Sakkara but lyrics are generic Gana Natha Om")
            
    # 4. Check for Pancharatnam truncated
    if 'பஞ்சரத்னம்' in title or 'pancharatnam' in title_lower:
        if 'முதாகராத்த' in desc and 'நதேதராதி' not in desc:
            issues.append("Ganesha Pancharatnam description has only Verse 1 (missing Verses 2-5)")

    # 5. Check if title indicates one work but description has another
    if ('சிவபுராணம்' in title or 'sivapuranam' in title_lower) and ('நமச்சிவாய வாழ்க' not in desc and 'சிவபுராணம்' not in desc and len(desc) > 300):
        issues.append("Title mentions Sivapuranam but lyrics missing Sivapuranam opening")

    if ('கோளறு' in title or 'kolaru' in title_lower) and ('வேயுறு தோளி' not in desc and len(desc) > 300):
        issues.append("Title mentions Kolaru Pathigam but lyrics missing 'வேயுறு தோளி'")

    if ('மாசில் வீணை' in title or 'maasil' in title_lower) and ('மாசில் வீணை' not in desc and len(desc) > 300):
        issues.append("Title mentions Maasil Veenai but lyrics missing 'மாசில் வீணை'")
        
    if issues:
        flagged.append({
            'videoId': vid,
            'title': title,
            'issues': issues,
            'desc_snippet': desc[:120].replace('\n', ' ')
        })

print(f"\nAudit Complete. Total Flagged Videos: {len(flagged)}")
for f_item in flagged:
    print(f"\n[{f_item['videoId']}] {f_item['title']}")
    for iss in f_item['issues']:
        print(f"   * {iss}")

with open('production/comprehensive_wrong_lyrics_audit.json', 'w', encoding='utf-8') as f:
    json.dump(flagged, f, indent=2, ensure_ascii=False)
