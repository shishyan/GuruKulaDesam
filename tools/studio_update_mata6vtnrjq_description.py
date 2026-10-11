import sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

vid = "Mata6vtnrjQ"
url = f"https://studio.youtube.com/video/{vid}/edit"

new_chapter_block = """⏱ Timestamps / Musical Chapters (அமைப்பும் நேரமும்):
00:00 - குறள் 610: மடியிலா மன்னவன் எய்தும் (தொடக்கப் பல்லவி)
00:30 - குறள் 601: குடியென்னும் குன்றா விளக்கம்
01:00 - குறள் 610: அடியளந்தான் தாஅய தெல்லாம் (பல்லவி)
01:31 - குறள் 609: குடியாண்மை யுள்வந்த குற்றம்
02:01 - குறள் 602: மடியை மடியா ஒழுகல்
02:16 - குறள் 604: குடிமடிந்து குற்றம் பெருகும்
02:31 - குறள் 610: மடியிலா மன்னவன் எய்தும் (இடைக்காலப் பல்லவி)
03:01 - குறள் 605: நெடுநீர் மறவி மடிதுயில் நான்கும்
03:12 - குறள் 607: இடிபுரிந்து எள்ளுஞ்சொல் & குறள் 603: மடிமடிக் கொண்டொழுகும்
03:24 - குறள் 608: மடிமை குடிமைக்கண் தங்கின்தன்
03:36 - குறள் 606: படியுடையார் பற்றமைந்தக் கண்ணும்
03:44 - குறள் 610: அடியளந்தான் தாஅய தெல்லாம் ஒருங்கு (நிறைவுப் பல்லவி)"""

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    page = browser.contexts[0].pages[0]
    
    print("Waiting for #description-textarea selector...", flush=True)
    page.wait_for_selector('#description-textarea', timeout=30000)
    print("Selector found! Page is stable.", flush=True)
        
    existing_desc = page.evaluate('''() => {
        const descBox = document.querySelector('#description-textarea #textbox, [aria-label*="Description"] #textbox, #description #textbox');
        return descBox ? descBox.innerText : null;
    }''')
    
    if not existing_desc:
        print("ERROR: Description box not found!", flush=True)
        sys.exit(1)
        
    print(f"Existing description found ({len(existing_desc)} chars). Updating chapters...", flush=True)
    
    lines = existing_desc.splitlines()
    new_lines = []
    skip = False
    replaced = False
    
    for line in lines:
        if "⏱ Timestamps" in line:
            new_lines.append(new_chapter_block)
            skip = True
            replaced = True
        elif skip and ("====" in line or "குறள் 601:" in line or "04:03" in line):
            if "04:03" in line:
                continue
            skip = False
            new_lines.append(line)
        elif not skip:
            new_lines.append(line)
            
    if not replaced:
        print("Warning: Chapter block not found, appending to top of description")
        new_desc = new_chapter_block + "\n\n" + existing_desc
    else:
        new_desc = "\n".join(new_lines)
        
    # Inject into description box
    res = page.evaluate('''(newText) => {
        const descBox = document.querySelector('#description-textarea #textbox, [aria-label*="Description"] #textbox, #description #textbox');
        if (!descBox) return { success: false, error: 'no desc box' };
        
        descBox.focus();
        document.execCommand('selectAll', false, null);
        document.execCommand('insertText', false, newText);
        
        descBox.dispatchEvent(new Event('input', { bubbles: true }));
        descBox.dispatchEvent(new Event('change', { bubbles: true }));
        
        const saveBtn = document.querySelector('#save-button, ytcp-button#save-button');
        return {
            success: true,
            newLen: descBox.innerText.length,
            saveBtnDisabled: saveBtn ? saveBtn.getAttribute('disabled') : 'no button'
        };
    }''', new_desc)
    print("Injected new description:", res, flush=True)
    time.sleep(2)
    
    # Click Save
    save_res = page.evaluate('''() => {
        const saveBtn = document.querySelector('#save-button, ytcp-button#save-button');
        if (saveBtn && !saveBtn.hasAttribute('disabled') && saveBtn.getAttribute('aria-disabled') !== 'true') {
            saveBtn.click();
            return { clicked: true };
        }
        return { clicked: false, attr: saveBtn ? saveBtn.getAttribute('disabled') : 'none' };
    }''')
    print("Save button clicked:", save_res, flush=True)
    time.sleep(4)
    
    ss_path = "scratch/studio_after_save_mata6vtnrjq.png"
    page.screenshot(path=ss_path)
    print(f"Saved confirmation screenshot to {ss_path}", flush=True)
    print("Description update finished successfully!", flush=True)
