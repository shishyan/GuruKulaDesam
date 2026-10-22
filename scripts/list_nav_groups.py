import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('moola-nool.html', 'r', encoding='utf-8') as f:
    text = f.read()

aside = re.search(r'<aside class="left-strip-bar".*?</aside>', text, re.DOTALL)
if aside:
    for m in re.finditer(r'<div class="strip-group"[^>]*data-group="([^"]+)".*?<span class="strip-item-label">([^<]+)</span>', aside.group(0), re.DOTALL):
        print(f"Group: {m.group(1):15} | Label: {m.group(2)}")
