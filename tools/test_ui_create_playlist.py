import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.new_page()

    print("Navigating to https://studio.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q/content/playlists ...")
    page.goto('https://studio.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q/content/playlists')
    time.sleep(5)

    # Click Create button
    print("Clicking Create button...")
    page.evaluate('''() => {
        const createBtn = document.querySelector('#create-icon, [aria-label="Create"], ytcp-button[id*="create"]');
        if (createBtn) createBtn.click();
    }''')
    time.sleep(2)

    # Check menu items
    menu_items = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('tp-yt-paper-item, ytcp-text-menu [role="menuitem"], tp-yt-paper-listbox [role="option"]')).map(el => ({
            text: el.innerText.trim(),
            id: el.id
        }));
    }''')
    print("Menu items:", menu_items)

    # Click "New playlist"
    clicked_np = page.evaluate('''() => {
        const items = Array.from(document.querySelectorAll('tp-yt-paper-item, [role="menuitem"]'));
        for (const item of items) {
            if (item.innerText && item.innerText.includes('playlist')) {
                item.click();
                return { clicked: true, text: item.innerText };
            }
        }
        return { clicked: false };
    }''')
    print("Clicked new playlist:", clicked_np)
    time.sleep(3)

    # Take screenshot of dialog
    page.screenshot(path=r'C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\create_playlist_dialog.png')

    # Fill dialog title & description
    fill_res = page.evaluate('''() => {
        const titleInput = document.querySelector('ytcp-playlist-dialog #textbox, ytcp-playlist-dialog input, [aria-label="Title (required)"], [aria-label*="Title"]');
        const descInput = document.querySelector('ytcp-playlist-dialog #description-textarea, [aria-label="Description"], [aria-label*="Description"]');
        const createBtn = document.querySelector('ytcp-playlist-dialog #create-button, [aria-label="Create"]');
        
        return {
            titleFound: !!titleInput,
            descFound: !!descInput,
            createBtnFound: !!createBtn,
            dialogSnippet: (document.querySelector('ytcp-playlist-dialog, tp-yt-paper-dialog')?.innerText || '').replace(/\\n+/g, ' ')
        };
    }''')
    print("Fill dialog status:", fill_res)

    page.close()
