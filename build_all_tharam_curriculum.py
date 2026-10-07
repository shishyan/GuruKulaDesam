# -*- coding: utf-8 -*-
"""
Upgraded Guru Kula Desam Curriculum Coursebook Generator with Sidebar & Sections
Builds world-class, paced, interactive, visual school coursebooks for Grades 2 to 12.
Includes:
- Two-Column Layout with Sticky Course Navigation Sidebar
- Detailed Sections with Smooth-Scrolling Anchors
- Mobile Flyout Drawer for Chapter & Section Navigation
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
- Quick Grade Switcher Grid at the Sidebar Bottom
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
from curriculum_fusion import FUSION_DATA

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
    prev_label = f"← தரம் {prev_g}" if prev_g >= 1 else "← வாழ்வியல் மையம்"
    
    if next_g:
        next_link = f"tharam-{next_g}.html"
        next_label = f"தரம் {next_g} →"
    else:
        next_link = "kalvi.html"
        next_label = "வாழ்வியல் மையம் 🌿"

    units = data['units']
    total_units = len(units)

    # 1. Build Sidebar Navigation Groups with WBS Identification
    sidebar_groups_html = ""
    for idx, u in enumerate(units):
        active_group_class = "active" if idx == 0 else ""
        active_btn_class = "active" if idx == 0 else ""
        short_title = u['title'].split('—')[0].strip()
        
        sidebar_groups_html += f"""
        <div class="sidebar-chapter-group {active_group_class}" id="side-group-{u['num']}">
          <button type="button" class="sidebar-chapter-btn {active_btn_class}" id="side-btn-{u['num']}" onclick="selectChapter({u['num']})">
            <span class="sidebar-chapter-pill">
              <span class="sidebar-num">{g}.{u['num']}</span>
              <span>{short_title}</span>
            </span>
            <span class="sidebar-arrow">▶</span>
          </button>
          <div class="sidebar-subsections">
            <a href="#u{u['num']}-part1" class="sidebar-sub-link" onclick="goToSection({u['num']}, 'u{u['num']}-part1')">
              <span class="wbs-sidebar-code">{g}.{u['num']}.1</span>
              <span>📖 பாடம் &amp; பாடல்</span>
            </a>
            <a href="#u{u['num']}-part2" class="sidebar-sub-link" onclick="goToSection({u['num']}, 'u{u['num']}-part2')">
              <span class="wbs-sidebar-code">{g}.{u['num']}.2</span>
              <span>🎨 காட்சி &amp; வரலாறு</span>
            </a>
            <a href="#u{u['num']}-part3" class="sidebar-sub-link" onclick="goToSection({u['num']}, 'u{u['num']}-part3')">
              <span class="wbs-sidebar-code">{g}.{u['num']}.3</span>
              <span>🌿 வாழ்வியல் &amp; இல்லற தர்மம்</span>
            </a>
            <a href="#u{u['num']}-part4" class="sidebar-sub-link" onclick="goToSection({u['num']}, 'u{u['num']}-part4')">
              <span class="wbs-sidebar-code">{g}.{u['num']}.4</span>
              <span>✍️ பயிற்சி &amp; பதிவு</span>
            </a>
          </div>
        </div>
        """

    # If Grade 2, add Sheets tab to sidebar
    if g == 2 and grade2_sheets:
        sidebar_groups_html += f"""
        <div class="sidebar-chapter-group" id="side-group-sheets">
          <button type="button" class="sidebar-chapter-btn" id="side-btn-sheets" onclick="selectChapter('sheets')">
            <span class="sidebar-chapter-pill">
              <span class="sidebar-num">2.S</span>
              <span>பாடநூல் தாள்கள் ({len(grade2_sheets)})</span>
            </span>
          </button>
        </div>
        """

    # All Chapters option
    sidebar_groups_html += """
    <div class="sidebar-chapter-group" id="side-group-all">
      <button type="button" class="sidebar-chapter-btn" id="side-btn-all" onclick="selectChapter('all')">
        <span class="sidebar-chapter-pill">
          <span class="sidebar-num">📚</span>
          <span>முழு பாடநூல் பார்வை</span>
        </span>
      </button>
    </div>
    """

    # Quick Grade Switcher Grid at the Sidebar Bottom
    sidebar_grades_grid = ""
    for grade_i in range(1, 13):
        is_cur = "active" if grade_i == g else ""
        sidebar_grades_grid += f"""<a href="tharam-{grade_i}.html" class="sidebar-grade-pill {is_cur}">{grade_i}</a>"""

    # Top Tabs Stepper HTML
    top_tabs_html = ""
    for idx, u in enumerate(units):
        active_class = "active" if idx == 0 else ""
        short_title = u['title'].split('—')[0].strip()
        top_tabs_html += f"""
        <button type="button" class="course-tab-btn {active_class}" id="tab-btn-{u['num']}" onclick="selectChapter({u['num']})">
          <span class="course-tab-num">{g}.{u['num']}</span>
          <span>{short_title}</span>
        </button>
        """

    if g == 2 and grade2_sheets:
        top_tabs_html += """
        <button type="button" class="course-tab-btn" id="tab-btn-sheets" onclick="selectChapter('sheets')">
          <span class="course-tab-num">2.S</span>
          <span>பாடநூல் தாள்கள் (64)</span>
        </button>
        """

    top_tabs_html += """
    <button type="button" class="course-tab-btn" id="tab-btn-all" onclick="selectChapter('all')">
      <span class="course-tab-num">📚</span>
      <span>முழு பாடநூல் பார்வை</span>
    </button>
    """

    # 2. Build Lesson Panels with Distinct Section Anchors
    panels_html = ""
    for idx, u in enumerate(units):
        active_class = "active" if idx == 0 else ""
        enrichment = enrich_unit(g, u)
        
        # 1. Objectives & Vocabulary (for Phase 1 Intro Grid)
        obj_li = "".join([f"<li>{o}</li>" for o in enrichment['objectives']])
        
        vocab_items = ""
        for v in enrichment['vocab']:
            vocab_items += f"""
            <div class="vocab-clean-item">
              <strong>📌 {v['term']}:</strong> {v['meaning']}
            </div>
            """

        # 2. Paced Deep Dive Lessons (for Phase 1)
        deep_dive_html = ""
        for dd_idx, dd in enumerate(enrichment['deep_dive']):
            h_text = dd['heading'] if re.match(r'^\d+\.', dd['heading']) else f"{dd_idx+1}. {dd['heading']}"
            deep_dive_html += f"""
            <div class="lesson-step-section" style="margin-bottom: 20px;">
              <div class="lesson-step-title" style="color:#38bdf8; font-size:1.05rem; font-weight:700; margin-bottom:6px;">
                <span>{h_text}</span>
              </div>
              <div class="lesson-step-content" style="color:#cbd5e1; font-size:0.96rem; line-height:1.8;">
                <p>{text_to_html(dd['content'])}</p>
              </div>
            </div>
            """

        # 3. Formatted Verses & Texts
        formatted_verse = u['verse'].replace('\n', '<br>')
        formatted_meaning = text_to_html(u['meaning'])
        formatted_living = text_to_html(u['living'])
        formatted_story = text_to_html(u['story'])

        # 4. Diagram & Video Micro-Clip for Phase 2
        diagram_html = get_diagram_for_topic(enrichment['diagram_key'])

        video_card_html = ""
        if enrichment.get('video_clip'):
            v_clip = enrichment['video_clip']
            v_title = enrichment.get('video_title', 'பாடக் காட்சிக் குறும்படம்')
            v_note = enrichment.get('video_note', 'காட்சியைப் பார்த்து பாடக் கருத்தை உணருங்கள்.')
            v_poster = enrichment.get('video_poster', enrichment.get('hero_image', 'assets/images/lessons/temple_architecture.jpg'))
            video_card_html = f"""
            <div class="lesson-video-microclip-card" style="margin: 22px 0; background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.92)); border: 1px solid rgba(229, 169, 60, 0.4); border-radius: 16px; padding: 20px 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
              <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:14px; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:10px;">
                <div style="display:flex; align-items:center; gap:10px;">
                  <span style="font-size:1.4rem;">🎬</span>
                  <div>
                    <strong style="color:#ffffff; font-size:1rem; display:block;">காட்சிக் குறும்படம் (Cinematic Micro-Learning Film)</strong>
                    <span style="color:var(--gold-soft); font-size:0.86rem;">{v_title}</span>
                  </div>
                </div>
                <span style="background:rgba(229,169,60,0.15); color:var(--accent-gold); border:1px solid rgba(229,169,60,0.3); font-size:0.75rem; font-weight:700; padding:4px 12px; border-radius:12px;">HD FILM CLIP</span>
              </div>
              <div style="position:relative; border-radius:12px; overflow:hidden; background:#000; box-shadow:0 8px 24px rgba(0,0,0,0.6);">
                <video controls preload="metadata" poster="{v_poster}" style="width:100%; max-height:420px; display:block;" playsinline>
                  <source src="{v_clip}" type="video/mp4">
                  உங்கள் உலாவி வீடியோ இயக்கத்தை ஆதரிக்கவில்லை.
                </video>
              </div>
              <div style="margin-top:12px; font-size:0.88rem; color:#cbd5e1; line-height:1.6; background:rgba(0,0,0,0.25); padding:10px 14px; border-radius:8px; border-left:3px solid var(--accent-gold);">
                💡 <strong style="color:#38bdf8;">கற்றல் சிந்தனை:</strong> {v_note}
              </div>
            </div>
            """

        # 5. Vedic-STEM 21st Century Fusion for Phase 3
        fusion = FUSION_DATA.get((g, u['num']))
        fusion_html = ""
        if fusion:
            fusion_html = f"""
            <div style="background: rgba(0, 0, 0, 0.28); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 14px; padding: 18px 22px; margin-top: 18px;">
              <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:8px;">
                <strong style="color:#38bdf8; font-size:1rem; display:flex; align-items:center; gap:8px;">
                  <span>🌐 21-ஆம் நூற்றாண்டு நவீன அறிவியல் பார்வை (Vedic-STEM Fusion)</span>
                </strong>
                <span style="font-size:0.75rem; color:#2dd4bf; background:rgba(45,212,191,0.1); padding:2px 10px; border-radius:12px; font-weight:700;">அறிவியல் சிந்தனை</span>
              </div>
              <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:14px; margin-bottom:12px;">
                <div style="color:#cbd5e1; font-size:0.92rem; line-height:1.7;">
                  <strong style="color:#38bdf8;">🔬 அறிவியல் விளக்கம்:</strong><br>{fusion['science_correlation']}
                </div>
                <div style="color:#cbd5e1; font-size:0.92rem; line-height:1.7;">
                  <strong style="color:#2dd4bf;">🌍 வாழ்வியல் தேவை:</strong><br>{fusion['world_application']}
                </div>
              </div>
              <div style="background:rgba(212, 175, 55, 0.08); border-left:3px solid var(--gold); border-radius:8px; padding:10px 14px; color:var(--gold-soft); font-size:0.9rem; line-height:1.6;">
                {fusion['inquiry_lab']}
              </div>
            </div>
            """

        # 6. Interactive Quiz for Phase 4
        quiz_items = ""
        for q_idx, q in enumerate(enrichment['quiz']):
            quiz_items += f"""
            <div class="quiz-card" style="margin-bottom:12px;">
              <details>
                <summary style="padding:14px 18px; font-size:0.96rem;">
                  <span><strong>வினா {q_idx+1}:</strong> {q['q']}</span>
                  <span class="quiz-badge">விடையைக் காண்க ▾</span>
                </summary>
                <div class="quiz-body" style="padding:14px 18px;">
                  <div class="quiz-answer-highlight">✓ விடை: {q['a']}</div>
                  <div style="color:var(--text-muted); font-size:0.88rem; margin-top:4px;">💡 விளக்கம்: {q['hint']}</div>
                </div>
              </details>
            </div>
            """

        # 7. Daily Habits Checklist for Phase 4
        sadhana_items = ""
        for s_idx, s in enumerate(enrichment['sadhana']):
            sadhana_items += f"""
            <div class="sadhana-item" style="margin-bottom:8px;">
              <input type="checkbox" id="g{g}u{u['num']}s{s_idx}">
              <label for="g{g}u{u['num']}s{s_idx}" style="cursor:pointer;">
                <span>{s}</span>
              </label>
            </div>
            """

        # 8. LMS Chapter Completion Tracker for Phase 4
        lms_chapter_html = f"""
        <div class="lms-chapter-complete-bar" style="background:rgba(0, 0, 0, 0.35); border:1px solid rgba(56,189,248,0.25); border-radius:12px; padding:16px 20px; margin-top:20px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
          <div>
            <div style="color:#ffffff; font-weight:700; font-size:0.95rem; display:flex; align-items:center; gap:8px;">
              <span style="font-size:1.1rem;">🎓</span>
              <span>அத்தியாயம் {u['num']} கற்றல் நிறைவுப் பதிவு (Progress Tracker):</span>
            </div>
            <div style="color:#94a3b8; font-size:0.82rem; margin-top:2px;">இப்பாடத்தைப் படித்து முடித்ததும் 'பாடம் நிறைவுற்றது' என்பதை அழுத்தவும்.</div>
          </div>
          <button type="button" class="lms-mark-btn" id="lms-btn-{g}-{u['num']}" onclick="toggleChapterCompletion({g}, {u['num']})" style="background:rgba(56,189,248,0.12); border:1px solid rgba(56,189,248,0.4); color:#38bdf8; padding:8px 18px; border-radius:10px; font-weight:700; cursor:pointer; display:inline-flex; align-items:center; gap:8px; transition:all 0.2s ease;">
            <span class="lms-icon" id="lms-icon-{g}-{u['num']}">○</span>
            <span class="lms-text" id="lms-text-{g}-{u['num']}">பாடம் நிறைவுற்றது (+50 XP)</span>
          </button>
        </div>
        """

        # Stepper buttons
        prev_btn = ""
        if u['num'] > 1:
            prev_btn = f"""<button type="button" class="lesson-nav-btn lesson-nav-prev" onclick="selectChapter({u['num']-1})">← முந்தைய அத்தியாயம் {u['num']-1}</button>"""
        else:
            prev_btn = f"""<a href="{prev_link}" class="lesson-nav-btn lesson-nav-prev">{prev_label}</a>"""

        next_btn = ""
        if u['num'] < total_units:
            next_btn = f"""<button type="button" class="lesson-nav-btn lesson-nav-next" onclick="selectChapter({u['num']+1})">அடுத்த அத்தியாயம் {u['num']+1} →</button>"""
        else:
            if g == 2 and grade2_sheets:
                next_btn = """<button type="button" class="lesson-nav-btn lesson-nav-next" onclick="selectChapter('sheets')">பாடநூல் தாள்கள் காண்க 📖 →</button>"""
            else:
                next_btn = f"""<a href="{next_link}" class="lesson-nav-btn lesson-nav-next">{next_label}</a>"""

        panels_html += f"""
        <div class="lesson-unit-panel {active_class}" id="unit-panel-{u['num']}">
          <article class="lesson-card" id="unit-{u['num']}" style="background: rgba(14, 18, 26, 0.95); border: 1px solid var(--border-gold); border-radius: 18px; padding: 28px; margin-bottom: 30px; box-shadow: 0 10px 35px rgba(0,0,0,0.6);">
            
            <!-- Chapter Header -->
            <div class="lesson-card-head" style="margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.08);">
              <div>
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px; flex-wrap:wrap;">
                  <span class="wbs-code wbs-code-primary">அத்தியாயம் {u['num']} • Chapter {u['num']}</span>
                  <span style="background:rgba(56,189,248,0.12); color:#38bdf8; border:1px solid rgba(56,189,248,0.3); font-weight:700; font-size:0.82rem; padding:4px 12px; border-radius:12px;">WBS {g}.{u['num']}</span>
                </div>
                <div class="lesson-main-title" style="font-size:1.6rem; color:#ffffff; font-weight:800; margin-bottom:4px;">{u['title']}</div>
                <div class="lesson-sub-title" style="color:#94a3b8; font-size:0.95rem;">{u['sub']}</div>
              </div>
              <div style="color:#cbd5e1; font-size:0.88rem; font-weight:600; background:rgba(255,255,255,0.06); padding:6px 14px; border-radius:20px; border:1px solid rgba(255,255,255,0.12); display:flex; align-items:center; gap:6px;">
                <span class="wbs-code">GRADE {g:02d}</span>
                <span>{data['grade_tamil']} • {data['age_group']}</span>
              </div>
            </div>

            <!-- Sacred Lesson Hero Artwork Card -->
            <div class="lesson-hero-visual-card" style="margin-bottom: 24px; border-radius: 16px; overflow: hidden; border: 1px solid rgba(56,189,248,0.25); background: rgba(11, 17, 30, 0.7); box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
              <div style="position: relative; max-height: 380px; overflow: hidden;">
                <img src="{enrichment.get('hero_image', 'assets/images/lessons/temple_architecture.jpg')}" alt="{enrichment.get('hero_caption', u['title'])}" style="width: 100%; height: auto; display: block; object-fit: cover; max-height: 380px; transition: transform 0.4s ease;" loading="lazy">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(180deg, transparent 0%, rgba(11,17,30,0.92) 80%); padding: 20px 24px 14px; display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 8px;">
                  <div>
                    <span style="display: inline-block; background: rgba(56,189,248,0.2); color: #38bdf8; border: 1px solid rgba(56,189,248,0.4); padding: 3px 10px; border-radius: 10px; font-size: 0.78rem; font-weight: 700; margin-bottom: 4px;">🎨 கற்பித்தல் காட்சிப் படம் • Sacred Lesson Art</span>
                    <div style="color: #f8fafc; font-size: 0.96rem; font-weight: 600; line-height: 1.4;">{enrichment.get('hero_caption', u['title'])}</div>
                  </div>
                  <a href="{enrichment.get('hero_image', 'assets/images/lessons/temple_architecture.jpg')}" target="_blank" style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.25); color: #e2e8f0; font-size: 0.8rem; padding: 5px 12px; border-radius: 8px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px;">
                    <span>முழு அளவு ↗</span>
                  </a>
                </div>
              </div>
            </div>

            <!-- PHASE 1: பாடம் & மூலப் பாடல் -->
            <section class="learning-phase-card phase-1-card" id="u{u['num']}-part1">
              <div class="phase-header">
                <span class="phase-badge phase-badge-blue">பகுதி 1</span>
                <h3 class="phase-title">📖 பாட அறிமுகமும் மூலப் பாடலும் (Core Lesson &amp; Scripture)</h3>
              </div>

              <!-- Objectives & Key Vocabulary Split Grid -->
              <div class="intro-grid">
                <div class="objectives-compact">
                  <div class="intro-box-title">🎯 கற்றல் நோக்கங்கள் (Learning Focus):</div>
                  <ul class="objectives-list-clean">
                    {obj_li}
                  </ul>
                </div>
                <div class="vocab-compact">
                  <div class="intro-box-title">📌 முக்கிய சொற்களஞ்சியம் (Key Vocabulary):</div>
                  <div class="vocab-clean-list">
                    {vocab_items}
                  </div>
                </div>
              </div>

              <!-- Paced Detailed Lessons -->
              <div style="margin: 22px 0;">
                <div class="phase-sub-title">📚 படிமுறைப் பாட விளக்கம் (Detailed Paced Lessons):</div>
                {deep_dive_html}
              </div>

              <!-- Sacred Verse & Meaning -->
              <div class="verse-callout-clean">
                <div class="verse-callout-tag">🪔 மூலப் பாடல் / தேவாரம்:</div>
                <div class="verse-text-sacred">{formatted_verse}</div>
                <div class="verse-source-tag">— {u['source']}</div>
                <div class="verse-meaning-clean">
                  <strong style="color:var(--gold-soft);">💡 எளிய தத்துவப் பொழிப்புரை:</strong><br>{formatted_meaning}
                </div>
              </div>
            </section>

            <!-- PHASE 2: காட்சி & வரலாறு -->
            <section class="learning-phase-card phase-2-card" id="u{u['num']}-part2">
              <div class="phase-header">
                <span class="phase-badge phase-badge-purple">பகுதி 2</span>
                <h3 class="phase-title">🎨 காட்சி வரைபடமும் ஆன்மீக வரலாறும் (Visual &amp; History)</h3>
              </div>

              <!-- Visual Diagram -->
              <div style="margin: 16px 0;">
                <div class="phase-sub-title">🎨 காட்சி வரைபடம் &amp; கருத்துப் படிமம் (Visual Schema):</div>
                {diagram_html}
              </div>

              {video_card_html}

              <!-- Inspiring Historical / Puranic Story -->
              <div class="story-card-clean">
                <div class="phase-sub-title" style="margin-top:0; color:#c084fc;">📜 ஆன்மீக வரலாறு &amp; உத்வேகக் கதை (Inspirational Narrative):</div>
                <div class="story-content-text">{formatted_story}</div>
              </div>
            </section>

            <!-- PHASE 3: வாழ்வியல் தர்மமும் உன்னத இல்லற மாண்பும் -->
            <section class="learning-phase-card phase-3-card" id="u{u['num']}-part3">
              <div class="phase-header">
                <span class="phase-badge phase-badge-teal">பகுதி 3</span>
                <h3 class="phase-title">🌿 வாழ்வியல் தர்மமும் உன்னத இல்லற மாண்பும் (Living Dharma &amp; Family Nobility)</h3>
              </div>

              <!-- Sacred Dharma Callout -->
              <div style="background: rgba(45, 212, 191, 0.08); border: 1px solid rgba(45, 212, 191, 0.25); border-radius: 10px; padding: 12px 18px; margin-bottom: 16px; display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 1.5rem;">🏡</span>
                <div style="font-size: 0.88rem; color: #e2e8f0; line-height: 1.6;">
                  <strong style="color: #2dd4bf;">வாழ்வியல் நெறியின் தலையாய லட்சியம்:</strong> வெறும் ஏட்டுக் கல்வியோ போதனையோ அல்ல — நற்பண்புகள் நிறைந்த சான்றோனாக வளர்ந்து, உன்னத இல்லறத்தை அறவழியில் வழிநடத்துவதே அதிவேக முக்தி / நிர்வாணப் பாதை.
                </div>
              </div>

              <!-- Student Daily Conduct -->
              <div class="living-conduct-clean">
                <div class="phase-sub-title" style="margin-top:0; color:#2dd4bf;">🌿 மாணவர் அன்றாட இல்லற-வாழ்வியல் நெறி (Student Daily Living &amp; Conduct):</div>
                <div class="living-conduct-text">{formatted_living}</div>
              </div>

              <!-- Vedic-STEM Fusion -->
              {fusion_html}
            </section>

            <!-- PHASE 4: சுயபயிற்சியும் சாதனைப் பதிவும் -->
            <section class="learning-phase-card phase-4-card" id="u{u['num']}-part4">
              <div class="phase-header">
                <span class="phase-badge phase-badge-gold">பகுதி 4</span>
                <h3 class="phase-title">✍️ சுயபயிற்சி, பதிக இசை &amp; படிப்புப் பதிவு (Review &amp; Progress)</h3>
              </div>

              <!-- Interactive Quiz -->
              <div style="margin: 16px 0;">
                <div class="phase-sub-title">❓ சுய பரிசோதனை வினாடி-வினா (Self-Check Quiz):</div>
                <p style="color:var(--text-muted); font-size:0.88rem; margin-bottom:12px;">வினாவை வாசித்து விடையைச் சிந்தியுங்கள்; பின்னர் 'விடையைக் காண்க' என்பதை அழுத்தி சரிபார்க்கவும்.</p>
                {quiz_items}
              </div>

              <!-- Daily Habits Checklist -->
              <div style="background: rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 18px 22px; margin: 18px 0;">
                <div class="phase-sub-title" style="margin-top:0; color:#fbbf24;">✅ மாணவர் தினசரி தர்ம சாதனைப் பட்டியல் (Daily Habit Checklist):</div>
                {sadhana_items}
              </div>

              <!-- Devotional Audio Link -->
              <div class="audio-clean-wrapper">
                <div>
                  <strong style="color:#ffffff;">🎵 இப்பாடத்திற்கான திருமுறைப் பதிக இசை</strong>
                  <div style="color:var(--text-muted); font-size:0.85rem; margin-top:2px;">இறை இசையைக் கேட்டு மன அமைதி பெறுங்கள்.</div>
                </div>
                <a href="irai-isai-virundhu.html" class="sheet-btn sheet-btn-view" style="text-decoration:none; padding:8px 18px;">
                  பாடலைக் கேட்க ↗
                </a>
              </div>

              <!-- LMS Chapter Completion Bar -->
              {lms_chapter_html}
            </section>

            <!-- Navigation Stepper Footer -->
            <div class="lesson-nav-footer">
              {prev_btn}
              <button type="button" onclick="window.print()" class="lesson-nav-btn lesson-nav-prev" style="border-color:rgba(255,255,255,0.15); color:#cbd5e1;">
                🖨️ அத்தியாயம் அச்சிடுக (Print / PDF)
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
                <button type="button" class="sheet-btn sheet-btn-view" onclick="openSheetModal('{img_url}', {p_num}, 'சைவ நெறி தரம் 2', 'தரம் 2')">
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
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px; flex-wrap:wrap;">
              <span class="wbs-code wbs-code-primary">WBS 2.S</span>
              <span class="source-badge">அங்கீகரிக்கப்பட்ட பாடநூல் படங்கள் • மொத்தம் {len(grade2_sheets)} பக்கங்கள்</span>
            </div>
            <h3 style="color:#f8fafc; font-size:1.4rem; margin-top:8px;">தரம் 2 முழுமையான பாடநூல் பக்கங்கள் (Official Textbook Sheets)</h3>
            <p style="color:var(--text-muted); font-size:0.92rem; margin-top:6px;">
              எந்தவொரு பக்கத்தின் மீதும் கிளிக் செய்து பெரிய அளவில் வாசிக்கலாம் (Click any sheet to zoom and read in high resolution).
            </p>
          </div>
          <div class="sheets-grid">
            {sheet_cards}
          </div>
          <div class="lesson-nav-footer">
            <button type="button" class="lesson-nav-btn lesson-nav-prev" onclick="selectChapter(5)">← அத்தியாயம் 5 திரும்புக</button>
            <a href="tharam-3.html" class="lesson-nav-btn lesson-nav-next">தரம் 3 காண்க (Grade 3) →</a>
          </div>
        </div>
        """

    # Assemble complete page HTML with the 2-Column Sidebar & Sections Layout
    html_content = f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>வாழ்வியல் நெறி — {data['grade_tamil']} ({data['grade_eng']} Coursebook) | Guru Kula Desam</title>
  <meta name="description" content="வாழ்வியல் நெறி &amp; உன்னத இல்லற தர்மப் பாடநூல் {data['grade_tamil']}. {data['hero_desc']}">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body class="has-left-strip">

  <!-- LEFT STRIP BAR (PRIMARY MOBILE-STYLE MENU OVERLAY) -->
  <aside class="left-strip-bar" id="leftStripBar" aria-label="முதன்மை பட்டி">
    <div class="strip-header">
      <a href="index.html" class="strip-brand-link" title="குரு குல தேசம்">
        <span class="strip-emblem">ॐ</span>
        <span class="strip-brand-text">குரு குல தேசம்</span>
      </a>
      <button type="button" class="strip-toggle-btn" id="stripToggleBtn" onclick="closePrimaryMenu()" title="பட்டி மூடுக" aria-label="Close Menu">
        <span class="strip-toggle-icon">✕</span>
      </button>
    </div>

    <nav class="strip-nav-list" id="stripNavList">

      <!-- 1. முகப்பு (Home) -->
      <div class="strip-group" data-group="home">
        <a href="index.html" class="strip-item" data-tooltip="முகப்பு">
          <span class="strip-item-icon">🏠</span>
          <span class="strip-item-label">முகப்பு (Home)</span>
        </a>
      </div>

      <!-- 2. வாழ்வியல் நெறி (Dharmic Way of Living & Curriculum) -->
      <div class="strip-group active" data-group="kalvi">
        <a href="kalvi.html" class="strip-item strip-has-sub" data-tooltip="வாழ்வியல் நெறி">
          <span class="strip-item-icon">🌿</span>
          <span class="strip-item-label">வாழ்வியல் நெறி &amp; பாடங்கள்</span>
          <span class="strip-sub-indicator">▾</span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header">வாழ்வியல் &amp; இல்லற தர்மம்</div>
          <a href="kalvi.html" class="strip-sub-item"><span class="strip-sub-icon">🏛️</span><span>வாழ்வியல் மையம் (12 நிலைகள்)</span></a>
          <a href="school.html" class="strip-sub-item"><span class="strip-sub-icon">🏫</span><span>இணையப் பள்ளி போர்டல்</span></a>
          <a href="higher-studies.html" class="strip-sub-item"><span class="strip-sub-icon">🔬</span><span>வேத-நவீன உயர்கல்வி</span></a>
          <a href="virtues.html" class="strip-sub-item"><span class="strip-sub-icon">🔤</span><span>அகர வரிசை நற்பண்புகள்</span></a>
          <a href="syllabus.html" class="strip-sub-item"><span class="strip-sub-icon">📚</span><span>முழு பாடத்திட்டம்</span></a>
          <a href="classes.html" class="strip-sub-item"><span class="strip-sub-icon">⏰</span><span>வகுப்புகள் அட்டவணை</span></a>
          <div class="strip-sub-header" style="margin-top:6px;">12 வாழ்வியல் நிலைகள் (Grades 1-12)</div>
          <div class="strip-grades-mini-grid">
            <a href="tharam-1.html" class="strip-grade-mini-pill">1</a>
            <a href="tharam-2.html" class="strip-grade-mini-pill">2</a>
            <a href="tharam-3.html" class="strip-grade-mini-pill">3</a>
            <a href="tharam-4.html" class="strip-grade-mini-pill">4</a>
            <a href="tharam-5.html" class="strip-grade-mini-pill">5</a>
            <a href="tharam-6.html" class="strip-grade-mini-pill">6</a>
            <a href="tharam-7.html" class="strip-grade-mini-pill">7</a>
            <a href="tharam-8.html" class="strip-grade-mini-pill">8</a>
            <a href="tharam-9.html" class="strip-grade-mini-pill">9</a>
            <a href="tharam-10.html" class="strip-grade-mini-pill">10</a>
            <a href="tharam-11.html" class="strip-grade-mini-pill">11</a>
            <a href="tharam-12.html" class="strip-grade-mini-pill">12</a>
          </div>
        </div>
      </div>

      <!-- 3. சைவ நெறி & தெய்வங்கள் (Saiva Neri & Deities) -->
      <div class="strip-group" data-group="saivam">
        <a href="saiva-neri.html" class="strip-item strip-has-sub" data-tooltip="சைவ நெறி">
          <span class="strip-item-icon">🕉️</span>
          <span class="strip-item-label">சைவ நெறி &amp; தெய்வங்கள்</span>
          <span class="strip-sub-indicator">▾</span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header">சைவ நெறி &amp; தெய்வங்கள்</div>
          <a href="saiva-neri.html" class="strip-sub-item"><span class="strip-sub-icon">🔱</span><span>சைவ சித்தாந்தம் &amp; நெறி</span></a>
          <a href="vinayagar.html" class="strip-sub-item"><span class="strip-sub-icon">🐘</span><span>முழுமுதற் கடவுள் விநாயகர்</span></a>
          <a href="murugan.html" class="strip-sub-item"><span class="strip-sub-icon">🪶</span><span>தமிழ் தெய்வம் முருகன்</span></a>
          <a href="sakthi.html" class="strip-sub-item"><span class="strip-sub-icon">🌸</span><span>அம்பிகை சக்தி நெறி</span></a>
          <a href="vaishnava.html" class="strip-sub-item"><span class="strip-sub-icon">🪷</span><span>அரங்கன் &amp; கிருஷ்ணர் வைணவம்</span></a>
        </div>
      </div>

      <!-- 4. இறை இசை விருந்து (Devotional Music) -->
      <div class="strip-group" data-group="isai">
        <a href="irai-isai-virundhu.html" class="strip-item strip-has-sub" data-tooltip="இறை இசை">
          <span class="strip-item-icon">🎵</span>
          <span class="strip-item-label">இறை இசை விருந்து</span>
          <span class="strip-sub-indicator">▾</span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header">இறை இசை &amp; பாடல்கள்</div>
          <a href="irai-isai-virundhu.html" class="strip-sub-item"><span class="strip-sub-icon">🎶</span><span>இறை இசை விருந்து (580)</span></a>
          <a href="youtube.html" class="strip-sub-item"><span class="strip-sub-icon">▶️</span><span>காணொளிகள் களஞ்சியம்</span></a>
        </div>
      </div>

      <!-- 5. அறநெறி & தத்துவம் (Dharma & Scripture) -->
      <div class="strip-group" data-group="dharma">
        <a href="thirukkural.html" class="strip-item strip-has-sub" data-tooltip="அறநெறி">
          <span class="strip-item-icon">📖</span>
          <span class="strip-item-label">அறநெறி &amp; தத்துவம்</span>
          <span class="strip-sub-indicator">▾</span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header">அறநெறி &amp; வாழ்வியல்</div>
          <a href="thirukkural.html" class="strip-sub-item"><span class="strip-sub-icon">📜</span><span>திருக்குறள் (1330 குறள்கள்)</span></a>
          <a href="sanmargam.html" class="strip-sub-item"><span class="strip-sub-icon">🪔</span><span>சுத்த சன்மார்க்கம் (வள்ளலார்)</span></a>
        </div>
      </div>

      <!-- 6. குருவருள் & அறிமுகம் (Guru & About) -->
      <div class="strip-group" data-group="about">
        <a href="about.html" class="strip-item strip-has-sub" data-tooltip="குருவருள்">
          <span class="strip-item-icon">🏛️</span>
          <span class="strip-item-label">குருவருள் &amp; அறிமுகம்</span>
          <span class="strip-sub-indicator">▾</span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header">குருவருள் &amp; தகவல்</div>
          <a href="about.html" class="strip-sub-item"><span class="strip-sub-icon">🙏</span><span>மகா பெரியவா அருளுரைகள்</span></a>
          <a href="google-site.html" class="strip-sub-item"><span class="strip-sub-icon">🌐</span><span>கூகிள் தளம் நேரடி இணைப்பு</span></a>
        </div>
      </div>

    </nav>

    <div class="strip-footer-dock">
      <button type="button" class="strip-dock-btn" onclick="openUserSettingsModal('preferences')" title="அமைப்புகள்">
        <span class="strip-dock-icon">⚙️</span>
        <span class="strip-dock-label">அமைப்புகள்</span>
      </button>
      <button type="button" class="strip-dock-btn profile-dock-btn" onclick="openUserSettingsModal('profile')" title="சுயவிவரம்">
        <span class="strip-dock-avatar" id="stripAvatarIcon">👤</span>
        <span class="strip-dock-label" id="stripUserName">சுயவிவரம்</span>
      </button>
    </div>
  </aside>

  <div class="strip-backdrop" id="stripBackdrop" onclick="closePrimaryMenu()"></div>

  <!-- CONTEXT-SENSITIVE TOP BAR -->
  <header class="context-top-bar" id="contextTopBar">
    <div class="context-bar-container">
      <button type="button" class="primary-hamburger-btn" onclick="togglePrimaryMenu()" title="முதன்மை பட்டி (6 பிரிவுகள்)" aria-label="முதன்மை பட்டி">
        <span class="hb-icon">☰</span>
        <span class="hb-emblem">ॐ</span>
        <span class="hb-label">முதன்மை பட்டி</span>
      </button>
      <nav class="context-tabs-nav" id="contextTabsNav" aria-label="Section Tabs">
        <button type="button" class="context-tab-pill active" onclick="selectChapter(1)"><span class="context-tab-pill-icon">📖</span><span>அத்தியாயம் 1</span></button>
        <button type="button" class="context-tab-pill" onclick="selectChapter(2)"><span class="context-tab-pill-icon">📖</span><span>அத்தியாயம் 2</span></button>
        <button type="button" class="context-tab-pill" onclick="selectChapter(3)"><span class="context-tab-pill-icon">📖</span><span>அத்தியாயம் 3</span></button>
        <button type="button" class="context-tab-pill" onclick="selectChapter(4)"><span class="context-tab-pill-icon">📖</span><span>அத்தியாயம் 4</span></button>
        <button type="button" class="context-tab-pill" onclick="selectChapter(5)"><span class="context-tab-pill-icon">📖</span><span>அத்தியாயம் 5</span></button>
        <a href="{prev_link}" class="context-tab-pill"><span class="context-tab-pill-icon">⏮️</span><span>{prev_label}</span></a>
        <a href="{next_link}" class="context-tab-pill"><span class="context-tab-pill-icon">⏭️</span><span>{next_label}</span></a>
        <a href="kalvi.html" class="context-tab-pill"><span class="context-tab-pill-icon">🌿</span><span>வாழ்வியல் மையம்</span></a>
      </nav>
      <div class="context-actions">
        <button type="button" class="context-profile-pill" onclick="openUserSettingsModal('profile')" title="பயனர் சுயவிவரம் &amp; அமைப்புகள்">
          <span class="context-avatar-dot"></span>
          <span class="context-user-name">மாணவர்</span>
          <span>⚙️</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Site Header -->
  <header class="site-header">
    <div class="header-container">
      <a href="index.html" class="brand" aria-label="Guru Kula Desam Home">
        <div class="brand-emblem">🔱</div>
        <div class="brand-text">
          <h1>குரு குல தேசம்</h1>
          <span>Guru Kula Desam <span class="brand-sub-extra">• வேத &amp; சைவ வாழ்வியல் நெறி</span></span>
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
            <span>வாழ்வியல் (Grades 1-12)</span>
            <span class="dropdown-arrow">▾</span>
          </button>
          <div class="dropdown-menu kalvi-menu" id="kalviDropdownMenu">
            <a href="kalvi.html" class="dropdown-item" style="grid-column: 1 / -1; border-bottom: 1px solid var(--border-subtle); margin-bottom: 4px;">
              <span class="dropdown-item-icon">🌿</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">வாழ்வியல் நெறி மையம் (Living the Dharma Hub)</div>
                <div class="dropdown-item-desc">சான்றாண்மை, உன்னத இல்லற தர்மம் &amp; அதிவேக முக்திப் பாதை</div>
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
    
    <!-- Hero Banner with WBS Grade Code -->
    <div class="hero-banner">
      <div class="sacred-tag">
        <span class="wbs-code">WBS G{g:02d}</span>
        🌿 {data['grade_tamil']} • வாழ்வியல் நெறி &amp; இல்லற தர்மப் பாடநூல் 🌿
      </div>
      <h1>வாழ்வியல் நெறி — {data['grade_tamil']} ({data['grade_eng']})</h1>
      <h2>Vedic &amp; Saiva Dharmic Living Coursebook — {data['age_group']}</h2>
      <div class="verse-quote">"அறத்தாற்றின் இல்வாழ்க்கை ஆற்றின் புறத்தாற்றின் போஒய்ப் பெறுவ தெவன்?" — திருக்குறள் 46</div>
      <p class="hero-desc">
        {data['hero_desc']}
      </p>
    </div>

    <!-- Course Metadata Bar -->
    <div class="course-header-meta">
      <div class="course-meta-badge"><span class="wbs-code">WBS G{g:02d}</span> நிலை: <strong>{data['age_group']}</strong></div>
      <div class="course-meta-badge">🌿 பாடநெறி: <strong>வாழ்வியல் நெறி &amp; உன்னத இல்லற தர்மம்</strong></div>
      <div class="course-meta-badge">🧩 அலகுகள்: <strong>{total_units} விரிவான அத்தியாயங்கள்</strong></div>
      <div class="course-meta-badge">👑 லட்சியம்: <strong>சான்றாண்மை &amp; இல்லற வழி முக்தி</strong></div>
    </div>

    <!-- Quick Grade Switcher Bar -->
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin: 15px 0 25px 0; padding: 14px 20px; background:var(--bg-card); border-radius:12px; border:1px solid var(--border-gold);">
      <a href="{prev_link}" style="color:var(--gold); text-decoration:none; font-weight:600;">{prev_label}</a>
      <span style="color:var(--text-muted); font-size:0.9rem;">{data['grade_tamil']} / 12</span>
      <a href="{next_link}" style="color:#ffffff; text-decoration:none; font-weight:700;">{next_label}</a>
    </div>

    <!-- Anchor for scrolling -->
    <div id="course-content-start"></div>



    <!-- Two-Column Layout Container: Sticky Sidebar + Main Content Column -->
    <div class="course-layout-container">
      
      <!-- Left Course Navigation Sidebar (Dedicated Sub-Menu for Kalvi Group) -->
      <aside class="course-sidebar dedicated-sub-sidebar" id="courseSidebar">
        <div class="sidebar-header">
          <div class="dedicated-sub-header">
            <span class="dedicated-group-pill">🌿 வாழ்வியல் நெறி (Dharmic Living)</span>
          </div>
          <span class="sidebar-grade-badge">{data['grade_tamil']} வாழ்வியல் நெறி</span>
          <h3 class="sidebar-title">பாடப் பொருளடக்கம்</h3>
          <p class="sidebar-sub">அத்தியாயங்கள் &amp; உட்பிரிவுகள் (Sections)</p>
        </div>

        <!-- Sidebar Navigation List -->
        <nav class="sidebar-nav" aria-label="Course Sections">
          {sidebar_groups_html}
        </nav>

        <!-- Quick Grade Switcher in Sidebar -->
        <div class="sidebar-other-grades">
          <div class="sidebar-other-grades-title">அனைத்து 12 தரங்கள் (Jump to Grade):</div>
          <div class="sidebar-grades-grid">
            {sidebar_grades_grid}
          </div>
        </div>
      </aside>

      <!-- Main Course Column -->
      <div class="course-main-column">
        {panels_html}
      </div>

    </div>

  </main>

  <!-- Mobile Floating Drawer Toggle Button & Backdrop -->
  <button type="button" class="course-sidebar-mobile-toggle" onclick="toggleCourseSidebar()" aria-label="பொருளடக்கம் காண்க">
    📋 பொருளடக்கம் (Sections)
  </button>
  <div class="course-sidebar-overlay" id="courseSidebarOverlay" onclick="closeCourseSidebar()"></div>

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
        <h4>வாழ்வியல் நெறி &amp; பாடங்கள்</h4>
        <ul class="footer-links">
          <li><a href="kalvi.html">வாழ்வியல் மையம் (Grades 1 - 12)</a></li>
          <li><a href="tharam-1.html">தரம் 1 — பாலப் பருவ வாழ்வியல் நெறி</a></li>
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
    function selectChapter(unitNum) {{
      const panels = document.querySelectorAll('.lesson-unit-panel');
      panels.forEach(p => p.classList.remove('active'));
      
      const tabs = document.querySelectorAll('.course-tab-btn');
      tabs.forEach(t => t.classList.remove('active'));

      const sideGroups = document.querySelectorAll('.sidebar-chapter-group');
      sideGroups.forEach(g => g.classList.remove('active'));

      const sideBtns = document.querySelectorAll('.sidebar-chapter-btn');
      sideBtns.forEach(b => b.classList.remove('active'));
      
      if (unitNum === 'all') {{
        panels.forEach(p => p.classList.add('active'));
        const allBtn = document.getElementById('tab-btn-all');
        if (allBtn) allBtn.classList.add('active');
        const sideAll = document.getElementById('side-group-all');
        if (sideAll) sideAll.classList.add('active');
      }} else if (unitNum === 'sheets') {{
        const sheetsPanel = document.getElementById('unit-panel-sheets');
        const sheetsTab = document.getElementById('tab-btn-sheets');
        const sideSheets = document.getElementById('side-group-sheets');
        if (sheetsPanel) sheetsPanel.classList.add('active');
        if (sheetsTab) sheetsTab.classList.add('active');
        if (sideSheets) sideSheets.classList.add('active');
      }} else {{
        const targetPanel = document.getElementById('unit-panel-' + unitNum);
        const targetTab = document.getElementById('tab-btn-' + unitNum);
        const sideGroup = document.getElementById('side-group-' + unitNum);
        const sideBtn = document.getElementById('side-btn-' + unitNum);
        if (targetPanel) targetPanel.classList.add('active');
        if (targetTab) targetTab.classList.add('active');
        if (sideGroup) sideGroup.classList.add('active');
        if (sideBtn) sideBtn.classList.add('active');
      }}
      
      closeCourseSidebar();
      const targetStart = document.getElementById('course-content-start');
      if (targetStart) {{
        targetStart.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }}
    }}

    function goToSection(unitNum, sectionId) {{
      selectChapter(unitNum);
      closeCourseSidebar();
      setTimeout(() => {{
        const el = document.getElementById(sectionId);
        if (el) {{
          el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        }}
      }}, 50);
    }}

    function toggleCourseSidebar() {{
      const sidebar = document.getElementById('courseSidebar');
      const overlay = document.getElementById('courseSidebarOverlay');
      if (sidebar && overlay) {{
        const isOpen = sidebar.classList.contains('open');
        if (isOpen) {{
          sidebar.classList.remove('open');
          overlay.classList.remove('active');
          document.body.style.overflow = '';
        }} else {{
          sidebar.classList.add('open');
          overlay.classList.add('active');
          document.body.style.overflow = 'hidden';
        }}
      }}
    }}

    function closeCourseSidebar() {{
      const sidebar = document.getElementById('courseSidebar');
      const overlay = document.getElementById('courseSidebarOverlay');
      if (sidebar && overlay) {{
        sidebar.classList.remove('open');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
      }}
    }}
  </script>
</body>
</html>
"""
    return html_content

def main():
    print("Building comprehensive school curriculum coursebooks with Sidebar & Sections for Tharams 2 to 12...")
    
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

    print("\nAll 11 Grade Coursebooks successfully generated with Sidebar & Sections navigation!")

if __name__ == '__main__':
    main()
