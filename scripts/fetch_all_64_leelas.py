import urllib.request
import re
import sys

# Let's inspect Thiruvilaiyadal Puranam on Project Madurai (64 Leelas)
# pmuni0463_01.html, pmuni0463_02.html, pmuni0474_01.html, pmuni0474_02.html, pmuni0497.html
urls = [
    'https://www.projectmadurai.org/pm_etexts/utf8/pmuni0463_01.html',
    'https://www.projectmadurai.org/pm_etexts/utf8/pmuni0463_02.html',
    'https://www.projectmadurai.org/pm_etexts/utf8/pmuni0474_01.html',
    'https://www.projectmadurai.org/pm_etexts/utf8/pmuni0474_02.html',
    'https://www.projectmadurai.org/pm_etexts/utf8/pmuni0497.html'
]

total_padalams = []
for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract padalam headings
            matches = re.findall(r'<h[34][^>]*>(.*?)</h[34]>', html, re.I | re.S)
            for m in matches:
                clean = re.sub(r'<[^>]+>', '', m).strip()
                if 'படலம்' in clean:
                    total_padalams.append(clean)
    except Exception as e:
        print(f"Error {u}: {e}")

sys.stdout.buffer.write((f"Total distinct padalams across Thiruvilaiyadal: {len(total_padalams)}\n").encode('utf-8'))
for i, p in enumerate(total_padalams[:20]):
    sys.stdout.buffer.write((f"{i+1}: {p}\n").encode('utf-8'))
