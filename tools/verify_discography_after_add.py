import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

# 1. Master catalog check
with open('master_all_598_songs_catalog.json', encoding='utf-8') as f:
    catalog = json.load(f)

missing = [s for s in catalog if 'Discography' not in s.get('playlists', [])]
print(f"Master Catalog Total Songs: {len(catalog)}")
print(f"Tagged with Discography in Catalog: {len(catalog) - len(missing)} / {len(catalog)}")
print(f"Missing from Discography in Catalog: {len(missing)}")

# 2. Live YouTube Playlist Verification
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    print("\nQuerying live Discography playlist (PLAjtBRKl_IlI) from YouTube...")
    info = page.evaluate('''async () => {
        const resp = await fetch('/youtubei/v1/browse?prettyPrint=false', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                context: window.ytcfg ? window.ytcfg.get('INNERTUBE_CONTEXT') : {},
                browseId: 'VLPLAjtBRKl_IlI'
            })
        });
        const data = await resp.json();
        
        // Extract playlist header/title/stats
        const header = data.header || {};
        const title = header.playlistHeaderRenderer ? header.playlistHeaderRenderer.title.simpleText : 'Unknown';
        const numVideosText = header.playlistHeaderRenderer ? header.playlistHeaderRenderer.numVideosText.runs.map(r => r.text).join('') : '';
        
        const str = JSON.stringify(data);
        const matches = [];
        const regex = /"videoId":"([a-zA-Z0-9_-]{11})"/g;
        let m;
        while ((m = regex.exec(str)) !== null) {
            matches.push(m[1]);
        }
        const unique = [...new Set(matches)];
        return {
            title,
            numVideosText,
            uniqueItemCountSample: unique.length
        };
    }''')
    
    print("Live Playlist Title:", info.get('title'))
    print("Live Video Count from YouTube Header:", info.get('numVideosText'))
    print("Unique Sample Items in Initial Response:", info.get('uniqueItemCountSample'))
