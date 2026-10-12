import sys
import pathlib

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

tokens = [
    'data/credentials/token.json',
    'data/credentials/token_alt.json',
    'data/credentials/token_backup_guru-kula-desam.json'
]

for t in tokens:
    p = pathlib.Path(t)
    if not p.exists():
        print(f"[{t}] does not exist.")
        continue
    try:
        c = Credentials.from_authorized_user_file(str(p))
        if c.expired and c.refresh_token:
            c.refresh(Request())
        yt = build('youtube', 'v3', credentials=c, cache_discovery=False)
        res = yt.videos().list(part='id', id='4s48KQnjSyQ').execute()
        print(f"[{t}] QUOTA_OK! Items returned: {len(res.get('items', []))}")
    except Exception as e:
        if 'quotaExceeded' in str(e):
            print(f"[{t}] QUOTA_EXCEEDED")
        else:
            print(f"[{t}] ERROR:", e)
