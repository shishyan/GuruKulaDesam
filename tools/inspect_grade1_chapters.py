import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('data/books/grade_1.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for b_id, b in d['books'].items():
    print(f"\n==========================================")
    print(f"BOOK: {b['title']} ({b_id})")
    print(f"==========================================")
    for ch in b['chapters']:
        num = ch['chapterNumber']
        title = ch['title']
        v_len = len(ch.get('verse', ''))
        e_len = len(ch.get('exposition', ''))
        s_len = len(ch.get('story', ''))
        first_sentence = ch.get('story', '').split('.')[0] if ch.get('story') else ''
        print(f"  Ch {num}: {title} | Verse: {v_len}c | Expo: {e_len}c | Story: {s_len}c")
        print(f"       Story snippet: {first_sentence[:80]}...")
