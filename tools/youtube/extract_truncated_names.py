import json
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    live_meta = json.load(f)

dots_vids = [
    "HRN77i6Kio8", "dthZW-Wo8IU", "2Gbhx6SwH-M", "nGBmGzsD-kM", "I-ZLmvGIiz4",
    "lAWfE9YSJME", "kshlDPh2IqE", "MlaG3Z3_Kck", "dbdp19C0j3M", "kyiaup-gjMc",
    "juuVtFBK3X8", "06ZOKy7SSvw", "YORF54ouPz0", "0TB3drCSvNc", "Z7qFXMBjnak",
    "DCJ2qoMSIBA", "hDoLscfeg5Q", "uMK4LISQFE4", "73GrCFM_v6Q", "EOkuHFSfv8c",
    "vZyHNMkm8xU", "qqpvlkv0mSY", "YycgNlQl6Go", "YxP_uh3dM18", "iPFEtwdcIxc",
    "XelTS98bLec", "4qnq1zW63hI", "7TlWCD9pa_0", "PLBuPRdKMHE", "-9bZmHzYO2g",
    "4UGFfmEpphI", "VyUqD3ZO3BU", "cVbT38ujUTQ", "8KQc368hCmg"
]

results = {}
for vid in dots_vids:
    data = live_meta.get(vid, {})
    title = data.get('title', '')
    desc = data.get('description', '')
    
    # Try to extract song name from DistroKid line: "<Song> · Guru Kula Desam"
    m = re.search(r'^(.*?)\s*·\s*Guru Kula Desam', desc, re.MULTILINE)
    distro_title = m.group(1).strip() if m else None
    
    # Or third line
    lines = [l.strip() for l in desc.splitlines() if l.strip()]
    line3 = lines[2] if len(lines) > 2 else None
    
    results[vid] = {
        'current_title': title,
        'distro_title': distro_title,
        'line3': line3
    }
    print(f"[{vid}] Current: '{title}'")
    print(f"       Distro: '{distro_title}'")
    print(f"       Line 3: '{line3}'\n")

