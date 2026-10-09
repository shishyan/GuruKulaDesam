import glob
import re
import os

pages = sorted(glob.glob("*.html"))
print(f"{'Page':<30} {'Imgs':<6} {'Sections with img':<20}")
print("=" * 60)

for p in pages:
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()
    
    imgs = re.findall(r'<img\s+[^>]*src=[\'"]([^\'"]+)[\'"][^>]*>', content, re.IGNORECASE)
    if not imgs:
        continue
    
    # Check for gallery or visual-grid containers
    galleries = re.findall(r'<div[^>]*class=[\'"][^\'"]*(?:gallery|visual-grid|image-grid|photo-grid|showcase|visual-mosaic)[^\'"]*[\'"][^>]*>', content, re.IGNORECASE)
    
    print(f"{p:<30} {len(imgs):<6} Galleries: {len(galleries)}")
    for g in galleries[:3]:
        print(f"   {g[:80]}")

