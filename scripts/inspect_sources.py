import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('higher-studies.html', 'r', encoding='utf-8') as f:
    c = f.read()

sources = re.findall(r'<div class="module-sources">(.*?)</div>', c, re.DOTALL)
unique_sources = sorted(list(set([re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s)).strip() for s in sources])))

print(f"Total module-sources found: {len(sources)}")
print(f"Unique sources: {len(unique_sources)}")
for i, s in enumerate(unique_sources, 1):
    print(f"{i}. {s}")

