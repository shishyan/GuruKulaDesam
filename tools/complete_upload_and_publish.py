import time, sys, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

vid = "Mata6vtnrjQ"
srt_file = os.path.abspath("production/subtitles/Mata6vtnrjQ.srt")
print(f"Target SRT: {srt_file}", flush=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    print('Current URL:', page.url, flush=True)
    
    # Click Continue with expect_file_chooser
    print("Intercepting file chooser on Continue click...", flush=True)
    with page.expect_file_chooser(timeout=10000) as fc_info:
        clicked = page.evaluate("""() => {
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
        print(f"Clicked Continue: {clicked}", flush=True)
        
    fc = fc_info.value
    print("File chooser intercepted! Setting SRT file...", flush=True)
    fc.set_files(srt_file)
    print("SRT file set! Waiting 7s for editor to load...", flush=True)
    time.sleep(7)
    
    os.makedirs("scratch", exist_ok=True)
    page.screenshot(path="scratch/after_srt_loaded.png")
    print("Saved scratch/after_srt_loaded.png", flush=True)
    
    # Find and click Publish button
    print("Finding and clicking Publish button...", flush=True)
    pub_res = page.evaluate("""() => {
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
                    if (rect.width > 0 && rect.height > 0 && !el.hasAttribute('disabled')) {
                        el.click();
                        return { clicked: true, tag: el.tagName, id: el.id, text: t };
                    }
                }
            }
            return null;
        }
        return findPublish(document.body);
    }""")
    print("Publish click result:", pub_res, flush=True)
    
    time.sleep(6)
    page.screenshot(path="scratch/after_publish_confirmed.png")
    print("Saved scratch/after_publish_confirmed.png", flush=True)
    print("Upload and publish workflow completed successfully!", flush=True)
