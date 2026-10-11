import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('production/master_133_athikarams.json', encoding='utf-8') as f:
    master = json.load(f)

with open('production/all_artist_releases.json', encoding='utf-8') as f:
    releases = json.load(f)

print(f"Total releases extracted: {len(releases)}")

# master is dict like {"1": {"number": 1, "name": "கடவுள் வாழ்த்து", ...}, ...}
name_to_num = {}
num_to_master = {}
for k, v in master.items():
    ch_num = int(k)
    ch_name = v.get('name', '').strip() if isinstance(v, dict) else str(v).strip()
    name_to_num[ch_name] = ch_num
    num_to_master[ch_num] = ch_name

print(f"Total canonical chapters in master: {len(name_to_num)}")

matched_releases = {}
unmatched_kural = []
other_releases = []

for r in releases:
    title = r['title'].strip()
    if 'திருக்குறள்' in title:
        first_line = title.split('\n')[0].strip()
        clean = first_line.replace('திருக்குறள்', '').replace('2026', '').replace('-', '').replace('|', '').strip()
        matched = False
        
        # Direct match or substring
        for ch_name, ch_num in name_to_num.items():
            if ch_name == clean or ch_name in clean or clean in ch_name:
                matched_releases[ch_num] = {
                    'chapter_num': ch_num,
                    'chapter_name': ch_name,
                    'release_title': first_line,
                    'href': r.get('href', ''),
                    'rowText': r.get('rowText', '')
                }
                matched = True
                break
        
        if not matched:
            unmatched_kural.append({
                'title': first_line,
                'clean': clean,
                'href': r.get('href', ''),
                'rowText': r.get('rowText', '')
            })
    else:
        other_releases.append(title.split('\n')[0].strip())

print(f"\n==========================================")
print(f"Thirukkural Releases Matched: {len(matched_releases)} / 133")
print(f"Unmatched Thirukkural Releases: {len(unmatched_kural)}")
print(f"Other Releases: {len(other_releases)}")
print(f"==========================================")

missing_chapters = []
for i in range(1, 134):
    if i not in matched_releases:
        missing_chapters.append((i, num_to_master.get(i, '')))

if missing_chapters:
    print(f"\nMissing Chapters ({len(missing_chapters)}):")
    for ch_num, ch_name in missing_chapters:
        print(f"  Chapter {ch_num:3d}: {ch_name}")
else:
    print("\nALL 133 CHAPTERS ARE PRESENT IN RELEASES!")

if unmatched_kural:
    print(f"\nUnmatched Thirukkural releases ({len(unmatched_kural)}):")
    for u in unmatched_kural:
        print(f"  Title: '{u['title']}' | Clean: '{u['clean']}'")

# Save detailed analysis
analysis = {
    'total_releases': len(releases),
    'matched_count': len(matched_releases),
    'missing_count': len(missing_chapters),
    'missing_chapters': missing_chapters,
    'matched_releases': matched_releases,
    'unmatched_kural': unmatched_kural,
    'other_releases': other_releases
}
with open('production/releases_chapter_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(analysis, f, indent=2, ensure_ascii=False)
