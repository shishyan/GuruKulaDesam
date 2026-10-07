# -*- coding: utf-8 -*-
"""
Upgrades Guru Kula Desam to a professional online school for the new world with Vedic concepts behind (Fusion).
Only adds things, does not remove.
Applies changes to root, site/, and docs/.
"""

import os
import re

def add_school_banner_to_kalvi(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'The Professional Vedic-Modern Online Academy' in content:
        print(f"School banner already present in {file_path}")
        return

    banner_html = """
    <!-- Online School Academy Flagship Banner -->
    <div style="background: linear-gradient(135deg, rgba(14, 25, 45, 0.95), rgba(15, 23, 42, 0.95)); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 16px; padding: 22px 28px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
      <div style="max-width: 760px;">
        <div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(56,189,248,0.12); color: #38bdf8; border: 1px solid rgba(56,189,248,0.3); padding: 3px 12px; border-radius: 14px; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;">
          <span>🏫 The Professional Vedic-Modern Online Academy</span>
        </div>
        <h3 style="color: #ffffff; font-size: 1.35rem; font-weight: 800; margin-bottom: 6px;">
          குருகுல இணையப் பள்ளி போர்டல் — 21-ஆம் நூற்றாண்டு மாணவர் தளம்
        </h3>
        <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.6; margin: 0;">
          வேத மெய்யறிவும் குவாண்டம் இயற்பியல், நரம்பியல், AI நெறிமுறைகள் சங்கமிக்கும் 8 தூண்கள், போமோடோரோ தியான படிப்பு அரங்கம், நினைவாற்றல் வினா அட்டைகள் மற்றும் உடனடிப் பட்டயச் சான்றிதழ் இயற்றி.
        </p>
      </div>
      <a href="school.html" class="sheet-btn sheet-btn-view" style="padding: 12px 24px; font-size: 0.95rem; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(56,189,248,0.3);">
        <span>இணையப் பள்ளி நுழைக ↗</span>
      </a>
    </div>
"""

    # Insert right before <div class="google-site-banner">
    if '<div class="google-site-banner">' in content:
        content = content.replace('<div class="google-site-banner">', banner_html + '\n    <div class="google-site-banner">')
    else:
        content = content.replace('<main class="main-content">', '<main class="main-content">\n' + banner_html)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Added school banner to {file_path}")

def update_tharam_1(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add LMS Grade Banner if not present
    if 'குருகுல இணையப் பள்ளி — தரம் 1' not in content:
        banner = """
    <!-- Grade 1 LMS Learning Progress Dashboard -->
    <div class="grade-lms-tracker-banner" style="background:linear-gradient(90deg, rgba(15,23,42,0.92), rgba(24,37,64,0.92)); border:1px solid rgba(56, 189, 248, 0.28); border-radius:14px; padding:14px 22px; margin-bottom:24px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px; box-shadow:0 6px 20px rgba(0,0,0,0.4);">
      <div style="display:flex; align-items:center; gap:14px;">
        <div style="font-size:1.8rem; background:rgba(56, 189, 248, 0.12); width:46px; height:46px; display:flex; align-items:center; justify-content:center; border-radius:12px; border:1px solid rgba(56, 189, 248, 0.3);">🏫</div>
        <div>
          <div style="color:#ffffff; font-weight:700; font-size:1rem; display:flex; align-items:center; gap:8px;">
            <span>குருகுல இணையப் பள்ளி — தரம் 1 கற்றல் முன்னேற்றம்</span>
            <span class="wbs-code" style="font-size:0.75rem;">WBS G01</span>
          </div>
          <div style="color:#94a3b8; font-size:0.85rem; margin-top:2px;" id="gradeProgressText-1">முன்னேற்றம்: கணக்கிடப்படுகிறது...</div>
        </div>
      </div>
      <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
        <div class="progress-bar-container" style="width:160px; height:10px; background:rgba(255,255,255,0.1); border-radius:10px; overflow:hidden;">
          <div id="gradeProgressBar-1" style="height:100%; width:0%; background:linear-gradient(90deg, #38bdf8, #2dd4bf); transition:width 0.4s ease;"></div>
        </div>
        <span id="gradeProgressPercent-1" style="font-size:0.92rem; font-weight:800; color:#38bdf8;">0%</span>
        <a href="school.html" class="sheet-btn sheet-btn-view" style="font-size:0.82rem; padding:6px 14px; text-decoration:none; display:inline-flex; align-items:center; gap:6px;">
          <span>பள்ளி போர்டல் ↗</span>
        </a>
      </div>
    </div>
"""
        content = content.replace('<div class="hero-banner">', banner + '\n    <div class="hero-banner">')

    # 2. Add WBS 1.5 Modern Science & Vedic Concepts Fusion for Grade 1
    if 'WBS 1.5' not in content:
        fusion_grade1 = """
    <!-- WBS 1.5 Modern Science & Vedic Concepts Fusion for Grade 1 -->
    <section style="background: linear-gradient(135deg, rgba(14, 25, 45, 0.95), rgba(18, 30, 54, 0.9)); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 16px; padding: 26px; margin: 30px 0; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:16px; border-bottom:1px solid rgba(56, 189, 248, 0.2); padding-bottom:12px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span class="wbs-code wbs-code-primary">WBS 1.5</span>
          <h3 style="color:#ffffff; font-size:1.25rem; font-weight:700; margin:0;">
            🌐 நவீன அறிவியல் &amp; வேதக் கருத்துக்களின் சங்கமம் — தொடக்க நிலை இயற்கை அறிவியலும் நற்பண்புகளும்
          </h3>
        </div>
        <span style="font-size:0.78rem; font-weight:700; color:#38bdf8; background:rgba(56, 189, 248, 0.1); border:1px solid rgba(56, 189, 248, 0.3); padding:4px 12px; border-radius:20px;">
          EARLY CHILDHOOD STEM &amp; VEDIC ECOLOGY
        </span>
      </div>

      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px; margin-bottom:18px;">
        <div style="background:rgba(0, 0, 0, 0.35); border:1px solid rgba(56, 189, 248, 0.2); border-left:3px solid #38bdf8; border-radius:10px; padding:16px;">
          <div style="color:#38bdf8; font-size:0.95rem; font-weight:700; margin-bottom:8px;">
            🔬 ஐம்புலன்களும் பஞ்சபூதங்களும் (Sensory Integration)
          </div>
          <div style="color:#cbd5e1; font-size:0.9rem; line-height:1.7;">
            தொடக்கப் பருவத்தில் குழந்தைகள் மண்ணைத் தொட்டு, நீரை உணர்ந்து, மலர்களை நுகர்ந்து பஞ்சபூதங்களை அறிவது அவர்களின் அறிவாற்றல் நரம்பு இணைப்புகளை (Neural Synaptogenesis) பன்மடங்கு பலப்படுத்துகிறது.
          </div>
        </div>

        <div style="background:rgba(0, 0, 0, 0.35); border:1px solid rgba(45, 212, 191, 0.2); border-left:3px solid #2dd4bf; border-radius:10px; padding:16px;">
          <div style="color:#2dd4bf; font-size:0.95rem; font-weight:700; margin-bottom:8px;">
            🚀 திரைநேரக் கட்டுப்பாடு &amp; வெளிப்புற நற்பண்புகள் (Healthy Screen Habits)
          </div>
          <div style="color:#cbd5e1; font-size:0.9rem; line-height:1.7;">
            தரம் 1 மாணவர்களுக்கு அதிக திரை நேரத்தைத் தவிர்த்து, அதிகாலையில் பறவைகளை நோக்குதல், செடிகளுக்கு நீர் ஊற்றுதல் மற்றும் பெற்றோரிடம் இன்சொல் பேசுதல் நற்பழக்கங்களாகப் பயிற்றுவிக்கப்படுகின்றன.
          </div>
        </div>
      </div>

      <div style="background:rgba(212, 175, 55, 0.06); border:1px solid rgba(212, 175, 55, 0.25); border-radius:10px; padding:14px 18px;">
        <div style="color:var(--gold-soft); font-size:0.92rem; font-weight:700; margin-bottom:4px;">
          🔬 இளங்குருகுல ஆய்வுப் பணி: ஒரு சிறிய செடியை நட்டு தினமும் ஒரு கைப்பிடி நீர் ஊற்றி, அதற்கு நன்றி கூறிப் பாருங்கள்.
        </div>
      </div>

      <!-- LMS Chapter 1 Completion Bar -->
      <div class="lms-chapter-complete-bar" id="lms-box-1-1" style="margin-top:20px;">
        <div>
          <div style="color:#ffffff; font-weight:700; font-size:0.95rem; display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.2rem;">🎓</span>
            <span>தரம் 1 மாணவர் படிப்புப் பதிவு (Student Progress Tracker):</span>
          </div>
          <div style="color:#94a3b8; font-size:0.85rem; margin-top:2px;">தரம் 1 பாடங்கள் அனைத்தையும் படித்து முடித்தவுடன் குறிக்கவும்.</div>
        </div>
        <button type="button" class="lms-mark-btn" id="lms-btn-1-1" onclick="toggleChapterCompletion(1, 1)">
          <span class="lms-icon" id="lms-icon-1-1">○</span>
          <span class="lms-text" id="lms-text-1-1">பாடம் முடிந்தது எனக் குறிக்கவும்</span>
        </button>
      </div>
    </section>
"""
        # Insert before closing </main>
        content = content.replace('</main>', fusion_grade1 + '\n  </main>')

    # 3. Add LMS JS script at bottom if not present
    if 'toggleChapterCompletion(1, 1)' not in content:
        js_code = """
  <script>
    function toggleChapterCompletion(grade, unit) {
      var key = 'gkd_completed_' + grade + '_' + unit;
      var isDone = localStorage.getItem(key) === 'true';
      localStorage.setItem(key, isDone ? 'false' : 'true');
      updateLmsButton(grade, unit, !isDone);
      updateGradeProgress(grade, 1);
    }

    function updateLmsButton(grade, unit, done) {
      var btn = document.getElementById('lms-btn-' + grade + '-' + unit);
      var icon = document.getElementById('lms-icon-' + grade + '-' + unit);
      var text = document.getElementById('lms-text-' + grade + '-' + unit);
      if (!btn) return;
      if (done) {
        btn.style.background = 'rgba(45, 212, 191, 0.2)';
        btn.style.borderColor = 'rgba(45, 212, 191, 0.6)';
        btn.style.color = '#2dd4bf';
        if (icon) icon.textContent = '✓';
        if (text) text.textContent = 'நிறைவு செய்யப்பட்டது! (+50 XP)';
      } else {
        btn.style.background = 'rgba(56, 189, 248, 0.12)';
        btn.style.borderColor = 'rgba(56, 189, 248, 0.4)';
        btn.style.color = '#38bdf8';
        if (icon) icon.textContent = '○';
        if (text) text.textContent = 'பாடம் முடிந்தது எனக் குறிக்கவும்';
      }
    }

    function updateGradeProgress(grade, totalUnits) {
      var doneCount = 0;
      for (var u = 1; u <= totalUnits; u++) {
        var isDone = localStorage.getItem('gkd_completed_' + grade + '_' + u) === 'true';
        updateLmsButton(grade, u, isDone);
        if (isDone) doneCount++;
      }
      var pct = Math.round((doneCount / totalUnits) * 100);
      var bar = document.getElementById('gradeProgressBar-' + grade);
      var pctEl = document.getElementById('gradeProgressPercent-' + grade);
      var txtEl = document.getElementById('gradeProgressText-' + grade);
      if (bar) bar.style.width = pct + '%';
      if (pctEl) pctEl.textContent = pct + '%';
      if (txtEl) txtEl.textContent = 'முன்னேற்றம்: ' + doneCount + ' / ' + totalUnits + ' பாடம் நிறைவு';
    }

    document.addEventListener('DOMContentLoaded', function() {
      updateGradeProgress(1, 1);
    });
  </script>
"""
        content = content.replace('</body>', js_code + '\n</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {file_path}")

def update_left_strip_in_all_files():
    school_strip_item = """      <a href="school.html" class="strip-item" data-tooltip="இணையப் பள்ளி">
        <span class="strip-item-icon">🏫</span>
        <span class="strip-item-label">இணையப் பள்ளி</span>
      </a>"""

    for root, dirs, files in os.walk('.'):
        if '.git' in root or '.gemini' in root or 'node_modules' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                p = os.path.join(root, f)
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    text = fp.read()
                
                if '<nav class="strip-nav-list"' in text and 'href="school.html"' not in text:
                    # Place right after kalvi.html strip item
                    pattern = r'(<a\s+href="kalvi\.html"[^>]*>.*?</a>)'
                    if re.search(pattern, text, re.DOTALL):
                        new_text = re.sub(pattern, r'\1\n' + school_strip_item, text, count=1, flags=re.DOTALL)
                        with open(p, 'w', encoding='utf-8') as fp:
                            fp.write(new_text)
                        print(f"Added school.html to stripNav in {p}")

def main():
    for target in ['kalvi.html', 'site/kalvi.html', 'docs/kalvi.html']:
        if os.path.exists(target):
            add_school_banner_to_kalvi(target)

    for target in ['tharam-1.html', 'site/tharam-1.html', 'docs/tharam-1.html']:
        if os.path.exists(target):
            update_tharam_1(target)

    update_left_strip_in_all_files()

if __name__ == '__main__':
    main()
