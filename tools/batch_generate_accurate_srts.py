# -*- coding: utf-8 -*-
import glob, re, os, sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

builders = glob.glob('tools/build_accurate_*.py')
print(f"Total accurate builders: {len(builders)}")

count = 0
for b in sorted(builders):
    with open(b, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Check if cues defined
    if 'cues = [' in code:
        cut = code.split('def main():')[0]
        loc = {}
        try:
            exec(cut, {}, loc)
            cues = loc.get('cues', [])
            to_srt_time = loc.get('to_srt_time')
            
            m = re.search(r'production/subtitles/([^\'"\s]+\.srt)', code)
            if m and cues and to_srt_time:
                srt_name = m.group(1)
                srt_path = os.path.join('production/subtitles', srt_name)
                with open(srt_path, 'w', encoding='utf-8') as out_f:
                    for idx, item in enumerate(cues, 1):
                        out_f.write(f"{idx}\n")
                        out_f.write(f"{to_srt_time(item['start'])} --> {to_srt_time(item['end'])}\n")
                        out_f.write(f"{item['text']}\n\n")
                print(f"  ✅ Generated {srt_name} ({len(cues)} cues) from {os.path.basename(b)}")
                count += 1
        except Exception as e:
            print(f"  ⚠️ Error parsing {b}: {e}")

print(f"Total verified accurate SRT files written: {count}")
