import soundfile as sf
import whisper, sys

sys.stdout.reconfigure(encoding='utf-8')
data, sr = sf.read('scratch/6r6TpY-sgbw.wav')
model = whisper.load_model('base')

chunks = [
    (15, 60, "Chorus 1"),
    (60, 120, "Verse 1"),
    (120, 160, "Chorus 2 / Verse 2"),
    (160, 210, "Verse 2 / Bridge"),
    (210, 273, "Final Chorus & Outro")
]

for start_s, end_s, label in chunks:
    chunk_data = data[int(start_s * sr):int(end_s * sr)]
    sf.write('scratch/temp_chunk.wav', chunk_data, sr)
    res = model.transcribe('scratch/temp_chunk.wav', language='ta', fp16=False)
    print(f"\n=== {label} [{start_s}s - {end_s}s] ===")
    for s in res['segments']:
        st = s['start'] + start_s
        en = s['end'] + start_s
        print(f"  [{st:6.2f} - {en:6.2f}] {s['text'].strip()}")
