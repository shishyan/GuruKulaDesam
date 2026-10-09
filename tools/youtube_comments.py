"""Post the lyrics description as a channel-owner comment on 'Topic' copies (videos not editable via videos.update).

  python tools/youtube_comments.py                 # preview matches
  python tools/youtube_comments.py --ids ID --confirm
  python tools/youtube_comments.py --limit 20 --confirm
Matches each Topic video to one of our own uploads that already has lyrics, by normalised title; comment text = that upload's description
(minus hashtags/links line). Logs to production/youtube_backup/comment_log.jsonl. Comment insert costs 50 quota units.
"""
import json, re, sys, argparse, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / 'production' / 'youtube_backup'
LOG = B / 'comment_log.jsonl'
ap = argparse.ArgumentParser()
ap.add_argument('--ids'); ap.add_argument('--limit', type=int, default=0); ap.add_argument('--confirm', action='store_true')
a = ap.parse_args()

TAMIL = re.compile(r'[\u0B80-\u0BFF]')
def norm(t):
    t = t.split('|')[0]
    t = re.sub(r'\((?:original|remix|female|symphony|i+|[0-9]+)\)|\[.*?\]|2026|[\s\-:!,.]+', '', t, flags=re.I)
    return t.lower()

own = json.load(open(B / 'videos.json', encoding='utf-8'))
topic = json.load(open(B / 'playlist_only_videos.json', encoding='utf-8'))
applied = set()
for l in open(B / 'apply_log.jsonl', encoding='utf-8'):
    r = json.loads(l)
    if r.get('ok') and not r.get('rollback'): applied.add(r['id'])
src = {}
for v in own:
    d = v['snippet']['description']
    if v['id'] not in applied: continue
    if sum(1 for l in d.splitlines() if TAMIL.search(l)) >= 4 and 'பாடல் வரிகள்' in d:
        src.setdefault(norm(v['snippet']['title']), v)

done = set()
if LOG.exists():
    for l in open(LOG, encoding='utf-8'):
        r = json.loads(l)
        if r.get('ok'): done.add(r['id'])

want = set(a.ids.split(',')) if a.ids else None
todo = []
f2o = {m['original']: m['film'] for m in json.load(open(B / 'film_to_original.json', encoding='utf-8'))}
ownd = {v['id']: v for v in own}
for t in topic:
    if t['id'] in done or (want and t['id'] not in want): continue
    f = f2o.get(t['id'])
    if f and f in applied and f in ownd: todo.append((t, ownd[f]))
print(len(topic), 'topic videos;', len(todo), 'matched to a lyrics description', flush=True)
if a.limit: todo = todo[:a.limit]
if not a.confirm:
    for t, s in todo[:8]:
        print(t['id'], '<-', s['id'], ascii(t['snippet']['title'])[:60])
    sys.exit()

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
creds = Credentials.from_authorized_user_file(str(ROOT / 'data/credentials/token.json'))
if creds.expired and creds.refresh_token: creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)
for t, s in todo:
    d = s['snippet']['description']
    d = '\n'.join(l for l in d.splitlines() if not l.strip().startswith('#') and 'youtube.com/watch' not in l)[:9500]
    try:
        r = yt.commentThreads().insert(part='snippet', body={'snippet': {'videoId': t['id'], 'topLevelComment': {'snippet': {'textOriginal': d}}}}).execute()
        log = {'id': t['id'], 'ok': True, 'comment': r['id'], 'from': s['id']}
        print(t['id'], 'COMMENTED', r['id'], flush=True)
    except HttpError as e:
        log = {'id': t['id'], 'ok': False, 'err': str(e)[:300]}
        print(t['id'], 'FAIL', str(e)[:200], flush=True)
        if 'quota' in str(e).lower(): break
    open(LOG, 'a', encoding='utf-8').write(json.dumps(log, ensure_ascii=False) + '\n')
