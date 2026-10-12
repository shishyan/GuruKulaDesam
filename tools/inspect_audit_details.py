import sys
import json

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/all_flawed_descriptions_audit.json', 'r', encoding='utf-8') as f:
    audit = json.load(f)

for item in audit:
    vid = item.get('id')
    if vid in ["jZFTlpJwn6A", "FGeahfpAbiw", "_eG3rWRIvJo", "udRsA-oWxS0", "iXHNzqOrxzw", "qPjurMK6xpI", "mPypwIgdo-E", "g42Pg2sg_gg", "rRoJfeRQiaM", "nGBmGzsD-kM"]:
        print(f"\n=================== {vid}: {item.get('title')} ===================")
        print("Mismatches/Issues:", item.get('issues'))
        print("Description snippet:\n", item.get('description', '')[:350])
