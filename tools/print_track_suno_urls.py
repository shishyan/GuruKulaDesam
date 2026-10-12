import sys, json

sys.stdout.reconfigure(encoding='utf-8')
data = json.load(open('production/metadata/all_songs_lyrics_and_meanings.json', encoding='utf-8'))
for vid in ['HezzLu_n6qE', 'vbMywONB5Wc', '6r6TpY-sgbw', 'BfgGC7DsHMI', 'bH23l5vVgL8', 'SWAjAbur-TQ', 'aSQrSHA4YtU']:
    item = data.get(vid)
    if item:
        print(f"=== {vid} | {item.get('title')} ===")
        print("Suno URL:", item.get('suno_url'))
        lyrics = item.get('tamil_lyrics', '')
        print(f"Lyrics (length {len(lyrics)}):\n{lyrics[:350]}\n...")
    else:
        print(f"{vid} NOT FOUND in all_songs_lyrics_and_meanings.json")
