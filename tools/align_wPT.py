import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/wPT_1jgn2Ys.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 28 கூடா ஒழுக்கம் வலியில் நிலைமையான் வல்லுருவம் பெற்றம் புலியின்தோல் போர்த்து மேய்ந்தற்று நெஞ்சில் துறவார் துறந்தார்போல்')
with open('temp_audio/wPT_1jgn2Ys_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
