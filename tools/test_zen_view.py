import asyncio
from playwright.async_api import async_playwright

async def snap():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe', headless=True)
        page = await b.new_page(viewport={'width': 1280, 'height': 850})
        await page.goto('http://127.0.0.1:8080/tharam-2.html', wait_until='networkidle')
        await page.wait_for_timeout(1500)
        await page.screenshot(path='renders/tharam_2_zen_above_fold.png', full_page=False)
        print('Captured renders/tharam_2_zen_above_fold.png')
        await b.close()

if __name__ == '__main__':
    asyncio.run(snap())
