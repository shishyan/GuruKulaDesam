import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file(str(ROOT / 'data/credentials/token.json'))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

with open(ROOT / 'live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    metadata = json.load(f)

targets = {
    'On2xoZqBsss': '4s48KQnjSyQ', # Muthai Tharu
    'SN7FIkL-o1k': '_6QdoqADlT0', # Muthai Tharu
    'bOxyDZgsI2c': 'XzTh3n_VGnY', # Rathinagiri
    'C9Ea0-FfMNs': 'CWh0TXSSACQ', # Naatha Vindhugal
    'eEYBleNgRGU': 'Gdv9p4cl7TE', # Naal En Seyyum
    'ZZKjQ1SD_mQ': 'T4CBo5OOQ1c', # Naal En Seyyum
    'MTvDDAQCFmk': 'Kj7ImPyZ3_4', # Naal En Seyyum
}

print(f"Applying corrections for {len(targets)} videos...")
for tid, yid in targets.items():
    if tid not in metadata: continue
    new_desc = metadata[tid]['description']
    try:
        r = yt.videos().list(part='snippet', id=yid).execute()
        if not r.get('items'): continue
        snippet = r['items'][0]['snippet']
        body = {
            'id': yid,
            'snippet': {k: snippet[k] for k in ('title', 'categoryId', 'tags', 'defaultLanguage', 'defaultAudioLanguage') if k in snippet}
        }
        body['snippet']['description'] = new_desc
        yt.videos().update(part='snippet', body=body).execute()
        print(f"SUCCESS: Updated YouTube description for {yid} ({tid})")
    except Exception as e:
        print(f"FAILED to update {yid}: {e}")
