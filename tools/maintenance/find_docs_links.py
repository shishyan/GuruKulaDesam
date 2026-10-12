import re
import glob

links = set()
for f in glob.glob('scraped_*.html'):
    content = open(f, encoding='utf-8').read()
    # find all URLs
    all_urls = re.findall(r'https?://[^\s"\'<>]+', content)
    for u in all_urls:
        if 'google.com' in u or 'drive.google' in u:
            # clean trailing punctuation
            u = u.rstrip('\\"\'.,;')
            if any(k in u for k in ['document', 'spreadsheets', 'presentation', 'drive.google', 'forms', 'viewer']):
                links.add((f, u))

print(f"Total unique doc/drive URLs found: {len(links)}")
for f, u in sorted(links):
    print(f"{f} -> {u}")
