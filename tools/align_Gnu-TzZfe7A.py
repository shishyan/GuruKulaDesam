import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/Gnu-TzZfe7A.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 41 கல்லாமை நல்லார்கண் பட்ட வறுமையின் இன்னாதே கல்லார்கண் பட்ட திரு')
with open('temp_audio/Gnu-TzZfe7A_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
