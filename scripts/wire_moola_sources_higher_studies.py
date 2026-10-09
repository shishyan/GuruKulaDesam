#!/usr/bin/env python3
"""
scripts/wire_moola_sources_higher_studies.py
Upgrades higher-studies.html to wire every module-sources div with an interactive
"📖 மூல நூல் வாசிக்க" button and modal viewer backed by assets/js/moola-nool-data.js.
"""

import re
import os

HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'higher-studies.html')

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS for moola buttons and modal if not already present
MOOLA_CSS = """
    /* Moola Nool Direct Scripture Reader Modal & Buttons */
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
    /* Modal Backdrop & Dialog */
    .moola-modal-backdrop {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.82);
      backdrop-filter: blur(6px);
      z-index: 9999;
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
      border: 1px solid rgba(212, 175, 55, 0.4);
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.85), 0 0 30px rgba(212, 175, 55, 0.15);
      border-radius: 18px;
      max-width: 820px;
      width: 100%;
      max-height: 88vh;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      animation: moolaFadeIn 0.25s ease-out;
    }
    @keyframes moolaFadeIn {
      from { opacity: 0; transform: scale(0.96) translateY(10px); }
      to { opacity: 1; transform: scale(1) translateY(0); }
    }
    .moola-modal-header {
      padding: 18px 24px;
      border-bottom: 1px solid rgba(212, 175, 55, 0.25);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(15, 23, 42, 0.95);
      border-radius: 18px 18px 0 0;
      position: sticky;
      top: 0;
      z-index: 10;
    }
    .moola-modal-title {
      font-size: 1.25rem;
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
      font-size: 1.1rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s;
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
      background: rgba(10, 16, 32, 0.9);
      border-radius: 0 0 18px 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }
"""

if '.moola-read-btn' not in content:
    content = content.replace('</style>', MOOLA_CSS + '\n  </style>', 1)

# Mapping dictionary for sources to scripture IDs
SOURCE_MAP = [
    (r'பதஞ்சலி யோக சூத்திரம் — சாதன பாதம்', 'patanjali-yoga-sutras', 'sadhana-pada'),
    (r'பதஞ்சலி யோக சூத்திரம் — விபூதி பாதம்', 'patanjali-yoga-sutras', 'samadhi-pada'),
    (r'பதஞ்சலி கைவல்ய பாதம்', 'patanjali-yoga-sutras', 'kaivalya-pada'),
    (r'பதஞ்சலி யோக சூத்திரம் &amp; வ்யாச பாஷ்யம்', 'patanjali-yoga-sutras', 'samadhi-pada'),
    (r'பாதஞ்சல யோக தர்சனம்', 'patanjali-yoga-sutras', 'samadhi-pada'),
    (r'விவேகசூடாமணி, கடோபநிடதம் &amp; பகவத் கீதை அத்\. 5', 'vivekachudamani', 'sadhana-chatushtaya'),
    (r'விவேகசூடாமணி மனவடக்க சுலோகங்கள் &amp; கீதை அத்\. 3', 'bhagavad-gita', 'gita-ch3'),
    (r'ஸ்ரீ ஆதிசங்கரரின் விவேகசூடாமணி', 'vivekachudamani', 'sadhana-chatushtaya'),
    (r'ஆதிசங்கரரின் தத்வ போதம்', 'vivekachudamani', 'sadhana-chatushtaya'),
    (r'மாண்டூக்ய உபநிடதம்', 'principal-upanishads', 'mandukya-upanishad'),
    (r'சாந்தோக்ய &amp; பிருஹதாரண்யக', 'principal-upanishads', 'taittiriya-upanishad'),
    (r'பாதராயண பிரம்ம சூத்திர', 'principal-upanishads', 'mandukya-upanishad'),
    (r'கௌடபாத காரிகை', 'principal-upanishads', 'mandukya-upanishad'),
    (r'தைத்திரீய உபநிடதம்', 'principal-upanishads', 'taittiriya-upanishad'),
    (r'தைத்திரீய ஆரண்யகம்', 'principal-upanishads', 'taittiriya-upanishad'),
    (r'ஸ்ரீமத் பகவத் கீதை சாங்கர பாஷ்யம் முழுமை', 'bhagavad-gita', 'gita-ch2'),
    (r'பகவத் கீதை சாங்கர பாஷ்யம் \(அத்\. 1-6\)', 'bhagavad-gita', 'gita-ch2'),
    (r'மெய்கண்டாரின் சிவஞானபோதம்', 'sivajnana-bodham', 'pramana-iyal'),
    (r'சிவஞான சித்தியார்', 'sivajnana-bodham', 'sadhana-iyal'),
    (r'சந்தான குரவர்கள்', 'sivajnana-bodham', 'payan-iyal'),
    (r'மாதவச் சிவஞான யோகிகளின் திராவிட மகாபாஷ்யம்', 'sivajnana-bodham', 'pramana-iyal'),
    (r'ஈஸ்வர பிரத்யபிஜ்ஞா', 'sivajnana-bodham', 'pramana-iyal'),
    (r'உண்மை விளக்கம்', 'sivajnana-bodham', 'payan-iyal'),
    (r'சிவ ஆகம சாரம் &amp; திருமந்திரம் 7-ஆம் தந்திரம்', 'tirumandiram-yoga', 'ashtanga-yoga-tamil'),
    (r'திருமந்திரம் \(மூன்றாம் தந்திரம் — யோகப் பகுதி\)', 'tirumandiram-yoga', 'ashtanga-yoga-tamil'),
    (r'அன்னம்பட்டர் அருளிய தர்க்க சங்கிரஹம்', 'tarka-sangraha', 'padartha-pramana'),
    (r'திருக்குறள் அறத்துப்பால்', 'thirukkural-arathuppal', 'illara-iyal'),
    (r'விதுர நீதி, ஆத்திசூடி', 'thirukkural-arathuppal', 'illara-iyal'),
    (r'இருபது சந்நியாச உபநிடதங்கள்', 'sannyasa-upanishads', 'paramahamsa-upanishad'),
    (r'அஷ்டாவக்ர கீதை', 'vivekachudamani', 'sadhana-chatushtaya'),
    (r'சங்கரரின் உபதேச சஹஸ்ரி', 'vivekachudamani', 'sadhana-chatushtaya'),
    (r'தெய்வத்தின் குரல்', 'principal-upanishads', 'taittiriya-upanishad'),
    (r'திருத்தொண்டர் புராணம்', 'thiruvarutpa', 'jivakarunya-ozhukkam'),
    (r'பன்னிரு திருமுறைகள்', 'thiruvarutpa', 'jivakarunya-ozhukkam'),
    (r'Erwin Schrödinger &amp; விவேகானந்தரின்', 'principal-upanishads', 'mandukya-upanishad'),
    (r'பாரத குடும்ப மரபியல்', 'thirukkural-arathuppal', 'illara-iyal')
]

def replace_source_div(match):
    full_match = match.group(0)
    # Check if already modified
    if 'moola-read-btn' in full_match:
        return full_match

    # Extract inner content
    inner = match.group(1)
    
    # Find matching scripture
    chosen_id = 'patanjali-yoga-sutras'
    chosen_sec = 'sadhana-pada'
    for pattern, sc_id, sec_id in SOURCE_MAP:
        if re.search(pattern, inner):
            chosen_id = sc_id
            chosen_sec = sec_id
            break
            
    btn_html = (
        f'<div class="moola-actions-row">'
        f'  <button type="button" class="moola-read-btn" onclick="openMoolaNoolModal(\'{chosen_id}\', \'{chosen_sec}\')">'
        f'    <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:13px; height:13px;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg> 📖 மூல நூல் வாசிக்க'
        f'  </button>'
        f'  <a href="moola-nool.html?text={chosen_id}&amp;sec={chosen_sec}" class="moola-canon-link" title="முழு மூல நூலகத்தில் திறக்க">'
        f'    நூலகத்தில் முழுமை &rarr;'
        f'  </a>'
        f'</div>'
    )
    
    return f'<div class="module-sources">{inner}{btn_html}</div>'

# Perform replacement on all module-sources
content = re.sub(r'<div class="module-sources">(.*?)</div>', replace_source_div, content, flags=re.DOTALL)

# Add Modal Markup and JS before </body>
MODAL_HTML = """
  <!-- MOOLA NOOL MODAL VIEWER -->
  <div class="moola-modal-backdrop" id="moolaNoolModalBackdrop" onclick="if(event.target===this) closeMoolaNoolModal()">
    <div class="moola-modal-card" role="dialog" aria-modal="true" aria-labelledby="moolaModalTitle">
      <div class="moola-modal-header">
        <h3 class="moola-modal-title" id="moolaModalTitle">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:20px; height:20px; color:var(--gold-bright);"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
          <span id="moolaModalTitleText">மூல நூல் வாசகம்</span>
        </h3>
        <button type="button" class="moola-modal-close-btn" onclick="closeMoolaNoolModal()" aria-label="Close">&times;</button>
      </div>
      <div class="moola-modal-body" id="moolaModalBody">
        <!-- Injected dynamically -->
      </div>
      <div class="moola-modal-footer">
        <span style="font-size:0.85rem; color:#94a3b8;" id="moolaModalAcademicTag">குருகுல வேதாந்த வித்யாபீடம் சான்றாதாரப் பாடப்பகுதி</span>
        <a href="moola-nool.html" id="moolaModalFullLink" class="moola-read-btn" style="text-decoration:none;">
          முழு நூலகத்தில் திறக்க &rarr;
        </a>
      </div>
    </div>
  </div>

  <script src="assets/js/moola-nool-data.js"></script>
  <script>
    function openMoolaNoolModal(scriptureId, sectionId) {
      var sc = window.getMoolaScripture(scriptureId);
      if (!sc) {
        window.location.href = 'moola-nool.html?text=' + encodeURIComponent(scriptureId);
        return;
      }

      document.getElementById('moolaModalTitleText').textContent = sc.title.split('(')[0].trim();
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
      var backdrop = document.getElementById('moolaNoolModalBackdrop');
      if (backdrop) backdrop.classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function closeMoolaNoolModal() {
      var backdrop = document.getElementById('moolaNoolModalBackdrop');
      if (backdrop) backdrop.classList.remove('open');
      document.body.style.overflow = '';
    }

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeMoolaNoolModal();
    });
  </script>
"""

if 'moolaNoolModalBackdrop' not in content:
    content = content.replace('</body>', MODAL_HTML + '\n</body>', 1)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully updated {HTML_PATH}")
