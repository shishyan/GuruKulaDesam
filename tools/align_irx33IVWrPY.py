import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/irx33IVWrPY.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 75 அரண் எல்லாப் பொருளும் உடைத்தாய் இடத்துதவும் நல்லாள் உடையது அரண்')
with open('temp_audio/irx33IVWrPY_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
