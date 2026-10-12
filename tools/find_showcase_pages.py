import glob
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

pages = sorted(glob.glob("*.html"))
print(f"Total HTML files: {len(pages)}")

showcase_pages = []
for p in pages:
    if p.startswith("scraped_"):
        continue
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()
    
    # check for visual showcase or any img tags
    has_showcase = "page-visual-showcase" in html
    imgs = re.findall(r'<img\s+[^>]*src=[\'"]([^\'"]+)[\'"][^>]*>', html, re.I)
    
    if has_showcase or len(imgs) > 0:
        showcase_pages.append((p, has_showcase, len(imgs)))

for sp, has_s, img_c in showcase_pages:
    print(f"{sp:<30} showcase={has_s!s:<6} img_count={img_c}")

