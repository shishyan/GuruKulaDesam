import json, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('data/books/grade_1.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("Grade:", d.get('grade'), d.get('gradeTitle'))
print("Phase:", d.get('phase'))
print("Literature Base:", d.get('literatureBase'))
print("Psychological Goal:", d.get('psychologicalGoal'))

books = d.get('books', {})
print(f"Total Books: {len(books)}")

total_chaps = 0
story_count = 0
empty_stories = []

for b_id, b in books.items():
    chaps = b.get('chapters', [])
    total_chaps += len(chaps)
    print(f"\n--- Book: {b.get('title')} ({b_id}) | Chapters: {len(chaps)} ---")
    for c in chaps:
        num = c.get('chapterNumber')
        title = c.get('title')
        story = c.get('story', '').strip()
        expo = c.get('exposition', '').strip()
        verse = c.get('verse', '').strip()
        app = c.get('lifeApplication', '').strip()
        ex = c.get('exercise', '').strip()
        imgs = len(c.get('images', []))
        
        has_story = len(story) > 100
        if has_story:
            story_count += 1
        else:
            empty_stories.append(f"{b_id} Chap {num}: {title}")
            
        print(f"  Chap {num}: {title} | Verse: {bool(verse)} | Story len: {len(story)} | Expo len: {len(expo)} | App: {bool(app)} | Exercise: {bool(ex)} | Imgs: {imgs}")

print("\n================ AUDIT SUMMARY ================")
print(f"Total Books: {len(books)} / 7")
print(f"Total Chapters: {total_chaps} / 49")
print(f"Chapters with Full Real Stories (>100 chars): {story_count} / {total_chaps}")
if empty_stories:
    print(f"Chapters MISSING full stories: {len(empty_stories)}")
    for es in empty_stories:
        print("  - ", es)
else:
    print("ALL 49 CHAPTERS HAVE DETAILED WRITTEN STORIES!")
