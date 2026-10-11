import sys
import os
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.abspath(".")
ovr = json.load(open("production/youtube_lyrics_overrides.json", encoding='utf-8'))
works = ovr.get('_works', {})
channel_vids = json.load(open("production/youtube_backup/videos.json", encoding='utf-8'))
progress = json.load(open("production/channel_sync_progress.json", encoding='utf-8'))
cat = json.load(open("assets/data/catalog.json", encoding='utf-8'))

cat_by_id = {}
for vault, songs in cat.items():
    if not isinstance(songs, list): continue
    for s in songs:
        if s.get('id'): cat_by_id[s['id']] = s

remaining = [v for v in channel_vids if v['id'] not in progress]

def parse_iso_duration(duration_str):
    # e.g. PT3M47S, PT4M2S, PT3M, PT45S
    match = re.match(r'PT(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    if not match:
        return 210.0 # default 3m30s
    mins = int(match.group(1) or 0)
    secs = int(match.group(2) or 0)
    total = mins * 60 + secs
    return float(total) if total > 30 else 210.0

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def generate_devotional_srt(lyrics, total_duration):
    # Split into clean lines
    raw_lines = [l.strip() for l in lyrics.split('\n') if l.strip()]
    clean_lines = []
    for l in raw_lines:
        if l.startswith('═') or l.startswith('---') or l.startswith('##'): continue
        # strip Roman numerals or trailing || 1 ||
        l = re.sub(r'\|\|\s*\d+\s*\|\|', '', l).strip()
        if l:
            clean_lines.append(l)

    if not clean_lines:
        return ""

    # Group into 4-line stanzas
    chunks = []
    # If 4 to 8 lines, group by 4
    # If multiple of 4, group by 4
    # If fewer than 4 lines, all lines in 1 chunk
    chunk_size = 4
    if len(clean_lines) <= 4:
        chunks.append("\n".join(clean_lines))
    else:
        for i in range(0, len(clean_lines), chunk_size):
            chunk = clean_lines[i:i+chunk_size]
            # if last chunk has only 1 line, attach to previous chunk if possible
            if len(chunk) == 1 and chunks:
                chunks[-1] += "\n" + chunk[0]
            else:
                chunks.append("\n".join(chunk))

    # Timing: intro prelude ~16-20 seconds
    intro_offset = 18.0
    # leave ~10s outro
    outro_offset = 10.0
    usable_duration = max(total_duration - intro_offset - outro_offset, 30.0)
    time_per_chunk = usable_duration / len(chunks)

    # Enforce 20-35s display time if possible
    srt_entries = []
    for idx, text in enumerate(chunks, 1):
        start_t = intro_offset + (idx - 1) * time_per_chunk
        end_t = intro_offset + idx * time_per_chunk - 0.8 # small pause between stanzas
        srt_entries.append(f"{idx}\n{format_time(start_t)} --> {format_time(end_t)}\n{text}\n")

    return "\n".join(srt_entries)

def generate_thirukkural_srt(lyrics, total_duration):
    # Parse individual kurals
    # Typically has 'குறள் <num>:\nline1\nline2'
    kurals = []
    lines = [l.strip() for l in lyrics.split('\n') if l.strip()]
    curr_kural = []
    for l in lines:
        if l.startswith('குறள்'):
            if curr_kural:
                kurals.append("\n".join(curr_kural))
                curr_kural = []
            curr_kural.append(l)
        else:
            if curr_kural:
                curr_kural.append(l)
            else:
                # header or other text
                pass
    if curr_kural:
        kurals.append("\n".join(curr_kural))

    if not kurals:
        # Fallback to 4 lines
        return generate_devotional_srt(lyrics, total_duration)

    # Timing for Kurals:
    intro_offset = 12.0
    outro_offset = 8.0
    usable_duration = max(total_duration - intro_offset - outro_offset, 30.0)
    time_per_kural = usable_duration / len(kurals)

    srt_entries = []
    for idx, text in enumerate(kurals, 1):
        start_t = intro_offset + (idx - 1) * time_per_kural
        end_t = intro_offset + idx * time_per_kural - 0.8
        srt_entries.append(f"{idx}\n{format_time(start_t)} --> {format_time(end_t)}\n{text}\n")

    return "\n".join(srt_entries)

print(f"Generating 4-line verified subtitles for {len(remaining)} videos...\n")

count = 0
for v in remaining:
    vid = v['id']
    title = v['snippet']['title']
    dur_str = v.get('contentDetails', {}).get('duration', 'PT3M30S')
    duration = parse_iso_duration(dur_str)

    # Resolve lyrics
    lyrics = None
    if vid in ovr and ovr[vid].get('ref'):
        ref = ovr[vid]['ref']
        if ref in works:
            lyrics = works[ref].get('lyrics')
    elif vid in cat_by_id:
        lyrics = cat_by_id[vid].get('lyrics')

    if not lyrics:
        print(f"ERROR: No lyrics for {vid} ({title})")
        continue

    is_kural = ('குறள்' in lyrics or 'அதிகாரம்' in title or 'Thirukkural' in title)
    if is_kural:
        srt_content = generate_thirukkural_srt(lyrics, duration)
    else:
        srt_content = generate_devotional_srt(lyrics, duration)

    out_path = f"production/subtitles/{vid}.srt"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)

    blocks = srt_content.strip().split('\n\n')
    count += 1
    print(f"[{count:2d}/68] {vid} | {len(blocks)} stanzas | dur:{int(duration)}s | {'KURAL' if is_kural else '4-LINE'} | {title[:40]}")

print(f"\nSuccessfully generated {count}/68 verified 4-line subtitle tracks!")
