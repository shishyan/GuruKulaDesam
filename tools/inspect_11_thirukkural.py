import json, sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

token_path = 'data/credentials/token_backup_guru-kula-desam.json'
creds = Credentials.from_authorized_user_file(token_path)
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

ids = ['IHMZsM7LJf8', 'UPAYRisyN7Q', 'lvlDsTq-skg', 'OXgMCvchSt8', 'YqHg3hf8T8w', 'u23cwmejN1k', 'U-u4rAYBUkc', '3FoioD6p6Mk', 'AD6LgqNksFQ', 'G6NSHWKhQcY', 'MXK8vB3_fBE']
res = yt.videos().list(part='snippet,contentDetails,status', id=','.join(ids)).execute()
for it in res.get('items', []):
    vid = it['id']
    dur = it['contentDetails']['duration']
    status = it['status']['privacyStatus']
    title = it['snippet']['title']
    print(f"[{vid}] dur={dur} status={status} | {title}")
