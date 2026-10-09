import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

def test_launch():
    with sync_playwright() as p:
        browser = None
        for channel in ['msedge', 'chrome']:
            try:
                browser = p.chromium.launch(channel=channel, headless=True)
                print(f"Successfully launched {channel}!")
                break
            except Exception as e:
                print(f"Failed to launch {channel}: {e}")
        
        if not browser:
            print("Could not launch Edge or Chrome.")
            return

        page = browser.new_page()
        page.goto("http://localhost:8000/tharam-1.html#books", wait_until="networkidle")
        print("Page title:", page.title())

        # Check console errors and failed network requests
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.on("console", lambda msg: print(f"[CONSOLE {msg.type}] {msg.text}") if msg.type in ['error', 'warning'] else None)
        page.on("requestfailed", lambda req: print(f"[REQUEST FAILED] {req.url} : {req.failure}"))

        # Click each book shelf button (re-query each time)
        num_books = len(page.query_selector_all(".shelf-book-btn"))
        print(f"Total book shelf buttons: {num_books}")

        for i in range(num_books):
            books = page.query_selector_all(".shelf-book-btn")
            book_btn = books[i]
            text = book_btn.inner_text().replace('\n', ' ')
            print(f"Clicking book button {i+1}: {text}")
            book_btn.click()
            page.wait_for_timeout(300)
            
            # Now verify chapters exist and click each
            num_chaps = len(page.query_selector_all(".reader-chap-btn"))
            print(f"  Under book {i+1}, found {num_chaps} chapter tabs.")
            for c_idx in range(num_chaps):
                chaps = page.query_selector_all(".reader-chap-btn")
                chap_btn = chaps[c_idx]
                c_text = chap_btn.inner_text().replace('\n', ' ')
                chap_btn.click()
                page.wait_for_timeout(150)
                # Verify reading card exists
                card = page.query_selector(".reading-chapter-card")
                if not card:
                    print(f"  ERROR: No reading chapter card found for book {i+1}, chap {c_idx+1}!")
                
                # Check carousel next / prev
                next_btn = page.query_selector(".carousel-next-btn")
                if next_btn:
                    next_btn.click()
                    page.wait_for_timeout(50)

        # Test Moola Nool button
        moola_btn = page.query_selector(".moola-read-btn")
        if moola_btn:
            print("Clicking Moola Nool button...")
            moola_btn.click()
            page.wait_for_timeout(300)
            modal = page.query_selector("#moolaNoolModalBackdrop.open")
            if modal:
                print("Moola modal opened with .open class successfully!")
                page.screenshot(path="tools/tharam1_moola_modal.png")
                close_btn = page.query_selector(".moola-modal-close-btn")
                if close_btn:
                    close_btn.click()
                    page.wait_for_timeout(200)
                    is_still_open = page.query_selector("#moolaNoolModalBackdrop.open")
                    if not is_still_open:
                        print("Moola modal closed cleanly!")
                    else:
                        print("ERROR: Moola modal failed to close!")

        # Test Art Lightbox
        main_img = page.query_selector("#carouselMainImg")
        if main_img:
            print("Clicking Carousel Main Image to test lightbox...")
            main_img.click()
            page.wait_for_timeout(300)
            art_modal = page.query_selector("#artLightboxModal.active")
            if art_modal:
                print("Art Lightbox opened successfully!")
                page.screenshot(path="tools/tharam1_art_lightbox.png")
                close_btn = page.query_selector("#artLightboxModal button[onclick*='closeArtLightbox']")
                if close_btn:
                    close_btn.click()
                    page.wait_for_timeout(200)
                    is_art_open = page.query_selector("#artLightboxModal.active")
                    if not is_art_open:
                        print("Art Lightbox closed cleanly!")

        # Check for page errors
        print(f"Total page errors encountered: {len(errors)}")
        for err in errors:
            print(f"PAGE ERROR: {err}")

        # Take final full-page screenshot
        page.screenshot(path="tools/tharam1_click_test.png", full_page=True)
        print("Full page screenshot saved to tools/tharam1_click_test.png")

        browser.close()

if __name__ == "__main__":
    test_launch()
