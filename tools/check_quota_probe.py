import sys, pathlib
p = pathlib.Path('data/credentials/token.json')
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
c = Credentials.from_authorized_user_file(str(p))
if c.expired and c.refresh_token: c.refresh(Request())
yt = build('youtube', 'v3', credentials=c, cache_discovery=False)
try:
    yt.videos().list(part='snippet', id='4s48KQnjSyQ').execute()
    print('QUOTA_OK')
except Exception as e:
    if 'quotaExceeded' in str(e):
        print('QUOTA_EXCEEDED')
    else:
        print('ERROR:', e)
