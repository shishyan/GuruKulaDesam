import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'yt_api_form' in t.url][0]
        await page.bring_to_front()

        print("Expanding all sections...")
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
                await asyncio.sleep(0.3)
            except Exception:
                pass

        print("Filling technical details...")
        
        # Section 2
        try:
            await page.locator("text='As an individual user'").click()
        except Exception:
            pass
        
        await page.fill("#organization_name", "self")
        await page.fill("#organization_website", "https://gurukuladesam.com")
        await page.fill("#organization_work_related_yt", "Digital cultural and spiritual archive channel (Guru Kula Desam) providing authentic classical Tamil scripture, hymn compositions, educational films, and devotional audio.")

        # Section 3
        try:
            await page.fill("#associated_channel_url", "https://www.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q")
        except Exception:
            pass

        # Section 4
        await page.fill("#api_client_form", "Guru Kula Desam Synchronizer")
        await page.fill("#primary_access_url", "https://gurukuladesam.com")
        await page.fill("#privacy_policy_url", "https://gurukuladesam.com")

        # Project 1 fields
        try:
            await page.fill("#google_cloud_project_1", "839236964216")
        except Exception:
            pass

        try:
            await page.fill("#default_per_day_project_1", "100000")
            await page.fill("#use_api_justification_project_1", "Syncing authentic Tamil scripture verses into descriptions and uploading native timed .srt subtitle caption tracks across 370+ published videos for hearing accessibility and student learning. Each caption track upload requires 400 quota units, exceeding the default 10,000 units/day limit.")
        except Exception:
            pass

        await asyncio.sleep(2)
        await page.screenshot(path='production/quota_form_prefilled.png')
        print("Successfully prefilled technical form fields and saved screenshot!")

asyncio.run(main())

