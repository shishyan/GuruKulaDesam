import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge', headless=True)
    page = b.new_page()
    page.goto('http://localhost:8000/tharam-1.html?grade=1&book=nanneri&chapter=1', wait_until='networkidle')
    page.wait_for_timeout(500)
    card = page.query_selector('.reading-chapter-card')
    if card:
        card.screenshot(path='tools/nanneri_ch1_enriched.png')
        print("Enriched Nanneri Ch 1 screenshot saved to tools/nanneri_ch1_enriched.png")
    b.close()
