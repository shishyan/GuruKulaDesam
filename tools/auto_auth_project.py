import sys
import os
import json
import time
import threading
from playwright.sync_api import sync_playwright
from google_auth_oauthlib.flow import InstalledAppFlow

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SECRET_FILE = "client_secret_299653451385-cmaaq0h7i1ptr6jdfv3865g82jdk21ah.apps.googleusercontent.com.json"
SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtubepartner'
]

flow = InstalledAppFlow.from_client_secrets_file(SECRET_FILE, SCOPES)
flow.redirect_uri = 'http://localhost:8088/'
auth_url, _ = flow.authorization_url(prompt='consent select_account', access_type='offline')

print(f"Generated Auth URL:\n{auth_url}\n", flush=True)

creds_result = []
def run_flow():
    try:
        c = flow.run_local_server(port=8088, open_browser=False)
        creds_result.append(c)
        print("FLOW COMPLETE!", flush=True)
    except Exception as e:
        print("Flow error:", e, flush=True)

t = threading.Thread(target=run_flow, daemon=True)
t.start()
time.sleep(2)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    print("Navigating to OAuth URL...", flush=True)
    page.goto(auth_url, wait_until="domcontentloaded")
    time.sleep(4)
    
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/oauth_screen_1.png")
    
    # 1. Select account
    account_selector = page.locator("[data-identifier='shishyan@gmail.com'], div:has-text('shishyan@gmail.com'), div:has-text('Guru Kula Desam')")
    if account_selector.count() > 0:
        print("Clicking shishyan account...", flush=True)
        account_selector.first.click()
        time.sleep(3)
        page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/oauth_screen_2.png")
        
    # 2. Check for "Advanced" / "Go to ... (unsafe)"
    adv = page.locator("text='Advanced', text='Show advanced', #advancedButton")
    if adv.count() > 0 and adv.first.is_visible():
        print("Clicking Advanced...", flush=True)
        adv.first.click()
        time.sleep(1)
        unsafe = page.locator("a:has-text('Go to'), #proceed-link")
        if unsafe.count() > 0 and unsafe.first.is_visible():
            print("Clicking proceed link...", flush=True)
            unsafe.first.click()
            time.sleep(2)
            
    # 3. Check for checkboxes (Select all)
    cb = page.locator("input[type='checkbox']")
    for i in range(cb.count()):
        try:
            if not cb.nth(i).is_checked():
                cb.nth(i).check()
        except Exception: pass
        
    # 4. Click Continue / Allow
    for name in ["Continue", "Allow", "Confirm"]:
        btn = page.get_by_role("button", name=name)
        if btn.count() > 0 and btn.first.is_visible():
            print(f"Clicking button: {name}...", flush=True)
            btn.first.click()
            time.sleep(3)
            
    page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/oauth_screen_final.png")

t.join(timeout=10)
if creds_result:
    new_creds = creds_result[0]
    out_path = "data/credentials/token_gurukuladesam-2.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(new_creds.to_json())
    print(f"\nSUCCESS! Fresh credentials saved to {out_path}", flush=True)
else:
    print("\nCould not complete OAuth flow within timeout.", flush=True)
