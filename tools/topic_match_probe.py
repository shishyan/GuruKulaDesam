import json, re
B = 'production/youtube_backup/'
own = {v['id']: v for v in json.load(open(B + 'videos.json', encoding='utf-8'))}
topic = json.load(open(B + 'playlist_only_videos.json', encoding='utf-8'))
applied = {json.loads(l)['id'] for l in open(B + 'apply_log.jsonl', encoding='utf-8') if json.loads(l).get('ok') and not json.loads(l).get('rollback')}
def key(t):
    t = re.split(r'[|(\[]', t)[0]
    t = re.sub(r'[^\u0B80-\u0BFF]', '', t)
    t = re.sub(r'[\u0BCD\u0BBE-\u0BCC\u0BC6-\u0BC8]', '', t)  # drop vowel signs and pulli for fuzz
    return t
ak = {}
for i in applied:
    if i in own: ak.setdefault(key(own[i]['snippet']['title']), []).append(i)
hits = [(t, ak[key(t['snippet']['title'])]) for t in topic if key(t['snippet']['title']) in ak]
print(len(hits))
for t, a in hits[:60]:
    print(t['id'], a[0], ascii(t['snippet']['title'])[:50])
