import whisper, sys, scipy.io.wavfile as wav
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')

rate, data = wav.read('temp_audio/rOowxP53oWA.wav')
sub_data = data[int(100*rate):int(135*rate)]
wav.write('temp_audio/rOowxP53oWA_100_135.wav', rate, sub_data)

res = model.transcribe('temp_audio/rOowxP53oWA_100_135.wav', language='ta')
for s in res['segments']:
    start = 100.0 + s['start']
    end = 100.0 + s['end']
    print(f"{start:.1f} - {end:.1f}: {s['text']}")
