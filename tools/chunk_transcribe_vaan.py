import soundfile as sf
import whisper, sys

sys.stdout.reconfigure(encoding='utf-8')
data, sr = sf.read('scratch/f1jxgAbXcdE.wav')
duration = len(data) / sr
print(f"Loaded f1jxgAbXcdE.wav: {duration:.2f} seconds ({sr} Hz)")

model = whisper.load_model('base')

step = 40 # 40 second chunks
for start_s in range(0, int(duration), step):
    end_s = min(start_s + step, int(duration))
    chunk_data = data[int(start_s * sr):int(end_s * sr)]
    sf.write('scratch/temp_vaan_chunk.wav', chunk_data, sr)
    res = model.transcribe('scratch/temp_vaan_chunk.wav', language='ta', fp16=False)
    print(f"\n=== Window [{start_s:03d}s - {end_s:03d}s] ===")
    for s in res['segments']:
        st = s['start'] + start_s
        en = s['end'] + start_s
        print(f"  [{st:6.2f} - {en:6.2f}] {s['text'].strip()}", flush=True)
