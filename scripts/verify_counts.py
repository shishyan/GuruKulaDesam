import json

index_data = json.load(open(r'C:\GitHub\Gurukuladesam\data\puranas\puranas_index.json', encoding='utf-8'))
for b in index_data['catalog']:
    print(f"{b['id']:30}: {b['total_chapters']} chapters")
