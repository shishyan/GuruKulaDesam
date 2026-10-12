import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/dBIUA3fKBJ0.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 71 குறிப்பறிதல் அடுத்தது காட்டும் பளிங்குபோல் நெஞ்சம் கடுத்தது காட்டும் முகம்')
with open('temp_audio/dBIUA3fKBJ0_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
