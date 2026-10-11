import sys, json, os, pathlib
sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path('.')
OUT = ROOT / 'production' / 'subtitles'
OUT.mkdir(parents=True, exist_ok=True)

with open(ROOT / 'assets/data/catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

with open(ROOT / 'production/youtube_lyrics_overrides.json', 'r', encoding='utf-8') as f:
    overrides = json.load(f)

works = overrides['_works']

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
    
    # Group into chunks of 2-3 lines
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

# Sample test for Muthai Tharu
w = works['muthaitharu']
sample_srt = generate_srt(w['lyrics'], 205.0)
(OUT / 'muthaitharu.srt').write_text(sample_srt, encoding='utf-8')
print("Sample SRT generated successfully! Lines count:", len(sample_srt.splitlines()))
print("\nFirst 3 entries:")
print("\n".join(sample_srt.splitlines()[:15]))
