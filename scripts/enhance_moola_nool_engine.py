#!/usr/bin/env python3
"""
scripts/enhance_moola_nool_engine.py
1. Appends universal moola modal CSS to assets/css/style.css.
2. Injects dynamic modal creation and lookup engine into assets/js/moola-nool-data.js.
3. Enhances assets/js/books-reader.js so every chapter in books.html has an instant "📖 மூல நூல் & பதவுரை" button.
4. Enhances tharam-1.html to tharam-12.html so all 7 books have direct moola nool reading buttons and load moola-nool-data.js.
"""

import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 1. Update style.css
STYLE_PATH = os.path.join(REPO_ROOT, 'assets', 'css', 'style.css')
with open(STYLE_PATH, 'r', encoding='utf-8') as f:
    css = f.read()

UNIVERSAL_MOOLA_CSS = """
/* ==========================================================================
   MOOLA NOOL CANONICAL SCRIPTURE UNIVERSAL MODAL & ACTION BUTTONS
   ========================================================================== */
.moola-actions-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px dashed rgba(212, 175, 55, 0.2);
}
.moola-read-btn {
  background: rgba(212, 175, 55, 0.15);
  border: 1px solid rgba(212, 175, 55, 0.4);
  color: var(--gold-bright, #ffd700);
  font-size: 0.82rem;
  font-weight: 700;
  padding: 5px 12px;
  border-radius: 16px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
  text-decoration: none;
}
.moola-read-btn:hover {
  background: rgba(212, 175, 55, 0.28);
  border-color: var(--gold, #d4af37);
  box-shadow: 0 0 12px rgba(212, 175, 55, 0.3);
  color: #fff;
}
.moola-canon-link {
  font-size: 0.78rem;
  color: #94a3b8;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: color 0.2s;
}
.moola-canon-link:hover {
  color: var(--gold-bright, #ffd700);
  text-decoration: underline;
}
.moola-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  z-index: 99999;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.moola-modal-backdrop.open {
  display: flex;
}
.moola-modal-card {
  background: linear-gradient(135deg, #0d1527 0%, #0a1020 100%);
  border: 1px solid rgba(212, 175, 55, 0.45);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.9), 0 0 30px rgba(212, 175, 55, 0.2);
  border-radius: 18px;
  max-width: 840px;
  width: 100%;
  max-height: 88vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  animation: moolaFadeIn 0.22s ease-out;
}
@keyframes moolaFadeIn {
  from { opacity: 0; transform: scale(0.96) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
.moola-modal-header {
  padding: 16px 24px;
  border-bottom: 1px solid rgba(212, 175, 55, 0.25);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(15, 23, 42, 0.98);
  border-radius: 18px 18px 0 0;
  position: sticky;
  top: 0;
  z-index: 10;
}
.moola-modal-title {
  font-size: 1.22rem;
  font-weight: 800;
  color: #fff;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}
.moola-modal-close-btn {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #cbd5e1;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  line-height: 1;
}
.moola-modal-close-btn:hover {
  background: rgba(239, 68, 68, 0.25);
  border-color: #ef4444;
  color: #fff;
}
.moola-modal-body {
  padding: 24px;
  color: #cbd5e1;
  font-size: 0.94rem;
  line-height: 1.7;
}
.moola-modal-footer {
  padding: 14px 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(10, 16, 32, 0.95);
  border-radius: 0 0 18px 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}
"""

if 'MOOLA NOOL CANONICAL SCRIPTURE UNIVERSAL MODAL' not in css:
    with open(STYLE_PATH, 'a', encoding='utf-8') as f:
        f.write('\n' + UNIVERSAL_MOOLA_CSS)
    print("Added universal modal CSS to assets/css/style.css")

# 2. Update assets/js/moola-nool-data.js to include global dynamic modal functions
JS_DATA_PATH = os.path.join(REPO_ROOT, 'assets', 'js', 'moola-nool-data.js')
with open(JS_DATA_PATH, 'r', encoding='utf-8') as f:
    js_content = f.read()

DYNAMIC_MODAL_ENGINE = """
// Dynamic Universal Moola Nool Modal Engine for Gurukula Desam
window.ensureMoolaModalDom = function() {
    var backdrop = document.getElementById('moolaNoolModalBackdrop');
    if (backdrop) return backdrop;

    backdrop = document.createElement('div');
    backdrop.id = 'moolaNoolModalBackdrop';
    backdrop.className = 'moola-modal-backdrop';
    backdrop.onclick = function(e) { if (e.target === backdrop) window.closeMoolaNoolModal(); };
    backdrop.innerHTML = 
      '<div class="moola-modal-card" role="dialog" aria-modal="true" aria-labelledby="moolaModalTitle">' +
      '  <div class="moola-modal-header">' +
      '    <h3 class="moola-modal-title" id="moolaModalTitle">' +
      '      <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:20px; height:20px; color:var(--gold-bright);"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>' +
      '      <span id="moolaModalTitleText">மூல நூல் வாசகம் & சொல்-பொருள் பதவுரை</span>' +
      '    </h3>' +
      '    <button type="button" class="moola-modal-close-btn" onclick="window.closeMoolaNoolModal()" aria-label="Close">&times;</button>' +
      '  </div>' +
      '  <div class="moola-modal-body" id="moolaModalBody"></div>' +
      '  <div class="moola-modal-footer">' +
      '    <span style="font-size:0.85rem; color:#94a3b8;" id="moolaModalAcademicTag">குருகுல தேசம் மூல சாத்திரக் களஞ்சியம்</span>' +
      '    <a href="moola-nool.html" id="moolaModalFullLink" class="moola-read-btn" style="text-decoration:none;" target="_blank">' +
      '      முழு மூல நூல் நூலகத்தில் திறக்க &rarr;' +
      '    </a>' +
      '  </div>' +
      '</div>';
    document.body.appendChild(backdrop);
    return backdrop;
};

window.openMoolaNoolModal = function(scriptureId, sectionId) {
    var sc = window.getMoolaScripture(scriptureId);
    if (!sc) {
        window.location.href = 'moola-nool.html?text=' + encodeURIComponent(scriptureId);
        return;
    }

    var backdrop = window.ensureMoolaModalDom();
    var titleText = document.getElementById('moolaModalTitleText');
    if (titleText) titleText.textContent = sc.title.split('(')[0].trim();

    var tagEl = document.getElementById('moolaModalAcademicTag');
    if (tagEl) tagEl.textContent = sc.title + ' • ' + sc.academicLevel;

    var fullLink = document.getElementById('moolaModalFullLink');
    if (fullLink) {
        fullLink.href = 'moola-nool.html?text=' + encodeURIComponent(scriptureId) + (sectionId ? '&sec=' + encodeURIComponent(sectionId) : '');
    }

    var bodyEl = document.getElementById('moolaModalBody');
    var html = '';

    html += '<div style="margin-bottom:18px; padding-bottom:14px; border-bottom:1px solid rgba(212,175,55,0.2);">';
    html += '  <p style="color:#f1f5f9; font-size:0.95rem; line-height:1.6; margin:0 0 10px 0;">' + sc.summary + '</p>';
    html += '  <div style="font-size:0.82rem; color:#cbd5e1;"><strong>பாஷ்ய மரபு:</strong> ' + sc.commentaryTradition + ' | <strong>ஆசிரியர்:</strong> ' + sc.author + '</div>';
    html += '</div>';

    var targetSections = sc.sections;
    if (sectionId) {
        var filtered = sc.sections.filter(function(s) { return s.id === sectionId; });
        if (filtered.length > 0) targetSections = filtered;
    }

    targetSections.forEach(function(sec) {
        html += '<h4 style="color:var(--gold-bright); font-size:1.15rem; margin:16px 0 12px; border-left:3px solid var(--gold); padding-left:10px;">' + sec.title + '</h4>';
        sec.verses.forEach(function(v) {
            html += '<div style="background:rgba(5, 10, 22, 0.7); border:1px solid rgba(255,255,255,0.1); border-radius:10px; padding:16px; margin-bottom:14px;">';
            html += '  <div style="display:flex; justify-content:space-between; margin-bottom:8px;">';
            html += '    <span style="background:rgba(212,175,55,0.2); color:var(--gold-bright); font-size:0.8rem; font-weight:700; padding:2px 8px; border-radius:10px;">' + v.num + '</span>';
            html += '  </div>';

            if (v.rootSanskrit) {
                html += '  <div style="color:#ffffff; font-family:serif; font-size:1.08rem; font-weight:600; line-height:1.6; margin-bottom:8px; white-space:pre-line;">' + v.rootSanskrit + '</div>';
            }
            if (v.rootTamilTranslit) {
                html += '  <div style="color:#f3f4f6; font-size:0.98rem; font-weight:500; line-height:1.6; margin-bottom:12px; white-space:pre-line;">' + v.rootTamilTranslit + '</div>';
            }

            if (v.padavurai && v.padavurai.length > 0) {
                html += '  <div style="background:rgba(0,0,0,0.3); border-radius:8px; padding:10px; margin-bottom:10px;">';
                html += '    <div style="font-size:0.8rem; font-weight:700; color:var(--gold-soft); margin-bottom:6px;">📖 சொல்-பொருள் பதவுரை (Word-by-word Padavurai):</div>';
                html += '    <table style="width:100%; border-collapse:collapse; font-size:0.85rem;">';
                v.padavurai.forEach(function(p) {
                    html += '      <tr><td style="color:var(--gold-bright); font-weight:600; padding:4px 8px; vertical-align:top; width:35%;">' + p.word + '</td><td style="color:#cbd5e1; padding:4px 8px;">' + p.meaning + '</td></tr>';
                });
                html += '    </table>';
                html += '  </div>';
            }

            if (v.bhavartha) {
                html += '  <div style="background:rgba(16,185,129,0.08); border-left:3px solid #10b981; padding:8px 12px; border-radius:0 6px 6px 0; margin-bottom:8px;">';
                html += '    <strong style="color:#34d399; font-size:0.82rem;">பொழிப்புரை: </strong><span style="color:#f1f5f9; font-size:0.92rem;">' + v.bhavartha + '</span>';
                html += '  </div>';
            }

            if (v.notes) {
                html += '  <div style="font-size:0.82rem; color:#93c5fd; background:rgba(56,189,248,0.06); padding:6px 10px; border-radius:6px;"><strong>பாஷ்யக் குறிப்பு:</strong> ' + v.notes + '</div>';
            }

            html += '</div>';
        });
    });

    bodyEl.innerHTML = html;
    backdrop.classList.add('open');
    document.body.style.overflow = 'hidden';
};

window.closeMoolaNoolModal = function() {
    var backdrop = document.getElementById('moolaNoolModalBackdrop');
    if (backdrop) backdrop.classList.remove('open');
    document.body.style.overflow = '';
};

// Map each of the 7 Ashram Books to its foundational canonical scripture
window.openChapterMoolaModal = function(bookId, chapterNum, grade) {
    var mapping = {
        'nanneri': { id: 'sivaprakasar-nanneri', sec: 'nanneri-incol' },
        'nallaram': { id: 'thirukkural-arathuppal', sec: 'illara-iyal' },
        'nalvazhi': { id: 'avvaiyar-nalvazhi', sec: 'nalvazhi-core' },
        'narthunai': { id: 'thevaram-thiruvasagam', sec: 'appar-thevaram' },
        'narchinthanai': { id: 'dhammapada-buddha', sec: 'yamaka-vagga' },
        'narchol': (grade && grade <= 3) ? { id: 'vedic-mantras-canon', sec: 'maha-mantras' } : { id: 'tirumandiram-yoga', sec: 'ashtanga-yoga-tamil' },
        'narcheyal': { id: 'bhagavad-gita', sec: 'gita-ch2' }
    };
    var target = mapping[bookId] || { id: 'thirukkural-arathuppal', sec: 'illara-iyal' };
    window.openMoolaNoolModal(target.id, target.sec);
};

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') window.closeMoolaNoolModal();
});
"""

if 'ensureMoolaModalDom' not in js_content:
    with open(JS_DATA_PATH, 'a', encoding='utf-8') as f:
        f.write('\n' + DYNAMIC_MODAL_ENGINE)
    print("Added dynamic modal engine to assets/js/moola-nool-data.js")

# 3. Update assets/js/books-reader.js
READER_JS_PATH = os.path.join(REPO_ROOT, 'assets', 'js', 'books-reader.js')
with open(READER_JS_PATH, 'r', encoding='utf-8') as f:
    r_code = f.read()

# Add button into verse-callout-clean in books-reader.js
OLD_VERSE_CALLOUT = """        <div class="verse-meaning-clean" style="color:#cbd5e1; font-size:0.92rem; margin-top:10px; line-height:1.6;">
          <strong style="color:var(--gold-soft);">பொருள் விளக்கம்:</strong> ${chap.verseMeaning}
        </div>"""

NEW_VERSE_CALLOUT = """        <div class="verse-meaning-clean" style="color:#cbd5e1; font-size:0.92rem; margin-top:10px; line-height:1.6;">
          <strong style="color:var(--gold-soft);">பொருள் விளக்கம்:</strong> ${chap.verseMeaning}
        </div>
        <div class="moola-reader-actions-row" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-top:14px; padding-top:10px; border-top:1px dashed rgba(212,175,55,0.25);">
          <button type="button" class="moola-read-btn" onclick="openChapterMoolaModal('${currentBook}', ${chap.chapterNumber}, ${currentGrade})">
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:13px; height:13px;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg> 📖 மூல நூல் &amp; பதவுரை காண்க
          </button>
          <a href="moola-nool.html" class="moola-canon-link" target="_blank" title="முழு மூல நூலகத்தில் திறக்க">
            மூல நூல் நூலகம் &rarr;
          </a>
        </div>"""

if 'moola-reader-actions-row' not in r_code and OLD_VERSE_CALLOUT in r_code:
    r_code = r_code.replace(OLD_VERSE_CALLOUT, NEW_VERSE_CALLOUT)
    with open(READER_JS_PATH, 'w', encoding='utf-8') as f:
        f.write(r_code)
    print("Added moola modal button to assets/js/books-reader.js")

# 4. Update books.html to include assets/js/moola-nool-data.js
BOOKS_HTML_PATH = os.path.join(REPO_ROOT, 'books.html')
with open(BOOKS_HTML_PATH, 'r', encoding='utf-8') as f:
    b_html = f.read()

if 'moola-nool-data.js' not in b_html:
    b_html = b_html.replace('<script src="assets/js/books-reader.js"></script>',
                            '<script src="assets/js/moola-nool-data.js"></script>\n  <script src="assets/js/books-reader.js"></script>')
    with open(BOOKS_HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(b_html)
    print("Added moola-nool-data.js to books.html")

# 5. Update tharam-1.html to tharam-12.html
BOOK_MAP = {
    '1. நன்னெறி': ('sivaprakasar-nanneri', 'nanneri-incol'),
    '2. நல்லறம்': ('thirukkural-arathuppal', 'illara-iyal'),
    '3. நல்வழி': ('avvaiyar-nalvazhi', 'nalvazhi-core'),
    '4. நற்துணை': ('thevaram-thiruvasagam', 'appar-thevaram'),
    '5. நற்சிந்தனை': ('dhammapada-buddha', 'yamaka-vagga'),
    '6. நற்சொல்': ('vedic-mantras-canon', 'maha-mantras'),
    '7. நற்செயல்': ('bhagavad-gita', 'gita-ch2')
}

for g in range(1, 13):
    t_path = os.path.join(REPO_ROOT, f'tharam-{g}.html')
    if not os.path.exists(t_path):
        continue
    with open(t_path, 'r', encoding='utf-8') as f:
        tc = f.read()

    # Include moola-nool-data.js before </body> if not present
    if 'moola-nool-data.js' not in tc:
        tc = tc.replace('</body>', '<script src="assets/js/moola-nool-data.js"></script>\n</body>')

    # Enhance 7 books list items with inline moola button
    for book_label, (sc_id, sec_id) in BOOK_MAP.items():
        # Check if book_label is in tc
        # e.g., <strong style="color:...;"><a href="books.html?grade=1&book=nanneri&chapter=1" ...>1. நன்னெறி:</a></strong>
        pattern = rf'(<strong[^>]*><a href="books\.html\?grade={g}&amp;book=[^"]+"[^>]*>{re.escape(book_label)}:?</a></strong>\s*<span[^>]*>.*?</span>)'
        
        def add_moola_inline(match, s_id=sc_id, se_id=sec_id):
            orig = match.group(0)
            if 'openMoolaNoolModal' in orig:
                return orig
            btn = f' <button type="button" class="moola-read-btn" style="padding:2px 8px; font-size:0.75rem; margin-left:6px;" onclick="openMoolaNoolModal(\'{s_id}\', \'{se_id}\')" title="மூல நூல் பாசுரம் & பதவுரை காண்க">📖 மூல நூல்</button>'
            return orig + btn

        tc = re.sub(pattern, add_moola_inline, tc)

    with open(t_path, 'w', encoding='utf-8') as f:
        f.write(tc)
    print(f"Enhanced 7 books & added moola-nool-data.js to tharam-{g}.html")

print("All enhancements completed successfully!")
