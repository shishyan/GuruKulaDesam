import asyncio, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
COMPLIANCE_DIR = ROOT / 'production' / 'compliance'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = await context.new_page()
        await page.set_viewport_size({'width': 1280, 'height': 900})

        items = [
            ('privacy_policy.html', 'privacy_policy_screenshot.png'),
            ('terms_of_service.html', 'terms_of_service_documentation.png'),
            ('homepage.html', 'homepage_screenshot.png'),
            ('internal_tool_dashboard.html', 'internal_tool_dashboard.png'),
            ('oauth_consent_flow.html', 'oauth_consent_flow.png'),
        ]

        for html_file, png_out in items:
            file_url = (COMPLIANCE_DIR / html_file).as_uri()
            print(f"Rendering {html_file}...")
            await page.goto(file_url, wait_until='load')
            await asyncio.sleep(1)
            await page.screenshot(path=str(COMPLIANCE_DIR / png_out), full_page=True)
            print(f" -> Generated {png_out}")

        await page.close()
        print("\nAll compliance evidence screenshots rendered successfully!")

asyncio.run(main())

