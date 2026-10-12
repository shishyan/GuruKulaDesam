import urllib.request, json, re, sys, pathlib

sys.stdout.reconfigure(encoding='utf-8')

# 1. Local SRT
p = pathlib.Path('production/subtitles/Mata6vtnrjQ.srt')
if p.exists():
    print("=== LOCAL SRT FILE (production/subtitles/Mata6vtnrjQ.srt) ===")
    print(p.read_text(encoding='utf-8')[:1200])
else:
    print("LOCAL SRT DOES NOT EXIST")

# 2. Live YouTube captions
url = "https://www.youtube.com/watch?v=Mata6vtnrjQ"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
m = re.search(r'"captionTracks":(\[.*?\])', html)
if m:
    tracks = json.loads(m.group(1))
    print("\n=== LIVE CAPTION TRACKS ON YOUTUBE ===")
    for t in tracks:
        print("Track:", t.get('name'), "| lang:", t.get('languageCode'), "| kind:", t.get('kind'))
        base_url = t.get('baseUrl')
        if base_url:
            cap_xml = urllib.request.urlopen(base_url, timeout=10).read().decode('utf-8', errors='ignore')
            print("--- First 800 chars of live timed text XML ---")
            print(repr(cap_xml[:300]))
            print(cap_xml)
else:
    print("No live captionTracks found in watch page.")
