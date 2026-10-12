import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/B60TIM5LLvY.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 44 குற்றங்கடிதல் வருமுன்னர் காவாதான் வாழ்க்கை எரிமுன்னர் வைத்தூறு போலக் கெடும்')
with open('temp_audio/B60TIM5LLvY_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
