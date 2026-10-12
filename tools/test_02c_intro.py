import whisper, wave, sys
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

model = whisper.load_model("tiny")

def test_window(s, e):
    with wave.open('scratch/02C8glMmetw.wav', 'rb') as fin:
        p = fin.getparams()
        fin.setpos(int(s * p.framerate))
        frames = fin.readframes(int((e - s) * p.framerate))
    with wave.open('scratch/temp_win.wav', 'wb') as fout:
        fout.setparams(p)
        fout.writeframes(frames)
    r = model.transcribe('scratch/temp_win.wav', language='ta', fp16=False)
    print(f"Window [{s:02d}s - {e:02d}s]: {r['text'].strip()}")

for start in [0, 6, 12, 18, 24, 28]:
    test_window(start, start + 6)
