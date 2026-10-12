import json, re
r = json.load(open('production/youtube_backup/audit_report.json', encoding='utf-8'))['rows']
known = set(re.findall(r'^(\S+) ', open('production/youtube_dryrun/_blocked_titles.txt', encoding='utf-8').read(), re.M))
held = set('T1KiH3G5WPs pYuwzoJkhTE Lki_Y8OSljs lEHLSYxnpbU mQpQEuXiEZ4 2tL-bKjkL18 pzW2LiiPSVo'.split())
idx = json.load(open('production/youtube_dryrun/_index.json', encoding='utf-8'))
idx = idx if isinstance(idx, list) else [dict(id=k, **x) for k, x in idx.items()]
vault = {i['id']: i.get('vault') for i in idx}
rest = [x for x in r if not x['lyrics'] and x['id'] not in known and x['id'] not in held]
print(len(rest))
with open('production/youtube_dryrun/_other_nolyrics.txt', 'w', encoding='utf-8') as f:
    for x in sorted(rest, key=lambda x: str(vault.get(x['id']))):
        f.write('%s %s %s len=%d %s\n' % (x['id'], vault.get(x['id']), 'PRIV' if x['private'] else 'pub', x['len'], x['title'][:70]))
