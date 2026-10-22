import glob
import re

html_files = glob.glob("*.html")
print(f"Total HTML files to inspect: {len(html_files)}")

# Group 7 replacement
# Replace links that go to books.html?book=... with puranas.html?id=...
# We also want to map the 7 ashram books shelf to puranas.html
books_sub_menu = """        <div class="strip-sub-menu">
          <div class="strip-sub-header">7 ஆசிரமப் பாடநூல்கள் அலமாரி</div>
          <a href="puranas.html?id=children-purana-stories" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3H4a2 2 0 0 0-2 2v13a3 3 0 0 0 3 3h13a3 3 0 0 0 3-3V5a2 2 0 0 0-2-2h-7"/><path d="M19 18a3 3 0 0 0 0-6H6a2 2 0 0 0 0 4h12"/><line x1="8" y1="7" x2="14" y2="7"/></svg></span><span>1. நன்னெறிப் புராணக் கதைகள்</span></a>
          <a href="puranas.html?id=mahabharatam" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 20A7 7 0 0 1 4 13a8.9 8.9 0 0 1 8.2-8.9 7 7 0 0 1 7.8 7.8A8.9 8.9 0 0 1 11 20z"/><path d="M12.5 4.5c.5 4.5-1 7.5-5 9.5"/></svg></span><span>2. நல்லற பாரதக் கதைகள்</span></a>
          <a href="puranas.html?id=ramayanam" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></span><span>3. நற்பண்பு ஸ்ரீ ராம சரிதம்</span></a>
          <a href="puranas.html?id=kandha-puranam" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2c-.8 2-1.5 3.5-1.5 5a1.5 1.5 0 0 0 3 0c0-1.5-.7-3-1.5-5z" fill="currentColor"/><path d="M5 13c0 4 3 6 7 6s7-2 7-6H5z"/><path d="M10 19v2h4v-2"/></svg></span><span>4. நற்துணை கந்தபுராணக் கதைகள்</span></a>
          <a href="puranas.html?id=bhagavata-puranam" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="2" fill="currentColor"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(30 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(-30 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(90 12 12)"/></svg></span><span>5. நற்சிந்தனை பாகவதக் கதைகள்</span></a>
          <a href="puranas.html?id=thiruvilaiyadal" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 4c-1.5 3-2 6-2 9 1 0 2-1 2-2 0 1 1 2 2 2 0-3-.5-6-2-9z"/><path d="M7 10c0 3 1.5 5 3 6-2 0-4-1.5-4.5-4 .5-.7 1-1.3 1.5-2z"/><path d="M17 10c0 3-1.5 5-3 6 2 0 4-1.5 4.5-4-.5-.7-1-1.3-1.5-2z"/><path d="M4 15c2 3 5 4 8 4s6-1 8-4c-2.5 0-4.5 1-8 1s-5.5-1-8-1z"/></svg></span><span>6. நற்சொல் சிவ லீலைக் கதைகள்</span></a>
          <a href="puranas.html?id=periyapuranam" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg></span><span>7. நற்செயல் பெரியபுராணக் கதைகள்</span></a>
        </div>"""

# Group 8 Books Library replacement
books_library_group = """      <!-- 8. நூலக அரங்கம் (Books Library — 100% தூய சிறார் புராண இதிகாசக் கதைகள்) -->
      <div class="strip-group" data-group="books-library">
        <a href="puranas.html" class="strip-item strip-has-sub" data-tooltip="நூலக அரங்கம் • Books Library">
          <span class="strip-item-icon">
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              <line x1="12" y1="6" x2="12" y2="14"/>
              <line x1="9" y1="10" x2="15" y2="10"/>
            </svg>
          </span>
          <span class="strip-item-label">நூலக அரங்கம் (Books Library)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color:#ffd700;">தூய புராண இதிகாசப் பெருங்கதைகள்</div>
          <a href="puranas.html?id=children-purana-stories" class="strip-sub-item"><span class="strip-sub-icon">🌸</span><span>சிறார் புராணக் கதைகள்</span></a>
          <a href="puranas.html?id=mahabharatam" class="strip-sub-item"><span class="strip-sub-icon">🏹</span><span>மகாபாரதக் கதைகள் (18 Parvas)</span></a>
          <a href="puranas.html?id=ramayanam" class="strip-sub-item"><span class="strip-sub-icon">👑</span><span>ஸ்ரீ ராம சரிதக் கதைகள் (6 Kandas)</span></a>
          <a href="puranas.html?id=kandha-puranam" class="strip-sub-item"><span class="strip-sub-icon">🪷</span><span>கந்த புராணக் கதைகள் (Murugan)</span></a>
          <a href="puranas.html?id=bhagavata-puranam" class="strip-sub-item"><span class="strip-sub-icon">🦚</span><span>பாகவதக் கதைகள் (12 Skandhas)</span></a>
          <a href="puranas.html?id=shiva-puranam" class="strip-sub-item"><span class="strip-sub-icon">🔱</span><span>சிவ புராணக் கதைகள் (Shiva Puranam)</span></a>
          <a href="puranas.html?id=vishnu-puranam" class="strip-sub-item"><span class="strip-sub-icon">✨</span><span>விஷ்ணு புராணக் கதைகள் (Vishnu)</span></a>
          <a href="puranas.html?id=periyapuranam" class="strip-sub-item"><span class="strip-sub-icon">🕊️</span><span>பெரியபுராண நாயன்மார் கதைகள்</span></a>
          <a href="puranas.html?id=thiruvilaiyadal" class="strip-sub-item"><span class="strip-sub-icon">🌊</span><span>திருவிளையாடல் 64 லீலைக் கதைகள்</span></a>
          <a href="puranas.html?id=thirumandhiram" class="strip-sub-item"><span class="strip-sub-icon">🌿</span><span>திருமூலர் வாழ்வியல் கதைகள்</span></a>
          <a href="puranas.html?id=matsya-puranam" class="strip-sub-item"><span class="strip-sub-icon">🐟</span><span>மத்ஸ்ய புராணக் கதைகள்</span></a>
          <a href="puranas.html?id=garuda-puranam" class="strip-sub-item"><span class="strip-sub-icon">🦅</span><span>கருட புராணக் கதைகள்</span></a>
          <a href="puranas.html?id=markandeya-puranam" class="strip-sub-item"><span class="strip-sub-icon">🔥</span><span>அரிச்சந்திரன் & துர்கா சரிதம்</span></a>
          <a href="puranas.html?id=padma-puranam" class="strip-sub-item"><span class="strip-sub-icon">🪷</span><span>பத்ம புராணக் கதைகள்</span></a>
          <a href="puranas.html" class="strip-sub-item" style="border-top:1px dashed rgba(255,255,255,0.15); margin-top:4px;"><span class="strip-sub-icon">📚</span><span style="font-weight:700; color:#ffd700;">அனைத்து 24 கதைப் புத்தகங்கள் ↗</span></a>
        </div>
      </div>"""

updated_count = 0
for fpath in html_files:
    with open(fpath, "r", encoding="utf-8") as fp:
        c = fp.read()
    
    # 1. Update group 7 books links to point to puranas.html?id=...
    c_new = re.sub(
        r'<div class="strip-group" data-group="books">[\s\S]*?<a href="books\.html" class="strip-item strip-has-sub"[\s\S]*?<div class="strip-sub-menu">[\s\S]*?</div>\s*</div>',
        lambda m: m.group(0).replace('href="books.html"', 'href="puranas.html"'),
        c
    )
    c_new = re.sub(
        r'<div class="strip-group" data-group="books">[\s\S]*?<div class="strip-sub-menu">[\s\S]*?</div>\s*</div>',
        f'<div class="strip-group" data-group="books">\n        <a href="puranas.html" class="strip-item strip-has-sub" data-tooltip="7 ஆசிரமப் பாடநூல்கள்">\n          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></span>\n          <span class="strip-item-label">7 ஆசிரமப் பாடநூல்கள்</span>\n          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>\n        </a>\n{books_sub_menu}\n      </div>',
        c_new
    )

    # 2. Update group 8 books-library
    c_new = re.sub(
        r'<div class="strip-group" data-group="books-library">[\s\S]*?</div>\s*</div>',
        books_library_group,
        c_new
    )

    if c_new != c:
        with open(fpath, "w", encoding="utf-8") as fp:
            fp.write(c_new)
        updated_count += 1

print(f"Updated sidebar book menus in {updated_count} HTML files!")
