import time, sys, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

vid = "Mata6vtnrjQ"
srt_file = os.path.abspath("production/subtitles/Mata6vtnrjQ.srt")
print(f"Uploading SRT: {srt_file}", flush=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    print(f"Current page URL: {page.url}", flush=True)
    
    # 1. Click Upload manual
    print("Clicking 'Upload manual' button...", flush=True)
    page.locator("#upload-default-language-button, ytcp-button:has-text('Upload manual')").first.click()
    time.sleep(2)
    
    page.screenshot(path="scratch/after_upload_manual_click.png")
    print("Saved scratch/after_upload_manual_click.png", flush=True)
    
    # 2. Wait for modal and click Continue with file chooser expectation
    print("Waiting for file chooser on 'Continue' click...", flush=True)
    with page.expect_file_chooser(timeout=10000) as fc_info:
        # Find Continue button inside the modal
        page.evaluate("""() => {
            let elms = Array.from(document.querySelectorAll('*'));
            for (let el of elms) {
                let t = (el.innerText || '').trim();
                if ((t === 'Continue' || t === 'CONTINUE') && (el.tagName === 'BUTTON' || el.tagName === 'YTCP-BUTTON')) {
                    el.click();
                    return true;
                }
            }
            return false;
        }""")
        
    fc = fc_info.value
    print("File chooser intercepted! Uploading SRT file...", flush=True)
    fc.set_files(srt_file)
    print("File chosen! Waiting 6s for subtitle editor to populate...", flush=True)
    time.sleep(6)
    
    page.screenshot(path="scratch/after_srt_file_set.png")
    print("Saved scratch/after_srt_file_set.png", flush=True)
    
    # 3. Click Publish
    print("Looking for 'Publish' button in editor...", flush=True)
    pub_clicked = page.evaluate("""() => {
        function findPublish(root) {
            let elms = Array.from(root.querySelectorAll('*'));
            for (let el of elms) {
                if (el.shadowRoot) {
                    let r = findPublish(el.shadowRoot);
                    if (r) return r;
                }
                let t = (el.innerText || '').trim();
                let aria = (el.getAttribute('aria-label') || '').trim();
                if ((t === 'Publish' || t === 'PUBLISH' || aria === 'Publish') && (el.tagName === 'BUTTON' || el.tagName === 'YTCP-BUTTON')) {
                    let rect = el.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) return el;
                }
            }
            return null;
        }
        let b = findPublish(document.body);
        if (b) {
            b.click();
            return true;
        }
        return false;
    }""")
    print(f"Publish button clicked: {pub_clicked}", flush=True)
    time.sleep(6)
    
    page.screenshot(path="scratch/after_publish_clicked.png")
    print("Saved scratch/after_publish_clicked.png", flush=True)

print("SRT upload and publish cycle finished!", flush=True)
