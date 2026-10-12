import time
from pathlib import Path
from playwright.sync_api import sync_playwright

dest_dir = Path("production/google_flow_renders/--4jzoezBW8")
dest_dir.mkdir(parents=True, exist_ok=True)
dest_clip = dest_dir / "scene_01.mp4"

print("Watching Google Flow generation on port 9222...")
start_time = time.time()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    ctx = browser.contexts[0]
    page = [pg for pg in ctx.pages if 'flow.google.com/project' in pg.url][0]

    for poll in range(40): # up to ~3 minutes
        time.sleep(5)
        elapsed = int(time.time() - start_time)
        
        # Check Stop button
        stop_btn = page.locator('button:has-text("Stop"), [role="button"]:has-text("Stop")').first
        is_generating = stop_btn.is_visible()
        
        # Check for error or credit exhaustion
        body_text = page.locator('body').inner_text()
        has_error = "reached your credit limit" in body_text or "reached your generation quota" in body_text
        
        # Check video elements
        videos = page.locator('video').all()
        
        print(f"[{elapsed}s] Generating: {is_generating} | Error: {has_error} | Videos: {len(videos)}")
        
        if has_error:
            print("Alert: Credit or quota limit reported!")
            break
            
        if not is_generating and elapsed > 20:
            print("Generation finished! Checking media card...")
            page.screenshot(path='production/flow_scene01_completed.png')
            break
            
    browser.close()
