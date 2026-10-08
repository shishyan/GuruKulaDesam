# -*- coding: utf-8 -*-
"""
Upgrade 7 Books summary cards in tharam-1.html to tharam-12.html:
Make each of the 7 books clickable directly to books.html?grade={N}&book={book_id}&chapter=1
and add an interactive "7 மின்னூல்கள் அரங்கம் (Read Digital Books)" button.
"""
import os
import re

BOOK_KEYS = [
    ("1. நன்னெறி", "nanneri"),
    ("2. நல்லறம்", "nallaram"),
    ("3. நல்வழி", "nalvazhi"),
    ("4. நற்துணை", "narthunai"),
    ("5. நற்சிந்தனை", "narchinthanai"),
    ("6. நற்சொல்", "narchol"),
    ("7. நற்செயல்", "narcheyal")
]

for g in range(1, 13):
    file_path = f"c:\\GitHub\\Gurukuladesam\\tharam-{g}.html"
    if not os.path.exists(file_path):
        continue
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Add direct link button to books.html in the header of the card if not present
    old_link = f'<a href="syllabus.html#sevenBooksArchitecture" style="color:var(--gold-bright); font-size:0.82rem; font-weight:700; text-decoration:none; display:inline-flex; align-items:center; gap:4px;">\n              முழு 12 தர பாட வரைபடம்'
    new_links = f'''<div style="display:flex; gap:8px; flex-wrap:wrap;">
            <a href="books.html?grade={g}" class="sheet-btn sheet-btn-view" style="font-size:0.78rem; padding:4px 10px; text-decoration:none;">
              7 மின்னூல்கள் அரங்கம் <svg class="gkd-icon gkd-external-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>
            </a>
            <a href="syllabus.html#sevenBooksArchitecture" style="color:var(--gold-bright); font-size:0.82rem; font-weight:700; text-decoration:none; display:inline-flex; align-items:center; gap:4px;">
              முழு 12 தர பாட வரைபடம்'''
    
    if "7 மின்னூல்கள் அரங்கம்" not in html and old_link in html:
        html = html.replace(old_link, new_links + '\n          </div>', 1)

    # Make each of the 7 book titles link to books.html?grade={g}&book={key}
    for title_txt, key in BOOK_KEYS:
        target = f'<strong style="color:'
        pattern = f'(<strong style="color:[^>]+>){re.escape(title_txt)}:</strong>'
        replacement = f'\\1<a href="books.html?grade={g}&book={key}&chapter=1" style="color:inherit; text-decoration:underline;" title="இம்மின்னூலை வாசிக்க">{title_txt}:</a></strong>'
        html = re.sub(pattern, replacement, html)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Upgraded tharam-{g}.html with direct book reader links.")

print("All grade pages upgraded.")
