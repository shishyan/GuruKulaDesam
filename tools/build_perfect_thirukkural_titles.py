import sys
import re
import json
import pathlib

sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent
plan = json.load(open(ROOT / 'production' / 'thirukkural_sort_plan.json', encoding='utf-8'))
athikarams = json.load(open(ROOT / 'production' / 'master_133_athikarams.json', encoding='utf-8'))
updates_old = json.load(open(ROOT / 'thirukkural_title_updates.json', encoding='utf-8'))
old_updates_by_id = {item['id']: item for item in updates_old}

STYLES = ['(Original)', '(Remix)', '(Symphony)', '(Rock)', '(Female)', '(Pop)', '(Sad)', '[Film]', '[Audio]', '[Full Song Film]', '[Full Song]', '(பகுதி 1)', '(பகுதி 2)', '(Part 1)', '(Part 2)']

output = []

for item in plan:
    chap_num = item['chapter']
    orig_title = item['title'].strip()
    vid = item['videoId']
    item_id = item['itemId']
    
    ath_info = athikarams.get(str(chap_num), {})
    chap_name = ath_info.get('name', '')
    
    prefix = f"திருக்குறள்: அதிகாரம் {chap_num} - {chap_name}"
    
    # Check if old updates had a clean title we can adapt
    old_up = old_updates_by_id.get(vid)
    if old_up and old_up.get('new_title'):
        raw = old_up['new_title']
        # e.g. "அதிகாரம் 1 - கடவுள் வாழ்த்து (அகர முதல) | Agara Muthala | Full Song Film"
        # strip "அதிகாரம் X - [^|]+" from beginning
        after_chap = re.sub(r'^அதிகாரம்\s*\d+\s*-\s*[^|]+', '', raw).strip(' -|')
        if after_chap:
            new_title = f"{prefix} | {after_chap}"
        else:
            new_title = prefix
    else:
        # Build from orig_title
        found_styles = [s for s in STYLES if s.lower() in orig_title.lower()]
        
        # Check parts
        part_tag = None
        if 'பகுதி 1' in orig_title or 'part 1' in orig_title.lower():
            part_tag = "(பகுதி 1)"
        elif 'பகுதி 2' in orig_title or 'part 2' in orig_title.lower():
            part_tag = "(பகுதி 2)"
            
        eng_part = ""
        if "|" in orig_title:
            cand = orig_title.split("|")[-1].strip()
            cand = re.sub(r'^(Thirukkural:\s*|Thirukkural\s*|Cinematic\s*Thirukkural\s*Film|Thirukkural\s*Film)', '', cand, flags=re.I).strip()
            if re.search(r'[a-zA-Z]', cand):
                eng_part = cand
        elif re.search(r'^[A-Za-z]', orig_title):
            cand = re.sub(r'^Thirukkural\s*', '', orig_title, flags=re.I).strip()
            cand = re.sub(r'\(.*?\)', '', cand).strip()
            if cand:
                eng_part = cand
                
        # Clean redundant words from eng_part
        for s in STYLES:
            eng_part = eng_part.replace(s, '').strip()
        eng_part = re.sub(r'\[Film\]|\[Audio\]|Cinematic\s*Thirukkural\s*Film|Cinematic\s*Film|Full\s*Song\s*Film', '', eng_part, flags=re.I).strip()
        eng_part = re.sub(r'\s+', ' ', eng_part).strip(' -|:')
        
        # Style tag
        style_str = " ".join(dict.fromkeys(found_styles))
        
        suffix_parts = []
        if eng_part:
            suffix_parts.append(eng_part)
        if part_tag:
            suffix_parts.append(part_tag)
        if style_str:
            # avoid duplicating words already in eng_part
            clean_style = []
            for word in style_str.split():
                if word.strip('()[]').lower() not in eng_part.lower():
                    clean_style.append(word)
            if clean_style:
                suffix_parts.append(" ".join(clean_style))
                
        suffix = " ".join(suffix_parts).strip()
        if suffix:
            new_title = f"{prefix} | {suffix}"
        else:
            new_title = prefix
            
    # Normalize spaces and check length
    new_title = re.sub(r'\s+', ' ', new_title).strip()
    if len(new_title) > 100:
        new_title = new_title[:97] + "..."
        
    output.append({
        'position': item['target_position'],
        'chapter': chap_num,
        'videoId': vid,
        'itemId': item_id,
        'current_title': orig_title,
        'standardized_title': new_title,
        'length': len(new_title)
    })

with open(ROOT / 'production' / 'thirukkural_standardized_titles_ready.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Generated {len(output)} standardized titles!")
print("\nPreview of First 20 Standardized Titles:")
print("=" * 80)
for r in output[:20]:
    print(f"Chap {r['chapter']:03d} (len {r['length']:02d}) : {r['standardized_title']}")
