import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('moola-nool.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'<aside class="left-strip-bar".*?</aside>', text, re.DOTALL)
if m:
    print("Found left-strip-bar in moola-nool.html, size:", len(m.group(0)))
else:
    print("Not found")
