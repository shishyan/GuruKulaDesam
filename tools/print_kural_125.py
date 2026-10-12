import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('production/thirukkural_all.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

kurals = {item['Number']: item for item in data['kural']}
for num in range(1241, 1251):
    kd = kurals[num]
    print(f"--- Kural {num} ---")
    print(kd['Line1'])
    print(kd['Line2'])
    print("Tam Mean:", kd.get('mv') or kd.get('mk') or kd.get('sp'))
    print("Eng Trans:", kd.get('translation'))
    print("Eng Mean:", kd.get('explanation'))
