import urllib.request
import urllib.parse
import re
import sys
import json
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding='utf-8')

pages = [
    ("Home", "/view/wwwgurukuladesamcom/home"),
    ("Saiva Neri - Grade 1", "/view/wwwgurukuladesamcom/home/சவ-நற/தரம-1"),
    ("Saiva Neri - Grade 2", "/view/wwwgurukuladesamcom/home/சவ-நற/தரம-2"),
    ("Saiva Neri - Grade 3", "/view/wwwgurukuladesamcom/home/சவ-நற/தரம-3"),
    ("Saiva Neri - Grade 4", "/view/wwwgurukuladesamcom/home/சவ-நற/தரம-4"),
    ("Saiva Neri - Grade 5", "/view/wwwgurukuladesamcom/home/சவ-நற/தரம-5"),
    ("Saiva Neri - Grade 6", "/view/wwwgurukuladesamcom/home/சவ-நற/தரம-6"),
    ("Saiva Neri - Grade 7", "/view/wwwgurukuladesamcom/home/சவ-நற/தரம-7"),
    ("Saiva Neri - Grade 8", "/view/wwwgurukuladesamcom/home/சவ-நற/தரம-8"),
    ("Saiva Neri - Grade 9", "/view/wwwgurukuladesamcom/home/சவ-நற/தரம-9"),
    ("Saiva Neri - Grade 10", "/view/wwwgurukuladesamcom/home/சவ-நற/தரம-10"),
    ("Saiva Neri - Grade 11", "/view/wwwgurukuladesamcom/home/சவ-நற/தரம-11"),
    ("Saiva Neri - Grade 12", "/view/wwwgurukuladesamcom/home/சவ-நற/தரம-12"),
    ("Syllabus - Irai Isai Virundhu", "/view/wwwgurukuladesamcom/home/syllabus/இற-இச-வரநத"),
    ("Syllabus - Untitled", "/view/wwwgurukuladesamcom/home/syllabus/untitled-page"),
    ("Classes - Untitled", "/view/wwwgurukuladesamcom/home/classes/untitled-page"),
    ("YouTube", "/view/wwwgurukuladesamcom/home/youtube"),
]

base_url = "https://sites.google.com"

results = {}

for name, path in pages:
    encoded_path = urllib.parse.quote(path)
    url = base_url + encoded_path
    print(f"\n==========================================")
    print(f"Fetching: {name} ({url})")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            # Find title
            title_m = re.search(r'<title>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
            title = title_m.group(1).strip() if title_m else ""
            
            # Find embedded iframes (e.g. YouTube, Google Drive, Forms)
            iframes = re.findall(r'<iframe[^>]+src=[\'"]([^\'"]+)[\'"]', html, re.IGNORECASE)
            
            # Find youtube video IDs or links
            yt_links = re.findall(r'(?:https?:)?//(?:www\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=|embed/|shorts/)?([a-zA-Z0-9_-]{11})', html)
            
            # Find google drive or docs links
            drive_links = re.findall(r'https?://(?:drive|docs)\.google\.com/[^\s"\'<>]+', html)

            # Find all text content in sections
            # In Google Sites, text often resides in role="region" or <section> or <div class="typography-body"> or similar
            # Let's extract paragraphs / headings
            text_blocks = re.findall(r'<(?:h1|h2|h3|p|div)[^>]*class=[\'"][^\'"]*(?:zfr3Q|duRjpb|JYVBee|OmQG5e|C9DxTc|typography)[^\'"]*[\'"][^>]*>(.*?)</(?:h1|h2|h3|p|div)>', html, re.DOTALL)
            clean_texts = []
            for tb in text_blocks:
                ct = re.sub(r'<[^>]+>', ' ', tb).strip()
                ct = ' '.join(ct.split())
                if ct and ct not in clean_texts and len(ct) > 1:
                    clean_texts.append(ct)
            
            print(f"Title: {title}")
            print(f"YouTube videos: {set(yt_links)}")
            print(f"Drive links: {set(drive_links)}")
            print(f"Iframes: {set(iframes)}")
            print(f"Text blocks count: {len(clean_texts)}")
            for t in clean_texts[:10]:
                print(f"  - {t}")
            if len(clean_texts) > 10:
                print(f"  ... and {len(clean_texts)-10} more text blocks")
                
            results[name] = {
                "name": name,
                "path": path,
                "url": url,
                "title": title,
                "youtube": list(set(yt_links)),
                "drive": list(set(drive_links)),
                "iframes": list(set(iframes)),
                "text_blocks": clean_texts,
                "html_len": len(html)
            }
            # Save raw html for reference
            clean_filename = re.sub(r'[^\w\-_\.]', '_', name)
            with open(f"scraped_{clean_filename}.html", "w", encoding="utf-8") as f_out:
                f_out.write(html)
    except Exception as e:
        print(f"Error fetching {name}: {e}")

with open("scraped_summary.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nDone scraping all pages.")
