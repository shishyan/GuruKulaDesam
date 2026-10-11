import urllib.request, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

def check_video_captions(vid):
    url = f'https://www.youtube.com/watch?v={vid}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
    except Exception as e:
        return f"Error: {e}"
        
    m = re.search(r'"captionTracks":(\[.*?\])', html)
    if m:
        try:
            tracks = json.loads(m.group(1))
            return tracks
        except Exception as e:
            return f"JSON Error: {e}"
    return []

sample_vids = ['4s48KQnjSyQ', 'IHMZsM7LJf8', 'uPk4dyag74Y', '02C8glMmetw', 'CikMJKSLIRw', 'lvlDsTq-skg']
for v in sample_vids:
    tr = check_video_captions(v)
    if isinstance(tr, list):
        print(f"{v}: {len(tr)} track(s)")
        for t in tr:
            lang = t.get('languageCode')
            name = t.get('name', {}).get('simpleText')
            kind = t.get('kind', 'standard')
            vssId = t.get('vssId')
            is_default = t.get('isDefault', False)
            print(f"   lang={lang} name='{name}' kind={kind} vssId={vssId} default={is_default}")
    else:
        print(f"{v}: {tr}")
