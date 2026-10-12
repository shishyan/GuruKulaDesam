import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/rOowxP53oWA.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 65 சொல்வன்மை நாநலம் என்னும் நலனுடைமை')
with open('temp_audio/rOowxP53oWA_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
