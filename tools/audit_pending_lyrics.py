import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    vids = json.load(f)

with open('production/youtube_backup/apply_log.jsonl', 'r', encoding='utf-8') as f:
    applied = set()
    for l in f:
        r = json.loads(l)
        if r.get('ok') and not r.get('rollback'):
            applied.add(r['id'])

total = len(vids)
with_lyrics_desc = 0
only_short_blurb = 0

for v in vids:
    vid = v['id']
    d = v['snippet'].get('description', '')
    if 'பாடல் வரிகள்' in d or 'Lyrics' in d:
        with_lyrics_desc += 1
    else:
        only_short_blurb += 1

print(f"Total videos on channel: {total}")
print(f"Videos updated with lyrics & meaning: {with_lyrics_desc}")
print(f"Videos still having ONLY short blurb / NO lyrics: {only_short_blurb}")
print(f"Videos updated via apply script before quota hit: {len(applied)}")
