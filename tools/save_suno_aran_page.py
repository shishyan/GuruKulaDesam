import asyncio, sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
            headless=True
        )
        page = await browser.new_page()
        await page.goto("https://suno.com/song/4d6133cc-4ae7-41ca-aef4-818821a2fefd", wait_until="networkidle")
        await asyncio.sleep(3)
        body = await page.inner_text("body")
        print("Body text length:", len(body))
        with open("scratch/suno_aran_body.txt", "w", encoding="utf-8") as f:
            f.write(body)
        print("Saved scratch/suno_aran_body.txt successfully!")
        await browser.close()

asyncio.run(main())
