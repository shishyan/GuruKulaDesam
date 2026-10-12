import urllib.request
import json

req = urllib.request.Request(
    'https://api.github.com/repos/shishyan/Gurukuladesam/pages',
    headers={'User-Agent': 'Mozilla/5.0'}
)

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print("GitHub Pages Config:")
        print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error fetching pages config: {e}")
