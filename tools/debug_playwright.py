import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

print("Line 1: starting playwright...", flush=True)
p = sync_playwright().start()
print("Line 2: connecting over CDP...", flush=True)
try:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225', timeout=5000)
    print("Line 3: connected!", flush=True)
    for c in browser.contexts:
        print("Context pages:", len(c.pages))
    browser.close()
except Exception as e:
    print("Error connecting:", e)
finally:
    p.stop()
    print("Stopped playwright.", flush=True)
