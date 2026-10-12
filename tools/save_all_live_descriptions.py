import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('data/credentials/token_backup_guru-kula-desam.json')
yt = build('youtube', 'v3', credentials=creds)

vids = [
    "Mata6vtnrjQ", "KFtS403RfbY", "mQpQEuXiEZ4", "31xVgvxoiUA",
    "AW4cljBWy2w", "QH-xL37NmGM", "hm7_qUlTUiU"
]

res = yt.videos().list(part='snippet', id=",".join(vids)).execute()
for item in res.get('items', []):
    vid = item['id']
    desc = item['snippet']['description']
    out_p = f"production/descriptions/{vid}.txt"
    with open(out_p, "w", encoding="utf-8") as f:
        f.write(desc)
    print(f"Saved {vid}.txt ({len(desc)} characters)")
