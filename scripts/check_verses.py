import json

for name in ['ramayanam.json', 'periyapuranam.json', 'thirumandhiram.json', 'mahabharatam.json']:
    fp = rf"C:\GitHub\Gurukuladesam\data\puranas\{name}"
    with open(fp, 'r', encoding='utf-8') as f:
        d = json.load(f)
    ch = d['chapters'][0]
    print('===', name, '===')
    print('Keys:', list(ch.keys()))
    text = ch.get('exposition', '')
    print('Exposition start:', text[:120].encode('ascii', 'replace').decode('ascii'))
