import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')

model = whisper.load_model("tiny")

def probe(start_s, dur_s):
    import wave
    with wave.open('scratch/ETELjf0OTi4.wav', 'rb') as fin:
        params = fin.getparams()
        fin.setpos(int(start_s * params.framerate))
        frames = fin.readframes(int(dur_s * params.framerate))
    with wave.open('scratch/temp_probe.wav', 'wb') as fout:
        fout.setparams(params)
        fout.writeframes(frames)
    res = model.transcribe('scratch/temp_probe.wav', language='ta', fp16=False)
    for s in res.get('segments', []):
        print(f"[{start_s + s['start']:6.2f}s -> {start_s + s['end']:6.2f}s]: {s['text'].strip()}")

print("--- Probe 0 to 30 ---")
probe(0, 30)

print("--- Probe 70 to 110 ---")
probe(70, 40)

print("--- Probe 150 to 195 ---")
probe(150, 45)
