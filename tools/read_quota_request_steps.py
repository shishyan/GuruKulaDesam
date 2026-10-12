import json
import sys

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

transcript_path = r"C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\.system_generated\logs\transcript.jsonl"

with open(transcript_path, 'r', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        if idx in [5592, 5593, 5594, 5595, 6986, 7000]:
            obj = json.loads(line)
            print(f"\n--- Step {idx} [{obj.get('type')}] ---")
            print(obj.get('content', '')[:500])
