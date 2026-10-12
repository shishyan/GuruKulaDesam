import os, sys, json, yt_dlp, librosa, soundfile as sf
import whisper

vid = sys.argv[1] if len(sys.argv) > 1 else '6r6TpY-sgbw'
os.makedirs('scratch', exist_ok=True)
out_base = f'scratch/{vid}'

print(f'=== Starting Audio Download for {vid} ===')
ydl_opts = {
    'format': 'ba/b',
    'outtmpl': f'{out_base}.%(ext)s',
    'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
    'quiet': False
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(f'https://www.youtube.com/watch?v={vid}', download=True)
    ext = info['ext']
    raw_audio = f'{out_base}.{ext}'
    print('Downloaded raw audio:', raw_audio)

wav_path = f'{out_base}.wav'
print('Converting audio to 16kHz mono WAV using librosa...')
y, sr = librosa.load(raw_audio, sr=16000, mono=True)
sf.write(wav_path, y, 16000)
print('WAV created successfully, duration:', len(y)/16000, 'sec')

print('Running Whisper base STT...')
model = whisper.load_model('base')
result = model.transcribe(wav_path, language='ta', verbose=False)

with open(f'scratch/whisper_{vid}.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print('Whisper transcription complete! Segments:', len(result['segments']))
for seg in result['segments'][:5]:
    st = seg['start']
    en = seg['end']
    tx = seg['text'].strip()
    print(f"[{st:.2f} - {en:.2f}]: {tx}")
