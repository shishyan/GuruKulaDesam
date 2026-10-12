import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data/books/grade_1.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

book = d['books']['nanneri']
print(f"Book: {book['title']} ({book['englishTitle']})")
print(f"Chapters count: {len(book['chapters'])}")
for ch in book['chapters']:
    print(f"\n--- Chapter {ch.get('chapterNumber')}: {ch.get('title')} ---")
    print(f"Verse/Moolam: {ch.get('verse')}")
    print(f"Meaning: {ch.get('meaning')}")
    print(f"Story Title: {ch.get('storyTitle')}")
    print(f"Keys: {list(ch.keys())}")

