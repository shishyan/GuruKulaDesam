import json
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('all_uploads.json', 'r', encoding='utf-8') as f:
    uploads = json.load(f)

print(f"Total uploads: {len(uploads)}")

# Check for anomalies:
# 1. Draft / QC marks
# 2. Trailing punctuation like ! or .m
# 3. Missing English transliteration (no pipe '|')
# 4. Thirukkural tracks missing 'அதிகாரம் <num> - '
# 5. English-only titles without Tamil
# 6. Title length > 95 chars (YouTube limit is 100)

issues = []
for v in uploads:
    vid = v['video_id']
    t = v['title']
    reasons = []

    if 'QC HOLD' in t or 'draft' in t.lower() or 'do not publish' in t.lower():
        reasons.append("Draft / QC hold marker")
    
    if t.endswith('!') or t.endswith('!.m') or t.endswith('.m'):
        reasons.append(f"Improper trailing punctuation/extension ({t[-4:]})")

    if '|' not in t:
        reasons.append("Missing English transliteration / delimiter ('|')")

    if re.search(r'^[A-Za-z0-9\s|—\-_()]+$', t):
        reasons.append("English-only title without Tamil script")

    if ('திருக்குறள்' in t or 'Kural' in t or 'அதிகாரம்' in t) and not re.search(r'அதிகாரம்\s+\d+\s*[-–]', t):
        reasons.append("Thirukkural track missing 'அதிகாரம் <எண்> - ' prefix")

    if len(t) > 95:
        reasons.append(f"Title length too long ({len(t)} chars > 95)")

    if reasons:
        issues.append({
            'video_id': vid,
            'current_title': t,
            'reasons': reasons
        })

print(f"\nUploads with issues: {len(issues)} / {len(uploads)}")
for item in issues:
    print(f"\n[{item['video_id']}] Current: '{item['current_title']}'")
    for r in item['reasons']:
        print(f"   -> {r}")
