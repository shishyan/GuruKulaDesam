import sys
import json

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('master_all_598_songs_catalog.json', encoding='utf-8') as f:
    catalog = json.load(f)

cat_by_id = {item['video_id']: item for item in catalog}

TARGET_IDS = [
    "-L3VXkM2MTY",
    "FFXImcs5Ehw",
    "QRSRyYEacMs",
    "iJ-3SHR2MKw",
    "yPfkP_EjTyc",
    "mQpQEuXiEZ4",
    "Yvlg_8JBHL4",
    "nGBmGzsD-kM",
    "T1KiH3G5WPs",
    "pYuwzoJkhTE",
    "zqStqzcFgbM"
]

print("=== Comparing Catalog vs Live YouTube ===")
for vid in TARGET_IDS:
    cat_item = cat_by_id.get(vid)
    if cat_item:
        print(f"\nID: {vid}")
        print(f"  Catalog Title:       {cat_item.get('title')}")
        print(f"  Catalog Tamil Title: {cat_item.get('tamil_title')}")
        print(f"  Catalog Category:    {cat_item.get('category')}")
        lyrics_snip = cat_item.get('lyrics', '')[:80].replace('\n', ' ')
        print(f"  Catalog Lyrics:      {lyrics_snip}")
    else:
        print(f"\nID: {vid} NOT FOUND IN CATALOG")
