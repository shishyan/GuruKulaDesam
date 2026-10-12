import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

for g in range(1, 13):
    path = f"data/books/grade_{g}.json"
    if not os.path.exists(path):
        print(f"Grade {g}: MISSING!")
        continue
    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        books = d.get('books', {})
        ch_count = sum(len(b.get('chapters', [])) for b in books.values()) if isinstance(books, dict) else 0
        print(f"Grade {g:<2}: {d.get('gradeTitle', 'No Title'):<40} Books: {len(books)} Total Chapters: {ch_count}")
    except Exception as e:
        print(f"Grade {g}: Error loading: {e}")

