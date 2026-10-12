import asyncio, json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'yt_api_form' in t.url][0]
        
        # Get details of inputs in Section 2, 3, 4, 5
        inputs = await page.evaluate('''() => {
            const arr = [];
            document.querySelectorAll('.field').forEach(f => {
                const label = f.querySelector('label, legend')?.innerText?.trim() || '';
                const input = f.querySelector('input[type="text"], textarea, select');
                if (input) {
                    arr.push({
                        label: label.substring(0, 80),
                        id: input.id,
                        name: input.name,
                        tagName: input.tagName.toLowerCase(),
                        placeholder: input.placeholder || ''
                    });
                }
            });
            return arr;
        }''')
        
        for idx, item in enumerate(inputs):
            print(f"[{idx}] Label: {item['label']} | ID: {item['id']} | Tag: {item['tagName']}")

asyncio.run(main())

