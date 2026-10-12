import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'yt_api_form' in t.url][0]
        
        # Click on all section headers to expand them
        sections = [
            "Section 2: Organization and Contact Information",
            "Section 3: Business Model and Google Contacts",
            "Section 4: API Client Overview and Access Information",
            "Section 5: Use Cases and Quota Extension Details",
            "Section 6: Additional Evidence and Documentation Requirements",
            "Section 7: Attestations and Submission"
        ]
        
        for sec in sections:
            try:
                el = page.locator(f"text='{sec}'")
                await el.click()
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Error expanding {sec}: {e}")

        # Extract all input, textarea, and select fields with their preceding labels
        fields_info = await page.evaluate('''() => {
            const results = [];
            const fields = document.querySelectorAll('input[type="text"], textarea, select');
            fields.forEach(f => {
                let label = '';
                let parent = f.closest('.field') || f.parentElement;
                if (parent) {
                    const l = parent.querySelector('label') || parent.querySelector('legend');
                    if (l) label = l.innerText.trim();
                }
                results.push({
                    name: f.name || f.id,
                    placeholder: f.placeholder,
                    type: f.tagName.toLowerCase(),
                    label: label
                });
            });
            return results;
        }''')

        print(f"Total fields found: {len(fields_info)}")
        for f in fields_info:
            print(f"- Label: {f['label']} | Tag: {f['type']} | Placeholder: {f['placeholder']}")

asyncio.run(main())

