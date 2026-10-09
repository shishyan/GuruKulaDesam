import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_drawer_tests():
    print("=== Testing Ashram Contextual Drawer & Modal System ===")
    errors = []
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True, channel="msedge")
        except Exception:
            browser = p.chromium.launch(headless=True, channel="chrome")
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        page.on("pageerror", lambda err: errors.append(f"PageError: {err}"))
        page.on("console", lambda msg: errors.append(f"Console: {msg.text}") if msg.type == "error" else None)

        url = "http://127.0.0.1:8000/index.html"
        print(f"Loading {url}...")
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(1000)

        # 1. Test Stage 1 Drawer
        print("\n[Test 1] Testing Stage 1 (Primary) Contextual Drawer...")
        # Scroll down to stages section
        stages_section = page.locator("#stagesSection")
        stages_section.scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        
        scroll_before = page.evaluate("window.scrollY")
        print(f"Scroll Y before drawer trigger: {scroll_before}px")

        # Click the Primary Stage Details button
        stage1_btn = page.locator("button[onclick*=\"openStageDrawer('primary')\"]")
        stage1_btn.click()
        page.wait_for_timeout(500)

        # Verify drawer is active
        drawer = page.locator("#ashramDrawerShell")
        assert drawer.is_visible(), "Drawer shell should be visible"
        assert "active" in (drawer.get_attribute("class") or ""), "Drawer shell must have active class"

        # Verify content
        drawer_text = drawer.inner_text()
        assert "பாலப் பருவம்" in drawer_text, "Drawer title must contain 'பாலப் பருவம்'"
        assert "நற்செயல்" in drawer_text, "Drawer must list 'நற்செயல்'"
        assert "தரம் 1" in drawer_text, "Drawer must have link to 'தரம் 1'"
        print("  ✓ Drawer opened with correct Stage 1 title, books, and grade pills.")

        # Verify body has drawer-open class
        body_class = page.evaluate("document.body.className")
        assert "drawer-open" in body_class, "Body should have 'drawer-open' class"
        print("  ✓ Body overflow locked via 'drawer-open' class.")

        # Close via Close button (X)
        close_btn = drawer.locator(".ashram-drawer-close-btn")
        close_btn.click()
        page.wait_for_timeout(400)

        assert "active" not in (drawer.get_attribute("class") or ""), "Drawer shell should not be active after close"
        scroll_after = page.evaluate("window.scrollY")
        print(f"Scroll Y after drawer close: {scroll_after}px")
        assert abs(scroll_after - scroll_before) < 10, f"Scroll position must be preserved! Before: {scroll_before}, After: {scroll_after}"
        print("  ✓ Context strictly retained! Scroll position remained unchanged.")

        # 2. Test Visual Card Drawer (Tapovanam)
        print("\n[Test 2] Testing Visual Card Drawer (Tapovanam)...")
        visual_btn = page.locator("button[onclick*=\"openVisualDrawer('tapovanam')\"]")
        visual_btn.scroll_into_view_if_needed()
        visual_btn.click()
        page.wait_for_timeout(400)

        drawer_text = drawer.inner_text()
        assert "ஆலமர வித்யாபீடம்" in drawer_text, "Drawer should have Tapovanam info"
        print("  ✓ Tapovanam visual drawer opened properly.")

        # Close via Escape key
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)
        assert "active" not in (drawer.get_attribute("class") or ""), "Drawer must close on Escape key"
        print("  ✓ Drawer closed via Escape key.")

        # 3. Test Pillar Drawer (Classroom / School)
        print("\n[Test 3] Testing Core Action Pillar Drawer (School)...")
        pillar_btn = page.locator("button[onclick*=\"openPillarDrawer('school')\"]")
        pillar_btn.scroll_into_view_if_needed()
        pillar_btn.click()
        page.wait_for_timeout(400)

        drawer_text = drawer.inner_text()
        assert "வித்யா குடீரம்" in drawer_text, "Drawer should have School pillar info"
        print("  ✓ School pillar drawer opened properly.")

        # Close via Backdrop click
        backdrop = page.locator("#ashramDrawerBackdrop")
        # Click on the left side of backdrop (outside the drawer)
        backdrop.click(position={"x": 50, "y": 200})
        page.wait_for_timeout(400)
        assert "active" not in (drawer.get_attribute("class") or ""), "Drawer must close on backdrop click"
        print("  ✓ Drawer closed via backdrop click.")

        # 4. Mobile Viewport Test (Bottom-sheet drawer)
        print("\n[Test 4] Testing Mobile Viewport (Bottom-sheet drawer)...")
        page.set_viewport_size({"width": 375, "height": 667})
        page.wait_for_timeout(300)

        stage2_btn = page.locator("button[onclick*=\"openStageDrawer('middle')\"]")
        stage2_btn.scroll_into_view_if_needed()
        stage2_btn.click()
        page.wait_for_timeout(400)

        drawer_text = drawer.inner_text()
        assert "இளம் பருவம்" in drawer_text, "Mobile drawer should open for Stage 2"
        print("  ✓ Mobile bottom-sheet drawer rendered and opened seamlessly.")

        page.keyboard.press("Escape")
        page.wait_for_timeout(400)

        browser.close()

    if errors:
        print("\n[ERROR] Errors found during test:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    else:
        print("\n=== ALL DRAWER & POPUP TESTS PASSED WITH 0 ERRORS! ===")

if __name__ == "__main__":
    run_drawer_tests()
