# -*- coding: utf-8 -*-
"""
Upgraded Guru Kula Desam Curriculum Coursebook Generator
Builds world-class, paced, interactive, visual school coursebooks for Grades 2 to 12.
Includes:
- Interactive Chapter Stepper & Navigation Tabs (Go slow, one topic at a time)
- Pedagogical Learning Objectives (கற்றல் நோக்கங்கள்)
- Key Vocabulary Builder (சொற்களஞ்சியம்)
- Step-by-Step Paced In-depth Lessons with Subheadings (படிமுறை விளக்கம்)
- Responsive Custom SVG Visual Diagrams (காட்சி விளக்கம்)
- Sacred Verses / Mantras with Word-by-Word Breakdown (பதவுரை & பொழிப்புரை)
- Engaging Puranic & Historical Stories (ஆன்மீக வரலாறு)
- Student Dharmic Living Rules (வாழ்வியல் தர்மம்)
- Interactive Self-Test Quizzes with Instant Reveal (சுய பரிசோதனை வினாடி-வினா)
- Daily Student Sadhana Checklist (தினசரி தர்ம சாதனைப் பட்டியல்)
- Devotional Audio Links (இறை இசை விருந்து)
- Grade 2 Scanned Textbook Reader (64 Sheets Gallery with Zoom Modal)
"""

import sys
import os
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

from curriculum_data_primary_middle import GRADES_2_TO_6
from curriculum_data_secondary_advanced import GRADES_7_TO_12
from visual_diagrams import get_diagram_for_topic
from curriculum_enricher import enrich_unit

# Combine all grades
ALL_GRADES = {}
ALL_GRADES.update(GRADES_2_TO_6)
ALL_GRADES.update(GRADES_7_TO_12)

# Load Grade 2 scanned sheets if available
grade2_sheets = []
if os.path.exists('grade2_images.json'):
    with open('grade2_images.json', 'r', encoding='utf-8') as f:
        grade2_sheets = json.load(f)

def text_to_html(text):
    if not text:
        return ""
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color:var(--gold-soft);">\1</strong>', text)
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        line_s = line.strip()
        if line_s.startswith('•') or line_s.startswith('-'):
            formatted_lines.append(f"<div style='margin-left:14px; margin-top:5px;'>• {line_s.lstrip('•- ')}</div>")
        elif re.match(r'^\d+\.', line_s):
            formatted_lines.append(f"<div style='margin-left:14px; margin-top:6px;'>{line_s}</div>")
        else:
            formatted_lines.append(line)
    return "<br>".join(formatted_lines)

def build_grade_coursebook(g, data):
    prev_g = g - 1
    next_g = g + 1 if g < 12 else None
    
    prev_link = f"tharam-{prev_g}.html" if prev_g >= 1 else "kalvi.html"
    prev_label = f"← முந்தைய தரம்: தரம் {prev_g}" if prev_g >= 1 else "← அனைத்து தரங்கள் (Kalvi Hub)"
    
    if next_g:
        next_link = f"tharam-{next_g}.html"
        next_label = f"அடுத்த தரம்: தரம் {next_g} (Grade {next_g}) →"
    else:
        next_link = "kalvi.html"
        next_label = "கல்வித் தளம் (Curriculum Hub) 🎓"

    units = data['units']
    total_units = len(units)

    # Tabs HTML
    tabs_html = ""
    for idx, u in enumerate(units):
        active_class = "active" if idx == 0 else ""
        tabs_html += f"""
        <button class="course-tab-btn {active_class}" id="tab-btn-{u['num']}" onclick="switchChapter({u['num']})">
          <span class="course-tab-num">{u['num']}</span>
          <span>{u['title'].split('—')[0].strip()}</span>
        </button>
        """

    # If Grade 2, add Sheets tab
    if g == 2 and grade2_sheets:
        tabs_html += """
        <button class="course-tab-btn" id="tab-btn-sheets" onclick="switchChapter('sheets')">
          <span class="course-tab-num">📖</span>
          <span>பாடநூல் தாள்கள் (64 பக்கங்கள்)</span>
        </button>
        """

    # Full view tab
    tabs_html += """
    <button class="course-tab-btn" id="tab-btn-all" onclick="switchChapter('all')">
      <span class="course-tab-num">📚</span>
      <span>முழு பாடநூல் பார்வை (Full Course)</span>
    </button>
    """

    # Panels HTML
    panels_html = ""
    for idx, u in enumerate(units):
        active_class = "active" if idx == 0 else ""
        enrichment = enrich_unit(g, u)
        
        # Objectives HTML
        obj_li = "".join([f"<li>{o}</li>" for o in enrichment['objectives']])
        objectives_html = f"""
        <div class="objectives-card">
          <div class="objectives-title">🎯 இப்பாடத்தின் கற்றல் நோக்கங்கள் (Learning Objectives):</div>
          <ul class="objectives-list">
            {obj_li}
          </ul>
        </div>
        """

        # Vocab HTML
        vocab_cards = ""
        for v in enrichment['vocab']:
            vocab_cards += f"""
            <div class="vocab-card">
              <div class="vocab-term">📌 {v['term']}</div>
              <div class="vocab-meaning">{v['meaning']}</div>
            </div>
            """
        vocab_html = f"""
        <div class="vocab-section">
          <h4 style="color:var(--gold); font-size:1.1rem; margin-bottom:6px; display:flex; align-items:center; gap:8px;">
            <span>📖</span> <span>சொற்களஞ்சியம் &amp; கலைச்சொல் விளக்கம் (Key Terminology):</span>
          </h4>
          <div class="vocab-grid">
            {vocab_cards}
          </div>
        </div>
        """

        # Deep Dive Subsections (Paced, Slow)
        deep_dive_html = ""
        for dd in enrichment['deep_dive']:
            deep_dive_html += f"""
            <div class="lesson-step-section">
              <div class="lesson-step-title">{dd['heading']}</div>
              <div class="lesson-step-content">
                <p>{text_to_html(dd['content'])}</p>
              </div>
            </div>
            """

        # Visual Diagram
        diagram_html = get_diagram_for_topic(enrichment['diagram_key'])

        # Formatted Verse
        formatted_verse = u['verse'].replace('\n', '<br>')
        formatted_meaning = text_to_html(u['meaning'])
        formatted_living = text_to_html(u['living'])
        formatted_story = text_to_html(u['story'])

        # Interactive Quiz HTML
        quiz_items = ""
        for q_idx, q in enumerate(enrichment['quiz']):
            quiz_items += f"""
            <div class="quiz-card">
              <details>
                <summary>
                  <span><strong>வினா {q_idx+1}:</strong> {q['q']}</span>
                  <span class="quiz-badge">விடையைக் காண்க ▾</span>
                </summary>
                <div class="quiz-body">
                  <div class="quiz-answer-highlight">✓ விடை: {q['a']}</div>
                  <div style="color:var(--text-muted); font-size:0.88rem; margin-top:4px;">💡 விளக்கம் / குறிப்பு: {q['hint']}</div>
                </div>
              </details>
            </div>
            """
        quiz_section_html = f"""
        <div class="quiz-section">
          <h4 style="color:var(--gold-bright); font-size:1.15rem; margin-bottom:14px; display:flex; align-items:center; gap:8px;">
            <span>❓</span> <span>சுய பரிசோதனை வினாடி-வினா (Interactive Self-Learning Check):</span>
          </h4>
          <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:12px;">
            கேள்வியை வாசித்து உங்கள் விடையைச் சிந்தியுங்கள்; பின்னர் 'விடையைக் காண்க' என்பதை அழுத்திச் சரிபார்க்கவும்.
          </p>
          {quiz_items}
        </div>
        """

        # Daily Sadhana Checklist HTML
        sadhana_items = ""
        for s_idx, s in enumerate(enrichment['sadhana']):
            sadhana_items += f"""
            <div class="sadhana-item">
              <input type="checkbox" id="g{g}u{u['num']}s{s_idx}">
              <label for="g{g}u{u['num']}s{s_idx}">{s}</label>
            </div>
            """
        sadhana_html = f"""
        <div class="sadhana-box">
          <div class="sadhana-header">
            <span>🌿</span> <span>மாணவர் தினசரி தர்ம சாதனைப் பட்டியல் (Daily Dharmic Habits Checklist)</span>
          </div>
          {sadhana_items}
        </div>
        """

        # Stepper buttons
        prev_btn = ""
        if u['num'] > 1:
            prev_btn = f"""<button class="lesson-nav-btn lesson-nav-prev" onclick="switchChapter({u['num']-1})">← முந்தைய பாடம் {u['num']-1}</button>"""
        else:
            prev_btn = f"""<a href="{prev_link}" class="lesson-nav-btn lesson-nav-prev">{prev_label}</a>"""

        next_btn = ""
        if u['num'] < total_units:
            next_btn = f"""<button class="lesson-nav-btn lesson-nav-next" onclick="switchChapter({u['num']+1})">அடுத்த பாடம் {u['num']+1} →</button>"""
        else:
            if g == 2 and grade2_sheets:
                next_btn = """<button class="lesson-nav-btn lesson-nav-next" onclick="switchChapter('sheets')">பாடநூல் தாள்கள் காண்க 📖 →</button>"""
            else:
                next_btn = f"""<a href="{next_link}" class="lesson-nav-btn lesson-nav-next">{next_label}</a>"""

        panels_html += f"""
        <div class="lesson-unit-panel {active_class}" id="unit-panel-{u['num']}">
          <article class="lesson-card" id="unit-{u['num']}" style="background: rgba(18, 22, 28, 0.92); border: 1px solid var(--border-gold); border-radius: 18px; padding: 32px; margin-bottom: 30px; box-shadow: 0 10px 35px rgba(0,0,0,0.6);">
            
            <div class="lesson-card-head">
              <div>
                <span style="background:var(--gold-gradient); color:#0a0c10; font-weight:800; font-size:0.85rem; padding:6px 16px; border-radius:14px; text-transform:uppercase; letter-spacing:0.5px;">அத்தியாயம் {u['num']} (Chapter {u['num']})</span>
                <div class="lesson-main-title" style="margin-top:12px;">{u['title']}</div>
                <div class="lesson-sub-title">{u['sub']}</div>
              </div>
              <div style="color:var(--gold-bright); font-size:0.9rem; font-weight:600; background:rgba(212,175,55,0.1); padding:6px 14px; border-radius:20px; border:1px solid var(--border-gold);">
                {data['grade_tamil']} • {data['age_group']}
              </div>
            </div>

            <!-- 1. Learning Objectives -->
            {objectives_html}

            <!-- 2. Vocabulary Builder -->
            {vocab_html}

            <!-- 3. Visual SVG Diagram / Infographic -->
            {diagram_html}

            <!-- 4. Paced Step-by-Step Deep Dive Sections -->
            <div style="margin: 28px 0;">
              <h4 style="color:var(--gold-bright); font-size:1.2rem; margin-bottom:8px; display:flex; align-items:center; gap:8px;">
                <span>📚</span> <span>படிமுறைப் பாட விளக்கம் (Paced Course Lessons):</span>
              </h4>
              <p style="color:var(--text-muted); font-size:0.92rem; margin-bottom:16px;">
                ஒவ்வொரு கருத்தையும் நிதானமாகப் படித்து, அன்றாட வாழ்வியலோடு பொருத்திப் பாருங்கள்.
              </p>
              {deep_dive_html}
            </div>

            <!-- 5. Sacred Verse / Mantra Box -->
            <div style="background:rgba(212,175,55,0.08); border-left:4px solid var(--gold); padding:20px 24px; border-radius:0 14px 14px 0; margin:28px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
              <div style="font-size:0.82rem; color:var(--gold-soft); text-transform:uppercase; letter-spacing:1px; margin-bottom:10px; font-weight:700;">📖 மூலப் பாடல் / வேத மந்திரம் &amp; சந்த கானம்:</div>
              <div style="font-family:'Mukta Malar', serif; font-size:1.2rem; color:#fff; line-height:1.9; font-weight:600;">{formatted_verse}</div>
              <div style="font-size:0.9rem; color:var(--gold-bright); margin-top:10px; font-weight:600;">— {u['source']}</div>
            </div>

            <!-- 6. Philosophical Meaning -->
            <div style="margin: 24px 0; background: rgba(255,255,255,0.02); padding:20px; border-radius:12px; border:1px solid var(--border-subtle);">
              <h4 style="color:var(--gold); font-size:1.15rem; margin-bottom:10px; display:flex; align-items:center; gap:8px;">
                <span>💡</span> <span>பதவுரை &amp; தத்துவப் பொழிப்புரை (Spiritual Essence):</span>
              </h4>
              <div style="color:var(--text-main); line-height:1.85; font-size:1.02rem;">{formatted_meaning}</div>
            </div>

            <!-- 7. Inspirational Story -->
            <div style="margin: 28px 0; background:rgba(224,159,62,0.06); border-radius:14px; padding:22px; border:1px solid rgba(224,159,62,0.25);">
              <h4 style="color:var(--amber); font-size:1.15rem; margin-bottom:10px; display:flex; align-items:center; gap:8px;">
                <span>📜</span> <span>ஆன்மீக வரலாறு / உத்வேகக் கதை (Inspirational Puranic &amp; Historic Event):</span>
              </h4>
              <div style="color:var(--text-main); line-height:1.85; font-size:1rem;">{formatted_story}</div>
            </div>

            <!-- 8. Dharmic Living in Daily Life -->
            <div style="margin: 28px 0; background:rgba(42,157,143,0.08); border-radius:14px; padding:22px; border:1px solid rgba(42,157,143,0.3);">
              <h4 style="color:#2a9d8f; font-size:1.15rem; margin-bottom:10px; display:flex; align-items:center; gap:8px;">
                <span>🌿</span> <span>மாணவர் வாழ்வியல் தர்மம் &amp; ஒழுக்க நெறிமுறை (Student Daily Conduct):</span>
              </h4>
              <div style="color:var(--text-main); line-height:1.85; font-size:1rem;">{formatted_living}</div>
            </div>

            <!-- 9. Daily Dharmic Habits Checklist -->
            {sadhana_html}

            <!-- 10. Self-Learning Interactive Quiz -->
            {quiz_section_html}

            <!-- 11. Audio Link to Hymns -->
            <div style="background:rgba(212,175,55,0.06); border:1px solid var(--border-gold); border-radius:12px; padding:16px 20px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-top:24px;">
              <div>
                <strong style="color:var(--gold-bright);">🎵 இப்பாடத்திற்கான திருமுறைப் பதிகம்:</strong>
                <div style="color:var(--text-muted); font-size:0.88rem; margin-top:3px;">குரு குல தேசம் இசை அலைவரிசையில் கேட்டு மனதை அமைதிப்படுத்துங்கள்.</div>
              </div>
              <a href="irai-isai-virundhu.html" class="sheet-btn sheet-btn-view" style="text-decoration:none; padding:8px 18px;">
                பாடலைக் கேட்க ↗
              </a>
            </div>

            <!-- Navigation Stepper Footer -->
            <div class="lesson-nav-footer">
              {prev_btn}
              <button onclick="window.print()" class="lesson-nav-btn lesson-nav-prev" style="border-color:var(--border-gold); color:var(--gold-soft);">
                🖨️ பாடம் அச்சிடுக (Print / PDF)
              </button>
              {next_btn}
            </div>

          </article>
        </div>
        """

    # If Grade 2, render Scanned Sheets Panel
    if g == 2 and grade2_sheets:
        sheet_cards = ""
        for s_idx, img_url in enumerate(grade2_sheets):
            p_num = s_idx + 1
            sheet_cards += f"""
            <div class="sheet-card">
              <div class="sheet-header">
                <span>பக்கம் {p_num}</span>
                <span style="font-size:0.75rem; color:var(--text-muted);">தரம் 2</span>
              </div>
              <div class="sheet-thumb" onclick="openSheetModal('{img_url}', {p_num}, 'சைவ நெறி தரம் 2', 'தரம் 2')">
                <img src="{img_url}" loading="lazy" alt="தரம் 2 சைவ நெறி - பக்கம் {p_num}">
                <div class="sheet-zoom-overlay">🔍</div>
              </div>
              <div class="sheet-actions">
                <button class="sheet-btn sheet-btn-view" onclick="openSheetModal('{img_url}', {p_num}, 'சைவ நெறி தரம் 2', 'தரம் 2')">
                  🔍 பெரிதாக்குக
                </button>
                <a href="https://sites.google.com/view/wwwgurukuladesamcom/home/%E0%AE%9A%E0%AE%B5-%E0%AE%A8%E0%AE%B1/%E0%AE%A4%E0%AE%B0%E0%AE%AE-2" target="_blank" rel="noopener" class="sheet-btn sheet-btn-direct" title="கூகிள் தளத்தில் காண்க">
                  Google Site ↗
                </a>
              </div>
            </div>
            """
        
        panels_html += f"""
        <div class="lesson-unit-panel" id="unit-panel-sheets">
          <div class="scripture-study-section" style="margin-bottom:24px;">
            <span class="source-badge">அங்கீகரிக்கப்பட்ட பாடநூல் படங்கள் • மொத்தம் {len(grade2_sheets)} பக்கங்கள்</span>
            <h3 style="color:var(--gold-bright); font-size:1.4rem; margin-top:8px;">தரம் 2 முழுமையான பாடநூல் பக்கங்கள் (Official Textbook Sheets)</h3>
            <p style="color:var(--text-muted); font-size:0.92rem; margin-top:6px;">
              எந்தவொரு பக்கத்தின் மீதும் கிளிக் செய்து பெரிய அளவில் வாசிக்கலாம் (Click any sheet to zoom and read in high resolution).
            </p>
          </div>
          <div class="sheets-grid">
            {sheet_cards}
          </div>
          <div class="lesson-nav-footer">
            <button class="lesson-nav-btn lesson-nav-prev" onclick="switchChapter(5)">← அத்தியாயம் 5 திரும்புக</button>
            <a href="tharam-3.html" class="lesson-nav-btn lesson-nav-next">தரம் 3 காண்க (Grade 3) →</a>
          </div>
        </div>
        """

    # Assemble complete page HTML
    html_content = f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{data['grade_tamil']} ({data['grade_eng']} Coursebook) | Guru Kula Desam</title>
  <meta name="description" content="சைவ நெறி &amp; வேத வாழ்வியல் பாடநூல் {data['grade_tamil']}. {data['hero_desc']}">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

  <!-- Site Header -->
  <header class="site-header">
    <div class="header-container">
      <a href="index.html" class="brand" aria-label="Guru Kula Desam Home">
        <div class="brand-emblem">🔱</div>
        <div class="brand-text">
          <h1>குரு குல தேசம்</h1>
          <span>Guru Kula Desam <span class="brand-sub-extra">• வேத &amp; சைவ வாழ்வியல் கல்வி</span></span>
        </div>
      </a>
      <button class="mobile-toggle" id="mobileNavToggle" onclick="toggleMobileNav()" aria-label="பட்டி (Menu)" aria-expanded="false">☰</button>
      <div class="nav-overlay" id="navOverlay" onclick="closeMobileNav()"></div>
      <nav class="main-nav" id="mainNav">
        <a href="index.html" class="nav-link">முகப்பு</a>
        <a href="saiva-neri.html" class="nav-link">சைவ நெறி</a>

        <!-- Kalvi (Grades 1-12) Dropdown -->
        <div class="nav-dropdown active" id="kalviDropdown">
          <button class="nav-link dropdown-toggle active" id="kalviDropdownBtn" onclick="toggleDropdown(event, 'kalviDropdown')" aria-haspopup="true" aria-expanded="false">
            <span>கல்வி (Grades 1-12)</span>
            <span class="dropdown-arrow">▾</span>
          </button>
          <div class="dropdown-menu kalvi-menu" id="kalviDropdownMenu">
            <a href="kalvi.html" class="dropdown-item" style="grid-column: 1 / -1; border-bottom: 1px solid var(--border-subtle); margin-bottom: 4px;">
              <span class="dropdown-item-icon">🏛️</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">சைவ நெறி கல்வித் தளம் (Curriculum Hub)</div>
                <div class="dropdown-item-desc">தரம் 1 முதல் 12 வரையிலான முழுமையான பாடநெறி</div>
              </div>
            </a>
            <a href="irai-isai-virundhu.html" class="dropdown-item" style="grid-column: 1 / -1; border-bottom: 1px solid var(--border-subtle); margin-bottom: 4px;">
              <span class="dropdown-item-icon">🎵</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">இறை இசை விருந்து (Syllabus Music)</div>
                <div class="dropdown-item-desc">தேவாரம், திருப்புகழ், விநாயகர் &amp; சிவபுராண இசை அமுது</div>
              </div>
            </a>
            <a href="tharam-1.html" class="dropdown-item">
              <span class="dropdown-item-icon">📖</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 1 (Grade 1)</div></div>
            </a>
            <a href="tharam-2.html" class="dropdown-item {'active' if g == 2 else ''}">
              <span class="dropdown-item-icon">🪔</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 2 (Grade 2)</div></div>
            </a>
            <a href="tharam-3.html" class="dropdown-item {'active' if g == 3 else ''}">
              <span class="dropdown-item-icon">🔱</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 3 (Grade 3)</div></div>
            </a>
            <a href="tharam-4.html" class="dropdown-item {'active' if g == 4 else ''}">
              <span class="dropdown-item-icon">📜</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 4 (Grade 4)</div></div>
            </a>
            <a href="tharam-5.html" class="dropdown-item {'active' if g == 5 else ''}">
              <span class="dropdown-item-icon">🌺</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 5 (Grade 5)</div></div>
            </a>
            <a href="tharam-6.html" class="dropdown-item {'active' if g == 6 else ''}">
              <span class="dropdown-item-icon">🕉️</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 6 (Grade 6)</div></div>
            </a>
            <a href="tharam-7.html" class="dropdown-item {'active' if g == 7 else ''}">
              <span class="dropdown-item-icon">🔔</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 7 (Grade 7)</div></div>
            </a>
            <a href="tharam-8.html" class="dropdown-item {'active' if g == 8 else ''}">
              <span class="dropdown-item-icon">✨</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 8 (Grade 8)</div></div>
            </a>
            <a href="tharam-9.html" class="dropdown-item {'active' if g == 9 else ''}">
              <span class="dropdown-item-icon">⚜️</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 9 (Grade 9)</div></div>
            </a>
            <a href="tharam-10.html" class="dropdown-item {'active' if g == 10 else ''}">
              <span class="dropdown-item-icon">🌟</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 10 (Grade 10)</div></div>
            </a>
            <a href="tharam-11.html" class="dropdown-item {'active' if g == 11 else ''}">
              <span class="dropdown-item-icon">🔱</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 11 (Grade 11)</div></div>
            </a>
            <a href="tharam-12.html" class="dropdown-item {'active' if g == 12 else ''}">
              <span class="dropdown-item-icon">👑</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 12 (Grade 12)</div></div>
            </a>
          </div>
        </div>

        <a href="thirukkural.html" class="nav-link">திருக்குறள்</a>
        <a href="sanmargam.html" class="nav-link">சன்மார்க்கம்</a>
        <a href="syllabus.html" class="nav-link">பாடத்திட்டம்</a>
        <a href="classes.html" class="nav-link">வகுப்புகள்</a>
      </nav>
    </div>
  </header>

  <main class="main-content">
    
    <!-- Hero Banner -->
    <div class="hero-banner">
      <div class="sacred-tag">📖 {data['grade_tamil']} • பாடநூல் &amp; சுயகற்றல் பயிற்சி நெறி 📖</div>
      <h1>சைவ நெறி — {data['grade_tamil']} ({data['grade_eng']})</h1>
      <h2>Vedic &amp; Saiva Dharmic Living Coursebook — {data['age_group']}</h2>
      <div class="verse-quote">"{data['verse_quote']}"</div>
      <p class="hero-desc">
        {data['hero_desc']}
      </p>
    </div>

    <!-- Course Metadata Bar -->
    <div class="course-header-meta">
      <div class="course-meta-badge">📚 பாடநெறி: <strong>சைவ நெறி &amp; வேத வாழ்வியல்</strong></div>
      <div class="course-meta-badge">🎯 நிலை: <strong>{data['age_group']}</strong></div>
      <div class="course-meta-badge">🧩 அலகுகள்: <strong>{total_units} விரிவான அத்தியாயங்கள்</strong></div>
      <div class="course-meta-badge">🎨 காட்சி விளக்கங்கள்: <strong>அனைத்து அத்தியாயங்களிலும் உண்டு</strong></div>
    </div>

    <!-- Quick Grade Switcher Bar -->
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin: 15px 0 25px 0; padding: 14px 20px; background:var(--bg-card); border-radius:12px; border:1px solid var(--border-gold);">
      <a href="{prev_link}" style="color:var(--gold); text-decoration:none; font-weight:600;">{prev_label}</a>
      <span style="color:var(--text-muted); font-size:0.9rem;">{data['grade_tamil']} / 12</span>
      <a href="{next_link}" style="color:var(--gold-bright); text-decoration:none; font-weight:700;">{next_label}</a>
    </div>

    <!-- Anchor for scrolling -->
    <div id="course-content-start"></div>

    <!-- Chapter Navigation Stepper (Tabs for Paced Learning) -->
    <div class="course-tabs-wrapper">
      <div style="font-size:0.85rem; color:var(--gold-bright); font-weight:700; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.5px;">
        📌 அத்தியாயத் தேர்வு (Select Chapter to Study at your own pace):
      </div>
      <div class="course-tabs">
        {tabs_html}
      </div>
    </div>

    <!-- Lesson Panels Container -->
    <div class="course-panels-container">
      {panels_html}
    </div>

  </main>

  <!-- Sheet Zoom Modal -->
  <div class="sheet-modal-overlay" id="sheetModal" onclick="closeSheetModal()">
    <div class="sheet-modal-content" onclick="event.stopPropagation()">
      <div class="sheet-modal-header">
        <div class="sheet-modal-title" id="sheetModalTitle">பாடநூல் பக்கம்</div>
        <button class="sheet-modal-close" onclick="closeSheetModal()" aria-label="மூடுக">✕</button>
      </div>
      <div class="sheet-modal-body">
        <img src="" id="sheetModalImg" alt="பெரிதாக்கப்பட்ட பாடப் படம்">
      </div>
    </div>
  </div>

  <!-- Site Footer -->
  <footer class="site-footer">
    <div class="footer-container">
      <div class="footer-col">
        <h4>குரு குல தேசம் (Guru Kula Desam)</h4>
        <p>வேதங்கள், பன்னிரு திருமுறைகள், சைவ சித்தாந்த சாத்திரங்கள், காஞ்சி மகா பெரியவா அருளுரைகள் மற்றும் வள்ளலார் பெருமானின் சுத்த சன்மார்க்க நெறிகளை உலகிற்கு பறைசாற்றும் ஆன்மீக இசை &amp; கல்விப் பெருவெளி.</p>
        <p style="margin-top: 10px; color: var(--gold); font-weight: 600;">அன்பே சிவம் • யாதும் ஊரே யாவரும் கேளிர் • ஏகன் அநேகன்</p>
      </div>
      <div class="footer-col">
        <h4>சைவ நெறி கல்வி &amp; பாடங்கள்</h4>
        <ul class="footer-links">
          <li><a href="kalvi.html">சைவ நெறி கல்வித் தளம் (Grades 1 - 12)</a></li>
          <li><a href="tharam-1.html">தரம் 1 — 60 பாடப் படங்கள் &amp; நூல்கள்</a></li>
          <li><a href="tharam-2.html">தரம் 2 — சிவ சின்னங்கள் &amp; ஆலய வழிபாடு</a></li>
          <li><a href="tharam-6.html">தரம் 6 — பதி-பசு-பாசம் &amp; திருமுறைகள்</a></li>
          <li><a href="tharam-10.html">தரம் 10 — சைவ சித்தாந்தம் (O/L)</a></li>
          <li><a href="tharam-12.html">தரம் 12 — உபநிடதங்கள் &amp; நடராஜ தத்துவம் (A/L)</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>ஆன்மீக வழிகள் &amp; இசை</h4>
        <ul class="footer-links">
          <li><a href="saiva-neri.html">சிவ நெறி (172 திருமுறைப் பாடல்கள்)</a></li>
          <li><a href="thirukkural.html">திருக்குறள் (185 அதிகாரப் படங்கள் &amp; இசை)</a></li>
          <li><a href="sanmargam.html">சன்மார்க்கம் (94 அருட்பெருஞ்சோதிப் பாடல்கள்)</a></li>
          <li><a href="murugan.html">முருக நெறி &amp; சக்தி நெறி</a></li>
          <li><a href="youtube.html">YouTube இசை &amp; பாடல்கள்</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      &copy; 2026 குரு குல தேசம் (Guru Kula Desam) | gurukuladesam.com | அனைத்து உரிமைகளும் இறைப்பணிக்கே சமர்ப்பணம்.
    </div>
  </footer>

  <script src="assets/data/catalog.js"></script>
  <script src="assets/js/main.js"></script>
  <script>
    function switchChapter(unitNum) {{
      const panels = document.querySelectorAll('.lesson-unit-panel');
      panels.forEach(p => p.classList.remove('active'));
      
      const tabs = document.querySelectorAll('.course-tab-btn');
      tabs.forEach(t => t.classList.remove('active'));
      
      if (unitNum === 'all') {{
        panels.forEach(p => p.classList.add('active'));
        const allBtn = document.getElementById('tab-btn-all');
        if (allBtn) allBtn.classList.add('active');
      }} else if (unitNum === 'sheets') {{
        const sheetsPanel = document.getElementById('unit-panel-sheets');
        const sheetsTab = document.getElementById('tab-btn-sheets');
        if (sheetsPanel) sheetsPanel.classList.add('active');
        if (sheetsTab) sheetsTab.classList.add('active');
      }} else {{
        const targetPanel = document.getElementById('unit-panel-' + unitNum);
        const targetTab = document.getElementById('tab-btn-' + unitNum);
        if (targetPanel) targetPanel.classList.add('active');
        if (targetTab) targetTab.classList.add('active');
      }}
      
      const targetStart = document.getElementById('course-content-start');
      if (targetStart) {{
        targetStart.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }}
    }}
  </script>
</body>
</html>
"""
    return html_content

def main():
    print("Building comprehensive school curriculum coursebooks for Tharams 2 to 12...")
    
    for g in sorted(ALL_GRADES.keys()):
        data = ALL_GRADES[g]
        html = build_grade_coursebook(g, data)
        filename = f"tharam-{g}.html"
        
        # Write to root
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
            
        # Write to site/
        site_path = os.path.join('site', filename)
        with open(site_path, 'w', encoding='utf-8') as f:
            f.write(html)
            
        # Write to docs/
        docs_path = os.path.join('docs', filename)
        with open(docs_path, 'w', encoding='utf-8') as f:
            f.write(html)
            
        print(f"Generated {filename} ({len(html)} bytes) across root, site/, and docs/")

    print("\nAll 11 Grade Coursebooks successfully generated!")

if __name__ == '__main__':
    main()
