import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    live_meta = json.load(f)

vids_to_check = [
    "2QOF2ycA4RQ", "Y0tOS_2Azxs", "nGBmGzsD-kM", "S9WQ-O0tZJI", "-bqKXZW8vFk",
    "I-ZLmvGIiz4", "lAWfE9YSJME", "kshlDPh2IqE", "MlaG3Z3_Kck", "dbdp19C0j3M",
    "kyiaup-gjMc", "juuVtFBK3X8", "06ZOKy7SSvw", "YORF54ouPz0", "0TB3drCSvNc",
    "Z7qFXMBjnak", "DCJ2qoMSIBA", "hDoLscfeg5Q", "SDPLWITWGho", "o5PVED0ZcfU",
    "qqpvlkv0mSY", "YycgNlQl6Go", "CSqgMX4LhJI", "IhE1OvdIBKs", "C9Ea0-FfMNs",
    "XqDL5bZgW9c", "XelTS98bLec", "LL77sdbmUNE"
]

for vid in vids_to_check:
    data = live_meta.get(vid, {})
    title = data.get('title', '')
    desc = data.get('description', '')
    first_few_lines = '\n'.join([line for line in desc.splitlines() if line.strip()][:3])
    print(f"\n========================================================")
    print(f"[{vid}] Title: {title}")
    print(f"Description snippet:\n{first_few_lines}")
