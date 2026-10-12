import sys, json, pathlib, shutil, os
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

ROOT = pathlib.Path(__file__).resolve().parent.parent
CRED_DIR = ROOT / 'data' / 'credentials'
NEW_SECRET = ROOT / 'client_secret_336846523109-uvh5e4e0209g2p1ojmhpq02uu349pkpt.apps.googleusercontent.com.json'

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtubepartner'
]

print(f"Loading client secret from: {NEW_SECRET}", flush=True)
flow = InstalledAppFlow.from_client_secrets_file(str(NEW_SECRET), SCOPES)

print("\nStarting local server on port 8088. Opening browser...", flush=True)

creds = flow.run_local_server(
    port=8088,
    prompt='consent select_account',
    open_browser=True,
    authorization_prompt_message="\n" + "="*70 + "\nPLEASE OPEN THIS URL IN YOUR BROWSER:\n{url}\n" + "="*70 + "\n"
)

# Test YouTube API call
try:
    yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)
    channels_res = yt.channels().list(part='snippet', mine=True).execute()
    channels = channels_res.get('items', [])
    print("\nSUCCESSFULLY CONNECTED TO YOUTUBE!", flush=True)
    for c in channels:
        print(f" -> Channel: {c['snippet']['title']} (ID: {c['id']})", flush=True)
    
    # Save new client_secrets.json and token.json
    old_secret = CRED_DIR / 'client_secrets.json'
    old_token = CRED_DIR / 'token.json'

    shutil.copy(NEW_SECRET, old_secret)
    with open(old_token, 'w', encoding='utf-8') as f:
        f.write(creds.to_json())

    print("\nSAVED new client_secrets.json and token.json!", flush=True)
    print("Project switched successfully to gurukuladesam-4 (Quota is now fresh!).", flush=True)

except Exception as e:
    err_msg = str(e)
    print(f"\nERROR testing YouTube API with new credentials: {err_msg}", flush=True)
    if "has not been used in project" in err_msg or "is not enabled" in err_msg or "accessNotConfigured" in err_msg:
        print("\n" + "!"*70, flush=True)
        print("ACTION REQUIRED: YouTube Data API v3 is not enabled yet in this project!")
        print("Please enable it at:", flush=True)
        print("https://console.cloud.google.com/apis/library/youtube.googleapis.com?project=gurukuladesam-2", flush=True)
        print("!"*70, flush=True)
    raise
