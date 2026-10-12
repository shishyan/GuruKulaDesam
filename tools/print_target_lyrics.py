import sys
import json

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/youtube_lyrics_overrides.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

works = d.get('_works', {})
for k in ['thigada', 'pancharatnam', 'thirupulambal', 'vedasara', 'thiruvaiyaru']:
    w = works.get(k)
    print(f"\n=================== {k.upper()} ===================")
    if w:
        print("Source:", w.get('source'))
        print("Lyrics:\n", w.get('lyrics'))
        print("Meaning:\n", w.get('meaning'))
    else:
        print("NOT FOUND IN _works!")
