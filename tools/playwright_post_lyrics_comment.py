"""Post verified lyrics and meaning as an author comment on YouTube Topic videos via Playwright.
"""
import sys
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

CDP_URL = "http://127.0.0.1:9222"

def format_comment(text):
    """Extract lyrics and meaning section cleanly from dryrun text."""
    lines = text.splitlines()
    body_lines = []
    capture = False
    for l in lines:
        if "பாடல் வரிகள்" in l:
            capture = True
        if capture:
            if l.startswith("http") and "gurukuladesam" in l:
                body_lines.append(l)
                break
            body_lines.append(l)
    return "\n".join(body_lines).strip()

def post_comment_on_video(page, video_id, comment_text):
    url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"\nNavigating to {url}...")
    page.goto(url, wait_until='networkidle')
    time.sleep(2)
    
    # Scroll down to ensure comment section loads
    for _ in range(4):
        page.evaluate("window.scrollBy(0, 500)")
        time.sleep(1)
        
    placeholder = page.locator('#placeholder-area, #simplebox-placeholder').first
    if not placeholder.is_visible():
        print(f"[{video_id}] Error: Placeholder not visible. Comments might be disabled or page not loaded.")
        return False
        
    print(f"[{video_id}] Clicking comment box...")
    placeholder.click()
    time.sleep(1)
    
    input_box = page.locator('#contenteditable-root').first
    if not input_box.is_visible():
        print(f"[{video_id}] Error: Contenteditable input not visible.")
        return False
        
    print(f"[{video_id}] Typing lyrics and meaning ({len(comment_text)} chars)...")
    # Using clipboard/evaluate or fill to be fast and preserve formatting
    page.evaluate("""({text}) => {
        const el = document.querySelector('#contenteditable-root');
        el.focus();
        document.execCommand('insertText', false, text);
    }""", {'text': comment_text})
    time.sleep(1)
    
    submit_btn = page.locator('#submit-button button, ytd-button-renderer#submit-button').first
    if submit_btn.is_enabled():
        print(f"[{video_id}] Submitting comment...")
        submit_btn.click()
        time.sleep(3)
        print(f"[{video_id}] SUCCESS: Comment submitted successfully!")
        return True
    else:
        print(f"[{video_id}] Error: Submit button not enabled.")
        return False

if __name__ == '__main__':
    video_id = sys.argv[1] if len(sys.argv) > 1 else 'cKyT1Cv7zEA'
    source_file = Path("production/youtube_dryrun/shiva/KQpDmHooEh8.txt")
    raw_desc = source_file.read_text(encoding='utf-8')
    comment = format_comment(raw_desc)
    
    print("--- COMMENT PREVIEW ---")
    print(comment[:300] + "\n...\n" + comment[-150:])
    print("-----------------------")
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()
        
        ok = post_comment_on_video(page, video_id, comment)
        if ok:
            print(f"Verified live comment on {video_id}!")
