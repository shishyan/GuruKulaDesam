import sys
import json

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/youtube_backup/videos.json', encoding='utf-8') as f:
    videos = json.load(f)

v_by_id = {v['id']: v for v in videos}

sample_ids = [
    'ssOkftpUcLE', # Hare Krishna in Murugan video
    'uPk4dyag74Y', # Gana Natha in Thigada
    '_eG3rWRIvJo', # Gana Natha in Thigada
    'udRsA-oWxS0', # Truncated Pancharatnam
    'TlaBaW3-ckI', # Thiruvarutpa
    'poRjt6i3SrU', # Natarajar Pathu
    '-yEq62Bu_d8', # Thiruvasagam
    'grjVzzo-RWc', # Samayapuram Mariamman (0 chars)
    'wehcVz3BMHo', # Samayapuram Mariamman (0 chars)
    'Q5G2h9GuGQs', # Raghupati Raghava (32 chars)
    'W2peLbC20sA', # Siva Subramaniyar (32 chars)
]

for vid in sample_ids:
    v = v_by_id.get(vid)
    if v:
        print("="*70)
        print(f"ID: {vid} | Title: {v['snippet']['title']}")
        print(f"Desc length: {len(v['snippet']['description'])}")
        print(f"Description:\n{v['snippet']['description']}")
