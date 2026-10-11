import asyncio
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe", headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 900})
        page = await context.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        print("--> Testing tharam-1.html for Preschool 50/50 Split Sections...")
        await page.goto("http://127.0.0.1:8080/tharam-1.html", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Ensure active chapter area is rendered
        await page.wait_for_selector("#activeChapterReadingArea", timeout=5000)
        
        split_sections = await page.query_selector_all(".primary-section-split")
        print(f"Found {len(split_sections)} .primary-section-split sections on tharam-1.html")
        assert len(split_sections) >= 5, f"Expected at least 5 split sections, found {len(split_sections)}"

        section_ids = ["#subchap-verse", "#subchap-exposition", "#subchap-story", "#subchap-life", "#subchap-exercise"]
        for s_id in section_ids:
            sec = await page.query_selector(s_id)
            assert sec is not None, f"Missing section {s_id}"
            
            # Check visual card and img exist
            img = await sec.query_selector(".split-visual-card img")
            assert img is not None, f"Missing image inside section {s_id}"
            src = await img.get_attribute("src")
            print(f"  ✓ {s_id} contains visual with src: {src}")
            assert src and len(src) > 5, f"Invalid image src in {s_id}"

            # Check text col exists
            text_col = await sec.query_selector(".split-text-col")
            assert text_col is not None, f"Missing text column in {s_id}"

        # Check alternating rhythm
        verse_sec = await page.query_selector("#subchap-verse")
        verse_classes = await verse_sec.get_attribute("class")
        assert "split-reverse" not in verse_classes, "Verse should not be reverse"

        expo_sec = await page.query_selector("#subchap-exposition")
        expo_classes = await expo_sec.get_attribute("class")
        assert "split-reverse" in expo_classes, "Exposition should have split-reverse"

        story_sec = await page.query_selector("#subchap-story")
        story_classes = await story_sec.get_attribute("class")
        assert "split-reverse" not in story_classes, "Story should not be reverse"

        life_sec = await page.query_selector("#subchap-life")
        life_classes = await life_sec.get_attribute("class")
        assert "split-reverse" in life_classes, "Life should have split-reverse"

        print("✓ Alternating 50/50 rhythm verified!")

        # Check 3 Ds structured cards
        cards_3d = await page.query_selector_all(".primary-3d-item")
        print(f"✓ Found {len(cards_3d)} primary 3D items inside Life section")
        assert len(cards_3d) >= 1, "Expected 3D items in life section"

        # Check Quick Chapter Visual Strip
        strip_thumbs = await page.query_selector_all(".primary-strip-thumb-btn")
        print(f"✓ Found {len(strip_thumbs)} quick jump thumbnail scenes in Visual Strip")
        assert len(strip_thumbs) >= 5, "Expected thumbnails in visual strip"

        # Test Lightbox Modal trigger on image click
        first_img_wrap = await page.query_selector(".split-visual-img-wrap")
        assert first_img_wrap is not None, "Missing split-visual-img-wrap"
        await first_img_wrap.click()
        await page.wait_for_timeout(600)

        lightbox = await page.query_selector("#artLightboxModal.active")
        assert lightbox is not None, "Art Lightbox should be active after image click"
        print("✓ Art Lightbox modal successfully opened on image click!")

        # Close lightbox
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(400)
        lightbox_inactive = await page.query_selector("#artLightboxModal.active")
        assert lightbox_inactive is None, "Art Lightbox should close on Escape"
        print("✓ Art Lightbox closed cleanly!")

        # Check Grade 2 as well
        print("--> Testing tharam-2.html for Preschool 50/50 Split Sections...")
        await page.goto("http://127.0.0.1:8080/tharam-2.html", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        split_sections_g2 = await page.query_selector_all(".primary-section-split")
        print(f"Found {len(split_sections_g2)} .primary-section-split sections on tharam-2.html")
        assert len(split_sections_g2) >= 5, f"Expected at least 5 split sections on tharam-2, found {len(split_sections_g2)}"

        # Check console errors (filter out known chrome-extension or missing favicon if any)
        real_errors = [e for e in console_errors if "favicon" not in e.lower() and "extension" not in e.lower()]
        print(f"Real console errors: {real_errors}")
        assert len(real_errors) == 0, f"Found unexpected console errors: {real_errors}"

        print("=== ALL PRIMARY 50/50 PRESCHOOL SPLIT TESTS PASSED! ===")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
