import sys
import os
import pathlib
import time

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

ROOT = pathlib.Path(__file__).resolve().parent.parent
CRED_DIR = ROOT / 'data' / 'credentials'
# Project: gurukuladesam-4
SECRET_FILE = ROOT / "client_secret_336846523109-uvh5e4e0209g2p1ojmhpq02uu349pkpt.apps.googleusercontent.com.json"

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtubepartner'
]

flow = InstalledAppFlow.from_client_secrets_file(str(SECRET_FILE), SCOPES)
flow.redirect_uri = 'http://localhost:8088/'

auth_url, _ = flow.authorization_url(
    prompt='consent select_account',
    access_type='offline',
    include_granted_scopes='true'
)

print("\n" + "="*80)
print("OAUTH LINK (Click or paste into your browser where shishyan@gmail.com is logged in):")
print("="*80)
print(auth_url)
print("="*80 + "\n", flush=True)

print("Listening on http://localhost:8088/ for authorization callback...", flush=True)
creds = flow.run_local_server(port=8088, prompt='consent select_account', open_browser=True)

# Save to token.json and token_backup
token_path = CRED_DIR / 'token.json'
with open(token_path, 'w', encoding='utf-8') as f:
    f.write(creds.to_json())

print("\nSUCCESS! New token saved to data/credentials/token.json (Project: gurukuladesam-2)", flush=True)
