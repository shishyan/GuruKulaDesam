import sys
import time
import json
import base64
import pathlib
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLAN_FILE = ROOT / 'production' / 'thirukkural_sort_plan.json'
PROGRESS_FILE = ROOT / 'production' / 'innertube_sort_progress.json'

def get_set_video_id(item_id):
    pad = len(item_id) % 4
    if pad:
        item_id += '=' * (4 - pad)
    decoded = base64.urlsafe_b64decode(item_id).decode('utf-8', errors='ignore')
    return decoded.split('.')[-1]

plan = json.load(open(PLAN_FILE, encoding='utf-8'))

progress = {}
if PROGRESS_FILE.exists():
    try:
        progress = json.load(open(PROGRESS_FILE, encoding='utf-8'))
    except Exception:
        progress = {}

def save_progress():
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

print(f"=== Starting Innertube Authenticated Thirukkural Playlist Sorting ===", flush=True)
print(f"Total planned items to sort: {len(plan)} (Chapters 1 to 133)", flush=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    # Reverse plan: from 206 down to 0
    # Moving each to top means 0 lands at top, followed by 1, 2, ..., 206!
    reverse_plan = list(reversed(plan))
    total = len(reverse_plan)
    
    # Define JS helper once
    page.evaluate('''() => {
        window.__moveVideoToTop = async function(svid) {
            const cookies = document.cookie.split('; ');
            let sapisid = '';
            for (const c of cookies) {
                if (c.startsWith('SAPISID=')) {
                    sapisid = c.split('=')[1];
                    break;
                }
            }
            if (!sapisid) {
                for (const c of cookies) {
                    if (c.startsWith('__Secure-3PAPISID=')) {
                        sapisid = c.split('=')[1];
                        break;
                    }
                }
            }
            
            const now = Math.floor(Date.now() / 1000);
            const origin = 'https://www.youtube.com';
            const msg = `${now} ${sapisid} ${origin}`;
            
            const enc = new TextEncoder().encode(msg);
            const hashBuf = await crypto.subtle.digest('SHA-1', enc);
            const hashArr = Array.from(new Uint8Array(hashBuf));
            const hashHex = hashArr.map(b => b.toString(16).padStart(2, '0')).join('');
            const authHeader = `SAPISIDHASH ${now}_${hashHex}`;
            
            const payload = {
                context: ytcfg.get('INNERTUBE_CONTEXT'),
                actions: [
                    {
                        setVideoId: svid,
                        action: "ACTION_MOVE_VIDEO_AFTER"
                    }
                ],
                params: "CAFAAQ%3D%3D",
                playlistId: "PLW7qBZp_Q8Ro"
            };
            
            const response = await fetch('/youtubei/v1/browse/edit_playlist?prettyPrint=false', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': authHeader,
                    'X-Origin': origin,
                    'X-YouTube-Client-Name': '1',
                    'X-YouTube-Client-Version': ytcfg.get('INNERTUBE_CLIENT_VERSION')
                },
                body: JSON.stringify(payload)
            });
            
            const data = await response.json();
            return {
                httpStatus: response.status,
                status: data.status,
                actions: data.actions ? data.actions.length : 0
            };
        };
    }''')
    
    success_count = 0
    
    for i, item in enumerate(reverse_plan):
        target_pos = item['target_position']
        chap = item['chapter']
        vid = item['videoId']
        title = item['title']
        item_id = item['itemId']
        set_vid = get_set_video_id(item_id)
        
        # Retry up to 3 times
        success = False
        for attempt in range(3):
            res = page.evaluate('svid => window.__moveVideoToTop(svid)', set_vid)
            if res.get('status') == 'STATUS_SUCCEEDED':
                success = True
                break
            time.sleep(0.5)
            
        if success:
            success_count += 1
            progress[set_vid] = {'done': True, 'target_position': target_pos, 'chapter': chap, 'videoId': vid}
            print(f"[{i+1:03d}/{total:03d}] Moved to top: Pos {target_pos:03d} (Chap {chap:03d}) -> {title[:40]}", flush=True)
        else:
            print(f"[{i+1:03d}/{total:03d}] FAILED moving Pos {target_pos:03d} (Chap {chap:03d}): {res}", flush=True)
            progress[set_vid] = {'done': False, 'error': str(res)}
            
        if success_count % 10 == 0:
            save_progress()
            
        time.sleep(0.35)
        
    save_progress()
    print("\nInnertube sorting pass finished! Reloading page to verify...", flush=True)
    page.reload(wait_until='domcontentloaded')
    time.sleep(4)
    page.screenshot(path='C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/playlist_innertube_final.png')
    print("Verification screenshot saved!", flush=True)
