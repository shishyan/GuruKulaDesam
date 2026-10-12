import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/QXWB2raWKXE.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 63 இடுக்கண் அழியாமை இடுக்கண் வருங்கால் நகுக அதனை அடுத்தூர்வது அஃதொப்பது இல்')
with open('temp_audio/QXWB2raWKXE_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
