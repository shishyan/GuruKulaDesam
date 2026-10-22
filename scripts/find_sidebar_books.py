import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('books.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'<aside[^>]*>.*?</aside>', text, re.DOTALL):
    print("Found <aside>:", m.group(0)[:300], "\n---\n")

# Check for .course-sidebar or .sidebar
for m in re.finditer(r'class="[^"]*sidebar[^"]*"', text):
    print("Sidebar class in books.html:", m.group(0))
