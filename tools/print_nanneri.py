import json
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/books/grade_1.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for ch in d['books']['nanneri']['chapters']:
    print(f"\n--- Chapter {ch['chapterNumber']}: {ch['title']} ---")
    print("Verse:", ch.get('verse'))
    print("Story:", ch.get('story'))
