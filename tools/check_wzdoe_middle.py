import whisper, sys, scipy.io.wavfile as wav
sys.stdout.reconfigure(encoding='utf-8')
model = whisper.load_model('base')

rate, data = wav.read('temp_audio/wzdoeFDq0iQ.wav')
sub_data = data[int(115*rate):int(185*rate)]
wav.write('temp_audio/wzdoeFDq0iQ_115_185.wav', rate, sub_data)

res = model.transcribe('temp_audio/wzdoeFDq0iQ_115_185.wav', language='ta', initial_prompt='ஆபயன் குன்றும் அறுதொழிலோர் நூல்மறப்பர் துளியின்மை ஞாலத்திற்கு அல்லற்பட்டு ஆற்றாது அழுதகண் நீரன்றே')
for s in res['segments']:
    start = 115.0 + s['start']
    end = 115.0 + s['end']
    print(f"{start:.1f} - {end:.1f}: {s['text']}")
