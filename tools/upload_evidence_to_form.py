import asyncio, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
COMPLIANCE_DIR = ROOT / 'production' / 'compliance'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'yt_api_form' in t.url][0]
        await page.bring_to_front()

        print("Attaching compliance evidence files to form...")

        # 1. Privacy Policy Screenshot
        p1_path = str(COMPLIANCE_DIR / 'privacy_policy_screenshot.png')
        await page.set_input_files('#upload_1_1', p1_path)
        print(" -> Attached Privacy Policy Screenshot (#upload_1_1)")
        await asyncio.sleep(1)

        # 2. Homepage Screenshot
        p2_path = str(COMPLIANCE_DIR / 'homepage_screenshot.png')
        await page.set_input_files('#upload_1_2', p2_path)
        print(" -> Attached Homepage Screenshot (#upload_1_2)")
        await asyncio.sleep(1)

        # 3. Terms of Service Documentation
        p3_path = str(COMPLIANCE_DIR / 'terms_of_service_documentation.png')
        await page.set_input_files('#upload_1_3', p3_path)
        print(" -> Attached Terms of Service Documentation (#upload_1_3)")
        await asyncio.sleep(1)

        # 4. Conditional Evidence (Internal Dashboard / OAuth Flow)
        p4_path = str(COMPLIANCE_DIR / 'internal_tool_dashboard.png')
        await page.set_input_files('#upload_1_4', p4_path)
        print(" -> Attached Conditional Evidence Dashboard (#upload_1_4)")
        await asyncio.sleep(2)

        # Scroll to upload section and take a screenshot to verify
        await page.evaluate('''() => {
            const el = document.querySelector('#upload_1_1');
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }''')
        await asyncio.sleep(2)
        await page.screenshot(path='production/compliance/form_attached_evidence.png')
        print("Saved verification screenshot to production/compliance/form_attached_evidence.png")

asyncio.run(main())

