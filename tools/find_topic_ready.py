import json
idx = json.load(open('production/youtube_dryrun/_index.json', encoding='utf-8'))
idx = idx if isinstance(idx, list) else [dict(id=k, **x) for k, x in idx.items()]
up = {v['id'] for v in json.load(open('production/youtube_backup/videos.json', encoding='utf-8'))}
top = [i for i in idx if i['id'] not in up]
print('index', len(idx), 'not own uploads', len(top))
from collections import Counter
print(Counter(i['action'].split(' ')[0] for i in top))
for i in [x for x in top if x['action'] == 'update'][:5]:
    print(i['id'], i['vault'], i['bytes'])
