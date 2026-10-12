import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/xcUlgFsrepU.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 31 வெகுளாமை தன்னைத்தான் காக்கின் சினங்காக்க காவாக்கால் தன்னையே கொல்லுஞ் சினம்')
with open('temp_audio/xcUlgFsrepU_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
