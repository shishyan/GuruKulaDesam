import glob, json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('production/owned_guru_kula_videos.json', 'r', encoding='utf-8') as f:
    owned_dict = dict(json.load(f)['owned'])

suno_tracks = []
for p in glob.glob('production/suno_meta/*.json'):
    try:
        with open(p, 'r', encoding='utf-8') as f:
            suno_tracks.append(json.load(f))
    except:
        pass

bad_ids = [
    '8AEEcskF-Jo', 'D95woYqPoPI', '9kHN9Dzrv7o', 'XN5ENUbmSOE', 'oEQ3sx6ujQc', 'Nb1nAcrGNeU',
    'CEh2a8KUIKU', 'lCBVB2Yj_7U', 'wylRNpaJNmY', 'rOowxP53oWA', 'hCHBPd8BH8A', 'gjo0AfKBzsU',
    'KLsXZa28uyE', 'JvonvWQHKQY', '_Q2t-TcmDT4', 'djYooU1LmGk', 'mv7AezrLzoU', 'VVkl8bORJXg',
    '0WurYH-hkNM', '3yB_oTqh6Jk', 'dVYI3ZgpDC8', 'wzdoeFDq0iQ', 'W4LQ0TT2cRA', 'irx33IVWrPY',
    'jdvz-yoK5eI', 'xcUlgFsrepU', 'HRN77i6Kio8', 'tzAYLpH3TkI', 'xVyPWHTMXHw', 'x3CyxNH5bpQ',
    'VENn3ip3XPA', 'dBIUA3fKBJ0', 'SWAjAbur-TQ', 'QXWB2raWKXE', 'wyDIU74Rs7Y', 'B60TIM5LLvY',
    'nR7R0TWyZHk', 'fRNAsDZr3QA', 'wPT_1jgn2Ys', 'mCwNR1Bytj4', 'q6Rg5CUbOD0', '817Wxel4F5s',
    'Gnu-TzZfe7A', 'zj4_pEqa_cs'
]

def extract_kw(title):
    m = re.search(r'அதிகாரம்\s*\d+\s*[-–:]\s*([^\s|]+)', title)
    if m:
        return m.group(1).strip()
    for w in ['கந்தசஷ்டி', 'திருப்பாவை', 'திருப்புகழ்', 'விநாயகர்', 'அம்பாள்', 'முருகன்', 'சிவ', 'பெருமாள்', 'கண்ணன்']:
        if w in title:
            return w
    return None

results = []
for b in bad_ids:
    title = owned_dict.get(b, '')
    kw = extract_kw(title)
    matches = [s for s in suno_tracks if kw and kw in s.get('title', '')]
    results.append({
        'video_id': b,
        'youtube_title': title,
        'keyword': kw,
        'matches_count': len(matches),
        'best_suno_id': matches[0].get('id') if matches else None,
        'best_suno_title': matches[0].get('title') if matches else None
    })

with open('production/metadata/bad_srts_matched_batch2.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

matched_count = sum(1 for r in results if r['matches_count'] > 0)
print(f'Successfully mapped {matched_count} / {len(bad_ids)} remaining targets to Suno tracks!')
for r in results[:15]:
    print(r['video_id'], '|', r['keyword'], '|', r['best_suno_title'])
