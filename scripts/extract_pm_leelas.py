import urllib.request
import re
import sys

# Fetch Project Madurai Thiruvilaiyadal Puranam parts
urls = [
    ('https://www.projectmadurai.org/pm_etexts/utf8/pmuni0463_01.html', 'மதுரைக் காண்டம் (பாகம் 1)'),
    ('https://www.projectmadurai.org/pm_etexts/utf8/pmuni0463_02.html', 'மதுரைக் காண்டம் (பாகம் 2)'),
    ('https://www.projectmadurai.org/pm_etexts/utf8/pmuni0474_01.html', 'கூடற் காண்டம் (பாகம் 1)'),
    ('https://www.projectmadurai.org/pm_etexts/utf8/pmuni0474_02.html', 'கூடற் காண்டம் (பாகம் 2)'),
    ('https://www.projectmadurai.org/pm_etexts/utf8/pmuni0497.html', 'திருவாலவாய்க் காண்டம்')
]

all_leelas = []

for u, kandam in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract sections by <h3 ...> or <h4 ...>
            sections = re.split(r'<h[34][^>]*>(.*?)</h[34]>', html, flags=re.I | re.S)
            for i in range(1, len(sections), 2):
                title = re.sub(r'<[^>]+>', '', sections[i]).strip()
                title = re.sub(r'\s+', ' ', title)
                body = sections[i+1]
                # Clean text to extract authentic verses / text
                text = re.sub(r'<br\s*/?>', '\n', body, flags=re.I)
                text = re.sub(r'<[^>]+>', '', text)
                lines = [l.strip() for l in text.split('\n') if l.strip()]
                clean_story = '\n'.join(lines)
                if 'படலம்' in title and len(clean_story) > 300:
                    all_leelas.append({
                        'kandam': kandam,
                        'title': title,
                        'content': clean_story
                    })
    except Exception as e:
        print(f"Error {u}: {e}")

sys.stdout.buffer.write((f"Successfully extracted {len(all_leelas)} authentic padalams with real text!\n").encode('utf-8'))
for i, l in enumerate(all_leelas[:10]):
    sys.stdout.buffer.write((f"{i+1}: {l['title']} ({len(l['content'])} chars)\n").encode('utf-8'))
