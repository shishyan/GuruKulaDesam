import asyncio, json
from playwright.async_api import async_playwright

async def get_suno_song_data(song_id):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
            headless=True
        )
        page = await browser.new_page()
        clip_data = {}
        
        async def on_response(response):
            if "api" in response.url and "clip" in response.url:
                try:
                    d = await response.json()
                    clip_data.update(d)
                except Exception:
                    pass
        page.on("response", on_response)
        
        url = f"https://suno.com/song/{song_id}"
        print(f"Loading {url}...")
        await page.goto(url, wait_until="networkidle", timeout=45000)
        await asyncio.sleep(3)
        
        # Also grab lyrics text directly from the DOM
        lyrics_text = ""
        try:
            # Selector for lyrics container on song page
            lyrics_el = await page.query_selector("[class*='lyrics'], [class*='Lyrics']")
            if lyrics_el:
                lyrics_text = await lyrics_el.inner_text()
        except Exception as e:
            pass
            
        print("DOM Lyrics len:", len(lyrics_text))
        if lyrics_text:
            print("Preview:\n", lyrics_text[:300])
            
        with open(f"scratch/suno_{song_id}.json", "w", encoding="utf-8") as f:
            json.dump({"clip_api": clip_data, "dom_lyrics": lyrics_text}, f, ensure_ascii=False, indent=2)
            
        await browser.close()

asyncio.run(get_suno_song_data("4d6133cc-4ae7-41ca-aef4-818821a2fefd"))
