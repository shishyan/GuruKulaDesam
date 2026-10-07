# -*- coding: utf-8 -*-
"""
Update Kalvi Hub cards with enhanced coursebook descriptions & visual pedagogy badges
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

card_badges = {
    1: ('60 பாடநூல் தாள்கள்', 'சுயகற்றல் பாடநெறி'),
    2: ('🎨 காட்சி விளக்கங்கள்', '64 தாள்கள் & பாடநூல்'),
    3: ('🎨 காட்சி விளக்கங்கள்', 'சுயகற்றல் பாடநூல்'),
    4: ('🎨 காட்சி விளக்கங்கள்', 'சுயகற்றல் பாடநூல்'),
    5: ('🎨 காட்சி விளக்கங்கள்', 'சுயகற்றல் பாடநூல்'),
    6: ('🎨 காட்சி விளக்கங்கள்', 'இடைநிலை பாடநூல்'),
    7: ('🎨 காட்சி விளக்கங்கள்', 'இடைநிலை பாடநூல்'),
    8: ('🎨 காட்சி விளக்கங்கள்', 'இடைநிலை பாடநூல்'),
    9: ('🎨 காட்சி விளக்கங்கள்', 'இடைநிலை பாடநூல்'),
    10: ('O/L தேர்வு நெறி', '🎨 காட்சி விளக்கங்கள்'),
    11: ('A/L உயர்தரம்', '🎨 காட்சி விளக்கங்கள்'),
    12: ('A/L பட்டம்', '🎨 காட்சி விளக்கங்கள்'),
}

for folder in ['site', 'docs', '.']:
    prefix = f"{folder}/" if folder != '.' else ""
    kalvi_path = f"{prefix}kalvi.html"
    if not os.path.exists(kalvi_path):
        continue
    
    with open(kalvi_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for g, (b1, b2) in card_badges.items():
        # Match the card block for tharam-g.html
        pattern = rf'(<a href="tharam-{g}\.html" class="grade-card">.*?<div class="grade-card-badge-row"[^>]*>)\s*<span class="grade-card-badge">.*?</span>\s*<span class="grade-card-badge">.*?</span>'
        replacement = rf'\g<1>\n            <span class="grade-card-badge">{b1}</span>\n            <span class="grade-card-badge">{b2}</span>'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(kalvi_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {kalvi_path}")

print("All kalvi hub files updated successfully!")
