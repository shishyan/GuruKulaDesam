import time, sys, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

vid = "Mata6vtnrjQ"
srt_file = os.path.abspath("production/subtitles/Mata6vtnrjQ.srt")
print(f"Target SRT: {srt_file}")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    print("Waiting 4s for page to stabilize...", flush=True)
    time.sleep(4)
    print("Current page:", page.url)
    
    # 1. Click Upload manual
    print("Clicking 'Upload manual'...", flush=True)
    clicked = page.evaluate("""() => {
        function findBtn(root) {
            let elms = Array.from(root.querySelectorAll('*'));
            for (let el of elms) {
                if (el.shadowRoot) {
                    let r = findBtn(el.shadowRoot);
                    if (r) return r;
                }
                let t = (el.innerText || '').trim();
                if ((t === 'Upload manual' || t === 'UPLOAD MANUAL') && (el.tagName === 'BUTTON' || el.tagName === 'YTCP-BUTTON')) {
                    return el;
                }
            }
            return null;
        }
        let b = findBtn(document.body);
        if (b) {
            b.click();
            return true;
        }
        return false;
    }""")
    print("Clicked 'Upload manual':", clicked)
    time.sleep(2)
    
    # 2. Wait for modal & Click Continue with file chooser
    print("Clicking 'Continue' with file chooser expectation...", flush=True)
    with page.expect_file_chooser(timeout=10000) as fc_info:
        cont_clicked = page.evaluate("""() => {
            function findContinue(root) {
                let elms = Array.from(root.querySelectorAll('*'));
                for (let el of elms) {
                    if (el.shadowRoot) {
                        let r = findContinue(el.shadowRoot);
                        if (r) return r;
                    }
                    let t = (el.innerText || '').trim();
                    if ((t === 'Continue' || t === 'CONTINUE') && (el.tagName === 'BUTTON' || el.tagName === 'YTCP-BUTTON')) {
                        return el;
                    }
                }
                return null;
            }
            let b = findContinue(document.body);
            if (b) {
                b.click();
                return true;
            }
            return false;
        }""")
        print("Clicked 'Continue':", cont_clicked)
        
    fc = fc_info.value
    print("File chooser caught! Setting files...", flush=True)
    fc.set_files(srt_file)
    print("Files set! Waiting 6s for subtitle editor DOM...", flush=True)
    time.sleep(6)
    
    page.screenshot(path="scratch/studio_in_editor.png")
    print("Saved scratch/studio_in_editor.png")
    
    # 3. Click Publish
    print("Looking for 'Publish' button...", flush=True)
    published = page.evaluate("""() => {
        function findPublish(root) {
            let elms = Array.from(root.querySelectorAll('*'));
            for (let el of elms) {
                if (el.shadowRoot) {
                    let r = findPublish(el.shadowRoot);
                    if (r) return r;
                }
                let t = (el.innerText || '').trim();
                if ((t === 'Publish' || t === 'PUBLISH') && (el.tagName === 'BUTTON' || el.tagName === 'YTCP-BUTTON')) {
                    let r = el.getBoundingClientRect();
                    if (r.width > 0 && r.height > 0) return el;
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
    print("Publish clicked:", published)
    
    time.sleep(6)
    page.screenshot(path="scratch/studio_after_publish.png")
    print("Saved scratch/studio_after_publish.png")
    print("Finished upload and publish workflow!")
