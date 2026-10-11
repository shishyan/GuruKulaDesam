import os
import time
from playwright.sync_api import sync_playwright

vid = "31xVgvxoiUA"
srt_path = os.path.abspath(f"production/subtitles/{vid}.srt")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    print(f"Navigating to video {vid} translations...")
    page.goto(f"https://studio.youtube.com/video/{vid}/translations", wait_until="domcontentloaded")
    time.sleep(3)
    
    print("Looking for Upload manual button...")
    upload_btn = page.locator("#upload-default-language-button button")
    if not upload_btn.is_visible():
        upload_btn = page.get_by_text("Upload manual").first
        
    print(f"Clicking Upload manual (visible: {upload_btn.is_visible()})...")
    upload_btn.click()
    time.sleep(2)
    
    print("Looking for Continue button in modal...")
    continue_btn = page.get_by_role("button", name="Continue")
    if not continue_btn.is_visible():
        continue_btn = page.locator("text=Continue").first
        
    print(f"Continue button visible: {continue_btn.is_visible()}")
    
    print("Setting up expect_file_chooser and clicking Continue...")
    with page.expect_file_chooser(timeout=10000) as fc_info:
        continue_btn.click()
        
    file_chooser = fc_info.value
    print(f"File chooser intercepted successfully! Setting files: {srt_path}")
    file_chooser.set_files(srt_path)
    print("File set! Waiting for Subtitle Editor to process...")
    time.sleep(5)
    
    print("Checking for Publish button...")
    publish_btn = page.get_by_role("button", name="Publish")
    if not publish_btn.is_visible():
        publish_btn = page.locator("#publish-button, text=Publish").first
        
    print(f"Publish button visible: {publish_btn.is_visible()}")
    if publish_btn.is_visible():
        print("Clicking Publish!")
        publish_btn.click()
        time.sleep(3)
        print("SUCCESS! Subtitles published!")
        
    page.screenshot(path=f"C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/final_result_{vid}.png")
