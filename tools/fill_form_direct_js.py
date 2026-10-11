import asyncio, sys
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = [t for t in context.pages if 'yt_api_form' in t.url][0]
        await page.bring_to_front()

        # Fill all fields using direct JavaScript
        res = await page.evaluate('''() => {
            function setVal(selector, val) {
                const el = document.querySelector(selector);
                if (el) {
                    el.value = val;
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                    return true;
                }
                return false;
            }

            function clickEl(selector) {
                const el = document.querySelector(selector);
                if (el) {
                    el.click();
                    return true;
                }
                return false;
            }

            // Click radio for individual
            const radios = document.querySelectorAll('input[type="radio"]');
            radios.forEach(r => {
                const parentText = r.closest('label, .list-item, div')?.innerText || '';
                if (parentText.includes('individual')) {
                    r.click();
                }
            });

            const results = {};
            results['org_name'] = setVal('#organization_name', 'self');
            results['website'] = setVal('#organization_website', 'https://gurukuladesam.com');
            results['work_desc'] = setVal('#organization_work_related_yt', 'Digital cultural and spiritual archive channel (Guru Kula Desam) providing authentic classical Tamil scripture, hymn compositions, educational films, and devotional audio.');
            results['channel_url'] = setVal('#associated_channel_url', 'https://www.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q');
            results['api_client'] = setVal('#api_client_form', 'Guru Kula Desam Channel Synchronizer');
            results['primary_url'] = setVal('#primary_access_url', 'https://gurukuladesam.com');
            results['privacy_url'] = setVal('#privacy_policy_url', 'https://gurukuladesam.com');
            results['project_num'] = setVal('#google_cloud_project_1', '839236964216');
            results['quota_num'] = setVal('#default_per_day_project_1', '100000');
            results['justification'] = setVal('#use_api_justification_project_1', 'Syncing authentic Tamil scripture verses into YouTube descriptions and uploading native timed .srt subtitle tracks across 370+ published videos for hearing accessibility and student learning. Each caption track upload requires 400 quota units, exceeding the default 10,000 units/day limit.');

            return results;
        }''')
        
        print("DOM Injection Results:", res, flush=True)
        await asyncio.sleep(1)
        await page.screenshot(path='production/quota_form_injected.png')
        print("Saved screenshot to production/quota_form_injected.png", flush=True)

asyncio.run(main())

