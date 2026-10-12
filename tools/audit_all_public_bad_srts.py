import json, sys, pathlib

sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path('.')
vids = json.load(open(ROOT / 'production/youtube_backup/videos.json', encoding='utf-8'))
public_vids = [v for v in vids if v['status']['privacyStatus'] == 'public']

def parse_time(t_str):
    parts = t_str.strip().replace(',', '.').split(':')
    if len(parts) == 3: return int(parts[0])*3600 + int(parts[1])*60 + float(parts[2])
    elif len(parts) == 2: return int(parts[0])*60 + float(parts[1])
    return 0.0

bad_srts = []
for v in public_vids:
    vid = v['id']
    srt_p = ROOT / f'production/subtitles/{vid}.srt'
    if not srt_p.exists():
        bad_srts.append((v, 0, 0.0, 'missing SRT file'))
        continue
    content = srt_p.read_text(encoding='utf-8', errors='ignore').strip()
    blocks = [b.strip() for b in content.split('\n\n') if b.strip()]
    num_blocks = len(blocks)
    max_d = 0.0
    for b in blocks:
        lines = b.split('\n')
        if len(lines) >= 2 and '-->' in lines[1]:
            t1, t2 = lines[1].split('-->')
            d = parse_time(t2) - parse_time(t1)
            max_d = max(max_d, d)
            
    is_thiru = 'திருக்குறள்' in v['snippet']['title'] or 'Thirukkural' in v['snippet']['title']
    
    if num_blocks <= 2:
        bad_srts.append((v, num_blocks, max_d, f'severely truncated ({num_blocks} blocks)'))
    elif is_thiru and num_blocks < 10:
        bad_srts.append((v, num_blocks, max_d, f'Thirukkural only {num_blocks} kurals'))
    elif max_d > 45.0:
        bad_srts.append((v, num_blocks, max_d, f'stretched block duration ({max_d:.1f}s)'))

print(f"Total public videos: {len(public_vids)}")
print(f"Bad SRTs count: {len(bad_srts)}")
for v, blk, max_d, reason in bad_srts:
    print(f"[{v['id']}] blk={blk} max_d={max_d:.1f}s | {v['snippet']['title'][:60]} -> {reason}")

out_path = ROOT / 'production' / 'public_videos_bad_srts.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump([{'id': v['id'], 'title': v['snippet']['title'], 'blocks': blk, 'max_d': max_d, 'reason': reason} for v, blk, max_d, reason in bad_srts], f, indent=2, ensure_ascii=False)
