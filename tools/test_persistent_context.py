import sys
import os
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

user_data_dir = r"C:\Users\Shishyan\.antigravity_shishyan"

print(f"Testing launch_persistent_context on {user_data_dir}...", flush=True)

with sync_playwright() as p:
    try:
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            channel="chrome",
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        page = context.pages[0] if context.pages else context.new_page()
        
        print("Navigating to https://studio.youtube.com...", flush=True)
        page.goto("https://studio.youtube.com", wait_until="domcontentloaded")
        time.sleep(5)
        
        print(f"Current URL: {page.url}", flush=True)
        print(f"Page Title: {page.title()}", flush=True)
        
        page.screenshot(path="C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/persistent_context_studio.png")
        print("Screenshot saved to persistent_context_studio.png", flush=True)
        
        context.close()
        print("SUCCESS! Context closed cleanly.", flush=True)
    except Exception as e:
        print("Error launching persistent context:", e, flush=True)
