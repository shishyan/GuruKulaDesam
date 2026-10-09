import glob
import json

for f in sorted(glob.glob('data/books/grade_*.json')):
    with open(f, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    if 'nalvazhi' in data.get('books', {}):
        data['books']['nalvazhi']['title'] = 'நற்பண்பு'
        data['books']['nalvazhi']['englishTitle'] = 'Narpanbu - The Noble Virtues of Wisdom, Truth & Character'
        with open(f, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

print("Updated nalvazhi -> Narpanbu in all grade JSONs successfully.")
