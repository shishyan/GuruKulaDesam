"""Test posting a comment on YouTube using Playwright connected to Chrome's CDP or profile.
"""
import sys
import json
import time
from playwright.sync_api import sync_playwright

CDP_URL = "http://127.0.0.1:9222"
TARGET_URL = "https://www.youtube.com/watch?v=yrmF7nfwnsQ"

with sync_playwright() as p:
    try:
        print(f"Connecting to CDP at {CDP_URL}...")
        browser = p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        
        # Check if YouTube tab already exists or open new page
        page = None
        for p_tab in context.pages:
            if "youtube.com" in p_tab.url:
                page = p_tab
                break
        
        if not page:
            print("Opening new tab for YouTube...")
            page = context.new_page()
            page.goto(TARGET_URL, wait_until='networkidle')
        else:
            print(f"Using existing tab: {page.url}")
            if "watch" not in page.url:
                page.goto(TARGET_URL, wait_until='networkidle')
        
        print("Page title:", page.title().encode('ascii', 'replace').decode())
        
        # Scroll down to ensure comments element is rendered
        for _ in range(3):
            page.evaluate("window.scrollBy(0, 500)")
            page.wait_for_timeout(1000)
            
        # Check for comment box
        simplebox = page.locator('#simplebox-placeholder, #placeholder-area, ytd-comment-simplebox-renderer')
        print("Simplebox count:", simplebox.count())
        if simplebox.count() > 0:
            print("Comment box is present in the browser DOM!")
        else:
            print("Comment box not found directly; checking if signed in...")
            avatar = page.locator('button#avatar-btn, ytd-topbar-menu-button-renderer img')
            print("Avatar elements found:", avatar.count())
            
    except Exception as e:
        print("Error during Playwright interaction:", e)
