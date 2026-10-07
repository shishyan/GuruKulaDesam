# -*- coding: utf-8 -*-
"""
Integrates Higher Studies (Vedanta Vidyapeeth) across:
1. Left Strip Navigation across all HTML files
2. kalvi.html (Collegiate Higher Studies section)
3. school.html (Graduation bridge)
4. tharam-12.html (Post-Grade 12 graduation bridge)
5. Synchronizes across ., site/, and docs/.
"""

import os
import re

def update_left_strip_for_higher_studies():
    higher_strip_item = """      <a href="higher-studies.html" class="strip-item" data-tooltip="உயர்கல்வி">
        <span class="strip-item-icon">🏛️</span>
        <span class="strip-item-label">உயர்கல்வி</span>
      </a>"""

    count = 0
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '.gemini' in root or 'node_modules' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                p = os.path.join(root, f)
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    text = fp.read()

                if '<nav class="strip-nav-list"' in text and 'href="higher-studies.html"' not in text:
                    # Insert right after school.html strip item
                    pattern = r'(<a\s+href="school\.html"[^>]*>.*?</a>)'
                    if re.search(pattern, text, re.DOTALL):
                        new_text = re.sub(pattern, r'\1\n' + higher_strip_item, text, count=1, flags=re.DOTALL)
                        with open(p, 'w', encoding='utf-8') as fp:
                            fp.write(new_text)
                        count += 1
    print(f"Added higher-studies.html to stripNav in {count} files")

def add_higher_studies_to_kalvi(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    if 'வேதாந்த வித்யாபீடம் — உயர்கல்வித் தளம்' in text:
        print(f"Higher studies card already in {file_path}")
        return

    higher_card = """
    <!-- Collegiate Higher Studies Vidyapeeth Card -->
    <div style="background: linear-gradient(135deg, rgba(8, 14, 26, 0.95), rgba(15, 23, 42, 0.95)); border: 1px solid rgba(212, 175, 55, 0.35); border-radius: 16px; padding: 22px 28px; margin: 30px 0 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
      <div style="max-width: 780px;">
        <div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(212,175,55,0.12); color: var(--gold-bright); border: 1px solid rgba(212,175,55,0.3); padding: 3px 12px; border-radius: 14px; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;">
          <span>🏛️ Collegiate Indic Studies • Post-Grade 12</span>
        </div>
        <h3 style="color: #ffffff; font-size: 1.35rem; font-weight: 800; margin-bottom: 6px;">
          வேதாந்த வித்யாபீடம் — உயர்கல்வித் தளம் (Advanced Indic Studies)
        </h3>
        <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.6; margin: 0;">
          பிரஸ்தானத்ரய ஆய்வுப் பட்டயம் (உபநிடதங்கள், கீதை, பிரம்ம சூத்திரம்), வேதாந்தப் பிரகரண கிரந்தங்கள் (தத்வ போதம், விவேகசூடாமணி), சைவ சித்தாந்த மெய்கண்ட சாத்திரங்கள், ஷட்தர்சன தர்க்கவியல் மற்றும் விவேகானந்தர் பிரயோக வேதாந்தம்.
        </p>
      </div>
      <a href="higher-studies.html" class="sheet-btn sheet-btn-view" style="padding: 12px 24px; font-size: 0.95rem; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 8px; border-color: var(--gold); box-shadow: 0 4px 15px rgba(212,175,55,0.25);">
        <span>உயர்கல்வித் தளம் காண்க ↗</span>
      </a>
    </div>
"""

    target = '    <!-- Key Navigation Highlights -->'
    if target in text:
        text = text.replace(target, higher_card + '\n' + target)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Added higher studies to {file_path}")

def add_higher_studies_bridge_to_school(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    if 'வேதாந்த வித்யாபீடம் — உயர்கல்விப் பட்டயம்' in text:
        print(f"Higher studies bridge already in {file_path}")
        return

    bridge_banner = """
    <!-- Graduation Bridge to Higher Studies -->
    <section style="background: linear-gradient(135deg, rgba(8, 14, 26, 0.95), rgba(15, 23, 42, 0.95)); border: 1px solid rgba(212, 175, 55, 0.35); border-radius: 18px; padding: 26px 30px; margin: 48px 0; box-shadow: 0 12px 35px rgba(0,0,0,0.5); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:20px;">
      <div style="max-width:780px;">
        <div style="display:inline-flex; align-items:center; gap:6px; background:rgba(212,175,55,0.12); color:var(--gold-bright); border:1px solid rgba(212,175,55,0.3); padding:3px 12px; border-radius:14px; font-size:0.78rem; font-weight:700; text-transform:uppercase; margin-bottom:8px;">
          <span>🎓 Post-School Collegiate Fellowship</span>
        </div>
        <h3 style="color:#ffffff; font-size:1.35rem; font-weight:800; margin-bottom:6px;">
          பள்ளிப் படிப்பை முடித்த சாதகர்களுக்கு: வேதாந்த வித்யாபீடம் — உயர்கல்விப் பட்டயம்
        </h3>
        <p style="color:#cbd5e1; font-size:0.92rem; line-height:1.7; margin:0;">
          ஆர்ஷ வித்யா, சின்மயா, மற்றும் ராமகிருஷ்ண மிஷன் உயர்கல்வி அமைப்புகளின் 5 முதன்மை ஆய்வுத் துறைகள்: பிரஸ்தானத்ரயம், விவேகசூடாமணி, சிவஞானபோதம், தர்க்க அளவையியல் &amp; பிரயோக வேதாந்தம்.
        </p>
      </div>
      <a href="higher-studies.html" class="sheet-btn sheet-btn-view" style="padding:12px 24px; font-size:0.95rem; font-weight:700; text-decoration:none; display:inline-flex; align-items:center; gap:8px; border-color:var(--gold);">
        <span>உயர்கல்வி வித்யாபீடம் ↗</span>
      </a>
    </section>
"""

    target = '    <!-- 6. DUAL-TRACK 12-GRADE ROADMAP TABLE -->'
    if target in text:
        text = text.replace(target, bridge_banner + '\n' + target)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Added higher studies bridge to {file_path}")

def add_graduation_to_tharam_12(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    if 'வேதாந்த வித்யாபீடம் — உயர்கல்விப் பட்டயம்' in text:
        print(f"Graduation bridge already in {file_path}")
        return

    bridge = """
            <!-- Post-Grade 12 Graduation Bridge to Higher Studies -->
            <div style="background: linear-gradient(135deg, rgba(8, 14, 26, 0.95), rgba(15, 23, 42, 0.95)); border: 1px solid rgba(212, 175, 55, 0.35); border-radius: 14px; padding: 22px 26px; margin: 28px 0; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
              <div>
                <div style="color:var(--gold-bright); font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">
                  🎓 பள்ளிப் பட்டய நிறைவு • GRADUATION COMPLETED
                </div>
                <div style="color:#ffffff; font-size:1.15rem; font-weight:800; margin-bottom:4px;">
                  அடுத்த கட்டம்: வேதாந்த வித்யாபீடம் — உயர்கல்விப் பட்டயம் (Higher Studies)
                </div>
                <div style="color:#94a3b8; font-size:0.88rem;">
                  12-ஆம் தரத்தை நிறைவு செய்த மாணவர்கள் பிரஸ்தானத்ரயம், விவேகசூடாமணி, சிவஞானபோதம் மற்றும் தர்க்கவியல் உயர் ஆய்வுகளைத் தொடரலாம்.
                </div>
              </div>
              <a href="higher-studies.html" class="sheet-btn sheet-btn-view" style="padding:10px 20px; font-weight:700; text-decoration:none; border-color:var(--gold);">
                உயர்கல்வி வித்யாபீடம் நுழைக ↗
              </a>
            </div>
"""

    target = '            <!-- Navigation Stepper Footer -->'
    # Insert in chapter 5 of tharam-12
    if target in text:
        parts = text.rsplit(target, 1)
        if len(parts) == 2:
            text = parts[0] + bridge + '\n' + target + parts[1]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Added graduation bridge to {file_path}")

def main():
    update_left_strip_for_higher_studies()

    for p in ['kalvi.html', 'site/kalvi.html', 'docs/kalvi.html']:
        if os.path.exists(p):
            add_higher_studies_to_kalvi(p)

    for p in ['school.html', 'site/school.html', 'docs/school.html']:
        if os.path.exists(p):
            add_higher_studies_bridge_to_school(p)

    for p in ['tharam-12.html', 'site/tharam-12.html', 'docs/tharam-12.html']:
        if os.path.exists(p):
            add_graduation_to_tharam_12(p)

if __name__ == '__main__':
    main()
