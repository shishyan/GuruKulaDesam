with open('assets/js/moola-nool-data.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'"([a-z0-9\-]+)":\s*\{\s*"id":', text)
print(f"Total scriptures in moola-nool-data.js: {len(matches)}")
for m in matches:
    print("  *", m)
