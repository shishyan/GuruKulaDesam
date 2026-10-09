import os
import sys
import re
from html.parser import HTMLParser

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'c:\GitHub\Gurukuladesam'
index_path = os.path.join(ROOT, 'index.html')

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

print("--- 1. Testing Title & Meta ---")
title_match = re.search(r'<title>(.*?)</title>', html)
assert title_match, "No <title> found!"
title = title_match.group(1).strip()
print("Title:", title)
assert title == "குரு குல ஆசிரமம் | Guru Kula Ashram", f"Unexpected title: {title}"

desc_match = re.search(r'<meta name="description" content="(.*?)">', html)
assert desc_match, "No meta description found!"
print("Meta Description:", desc_match.group(1))

print("\n--- 2. Testing Cards Structure ---")
# Check hero card
assert '<div class="home-hero-card"' in html, "Missing .home-hero-card"
assert '<h1 class="home-hero-title">குரு குல ஆசிரமம்</h1>' in html, "Missing clean hero title"

# Check visual cards
visual_cards = re.findall(r'<article class="home-visual-card">', html)
print(f"Visual cards count: {len(visual_cards)}")
assert len(visual_cards) == 2, f"Expected 2 visual cards, got {len(visual_cards)}"
assert 'assets/images/gurukula-banyan-tree-bg.jpg' in html, "Missing Banyan tree image"
assert 'assets/images/lessons/disciples_under_sacred_tree.jpg' in html, "Missing Disciples image"

# Check 5 stage cards
stage_cards = re.findall(r'<div class="stage-card\s+stage-([^"]+)">', html)
print(f"Stage cards found: {len(stage_cards)} ({stage_cards})")
assert len(stage_cards) == 5, f"Expected 5 stage cards, got {len(stage_cards)}"
expected_stages = ['primary', 'middle', 'secondary', 'senior', 'collegiate']
assert stage_cards == expected_stages, f"Stage cards mismatch: {stage_cards} vs {expected_stages}"

# Check all 12 grades have direct buttons in the stage cards
for g in range(1, 13):
    assert f'tharam-{g}.html' in html, f"Missing direct link to tharam-{g}.html in stage cards!"
print("All 12 grade direct links (tharam-1 to tharam-12) present in stage cards!")

# Check Collegiate links
assert 'higher-studies.html#tierUG' in html, "Missing B.A. link"
assert 'higher-studies.html#tierPG' in html, "Missing M.A. link"
assert 'higher-studies.html#tierPhD' in html, "Missing Ph.D. link"
print("Higher studies direct links present!")

# Check 3 core portal cards
portal_cards = re.findall(r'<div class="portal-card">', html)
print(f"Portal cards count: {len(portal_cards)}")
assert len(portal_cards) == 3, f"Expected 3 portal cards, got {len(portal_cards)}"

print("\n--- 3. Testing Navigation & Integrity ---")
# Check left strip bar
assert 'id="leftStripBar"' in html, "Missing left strip bar"
# Check breadcrumb
assert '<span class="crumb-current">குரு குல ஆசிரமம்</span>' in html, "Breadcrumb should be 'குரு குல ஆசிரமம்'"
# Check no dumped lesson anatomy or 7-book paragraph dumps
assert 'curriculum-anatomy-section' not in html, "Lesson anatomy should not be dumped on index"
assert 'The 7 Sub-Chapters of Every Lesson' not in html, "Sub-chapters dump should not be on index"

print("\n✓ ALL INDEX DOM & CARD ARCHITECTURE CHECKS PASSED PERFECTLY!")
