import json, sys
from pathlib import Path

out = []
p_over = Path('production/youtube_lyrics_overrides.json')
p_db = Path('production/metadata/all_songs_lyrics_and_meanings.json')
p_live = Path('live_youtube_metadata.json')

out.append("=== SEARCHING nuSx1NgiCuo ===")
if p_over.exists():
    with open(p_over, 'r', encoding='utf-8') as f:
        over = json.load(f)
    out.append(f"In overrides: {json.dumps(over.get('nuSx1NgiCuo'), ensure_ascii=False, indent=2)}")

if p_db.exists():
    with open(p_db, 'r', encoding='utf-8') as f:
        db = json.load(f)
    entry = db.get('nuSx1NgiCuo')
    if entry:
        out.append(f"In db title: {entry.get('title')}")
        out.append(f"In db tamil_lyrics:\n{entry.get('tamil_lyrics')}")
    else:
        out.append("nuSx1NgiCuo not found in all_songs_lyrics_and_meanings.json")

if p_live.exists():
    with open(p_live, 'r', encoding='utf-8') as f:
        live = json.load(f)
    l_entry = live.get('nuSx1NgiCuo')
    if l_entry:
        out.append(f"In live_youtube_metadata: {l_entry.get('title')}")
        out.append(f"Description:\n{l_entry.get('description')}")

out.append("\n=== SEARCHING ALL TRACKS WITH 'நாத' OR 'NATHA' ===")
if p_db.exists():
    for k, v in db.items():
        t = v.get('title', '')
        if 'நாத' in t or 'natha' in t.lower():
            out.append(f"Track: {k} | Title: {t}")
            out.append(f"Lyrics snippet:\n{v.get('tamil_lyrics', '')[:300]}\n---")

Path('scratch_natha_check.txt').write_text('\n'.join(out), encoding='utf-8')
print("Wrote scratch_natha_check.txt")
