import sys
import re
import json
import pathlib

sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent
plan = json.load(open(ROOT / 'production' / 'thirukkural_sort_plan.json', encoding='utf-8'))
athikarams = json.load(open(ROOT / 'production' / 'master_133_athikarams.json', encoding='utf-8'))

# Clean styling tags
STYLES = ['(Original)', '(Remix)', '(Symphony)', '(Rock)', '(Female)', '(Pop)', '(Sad)', '[Film]', '[Audio]', '[Full Song Film]', '[Full Song]', '(பகுதி 1)', '(பகுதி 2)', '(Part 1)', '(Part 2)']

results = []

# Group items by chapter to handle multi-video chapters
chap_groups = {}
for item in plan:
    chap_groups.setdefault(item['chapter'], []).append(item)

for chap_num, items in sorted(chap_groups.items()):
    ath_info = athikarams.get(str(chap_num), {})
    chap_name = ath_info.get('name', '')
    prefix = f"திருக்குறள்: அதிகாரம் {chap_num} - {chap_name}"
    
    for idx, item in enumerate(items):
        orig_title = item['title'].strip()
        vid = item['videoId']
        item_id = item['itemId']
        
        # Detect style / variant
        found_style = None
        for s in STYLES:
            if s.lower() in orig_title.lower():
                found_style = s
                break
                
        # Detect part
        part_tag = None
        if 'பகுதி 1' in orig_title or 'part 1' in orig_title.lower():
            part_tag = "(பகுதி 1)"
        elif 'பகுதி 2' in orig_title or 'part 2' in orig_title.lower():
            part_tag = "(பகுதி 2)"
            
        # Detect English or subtitle
        eng_part = ""
        if "|" in orig_title:
            parts = orig_title.split("|")
            cand = parts[-1].strip()
            # Clean redundant words
            cand = re.sub(r'^(Thirukkural:\s*|Thirukkural\s*|Cinematic\s*Thirukkural\s*Film|Thirukkural\s*Film)', '', cand, flags=re.I).strip()
            if re.search(r'[a-zA-Z]', cand):
                eng_part = cand
        elif re.search(r'^[A-Za-z]', orig_title):
            cand = re.sub(r'^Thirukkural\s*', '', orig_title, flags=re.I).strip()
            cand = re.sub(r'\(.*?\)', '', cand).strip()
            if cand:
                eng_part = cand
                
        # Clean eng_part
        for s in STYLES:
            eng_part = eng_part.replace(s, '').strip()
        eng_part = re.sub(r'\[Film\]|\[Audio\]|Cinematic\s*Thirukkural\s*Film|Cinematic\s*Film|Full\s*Song\s*Film', '', eng_part, flags=re.I).strip()
        eng_part = re.sub(r'\s+', ' ', eng_part).strip(' -|:')
        
        # Build clean suffix
        components = []
        if eng_part:
            components.append(eng_part)
        if part_tag:
            components.append(part_tag)
        if found_style and found_style not in [part_tag]:
            components.append(found_style)
            
        suffix = " ".join(components).strip()
        
        # Handle case where multiple videos exist in same chapter but no suffix detected
        if not suffix and len(items) > 1:
            if idx == 0:
                suffix = "(Version 1)"
            else:
                suffix = f"(Version {idx+1})"
                
        if suffix:
            new_title = f"{prefix} | {suffix}"
        else:
            new_title = prefix
            
        new_title = re.sub(r'\s+', ' ', new_title).strip()
        if len(new_title) > 100:
            new_title = new_title[:97] + "..."
            
        results.append({
            'position': item['target_position'],
            'chapter': chap_num,
            'videoId': vid,
            'itemId': item_id,
            'old_title': orig_title,
            'new_title': new_title
        })

with open(ROOT / 'production' / 'thirukkural_standardized_titles.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Generated {len(results)} standardized titles cleanly!")
print("\nSample Preview (First 20 items):")
print("-" * 85)
for r in results[:20]:
    print(f"Chap {r['chapter']:03d} | {r['new_title']}")
print("...")
print("Sample Preview (Last 10 items):")
for r in results[-10:]:
    print(f"Chap {r['chapter']:03d} | {r['new_title']}")
