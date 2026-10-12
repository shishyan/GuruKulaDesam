import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/fRNAsDZr3QA.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 32 இன்னா செய்யாமை இன்னாசெய்தாரை ஒறுத்தல் அவர்நாண நன்னயஞ்செய்து விடல்')
with open('temp_audio/fRNAsDZr3QA_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
