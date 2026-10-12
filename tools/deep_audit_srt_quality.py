import os, sys, glob, json, pathlib

sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path('.')
SRT_DIR = ROOT / 'production' / 'subtitles'
srts = sorted(list(SRT_DIR.glob('*.srt')))
print(f"Total SRT files in production/subtitles: {len(srts)}")

# Load videos backup to correlate with titles and durations
vids = json.load(open('production/youtube_backup/videos.json', encoding='utf-8'))
vid_map = {v['id']: v for v in vids}

results = []

def parse_time(t_str):
    parts = t_str.strip().replace(',', '.').split(':')
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    return 0.0

for srt_path in srts:
    vid = srt_path.stem
    content = srt_path.read_text(encoding='utf-8', errors='ignore').strip()
    
    blocks = [b.strip() for b in content.split('\n\n') if b.strip()]
    num_blocks = len(blocks)
    
    max_block_dur = 0.0
    total_covered_dur = 0.0
    all_lines = []
    
    for b in blocks:
        lines = b.split('\n')
        if len(lines) >= 3 and '-->' in lines[1]:
            try:
                t1_str, t2_str = lines[1].split('-->')
                t1 = parse_time(t1_str)
                t2 = parse_time(t2_str)
                dur = t2 - t1
                if dur > max_block_dur:
                    max_block_dur = dur
                total_covered_dur = max(total_covered_dur, t2)
                text = " ".join(lines[2:])
                all_lines.append(text)
            except Exception:
                pass
                
    meta = vid_map.get(vid, {})
    title = meta.get('snippet', {}).get('title', 'Unknown')
    is_thirukkural = 'திருக்குறள்' in title or 'Thirukkural' in title
    
    # Flags:
    # 1. Thirukkural must have 10 blocks (or 20 lines)
    # 2. Block duration > 25 seconds is suspicious
    # 3. Very few blocks (< 4) for any full song
    issues = []
    if is_thirukkural and num_blocks < 10:
        issues.append(f"Thirukkural has only {num_blocks} blocks (expected 10 kurals)")
    if max_block_dur > 25.0:
        issues.append(f"Max block duration is {max_block_dur:.1f}s (stretched timing)")
    if num_blocks <= 2:
        issues.append(f"Severely truncated ({num_blocks} blocks)")
        
    results.append({
        'vid': vid,
        'title': title,
        'is_thirukkural': is_thirukkural,
        'blocks': num_blocks,
        'max_block_dur': round(max_block_dur, 1),
        'total_srt_dur': round(total_covered_dur, 1),
        'issues': issues,
        'path': str(srt_path)
    })

problem_files = [r for r in results if r['issues']]
print(f"\nAudited {len(results)} SRT files. Found {len(problem_files)} problematic files:\n")

for p in problem_files:
    print(f"[{p['vid']}] {p['title'][:60]}")
    print(f"   Blocks: {p['blocks']} | Max block dur: {p['max_block_dur']}s | Total SRT: {p['total_srt_dur']}s")
    for iss in p['issues']:
        print(f"   -> ISSUE: {iss}")
    print()

# Save report
out_path = ROOT / 'production' / 'srt_timing_issues_report.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump({'total_audited': len(results), 'problems_count': len(problem_files), 'problems': problem_files, 'all': results}, f, indent=2, ensure_ascii=False)
print(f"Full report saved to {out_path}")
