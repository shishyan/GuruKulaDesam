# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Audio-to-Video Production Pipeline
Builds cinematic videos from audio releases using:
1. Google Flow Prompts (locked continuity, scene timing, negative prompts)
2. Image-based fluid animation (sub-pixel zoompan ease + procedural Perlin dhoopam haze + color grade)
3. Direct FFmpeg assembly with master audio tracks
"""

import os
import re
import sys
import json
import shutil
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent
FFMPEG = Path(shutil.which('ffmpeg') or 'C:/ffmpeg/bin/ffmpeg.exe')
FFPROBE = Path(shutil.which('ffprobe') or 'C:/ffmpeg/bin/ffprobe.exe')

SOURCES_DIR = ROOT / "source" / "youtube"
VISUALS_DIR = ROOT / "production" / "visuals"
PROMPTS_DIR = ROOT / "production" / "google_flow_prompts"
RENDERS_DIR = ROOT / "renders" / "releases"

SOURCES_DIR.mkdir(parents=True, exist_ok=True)
VISUALS_DIR.mkdir(parents=True, exist_ok=True)
PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
RENDERS_DIR.mkdir(parents=True, exist_ok=True)

def sanitize_slug(text, fallback_id="track"):
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    slug = re.sub(r'[^a-zA-Z0-9_-]', '_', text)
    slug = re.sub(r'_+', '_', slug).strip('_').lower()
    return slug[:40] if len(slug) > 3 else fallback_id

def get_audio_duration(audio_file):
    cmd = [
        str(FFPROBE), "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_file)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def download_audio(video_id):
    candidates = list(SOURCES_DIR.glob(f"{video_id}.*"))
    for c in candidates:
        if c.suffix in ['.m4a', '.mp3', '.webm', '.opus'] and c.stat().st_size > 10000:
            return c
            
    import yt_dlp
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': str(SOURCES_DIR / f"{video_id}.%(ext)s"),
        'quiet': True,
        'no_warnings': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
    
    candidates = list(SOURCES_DIR.glob(f"{video_id}.*"))
    for c in candidates:
        if c.suffix in ['.m4a', '.mp3', '.webm', '.opus']:
            return c
    raise FileNotFoundError(f"Audio not found for {video_id}")

def generate_flow_prompts(item):
    """Generate structured Google Flow Director Prompts for the track"""
    ch_num = item.get('chapter_number', '')
    ch_name = item.get('chapter_name', '')
    en_name = item.get('english_name', '')
    aid = item.get('audio_id')
    theme = item.get('theme', '')
    slug = f"adhikaram_{ch_num}_{sanitize_slug(en_name, aid)}"
    
    out_dir = PROMPTS_DIR / "thirukkural"
    out_dir.mkdir(parents=True, exist_ok=True)
    prompt_file = out_dir / f"{slug}.md"
    
    content = f"""# Google Flow Cinematic Video Plan — அதிகாரம் {ch_num}: {ch_name}
**English Title:** {en_name}  
**Track ID:** `{aid}`  
**Theme:** {theme}  
**Soundtrack:** Original master recording from Guru Kula Desam (`{aid}.m4a`).  
**Visual Grammar:** Photorealistic 16:9, 24 fps, authentic ancient classical Tamil aesthetics, 8k resolution.

---

## Locked Continuity Bible
- **Setting:** Ancient Sangam Tamil landscape, Western Ghats mist, sacred river banks, pristine banyan groves, weathered granite temple architecture.
- **Lighting:** Warm early morning dawn sunlight (6:00 AM) breaking through mountain mist, golden hour backlight, bronze oil lamp flickering warmth.
- **Atmosphere:** Deep tranquility, reverence, ethical moral clarity, gentle procedural dhoopam / mountain mist haze.
- **Hard Exclusions:** No subtitles, no text on screen, no logos, no watermarks, no modern vehicles, no electric wires, no plastic, no morphing fingers/limbs, no floating objects.

---

## 10-Second Continuous Scene Prompts for Google Flow

### Scene 1 (00:00 - 00:10): The Sacred Landscape & Dawn Reveal
**Prompt:**  
Create a single continuous 16:9 cinematic photorealistic video shot at 24 fps. Wide aerial glide over majestic Western Ghats mountain ridges in ancient Tamil Nadu at predawn. Layered misty green peaks, morning clouds drifting gently across forested valleys, pristine mountain stream flowing through weathered granite boulders. Soft golden sun rays piercing through lavender mist. 8k resolution, ultra-detailed nature cinematography, calm spiritual grandeur.
*Exclusions:* No modern items, no roads, no buildings, no camera shake, no digital zoom, no text.

### Scene 2 (00:10 - 00:20): Classical Tamil Setting & Moral Allegory
**Prompt:**  
Create a single continuous 16:9 cinematic live-action video shot at 24 fps. Ground-level slow dolly forward along an ancient granite courtyard surrounded by lush tropical trees. {theme} Bronze oil lamps (kuthuvilakku) glow on stone ledges with natural flickering flames. A gentle mountain breeze sways nearby foliage, and subtle incense smoke curls toward the morning sky.
*Exclusions:* No morphing limbs, no fantasy styling, no text, no logos.

### Scene 3 (00:20 - 00:30): Timeless Ethical Awakening
**Prompt:**  
Create a single continuous 16:9 cinematic slow crane rise at 24 fps. An ancient Tamil sage / philosopher seated in peaceful contemplation on stone steps overlooking a tranquil lotus pond reflecting the morning sky. Sacred temple tower in distant mist. Deep moral serenity, profound inner peace.
*Exclusions:* No rapid motion, no modern artifacts, no text.
"""
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(content)
    return prompt_file

def render_image_based_video(image_path, audio_path, output_path, duration=None):
    """
    Renders high-grade cinematic video using:
    - 2x oversampled zoompan with cosine ease
    - High-fidelity pre-rendered procedural Perlin dhoopam smoke / atmospheric haze loop
    - Rec.709 color grading
    - Synchronized with master audio track
    """
    if duration is None:
        duration = get_audio_duration(audio_path)
    
    fps = 24
    cycle_frames = 12 * fps  # 288 frames per ease cycle
    ease = f"(0.5-0.5*cos(2*PI*mod(on,{cycle_frames})/{cycle_frames}))"
    smoke_loop = ROOT / "production" / "smoke_composite_loop.mp4"
    
    if not smoke_loop.exists():
        print("Generating smoke composite loop once...", flush=True)
        # Create base smoke and composite loop
        raw_smoke = ROOT / "production" / "smoke_loop.mp4"
        cmd_raw = [
            str(FFMPEG), "-y",
            "-f", "lavfi", "-i",
            f"perlin=s=1280x720:r={fps}:octaves=5:persistence=0.55:xscale=0.006:yscale=0.010:tscale=0.10:random_mode=seed:seed=71",
            "-t", "12", "-c:v", "libx264", "-crf", "15", "-preset", "ultrafast", str(raw_smoke)
        ]
        subprocess.run(cmd_raw, check=True)
        cmd_bake = [
            str(FFMPEG), "-y", "-i", str(raw_smoke),
            "-vf", "format=gray,scroll=v=-0.0016,gblur=sigma=22,lut='val*0.55',format=yuv420p,colorchannelmixer=rr=1.12:gg=0.96:bb=0.76",
            "-c:v", "libx264", "-crf", "15", "-preset", "ultrafast", str(smoke_loop)
        ]
        subprocess.run(cmd_bake, check=True)
    
    filter_graph = (
        f"[0:v]scale=2688:1512:force_original_aspect_ratio=increase,"
        f"crop=2688:1512,zoompan=z='1+0.035*{ease}':"
        f"x='iw/2-iw/zoom/2+18*{ease}':"
        f"y='ih/2-ih/zoom/2-10*{ease}':d=1:s=1920x1080:fps={fps},"
        "scale=1280:720:flags=lanczos,format=yuv420p[base];"
        "[1:v]format=yuv420p[smoke];"
        "[base][smoke]blend=all_mode=screen:all_opacity=0.10,"
        "eq=saturation=0.98:contrast=1.02,format=yuv420p[out]"
    )
    
    cmd = [
        str(FFMPEG), "-y",
        "-loop", "1", "-framerate", str(fps), "-t", str(duration), "-i", str(image_path),
        "-stream_loop", "-1", "-i", str(smoke_loop),
        "-i", str(audio_path),
        "-filter_complex", filter_graph,
        "-map", "[out]", "-map", "2:a",
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-r", str(fps), "-movflags", "+faststart", "-shortest",
        str(output_path)
    ]
    
    print(f"Executing video render -> {output_path.name} (Duration: {duration:.1f}s)...", flush=True)
    subprocess.run(cmd, check=True)
    print(f"Render complete: {output_path} ({output_path.stat().st_size / (1024*1024):.2f} MB)", flush=True)
    return output_path

def build_all_missing_videos():
    manifest_file = ROOT / "audios_without_video_manifest.json"
    with open(manifest_file, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    visual_map = {
        26: ROOT / "production/visuals/thirukkural/26-pulaal-unnaamai/01-pulaal-unnaamai.jpg",
        27: ROOT / "production/visuals/thirukkural/27-thavam/01-thavam.jpg",
        52: ROOT / "production/visuals/thirukkural/52-therinthu-vinaiyaadal/01-therinthu-vinaiyaadal.jpg",
        54: ROOT / "production/visuals/thirukkural/54-pochchaavaamai/01-pochchaavaamai.jpg",
        57: ROOT / "production/visuals/thirukkural/57-veruvantha-seyyaamai/01-veruvantha-seyyaamai.jpg",
        61: ROOT / "production/visuals/thirukkural/61-madiyinmai/01-madiyinmai.jpg",
    }
    
    results = []
    for item in manifest:
        ch = item['chapter_number']
        en = sanitize_slug(item['english_name'])
        aid = item['audio_id']
        audio_file = SOURCES_DIR / f"{aid}.m4a"
        if not audio_file.exists():
            print(f"Audio not found for ch {ch}: {audio_file}, downloading...", flush=True)
            audio_file = download_audio(aid)
            
        image_file = visual_map.get(ch)
        if not image_file or not image_file.exists():
            print(f"Visual not found for ch {ch}: {image_file}, skipping...", flush=True)
            continue
            
        out_video = RENDERS_DIR / f"adhikaram_{ch}_{en}_cinematic.mp4"
        print(f"\n=======================================================", flush=True)
        print(f"Processing Chapter {ch}: {item['chapter_name']} ({en})", flush=True)
        print(f"Image: {image_file}", flush=True)
        print(f"Audio: {audio_file}", flush=True)
        print(f"Output: {out_video}", flush=True)
        print(f"=======================================================", flush=True)
        
        # Ensure Flow prompt is generated
        prompt_path = generate_flow_prompts(item)
        print(f"Flow Prompt: {prompt_path.name}", flush=True)
        
        # Render Video
        render_image_based_video(image_file, audio_file, out_video)
        results.append({
            "chapter": ch,
            "title": item['chapter_name'],
            "english_title": item['english_name'],
            "video_path": str(out_video),
            "size_mb": round(out_video.stat().st_size / (1024*1024), 2)
        })
        
    print("\n\nAll releases processed successfully!")
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        target_ch = int(sys.argv[1])
        manifest_file = ROOT / "audios_without_video_manifest.json"
        with open(manifest_file, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        for item in manifest:
            if item['chapter_number'] == target_ch:
                ch = item['chapter_number']
                en = sanitize_slug(item['english_name'])
                aid = item['audio_id']
                audio_file = SOURCES_DIR / f"{aid}.m4a"
                image_file = ROOT / f"production/visuals/thirukkural/{ch}-{en.split('_')[0]}/01-{en.split('_')[0]}.jpg"
                out_video = RENDERS_DIR / f"adhikaram_{ch}_{en}_cinematic.mp4"
                render_image_based_video(image_file, audio_file, out_video)
                break
    else:
        build_all_missing_videos()
