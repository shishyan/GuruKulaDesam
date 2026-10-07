# -*- coding: utf-8 -*-
import os
import shutil

from update_virtue_mapping import VIRTUES_BY_GRADE

def generate_virtues_page():
    all_cards_html = ""
    for g in range(1, 13):
        data = VIRTUES_BY_GRADE[g]
        letters_str = " • ".join(f"‘{l}’" for l in data["letters"])
        tier_class = "tier-1" if g <= 4 else ("tier-2" if g <= 8 else "tier-3")

        virtues_inner = ""
        for v in data["virtues"]:
            virtues_inner += f"""
            <div class="virtue-item-card" style="background: rgba(0,0,0,0.35); border-left: 3px solid var(--gold); border-radius: 0 10px 10px 0; padding: 16px 20px; margin-bottom: 14px;">
              <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px;">
                <div style="font-size: 1.15rem; font-weight: 700; color: var(--gold-bright);">
                  <span class="letter-circle">{v['letter']}</span> {v['virtue']}
                </div>
                <span class="card-badge badge-audio">தரம் {g}</span>
              </div>
              <div style="font-family:'Mukta Malar', serif; font-size:1.02rem; color:#fff; line-height:1.6; margin-bottom:8px; font-weight:500;">
                📖 <em>{v['verse']}</em>
              </div>
              <div style="color:var(--text-muted); font-size:0.92rem; line-height:1.6; margin-bottom:10px;">
                💡 <strong>தத்துவ விளக்கம்:</strong> {v['meaning']}
              </div>
              <div style="background:rgba(42,157,143,0.08); border:1px solid rgba(42,157,143,0.25); border-radius:8px; padding:10px 14px; font-size:0.9rem; color:#b7e4c7; line-height:1.5;">
                🎯 <strong>மாணவர் அன்றாட வாழ்வியல் பயிற்சி (Daily Living Practice):</strong> {v['exercise']}
              </div>
            </div>
            """

        all_cards_html += f"""
        <div class="virtue-grade-block {tier_class}" id="grade-{g}-block" style="background: rgba(18, 22, 32, 0.9); border: 1px solid var(--border-gold); border-radius: 16px; padding: 26px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:16px; border-bottom:1px solid rgba(212,175,55,0.2); padding-bottom:12px;">
            <div>
              <span style="background:var(--gold-gradient); color:#000; font-weight:800; font-size:0.85rem; padding:4px 14px; border-radius:14px; margin-right:10px;">
                தரம் {g} (Grade {g})
              </span>
              <span style="color:var(--gold-bright); font-size:1.25rem; font-weight:700;">
                எழுத்துகள் {letters_str} — {data['title']}
              </span>
            </div>
            <span style="background:{data['tier_color']}22; color:{data['tier_color']}; border:1px solid {data['tier_color']}55; padding:4px 12px; border-radius:14px; font-size:0.82rem; font-weight:700;">
              {data['tier_badge']}
            </span>
          </div>

          <div style="color:var(--gold-soft); font-size:0.9rem; font-weight:600; margin-bottom:12px;">
            {data['english_title']} • {data['tier']}
          </div>
          <p style="color:var(--text-main); font-size:0.95rem; line-height:1.7; margin-bottom:20px;">
            {data['description']}
          </p>

          <div class="virtues-list">
            {virtues_inner}
          </div>

          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:14px; padding-top:12px; border-top:1px dashed rgba(212,175,55,0.2); font-size:0.84rem;">
            <span style="color:var(--text-muted);">இத்தகு நற்பண்பை வளர்க்கும் தரம் {g} சைவ நெறி பாடநூல்கள்:</span>
            <a href="tharam-{g}.html" style="color:var(--gold-bright); text-decoration:none; font-weight:700;">தரம் {g} பாடங்களைக் காண்க ↗</a>
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>அகர வரிசை நற்பண்பு நெறிமுறைமை — தமிழ் எழுத்து முதல் தர்மம் வரை | குரு குல தேசம்</title>
  <meta name="description" content="தமிழ் எழுத்துக்களோடு மாணவர்களின் நற்பண்புகளையும் ஒழுக்கத்தையும் படிப்படியாகக் கற்பித்து, பின்பற்றி, நிலைநிறுத்தும் 12 தரங்களுக்கான நற்பண்பு வரைபடம்.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Mukta+Malar:wght@300;400;500;600;700;800&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css">
  <style>
    .letter-circle {{
      display: inline-block;
      width: 32px;
      height: 32px;
      line-height: 32px;
      background: var(--gold);
      color: #07080b;
      font-weight: 800;
      text-align: center;
      border-radius: 50%;
      margin-right: 8px;
    }}
    .tier-filter-btn {{
      padding: 8px 18px;
      border-radius: 20px;
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(212,175,55,0.25);
      color: var(--text-muted);
      cursor: pointer;
      font-weight: 600;
      font-size: 0.88rem;
      transition: all 0.2s;
    }}
    .tier-filter-btn:hover, .tier-filter-btn.active {{
      background: var(--gold);
      color: #000;
      border-color: var(--gold);
    }}
  </style>
</head>
<body>

  <!-- Navigation Bar -->
  <header class="site-header">
    <div class="nav-container">
      <a href="index.html" class="logo">
        <span class="om-symbol">ॐ</span>
        <div class="logo-text">
          <span class="logo-main">குரு குல தேசம்</span>
          <span class="logo-sub">GURU KULA DESAM</span>
        </div>
      </a>

      <button class="mobile-toggle" id="mobileNavToggle" onclick="toggleMobileNav()" aria-label="Toggle navigation">
        ☰
      </button>

      <nav class="nav-links" id="mainNav">
        <a href="index.html" class="nav-link">முகப்பு</a>
        
        <!-- Kalvi Dropdown -->
        <div class="nav-dropdown" id="kalviDropdown">
          <button class="nav-link dropdown-toggle" id="kalviDropdownBtn" onclick="toggleDropdown(event, 'kalviDropdown')" aria-haspopup="true" aria-expanded="false">
            <span>கல்வி (Grades 1-12)</span>
            <span class="dropdown-arrow">▾</span>
          </button>
          <div class="dropdown-menu dropdown-grid-4col" id="kalviDropdownMenu">
            <a href="kalvi.html" class="dropdown-item dropdown-item-hub">
              <span class="dropdown-item-icon">🏛️</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">கல்வி முகப்பு (Hub)</div>
                <div class="dropdown-item-desc">அனைத்து 12 தரங்களின் பாடநெறி</div>
              </div>
            </a>
            <a href="virtues.html" class="dropdown-item dropdown-item-hub active" style="grid-column: span 3;">
              <span class="dropdown-item-icon">🔤</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">அகர வரிசை நற்பண்பு நெறி (Virtues Mapping)</div>
                <div class="dropdown-item-desc">எழுத்து முதல் தர்மம் வரை — 12 தரங்களின் நற்பண்பு வளர்ச்சி</div>
              </div>
            </a>
            <a href="tharam-1.html" class="dropdown-item"><span class="dropdown-item-icon">📖</span><div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 1 (Grade 1)</div></div></a>
            <a href="tharam-2.html" class="dropdown-item"><span class="dropdown-item-icon">🪔</span><div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 2 (Grade 2)</div></div></a>
            <a href="tharam-3.html" class="dropdown-item"><span class="dropdown-item-icon">🔱</span><div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 3 (Grade 3)</div></div></a>
            <a href="tharam-4.html" class="dropdown-item"><span class="dropdown-item-icon">🌿</span><div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 4 (Grade 4)</div></div></a>
            <a href="tharam-5.html" class="dropdown-item"><span class="dropdown-item-icon">🌺</span><div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 5 (Grade 5)</div></div></a>
            <a href="tharam-6.html" class="dropdown-item"><span class="dropdown-item-icon">📿</span><div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 6 (Grade 6)</div></div></a>
            <a href="tharam-7.html" class="dropdown-item"><span class="dropdown-item-icon">🕉️</span><div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 7 (Grade 7)</div></div></a>
            <a href="tharam-8.html" class="dropdown-item"><span class="dropdown-item-icon">📜</span><div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 8 (Grade 8)</div></div></a>
            <a href="tharam-9.html" class="dropdown-item"><span class="dropdown-item-icon">🔆</span><div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 9 (Grade 9)</div></div></a>
            <a href="tharam-10.html" class="dropdown-item"><span class="dropdown-item-icon">🌟</span><div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 10 (Grade 10)</div></div></a>
            <a href="tharam-11.html" class="dropdown-item"><span class="dropdown-item-icon">🔱</span><div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 11 (Grade 11)</div></div></a>
            <a href="tharam-12.html" class="dropdown-item"><span class="dropdown-item-icon">👑</span><div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 12 (Grade 12)</div></div></a>
          </div>
        </div>

        <a href="saiva-neri.html" class="nav-link">சிவ நெறி</a>
        <a href="thirukkural.html" class="nav-link">திருக்குறள்</a>
        <a href="sanmargam.html" class="nav-link">சன்மார்க்கம்</a>
        <a href="irai-isai-virundhu.html" class="nav-link">இறை இசை</a>
        <a href="syllabus.html" class="nav-link">பாடத்திட்டம்</a>
        <a href="classes.html" class="nav-link">வகுப்புகள்</a>
        <a href="about.html" class="nav-link">பெரியவா தரிசனம்</a>
        <a href="https://sites.google.com/view/wwwgurukuladesamcom" target="_blank" rel="noopener" class="nav-link" style="border: 1px solid var(--border-gold); padding: 5px 12px; border-radius: 16px; color: var(--gold-bright);">🌐 கூகிள் தளம் ↗</a>
      </nav>
    </div>
  </header>

  <main class="main-content">
    <div class="hero-banner">
      <div class="sacred-tag">🔤 அகர வரிசை நற்பண்பு நெறிமுறைமை • Alphabet to Virtue Progression Portal 🔤</div>
      <h1>அகர வரிசை நற்பண்பு நெறி</h1>
      <h2>Alphabet to Virtue Progression Matrix — From First Letter to Divine Wisdom</h2>
      <div class="verse-quote">"எண்ணும் எழுத்தும் கண் எனத் தகும் — ஔவையார் (கொன்றை வேந்தன்)"</div>
      <p class="hero-desc">
        குழந்தைகள் மற்றும் மாணவர்கள் தமிழ் எழுத்துக்களைக் கற்கும் போதே, அதனோடு இணைந்து நற்பண்புகளையும் அறிந்து, பின்பற்றி, வாழ்வின் சோதனைகளிலும் நிலைநிறுத்தும் முப்பரிமாண ஆன்மீக ஒழுக்க வளர்ச்சிப் பாடத்திட்டம்.
      </p>
    </div>

    <!-- 3 Tier Progression Summary Cards -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0;">
      <div style="background: rgba(42, 157, 143, 0.1); border: 2px solid #2a9d8f; border-radius: 14px; padding: 22px;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
          <span style="font-size: 1.6rem;">🟢</span>
          <div>
            <h3 style="color: #2a9d8f; margin: 0; font-size: 1.15rem;">நிலை 1: அறிதல் &amp; கற்றல் (To Learn)</h3>
            <span style="font-size: 0.8rem; color: var(--gold-soft); font-weight: 700;">தரம் 1 முதல் தரம் 4 வரை (வயது 5 - 9)</span>
          </div>
        </div>
        <p style="color: var(--text-main); font-size: 0.9rem; line-height: 1.6; margin: 0;">
          அறஞ்செய விரும்பு, ஆறுவது சினம், இன்சொல், ஈகை, உண்மை, ஊக்கம் மற்றும் ஜீவகாருண்யம் ஆகிய அடிப்படை நற்பண்புகளை எளிமையான கதைகள், பாடல்கள் மூலம் அறிந்து கொள்ளுதல்.
        </p>
      </div>

      <div style="background: rgba(233, 196, 106, 0.1); border: 2px solid #e9c46a; border-radius: 14px; padding: 22px;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
          <span style="font-size: 1.6rem;">🟡</span>
          <div>
            <h3 style="color: #e9c46a; margin: 0; font-size: 1.15rem;">நிலை 2: செய்தல் &amp; பின்பற்றுதல் (To Follow)</h3>
            <span style="font-size: 0.8rem; color: var(--gold-soft); font-weight: 700;">தரம் 5 முதல் தரம் 8 வரை (வயது 10 - 13)</span>
          </div>
        </div>
        <p style="color: var(--text-main); font-size: 0.9rem; line-height: 1.6; margin: 0;">
          செய்த நன்றியை மறவாமை, ஐம்பொறி அடக்கம், வெகுளாமை, நடுவுநிலைமை மற்றும் கடமை உணர்வை வாழ்க்கையில் விருப்பத்தோடு இடைவிடாது கடைப்பிடித்து நற்பழக்கமாக்குதல்.
        </p>
      </div>

      <div style="background: rgba(231, 111, 81, 0.1); border: 2px solid #e76f51; border-radius: 14px; padding: 22px;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
          <span style="font-size: 1.6rem;">🔴</span>
          <div>
            <h3 style="color: #e76f51; margin: 0; font-size: 1.15rem;">நிலை 3: நிலைநிறுத்துதல் &amp; காத்தல் (To Maintain)</h3>
            <span style="font-size: 0.8rem; color: var(--gold-soft); font-weight: 700;">தரம் 9 முதல் தரம் 12 வரை (வயது 14 - 18)</span>
          </div>
        </div>
        <p style="color: var(--text-main); font-size: 0.9rem; line-height: 1.6; margin: 0;">
          அழுக்காறாமை, எந்தச் சூழ்நிலையிலும் வாய்மை தவறாமை, உயிரினும் மேலாக ஒழுக்கத்தைப் பேணல், அவாவறுத்தல் மற்றும் உலக நன்மைக்காக தர்மத்தை நிலைநிறுத்தி பரசிவ சரணாகதி அடைதல்.
        </p>
      </div>
    </div>

    <!-- Filter Buttons Bar -->
    <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 30px; justify-content: center; background: var(--bg-card); padding: 14px; border-radius: 14px; border: 1px solid var(--border-gold);">
      <button class="tier-filter-btn active" onclick="filterTier('all', this)">அனைத்து 12 தரங்களும் (All Grades)</button>
      <button class="tier-filter-btn" onclick="filterTier('tier-1', this)">🟢 நிலை 1: அறிதல் (Grades 1-4)</button>
      <button class="tier-filter-btn" onclick="filterTier('tier-2', this)">🟡 நிலை 2: பின்பற்றுதல் (Grades 5-8)</button>
      <button class="tier-filter-btn" onclick="filterTier('tier-3', this)">🔴 நிலை 3: நிலைநிறுத்துதல் (Grades 9-12)</button>
    </div>

    <!-- Grades Container -->
    <div id="virtuesContainer">
      {all_cards_html}
    </div>
  </main>

  <footer class="site-footer">
    <div class="footer-container">
      <div class="footer-col">
        <h4>குரு குல தேசம் (Guru Kula Desam)</h4>
        <p>வேதங்கள், பன்னிரு திருமுறைகள், சைவ சித்தாந்த சாத்திரங்கள், காஞ்சி மகா பெரியவா அருளுரைகள் மற்றும் வள்ளலார் பெருமானின் சுத்த சன்மார்க்க நெறிகளை உலகிற்கு பறைசாற்றும் ஆன்மீக இசை &amp; கல்விப் பெருவெளி.</p>
        <div style="margin-top: 14px; font-size: 0.84rem; color: var(--gold-soft); line-height: 1.6; border-left: 2px solid var(--gold); padding-left: 12px; background: rgba(212, 175, 55, 0.05); padding-top: 6px; padding-bottom: 6px; border-radius: 0 8px 8px 0;">
          📍 <strong>மைய முகவரி:</strong> 32, SSS Jaya Enclave, Kovaipudur, Coimbatore, 641042, Tamil Nadu, India.
        </div>
      </div>
      <div class="footer-col">
        <h4>கல்வி &amp; நற்பண்பு நெறி</h4>
        <ul class="footer-links">
          <li><a href="virtues.html">அகர வரிசை நற்பண்பு நெறி (Virtues Mapping)</a></li>
          <li><a href="kalvi.html">சைவ நெறி கல்வித் தளம் (Grades 1 - 12)</a></li>
          <li><a href="syllabus.html">பாடத்திட்டம் (Comprehensive Syllabus)</a></li>
          <li><a href="tharam-1.html">தரம் 1 — 60 பாடப் படங்கள்</a></li>
          <li><a href="classes.html">வகுப்புகள் (Online Classes &amp; Timetable)</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>ஆன்மீக வழிகள் &amp; இசை</h4>
        <ul class="footer-links">
          <li><a href="saiva-neri.html">சிவ நெறி (172 திருமுறைப் பாடல்கள்)</a></li>
          <li><a href="thirukkural.html">திருக்குறள் (185 அதிகாரப் படங்கள் &amp; இசை)</a></li>
          <li><a href="sanmargam.html">சன்மார்க்கம் (94 அருட்பெருஞ்சோதிப் பாடல்கள்)</a></li>
          <li><a href="murugan.html">முருக நெறி &amp; கந்த சஷ்டி</a></li>
          <li><a href="sakthi.html">சக்தி நெறி &amp; விநாயகர்</a></li>
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
    function filterTier(tier, btn) {{
      document.querySelectorAll('.tier-filter-btn').forEach(function(b) {{
        b.classList.remove('active');
      }});
      if (btn) btn.classList.add('active');

      var blocks = document.querySelectorAll('.virtue-grade-block');
      blocks.forEach(function(b) {{
        if (tier === 'all' || b.classList.contains(tier)) {{
          b.style.display = 'block';
        }} else {{
          b.style.display = 'none';
        }}
      }});
    }}
  </script>
</body>
</html>
"""
    return html

def main():
    content = generate_virtues_page()
    for dest in ['virtues.html', 'docs/virtues.html', 'site/virtues.html']:
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated: {dest}")

if __name__ == '__main__':
    main()
