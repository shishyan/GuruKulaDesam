import sys, json

sys.stdout.reconfigure(encoding='utf-8')
g = json.load(open('scratch/suno_gurukuladesam_api.json', encoding='utf-8'))
clips = g[0]['data'].get('clips', [])
print(f"=== Gurukuladesam clips count: {len(clips)} ===")
for c in clips:
    title = c.get('title')
    cid = c.get('id')
    prompt = c.get('metadata', {}).get('prompt', '')
    print(f"  {title} | {cid} | lyrics_len: {len(prompt)}")

s = json.load(open('scratch/suno_shishyan_api.json', encoding='utf-8'))
s_clips = s[0]['data'].get('clips', [])
print(f"\n=== Shishyan clips count: {len(s_clips)} ===")
for c in s_clips:
    title = c.get('title')
    cid = c.get('id')
    prompt = c.get('metadata', {}).get('prompt', '')
    print(f"  {title} | {cid} | lyrics_len: {len(prompt)}")
