import time, sys, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

vid = "Mata6vtnrjQ"
srt_file = os.path.abspath("production/subtitles/Mata6vtnrjQ.srt")
print(f"Target SRT file: {srt_file}")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    print("Clicking 'Continue' with file chooser expectation...", flush=True)
    with page.expect_file_chooser(timeout=10000) as fc_info:
        # Click Continue button
        page.evaluate("""() => {
            function findContinue(root) {
                let elms = Array.from(root.querySelectorAll('*'));
                for (let el of elms) {
                    if (el.shadowRoot) {
                        let res = findContinue(el.shadowRoot);
                        if (res) return res;
                    }
                    if ((el.innerText || '').trim() === 'Continue' && (el.tagName === 'BUTTON' || el.tagName === 'YTCP-BUTTON')) {
                        return el;
                    }
                }
                return null;
            }
            let btn = findContinue(document.body);
            if (btn) btn.click();
            else console.log('Continue button not found!');
        }""")
        
    file_chooser = fc_info.value
    print(f"File chooser opened! Uploading {srt_file}...", flush=True)
    file_chooser.set_files(srt_file)
    print("File set successfully! Waiting 5s for Studio subtitle editor to load...", flush=True)
    time.sleep(5)
    
    screenshot_editor = "scratch/studio_subtitle_editor_loaded.png"
    page.screenshot(path=screenshot_editor)
    print(f"Saved editor screenshot to {screenshot_editor}", flush=True)
    
    # Inspect editor buttons (Publish, Save draft, etc.)
    editor_btns = page.evaluate("""() => {
        function findButtons(root) {
            let res = [];
            let elms = Array.from(root.querySelectorAll('*'));
            for (let el of elms) {
                if (el.shadowRoot) res = res.concat(findButtons(el.shadowRoot));
                let txt = (el.innerText || '').trim();
                if (txt === 'Publish' || txt === 'PUBLISH' || txt === 'Save' || txt === 'SAVE' || txt === 'Done' || txt === 'DONE') {
                    let r = el.getBoundingClientRect();
                    if (r.width > 0 && r.height > 0) {
                        res.push({tag: el.tagName, id: el.id, text: txt, x: r.x + r.width/2, y: r.y + r.height/2});
                    }
                }
            }
            return res;
        }
        return findButtons(document.body);
    }""")
    print("Editor action buttons found:", editor_btns, flush=True)
    
    # If Publish button found, click it!
    pub_btn = next((b for b in editor_btns if 'PUBLISH' in b['text'].upper()), None)
    if pub_btn:
        print(f"Clicking '{pub_btn['text']}' at ({pub_btn['x']}, {pub_btn['y']})...", flush=True)
        page.mouse.click(pub_btn['x'], pub_btn['y'])
        print("Waiting 5s for publish to complete...", flush=True)
        time.sleep(5)
        
        final_ss = "scratch/studio_subtitles_published.png"
        page.screenshot(path=final_ss)
        print(f"Saved published screenshot to {final_ss}", flush=True)
        print("SUCCESS! Subtitles published live on YouTube Studio!", flush=True)
    else:
        print("Publish button not found automatically. Check editor screenshot.", flush=True)
