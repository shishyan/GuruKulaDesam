# -*- coding: utf-8 -*-
"""
Curriculum HTML Generator for Gurukuladesam
Builds rich, progressive, student-appropriate curriculum pages for Grades 2 to 12
in site/, docs/, and root .
"""

import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

from curriculum_data_primary_middle import GRADES_2_TO_6
from curriculum_data_secondary_advanced import GRADES_7_TO_12

# Combine all grades
ALL_GRADES = {}
ALL_GRADES.update(GRADES_2_TO_6)
ALL_GRADES.update(GRADES_7_TO_12)

def text_to_html(text):
    if not text:
        return ""
    # Convert **bold** to <strong>bold</strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color:var(--gold-soft);">\1</strong>', text)
    # Convert \n• or \n- to list items or styled lines
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        line_s = line.strip()
        if line_s.startswith('•') or line_s.startswith('-'):
            formatted_lines.append(f"<div style='margin-left:12px; margin-top:4px;'>• {line_s.lstrip('•- ')}</div>")
        elif re.match(r'^\d+\.', line_s):
            formatted_lines.append(f"<div style='margin-left:12px; margin-top:6px;'>{line_s}</div>")
        else:
            formatted_lines.append(line)
    return "<br>".join(formatted_lines)

def generate_tharam_html(g, data):
    prev_g = g - 1
    next_g = g + 1 if g < 12 else None
    
    prev_link = f"tharam-{prev_g}.html" if prev_g >= 1 else "kalvi.html"
    prev_label = f"← முந்தைய தரம்: தரம் {prev_g}" if prev_g >= 1 else "← அனைத்து தரங்கள்"
    
    if next_g:
        next_link = f"tharam-{next_g}.html"
        next_label = f"அடுத்த தரம்: தரம் {next_g} (Grade {next_g}) →"
    else:
        next_link = "kalvi.html"
        next_label = "கல்வித் தளம் (Curriculum Hub) 🎓"

    # Build syllabus summary bullets HTML
    summary_html = "".join([f"<li style='margin-bottom:8px;'><strong>{b.split(':')[0]}:</strong>{':'.join(b.split(':')[1:]) if ':' in b else ''}</li>" for b in data['summary_bullets']])

    # Build Lesson Units HTML
    units_html = ""
    for u in data['units']:
        q_html = "".join([f"<li style='margin-bottom:6px;'>{q}</li>" for q in u['questions']])
        
        # Format verse lines with line breaks
        formatted_verse = u['verse'].replace('\n', '<br>')
        formatted_meaning = text_to_html(u['meaning'])
        formatted_living = text_to_html(u['living'])
        formatted_story = text_to_html(u['story'])
        
        units_html += f"""
      <article class="lesson-card" id="unit-{u['num']}" style="background: rgba(18, 22, 28, 0.9); border: 1px solid var(--border-gold); border-radius: 16px; padding: 28px; margin-bottom: 30px; box-shadow: 0 6px 24px rgba(0,0,0,0.5);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:16px; border-bottom:1px solid rgba(212,175,55,0.25); padding-bottom:12px;">
          <span style="background:var(--gold-gradient); color:#0a0c10; font-weight:800; font-size:0.85rem; padding:5px 14px; border-radius:14px; text-transform:uppercase; letter-spacing:0.5px;">பாட அலகு {u['num']}</span>
          <span style="color:var(--gold-soft); font-size:0.9rem; font-weight:600;">{u['sub']}</span>
        </div>

        <h3 style="color:var(--gold-bright); font-size:1.45rem; margin-bottom:16px; font-weight:700;">{u['title']}</h3>
        
        <!-- Sacred Verse / Vedic Mantra Box -->
        <div style="background:rgba(212,175,55,0.08); border-left:4px solid var(--gold); padding:16px 20px; border-radius:0 12px 12px 0; margin-bottom:20px;">
          <div style="font-size:0.8rem; color:var(--gold-soft); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px; font-weight:700;">📖 மூலப் பாடல் / வேத மந்திர மேற்கோள்:</div>
          <div style="font-family:'Mukta Malar', serif; font-size:1.18rem; color:#fff; line-height:1.85; font-style:normal; font-weight:600;">{formatted_verse}</div>
          <div style="font-size:0.88rem; color:var(--gold-light); margin-top:8px; font-weight:500;">— {u['source']}</div>
        </div>

        <!-- Philosophical Meaning -->
        <div style="margin-bottom:18px;">
          <h4 style="color:var(--gold); font-size:1.1rem; margin-bottom:8px; display:flex; align-items:center; gap:8px;">
            <span>💡</span> <span>தத்துவ விளக்கம் &amp; ஆழமான பொருளுரை (Spiritual Essence):</span>
          </h4>
          <div style="color:var(--text-main); line-height:1.85; font-size:1rem; margin-left:4px;">{formatted_meaning}</div>
        </div>

        <!-- Dharmic Way of Living -->
        <div style="margin-bottom:18px; background:rgba(42,157,143,0.06); border-radius:10px; padding:16px; border:1px solid rgba(42,157,143,0.2);">
          <h4 style="color:#2a9d8f; font-size:1.1rem; margin-bottom:8px; display:flex; align-items:center; gap:8px;">
            <span>🌿</span> <span>மாணவர் வாழ்வியல் தர்மம் &amp; அன்றாடப் பயிற்சி (Dharmic Living in Daily Life):</span>
          </h4>
          <div style="color:var(--text-main); line-height:1.85; font-size:0.98rem; margin:0;">{formatted_living}</div>
        </div>

        <!-- Puranic / Historic / Saint Story -->
        <div style="margin-bottom:20px; background:rgba(230,57,70,0.05); border-radius:10px; padding:16px; border:1px solid rgba(230,57,70,0.18);">
          <h4 style="color:#f28482; font-size:1.1rem; margin-bottom:8px; display:flex; align-items:center; gap:8px;">
            <span>📜</span> <span>ஆன்மீக வரலாறு &amp; வழிகாட்டும் நிகழ்வு (Inspirational Story):</span>
          </h4>
          <div style="color:var(--text-main); line-height:1.85; font-size:0.98rem; margin:0;">{formatted_story}</div>
        </div>

        <!-- Self-Reflection Questions -->
        <div style="background:rgba(255,255,255,0.03); border:1px dashed var(--border-gold); border-radius:10px; padding:16px 20px;">
          <strong style="color:var(--gold-bright); font-size:0.95rem; display:block; margin-bottom:8px;">❓ சிந்தனை வினாக்கள் &amp; சுய மதிப்பீடு (Self-Reflection Questions):</strong>
          <ol style="margin-left:22px; color:var(--text-muted); line-height:1.75; font-size:0.92rem;">
            {q_html}
          </ol>
        </div>
      </article>
"""

    html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>சைவ நெறி — {data['grade_tamil']} ({data['grade_eng']}) | Guru Kula Desam</title>
  <meta name="description" content="குரு குல தேசம் சைவ நெறி {data['grade_tamil']}. {data['hero_desc']}">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

  <header class="site-header">
    <div class="header-container">
      <a href="index.html" class="brand" aria-label="Guru Kula Desam Home">
        <div class="brand-emblem">ॐ</div>
        <div class="brand-text">
          <h1>குரு குல தேசம்</h1>
          <span>Guru Kula Desam <span class="brand-sub-extra">• வேத &amp; சைவ நெறி</span></span>
        </div>
      </a>
      <button class="mobile-toggle" id="mobileNavToggle" onclick="toggleMobileNav()" aria-label="பட்டி (Menu)" aria-expanded="false">☰</button>
      <div class="nav-overlay" id="navOverlay" onclick="closeMobileNav()"></div>
      <nav class="main-nav" id="mainNav">
        <a href="index.html" class="nav-link ">முகப்பு</a>
        <a href="saiva-neri.html" class="nav-link ">சைவ நெறி</a>

        <!-- Kalvi (Grades 1-12) Dropdown -->
        <div class="nav-dropdown " id="kalviDropdown">
          <button class="nav-link dropdown-toggle " id="kalviDropdownBtn" onclick="toggleDropdown(event, 'kalviDropdown')" aria-haspopup="true" aria-expanded="false">
            <span>கல்வி (Grades 1-12)</span>
            <span class="dropdown-arrow">▾</span>
          </button>
          <div class="dropdown-menu kalvi-menu" id="kalviDropdownMenu">
            <a href="kalvi.html" class="dropdown-item " style="grid-column: 1 / -1; border-bottom: 1px solid var(--border-subtle); margin-bottom: 4px;">
              <span class="dropdown-item-icon">🏛️</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">சைவ நெறி கல்வித் தளம் (Curriculum Hub)</div>
                <div class="dropdown-item-desc">தரம் 1 முதல் 12 வரையிலான முழுமையான பாடநெறி</div>
              </div>
            </a>
            <a href="irai-isai-virundhu.html" class="dropdown-item " style="grid-column: 1 / -1; border-bottom: 1px solid var(--border-subtle); margin-bottom: 4px;">
              <span class="dropdown-item-icon">🎵</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">இறை இசை விருந்து (Syllabus Music)</div>
                <div class="dropdown-item-desc">தேவாரம், திருப்புகழ், விநாயகர் &amp; சிவபுராண இசை அமுது</div>
              </div>
            </a>
            <a href="tharam-1.html" class="dropdown-item ">
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

        <!-- Traditions Dropdown -->
        <div class="nav-dropdown " id="traditionsDropdown">
          <button class="nav-link dropdown-toggle" id="traditionsDropdownBtn" onclick="toggleDropdown(event, 'traditionsDropdown')" aria-haspopup="true" aria-expanded="false">
            <span>வழிபாட்டு நெறிகள்</span>
            <span class="dropdown-arrow">▾</span>
          </button>
          <div class="dropdown-menu" id="traditionsDropdownMenu">
            <a href="murugan.html" class="dropdown-item ">
              <span class="dropdown-item-icon">🔱</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">முருகன் (Kaumaram)</div>
                <div class="dropdown-item-desc">கந்த சஷ்டி, திருப்புகழ் &amp; கானங்கள்</div>
              </div>
            </a>
            <a href="sakthi.html" class="dropdown-item ">
              <span class="dropdown-item-icon">🌸</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">சக்தி (Shaktham)</div>
                <div class="dropdown-item-desc">அபிராமி அந்தாதி &amp; லலிதா போற்றிகள்</div>
              </div>
            </a>
            <a href="vinayagar.html" class="dropdown-item ">
              <span class="dropdown-item-icon">🐘</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">விநாயகர் (Ganapathyam)</div>
                <div class="dropdown-item-desc">விநாயகர் அகவல் &amp; மூல கணபதி பதிகங்கள்</div>
              </div>
            </a>
            <a href="vaishnava.html" class="dropdown-item ">
              <span class="dropdown-item-icon">🪷</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">வைணவம் (Vaishnavam)</div>
                <div class="dropdown-item-desc">விஷ்ணு, கிருஷ்ணர் &amp; திவ்வியப் பிரபந்தம்</div>
              </div>
            </a>
          </div>
        </div>

        <a href="thirukkural.html" class="nav-link ">திருக்குறள்</a>
        <a href="sanmargam.html" class="nav-link ">சன்மார்க்கம்</a>
        <a href="irai-isai-virundhu.html" class="nav-link ">இறை இசை</a>
        <a href="syllabus.html" class="nav-link ">பாடத்திட்டம்</a>
        <a href="classes.html" class="nav-link ">வகுப்புகள்</a>
        <a href="about.html" class="nav-link ">பெரியவா தரிசனம்</a>
        <a href="https://sites.google.com/view/wwwgurukuladesamcom" target="_blank" rel="noopener" class="nav-link" style="border: 1px solid var(--border-gold); padding: 5px 12px; border-radius: 16px; color: var(--gold-bright);">🌐 கூகிள் தளம் ↗</a>
        <a href="https://www.youtube.com/@guru-kula-desam?sub_confirmation=1" target="_blank" rel="noopener noreferrer" class="yt-btn-header">
          ▶ YouTube
        </a>
      </nav>
    </div>
  </header>

  <main class="main-content">
    <div class="hero-banner">
      <div class="sacred-tag">ॐ சைவ நெறி • {data['grade_tamil']} • {data['grade_eng']} • {data['age_group']} ॐ</div>
      <h1>சைவ நெறி — {data['grade_tamil']}</h1>
      <h2>Saiva Neri Spiritual &amp; Vedic Curriculum — {data['grade_eng']}</h2>
      <div class="verse-quote">"{data['verse_quote']}"</div>
      <p class="hero-desc">{data['hero_desc']}</p>
    </div>

    <!-- Live Google Sites Link Bar -->
    <div class="google-site-banner">
      <div class="gs-banner-content">
        <h3>🌐 கூகிள் சைட்ஸ் நேரடி இணைப்பு (Google Sites Mirror)</h3>
        <p>கூகிள் தளத்தில் உள்ள இந்த {data['grade_tamil']} பக்கத்தை நேரடியாகப் பார்வையிடவும்.</p>
      </div>
      <a href="https://sites.google.com/view/wwwgurukuladesamcom/home/%E0%AE%9A%E0%AE%B5-%E0%AE%A8%E0%AE%B1/%E0%AE%A4%E0%AE%B0%E0%AE%AE-{g}" target="_blank" rel="noopener" class="gs-banner-btn">
        கூகிள் தளத்தில் {data['grade_tamil']} காண்க ↗
      </a>
    </div>

    <!-- Grade Quick Navigation -->
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin: 20px 0; padding: 14px 20px; background:var(--bg-card); border-radius:12px; border:1px solid var(--border-gold);">
      <a href="{prev_link}" style="color:var(--gold); text-decoration:none; font-weight:600;">{prev_label}</a>
      <a href="kalvi.html" style="color:var(--text-muted); text-decoration:none; font-size:0.9rem;">கல்வித் தளம் ({data['grade_tamil']} / 12)</a>
      <a href="{next_link}" style="color:var(--gold-bright); text-decoration:none; font-weight:700;">{next_label}</a>
    </div>

    <!-- Syllabus Content Box -->
    <div class="scripture-study-section" style="margin-bottom:30px;">
      <span class="source-badge">{data['grade_tamil']} — பாடத்திட்ட விவரங்கள் &amp; தலைப்புகள்</span>
      <h2>கற்பித்தல் நெறிகளும் பாட உள்ளடக்கமும் (Curriculum &amp; Learning Outcomes)</h2>
      <ul style="margin-left: 20px; margin-top: 14px; color: var(--text-main); line-height: 1.8;">
        {summary_html}
      </ul>
    </div>

    <!-- Detailed Learning Units / Master Lessons -->
    <h2 class="section-divider-title" style="margin-top:20px;">முழுமையான பாட அலகுகள் &amp; விரிவுரைகள் (Core Lessons &amp; Study Units)</h2>
    <p style="color:var(--text-muted); font-size:0.95rem; margin-top:6px; margin-bottom:24px;">
      மாணவர்கள் முறையாகப் படித்து வாழ்க்கையில் கடைப்பிடிப்பதற்கான வேத தத்துவங்கள், மூலப் பாடல்கள், வாழ்வியல் பயிற்சி மற்றும் சிந்தனை வினாக்கள்.
    </p>

    <div class="lessons-container">
      {units_html}
    </div>

    <!-- Vedic Way of Living Box -->
    <div style="background: linear-gradient(135deg, rgba(212,175,55,0.1) 0%, rgba(26,29,36,0.9) 100%); border: 2px solid var(--gold); border-radius: 16px; padding: 26px; margin: 40px 0;">
      <h3 style="color:var(--gold-bright); font-size:1.35rem; margin-bottom:12px; display:flex; align-items:center; gap:10px;">
        <span>🕉️</span> <span>{data['grade_tamil']} மாணவர்களுக்கான வேத வாழ்வியல் நெறிமுறைகள் (Dharmic Code of Living)</span>
      </h3>
      <p style="color:var(--text-main); line-height:1.8; margin-bottom:14px;">
        சைவ நெறியும் வேத தர்மமும் வெறும் நூலறிவு மட்டுமல்ல; அவை ஒரு மனிதனை உலகிற்கே ஒளியாக மாற்றும் நடைமுறை வாழ்வியல் முறையாகும். மாணவர்கள் தினமும் கீழ்க்கண்ட நெறிகளைக் கடைப்பிடிக்க வேண்டும்:
      </p>
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">
        <div style="background:rgba(0,0,0,0.3); border-radius:10px; padding:14px; border-left:3px solid var(--gold);">
          <strong style="color:var(--gold-soft); display:block; margin-bottom:4px;">1. பிரம்ம முகூர்த்த விழிப்பு:</strong>
          <span style="font-size:0.9rem; color:var(--text-muted);">அதிகாலையில் எழுந்து இரு கைகளையும் பார்த்து பூமி மாதாவை வணங்குதல்.</span>
        </div>
        <div style="background:rgba(0,0,0,0.3); border-radius:10px; padding:14px; border-left:3px solid var(--gold);">
          <strong style="color:var(--gold-soft); display:block; margin-bottom:4px;">2. தூய்மையும் திருநீறும்:</strong>
          <span style="font-size:0.9rem; color:var(--text-muted);">நீராடி தூய ஆடை அணிந்து, நெற்றியில் 'சிவ சிவ' கூறி திருநீறு அணிதல்.</span>
        </div>
        <div style="background:rgba(0,0,0,0.3); border-radius:10px; padding:14px; border-left:3px solid var(--gold);">
          <strong style="color:var(--gold-soft); display:block; margin-bottom:4px;">3. பெற்றோர் &amp; ஆசிரியர் மரியாதை:</strong>
          <span style="font-size:0.9rem; color:var(--text-muted);">தினமும் பெற்றோர் கால்களைத் தொட்டு வணங்குதல்; ஆசிரியருக்குக் கீழ்ப்படிதல்.</span>
        </div>
        <div style="background:rgba(0,0,0,0.3); border-radius:10px; padding:14px; border-left:3px solid var(--gold);">
          <strong style="color:var(--gold-soft); display:block; margin-bottom:4px;">4. சாத்வீக உணவு &amp; ஜீவகாருண்யம்:</strong>
          <span style="font-size:0.9rem; color:var(--text-muted);">புலால் உணவைத் தவிர்த்து சாத்வீக உணவு உண்ணுதல்; எளிய உயிர்களுக்கு உணவளித்தல்.</span>
        </div>
      </div>
    </div>

    <!-- Related Devotional Links -->
    <h2 class="section-divider-title" style="margin-top:40px;">இணைந்த ஆன்மீகப் பிரிவுகள் &amp; இசை நூலகம் (Related Traditions)</h2>
    <div class="canonical-grid">
      <div class="canonical-card" onclick="location.href='saiva-neri.html'" style="cursor: pointer;">
        <h4>🔱 பன்னிரு திருமுறைகள் (178 பாடல்கள்)</h4>
        <p>தேவாரம், திருவாசகம், திருவிசைப்பா, திருமந்திரப் பெருவெளியின் இசை வடிவங்கள்.</p>
        <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">கேட்க &amp; தியானிக்க ↗</span>
      </div>

      <div class="canonical-card" onclick="location.href='irai-isai-virundhu.html'" style="cursor: pointer;">
        <h4>🎵 இறை இசை விருந்து (5 பாடல்கள்)</h4>
        <p>பாலும் தெளிர் தேனும், குரு வணக்கம், கந்தர் அநுபூதி, சிவபுராணப் பாடல்கள்.</p>
        <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">இறை இசை கேட்க ↗</span>
      </div>

      <div class="canonical-card" onclick="location.href='thirukkural.html'" style="cursor: pointer;">
        <h4>📜 திருக்குறள் வாழ்வியல் தர்மம் (185 அதிகாரங்கள்)</h4>
        <p>அறத்துப்பால், பொருட்பால், இன்பத்துப்பால் அதிகாரங்களின் சினிமா இசைத் திரைப்படங்கள்.</p>
        <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">குறள் நல்வழி ↗</span>
      </div>

      <div class="canonical-card" onclick="location.href='classes.html'" style="cursor: pointer;">
        <h4>🏛️ ஆன்லைன் &amp; குருகுல வகுப்புகள்</h4>
        <p>வாராந்திர நேரலை வகுப்புகள் மற்றும் தேர்வு வழிகாட்டுதலில் இணையுங்கள்.</p>
        <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">வகுப்பில் சேர ↗</span>
      </div>
    </div>
  </main>

  <footer class="site-footer">
    <div class="footer-container">
      <div class="footer-col">
        <h4>குரு குல தேசம் (Guru Kula Desam)</h4>
        <p>வேதங்கள், பன்னிரு திருமுறைகள், சைவ சித்தாந்த சாத்திரங்கள், காஞ்சி மகா பெரியவா அருளுரைகள் மற்றும் வள்ளலார் பெருமானின் சுத்த சன்மார்க்க நெறிகளை உலகிற்கு பறைசாற்றும் ஆன்மீக இசை &amp; கல்விப் பெருவெளி.</p>
        <p style="margin-top: 10px; color: var(--gold); font-weight: 600;">அன்பே சிவம் • யாதும் ஊரே யாவரும் கேளிர் • ஏகன் அநேகன்</p>
        <div style="margin-top: 14px; font-size: 0.84rem; color: var(--gold-soft); line-height: 1.6; border-left: 2px solid var(--gold); padding-left: 12px; background: rgba(212, 175, 55, 0.05); padding-top: 6px; padding-bottom: 6px; border-radius: 0 8px 8px 0;">
          📍 <strong>மைய முகவரி (Headquarters):</strong><br>
          32, SSS Jaya Enclave, Kovaipudur,<br>
          Coimbatore, 641042, Tamil Nadu, India.
        </div>
      </div>
      <div class="footer-col">
        <h4>சைவ நெறி கல்வி &amp; பாடங்கள்</h4>
        <ul class="footer-links">
          <li><a href="kalvi.html">சைவ நெறி கல்வித் தளம் (Grades 1 - 12)</a></li>
          <li><a href="tharam-1.html">தரம் 1 — 60 பாடப் படங்கள் &amp; நூல்கள்</a></li>
          <li><a href="tharam-2.html">தரம் 2 — சிவ சின்னங்கள் &amp; ஆலய வழிபாடு</a></li>
          <li><a href="tharam-3.html">தரம் 3 — சமய குரவர் நால்வர் &amp; திருவெம்பாவை</a></li>
          <li><a href="tharam-4.html">தரம் 4 — பன்னிரு திருமுறைகள் &amp; சைவ விரதங்கள்</a></li>
          <li><a href="tharam-5.html">தரம் 5 — 63 நாயன்மார்கள் &amp; திருக்குறள் அறம்</a></li>
          <li><a href="tharam-6.html">தரம் 6 — நான்கு வேதங்கள் &amp; பதி-பசு-பாசம்</a></li>
          <li><a href="tharam-7.html">தரம் 7 முதல் தரம் 12 வரை (O/L &amp; A/L)</a></li>
          <li><a href="irai-isai-virundhu.html">இறை இசை விருந்து (5 சிறப்புப் பாடல்கள்)</a></li>
          <li><a href="syllabus.html">பாடத்திட்டம் (Comprehensive Syllabus)</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>ஆன்மீக வழிகள் &amp; இசை</h4>
        <ul class="footer-links">
          <li><a href="saiva-neri.html">சிவ நெறி (178 திருமுறைப் பாடல்கள்)</a></li>
          <li><a href="thirukkural.html">திருக்குறள் (185 அதிகாரப் படங்கள் &amp; இசை)</a></li>
          <li><a href="sanmargam.html">சன்மார்க்கம் (96 அருட்பெருஞ்சோதிப் பாடல்கள்)</a></li>
          <li><a href="murugan.html">முருக நெறி (47 கந்த சஷ்டி &amp; திருப்புகழ்)</a></li>
          <li><a href="sakthi.html">சக்தி நெறி (23 அபிராமி அந்தாதி &amp; போற்றிகள்)</a></li>
          <li><a href="vinayagar.html">விநாயகர் நெறி (11 கானங்கள்)</a></li>
          <li><a href="vaishnava.html">வைணவ நெறி (40 கானங்கள்)</a></li>
          <li><a href="youtube.html">YouTube இசை &amp; படக் களஞ்சியம்</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      &copy; 2026 குரு குல தேசம் (Guru Kula Desam) | gurukuladesam.com | அனைத்து உரிமைகளும் இறைப்பணிக்கே சமர்ப்பணம்.
    </div>
  </footer>

  <script src="assets/js/main.js"></script>
</body>
</html>
"""
    return html

# Generate all Tharams 2 to 12 across site/, docs/, and root .
for g in range(2, 13):
    data = ALL_GRADES.get(g)
    if not data:
        print(f"Skipping Grade {g} (no data)")
        continue
    
    html_content = generate_tharam_html(g, data)
    
    for folder in ['site', 'docs', '.']:
        prefix = f"{folder}/" if folder != '.' else ""
        filepath = f"{prefix}tharam-{g}.html"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ Generated {filepath} ({len(html_content)} bytes)")

print("\nSuccessfully built comprehensive curriculum for all missing Tharams (2 to 12)!")
