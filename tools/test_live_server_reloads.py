import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def test_refresh_loop():
    print("=== Testing for Live Server Refresh Loop ===")
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True, channel="msedge")
        except Exception:
            browser = p.chromium.launch(headless=True, channel="chrome")
            
        context = browser.new_context()
        page = context.new_page()

        # Try connecting to port 5500
        urls_to_test = [
            "http://127.0.0.1:5500/Gurukuladesam/index.html",
            "http://127.0.0.1:5500/index.html",
            "http://127.0.0.1:8000/index.html"
        ]

        working_url = None
        for u in urls_to_test:
            try:
                resp = page.goto(u, timeout=4000)
                if resp and resp.status == 200:
                    working_url = u
                    print(f"Successfully reached: {working_url}")
                    break
            except Exception as e:
                print(f"Could not reach {u}: {e}")

        if not working_url:
            print("[ERROR] Could not connect to any test server.")
            browser.close()
            return False

        # Monitor navigations over 15 seconds
        navigation_count = 0
        ws_messages = []

        def on_nav(frame):
            nonlocal navigation_count
            if frame == page.main_frame:
                navigation_count += 1
                print(f"  [Frame Navigation Detected #{navigation_count}] url: {frame.url}")

        page.on("framenavigated", on_nav)

        def on_ws(ws):
            print(f"  [WebSocket Connected] {ws.url}")
            ws.on("framereceived", lambda payload: ws_messages.append(payload))

        page.on("websocket", on_ws)

        # Set a token in sessionStorage/window to detect reloads
        page.evaluate("window.__test_token = 'INITIAL_LOAD_OK'")

        print(f"\nMonitoring '{working_url}' for 20 seconds for unprompted reloads...")
        
        # Reset count for initial load
        navigation_count = 0

        # Wait in increments of 1 second for 20 seconds
        for s in range(20):
            page.wait_for_timeout(1000)
            token = page.evaluate("window.__test_token")
            if token != 'INITIAL_LOAD_OK':
                print(f"  [ALERT] window.__test_token was wiped at second {s+1}! Page reloaded.")
            print(f"  T+{s+1}s: Active, Navigations: {navigation_count}, Token: {token}")

        token_final = page.evaluate("window.__test_token")
        browser.close()

        print("\n--- RESULTS ---")
        print(f"Total Navigations in 20 seconds: {navigation_count}")
        print(f"WebSocket Messages Received: {len(ws_messages)}")
        for m in ws_messages[:10]:
            print(f"  WS msg: {m}")
            
        if navigation_count == 0 and token_final == 'INITIAL_LOAD_OK':
            print("✓ ZERO RELOADS OCCURRED! Refresh loop is completely stopped.")
            return True
        else:
            print(f"✗ RELOADS DETECTED ({navigation_count} reloads). Refresh loop is still active!")
            return False

if __name__ == "__main__":
    success = test_refresh_loop()
    sys.exit(0 if success else 1)
