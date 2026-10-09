"""Read-only: for 'no lyrics' films, find the linked ORIGINAL song upload and check whether it has lyrics."""
import json, re, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / 'production' / 'youtube_backup'
vids = {v['id']: v for v in json.load(open(B / 'videos.json', encoding='utf-8'))}
rows = {r['id']: r for r in json.load(open(B / 'audit_report.json', encoding='utf-8'))['rows']}
URL = re.compile(r'(?:youtu\.be/|watch\?v=)([A-Za-z0-9_-]{11})')

st = collections.Counter()
detail = []
for vid, r in rows.items():
    if r['lyrics']:
        continue
    d = vids[vid]['snippet'].get('description', '')
    links = [m for m in URL.findall(d) if m != vid]
    if not links:
        st['no_original_link'] += 1; detail.append((vid, None, 'no link')); continue
    src = None
    for l in links:
        if l in rows and rows[l]['lyrics']:
            src = l; break
    if src:
        st['original_in_channel_with_lyrics'] += 1; detail.append((vid, src, 'ok'))
    elif any(l in rows for l in links):
        st['original_in_channel_no_lyrics'] += 1; detail.append((vid, links[0], 'orig no lyrics'))
    else:
        st['original_not_in_audit'] += 1; detail.append((vid, links[0], 'orig outside audit'))
print(dict(st))
json.dump([{'film': a, 'original': b, 'status': c} for a, b, c in detail],
          open(B / 'film_to_original.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for a, b, c in [x for x in detail if x[2] != 'ok'][:10]:
    print(c, a, b, vids[a]['snippet']['title'][:50])
