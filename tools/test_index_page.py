import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge', headless=True)
    page = b.new_page()
    errors = []
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    page.on('pageerror', lambda exc: errors.append(str(exc)))
    
    page.goto('http://localhost:8000/index.html', wait_until='domcontentloaded')
    page.wait_for_selector('.home-hero-card')

    title = page.title()
    print('Title:', title, flush=True)
    assert title == 'குரு குல ஆசிரமம் | Guru Kula Ashram', f'Unexpected title: {title}'

    stage_cards = page.locator('.stage-card').count()
    print('Stage cards count:', stage_cards, flush=True)
    assert stage_cards == 5, f'Expected 5 stage cards, got {stage_cards}'

    portal_cards = page.locator('.portal-card').count()
    print('Portal cards count:', portal_cards, flush=True)
    assert portal_cards == 3, f'Expected 3 portal cards, got {portal_cards}'

    visual_cards = page.locator('.home-visual-card').count()
    print('Visual cards count:', visual_cards, flush=True)
    assert visual_cards == 2, f'Expected 2 visual cards, got {visual_cards}'

    assert len(errors) == 0, f'Console errors: {errors}'
    print('ALL INDEX CHECKS PASSED!', flush=True)
    b.close()
