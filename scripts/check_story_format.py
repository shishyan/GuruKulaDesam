import glob
import json

pattern = 'data/puranas/*.json'
for f in sorted(glob.glob(pattern)):
    with open(f, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    total_ch = len(data.get('chapters', []))
    first_expo = data['chapters'][0].get('exposition', '') if total_ch > 0 else ''
    is_verse = 'child-story-body' not in first_expo
    status = 'HAS VERSES / RAW POETRY' if is_verse else 'PURE STORY'
    print(f"{f} ({total_ch} ch) -> {status}")
