import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/SWAjAbur-TQ.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 1 கடவுள் வாழ்த்து அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு மலர்மிசை ஏகினான் மாணடி சேர்ந்தார்')
with open('temp_audio/SWAjAbur-TQ_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
