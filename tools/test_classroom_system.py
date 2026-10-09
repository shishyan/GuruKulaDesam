import sys
import io
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def test_classroom():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context()
        page = context.new_page()

        console_errors = []
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda err: console_errors.append(str(err)))

        print("=== Test 1: Grade 1 (Primary - 3 Books + 60 Author Sheets) ===")
        page.goto('http://localhost:8000/tharam-1.html', wait_until='networkidle')
        page.wait_for_timeout(1000)

        # Check shelf tabs count
        shelf_buttons = page.locator('#booksShelfTabs .shelf-book-btn')
        shelf_count = shelf_buttons.count()
        print(f"Grade 1 Shelf Books Count: {shelf_count}")
        assert shelf_count == 3, f"Expected 3 books for Grade 1, found {shelf_count}"

        # Check default active book
        active_title = page.locator('#readerBookTitle').inner_text()
        print(f"Grade 1 Active Book Title: {active_title}")
        assert 'நற்செயல்' in active_title, f"Expected default book to be நற்செயல், got {active_title}"

        # Check tabs exist
        classwork_tab = page.locator('#btnTabClasswork')
        assert classwork_tab.is_visible()
        print("Classwork tab visible: OK")

        author_sheets_tab = page.locator('#btnTabAuthorSheets')
        assert author_sheets_tab.is_visible()
        print("Author sheets tab visible: OK")

        # Click Author Sheets Tab
        author_sheets_tab.click()
        page.wait_for_timeout(500)

        # Verify 60 sheets rendered
        sheets = page.locator('#classroomTabAuthorSheets .sheet-card')
        sheet_count = sheets.count()
        print(f"Grade 1 Author Scanned Sheets Count: {sheet_count}")
        assert sheet_count == 60, f"Expected 60 sheets for Grade 1, found {sheet_count}"

        # Click first sheet to open modal
        sheets.first.locator('.sheet-thumb').click()
        page.wait_for_timeout(500)

        modal = page.locator('#authorSheetLightboxModal')
        assert modal.is_visible(), "Expected Author Sheet modal to be open"
        modal_title = page.locator('#authorSheetPageTitle').inner_text()
        print(f"Modal sheet title: {modal_title}")
        assert 'பக்கம் 1' in modal_title

        # Close modal
        page.locator('.art-lightbox-close').click()
        page.wait_for_timeout(300)
        assert not modal.is_visible()
        print("Modal close: OK")

        # Test Schedule Tab
        page.locator('#btnTabSchedule').click()
        page.wait_for_timeout(500)
        weeks = page.locator('#classroomTabSchedule .trimester-week-card')
        print(f"Grade 1 Weeks in Roadmap: {weeks.count()}")
        assert weeks.count() == 12, "Expected 12 weeks"

        # Count total lessons in schedule
        lesson_rows = page.locator('#classroomTabSchedule .week-lesson-row')
        print(f"Grade 1 Lessons in Roadmap: {lesson_rows.count()}")
        assert lesson_rows.count() == 21, f"Expected 21 chapters in Primary schedule, found {lesson_rows.count()}"

        # Test Mastery Tab
        page.locator('#btnTabMastery').click()
        page.wait_for_timeout(500)
        mastery_cards = page.locator('#classroomTabMastery .mastery-book-card')
        print(f"Grade 1 Mastery Cards Count: {mastery_cards.count()}")
        assert mastery_cards.count() == 3, f"Expected 3 mastery cards, found {mastery_cards.count()}"

        # Test Diploma Tab
        page.locator('#btnTabDiploma').click()
        page.wait_for_timeout(500)
        diploma_title = page.locator('#gradeDiplomaShell .diploma-cert-title').inner_text()
        print(f"Grade 1 Diploma Title: {diploma_title}")
        assert 'தொடக்கப் பள்ளி' in diploma_title

        print("=== Test 2: Grade 2 (Primary - 3 Books + 64 Author Sheets) ===")
        page.goto('http://localhost:8000/tharam-2.html', wait_until='networkidle')
        page.wait_for_timeout(1000)

        g2_shelf_count = page.locator('#booksShelfTabs .shelf-book-btn').count()
        print(f"Grade 2 Shelf Books Count: {g2_shelf_count}")
        assert g2_shelf_count == 3, f"Expected 3 books for Grade 2, found {g2_shelf_count}"

        # Check 64 author sheets
        page.locator('#btnTabAuthorSheets').click()
        page.wait_for_timeout(500)
        g2_sheet_count = page.locator('#classroomTabAuthorSheets .sheet-card').count()
        print(f"Grade 2 Author Scanned Sheets Count: {g2_sheet_count}")
        assert g2_sheet_count == 64, f"Expected 64 sheets for Grade 2, found {g2_sheet_count}"

        print("=== Test 3: Grade 5 (Primary - 3 Books, No Scanned Sheets) ===")
        page.goto('http://localhost:8000/tharam-5.html', wait_until='networkidle')
        page.wait_for_timeout(1000)

        g5_shelf_count = page.locator('#booksShelfTabs .shelf-book-btn').count()
        print(f"Grade 5 Shelf Books Count: {g5_shelf_count}")
        assert g5_shelf_count == 3, f"Expected 3 books for Grade 5, found {g5_shelf_count}"
        assert page.locator('#btnTabAuthorSheets').count() == 0, "Grade 5 should not have Author Sheets tab"

        print("=== Test 4: Grade 6 (Secondary - 7 Books, 49 Chapters) ===")
        page.goto('http://localhost:8000/tharam-6.html', wait_until='networkidle')
        page.wait_for_timeout(1000)

        g6_shelf_count = page.locator('#booksShelfTabs .shelf-book-btn').count()
        print(f"Grade 6 Shelf Books Count: {g6_shelf_count}")
        assert g6_shelf_count == 7, f"Expected 7 books for Grade 6, found {g6_shelf_count}"

        # Check Schedule has 49 lessons
        page.locator('#btnTabSchedule').click()
        page.wait_for_timeout(500)
        g6_lessons = page.locator('#classroomTabSchedule .week-lesson-row').count()
        print(f"Grade 6 Lessons in Roadmap: {g6_lessons}")
        assert g6_lessons == 49, f"Expected 49 lessons for Secondary, found {g6_lessons}"

        # Check Mastery has 7 cards
        page.locator('#btnTabMastery').click()
        page.wait_for_timeout(500)
        g6_mastery = page.locator('#classroomTabMastery .mastery-book-card').count()
        print(f"Grade 6 Mastery Cards Count: {g6_mastery}")
        assert g6_mastery == 7, f"Expected 7 mastery cards, found {g6_mastery}"

        print("=== Test 5: Grade 12 (Secondary - 7 Books, 49 Chapters) ===")
        page.goto('http://localhost:8000/tharam-12.html', wait_until='networkidle')
        page.wait_for_timeout(1000)

        g12_shelf_count = page.locator('#booksShelfTabs .shelf-book-btn').count()
        print(f"Grade 12 Shelf Books Count: {g12_shelf_count}")
        assert g12_shelf_count == 7, f"Expected 7 books for Grade 12, found {g12_shelf_count}"

        browser.close()

        print("\n=== CONSOLE ERRORS CHECK ===")
        print(f"Total Console Errors Recorded: {len(console_errors)}")
        if console_errors:
            for err in console_errors:
                print(f"  ERROR: {err}")
            sys.exit(1)
        else:
            print("Zero console errors across all tested grades! PASSED!")

if __name__ == '__main__':
    test_classroom()
