import json
log = {}
for l in open('production/youtube_backup/apply_log.jsonl', encoding='utf-8'):
    r = json.loads(l)
    if r.get('ok'):
        log[r['id']] = r
rows = {x['id']: x for x in json.load(open('production/youtube_backup/audit_report.json', encoding='utf-8'))['rows']}
bad = [i for i, r in log.items() if not r.get('rollback') and i in rows and not rows[i]['lyrics']]
print('applied:', len([1 for r in log.values() if not r.get('rollback')]), 'now lacking lyrics live:', len(bad))
for i in bad:
    print(i, rows[i]['len'], len(log[i].get('new', '')), rows[i]['title'][:50].encode('ascii', 'replace').decode())
