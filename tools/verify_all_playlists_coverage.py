import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

# 1. Master catalog
with open('master_all_598_songs_catalog.json', encoding='utf-8') as f:
    master_catalog = json.load(f)

catalog_by_id = {s['video_id']: s for s in master_catalog}
print(f"Catalog total songs: {len(catalog_by_id)}")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    
    # Use existing YouTube tab
    pl_page = None
    for pg in ctx.pages:
        if 'youtube.com' in pg.url and 'studio' not in pg.url:
            pl_page = pg
            break
    if not pl_page:
        pl_page = ctx.pages[0]
        
    print(f"Active tab: {pl_page.url}")
    
    # Query Innertube for all items in Discography (PLAjtBRKl_IlI)
    print("Fetching live videos from Discography (PLAjtBRKl_IlI)...")
    disco_vids = pl_page.evaluate('''async () => {
        const resp = await fetch('/youtubei/v1/browse?prettyPrint=false', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                context: window.ytcfg ? window.ytcfg.get('INNERTUBE_CONTEXT') : {},
                browseId: 'VLPLAjtBRKl_IlI'
            })
        });
        const data = await resp.json();
        const str = JSON.stringify(data);
        const matches = [];
        const regex = /"videoId":"([a-zA-Z0-9_-]{11})"/g;
        let m;
        while ((m = regex.exec(str)) !== null) {
            matches.push(m[1]);
        }
        return [...new Set(matches)];
    }''')
    
    print(f"Live unique videos retrieved from Discography (PLAjtBRKl_IlI): {len(disco_vids)}")
    
    # Compare with master catalog
    catalog_ids = set(catalog_by_id.keys())
    disco_set = set(disco_vids)
    
    missing_from_disco = [catalog_by_id[vid] for vid in catalog_ids if vid not in disco_set]
    print(f"Songs in Master Catalog missing from Discography: {len(missing_from_disco)}")
    
    by_genre = {}
    for s in missing_from_disco:
        g = s.get('genre', 'Unknown')
        by_genre[g] = by_genre.get(g, 0) + 1
        
    print("\nMissing by Genre:")
    for g, cnt in sorted(by_genre.items(), key=lambda x: -x[1]):
        print(f"  {g}: {cnt}")
        
    # Save audit report
    with open('production/grand_master_audit_report.json', 'w', encoding='utf-8') as f:
        json.dump({
            'total_in_catalog': len(catalog_by_id),
            'total_in_discography_live_sample': len(disco_vids),
            'total_missing_from_discography': len(missing_from_disco),
            'missing_by_genre': by_genre,
            'missing_songs': [
                {
                    'videoId': s.get('video_id'),
                    'title': s.get('canonical_title'),
                    'genre': s.get('genre'),
                    'track_type': s.get('track_type')
                }
                for s in missing_from_disco
            ]
        }, f, indent=2, ensure_ascii=False)
        
    print("Report saved to production/grand_master_audit_report.json")
