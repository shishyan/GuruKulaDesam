import sys, os, json, pathlib, re

sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent
SUB_DIR = ROOT / 'production' / 'subtitles'
SUB_DIR.mkdir(parents=True, exist_ok=True)

audit = json.load(open(ROOT / 'production' / 'public_videos_lyrics_srt_audit.json', encoding='utf-8'))
missing_srts = audit['missing_local_srt']

vids = {v['id']: v for v in json.load(open(ROOT / 'production' / 'youtube_backup' / 'videos.json', encoding='utf-8'))}
full_audit = {v['id']: v for v in json.load(open(ROOT / 'production' / 'channel_all_videos_full_audit.json', encoding='utf-8'))}

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def extract_lyrics_from_desc(desc):
    # Try finding 📜 பாடல் வரிகள்
    if '📜 பாடல் வரிகள்' in desc:
        parts = re.split(r'📜\s*பாடல் வரிகள்.*?═════════════════════════════════════════════════════════════════', desc, flags=re.DOTALL)
        if len(parts) >= 2:
            body = parts[1].split('═════════════════════════════════════════════════════════════════')[0]
            return body.strip()
    # Try finding பாடல் வரிகள்:
    if 'பாடல் வரிகள்' in desc:
        parts = desc.split('பாடல் வரிகள்')
        if len(parts) >= 2:
            body = parts[1].split('══════════')[0].split('பொருள்')[0].split('— குரு குல')[0]
            return body.strip(' :\n\r\t')
    # Try finding குறள்
    if 'குறள் ' in desc:
        kurals = []
        for line in desc.split('\n'):
            line = line.strip()
            if line.startswith('குறள் ') or line.startswith('பொருள்:') or line.startswith('விளக்கம்:'):
                continue
            if len(line) > 10 and not line.startswith('═') and not line.startswith('#'):
                kurals.append(line)
        if kurals:
            return "\n".join(kurals)
    return ""

def generate_srt(lyrics, total_dur):
    lines = [l.strip() for l in lyrics.split('\n') if l.strip()]
    clean = [l for l in lines if not l.startswith('═') and not l.startswith('---') and not l.startswith('#')]
    if not clean:
        return ""
    
    # 2 lines per subtitle chunk
    chunks = []
    chunk_size = 2 if len(clean) > 4 else 1
    for i in range(0, len(clean), chunk_size):
        chunks.append("\n".join(clean[i:i+chunk_size]))
        
    time_per_chunk = total_dur / len(chunks)
    srt_entries = []
    for idx, text in enumerate(chunks, 1):
        start_t = (idx - 1) * time_per_chunk
        end_t = min(idx * time_per_chunk, total_dur)
        srt_entries.append(f"{idx}\n{format_time(start_t)} --> {format_time(end_t)}\n{text}\n")
    return "\n".join(srt_entries)

generated_count = 0

for item in missing_srts:
    vid = item['id']
    title = item['title']
    v_data = vids.get(vid, {})
    desc = v_data.get('snippet', {}).get('description', '')
    
    dur = full_audit.get(vid, {}).get('duration_sec', 240)
    if dur <= 0:
        dur = 240
        
    lyrics = extract_lyrics_from_desc(desc)
    if not lyrics or len(lyrics) < 20:
        # Check canonical data
        from enrich_9_descriptions_with_lyrics_and_meaning import CANONICAL_DATA
        if vid in CANONICAL_DATA:
            lyrics = CANONICAL_DATA[vid]['lyrics']
            
    if lyrics:
        srt_content = generate_srt(lyrics, dur)
        if srt_content:
            target_path = SUB_DIR / f"{vid}.srt"
            target_path.write_text(srt_content, encoding='utf-8')
            generated_count += 1
            print(f"Generated SRT for {vid}: {title[:40]} ({len(lyrics)} chars lyrics, {dur}s)")
        else:
            print(f"Could not format SRT for {vid}")
    else:
        print(f"Warning: No lyrics found for {vid}: {title[:40]}")

print(f"\nGenerated {generated_count} / {len(missing_srts)} missing SRT files!")
