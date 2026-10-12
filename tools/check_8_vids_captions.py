from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import sys, json

sys.stdout.reconfigure(encoding='utf-8')

c = Credentials.from_authorized_user_file('data/credentials/token.json')
if c.expired and c.refresh_token: c.refresh(Request())
yt = build('youtube', 'v3', credentials=c, cache_discovery=False)

en_us_vids = ['klSi7r6YhCU', 'PO4U3nRv6o0', '255aVCj3t0w', 'KjQZFlnCluU', 'JzGTK1V3dkM', 'HPP3IG7DWRc', 'cKyT1Cv7zEA', 'ETELjf0OTi4']

for vid in en_us_vids:
    r = yt.captions().list(part='snippet', videoId=vid).execute()
    items = r.get('items', [])
    print(f"Video {vid}: {len(items)} track(s)")
    for item in items:
        snip = item['snippet']
        lang = snip.get('language')
        kind = snip.get('trackKind')
        is_default = snip.get('isDefault')
        name = snip.get('name')
        print(f"   id={item['id']} lang={lang} kind={kind} isDefault={is_default} name='{name}'")
