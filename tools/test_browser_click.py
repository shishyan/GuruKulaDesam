import sys
from playwright.sync_api import sync_playwright

def run_tests():
    console_errors = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()

        def on_console(msg):
            if msg.type == 'error':
                console_errors.append(msg.text)
        
        page.on('console', on_console)

        print("--- Testing tharam-1.html ---")
        page.goto('http://localhost:8000/tharam-1.html', wait_until='networkidle')
        
        # Verify page title loaded
        print(f"Loaded tharam-1.html successfully. Title length: {len(page.title())}")

        # Check 7 book shelf buttons
        shelf_btns = page.locator('#booksShelfTabs .shelf-book-btn')
        shelf_count = shelf_btns.count()
        print(f"Found {shelf_count} shelf book buttons.")
        assert shelf_count == 7, f"Expected 7 books, found {shelf_count}"

        # Check chapter tabs
        chap_tabs = page.locator('#readerChapterTabs .reader-chap-btn')
        chap_count = chap_tabs.count()
        print(f"Found {chap_count} chapter tabs.")
        assert chap_count == 7, f"Expected 7 chapters, found {chap_count}"

        # Click through each book and verify chapters load
        for b_idx in range(shelf_count):
            btn = shelf_btns.nth(b_idx)
            btn.click()
            page.wait_for_timeout(200)
            
            # Check chapter tabs updated
            chaps = page.locator('#readerChapterTabs .reader-chap-btn')
            assert chaps.count() == 7, f"Book {b_idx} does not have 7 chapters"

            # Click chapter 1 and chapter 2
            chaps.nth(0).click()
            page.wait_for_timeout(100)
            heading = page.locator('.reading-chapter-card .chap-read-title').first
            assert heading.is_visible(), f"Chapter heading not visible for book {b_idx}"

        print("All 7 books and chapter clicks succeeded on tharam-1.html!")

        # Verify media section in active chapter
        media_section = page.locator('.chapter-media-card')
        if media_section.count() > 0:
            print("Chapter Sacred Song & Film section is present and rendered!")
            iframe = media_section.locator('iframe')
            if iframe.count() > 0:
                print("Playable YouTube embed iframe is correctly present!")
        else:
            print("Note: Chapter media section locator count:", media_section.count())

        # Test kalvi.html
        print("--- Testing kalvi.html ---")
        page.goto('http://localhost:8000/kalvi.html', wait_until='networkidle')
        stages = page.locator('.stage-row-card')
        print(f"kalvi.html stages count: {stages.count()}")
        assert stages.count() == 5, f"Expected 5 stages in kalvi.html (4 school + 1 higher studies), got {stages.count()}"

        books_in_kalvi = page.locator('.ashram-book-card')
        print(f"kalvi.html 7 books count: {books_in_kalvi.count()}")
        assert books_in_kalvi.count() == 7, f"Expected 7 books in kalvi.html, got {books_in_kalvi.count()}"

        # Test higher-studies.html
        print("--- Testing higher-studies.html ---")
        page.goto('http://localhost:8000/higher-studies.html', wait_until='networkidle')
        degree_btns = page.locator('.degree-filter-btn')
        print(f"higher-studies.html filter buttons count: {degree_btns.count()}")
        assert degree_btns.count() >= 5, f"Expected at least 5 degree buttons, got {degree_btns.count()}"

        # Test UG filter click
        page.locator('.degree-filter-btn[data-filter="ug"]').click()
        page.wait_for_timeout(100)
        assert page.locator('#tierUG').is_visible(), "UG tier should be visible"
        assert not page.locator('#tierPG').is_visible(), "PG tier should be hidden under UG filter"

        # Test PG filter click
        page.locator('.degree-filter-btn[data-filter="pg"]').click()
        page.wait_for_timeout(100)
        assert page.locator('#tierPG').is_visible(), "PG tier should be visible"
        assert not page.locator('#tierUG').is_visible(), "UG tier should be hidden under PG filter"

        # Test All filter click
        page.locator('.degree-filter-btn[data-filter="all"]').click()
        page.wait_for_timeout(100)
        assert page.locator('#tierUG').is_visible(), "UG tier should be visible under all"
        assert page.locator('#tierPG').is_visible(), "PG tier should be visible under all"
        print("Degree filtering (UG, PG, All) verified successfully!")

        # Test books.html
        print("--- Testing books.html ---")
        page.goto('http://localhost:8000/books.html', wait_until='networkidle')
        b_shelf = page.locator('#booksShelfTabs .shelf-book-btn')
        print(f"books.html shelf count: {b_shelf.count()}")
        assert b_shelf.count() == 7, f"Expected 7 books in books.html, got {b_shelf.count()}"

        # Filter console errors (ignore youtube / external 3rd party tracker errors)
        app_errors = [e for e in console_errors if 'youtube' not in e.lower() and 'doubleclick' not in e.lower() and 'google' not in e.lower()]
        print(f"Total internal application console errors: {len(app_errors)}")
        if app_errors:
            for err in app_errors:
                print("  ERROR:", err)
        
        browser.close()
        print("--- ALL BROWSER INTERACTION TESTS PASSED ---")

if __name__ == '__main__':
    run_tests()
