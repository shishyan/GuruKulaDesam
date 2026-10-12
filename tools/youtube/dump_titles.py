import json

with open('all_uploads.json', 'r', encoding='utf-8') as f:
    uploads = json.load(f)

with open('all_uploads_titles.txt', 'w', encoding='utf-8') as out:
    for i, v in enumerate(uploads):
        out.write(f"{i+1:3d}. [{v.get('video_id')}] {v.get('title')}\n")

print(f"Wrote {len(uploads)} titles to all_uploads_titles.txt")
