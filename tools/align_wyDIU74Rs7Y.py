import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/wyDIU74Rs7Y.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 73 அவையஞ்சாமை வகையறிந்து வல்லவை வாய்சோரார் சொல்லின் தொகையறிந்த தூய்மையவர்')
with open('temp_audio/wyDIU74Rs7Y_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
