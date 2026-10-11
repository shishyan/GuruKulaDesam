import sys
import time
import json
import base64
import pathlib
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLAN_FILE = ROOT / 'production' / 'thirukkural_sort_plan.json'
PROGRESS_FILE = ROOT / 'production' / 'browser_sort_progress.json'

def get_set_video_id(item_id):
    pad = len(item_id) % 4
    if pad:
        item_id += '=' * (4 - pad)
    decoded = base64.urlsafe_b64decode(item_id).decode('utf-8', errors='ignore')
    return decoded.split('.')[-1]

plan = json.load(open(PLAN_FILE, encoding='utf-8'))

if PROGRESS_FILE.exists():
    try:
        progress = json.load(open(PROGRESS_FILE, encoding='utf-8'))
    except Exception:
        progress = {}
else:
    progress = {}

def save_progress():
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

print(f"=== Starting Browser-Controlled Thirukkural Playlist Sorting ===", flush=True)
print(f"Total planned items to sort: {len(plan)} (Chapters 1 to 133)", flush=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    # Ensure on playlist page
    if 'list=PLW7qBZp_Q8Ro' not in page.url:
        print("Navigating to Thirukkural playlist page...", flush=True)
        page.goto('https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro', wait_until='domcontentloaded')
        time.sleep(3)
        
    # We sort in REVERSE order from target_pos 206 down to 0.
    # Moving each item to TOP means the last one moved (target_pos 0) stays at the absolute top,
    # followed by 1, 2, 3... down to 206!
    reverse_plan = list(reversed(plan))
    
    success_count = 0
    total = len(reverse_plan)
    
    for i, item in enumerate(reverse_plan):
        target_pos = item['target_position']
        chap = item['chapter']
        vid = item['videoId']
        title = item['title']
        item_id = item['itemId']
        set_vid = get_set_video_id(item_id)
        
        # Check if already processed in this reverse pass
        if progress.get(set_vid, {}).get('done'):
            continue
            
        # Execute Move to Top via YouTube's internal authenticated session
        res = page.evaluate('''async (svid) => {
            try {
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
                    headers: {
                        'Content-Type': 'application/json',
                        'X-YouTube-Client-Name': '1',
                        'X-YouTube-Client-Version': ytcfg.get('INNERTUBE_CLIENT_VERSION')
                    },
                    body: JSON.stringify(payload)
                });
                const data = await response.json();
                return {
                    status: response.status,
                    ok: response.ok,
                    statusText: response.statusText,
                    error: data.error ? data.error.message : null
                };
            } catch (err) {
                return { error: String(err), status: 0 };
            }
        }''', set_vid)
        
        if res.get('status') == 200 and not res.get('error'):
            success_count += 1
            progress[set_vid] = {'done': True, 'target_position': target_pos, 'chapter': chap, 'videoId': vid}
            print(f"[{i+1:03d}/{total:03d}] Moved to top: Pos {target_pos:03d} (Chap {chap:03d}) -> {title[:40]}", flush=True)
        else:
            print(f"[{i+1:03d}/{total:03d}] ERROR moving Pos {target_pos:03d} (Chap {chap:03d}): {res}", flush=True)
            progress[set_vid] = {'done': False, 'error': str(res)}
            
        if success_count % 10 == 0:
            save_progress()
            
        time.sleep(0.35)
        
    save_progress()
    print("\nSorting complete! Refreshing browser page to verify...", flush=True)
    page.reload(wait_until='domcontentloaded')
    time.sleep(4)
    page.screenshot(path='C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/playlist_sorted_final.png')
    print("Final playlist screenshot saved to playlist_sorted_final.png!", flush=True)
