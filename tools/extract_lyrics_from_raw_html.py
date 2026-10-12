import json, re, sys

sys.stdout.reconfigure(encoding='utf-8')

def extract_lyrics_from_html(html_path):
    html = open(html_path, encoding='utf-8').read()
    # In NextJS server-rendered HTML for Suno, the prompt / lyrics are passed inside a stream chunk
    # e.g., "prompt":"..." or \"prompt\":\"...\"
    m = re.search(r'\"prompt\":\"(.*?)\",\"type\"', html)
    if not m:
        m = re.search(r'\\\"prompt\\\":\\\"(.*?)\\\",\\\"type\\\"', html)
    if m:
        lyrics = m.group(1).encode('utf-8').decode('unicode-escape')
        return lyrics
    # Search for any large Tamil text block with brackets like [Chorus] or [Verse]
    m2 = re.search(r'(\[(?:Chorus|Verse|Intro|Bridge)\][\s\S]*?)(?:\"|\}\])', html)
    if m2:
        return m2.group(1).encode('utf-8').decode('unicode-escape')
    return None

for name in ['poraiyudaimai', 'vinaithitpam']:
    path = f'scratch/raw_{name}.html'
    l = extract_lyrics_from_html(path)
    print(f"=== {name} lyrics (found: {l is not None}) ===")
    if l:
        print(l[:500])
        with open(f'scratch/lyrics_{name}.txt', 'w', encoding='utf-8') as f:
            f.write(l)
