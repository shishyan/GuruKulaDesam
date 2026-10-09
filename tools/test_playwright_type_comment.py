"""Tests clicking the comment box, typing a test lyric comment, and checking the submit button status.
"""
import sys
import time
from playwright.sync_api import sync_playwright

CDP_URL = "http://127.0.0.1:9222"
TARGET_URL = "https://www.youtube.com/watch?v=yrmF7nfwnsQ"

with sync_playwright() as p:
    try:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = None
        for p_tab in context.pages:
            if "youtube.com" in p_tab.url and "yrmF7nfwnsQ" in p_tab.url:
                page = p_tab
                break
        if not page:
            page = context.new_page()
            page.goto(TARGET_URL)
            
        print("Tab URL:", page.url)
        page.evaluate("window.scrollBy(0, 500)")
        page.wait_for_timeout(2000)
        
        # Click placeholder to focus comment box
        placeholder = page.locator('#placeholder-area, #simplebox-placeholder').first
        if placeholder.is_visible():
            print("Clicking placeholder area...")
            placeholder.click()
            page.wait_for_timeout(1000)
            
        # Check contenteditable input box
        input_box = page.locator('#contenteditable-root').first
        if input_box.is_visible():
            print("Contenteditable comment input is visible and active!")
            # Check comment submit button
            submit_btn = page.locator('#submit-button').first
            print("Submit button found:", submit_btn.is_visible())
        else:
            print("Input box not visible after click.")
            
    except Exception as e:
        print("Error:", e)
