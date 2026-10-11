import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        print(f"Connected! Contexts: {len(browser.contexts)}")
        contexts = browser.contexts
        if contexts:
            pages = contexts[0].pages
            print(f"Pages: {len(pages)}")
            for page in pages:
                print(f" - {page.url} ({await page.title()})")

asyncio.run(main())

