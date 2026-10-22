import urllib.request, urllib.parse, json, sys
sys.stdout.reconfigure(encoding='utf-8')

keywords = [
    'கந்த புராணம் நாவலர்',
    'பெரியபுராணம் நாவலர்',
    'திருவிளையாடல் நாவலர்',
    'சிவபுராணம் நாவலர்',
    'சேதுபுராணம்',
    'விநாயக புராணம்',
    'மகாபாரதம் நாவலர்',
    'இராமாயணம் நாவலர்',
    'காசிகாண்டம் நாவலர்',
    'வித்தியாநுபாலன',
    'யாழ்ப்பாணம் கந்தபுராணம்',
    'யாழ்ப்பாணம் பெரியபுராணம்',
    'சுவாமி விபுலானந்தர்',
    'யாழ்ப்பாணம் வித்துவான்'
]

for kw in keywords:
    q = urllib.parse.quote(kw)
    url = f'http://noolaham.org/wiki/api.php?action=query&list=search&srsearch={q}&srlimit=5&format=json'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
        results = data.get('query', {}).get('search', [])
        print(f"=== Keyword: {kw} ({len(results)} found) ===")
        for r in results:
            print("  - " + r["title"])
    except Exception as e:
        print(f"Error for {kw}:", e)
