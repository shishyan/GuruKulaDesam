import re
import glob

for f in sorted(glob.glob('scraped_*.html')):
    content = open(f, encoding='utf-8').read()
    
    # search for iframe src
    for m in re.finditer(r'<iframe[^>]+src=["\']([^"\']+)["\']', content, re.IGNORECASE):
        print(f"{f} iframe src: {m.group(1)}")
        
    # search for href with docs or drive
    for m in re.finditer(r'<a[^>]+href=["\']([^"\']*(?:docs\.google|drive\.google)[^"\']*)["\'][^>]*>(.*?)</a>', content, re.IGNORECASE | re.DOTALL):
        print(f"{f} link: {m.group(1)} -> {m.group(2)[:40]}")
        
    # search for any occurrences of docs.google.com/document/d/
    for m in re.finditer(r'https?://docs\.google\.com/document/d/([a-zA-Z0-9_-]+)', content):
        print(f"{f} GOOGLE DOC FOUND: {m.group(0)}")

    # search for any occurrences of docs.google.com/spreadsheets/d/
    for m in re.finditer(r'https?://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)', content):
        print(f"{f} GOOGLE SHEET FOUND: {m.group(0)}")
        
    # search for any occurrences of drive.google.com/file/d/
    for m in re.finditer(r'https?://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)', content):
        print(f"{f} DRIVE FILE FOUND: {m.group(0)}")

print("Done scanning scraped files.")
