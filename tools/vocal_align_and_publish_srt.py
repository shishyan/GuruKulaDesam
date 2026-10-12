import os, sys, json, time
import subprocess
import whisper

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

def format_timestamp(seconds: float) -> str:
    millis = int(round((seconds - int(seconds)) * 1000))
    s = int(seconds)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d},{millis:03d}"

def generate_srt(segments):
    srt_lines = []
    for idx, seg in enumerate(segments, 1):
        start_str = format_timestamp(seg['start'])
        end_str = format_timestamp(seg['end'])
        text = seg['text'].strip()
        srt_lines.append(f"{idx}\n{start_str} --> {end_str}\n{text}\n")
    return "\n".join(srt_lines)

def process_track(video_id: str, suno_id: str, title: str):
    print(f"\n" + "=" * 60)
    print(f"Aligning: {video_id} - {title}")
    print("=" * 60)

    lyrics_file = f"production/suno_lyrics/{suno_id}.txt"
    if not os.path.exists(lyrics_file):
        print(f"Lyrics file missing: {lyrics_file}")
        return False

    with open(lyrics_file, "r", encoding="utf-8") as f:
        lyrics_text = f.read().strip()

    # Audio path
    audio_path = f"production/audio/{video_id}.mp3"
    wav_path = f"scratch/{video_id}.wav"
    os.makedirs("scratch", exist_ok=True)
    os.makedirs("production/subtitles", exist_ok=True)

    # Check if wav already exists in scratch
    if not os.path.exists(wav_path):
        if os.path.exists(audio_path):
            print(f"Converting {audio_path} -> {wav_path}...")
            cmd = f'ffmpeg -y -i "{audio_path}" -ar 16000 -ac 1 -c:a pcm_s16le "{wav_path}"'
            subprocess.run(cmd, shell=True, capture_output=True)
        else:
            # First try downloading directly from Suno CDN
            suno_cdn_url = f"https://cdn1.suno.ai/{suno_id}.mp4"
            print(f"Attempting Suno CDN download: {suno_cdn_url}...")
            cmd = f'ffmpeg -y -i "{suno_cdn_url}" -ar 16000 -ac 1 -c:a pcm_s16le "{wav_path}"'
            res = subprocess.run(cmd, shell=True, capture_output=True)
            if not os.path.exists(wav_path) or os.path.getsize(wav_path) < 10000:
                print(f"Suno CDN not accessible or empty. Falling back to yt_dlp for {video_id}...")
                try:
                    import yt_dlp
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': f'scratch/{video_id}.%(ext)s',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'wav',
                            'preferredquality': '192',
                        }],
                        'postprocessor_args': [
                            '-ar', '16000',
                            '-ac', '1'
                        ],
                        'quiet': True
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([f'https://www.youtube.com/watch?v={video_id}'])
                except Exception as e:
                    print(f"yt_dlp download failed: {e}")
                    return False

    if not os.path.exists(wav_path):
        print(f"Failed to obtain {wav_path}!")
        return False

    print("Running Whisper with Suno lyrics prompt...")
    model = whisper.load_model("base")
    
    # Clean prompt for Whisper (remove headers like [Chorus], [Verse])
    cleaned_prompt = "\n".join([line for line in lyrics_text.splitlines() if not line.startswith('[') and line.strip()])[:800]
    
    transcription = model.transcribe(
        wav_path,
        language="ta",
        initial_prompt=cleaned_prompt,
        fp16=False
    )

    srt_content = generate_srt(transcription["segments"])
    srt_out = f"production/subtitles/{video_id}.srt"
    with open(srt_out, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"Generated {len(transcription['segments'])} subtitle cues -> {srt_out}")

    # Publish subtitle to YouTube
    print(f"Publishing master SRT live to YouTube for {video_id}...")
    pub_cmd = f'python tools/api_publish_master.py "{video_id}"'
    subprocess.run(pub_cmd, shell=True)
    return True

if __name__ == "__main__":
    if len(sys.argv) > 2:
        vid = sys.argv[1]
        sid = sys.argv[2]
        process_track(vid, sid, "Single Run")
    else:
        # Run top priority tracks
        targets = [
            ("KI7uUFiJO1E", "b1db6391-fe2c-439b-992e-689b8e75eb1b", "அதிகாரம் 16 - பொறையுடைமை"),
            ("f1jxgAbXcdE", "75b979f1-bb57-4a2a-bb6a-90a92321ec13", "அதிகாரம் 2 - வான் சிறப்பு"),
            ("02C8glMmetw", "8cb22c54-8326-4af2-9a05-cf75ad2393cf", "அதிகாரம் 1 - கடவுள் வாழ்த்து"),
            ("C05GEfkJZaY", "cc5def14-edba-4e10-9542-eabf2afea1d6", "அதிகாரம் 5 - இல்வாழ்க்கை")
        ]
        for vid, sid, t in targets:
            process_track(vid, sid, t)
