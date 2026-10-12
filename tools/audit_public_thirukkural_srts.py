import json, sys, pathlib

sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path('.')
vids = json.load(open(ROOT / 'production/youtube_backup/videos.json', encoding='utf-8'))
thiru_public = [v for v in vids if v['status']['privacyStatus'] == 'public' and ('திருக்குறள்' in v['snippet']['title'] or 'Thirukkural' in v['snippet']['title'])]

print(f"Total public Thirukkural videos: {len(thiru_public)}")

def parse_time(t_str):
    parts = t_str.strip().replace(',', '.').split(':')
    if len(parts) == 3: return int(parts[0])*3600 + int(parts[1])*60 + float(parts[2])
    elif len(parts) == 2: return int(parts[0])*60 + float(parts[1])
    return 0.0

bad_srt = []
missing_srt = []
good_srt = []

for v in thiru_public:
    vid = v['id']
    srt_p = ROOT / f'production/subtitles/{vid}.srt'
    if not srt_p.exists():
        missing_srt.append(v)
        continue
    content = srt_p.read_text(encoding='utf-8', errors='ignore').strip()
    blocks = [b.strip() for b in content.split('\n\n') if b.strip()]
    if len(blocks) < 10:
        bad_srt.append((v, len(blocks), 'fewer than 10 blocks'))
    else:
        max_d = 0.0
        for b in blocks:
            lines = b.split('\n')
            if len(lines) >= 2 and '-->' in lines[1]:
                t1, t2 = lines[1].split('-->')
                d = parse_time(t2) - parse_time(t1)
                max_d = max(max_d, d)
        if max_d > 40.0:
            bad_srt.append((v, len(blocks), f'max duration {max_d:.1f}s'))
        else:
            good_srt.append(v)

print(f"Good SRTs: {len(good_srt)}")
print(f"Missing SRTs: {len(missing_srt)}")
print(f"Bad SRTs: {len(bad_srt)}")
print("\nList of bad public Thirukkural SRTs:")
for v, blk, reason in bad_srt:
    print(f"  [{v['id']}] {v['snippet']['title']} -> {reason} ({blk} blocks)")
