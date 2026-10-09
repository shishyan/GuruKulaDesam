"""Test Playwright with existing user profile to interact with the YouTube comment box.
"""
import sys
import os
import pathlib
from playwright.sync_api import sync_playwright

LOCALAPPDATA = os.environ['LOCALAPPDATA']
EDGE_USER_DATA = str(pathlib.Path(LOCALAPPDATA) / 'Microsoft' / 'Edge' / 'User Data')

VIDEO_ID = 'yrmF7nfwnsQ'
URL = f'https://www.youtube.com/watch?v={VIDEO_ID}'

print(f"Opening {URL} using Edge with user profile...")

with sync_playwright() as p:
    try:
        # Launch persistent context with msedge channel
        context = p.chromium.launch_persistent_context(
            user_data_dir=EDGE_USER_DATA,
            channel='msedge',
            headless=True,
            args=['--no-first-run', '--no-default-browser-check'],
            viewport={'width': 1280, 'height': 900}
        )
        page = context.new_page()
        page.goto(URL, wait_until='networkidle')
        print("Page title:", page.title())
        
        # Scroll down to load comments section
        page.evaluate("window.scrollBy(0, 600)")
        page.wait_for_timeout(3000)
        
        # Look for comment input or simplebox
        comment_box = page.locator('#placeholder-area, #contenteditable-root, ytd-comment-simplebox-renderer')
        count = comment_box.count()
        print(f"Found {count} comment box elements on page.")
        
        context.close()
    except Exception as e:
        print("Error:", e)
