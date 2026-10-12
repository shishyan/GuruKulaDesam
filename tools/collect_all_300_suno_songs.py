import asyncio, json, os, sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def scroll_and_collect_all_songs(url, out_prefix):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
            headless=True
        )
        page = await browser.new_page()
        
        all_songs = {}
        
        async def on_response(response):
            if "api" in response.url and ("feed" in response.url or "clip" in response.url or "playlist" in response.url):
                try:
                    data = await response.json()
                    clips = []
                    if isinstance(data, list):
                        clips = data
                    elif isinstance(data, dict):
                        clips = data.get("clips", data.get("items", []))
                    for c in clips:
                        if isinstance(c, dict) and "id" in c:
                            cid = c["id"]
                            if cid not in all_songs:
                                all_songs[cid] = {
                                    "id": cid,
                                    "title": c.get("title"),
                                    "url": f"https://suno.com/song/{cid}",
                                    "lyrics": c.get("metadata", {}).get("prompt", ""),
                                    "tags": c.get("metadata", {}).get("tags", ""),
                                    "duration": c.get("metadata", {}).get("duration", 0),
                                    "is_public": c.get("is_public", True)
                                }
                except Exception:
                    pass
        page.on("response", on_response)
        
        print(f"\n==========================================")
        print(f"Loading {url} and scrolling to end...")
        print(f"==========================================")
        await page.goto(url, wait_until="domcontentloaded", timeout=45000)
        await asyncio.sleep(4)
        
        # Continuously scroll down to trigger infinite scroll pagination
        previous_count = 0
        no_new_scrolls = 0
        for scroll_round in range(1, 150):
            # Also extract links directly from DOM
            dom_links = await page.evaluate('''() => {
                const links = Array.from(document.querySelectorAll('a[href*="/song/"]'));
                return links.map(a => ({
                    href: a.href,
                    text: a.innerText || a.textContent
                }));
            }''')
            for l in dom_links:
                href = l['href']
                if '/song/' in href:
                    cid = href.split('/song/')[-1].split('?')[0]
                    if cid and cid not in all_songs:
                        all_songs[cid] = {
                            "id": cid,
                            "title": l['text'].split('\n')[0].strip() or "Untitled",
                            "url": href,
                            "lyrics": "",
                            "is_public": True
                        }
                        
            current_count = len(all_songs)
            if scroll_round % 5 == 0 or current_count != previous_count:
                print(f"Scroll {scroll_round:02d}: Collected {current_count} unique songs so far...")
                
            if current_count == previous_count:
                no_new_scrolls += 1
                if no_new_scrolls >= 15:
                    print("Reached end of profile feed!")
                    break
            else:
                no_new_scrolls = 0
                
            previous_count = current_count
            await page.keyboard.press("PageDown")
            await page.mouse.wheel(0, 1500)
            await asyncio.sleep(1.2)
            
        print(f"\nTotal songs collected for {out_prefix}: {len(all_songs)}")
        os.makedirs("production/suno_library", exist_ok=True)
        out_file = f"production/suno_library/{out_prefix}_full.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(list(all_songs.values()), f, ensure_ascii=False, indent=2)
            
        print(f"Saved to {out_file}!")
        await browser.close()

async def main():
    await scroll_and_collect_all_songs("https://suno.com/@gurukuladesam", "gurukuladesam")
    await scroll_and_collect_all_songs("https://suno.com/@shishyan", "shishyan")

if __name__ == "__main__":
    asyncio.run(main())
