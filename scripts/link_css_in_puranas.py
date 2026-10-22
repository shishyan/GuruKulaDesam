import os

ROOT = r"C:\GitHub\Gurukuladesam"
files = [
    os.path.join(ROOT, "puranas.html"),
    os.path.join(ROOT, "docs", "puranas.html"),
    os.path.join(ROOT, "site", "puranas.html")
]

for f in files:
    with open(f, "r", encoding="utf-8") as fp:
        html = fp.read()
    if "story-reader-layout.css" not in html:
        html = html.replace('</head>', '  <link rel="stylesheet" href="assets/css/story-reader-layout.css?v=1.0">\n</head>')
        with open(f, "w", encoding="utf-8") as fp:
            fp.write(html)
        print(f"Added story-reader-layout.css to {f}")
    else:
        print(f"Already linked in {f}")
