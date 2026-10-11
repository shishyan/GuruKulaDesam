import sys, json, os, pathlib
sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path('.')
OUT_DIR = ROOT / 'production' / 'subtitles'
OUT_DIR.mkdir(parents=True, exist_ok=True)

with open(ROOT / 'assets/data/catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

with open(ROOT / 'production/youtube_lyrics_overrides.json', 'r', encoding='utf-8') as f:
    ovr = json.load(f)

with open(ROOT / 'production/youtube_backup/videos.json', 'r', encoding='utf-8') as f:
    vids = {v['id']: v for v in json.load(f)}

works = ovr.get('_works', {})

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def generate_srt(lyrics, total_duration=240.0):
    lines = [l.strip() for l in lyrics.split('\n') if l.strip()]
    if not lines:
        return ""
    
    # Break into clean couplets or stanzas
    chunks = []
    chunk_size = 2 if len(lines) > 8 else 1
    for i in range(0, len(lines), chunk_size):
        chunks.append("\n".join(lines[i:i+chunk_size]))
    
    time_per_chunk = total_duration / len(chunks)
    srt_entries = []
    for idx, text in enumerate(chunks, 1):
        start_t = (idx - 1) * time_per_chunk
        end_t = min(idx * time_per_chunk, total_duration)
        srt_entries.append(f"{idx}\n{format_time(start_t)} --> {format_time(end_t)}\n{text}\n")
    
    return "\n".join(srt_entries)

# Build subtitles for every video on the channel
generated = 0
for vid, vdata in vids.items():
    # 1. Check override first
    lyrics = None
    if vid in ovr:
        ref = ovr[vid]['ref']
        if ref in works:
            lyrics = works[ref].get('lyrics')
    
    # 2. Check catalog
    if not lyrics:
        for vault, songs in cat.items():
            if not isinstance(songs, list): continue
            for s in songs:
                if s.get('id') == vid:
                    l = (s.get('lyrics') or '').strip()
                    if len(l) > 30:
                        lyrics = l
                    break
            if lyrics: break
            
    if lyrics:
        # Estimate duration or default to 210s
        srt_content = generate_srt(lyrics, total_duration=210.0)
        srt_path = OUT_DIR / f"{vid}.srt"
        srt_path.write_text(srt_content, encoding='utf-8')
        generated += 1

print(f"Generated {generated} subtitle files in production/subtitles/")
