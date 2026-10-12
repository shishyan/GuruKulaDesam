import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/jdvz-yoK5eI.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 79 நட்பு முகநக நட்பது நட்பன்று நெஞ்சத்து அகநக நட்பது நட்பு')
with open('temp_audio/jdvz-yoK5eI_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
