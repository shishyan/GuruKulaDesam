#!/usr/bin/env python3
"""
Clean remaining emojis from HTML and main.js
"""

import os
import glob
import re

svg_sun = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
svg_star = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L15 9L22 12L15 15L12 22L9 15L2 12L9 9Z"/></svg>'
svg_cal = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
svg_path = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>'

svg_map = {
    '\u2600': svg_sun,
    '\ufe0f': '',  # variation selector 16
    '\u2726': svg_star,
    '\U0001f4c5': svg_cal,
    '\U0001f306': svg_path
}

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
docs_dir = os.path.join(repo_root, 'docs')

for f in ['index.html', 'kalvi.html', 'sanmargam.html', 'tharam-3.html', 'thirukkural.html']:
    p = os.path.join(docs_dir, f)
    if not os.path.exists(p):
        continue
    txt = open(p, encoding='utf-8').read()
    for ch, svg in svg_map.items():
        txt = txt.replace(ch, svg)
    open(p, 'w', encoding='utf-8').write(txt)
    print('Cleaned', f)

# Also check main.js for any raw emojis in getContextTabsForPage and UNIVERSAL_SEARCH_ITEMS
main_js_path = os.path.join(docs_dir, 'assets', 'js', 'main.js')
js_txt = open(main_js_path, encoding='utf-8').read()

# Replace any emojis in icon: '...' with standard icon keys
js_icon_replacements = {
    "icon: '📖'": "icon: 'book'",
    "icon: '🔤'": "icon: 'virtues'",
    "icon: '🎨'": "icon: 'palette'",
    "icon: '❓'": "icon: 'question'",
    "icon: '🪔'": "icon: 'deepam'",
    "icon: '⏪'": "icon: 'arrowLeft'",
    "icon: '⏩'": "icon: 'arrowRight'",
    "icon: '🌿'": "icon: 'leaf'",
    "icon: '📚'": "icon: 'book'",
    "icon: '✅'": "icon: 'check'",
    "icon: '📜'": "icon: 'scroll'",
    "icon: '🏛️'": "icon: 'temple'",
    "icon: '🏫'": "icon: 'school'",
    "icon: '🔬'": "icon: 'science'",
    "icon: '📊'": "icon: 'target'",
    "icon: '⏱️'": "icon: 'clock'",
    "icon: '🗂️'": "icon: 'scroll'",
    "icon: '🧭'": "icon: 'target'",
    "icon: '🔱'": "icon: 'trishul'",
    "icon: '👑'": "icon: 'crown'",
    "icon: '🌟'": "icon: 'flame'",
    "icon: '🟢'": "icon: 'tierGreen'",
    "icon: '🟡'": "icon: 'tierYellow'",
    "icon: '🔴'": "icon: 'tierRed'",
    "icon: '🏠'": "icon: 'home'",
    "icon: '🏡'": "icon: 'home'",
    "icon: '🔥'": "icon: 'flame'",
    "icon: '🎬'": "icon: 'cinema'",
    "icon: '📺'": "icon: 'cinema'",
    "icon: '📍'": "icon: 'mapPin'",
    "icon: '💎'": "icon: 'om'",
    "icon: '🧘'": "icon: 'om'",
    "icon: '🌸'": "icon: 'lotus'",
    "icon: '🐘'": "icon: 'ganesha'",
    "icon: '🪷'": "icon: 'lotus'",
    "icon: '❤️'": "icon: 'lotus'",
    "icon: '🛡️'": "icon: 'trishul'",
    "icon: '🌱'": "icon: 'leaf'",
    "icon: '☀️'": "icon: 'flame'",
    "icon: '🕯️'": "icon: 'deepam'",
    "icon: '🎵'": "icon: 'music'",
    "icon: '🎶'": "icon: 'music'",
    "icon: '🥛'": "icon: 'lotus'",
    "icon: '🙏'": "icon: 'lotus'",
    "icon: '🇮🇳'": "icon: 'temple'",
    "icon: '▶️'": "icon: 'play'",
    "icon: '🎓'": "icon: 'grad'",
    "icon: '🧑‍🏫'": "icon: 'user'",
    "icon: '👤'": "icon: 'user'",
    "icon: '🕉️'": "icon: 'om'",
    "icon: '🌐'": "icon: 'globe'",
    "icon: '⏰'": "icon: 'clock'",
    "icon: '🪞'": "icon: 'om'",
    "avatar: '👤'": "avatar: 'user'",
    "badge: '🎬 படம்'": "badge: 'திரைப்படம்'",
    "badge: '🎵 பாடல்'": "badge: 'இசைப்பாடல்'",
    "badge: '🌟 தொடக்க": "badge: 'தொடக்க",
    "badge: '🪔 இடைநிலை": "badge: 'இடைநிலை",
    "badge: '🔱 உயர்நிலை": "badge: 'உயர்நிலை",
    "🌟 தொடக்க சாதகர்": "தொடக்க சாதகர்",
    "🪔 இடைநிலை சாதகர்": "இடைநிலை சாதகர்",
    "🔱 உயர்நிலை சிவநேசர்": "உயர்நிலை சிவநேசர்",
    "⛶ பெரிய திரை": "பெரிய திரை",
    "⛶ இயல்பு": "இயல்பு",
    "📜 வரிகள்": "வரிகள்",
    "✕ மூடுக": "மூடுக",
    "✓ நகலெடுக்கப்பட்டது": "நகலெடுக்கப்பட்டது",
    "📋 வரிகளை": "வரிகளை",
    "✍️ ஆசிரியர்": "ஆசிரியர்",
    "📖 மூலம்": "மூலம்",
    "🎬 முழுப் படம்": "முழுப் படம்",
    "🎵 இசை வெளியீடு": "இசை வெளியீடு",
    "🔍": ""
}

for old, new in js_icon_replacements.items():
    js_txt = js_txt.replace(old, new)

open(main_js_path, 'w', encoding='utf-8').write(js_txt)
print('[OK] Cleaned icon keys and text in main.js')
