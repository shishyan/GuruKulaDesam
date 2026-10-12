import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/wzdoeFDq0iQ.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 56 கொடுங்கோன்மை முறைகோடி மன்னவன் செய்யின் உறைகோடி ஒல்லாது வானம் பெயல்')
with open('temp_audio/wzdoeFDq0iQ_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
