import sys
sys.path.insert(0, '.')
from production.publish_murugan_masters import get_authenticated_service

yt = get_authenticated_service()
req = yt.playlists().list(part='snippet,contentDetails', mine=True, maxResults=50)
res = req.execute()

items = res.get('items', [])
print(f"Total Playlists: {len(items)}")
for item in items:
    pid = item['id']
    title = item['snippet']['title']
    count = item['contentDetails']['itemCount']
    print(f"{pid} | ({count:3d} videos) | {title}")
