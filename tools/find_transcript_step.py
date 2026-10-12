import sys

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open(r"C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\.system_generated\logs\transcript.jsonl", encoding='utf-8') as f:
    for line_num, line in enumerate(f, 1):
        if "shot_after_edit_text" in line or "test_single_done" in line:
            print(f"Line {line_num}: {line[:200]}...")
