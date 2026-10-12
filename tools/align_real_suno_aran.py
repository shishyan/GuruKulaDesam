import whisper, json, sys, os

sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')

prompt = """
மணிநீரும் மண்ணும் மலையும் அணிநிழற் காடும் உடையது அரண்
எனைமாட்சித் தாகிய கண்ணும் வினைமாட்சி இல்லார்கண் இல்லது அரண்
எல்லாப் பொருளும் உடைத்தாய் இடத்துதவும் நல்லாள் உடையது அரண்
ஆற்று பவர்க்கும் அரண்பொருள் அஞ்சித்தற்போற்று பவர்க்கும் பொருள்
உயர்வகலம் திண்மை அருமை இந் நான்கின் அமைவரண் என்றுரைக்கும் நூல்
கொளற்கரிதாய்க் கொண்டகூழ்த் தாகி அகத்தார் நிலைக்கெளிதாம் நீரது அரண்
சிறுகாப்பிற் பேரிடத்த தாகி உறுபகை ஊக்கம் அழிப்பது அரண்
முனைமுகத்து மாற்றலர் சாய வினைமுகத்து வீறெய்தி மாண்டது அரண்
முற்றியும் முற்றா தெறிந்தும் அறைப்படுத்தும் பற்றற் கரியது அரண்
"""

print("Running Whisper on scratch/6r6TpY-sgbw.wav with exact Suno lyrics prompt...")
res = model.transcribe('scratch/6r6TpY-sgbw.wav', language='ta', initial_prompt=prompt, fp16=False)

with open('scratch/whisper_6r6TpY-sgbw_real_lyrics.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print(f"Done! {len(res['segments'])} segments decoded:")
for i, s in enumerate(res['segments']):
    print(f"{i+1:02d} [{s['start']:6.2f} - {s['end']:6.2f}] {s['text'].strip()}")
