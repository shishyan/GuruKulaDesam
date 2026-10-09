"""READ-ONLY YouTube audit: back up all uploads + playlists and classify descriptions.

Writes production/youtube_backup/{videos,playlists}.json and audit_report.json.
Makes list calls only (1 quota unit each). Never calls update/insert/delete.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CRED = ROOT / 'data' / 'credentials'
OUT = ROOT / 'production' / 'youtube_backup'
OUT.mkdir(parents=True, exist_ok=True)

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file(str(CRED / 'token.json'))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

ch = yt.channels().list(part='snippet,contentDetails,statistics', mine=True).execute()['items'][0]
print('channel:', ch['snippet']['title'], '| videos:', ch['statistics'].get('videoCount'), flush=True)
uploads = ch['contentDetails']['relatedPlaylists']['uploads']

ids, tok = [], None
while True:
    r = yt.playlistItems().list(part='contentDetails', playlistId=uploads, maxResults=50, pageToken=tok).execute()
    ids += [i['contentDetails']['videoId'] for i in r['items']]
    tok = r.get('nextPageToken')
    if not tok: break
videos = []
for i in range(0, len(ids), 50):
    r = yt.videos().list(part='snippet,status,contentDetails', id=','.join(ids[i:i+50])).execute()
    videos += r['items']

playlists, tok = [], None
while True:
    r = yt.playlists().list(part='snippet,contentDetails,status', mine=True, maxResults=50, pageToken=tok).execute()
    playlists += r['items']
    tok = r.get('nextPageToken')
    if not tok: break
pl_items = {}
for p in playlists:
    tok, items = None, []
    while True:
        r = yt.playlistItems().list(part='contentDetails', playlistId=p['id'], maxResults=50, pageToken=tok).execute()
        items += [x['contentDetails']['videoId'] for x in r['items']]
        tok = r.get('nextPageToken')
        if not tok: break
    pl_items[p['id']] = items

(OUT / 'videos.json').write_text(json.dumps(videos, ensure_ascii=False, indent=1), encoding='utf-8')
(OUT / 'playlists.json').write_text(json.dumps({'playlists': playlists, 'items': pl_items}, ensure_ascii=False, indent=1), encoding='utf-8')

TAMIL = re.compile(r'[\u0B80-\u0BFF]')
def classify(v):
    d = v['snippet'].get('description', '')
    lines = [l for l in d.splitlines() if l.strip()]
    tamil_lines = sum(1 for l in lines if TAMIL.search(l))
    has_lyrics = tamil_lines >= 4
    has_meaning = bool(re.search(r'பொருள்|விளக்கம்|meaning|Meaning|அர்த்தம்', d))
    return {'id': v['id'], 'title': v['snippet']['title'], 'len': len(d), 'tamil_lines': tamil_lines,
            'lyrics': has_lyrics, 'meaning': has_meaning, 'private': v['status']['privacyStatus'] != 'public'}
rows = [classify(v) for v in videos]
rep = {
    'videos': len(rows),
    'with_lyrics': sum(r['lyrics'] for r in rows),
    'with_meaning': sum(r['meaning'] for r in rows),
    'lyrics_and_meaning': sum(r['lyrics'] and r['meaning'] for r in rows),
    'lyrics_no_meaning': sum(r['lyrics'] and not r['meaning'] for r in rows),
    'no_lyrics': sum(not r['lyrics'] for r in rows),
    'empty_desc': sum(r['len'] < 30 for r in rows),
    'playlists': [{'id': p['id'], 'title': p['snippet']['title'], 'videos': len(pl_items[p['id']]),
                   'desc_len': len(p['snippet'].get('description', ''))} for p in playlists],
    'rows': rows,
}
(OUT / 'audit_report.json').write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding='utf-8')
print({k: v for k, v in rep.items() if k not in ('rows', 'playlists')}, flush=True)
for p in rep['playlists']:
    print(f"  playlist {p['title'][:50]} | {p['videos']} videos | desc {p['desc_len']} chars", flush=True)

