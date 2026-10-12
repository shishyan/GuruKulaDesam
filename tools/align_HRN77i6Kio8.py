import whisper, sys
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')
res = model.transcribe('temp_audio/HRN77i6Kio8.wav', language='ta', initial_prompt='திருக்குறள் அதிகாரம் 45 பெரியாரைத் துணைக்கோடல் அரியவற்றுள் எல்லாம் அரிதே பெரியாரை பேணித் தமராக் கொளல்')
with open('temp_audio/HRN77i6Kio8_whisper.txt', 'w', encoding='utf-8') as f:
    for seg in res['segments']:
        line = f"{seg['start']:.1f} - {seg['end']:.1f}: {seg['text']}\n"
        print(line, end='')
        f.write(line)
print('Whisper transcription complete!')
