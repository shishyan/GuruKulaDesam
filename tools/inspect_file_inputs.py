import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'yt_api_form' in t.url][0]
        
        file_inputs = await page.evaluate('''() => {
            const arr = [];
            document.querySelectorAll('input[type="file"]').forEach((fi, idx) => {
                const parent = fi.closest('.field') || fi.parentElement;
                const label = parent ? (parent.querySelector('label, legend')?.innerText?.trim() || '') : '';
                arr.push({
                    idx: idx,
                    id: fi.id,
                    name: fi.name,
                    label: label
                });
            });
            return arr;
        }''')
        
        print(f"Total file upload inputs found: {len(file_inputs)}")
        for fi in file_inputs:
            print(f"[{fi['idx']}] ID: '{fi['id']}' | Name: '{fi['name']}' | Label: '{fi['label'][:80]}'")

asyncio.run(main())

