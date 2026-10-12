import whisper, json, sys, os

sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')

print("Transcribing scratch/f1jxgAbXcdE.wav directly without prompt...")
res = model.transcribe('scratch/f1jxgAbXcdE.wav', language='ta', fp16=False)

with open('scratch/f1jxgAbXcdE_whisper_direct.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print(f"Decoded {len(res['segments'])} segments:")
for s in res['segments']:
    print(f"  [{s['start']:6.2f} - {s['end']:6.2f}] {s['text'].strip()}")
