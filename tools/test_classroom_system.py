import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import asyncio
from playwright.async_api import async_playwright

async def run_classroom_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='msedge', headless=True)
        page = await browser.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: console_errors.append(str(err)))

        print("=== 1. Testing Grade 1 Classroom (tharam-1.html) ===")
        await page.goto("http://localhost:8000/tharam-1.html", wait_until="networkidle")
        await page.evaluate("() => localStorage.clear()")
        await page.reload(wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # 1. Verify classroom header mounted
        header = await page.query_selector(".classroom-header-card")
        assert header is not None, "Classroom header card not found!"
        title = await page.inner_text(".classroom-main-title")
        print(f"Found Classroom Title: {title}")
        assert "தரம் 1" in title, f"Expected தரம் 1 in title, got: {title}"

        # 2. Verify Tab navigation exists
        tabs = await page.query_selector_all(".classroom-tab-btn")
        print(f"Found {len(tabs)} classroom navigation tabs.")
        assert len(tabs) == 4, f"Expected 4 tabs, found {len(tabs)}"

        # 3. Check Tab 1: Classwork & Chapter Reader
        active_reading = await page.query_selector("#activeChapterReadingArea")
        assert active_reading is not None, "Active chapter reading area not found"
        chap_title = await page.inner_text(".chap-read-title")
        print(f"Active Chapter Title in Tab 1: {chap_title}")

        # 4. Switch to Tab 2: 12-Week Roadmap
        print("Switching to Tab 2 (12-Week Roadmap)...")
        await page.click("#btnTabSchedule")
        await page.wait_for_timeout(500)
        months = await page.query_selector_all(".trimester-month-card")
        print(f"Found {len(months)} Trimester Month cards.")
        assert len(months) == 3, f"Expected 3 month cards, got {len(months)}"

        weeks = await page.query_selector_all(".trimester-week-card")
        print(f"Found {len(weeks)} Trimester Week cards.")
        assert len(weeks) == 12, f"Expected 12 week cards, got {len(weeks)}"

        # 5. Toggle a lesson checkmark in Week 1
        lesson_check = await page.query_selector(".week-lesson-check")
        assert lesson_check is not None, "Lesson check button not found"
        await lesson_check.click()
        await page.wait_for_timeout(500)

        progress_label = await page.inner_text("#classroomProgressLabel")
        print(f"Updated Progress Label after click: {progress_label}")
        assert "1 / 49" in progress_label, f"Expected 1 / 49 in label, got {progress_label}"

        # 6. Test opening a lesson from Week 2
        print("Testing lesson navigation from schedule...")
        open_btns = await page.query_selector_all(".week-lesson-open-btn")
        if len(open_btns) > 4:
            await open_btns[4].click() # Click a lesson in week 2
            await page.wait_for_timeout(500)
            # Should have switched back to classwork tab
            active_btn = await page.inner_text(".classroom-tab-btn.active")
            print(f"Active tab after clicking lesson: {active_btn}")
            assert "பாடப் பணிகள்" in active_btn

        # 7. Switch to Tab 3: Mastery Tracker
        print("Switching to Tab 3 (Mastery Tracker)...")
        await page.click("#btnTabMastery")
        await page.wait_for_timeout(500)
        mastery_books = await page.query_selector_all(".mastery-book-card")
        print(f"Found {len(mastery_books)} Mastery Book cards.")
        assert len(mastery_books) == 7, f"Expected 7 books in mastery grid, got {len(mastery_books)}"

        # 8. Switch to Tab 4: Grade Term Diploma
        print("Switching to Tab 4 (Grade Term Diploma)...")
        await page.click("#btnTabDiploma")
        await page.wait_for_timeout(500)
        cert_title = await page.inner_text(".diploma-cert-title")
        print(f"Found Diploma Certificate: {cert_title}")
        assert "பருவ நிறைவுப் பட்டயச் சான்றிதழ்" in cert_title

        print("=== 2. Testing Grade 6 Classroom (tharam-6.html) ===")
        await page.goto("http://localhost:8000/tharam-6.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        title6 = await page.inner_text(".classroom-main-title")
        print(f"Found Grade 6 Title: {title6}")
        assert "தரம் 6" in title6

        print("=== 3. Testing Grade 12 Classroom (tharam-12.html) ===")
        await page.goto("http://localhost:8000/tharam-12.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        title12 = await page.inner_text(".classroom-main-title")
        print(f"Found Grade 12 Title: {title12}")
        assert "தரம் 12" in title12

        print(f"\nConsole Errors Count: {len(console_errors)}")
        if console_errors:
            print("Console Errors:")
            for err in console_errors:
                print(f"  - {err}")
        assert len(console_errors) == 0, f"Found {len(console_errors)} console errors!"

        await browser.close()
        print("\n ALL CLASSROOM & TRIMESTER TESTS PASSED WITH 0 CONSOLE ERRORS!")

if __name__ == "__main__":
    asyncio.run(run_classroom_test())
