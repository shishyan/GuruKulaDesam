"""Apply dry-run descriptions to YouTube (videos.update) safely.

  python tools/youtube_apply.py --ids ID1,ID2            # preview only
  python tools/youtube_apply.py --ids ID1 --confirm      # really update
  python tools/youtube_apply.py --vault thirukkural --limit 25 --confirm
  python tools/youtube_apply.py --rollback ID1,ID2 --confirm   # restore previous descriptions

Safety:
 * only items in production/youtube_dryrun/_index.json with action 'update'
 * items flagged needs_audio_check are skipped unless --allow-audio-check
 * re-reads the live video first; refuses if its description differs from the backup (edited since)
 * sends the full existing snippet back (title, categoryId, tags, languages) so nothing else changes
 * logs old+new description to production/youtube_backup/apply_log.jsonl; re-reads after update to verify
 * stops cleanly on quota exhaustion (videos.update = 50 units; default quota 10,000/day)
"""
import argparse, json, pathlib, sys, time
ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / 'production' / 'youtube_backup'
D = ROOT / 'production' / 'youtube_dryrun'
LOG = B / 'apply_log.jsonl'

ap = argparse.ArgumentParser()
ap.add_argument('--ids'); ap.add_argument('--vault'); ap.add_argument('--limit', type=int, default=0)
ap.add_argument('--confirm', action='store_true'); ap.add_argument('--allow-audio-check', action='store_true')
ap.add_argument('--rollback')
a = ap.parse_args()

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
creds = Credentials.from_authorized_user_file(str(ROOT / 'data/credentials/token.json'))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

def live(vid):
    r = yt.videos().list(part='snippet', id=vid).execute()['items']
    return r[0]['snippet'] if r else None

def update(vid, new_desc):
    sn = live(vid)
    body = {'id': vid, 'snippet': {k: sn[k] for k in ('title', 'categoryId', 'tags', 'defaultLanguage', 'defaultAudioLanguage') if k in sn}}
    body['snippet']['description'] = new_desc
    yt.videos().update(part='snippet', body=body).execute()
    return sn.get('description', '')

def log(rec):
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')

if a.rollback:
    last = {}
    for l in open(LOG, encoding='utf-8'):
        r = json.loads(l)
        if r.get('ok'):
            last[r['id']] = r
    for vid in a.rollback.split(','):
        r = last.get(vid)
        if not r:
            print(vid, 'nothing to roll back'); continue
        print(vid, 'ROLLBACK ->', len(r['old']), 'chars', '(applied)' if a.confirm else '(preview)')
        if a.confirm:
            update(vid, r['old']); log({'id': vid, 'ok': True, 'rollback': True, 'old': r['new'], 'new': r['old'], 't': time.time()})
    sys.exit(0)

backup = {v['id']: v for v in json.load(open(B / 'videos.json', encoding='utf-8'))}
index = json.load(open(D / '_index.json', encoding='utf-8'))
want = set(a.ids.split(',')) if a.ids else None
latest = {}
if LOG.exists():
    for l in open(LOG, encoding='utf-8'):
        r = json.loads(l)
        if r.get('ok'):
            latest[r['id']] = r
done = {k for k, r in latest.items() if not r.get('rollback')}
todo = []
for x in index:
    if x['action'] != 'update' or x['id'] in done:
        continue
    if want and x['id'] not in want:
        continue
    if a.vault and x['vault'] != a.vault:
        continue
    if 'needs_audio_check' in x.get('note', '') and not a.allow_audio_check:
        continue
    if not x.get('public', True):
        continue
    todo.append(x)
if a.limit:
    todo = todo[:a.limit]
print(f'{len(todo)} video(s) to {"UPDATE" if a.confirm else "preview"}', flush=True)

ok = 0
for x in todo:
    vid = x['id']
    new = (D / x['vault'] / f'{vid}.txt').read_bytes().decode('utf-8').replace('\r\n', '\n')
    cur = live(vid)
    if cur is None:
        print(vid, 'SKIP: not found'); continue
    if cur.get('description', '').strip() == new.strip():
        print(vid, 'already shows the new description - recording as done')
        if a.confirm:
            log({'id': vid, 'ok': True, 'old': backup[vid]['snippet'].get('description', ''), 'new': new, 't': time.time(), 'note': 'found already applied'})
        continue
    if cur.get('description', '') != backup[vid]['snippet'].get('description', ''):
        print(vid, 'SKIP: description changed on YouTube since backup - re-run youtube_audit.py'); continue
    if len(new.encode('utf-8')) > 5000 or '<' in new or '>' in new:
        print(vid, 'SKIP: invalid new description'); continue
    print(f"{vid} {x['title'][:40]} | {len(cur['description'])} -> {len(new)} chars", flush=True)
    if not a.confirm:
        continue
    try:
        old = update(vid, new)
        good = False
        for _ in range(6):
            time.sleep(2)
            chk = live(vid)
            good = chk['description'].strip() == new.strip() and chk.get('title') == cur.get('title') and chk.get('categoryId') == cur.get('categoryId')
            if good:
                break
        log({'id': vid, 'ok': good, 'old': old, 'new': new, 't': time.time()})
        print('   ', 'VERIFIED live' if good else 'MISMATCH after update!', flush=True)
        ok += good
    except HttpError as e:
        msg = str(e)
        log({'id': vid, 'ok': False, 'error': msg[:300], 't': time.time()})
        print('   ERROR', msg[:200])
        if 'quota' in msg.lower():
            print('Quota exhausted - stopping. Resume tomorrow (script skips completed videos).'); break
        time.sleep(2)
print(f'done: {ok} verified')
