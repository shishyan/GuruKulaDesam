import json, os, time, sys, re
import requests

sys.stdout.reconfigure(encoding='utf-8')

def scrape_missing_lyrics():
    with open('production/metadata/all_browser_history_suno.json', 'r', encoding='utf-8') as f:
        songs = json.load(f)

    os.makedirs('production/suno_lyrics', exist_ok=True)
    os.makedirs('production/suno_meta', exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    success = 0
    failed = 0
    
    for i, s in enumerate(songs, 1):
        url = s['url']
        cid = url.split('/song/')[-1].split('?')[0].strip()
        txt_path = f"production/suno_lyrics/{cid}.txt"
        meta_path = f"production/suno_meta/{cid}.json"
        
        if os.path.exists(txt_path) and os.path.getsize(txt_path) > 10:
            continue
            
        print(f"[{i}/{len(songs)}] Fetching {cid} - {s.get('title', '')[:30]}...")
        try:
            # Try Suno public clip API first
            api_url = f"https://studio-api.prod.suno.com/api/clip/{cid}"
            r = requests.get(api_url, headers=headers, timeout=10)
            lyrics = ""
            meta_data = {}
            if r.status_code == 200:
                meta_data = r.json()
                lyrics = meta_data.get("metadata", {}).get("prompt", "")
                
            if not lyrics:
                # Try fetching web page and extracting next_data or meta tags
                page_url = f"https://suno.com/song/{cid}"
                r_web = requests.get(page_url, headers=headers, timeout=10)
                if r_web.status_code == 200:
                    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">({.*?})</script>', r_web.text)
                    if m:
                        try:
                            nd = json.loads(m.group(1))
                            page_props = nd.get('props', {}).get('pageProps', {})
                            clip = page_props.get('clip', {})
                            lyrics = clip.get('metadata', {}).get('prompt', '')
                            if clip:
                                meta_data = clip
                        except Exception:
                            pass
                            
            if lyrics:
                with open(txt_path, "w", encoding="utf-8") as f_out:
                    f_out.write(lyrics.strip())
                if meta_data:
                    with open(meta_path, "w", encoding="utf-8") as f_meta:
                        json.dump(meta_data, f_meta, ensure_ascii=False, indent=2)
                print(f"  --> Saved lyrics ({len(lyrics)} chars)")
                success += 1
            else:
                print(f"  --> No lyrics found (HTTP {r.status_code})")
                failed += 1
        except Exception as e:
            print(f"  --> Error: {e}")
            failed += 1
            
        time.sleep(0.3)
        
    print(f"\nCompleted! New fetched: {success}, Failed/Empty: {failed}")

if __name__ == "__main__":
    scrape_missing_lyrics()
