import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

CANDIDATES = [
    ("ssOkftpUcLE", "Siva Subramaniyar"),
    ("uPk4dyag74Y", "Thigada Sakkara 2026"),
    ("_eG3rWRIvJo", "Thigada Sakkara Film"),
    ("udRsA-oWxS0", "Ganesha Pancharatnam 1"),
    ("iXHNzqOrxzw", "Ganesha Pancharatnam 2"),
    ("qPjurMK6xpI", "Ganesha Pancharatnam 3"),
    ("Yg_IgGStRvY", "Kolaru Pathigam 2026"),
    ("CV1j4ieFw5w", "Avinasi Pathu"),
    ("bZ03UopgYcc", "Thaaye Karumari"),
    ("vaXLG5kUGVc", "Annai Renukambal"),
    ("grjVzzo-RWc", "Samayapurathaye Moolam"),
    ("wehcVz3BMHo", "Samayapurathaye Film"),
    ("Q5G2h9GuGQs", "Raghupati Raghava 1"),
    ("O7n8bL9XOn4", "Raghupati Raghava 2"),
    ("W2peLbC20sA", "Siva Subramaniyar Stub"),
    ("xAgvuRIIl6o", "Thiruvaiyaru Stub"),
    ("fq0nJxj5aU4", "Abirami Anthadhi 69"),
    ("mPypwIgdo-E", "Thirupulambal"),
    ("g42Pg2sg_gg", "Vedasaara Stotram"),
    ("rRoJfeRQiaM", "Thiruvaiyaru")
]

print(f"Connecting to Chrome on port 9225 to check {len(CANDIDATES)} candidates live on YouTube...", flush=True)
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    live_results = []
    for idx, (vid, name) in enumerate(CANDIDATES):
        print(f"[{idx+1}/{len(CANDIDATES)}] Fetching live {vid} ({name})...", flush=True)
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
                    desc: d.shortDescription || ''
                };
            }''', vid)
            
            d_text = info['desc']
            has_lyrics = "பாடல் வரிகள்" in d_text or "lyrics" in d_text.lower()
            verse_sample = ""
            if "பாடல் வரிகள்" in d_text:
                verse_sample = d_text.split("பாடல் வரிகள்")[1][:80].replace('\n', ' ').strip()
            elif len(d_text) > 0:
                verse_sample = d_text[:80].replace('\n', ' ').strip()
                
            live_results.append({
                'id': vid,
                'name': name,
                'title': info['title'],
                'desc_len': len(d_text),
                'has_lyrics': has_lyrics,
                'sample': verse_sample,
                'full_desc': d_text
            })
            print(f"   -> Live Title: {info['title']}", flush=True)
            print(f"   -> Desc len: {len(d_text)} | Has lyrics: {has_lyrics}", flush=True)
            print(f"   -> Sample: {verse_sample[:60]}", flush=True)
        except Exception as e:
            print(f"   -> Error: {e}", flush=True)
        time.sleep(0.3)

    with open('production/live_status_candidates.json', 'w', encoding='utf-8') as f:
        json.dump(live_results, f, indent=2, ensure_ascii=False)
    print("\nSaved live status to production/live_status_candidates.json", flush=True)
