import time, sys, pathlib, json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path('.')

def upload_srt_browser(vid):
    srt_path = str((ROOT / f'production/subtitles/{vid}.srt').resolve())
    print(f"\n=======================================================")
    print(f"Browser Upload for {vid}")
    print(f"SRT: {srt_path}")
    print(f"=======================================================")
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
        page = browser.contexts[0].pages[0]
        
        target_url = f"https://studio.youtube.com/video/{vid}/translations"
        if page.url != target_url:
            print(f"Navigating to {target_url}...")
            page.goto(target_url)
            page.wait_for_load_state('domcontentloaded')
            time.sleep(3)
            
        print("Page ready. Checking for upload buttons...")
        
        # Look for the 'Upload manual' button or 'Edit subtitles' button or 'ADD' button in Translations table
        # Let's inspect buttons inside shadow dom
        click_info = page.evaluate("""() => {
            function findElements(root) {
                let found = [];
                let elms = Array.from(root.querySelectorAll('*'));
                for (let el of elms) {
                    if (el.shadowRoot) found = found.concat(findElements(el.shadowRoot));
                    let txt = (el.innerText || '').trim();
                    if (txt === 'Upload manual' || txt === 'UPLOAD MANUAL' || txt === 'Add' || txt === 'ADD') {
                        let r = el.getBoundingClientRect();
                        if (r.width > 0 && r.height > 0) {
                            found.push({tag: el.tagName, id: el.id, text: txt, x: r.x + r.width/2, y: r.y + r.height/2});
                        }
                    }
                }
                return found;
            }
            return findElements(document.body);
        }""")
        print("Found matching elements:", click_info)
        
        if not click_info:
            print("No button found! Taking screenshot...")
            page.screenshot(path=f"scratch/debug_{vid}.png")
            return False
            
        # Click the first matching element
        btn = click_info[0]
        print(f"Clicking '{btn['text']}' at ({btn['x']}, {btn['y']})...")
        
        # Set up file chooser expectation
        try:
            with page.expect_file_chooser(timeout=5000) as fc_info:
                page.mouse.click(btn['x'], btn['y'])
                time.sleep(1)
                
                # Check if a modal with "Continue" or "With timing" appeared
                modal_btns = page.evaluate("""() => {
                    function findButtons(root) {
                        let res = [];
                        let elms = Array.from(root.querySelectorAll('*'));
                        for (let el of elms) {
                            if (el.shadowRoot) res = res.concat(findButtons(el.shadowRoot));
                            let txt = (el.innerText || '').trim();
                            if (txt === 'Continue' || txt === 'CONTINUE') {
                                let r = el.getBoundingClientRect();
                                if (r.width > 0 && r.height > 0) {
                                    res.push({tag: el.tagName, text: txt, x: r.x + r.width/2, y: r.y + r.height/2});
                                }
                            }
                        }
                        return res;
                    }
                    return findButtons(document.body);
                }""")
                print("Modal buttons:", modal_btns)
                if modal_btns:
                    mb = modal_btns[0]
                    print(f"Clicking Continue at ({mb['x']}, {mb['y']})...")
                    page.mouse.click(mb['x'], mb['y'])
                    
            file_chooser = fc_info.value
            print(f"Setting file to: {srt_path}")
            file_chooser.set_files(srt_path)
            time.sleep(3)
            
            # Now click Publish inside the editor
            pub_btn = page.evaluate("""() => {
                function findPublish(root) {
                    let res = [];
                    let elms = Array.from(root.querySelectorAll('*'));
                    for (let el of elms) {
                        if (el.shadowRoot) res = res.concat(findPublish(el.shadowRoot));
                        let txt = (el.innerText || '').trim();
                        if (txt === 'Publish' || txt === 'PUBLISH') {
                            let r = el.getBoundingClientRect();
                            if (r.width > 0 && r.height > 0) {
                                res.push({tag: el.tagName, text: txt, x: r.x + r.width/2, y: r.y + r.height/2});
                            }
                        }
                    }
                    return res;
                }
                return findPublish(document.body);
            }""")
            print("Publish buttons:", pub_btn)
            if pub_btn:
                pb = pub_btn[0]
                print(f"Clicking Publish at ({pb['x']}, {pb['y']})...")
                page.mouse.click(pb['x'], pb['y'])
                time.sleep(3)
                print("PUBLISHED SUCCESSFULLY!")
                page.screenshot(path=f"scratch/published_{vid}.png")
                return True
        except Exception as e:
            print("File chooser / modal flow:", e)
            page.screenshot(path=f"scratch/error_{vid}.png")
            return False

if __name__ == '__main__':
    upload_srt_browser('IHMZsM7LJf8')
