import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

creds_path = os.path.join('data', 'credentials', 'token.json')
creds = Credentials.from_authorized_user_file(creds_path)
yt = build('youtube', 'v3', credentials=creds)

targets = [
    {
        "videoId": "NK2PqzKz3aI",
        "title": "Thiru Pallaandu",
        "srt": "production/subtitles/NK2PqzKz3aI.srt",
        "lang": "ta"
    },
    {
        "videoId": "XErAOEtZdAU",
        "title": "Magaram Alaru Idai / Vel Virutham",
        "srt": "production/subtitles/XErAOEtZdAU.srt",
        "lang": "ta"
    },
    {
        "videoId": "VMqFjcQtebw",
        "title": "Magaram Alaru Idai (Remix)",
        "srt": "production/subtitles/VMqFjcQtebw.srt",
        "lang": "ta"
    }
]

for item in targets:
    vid = item["videoId"]
    srt_path = item["srt"]
    lang = item["lang"]
    print(f"\nProcessing {vid} ({item['title']})...")
    
    if not os.path.exists(srt_path):
        print(f"  ERROR: Subtitle file not found: {srt_path}")
        continue
        
    res = yt.captions().list(part="snippet", videoId=vid).execute()
    existing_captions = res.get("items", [])
    
    existing_track = None
    for c in existing_captions:
        snip = c.get("snippet", {})
        if snip.get("language") == lang and snip.get("trackKind") != "ASR":
            existing_track = c
            break
            
    media = MediaFileUpload(srt_path, mimetype="application/x-subrip", resumable=True)
    
    if existing_track:
        cap_id = existing_track["id"]
        print(f"  Found existing caption track {cap_id}. Updating with verified 4-line stanzas...")
        body = {
            "id": cap_id,
            "snippet": {
                "isDraft": False
            }
        }
        updated = yt.captions().update(
            part="snippet",
            body=body,
            media_body=media
        ).execute()
        print(f"  SUCCESS! Updated caption track {updated.get('id')}")
    else:
        print(f"  No existing custom caption track found. Inserting new track...")
        body = {
            "snippet": {
                "videoId": vid,
                "language": lang,
                "name": "Tamil",
                "isDraft": False
            }
        }
        inserted = yt.captions().insert(
            part="snippet",
            body=body,
            media_body=media
        ).execute()
        print(f"  SUCCESS! Inserted new caption track {inserted.get('id')}")

print("\nDone!")
