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
    page.wait_for_load_state('networkidle')
    time.sleep(3)

    print("Clicking Create button...")
    page.locator('#create-icon, [aria-label="Create"]').click()
    time.sleep(1)

    print("Clicking New playlist...")
    page.locator('text=New playlist').click()
    time.sleep(3)

    print("Waiting for modal...")
    page.screenshot(path=r'C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\modal_opened.png')

    # Fill Title
    print("Filling Title...")
    # Find active textboxes in dialog
    title_box = page.locator('#textbox').first
    title_box.click()
    page.keyboard.type('திருக்குறள் | Thirukkural — Audio Master Collection', delay=10)
    time.sleep(1)

    # Fill Description
    print("Filling Description...")
    desc_box = page.locator('#textbox').nth(1)
    desc_box.click()
    page.keyboard.type('Official Thirukkural Audio Master Collection by Guru Kula Desam (@gurukuladesam). All released audio chapters in sequential order (1 to 133).', delay=10)
    time.sleep(1)

    page.screenshot(path=r'C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\modal_typed.png')

    print("Clicking Create button...")
    create_btn = page.locator('#create-button').last
    create_btn.click()
    time.sleep(6)

    page.screenshot(path=r'C:\Users\Shishyan\.gemini\antigravity\brain\80e87c4b-c142-450e-bc23-6a6b12ae1e34\after_create_click.png')

    # Refresh playlists list or inspect current URL
    print("Current URL:", page.url)
    page.goto('https://studio.youtube.com/channel/UCPqB1A_WzpLJec6q69BOO3Q/content/playlists')
    time.sleep(4)

    new_pls = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a[href*="/playlist/"]')).map(a => ({
            text: a.innerText.trim(),
            href: a.href
        })).filter(x => x.text && x.text.includes('Audio Master'));
    }''')
    print("New playlist found:", new_pls)

    if new_pls:
        with open('production/new_audio_playlist.json', 'w', encoding='utf-8') as f:
            json.dump(new_pls[0], f, indent=2, ensure_ascii=False)

    page.close()
