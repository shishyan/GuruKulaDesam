"""Sign in with a different Google account and save a separate token (does NOT touch token.json).

  python tools/youtube_login_alt.py [login_hint_email]
A browser window opens; pick the account and approve. Prints the channel(s) the token can act as.
"""
import sys, pathlib
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
ROOT = pathlib.Path(__file__).resolve().parent.parent
CRED = ROOT / 'data' / 'credentials'
hint = sys.argv[1] if len(sys.argv) > 1 else None
flow = InstalledAppFlow.from_client_secrets_file(str(CRED / 'client_secrets.json'), ['https://www.googleapis.com/auth/youtube.force-ssl'])
creds = flow.run_local_server(port=8765, login_hint=hint, prompt='consent select_account', open_browser=False,
                              authorization_prompt_message='OPEN THIS URL: {url}')
(CRED / 'token_alt.json').write_text(creds.to_json(), encoding='utf-8')
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)
for c in yt.channels().list(part='snippet', mine=True).execute().get('items', []):
    print('channel:', c['snippet']['title'], c['id'])
print('saved token_alt.json')
