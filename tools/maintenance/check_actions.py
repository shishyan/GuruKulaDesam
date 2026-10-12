import urllib.request
import json
import sys

req = urllib.request.Request(
    'https://api.github.com/repos/shishyan/Gurukuladesam/actions/runs',
    headers={'User-Agent': 'Mozilla/5.0'}
)

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print(f"Total Workflow Runs: {data.get('total_count', 0)}")
        for r in data.get('workflow_runs', [])[:5]:
            print(f"- Run ID: {r['id']}")
            print(f"  Name: {r.get('name')}")
            print(f"  Status: {r.get('status')}")
            print(f"  Conclusion: {r.get('conclusion')}")
            print(f"  Commit: {r.get('head_commit', {}).get('message', '')[:60]}")
            print(f"  URL: {r.get('html_url')}")
            print()
except Exception as e:
    print(f"Error fetching actions: {e}")
