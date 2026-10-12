import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/whisper_ETELjf0OTi4.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for idx, s in enumerate(d['segments']):
    # print text and avg logprob and no speech prob
    print(f"[{idx+1:02d}] {s['start']:6.2f}s - {s['end']:6.2f}s (no_speech: {s['no_speech_prob']:.2f}, avg_logprob: {s['avg_logprob']:.2f}): {s['text'].strip()}")
