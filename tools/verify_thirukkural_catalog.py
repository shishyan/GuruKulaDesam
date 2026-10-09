"""Verify Thirukkural catalog lyrics against the canonical kural dataset (production/thirukkural_all.json).

For each catalog entry: parse 'குறள் N:' blocks, compare the two lines with the canonical text
(whitespace/punctuation-insensitive), and report kural count, mismatches, and chapter coverage.
Writes production/youtube_backup/thirukkural_verified.json (id -> {status, kurals, issues}).
"""
import json, re, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
canon = {k['Number']: (k['Line1'], k['Line2']) for k in json.load(open(ROOT / 'production/thirukkural_all.json', encoding='utf-8'))['kural']}
norm = lambda s: re.sub(r'[\s\.\,\;\!\?\u200c\u200d]+', '', s or '')
cat = json.load(open(ROOT / 'assets/data/catalog.json', encoding='utf-8'))['thirukkural']
rep = {k['id']: k for k in json.load(open(ROOT / 'production/youtube_backup/audit_report.json', encoding='utf-8'))['rows']}

out, tally = {}, {'ok': 0, 'mismatch': 0, 'parse_fail': 0}
for it in cat:
    L = it.get('lyrics') or ''
    blocks = re.findall(r'குறள்\s*(\d+)\s*:\s*\n(.+?)\n(.+?)(?:\n|$)', L)
    issues, nums = [], []
    for n, l1, l2 in blocks:
        n = int(n); nums.append(n)
        c = canon.get(n)
        if not c:
            issues.append(f'{n}: not in dataset'); continue
        if norm(l1) != norm(c[0]) or norm(l2) != norm(c[1]):
            issues.append(f'{n}: text differs')
    m = re.search(r'அதிகாரம்\s*(\d+)', it['title'])
    exp = None
    if m:
        a = int(m.group(1)); exp = set(range((a - 1) * 10 + 1, a * 10 + 1))
        if nums and not set(nums) <= exp:
            issues.append(f'kural numbers {nums[:3]}.. outside adhikaram {a}')
    status = 'parse_fail' if not nums else ('ok' if not issues else 'mismatch')
    tally[status] += 1
    out[it['id']] = {'status': status, 'kurals': len(nums), 'expected10': (exp is not None and set(nums) == exp),
                     'issues': issues[:5], 'title': it['title'][:50], 'yt_has_lyrics': rep.get(it['id'], {}).get('lyrics')}
(ROOT / 'production/youtube_backup/thirukkural_verified.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print(tally)
import collections
print('kural-count distribution (ok only):', collections.Counter(v['kurals'] for v in out.values() if v['status'] == 'ok'))
print('full-10 chapters:', sum(1 for v in out.values() if v['expected10']))
for k, v in list(out.items()):
    if v['status'] != 'ok':
        print(k, v['status'], v['issues'][:2], v['title'])
        break
