import os
import re

ROOT = r"c:\GitHub\Gurukuladesam"
files_to_clean = ["index.html", "kalvi.html", "saiva-neri.html", "irai-isai-virundhu.html", "thirukkural.html", "about.html"]

for fn in files_to_clean:
    fp = os.path.join(ROOT, fn)
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Match course-layout-container with dedicated-sub-sidebar
    pattern = r'<div class="course-layout-container">\s*<!-- Dedicated Sub-Menu Sidebar[\s\S]*?<div class="course-main-column">\s*([\s\S]*?)\s*</div>\s*</div>'
    
    m = re.search(pattern, content)
    if m:
        inner = m.group(1)
        content = content[:m.start()] + inner + content[m.end():]
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        
        for dest in ["docs", "site"]:
            dfp = os.path.join(ROOT, dest, fn)
            if os.path.exists(dfp):
                with open(dfp, "w", encoding="utf-8") as f:
                    f.write(content)
        print(f"Cleaned up {fn} layout successfully")
    else:
        print(f"Pattern did not match {fn}")
