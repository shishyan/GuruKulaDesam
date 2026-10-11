import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    # Use existing page if dialog is already open, or navigate
    page = ctx.pages[0]

    # Check if dialog is open
    is_dialog_open = page.evaluate('''() => {
        return !!document.querySelector('ytcp-playlist-dialog, tp-yt-paper-dialog');
    }''')
    print("Is dialog currently open?", is_dialog_open)

    if not is_dialog_open:
        page.goto('https://studio.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q/content/playlists')
        time.sleep(5)
        # click create
        page.evaluate('''() => {
            const btn = document.querySelector('#create-icon, [aria-label="Create"]');
            if (btn) btn.click();
        }''')
        time.sleep(2)
        page.evaluate('''() => {
            const items = Array.from(document.querySelectorAll('tp-yt-paper-item, [role="menuitem"]'));
            for (const item of items) {
                if (item.innerText && item.innerText.includes('playlist')) {
                    item.click();
                    break;
                }
            }
        }''')
        time.sleep(3)

    # Let's inspect the input fields inside ytcp-playlist-dialog
    input_details = page.evaluate('''() => {
        const dialog = document.querySelector('ytcp-playlist-dialog');
        if (!dialog) return { error: 'No dialog found' };
        
        const inputs = Array.from(dialog.querySelectorAll('input, textarea, #textbox, [contenteditable]')).map(el => ({
            tag: el.tagName,
            id: el.id,
            placeholder: el.getAttribute('placeholder'),
            ariaLabel: el.getAttribute('aria-label'),
            className: el.className
        }));
        
        const buttons = Array.from(dialog.querySelectorAll('ytcp-button, button')).map(b => ({
            text: b.innerText.trim(),
            id: b.id,
            disabled: b.hasAttribute('disabled')
        }));
        
        return { inputs, buttons };
    }''')
    print("Dialog input details:", json.dumps(input_details, indent=2))

    # Now let's fill the title and description using Playwright's locator/fill or JS
    # Title is typically: ytcp-playlist-dialog #input-1 or #textbox
    page.evaluate('''() => {
        const dialog = document.querySelector('ytcp-playlist-dialog');
        // The first contenteditable or textarea/input is Title
        const textboxes = dialog.querySelectorAll('#textbox, textarea, [contenteditable="true"]');
        if (textboxes.length > 0) {
            textboxes[0].focus();
            textboxes[0].innerText = 'திருக்குறள் | Thirukkural — Audio Master Collection';
            textboxes[0].dispatchEvent(new Event('input', { bubbles: true }));
        }
        if (textboxes.length > 1) {
            textboxes[1].focus();
            textboxes[1].innerText = 'Official Thirukkural Audio Master Collection by Guru Kula Desam (@gurukuladesam). All released audio chapters in sequential order (1 to 133).';
            textboxes[1].dispatchEvent(new Event('input', { bubbles: true }));
        }
    }''')
    time.sleep(2)

    page.screenshot(path=r'C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\playlist_dialog_filled.png')

    # Now click create button
    create_res = page.evaluate('''() => {
        const dialog = document.querySelector('ytcp-playlist-dialog');
        const createBtn = dialog.querySelector('#create-button:not([disabled]), ytcp-button#create-button');
        if (createBtn) {
            createBtn.click();
            return { clicked: true, text: createBtn.innerText };
        }
        return { clicked: false };
    }''')
    print("Click Create button result:", create_res)

    time.sleep(5)
    page.screenshot(path=r'C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\playlist_after_create.png')

    # Now let's see if the new playlist is listed in playlists page
    print("Current page URL:", page.url)
    
    # Check playlists
    playlists_after = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a[href*="/playlist/"]')).map(a => ({
            text: a.innerText.trim(),
            href: a.href
        })).filter(x => x.text && x.text.includes('Audio Master'));
    }''')
    print("Found new playlist:", playlists_after)
