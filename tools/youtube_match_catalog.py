"""Read-only: spot-check 'no lyrics' videos and match all videos to catalog.json."""
import json, pathlib, random, collections, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / 'production' / 'youtube_backup'
rep = json.load(open(B / 'audit_report.json', encoding='utf-8'))
vids = {v['id']: v for v in json.load(open(B / 'videos.json', encoding='utf-8'))}
cat = json.load(open(ROOT / 'assets/data/catalog.json', encoding='utf-8'))
cid = {}
for vault, items in cat.items():
    for i in items:
        cid.setdefault(i['id'], (vault, i))

rows = rep['rows']
nol = [r for r in rows if not r['lyrics']]
random.seed(7)
print('--- SPOT CHECK: 8 random "no lyrics" videos ---')
for r in random.sample(nol, 8):
    d = vids[r['id']]['snippet'].get('description', '')
    print(f"[{r['id']}] {r['title'][:60]} | len={r['len']} private={r['private']}")
    print('   ', d[:230].replace('\n', ' / '), flush=True)

print('\n--- CATALOG MATCH ---')
st = collections.Counter()
by = collections.defaultdict(collections.Counter)
for r in rows:
    hit = cid.get(r['id'])
    if not hit:
        k = 'not_in_catalog'; vault = 'none'
    else:
        vault, it = hit
        has_l = len((it.get('lyrics') or '').strip()) > 40
        has_m = len((it.get('meaning') or '').strip()) > 40
        k = ('cat_lyrics+meaning' if has_l and has_m else 'cat_lyrics_only' if has_l else 'cat_meaning_only' if has_m else 'cat_neither')
    st[k] += 1
    by[vault][('yt_has_lyrics' if r['lyrics'] else 'yt_no_lyrics') + '|' + k] += 1
print(dict(st))
for v, c in by.items():
    print(v, dict(c))
need = [r for r in rows if not r['lyrics'] and cid.get(r['id']) and len((cid[r['id']][1].get('lyrics') or '').strip()) > 40]
print(f'\nFILLABLE from catalog (YT lacks lyrics, catalog has them): {len(need)}')
private = sum(r['private'] for r in rows)
print('non-public videos:', private)
print('titles not in catalog (sample):', [r['title'][:40] for r in rows if r['id'] not in cid][:8])
