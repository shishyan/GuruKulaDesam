import asyncio, json, os
from playwright.async_api import async_playwright

async def inspect_suno_profile(url, out_prefix):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
            headless=True
        )
        page = await browser.new_page()
        
        # Intercept Suno internal API responses for songs/clips
        songs = []
        async def on_response(response):
            if "api" in response.url and ("clip" in response.url or "feed" in response.url or "playlist" in response.url or "song" in response.url):
                try:
                    data = await response.json()
                    songs.append({"url": response.url, "data": data})
                except Exception:
                    pass
        page.on("response", on_response)
        
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(5)
        
        title = await page.title()
        print(f"Title: {title}")
        
        # Save screenshot
        os.makedirs("scratch", exist_ok=True)
        await page.screenshot(path=f"scratch/{out_prefix}.png", full_page=True)
        
        # Save page content
        content = await page.content()
        with open(f"scratch/{out_prefix}.html", "w", encoding="utf-8") as f:
            f.write(content)
            
        with open(f"scratch/{out_prefix}_api.json", "w", encoding="utf-8") as f:
            json.dump(songs, f, ensure_ascii=False, indent=2)
            
        print(f"Captured {out_prefix}! API calls: {len(songs)}")
        await browser.close()

async def main():
    await inspect_suno_profile("https://suno.com/@gurukuladesam", "suno_gurukuladesam")
    await inspect_suno_profile("https://suno.com/@shishyan", "suno_shishyan")

if __name__ == "__main__":
    asyncio.run(main())
