import os
import sys
import json
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

ROOT = r'c:\GitHub\Gurukuladesam'

def test_data_files():
    print("--- 1. Testing data/books/ JSON files ---")
    for g in range(1, 13):
        fpath = os.path.join(ROOT, 'data', 'books', f'grade_{g}.json')
        assert os.path.exists(fpath), f"File missing: {fpath}"
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        nalvazhi_title = data['books']['nalvazhi']['title']
        assert nalvazhi_title == 'நற்பண்பு', f"Grade {g} nalvazhi title is '{nalvazhi_title}', expected 'நற்பண்பு'"
    print("✓ All 12 grade JSON files have nalvazhi title = 'நற்பண்பு'")

def test_reader_js_integrity():
    print("--- 2. Testing assets/js/books-reader.js ---")
    js_path = os.path.join(ROOT, 'assets', 'js', 'books-reader.js')
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()

    # Zero occurrences of நல்வழி
    assert 'நல்வழி' not in js, "Found occurrence of 'நல்வழி' in books-reader.js!"
    assert 'GRADE_1_2_SCHEDULE' in js, "Missing GRADE_1_2_SCHEDULE"
    assert 'GRADE_3_4_SCHEDULE' in js, "Missing GRADE_3_4_SCHEDULE"
    assert 'MIDDLE_SCHOOL_SCHEDULE' in js, "Missing MIDDLE_SCHOOL_SCHEDULE"
    assert 'HIGH_SCHOOL_SCHEDULE' in js, "Missing HIGH_SCHOOL_SCHEDULE"
    assert 'COLLEGIATE_SCHEDULE' in js, "Missing COLLEGIATE_SCHEDULE"
    print("✓ books-reader.js has 0 occurrences of 'நல்வழி' and all schedules present")

def test_browser_live_pages():
    print("--- 3. Testing Live Pages via Playwright ---")

    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)

        # Test Grade 1
        page = browser.new_page()
        page_errors = []
        page.on('console', lambda msg: page_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda exc: page_errors.append(str(exc)))

        page.goto('http://localhost:8000/tharam-1.html', wait_until='networkidle')
        # Check books shelf tabs count
        tabs = page.locator('#booksShelfTabs .shelf-book-btn')
        tab_count = tabs.count()
        assert tab_count == 1, f"Grade 1 expected 1 book tab, got {tab_count}"
        tab_text = tabs.first.inner_text()
        assert 'நற்செயல்' in tab_text, f"Grade 1 tab should be நற்செயல், got: {tab_text}"

        # Check Original sheets tab
        sheets_tab = page.locator('#btnTabAuthorSheets')
        assert sheets_tab.count() == 1, "Grade 1 should have Author's Original Sheets tab"

        # Check total chapters in progress
        progress_text = page.locator('#classroomProgressLabel').inner_text()
        assert '/ 7 அத்தியாயங்கள்' in progress_text, f"Grade 1 expected 7 total chapters, got {progress_text}"

        assert len(page_errors) == 0, f"Grade 1 console errors: {page_errors}"
        print("✓ Grade 1: Exactly 1 book (நற்செயல்), 7 chapters, Original Sheets tab present, 0 console errors")
        page.close()

        # Test Grade 2
        page = browser.new_page()
        page_errors = []
        page.on('console', lambda msg: page_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda exc: page_errors.append(str(exc)))

        page.goto('http://localhost:8000/tharam-2.html', wait_until='networkidle')
        tabs = page.locator('#booksShelfTabs .shelf-book-btn')
        tab_count = tabs.count()
        assert tab_count == 1, f"Grade 2 expected 1 book tab, got {tab_count}"
        tab_text = tabs.first.inner_text()
        assert 'நற்செயல்' in tab_text, f"Grade 2 tab should be நற்செயல், got: {tab_text}"

        sheets_tab = page.locator('#btnTabAuthorSheets')
        assert sheets_tab.count() == 1, "Grade 2 should have Author's Original Sheets tab"

        progress_text = page.locator('#classroomProgressLabel').inner_text()
        assert '/ 7 அத்தியாயங்கள்' in progress_text, f"Grade 2 expected 7 total chapters, got {progress_text}"

        assert len(page_errors) == 0, f"Grade 2 console errors: {page_errors}"
        print("✓ Grade 2: Exactly 1 book (நற்செயல்), 7 chapters, Original Sheets tab present, 0 console errors")
        page.close()

        # Test Grade 3
        page = browser.new_page()
        page_errors = []
        page.on('console', lambda msg: page_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda exc: page_errors.append(str(exc)))

        page.goto('http://localhost:8000/tharam-3.html', wait_until='networkidle')
        tabs = page.locator('#booksShelfTabs .shelf-book-btn')
        tab_count = tabs.count()
        assert tab_count == 2, f"Grade 3 expected 2 book tabs, got {tab_count}"
        names = [tabs.nth(i).inner_text() for i in range(tab_count)]
        assert any('நற்செயல்' in n for n in names), f"Expected நற்செயல் in {names}"
        assert any('நற்பண்பு' in n for n in names), f"Expected நற்பண்பு in {names}"
        assert not any('நல்வழி' in n for n in names), f"Unexpected நல்வழி in {names}"

        sheets_tab = page.locator('#btnTabAuthorSheets')
        assert sheets_tab.count() == 0, "Grade 3 should NOT have Author's Original Sheets tab"

        progress_text = page.locator('#classroomProgressLabel').inner_text()
        assert '/ 14 அத்தியாயங்கள்' in progress_text, f"Grade 3 expected 14 total chapters, got {progress_text}"

        assert len(page_errors) == 0, f"Grade 3 console errors: {page_errors}"
        print("✓ Grade 3: Exactly 2 books (நற்செயல், நற்பண்பு), 14 chapters, 0 console errors")
        page.close()

        # Test Grade 4
        page = browser.new_page()
        page_errors = []
        page.on('console', lambda msg: page_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda exc: page_errors.append(str(exc)))

        page.goto('http://localhost:8000/tharam-4.html', wait_until='networkidle')
        tabs = page.locator('#booksShelfTabs .shelf-book-btn')
        tab_count = tabs.count()
        assert tab_count == 2, f"Grade 4 expected 2 book tabs, got {tab_count}"
        progress_text = page.locator('#classroomProgressLabel').inner_text()
        assert '/ 14 அத்தியாயங்கள்' in progress_text, f"Grade 4 expected 14 total chapters, got {progress_text}"
        assert len(page_errors) == 0, f"Grade 4 console errors: {page_errors}"
        print("✓ Grade 4: Exactly 2 books (நற்செயல், நற்பண்பு), 14 chapters, 0 console errors")
        page.close()

        # Test Grade 6 (Middle School)
        page = browser.new_page()
        page_errors = []
        page.on('console', lambda msg: page_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda exc: page_errors.append(str(exc)))

        page.goto('http://localhost:8000/tharam-6.html', wait_until='networkidle')
        tabs = page.locator('#booksShelfTabs .shelf-book-btn')
        tab_count = tabs.count()
        assert tab_count == 5, f"Grade 6 expected 5 book tabs, got {tab_count}"
        names = [tabs.nth(i).inner_text() for i in range(tab_count)]
        assert any('நன்னெறி' in n for n in names), f"Expected நன்னெறி in {names}"
        assert any('நல்லறம்' in n for n in names), f"Expected நல்லறம் in {names}"
        assert any('நற்பண்பு' in n for n in names), f"Expected நற்பண்பு in {names}"
        assert any('நற்துணை' in n for n in names), f"Expected நற்துணை in {names}"
        assert any('நற்செயல்' in n for n in names), f"Expected நற்செயல் in {names}"
        assert not any('நற்சொல்' in n for n in names), f"Middle school should not have நற்சொல், got {names}"
        assert not any('நற்சிந்தனை' in n for n in names), f"Middle school should not have நற்சிந்தனை, got {names}"

        progress_text = page.locator('#classroomProgressLabel').inner_text()
        assert '/ 35 அத்தியாயங்கள்' in progress_text, f"Grade 6 expected 35 total chapters, got {progress_text}"

        assert len(page_errors) == 0, f"Grade 6 console errors: {page_errors}"
        print("✓ Grade 6: Exactly 5 books (no நற்சிந்தனை, no நற்சொல்), 35 chapters, 0 console errors")
        page.close()

        # Test Grade 10 (High School)
        page = browser.new_page()
        page_errors = []
        page.on('console', lambda msg: page_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda exc: page_errors.append(str(exc)))

        page.goto('http://localhost:8000/tharam-10.html', wait_until='networkidle')
        tabs = page.locator('#booksShelfTabs .shelf-book-btn')
        tab_count = tabs.count()
        assert tab_count == 6, f"Grade 10 expected 6 book tabs, got {tab_count}"
        names = [tabs.nth(i).inner_text() for i in range(tab_count)]
        assert any('நன்னெறி' in n for n in names), f"Expected நன்னெறி in {names}"
        assert any('நல்லறம்' in n for n in names), f"Expected நல்லறம் in {names}"
        assert any('நற்பண்பு' in n for n in names), f"Expected நற்பண்பு in {names}"
        assert any('நற்துணை' in n for n in names), f"Expected நற்துணை in {names}"
        assert any('நற்சொல்' in n for n in names), f"High school expected நற்சொல் in {names}"
        assert any('நற்செயல்' in n for n in names), f"Expected நற்செயல் in {names}"
        assert not any('நற்சிந்தனை' in n for n in names), f"High school should not have நற்சிந்தனை, got {names}"

        progress_text = page.locator('#classroomProgressLabel').inner_text()
        assert '/ 42 அத்தியாயங்கள்' in progress_text, f"Grade 10 expected 42 total chapters, got {progress_text}"

        assert len(page_errors) == 0, f"Grade 10 console errors: {page_errors}"
        print("✓ Grade 10: Exactly 6 books (no நற்சிந்தனை, includes நற்சொல்), 42 chapters, 0 console errors")
        page.close()

        # Test Grade 12 (Senior High School)
        page = browser.new_page()
        page_errors = []
        page.on('console', lambda msg: page_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda exc: page_errors.append(str(exc)))

        page.goto('http://localhost:8000/tharam-12.html', wait_until='networkidle')
        tabs = page.locator('#booksShelfTabs .shelf-book-btn')
        tab_count = tabs.count()
        assert tab_count == 6, f"Grade 12 expected 6 book tabs, got {tab_count}"
        progress_text = page.locator('#classroomProgressLabel').inner_text()
        assert '/ 42 அத்தியாயங்கள்' in progress_text, f"Grade 12 expected 42 total chapters, got {progress_text}"

        assert len(page_errors) == 0, f"Grade 12 console errors: {page_errors}"
        print("✓ Grade 12: Exactly 6 books, 42 chapters, 0 console errors")
        page.close()

        browser.close()

if __name__ == '__main__':
    test_data_files()
    test_reader_js_integrity()
    test_browser_live_pages()
    print("\n🎉 ALL CLASSROOM SYSTEM TESTS PASSED SUCCESSFULLY!")
