import re, sys
sys.stdout.reconfigure(encoding='utf-8')

for p in ["panpaadu.html", "siddha.html", "grihastha.html", "moola-nool.html", "higher-studies.html", "kalvi.html", "books.html", "admissions.html", "index.html"]:
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()
    
    # find images
    matches = re.finditer(r'<img\s+[^>]*src=[\'"]([^\'"]+)[\'"][^>]*>', html, re.I)
    print(f"=== {p} ===")
    for m in matches:
        start = max(0, m.start() - 100)
        end = min(len(html), m.end() + 150)
        print("  IMG:", m.group(1))
        print("  CONTEXT:", html[start:end].replace("\n", " ").strip()[:180])

