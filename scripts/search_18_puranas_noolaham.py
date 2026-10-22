import urllib.request, urllib.parse, json, sys
sys.stdout.reconfigure(encoding='utf-8')

puranas = [
    'விநாயக புராணம்',
    'கந்த புராணம்',
    'மகாபாரதம்',
    'பாகவதம்',
    'விஷ்ணு புராணம்',
    'சிவபுராணம்',
    'கூர்ம புராணம்',
    'லிங்க புராணம்',
    'மச்ச புராணம்',
    'மார்க்கண்டேய புராணம்',
    'பிரம்மாண்ட புராணம்',
    'அக்னி புராணம்',
    'பவிஷ்ய புராணம்',
    'வாமன புராணம்',
    'வராக புராணம்',
    'பத்ம புராணம்',
    'பிரம்ம புராணம்'
]

for p in puranas:
    q = urllib.parse.quote(p)
    url = f'http://noolaham.org/wiki/api.php?action=query&list=search&srsearch={q}&srlimit=5&format=json'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
        results = data.get('query', {}).get('search', [])
        print(f"=== {p} ({len(results)} found) ===")
        for r in results:
            print("  - " + r["title"])
    except Exception as e:
        print(f"Error for {p}:", e)
