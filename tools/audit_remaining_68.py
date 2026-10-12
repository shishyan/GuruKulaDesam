import sys
import os
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    all_vids = json.load(f)

with open('production/channel_sync_progress.json', 'r', encoding='utf-8') as f:
    synced = json.load(f)

synced_ids = set(synced.keys())
remaining = [v for v in all_vids if v['id'] not in synced_ids]

print(f"Total videos in backup: {len(all_vids)}")
print(f"Total synced so far: {len(synced_ids)}")
print(f"Remaining videos to process: {len(remaining)}\n")

def parse_srt(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().strip()
    blocks = re.split(r'\n\s*\n', content)
    stanzas = []
    for b in blocks:
        lines = [line.strip() for line in b.strip().split('\n') if line.strip()]
        if len(lines) >= 3:
            # line 0 is index, line 1 is timestamp, line 2+ is text
            time_range = lines[1]
            text_lines = lines[2:]
            stanzas.append({'time': time_range, 'lines': text_lines})
    return stanzas

one_or_two_lines = 0
four_lines = 0
missing = 0

for i, v in enumerate(remaining):
    vid = v['id']
    title = v['snippet']['title']
    srt_path = f"production/subtitles/{vid}.srt"
    stanzas = parse_srt(srt_path)
    if not stanzas:
        status = "MISSING"
        missing += 1
    else:
        avg_lines = sum(len(s['lines']) for s in stanzas) / len(stanzas)
        if avg_lines < 3.5:
            status = f"LOW_LINES ({avg_lines:.1f} lines/block, {len(stanzas)} blocks)"
            one_or_two_lines += 1
        else:
            status = f"4_LINE_OK ({len(stanzas)} blocks)"
            four_lines += 1
    print(f"{i+1:2d}. {vid} | {status:<30} | {title[:45]}")

print(f"\nSummary:")
print(f"4-line compliant: {four_lines}")
print(f"Needs 4-line reformatting: {one_or_two_lines}")
print(f"Missing SRT: {missing}")
