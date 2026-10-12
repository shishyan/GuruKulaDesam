import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/mCwNR1Bytj4.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 39 இறைமாட்சி முறைசெய்து காப்பாற்றும் மன்னவன் மக்கட்கு இறையென்று வைக்கப் படும்')
with open('temp_audio/mCwNR1Bytj4_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
