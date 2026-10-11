import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

audit = json.load(open('production/final_sorted_playlist_audit.json', encoding='utf-8'))
plan = json.load(open('production/thirukkural_sort_plan.json', encoding='utf-8'))

# Map videoId to chapter in plan
vid_to_chap = {item['videoId']: item['chapter'] for item in plan}

print("Audit of all 212 videos in current playlist:")
for item in audit:
    pos = item['position']
    vid = item['videoId']
    title = item['title']
    chap = vid_to_chap.get(vid, 'EXTRA')
    if pos < 20 or pos > 190 or pos % 15 == 0:
        print(f"Pos {pos:03d} | Chap {str(chap):<5} | Vid: {vid} | {title[:45]}")
