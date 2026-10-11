import sys, json, os, pathlib, re
sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path('.')
OUT_DIR = ROOT / 'production' / 'subtitles'
OUT_DIR.mkdir(parents=True, exist_ok=True)

with open(ROOT / 'assets/data/catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

with open(ROOT / 'production/youtube_lyrics_overrides.json', 'r', encoding='utf-8') as f:
    ovr = json.load(f)

works = ovr.get('_works', {})

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def generate_srt(lyrics, total_duration=210.0):
    lines = [l.strip() for l in lyrics.split('\n') if l.strip()]
    if not lines:
        return ""
    
    # Clean out formatting artifacts if any
    clean_lines = []
    for l in lines:
        if l.startswith('═') or l.startswith('---'): continue
        clean_lines.append(l)
    
    if not clean_lines:
        return ""

    chunks = []
    chunk_size = 2 if len(clean_lines) > 6 else 1
    for i in range(0, len(clean_lines), chunk_size):
        chunks.append("\n".join(clean_lines[i:i+chunk_size]))
    
    time_per_chunk = total_duration / len(chunks)
    srt_entries = []
    for idx, text in enumerate(chunks, 1):
        start_t = (idx - 1) * time_per_chunk
        end_t = min(idx * time_per_chunk, total_duration)
        srt_entries.append(f"{idx}\n{format_time(start_t)} --> {format_time(end_t)}\n{text}\n")
    
    return "\n".join(srt_entries)

# Process every song across all vaults in catalog.json
all_songs = {}
for vault, songs in cat.items():
    if not isinstance(songs, list): continue
    for s in songs:
        sid = s.get('id')
        if not sid: continue
        all_songs[sid] = (vault, s)

print(f"Total unique song IDs in catalog.json: {len(all_songs)}")

generated = 0
skipped = 0
for sid, (vault, s) in all_songs.items():
    lyrics = None
    
    # 1. Overrides take precedence
    if sid in ovr:
        ref = ovr[sid].get('ref')
        if ref and ref in works:
            lyrics = works[ref].get('lyrics')
            
    # 2. Catalog lyrics
    if not lyrics:
        l = (s.get('lyrics') or '').strip()
        if len(l) > 15:
            lyrics = l
            
    if lyrics:
        srt_content = generate_srt(lyrics, total_duration=210.0)
        if srt_content:
            (OUT_DIR / f"{sid}.srt").write_text(srt_content, encoding='utf-8')
            generated += 1
        else:
            skipped += 1
    else:
        skipped += 1

print(f"DONE! Generated {generated} SRT subtitle files in {OUT_DIR}")
print(f"Skipped {skipped} songs (no lyrics available)")
