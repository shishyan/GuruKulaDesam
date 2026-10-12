import sys
import json

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/all_flawed_descriptions_audit.json', 'r', encoding='utf-8') as f:
    audit = json.load(f)

print("Type of audit:", type(audit))
if isinstance(audit, dict):
    print("Keys:", list(audit.keys())[:10])
elif isinstance(audit, list):
    print("Length:", len(audit))
    print("First item:", audit[0])
