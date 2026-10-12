import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data/books/grade_1.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

ch = d['books']['nanneri']['chapters'][0]
for k, v in ch.items():
    print(f"\n=== {k} ===")
    print(v)

