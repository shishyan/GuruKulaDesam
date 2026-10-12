import urllib.request
import json

req = urllib.request.Request(
    'https://api.github.com/repos/shishyan/Gurukuladesam/actions/runs/37547632992/jobs',
    headers={'User-Agent': 'Mozilla/5.0'}
)

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    job = data['jobs'][0]
    print(json.dumps(job['steps'], indent=2))
