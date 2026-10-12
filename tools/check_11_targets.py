import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

TARGET_IDS = [
    "-L3VXkM2MTY",
    "FFXImcs5Ehw",
    "QRSRyYEacMs",
    "iJ-3SHR2MKw",
    "yPfkP_EjTyc",
    "mQpQEuXiEZ4",
    "Yvlg_8JBHL4",
    "nGBmGzsD-kM",
    "T1KiH3G5WPs",
    "pYuwzoJkhTE",
    "zqStqzcFgbM"
]

print("Connecting to Chrome on port 9225...", flush=True)
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    print(f"Using browser tab: {page.url}", flush=True)
    
    results = []
    for idx, vid in enumerate(TARGET_IDS):
        print(f"[{idx+1}/{len(TARGET_IDS)}] Querying {vid}...", flush=True)
        try:
            info = page.evaluate('''async (v) => {
                const resp = await fetch('/youtubei/v1/player?prettyPrint=false', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        context: window.ytcfg ? window.ytcfg.get('INNERTUBE_CONTEXT') : {},
                        videoId: v
                    })
                });
                const data = await resp.json();
                const d = data.videoDetails || {};
                return {
                    videoId: v,
                    title: d.title || 'UNKNOWN',
                    shortDescription: d.shortDescription || ''
                };
            }''', vid)
            results.append(info)
            print(f"   -> Title: {info['title']}", flush=True)
            print(f"   -> Desc snippet: {repr(info['shortDescription'][:100])}", flush=True)
        except Exception as e:
            print(f"   -> Error: {e}", flush=True)
            results.append({'videoId': vid, 'error': str(e)})
        time.sleep(0.5)

    with open('production/current_11_targets.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\nSaved full details to production/current_11_targets.json", flush=True)
