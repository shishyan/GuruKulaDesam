import asyncio
import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def verify_zen():
    os.makedirs('renders', exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe', headless=True)
        page = await b.new_page(viewport={'width': 1280, 'height': 850})
        
        grades_to_test = [1, 2, 3, 4, 5, 6, 7, 8]
        for g in grades_to_test:
            url = f'http://127.0.0.1:8080/tharam-{g}.html'
            print(f"\n[Testing Grade {g}] {url}...")
            await page.goto(url, wait_until='networkidle')
            await page.wait_for_timeout(1500)
            
            # 1. Verify Zen Grade Bar exists & is visible
            zen_bar = await page.query_selector('.zen-grade-bar')
            assert zen_bar is not None, f"Grade {g}: .zen-grade-bar missing!"
            is_zen_visible = await zen_bar.is_visible()
            assert is_zen_visible, f"Grade {g}: .zen-grade-bar not visible!"
            
            # 2. Verify Chapter Track exists & is visible
            chap_track = await page.query_selector('.reader-chapter-tabs')
            assert chap_track is not None, f"Grade {g}: .reader-chapter-tabs missing!"
            is_track_visible = await chap_track.is_visible()
            assert is_track_visible, f"Grade {g}: .reader-chapter-tabs not visible!"
            
            # 3. Verify Active Chapter Area exists
            active_area = await page.query_selector('#activeChapterReadingArea')
            assert active_area is not None, f"Grade {g}: #activeChapterReadingArea missing!"
            
            # 4. Check Section 1 top position (Should be above 500px, perfectly above the fold!)
            sec1 = await page.query_selector('#subchap-verse, .primary-section-split, .reader-section-card')
            assert sec1 is not None, f"Grade {g}: Section 1 missing in chapter!"
            box = await sec1.bounding_box()
            assert box is not None, f"Grade {g}: Bounding box for Section 1 is None!"
            print(f"  ✓ Grade {g} Section 1 top coordinate: {box['y']:.1f}px (Target: < 450px for immediate above-the-fold display)")
            assert box['y'] < 500, f"Grade {g} Section 1 is too far down ({box['y']}px)!"
            
            # Snapshot representative grades
            if g in [1, 3, 5, 8]:
                snap_path = f'renders/tharam_{g}_zen_above_fold.png'
                await page.screenshot(path=snap_path, full_page=False)
                print(f"  📸 Captured screenshot: {snap_path}")

        print("\n✅ ALL PRIMARY & MIDDLE GRADES (1-8) VERIFIED: Distraction-free Zen Above-The-Fold!")
        await b.close()

if __name__ == '__main__':
    asyncio.run(verify_zen())
