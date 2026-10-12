import sys
from playwright.sync_api import sync_playwright

def test():
    print("Testing Playwright connect_over_cdp to port 9225...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9225", timeout=10000)
            print("Connected! Contexts:", len(browser.contexts))
            for ctx in browser.contexts:
                print("Pages in context:", len(ctx.pages))
                for page in ctx.pages:
                    print("  Page:", page.title(), "| URL:", page.url)
            browser.close()
            print("Successfully closed CDP connection.")
    except Exception as e:
        print("Playwright CDP connect error:", e)

if __name__ == "__main__":
    test()
