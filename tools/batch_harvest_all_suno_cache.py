import json, os, sys, time, re
import requests

sys.stdout.reconfigure(encoding='utf-8')

def batch_harvest_all_suno():
    uuids_file = 'production/metadata/all_blob_uuids.json'
    if not os.path.exists(uuids_file):
        print(f"Error: {uuids_file} does not exist!")
        return

    uuids = json.load(open(uuids_file, encoding='utf-8'))
    print(f"Loaded {len(uuids)} total Suno cache UUIDs.")

    os.makedirs('production/suno_lyrics', exist_ok=True)
    os.makedirs('production/suno_meta', exist_ok=True)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    success_count = 0
    already_have = 0
    not_found = 0

    print(f"Harvesting songs and original lyrics across all {len(uuids)} IDs...")
    for idx, u in enumerate(uuids, 1):
        txt_path = f"production/suno_lyrics/{u}.txt"
        meta_path = f"production/suno_meta/{u}.json"

        # If we already have a good lyrics file, skip
        if os.path.exists(txt_path) and os.path.getsize(txt_path) > 20:
            already_have += 1
            continue

        try:
            r = requests.get(f"https://studio-api.prod.suno.com/api/clip/{u}", headers=headers, timeout=6)
            if r.status_code == 200:
                data = r.json()
                title = data.get('title', 'Untitled')
                lyrics = data.get('metadata', {}).get('prompt', '')
                
                # Save metadata
                with open(meta_path, 'w', encoding='utf-8') as mf:
                    json.dump(data, mf, ensure_ascii=False, indent=2)

                # Save lyrics if present
                if lyrics and len(lyrics.strip()) > 5:
                    with open(txt_path, 'w', encoding='utf-8') as lf:
                        lf.write(lyrics.strip())
                    print(f"  [{idx}/{len(uuids)}] ✅ {u} | {title[:35]} ({len(lyrics)} chars lyrics)", flush=True)
                    success_count += 1
                else:
                    print(f"  [{idx}/{len(uuids)}] ℹ️ {u} | {title[:35]} (Audio only / empty prompt)", flush=True)
            else:
                not_found += 1
        except Exception as e:
            pass

        time.sleep(0.12) # gentle rate limiting

    print("\n" + "=" * 60)
    print(f"HARVEST FINISHED: {success_count} newly fetched, {already_have} already present, {not_found} non-clip/private.")
    print(f"Total songs now in production/suno_lyrics: {len([f for f in os.listdir('production/suno_lyrics') if f.endswith('.txt')])}")
    print("=" * 60)

if __name__ == "__main__":
    batch_harvest_all_suno()
