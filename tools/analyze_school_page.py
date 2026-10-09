import re, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('school.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in school.html: {len(lines)}")

current_comment = ""
for idx, line in enumerate(lines):
    line_s = line.strip()
    if line_s.startswith("<!--") and ("SECTION" in line_s or "HERO" in line_s or "STAGE" in line_s or "===" in line_s or "1." in line_s or "2." in line_s or "3." in line_s or "4." in line_s):
        print(f"Line {idx+1}: {line_s}")
    elif line_s.startswith("<section"):
        print(f"Line {idx+1}: {line_s[:100]}")
