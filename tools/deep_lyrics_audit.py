import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# Load master catalog
with open('master_all_598_songs_catalog.json', encoding='utf-8') as f:
    catalog = json.load(f)

# Load overrides
with open('production/youtube_lyrics_overrides.json', encoding='utf-8') as f:
    overrides = json.load(f)

works = overrides.get('_works', {})

# Load live YouTube descriptions backup
try:
    with open('production/youtube_backup/videos.json', encoding='utf-8') as f:
        yt_videos = {v['id']: v for v in json.load(f)}
except Exception:
    yt_videos = {}

print(f"Total songs in catalog: {len(catalog)}")
print(f"Total videos in YouTube backup: {len(yt_videos)}")

# Define keywords to detect mismatches
mismatches = []

for s in catalog:
    vid = s['video_id']
    title = s.get('canonical_title', '')
    desc = yt_videos.get(vid, {}).get('snippet', {}).get('description', '')
    
    # Check override if any
    ov_ref = overrides.get(vid, {}).get('ref')
    ov_work = works.get(ov_ref, {}) if ov_ref else None
    
    # Text to check
    lyric_source = ov_work.get('source', '') if ov_work else ''
    lyric_text = ov_work.get('lyrics', '') if ov_work else ''
    if not lyric_text:
        lyric_text = desc
        
    t_lower = title.lower()
    l_lower = (lyric_text + " " + desc).lower()
    
    reasons = []
    
    # 1. Kandar Anubhuti vs Skanda Mantram
    if 'அநுபூதி' in title or 'anuboothi' in t_lower or 'anubhuti' in t_lower:
        if ov_ref == 'skandamantram' or ('காயத்ரி' in lyric_text and 'உருவாய்' not in lyric_text):
            reasons.append(f"Title is Kandar Anubhuti, but lyrics/override is Skanda Mantram ({ov_ref})")
            
    # 2. Thigada Chakkaram vs Gananatha Om
    if 'திகட' in title or 'thigada' in t_lower:
        if 'கணநாதா' in lyric_text or 'gana natha' in l_lower:
            reasons.append("Title is Thigada Chakkara Vinayagar, but lyrics contain 'Gana Natha Om'")
            
    # 3. Thirukkural Chapter mismatch (Title Chapter X vs Lyrics Chapter Y)
    ch_match = re.search(r'அதிகாரம்\s*(\d+)', title)
    if ch_match:
        ch_num = int(ch_match.group(1))
        # Look for couplet numbers or chapter mention in description
        kural_mentions = re.findall(r'குறள்\s*(\d+)', desc)
        if kural_mentions:
            first_kural = int(kural_mentions[0])
            expected_start = (ch_num - 1) * 10 + 1
            expected_end = ch_num * 10
            if not (expected_start <= first_kural <= expected_end):
                reasons.append(f"Thirukkural Chapter {ch_num} (Kurals {expected_start}-{expected_end}) has description mentioning Kural {first_kural}")
                
    # 4. Ganesha Pancharatnam vs other Vinayagar
    if 'பஞ்சரத்னம்' in title or 'pancharatnam' in t_lower:
        if 'முதாகராத்த' not in lyric_text and 'mudakaratha' not in l_lower and len(lyric_text) > 50:
            reasons.append("Title is Pancharatnam but lyrics don't contain Mudaakaraatha")
            
    # 5. Muthaitharu vs Kaithala / other Thiruppugazh
    if 'முத்தைத் தரு' in title or 'muthaitharu' in t_lower or 'muthaith tharu' in t_lower:
        if 'முத்தைத்' not in lyric_text and 'கைத்தல' in lyric_text:
            reasons.append("Title is Muthaitharu, but lyrics contain Kaithala Nirai Kani")
            
    # 6. Kaithala vs Muthaitharu
    if 'கைத்தல' in title or 'kaithala' in t_lower:
        if 'கைத்தல' not in lyric_text and 'முத்தைத்' in lyric_text:
            reasons.append("Title is Kaithala, but lyrics contain Muthaitharu")
            
    # 7. Maasil Veenaiyum vs other Thevaram
    if 'மாசில் வீணையும்' in title or 'maasil veenai' in t_lower:
        if 'மாசில்' not in lyric_text and len(lyric_text) > 50:
            reasons.append("Title is Maasil Veenaiyum, but lyrics do not contain Maasil Veenaiyum")

    # 8. Kolaru Pathigam vs other
    if 'கோளறு' in title or 'kolaru' in t_lower:
        if 'வேயுறு' not in lyric_text and len(lyric_text) > 50:
            reasons.append("Title is Kolaru Pathigam, but lyrics do not contain 'வேயுறு தோளிபங்கன்'")
            
    # 9. Sivapuranam vs other
    if 'சிவபுராணம்' in title or 'sivapuranam' in t_lower:
        if 'நமச்சிவாய வாழ்க' not in lyric_text and len(lyric_text) > 50:
            reasons.append("Title is Sivapuranam, but lyrics do not contain 'நமச்சிவாய வாழ்க'")
            
    # 10. Check if description has placeholder text
    if 'lorem ipsum' in desc.lower() or 'placeholder' in desc.lower() or 'todo' in desc.lower():
        reasons.append("Description contains placeholder / TODO text")

    if reasons:
        mismatches.append({
            'video_id': vid,
            'title': title,
            'reasons': reasons,
            'override_ref': ov_ref,
            'desc_snippet': desc[:150].replace('\n', ' ')
        })

print(f"\n========================================================")
print(f"TOTAL VIDEOS WITH DETECTED LYRICS MISMATCHES: {len(mismatches)}")
print(f"========================================================")

for idx, m in enumerate(mismatches, 1):
    print(f"\n{idx}. [{m['video_id']}] {m['title']}")
    for r in m['reasons']:
        print(f"   ⚠️  MISMATCH: {r}")
    if m['desc_snippet']:
        print(f"   📄 Desc Preview: {m['desc_snippet']}")

# Save report
with open('production/flagged_wrong_lyrics_audit.json', 'w', encoding='utf-8') as f:
    json.dump(mismatches, f, indent=2, ensure_ascii=False)

print("\nSaved detailed report to production/flagged_wrong_lyrics_audit.json")
