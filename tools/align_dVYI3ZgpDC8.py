import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/dVYI3ZgpDC8.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 49 காலமறிதல் அருவினை என்ப உளவோ கருவியான் காலம் அறிந்து செயின்')
with open('temp_audio/dVYI3ZgpDC8_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
