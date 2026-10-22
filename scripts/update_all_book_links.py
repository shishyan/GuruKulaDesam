import os
import re

ROOT = r"C:\GitHub\Gurukuladesam"

# We want to replace books.html?book=... and books.html references outside the sidebar with puranas.html?id=...
mapping = {
    'books.html?book=nanneri': 'puranas.html?id=children-purana-stories',
    'books.html?book=nallaram': 'puranas.html?id=mahabharatam',
    'books.html?book=nalvazhi': 'puranas.html?id=ramayanam',
    'books.html?book=narthunai': 'puranas.html?id=kandha-puranam',
    'books.html?book=narchinthanai': 'puranas.html?id=bhagavata-puranam',
    'books.html?book=narchol': 'puranas.html?id=thiruvilaiyadal',
    'books.html?book=narcheyal': 'puranas.html?id=periyapuranam',
}

files_to_update = []
for fname in os.listdir(ROOT):
    if fname.endswith('.html'):
        files_to_update.append(os.path.join(ROOT, fname))

print(f"Total HTML files to scan in root: {len(files_to_update)}")

total_replaced = 0
for fp in files_to_update:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_content = content
    for old_link, new_link in mapping.items():
        if old_link in content:
            content = content.replace(old_link, new_link)

    if content != orig_content:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        total_replaced += 1
        print(f"Updated book links in {os.path.basename(fp)}")

print(f"Done! Updated {total_replaced} files in root.")
