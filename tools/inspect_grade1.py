import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data/books/grade_1.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('Grade:', d.get('grade'), d.get('gradeTitle'))
for i, b in enumerate(d.get('books', [])):
    print(f"\n--- Book {i+1}: {b.get('id')} - {b.get('title')} ({b.get('titleEn')}) ---")
    print(f"Subtitle: {b.get('subtitle')}")
    chapters = b.get('chapters', [])
    print(f"Chapters count: {len(chapters)}")
    for j, ch in enumerate(chapters[:3]):
        if isinstance(ch, dict):
            print(f"   Ch {j+1}: {ch.get('title')} (ID: {ch.get('id')})")
            if 'content' in ch:
                print(f"      Content keys: {list(ch['content'].keys())}")
            if 'sections' in ch:
                print(f"      Sections count: {len(ch['sections'])}")
        else:
            print(f"   Ch {j+1}: {ch}")

