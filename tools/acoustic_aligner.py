"""
Acoustic Subtitle Aligner
Matches Whisper acoustic segments with canonical Tamil lyrics/kurals
and outputs professional, synchronized SubRip (.srt) subtitle tracks.
"""

import json
import re
import difflib

def format_timestamp(seconds: float) -> str:
    """Format seconds into SRT timestamp HH:MM:SS,mmm"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis >= 1000:
        secs += 1
        millis -= 1000
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

def clean_tamil_text(text: str) -> str:
    """Strip punctuation and whitespace for phonetic/fuzzy comparison"""
    text = re.sub(r'[^\u0B80-\u0BFF\s]', '', text)
    return ' '.join(text.split())

def align_segments_to_kurals(whisper_segments, kurals):
    """
    whisper_segments: list of {'start': float, 'end': float, 'text': str}
    kurals: dict mapping kural_num -> {'Number': int, 'Line1': str, 'Line2': str}
    """
    aligned_blocks = []
    
    # Pre-clean kural lines
    kural_keywords = {}
    for num, k in kurals.items():
        full = clean_tamil_text(k['Line1'] + ' ' + k['Line2'])
        words = full.split()
        kural_keywords[num] = {
            'first_words': words[:3],
            'full': full,
            'kural': k
        }
    
    # Process each acoustic segment
    for seg in whisper_segments:
        seg_text = clean_tamil_text(seg['text'])
        if not seg_text or len(seg_text) < 3:
            continue
            
        best_num = None
        best_ratio = 0.0
        
        for num, data in kural_keywords.items():
            # Check ratio
            matcher = difflib.SequenceMatcher(None, seg_text, data['full'])
            ratio = matcher.ratio()
            # Also check if any prominent keyword is in seg_text
            for kw in data['first_words']:
                if len(kw) >= 3 and kw in seg_text:
                    ratio += 0.3
            if ratio > best_ratio:
                best_ratio = ratio
                best_num = num
                
        # Require a minimal confidence threshold
        if best_ratio > 0.25 and best_num is not None:
            k = kurals[best_num]
            aligned_blocks.append({
                'start': seg['start'],
                'end': seg['end'],
                'kural_number': best_num,
                'text': f"{k['Line1']}\n{k['Line2']}",
                'acoustic_transcription': seg['text'],
                'confidence': best_ratio
            })
            
    return aligned_blocks

def export_srt(blocks, out_srt_path):
    """Write blocks to valid SRT file"""
    lines = []
    for idx, b in enumerate(blocks, 1):
        s_str = format_timestamp(b['start'])
        e_str = format_timestamp(b['end'])
        lines.append(f"{idx}\n{s_str} --> {e_str}\n{b['text']}\n")
        
    content = "\n".join(lines).strip() + "\n"
    with open(out_srt_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[SRT] Exported {len(blocks)} blocks to {out_srt_path}")
    return content
