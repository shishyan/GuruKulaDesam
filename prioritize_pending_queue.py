"""
Prioritize latest uploaded videos on the channel at the very front of the pending queue.
"""

import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from update_youtube_channel_titles import get_authenticated_service

youtube = get_authenticated_service()

ch_resp = youtube.channels().list(part="contentDetails", mine=True).execute()
uploads_pl = ch_resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

all_ch_vids = []
next_token = None
while True:
    pl_resp = youtube.playlistItems().list(part="snippet", playlistId=uploads_pl, maxResults=50, pageToken=next_token).execute()
    for item in pl_resp["items"]:
        all_ch_vids.append(item["snippet"]["resourceId"]["videoId"])
    next_token = pl_resp.get("nextPageToken")
    if not next_token:
        break

print(f"Total uploads in channel: {len(all_ch_vids)}")

with open("channel_direct_uploads_pending.json", "r", encoding="utf-8") as f:
    pending = json.load(f)

pending_by_id = {u["video_id"]: u for u in pending}

ordered = []
seen = set()
for vid in all_ch_vids:
    if vid in pending_by_id and vid not in seen:
        ordered.append(pending_by_id[vid])
        seen.add(vid)

for u in pending:
    if u["video_id"] not in seen:
        ordered.append(u)
        seen.add(u["video_id"])

with open("channel_direct_uploads_pending.json", "w", encoding="utf-8") as f:
    json.dump(ordered, f, ensure_ascii=False, indent=2)

print(f"Reordered {len(ordered)} tracks. Top 10 queued for live update:")
for i, u in enumerate(ordered[:10], 1):
    print(f"[{i:02d}] {u['video_id']} : {u['new_title']}")
