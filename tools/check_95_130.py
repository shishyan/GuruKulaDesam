import whisper, sys, scipy.io.wavfile as wav
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')

rate, data = wav.read('temp_audio/rOowxP53oWA.wav')
sub_data = data[int(95*rate):int(130*rate)]
wav.write('temp_audio/rOowxP53oWA_95_130.wav', rate, sub_data)

res = model.transcribe('temp_audio/rOowxP53oWA_95_130.wav', language='ta', initial_prompt='ஆக்கமுங் கேடும் அதனால் வருதலால் காத்தோம்பல் சொல்லின்கட் சோர்வு')
for s in res['segments']:
    start = 95.0 + s['start']
    end = 95.0 + s['end']
    print(f"{start:.1f} - {end:.1f}: {s['text']}")
