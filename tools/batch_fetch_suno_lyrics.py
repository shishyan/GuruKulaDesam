import asyncio, json, os, sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def batch_fetch_lyrics():
    songs = json.load(open('production/metadata/all_extracted_suno_urls.json', encoding='utf-8'))
    os.makedirs('production/suno_lyrics', exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
            headless=True
        )
        page = await browser.new_page()
        
        print(f"Starting batch fetch for {len(songs)} Suno songs...")
        for i, s in enumerate(songs):
            song_id = s['id']
            title = s['title']
            out_file = f"production/suno_lyrics/{song_id}.txt"
            if os.path.exists(out_file) and os.path.getsize(out_file) > 100:
                continue
                
            url = s['url']
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(2)
                body = await page.inner_text("body")
                
                # Check if lyrics are found in body
                lines = body.split("\n")
                lyrics_lines = []
                capture = False
                for line in lines:
                    if any(tag in line for tag in ["[Chorus", "[Verse", "[Intro", "[Bridge", "[Outro", "[Hook"]):
                        capture = True
                    if capture:
                        if any(stop in line for stop in ["No comments yet", "Be the first one", "Comments", "More like this"]):
                            break
                        lyrics_lines.append(line)
                        
                extracted = "\n".join(lyrics_lines).strip()
                if not extracted:
                    extracted = body
                    
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(extracted)
                    
                print(f"[{i+1}/{len(songs)}] ✅ {title[:40]} -> {len(extracted)} chars")
            except Exception as e:
                print(f"[{i+1}/{len(songs)}] ❌ {title[:40]} -> {e}")
                
        await browser.close()
        print("Batch fetch complete!")

if __name__ == "__main__":
    asyncio.run(batch_fetch_lyrics())
