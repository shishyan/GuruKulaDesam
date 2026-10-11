import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

PLAYLIST_ID = 'PLKng43jJe18o'  # Goddess Amman Songs
TARGET_VID = 'fq0nJxj5aU4'      # அபிராமி அந்தாதி: தனந்தரும் கல்விதரும்

print(f"Adding {TARGET_VID} to Goddess Amman Songs ({PLAYLIST_ID})...")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    res = page.evaluate('''async ([plId, vid]) => {
        const cookies = document.cookie.split('; ');
        let sapisid = '';
        for (const c of cookies) {
            if (c.startsWith('SAPISID=')) { sapisid = c.split('=')[1]; break; }
        }
        if (!sapisid) {
            for (const c of cookies) {
                if (c.startsWith('__Secure-3PAPISID=')) { sapisid = c.split('=')[1]; break; }
            }
        }
        const now = Math.floor(Date.now() / 1000);
        const origin = window.location.origin;
        const msg = `${now} ${sapisid} ${origin}`;
        const enc = new TextEncoder().encode(msg);
        const hashBuf = await crypto.subtle.digest('SHA-1', enc);
        const hashArr = Array.from(new Uint8Array(hashBuf));
        const hashHex = hashArr.map(b => b.toString(16).padStart(2, '0')).join('');
        const authHeader = `SAPISIDHASH ${now}_${hashHex}`;

        const payload = {
            context: window.ytcfg ? window.ytcfg.get('INNERTUBE_CONTEXT') : {},
            playlistId: plId,
            actions: [
                {
                    action: "ACTION_ADD_VIDEO",
                    addedVideoId: vid
                }
            ]
        };

        const resp = await fetch('/youtubei/v1/browse/edit_playlist?prettyPrint=false', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': authHeader,
                'X-Origin': origin
            },
            body: JSON.stringify(payload)
        });
        return await resp.json();
    }''', [PLAYLIST_ID, TARGET_VID])
    
    print("Addition response:", res.get('status'))
    if res.get('status') == 'STATUS_SUCCEEDED':
        print(f"Successfully added {TARGET_VID} (அபிராமி அந்தாதி) to Goddess Amman Songs playlist!")
    else:
        print("Response details:", json.dumps(res)[:200])

# Update master catalog
with open('master_all_598_songs_catalog.json', encoding='utf-8') as f:
    catalog = json.load(f)

for s in catalog:
    if s['video_id'] == TARGET_VID:
        if 'Goddess Amman Songs' not in s.get('playlists', []):
            s.setdefault('playlists', []).append('Goddess Amman Songs')
        s['genre'] = 'அம்மன் / சக்தி (Goddess Amman)'
        print("Updated catalog metadata for fq0nJxj5aU4 (Genre: Amman, Playlist: Goddess Amman Songs)")
        break

with open('master_all_598_songs_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)
