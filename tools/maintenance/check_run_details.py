import urllib.request
import json

req = urllib.request.Request(
    'https://api.github.com/repos/shishyan/Gurukuladesam/actions/runs/37567155172/jobs',
    headers={'User-Agent': 'Mozilla/5.0'}
)

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        for job in data.get('jobs', []):
            print(f"Job: {job['name']} | Status: {job['status']} | Conclusion: {job['conclusion']}")
            for step in job.get('steps', []):
                print(f"  - Step: {step['name']} ({step.get('conclusion')})")
except Exception as e:
    print(f"Error fetching jobs: {e}")
