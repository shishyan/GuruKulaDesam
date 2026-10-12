import json
import sys

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

transcript_path = r"C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\.system_generated\logs\transcript.jsonl"

with open(transcript_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print(f"Total steps in transcript: {len(lines)}")

quota_events = []
for idx, line in enumerate(lines):
    try:
        obj = json.loads(line)
        content = obj.get('content', '') or ''
        source = obj.get('source', '')
        type_ = obj.get('type', '')
        if 'quota' in content.lower() or 'resume' in content.lower():
            if type_ == 'USER_INPUT' or 'quotaExceeded' in content or 'reset' in content.lower():
                quota_events.append((idx, source, type_, content[:200]))
    except:
        pass

print(f"Found {len(quota_events)} quota events. Last 10:")
for q in quota_events[-10:]:
    print(f"Step {q[0]} [{q[1]} - {q[2]}]: {q[3]}")
