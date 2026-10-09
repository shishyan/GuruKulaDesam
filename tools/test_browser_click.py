import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
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
        page.goto('http://localhost:8000/tharam-1.html', wait_until='domcontentloaded')
        
        # Verify page title loaded
        print(f"Loaded tharam-1.html successfully. Title length: {len(page.title())}")

        # Check 7 book shelf buttons
        page.wait_for_selector('#booksShelfTabs .shelf-book-btn', timeout=10000)
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

        # STUDENT PERSONA TEST: Chapter Completion, Quick Quiz & Reflection Notes
        print("--- Testing Student Persona: Chapter Mastery Deck & LMS Progress ---")
        mastery_deck = page.locator('#studentMasteryDeck')
        assert mastery_deck.is_visible(), "Student Mastery Deck should be visible in chapter"
        
        # 1. Mark as completed
        lms_btn = page.locator('#chapterLmsBtn')
        assert lms_btn.is_visible(), "Chapter LMS completion button should be visible"
        print("Initial LMS button text:", lms_btn.text_content().strip())
        lms_btn.click()
        page.wait_for_timeout(200)
        assert 'completed' in lms_btn.get_attribute('class'), "Button should have 'completed' class after click"
        print("Chapter marked as completed successfully!")

        # 2. Interactive Quick Knowledge Check (Quiz)
        quiz_opt = page.locator('.chapter-quiz-opt').first
        assert quiz_opt.is_visible(), "Quiz options should be visible"
        quiz_opt.click()
        page.wait_for_timeout(200)
        feedback = page.locator('.chapter-quiz-feedback')
        assert feedback.is_visible(), "Quiz feedback should be visible after answering"
        print("Quiz answered and interactive feedback verified!")

        # 3. Reflection Notes entry
        notes_textarea = page.locator('.chapter-note-textarea')
        assert notes_textarea.is_visible(), "Student reflection notes textarea should be visible"
        notes_textarea.fill("இன்று முதல் தினமும் காலையில் பெற்றோருக்கு வணக்கம் செய்வேன்.")
        page.wait_for_timeout(100)
        saved_badge = page.locator('#chapterNoteSavedBadge')
        assert saved_badge.is_visible(), "Saved note indicator should be visible"
        print("Student reflection note saved locally!")

        # 4. Student School Dashboard & Certificate Verification in school.html
        print("--- Testing Student Persona in school.html ---")
        page.goto('http://localhost:8000/school.html', wait_until='domcontentloaded')
        
        # Check student name customization
        page.fill('#studentNameInput', 'கவியரசன் மாணவர்')
        page.wait_for_timeout(100)
        assert page.locator('#certStudentNameDisplay').text_content().strip() == 'கவியரசன் மாணவர்'
        print("Student name dynamically synced to Certificate!")

        # Check LMS progress bar and completed count
        completed_val = page.locator('#completedLessonsCount').text_content().strip()
        print(f"School Dashboard completed count: {completed_val}")
        assert int(completed_val) >= 1, "Completed lessons count should be at least 1 after marking chapter completed"
        
        xp_val = page.locator('#totalVedicXP').text_content().strip()
        print(f"School Dashboard Vedic XP: {xp_val}")
        assert int(xp_val) >= 50, "Vedic XP should be at least 50"

        # Check Certificate Grade Switch to Collegiate degree
        page.select_option('#certGradeSelect', 'இளங்கலை (B.A. சனாதன தர்மம் & அறிவியல்)')
        page.wait_for_timeout(100)
        cert_tamil_title = page.locator('.certificate-title-tamil').text_content().strip()
        print("Collegiate Certificate title:", cert_tamil_title)
        assert 'வித்யாபீடம்' in cert_tamil_title, "Collegiate certificate title should reflect higher studies"
        assert 'இளங்கலை' in page.locator('#certBodyDisplay').text_content()
        print("Student Certificate graduation tier switch verified successfully!")

        # Test kalvi.html
        print("--- Testing kalvi.html ---")
        page.goto('http://localhost:8000/kalvi.html', wait_until='domcontentloaded')
        stages = page.locator('.stage-row-card')
        print(f"kalvi.html stages count: {stages.count()}")
        assert stages.count() == 5, f"Expected 5 stages in kalvi.html (4 school + 1 higher studies), got {stages.count()}"

        books_in_kalvi = page.locator('.ashram-book-card')
        print(f"kalvi.html 7 books count: {books_in_kalvi.count()}")
        assert books_in_kalvi.count() == 7, f"Expected 7 books in kalvi.html, got {books_in_kalvi.count()}"

        # Test higher-studies.html
        print("--- Testing higher-studies.html ---")
        page.goto('http://localhost:8000/higher-studies.html', wait_until='domcontentloaded')
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

        # Test admissions and administration section policy
        print("--- Testing Administration Section & Zero-BS-Pitch Sanctuary Policy ---")
        # 1. Verify admissions is located strictly under the dedicated Administration section
        admin_group = page.locator('.strip-group[data-group="admin"]')
        assert admin_group.count() > 0, "Dedicated administration section must exist in left-strip nav"
        assert admin_group.locator('a[href="admissions.html"]').count() >= 1, "Admissions must be under Administration section"
        
        # 2. Verify Grade 1 is completely isolated (no cross-grade links in main content)
        page.goto('http://localhost:8000/tharam-1.html', wait_until='domcontentloaded')
        assert page.locator('.grade-focus-bar').count() > 0, "Grade focus bar must be present"
        assert page.locator('.main-content a[href*="tharam-2"]').count() == 0, "No cross-grade link to tharam-2 in tharam-1 main"
        assert page.locator('.main-content a[href*="tharam-3"]').count() == 0, "No cross-grade link to tharam-3 in tharam-1 main"

        # 3. Verify zero commercial sales pitch on home page (index.html)
        page.goto('http://localhost:8000/index.html', wait_until='domcontentloaded')
        assert page.locator('text=PARENT ADMISSIONS NOTICE').count() == 0, "Commercial admissions sales box must be removed from index.html"
        assert page.locator('.hero-actions a[href="admissions.html"]').count() == 0, "No admissions button in hero banner"
        print("index.html is free of commercial sales pitch!")

        # 4. Verify admissions.html itself displays elevated 'Opening Soon' notification
        page.goto('http://localhost:8000/admissions.html', wait_until='domcontentloaded')
        notice = page.locator('#admissionFormSection')
        assert notice.is_visible(), "Admissions Opening Soon notice should be visible"
        assert "தயாரிப்பு நிலையில் உள்ளது" in notice.text_content(), "Notice should state admissions are in preparation"
        assert page.locator('#admissionForm').count() == 0, "Live application submit form should be disabled/hidden"
        print("admissions.html dignified 'Opening Soon' sanctuary notice verified successfully!")

        # Test books.html
        print("--- Testing books.html ---")
        page.goto('http://localhost:8000/books.html', wait_until='domcontentloaded')
        page.wait_for_selector('#booksShelfTabs .shelf-book-btn', timeout=10000)
        b_shelf = page.locator('#booksShelfTabs .shelf-book-btn')
        print(f"books.html shelf count: {b_shelf.count()}")
        assert b_shelf.count() == 7, f"Expected 7 books in books.html, got {b_shelf.count()}"

        # TEACHER / ACHARYA PERSONA TEST: Pedagogical Guide, 40-Week Calendar & Assessment Rubric
        print("--- Testing Teacher Persona: Pedagogical Guide & 40-Week Calendar in syllabus.html ---")
        page.goto('http://localhost:8000/syllabus.html', wait_until='domcontentloaded')
        teacher_section = page.locator('#teacherPedagogySection')
        assert teacher_section.is_visible(), "Teacher Pedagogy Section should be visible in syllabus.html"
        
        # Verify 5-Step Gurukula Classroom steps
        steps = teacher_section.locator('div[style*="border-radius: 12px"]')
        print(f"Found {steps.count()} classroom flow steps in Teacher Guide")
        assert steps.count() >= 5, f"Expected 5 classroom flow steps, got {steps.count()}"

        # Verify 40-Week 3-Term Academic Calendar
        term_cards = teacher_section.locator('div[style*="border-radius: 14px"]')
        print(f"Found {term_cards.count()} term calendar cards")
        assert term_cards.count() >= 3, f"Expected 3 term calendar cards, got {term_cards.count()}"

        # Verify Assessment Rubric Table (4 holistic pillars)
        rubric_rows = teacher_section.locator('tbody tr')
        print(f"Found {rubric_rows.count()} rubric evaluation rows")
        assert rubric_rows.count() >= 4, f"Expected 4 rubric pillars, got {rubric_rows.count()}"
        print("Teacher Pedagogical Handbook, 40-Week Calendar & Rubric verified successfully!")

        # Verify Teacher Moola Nool Reference Library
        print("--- Testing Teacher Persona: Moola Nool Direct Reference ---")
        page.goto('http://localhost:8000/moola-nool.html', wait_until='domcontentloaded')
        assert page.locator('#moolaSearchInput').is_visible(), "Moola Nool search input should be visible for teachers"
        print("Teacher Moola Nool reference library verified successfully!")

        # Filter console errors (ignore youtube / external 3rd party tracker errors / browser feature policy)
        app_errors = [e for e in console_errors if 'youtube' not in e.lower() and 'doubleclick' not in e.lower() and 'google' not in e.lower() and 'compute-pressure' not in e.lower()]
        print(f"Total internal application console errors: {len(app_errors)}")
        if app_errors:
            for err in app_errors:
                print("  ERROR:", err)
        
        browser.close()
        print("--- ALL BROWSER INTERACTION TESTS PASSED ---")

if __name__ == '__main__':
    run_tests()
