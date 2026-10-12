import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/x3CyxNH5bpQ.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 69 தூது கற்றுக்கண் அஞ்சான் செலச்சொல்லிக் காலத்தால் தக்கது அறிவதாம் தூது')
with open('temp_audio/x3CyxNH5bpQ_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
