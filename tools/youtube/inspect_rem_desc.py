import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    live_meta = json.load(f)

vids_to_check = ["nGBmGzsD-kM", "kshlDPh2IqE", "MlaG3Z3_Kck", "dbdp19C0j3M", "kyiaup-gjMc", "juuVtFBK3X8"]

for vid in vids_to_check:
    data = live_meta.get(vid, {})
    title = data.get('title', '')
    desc = data.get('description', '')
    first_few_lines = '\n'.join([line for line in desc.splitlines() if line.strip()][:4])
    print(f"\n========================================================")
    print(f"[{vid}] Title: {title}")
    print(f"Description snippet:\n{first_few_lines}")
