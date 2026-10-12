import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            print("Connected to CDP 9222!")
            context = browser.contexts[0]
            page = await context.new_page()
            await page.goto("https://suno.com/me", wait_until="domcontentloaded")
            await asyncio.sleep(5)
            print("Current Suno URL:", page.url)
            print("Page Title:", await page.title())
            # Save screenshot
            await page.screenshot(path="scratch/suno_page.png")
            print("Saved scratch/suno_page.png")
        except Exception as e:
            print("Error connecting or opening Suno:", e)

asyncio.run(main())
