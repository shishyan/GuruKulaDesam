import json, sys, pathlib, re

sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent
vids = json.load(open(ROOT / 'production' / 'channel_all_videos_full_audit.json', encoding='utf-8'))
priv_log = json.load(open(ROOT / 'production' / 'privatized_duplicates_log.json', encoding='utf-8')) if (ROOT / 'production' / 'privatized_duplicates_log.json').exists() else []
priv_ids = set(d['id'] for d in priv_log if d.get('status') == 'private')

caps_audit = {}
if (ROOT / 'production' / 'caption_tracks_audit.json').exists():
    raw_caps = json.load(open(ROOT / 'production' / 'caption_tracks_audit.json', encoding='utf-8'))
    caps_audit = {c['vid']: c for c in raw_caps}

# Fetch live snippets for descriptions if needed, or check local backup
backup_vids = {v['id']: v for v in json.load(open(ROOT / 'production' / 'youtube_backup' / 'videos.json', encoding='utf-8'))}
sub_dir = ROOT / 'production' / 'subtitles'

public_vids = [v for v in vids if v['id'] not in priv_ids and v.get('privacyStatus') == 'public']

print(f"Total Public Videos: {len(public_vids)}\n")

results = []
missing_lyrics_in_desc = []
missing_meaning_in_desc = []
missing_srt_track = []
missing_local_srt = []

for v in public_vids:
    vid = v['id']
    title = v['title']
    
    # Description check
    b_snip = backup_vids.get(vid, {}).get('snippet', {})
    desc = b_snip.get('description', '')
    
    has_lyrics = ('பாடல் வரிகள்' in desc or 'Lyrics' in desc or 'குறள் ' in desc) and len(desc) > 300
    has_meaning = ('பொருள் விளக்கம்' in desc or 'பொருள்:' in desc or 'விளக்கம்:' in desc or 'Spiritual Meaning' in desc or 'Meaning' in desc)
    
    # Subtitle tracks check
    c_info = caps_audit.get(vid, {})
    all_tracks = c_info.get('all_tracks', [])
    has_tamil_standard_cc = any(t.get('languageCode') == 'ta' and t.get('kind') != 'asr' for t in all_tracks)
    has_tamil_asr = any(t.get('languageCode') == 'ta' and t.get('kind') == 'asr' for t in all_tracks)
    
    local_srt_exists = (sub_dir / f"{vid}.srt").exists()
    
    status = {
        'id': vid,
        'title': title,
        'desc_len': len(desc),
        'has_lyrics': has_lyrics,
        'has_meaning': has_meaning,
        'has_tamil_standard_cc': has_tamil_standard_cc,
        'has_tamil_asr': has_tamil_asr,
        'has_local_srt': local_srt_exists,
        'total_tracks': len(all_tracks)
    }
    results.append(status)
    
    if not has_lyrics:
        missing_lyrics_in_desc.append(status)
    if not has_meaning:
        missing_meaning_in_desc.append(status)
    if not has_tamil_standard_cc:
        missing_srt_track.append(status)
    if not local_srt_exists:
        missing_local_srt.append(status)

report = {
    'total_public_videos': len(public_vids),
    'with_complete_lyrics_desc': len(public_vids) - len(missing_lyrics_in_desc),
    'missing_lyrics_desc_count': len(missing_lyrics_in_desc),
    'with_complete_meaning_desc': len(public_vids) - len(missing_meaning_in_desc),
    'missing_meaning_desc_count': len(missing_meaning_in_desc),
    'with_tamil_standard_cc_live': len(public_vids) - len(missing_srt_track),
    'missing_tamil_standard_cc_count': len(missing_srt_track),
    'with_local_srt_file': len(public_vids) - len(missing_local_srt),
    'missing_local_srt_count': len(missing_local_srt)
}

print("=" * 60)
print("COMPREHENSIVE PUBLIC AUDIT RESULTS:")
print(f"Total Public Videos: {report['total_public_videos']}")
print(f"Videos with Lyrics in Description: {report['with_complete_lyrics_desc']} / {report['total_public_videos']}")
print(f"Videos Missing Lyrics in Description: {report['missing_lyrics_desc_count']}")
print(f"Videos with Meaning in Description: {report['with_complete_meaning_desc']} / {report['total_public_videos']}")
print(f"Videos Missing Meaning in Description: {report['missing_meaning_desc_count']}")
print(f"Videos with Live Tamil Standard CC: {report['with_tamil_standard_cc_live']} / {report['total_public_videos']}")
print(f"Videos Missing Live Tamil Standard CC: {report['missing_tamil_standard_cc_count']}")
print(f"Videos with Local SRT file ready: {report['with_local_srt_file']} / {report['total_public_videos']}")
print(f"Videos Missing Local SRT file: {report['missing_local_srt_count']}")
print("=" * 60)

with open(ROOT / 'production' / 'public_videos_lyrics_srt_audit.json', 'w', encoding='utf-8') as f:
    json.dump({
        'summary': report,
        'missing_lyrics': missing_lyrics_in_desc,
        'missing_meaning': missing_meaning_in_desc,
        'missing_standard_cc': missing_srt_track,
        'missing_local_srt': missing_local_srt,
        'all': results
    }, f, indent=2, ensure_ascii=False)
