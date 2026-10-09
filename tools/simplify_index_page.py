import os
import re

ROOT = r'c:\GitHub\Gurukuladesam'
index_path = os.path.join(ROOT, 'index.html')

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update <title>
content = re.sub(
    r'<title>.*?</title>',
    '<title>குரு குல ஆசிரமம் | Guru Kula Ashram</title>',
    content,
    count=1
)

# 2. Update <meta name="description">
content = re.sub(
    r'<meta name="description" content=".*?">',
    '<meta name="description" content="குரு குல ஆசிரமம் — வித்யா குடீரம் இணையப் பள்ளி. தரம் 1 முதல் தரம் 12 மற்றும் உயர்கல்வி வித்யாபீடம். 7 ஆசிரமப் பாடநூல்கள் &amp; 3 Ds வாழ்வியல் நெறி.">',
    content,
    count=1
)

# 3. Update breadcrumbs
content = re.sub(
    r'<span class="crumb-current">.*?</span>',
    '<span class="crumb-current">குரு குல ஆசிரமம்</span>',
    content,
    count=1
)

# 4. Update Custom CSS in <style>
new_styles = '''    /* Card-Driven Focused Architecture for Index */
    .home-hero-card {
      background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(30, 41, 59, 0.75) 100%) !important;
      border: 1px solid rgba(212, 175, 55, 0.25) !important;
      border-radius: 20px !important;
      padding: 36px 28px !important;
      text-align: center;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5) !important;
      backdrop-filter: blur(10px);
      margin-bottom: 28px !important;
    }
    .home-hero-emblem-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 0.85rem;
      color: var(--gold-bright, #ffd700);
      background: rgba(212, 175, 55, 0.12);
      border: 1px solid rgba(212, 175, 55, 0.3);
      padding: 5px 16px;
      border-radius: 20px;
      font-weight: 700;
      letter-spacing: 0.05em;
      margin-bottom: 12px;
    }
    .home-hero-title {
      font-size: 2.4rem;
      font-weight: 900;
      color: #ffffff;
      margin: 8px 0;
      text-shadow: 0 2px 10px rgba(0,0,0,0.9);
      letter-spacing: -0.01em;
    }
    .home-hero-subtitle {
      font-size: 1.15rem;
      color: #2dd4bf;
      font-weight: 600;
      margin-bottom: 14px;
      text-shadow: 0 1px 4px rgba(0,0,0,0.8);
    }
    .home-hero-desc {
      max-width: 820px;
      margin: 0 auto 24px auto;
      color: #cbd5e1;
      font-size: 1rem;
      line-height: 1.7;
    }
    .home-hero-actions {
      display: flex;
      justify-content: center;
      gap: 12px;
      flex-wrap: wrap;
    }
    .hero-action-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 22px;
      border-radius: 12px;
      font-weight: 700;
      font-size: 0.95rem;
      text-decoration: none;
      transition: all 0.25s ease;
    }
    .hero-action-btn.primary {
      background: linear-gradient(135deg, #d97706, #b45309);
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(217, 119, 6, 0.4);
    }
    .hero-action-btn.primary:hover {
      background: linear-gradient(135deg, #f59e0b, #d97706);
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(217, 119, 6, 0.6);
    }
    .hero-action-btn.secondary {
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.4);
    }
    .hero-action-btn.secondary:hover {
      background: rgba(56, 189, 248, 0.25);
      transform: translateY(-2px);
    }
    .hero-action-btn.tertiary {
      background: rgba(45, 212, 191, 0.15);
      color: #2dd4bf;
      border: 1px solid rgba(45, 212, 191, 0.4);
    }
    .hero-action-btn.tertiary:hover {
      background: rgba(45, 212, 191, 0.25);
      transform: translateY(-2px);
    }

    /* 50/50 Visual Highlight Cards */
    .home-visual-strip {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 20px;
      margin-bottom: 32px;
    }
    .home-visual-card {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 16px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
      transition: transform 0.25s ease, border-color 0.25s ease;
    }
    .home-visual-card:hover {
      transform: translateY(-3px);
      border-color: rgba(212, 175, 55, 0.4);
    }
    .home-visual-media {
      position: relative;
      width: 100%;
      height: 180px;
      overflow: hidden;
    }
    .home-visual-media img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.4s ease;
    }
    .home-visual-card:hover .home-visual-media img {
      transform: scale(1.04);
    }
    .home-visual-tag {
      position: absolute;
      bottom: 12px;
      left: 12px;
      background: rgba(0, 0, 0, 0.75);
      color: var(--gold-bright, #ffd700);
      padding: 4px 12px;
      border-radius: 10px;
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      border: 1px solid rgba(212, 175, 55, 0.4);
    }
    .home-visual-body {
      padding: 20px;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
      justify-content: space-between;
    }
    .home-visual-body h3 {
      font-size: 1.25rem;
      font-weight: 800;
      color: #ffffff;
      margin: 0 0 8px 0;
    }
    .home-visual-body p {
      color: #94a3b8;
      font-size: 0.92rem;
      line-height: 1.6;
      margin: 0 0 16px 0;
    }
    .home-card-link {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: #2dd4bf;
      font-weight: 700;
      font-size: 0.9rem;
      text-decoration: none;
      transition: gap 0.2s ease;
    }
    .home-card-link:hover {
      gap: 10px;
      color: #5eead4;
    }

    /* Section Title Strip */
    .section-title-strip {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      flex-wrap: wrap;
      gap: 10px;
      padding-bottom: 12px;
      margin-bottom: 20px;
      border-bottom: 2px solid rgba(212, 175, 55, 0.3);
    }
    .section-pill {
      display: inline-block;
      background: rgba(212, 175, 55, 0.15);
      color: var(--gold-bright, #ffd700);
      border: 1px solid rgba(212, 175, 55, 0.35);
      padding: 3px 12px;
      border-radius: 12px;
      font-size: 0.76rem;
      font-weight: 800;
      text-transform: uppercase;
      margin-bottom: 4px;
    }
    .section-main-title {
      font-size: 1.55rem;
      font-weight: 800;
      color: #ffffff;
      margin: 0;
      text-shadow: 0 2px 4px rgba(0,0,0,0.8);
    }
    .section-sub-text {
      color: #94a3b8;
      font-size: 0.88rem;
    }

    /* 5 Stage Cards Grid */
    .home-stages-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 20px;
      margin-bottom: 36px;
    }
    .stage-card {
      background: rgba(15, 23, 42, 0.75);
      border-radius: 16px;
      padding: 22px;
      border: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s ease;
      position: relative;
    }
    .stage-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.4);
    }
    .stage-card.stage-primary { border-left: 4px solid #38bdf8; }
    .stage-card.stage-middle { border-left: 4px solid #34d399; }
    .stage-card.stage-secondary { border-left: 4px solid #facc15; }
    .stage-card.stage-senior { border-left: 4px solid #fb923c; }
    .stage-card.stage-collegiate { border-left: 4px solid #c084fc; }

    .stage-card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
      margin-bottom: 10px;
    }
    .stage-card-badge {
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .stage-primary .stage-card-badge { color: #38bdf8; }
    .stage-middle .stage-card-badge { color: #34d399; }
    .stage-secondary .stage-card-badge { color: #facc15; }
    .stage-senior .stage-card-badge { color: #fb923c; }
    .stage-collegiate .stage-card-badge { color: #c084fc; }

    .stage-card-title {
      font-size: 1.25rem;
      font-weight: 800;
      color: #ffffff;
      margin: 4px 0 2px 0;
    }
    .stage-card-age {
      font-size: 0.82rem;
      color: #94a3b8;
      font-weight: 500;
    }
    .stage-card-icon {
      font-size: 1.8rem;
    }
    .stage-card-desc {
      color: #cbd5e1;
      font-size: 0.9rem;
      line-height: 1.55;
      margin: 0 0 18px 0;
    }
    .stage-grades-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .stage-grade-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 7px 14px;
      border-radius: 8px;
      background: rgba(30, 41, 59, 0.8);
      color: #e2e8f0;
      text-decoration: none;
      font-size: 0.86rem;
      font-weight: 700;
      border: 1px solid rgba(255, 255, 255, 0.1);
      transition: all 0.2s ease;
    }
    .stage-grade-btn:hover {
      background: rgba(45, 212, 191, 0.2);
      border-color: #2dd4bf;
      color: #2dd4bf;
      transform: translateY(-2px);
    }

    /* Core Portals 3 Cards Grid */
    .home-portals-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      margin-bottom: 24px;
    }
    .portal-card {
      background: rgba(15, 23, 42, 0.65);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s ease;
    }
    .portal-card:hover {
      border-color: rgba(212, 175, 55, 0.4);
      transform: translateY(-3px);
      box-shadow: 0 10px 24px rgba(0, 0, 0, 0.3);
    }
    .portal-icon {
      font-size: 2.2rem;
      margin-bottom: 12px;
      display: inline-block;
    }
    .portal-card h4 {
      font-size: 1.15rem;
      font-weight: 800;
      color: #ffffff;
      margin: 0 0 8px 0;
    }
    .portal-card p {
      color: #94a3b8;
      font-size: 0.88rem;
      line-height: 1.6;
      margin: 0 0 18px 0;
    }
    .portal-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--gold-bright, #ffd700);
      font-size: 0.88rem;
      font-weight: 700;
      text-decoration: none;
      transition: gap 0.2s ease;
    }
    .portal-btn:hover {
      gap: 10px;
      color: #ffffff;
    }'''

style_pattern = r'<style>[\s\S]*?</style>'
content = re.sub(style_pattern, f'<style>\n{new_styles}\n  </style>', content, count=1)

# 5. Replace <main class="main-content" ...>...</main>
new_main = '''  <main class="main-content" style="max-width: 1240px; margin: 0 auto; padding: 20px 20px 80px 20px;">

    <!-- 1. FOCUSED HERO CARD (CLEAN & NON-CLUTTERED) -->
    <div class="home-hero-card" id="curriculumOverview">
      <div class="home-hero-emblem-pill">
        <span style="font-size: 1.1rem;">ॐ</span>
        <span>குரு குல ஆசிரமம் • வித்யா குடீரம்</span>
      </div>
      <h1 class="home-hero-title">குரு குல ஆசிரமம்</h1>
      <div class="home-hero-subtitle">Guru Kula Ashram — Modern Gurukulam Online Education</div>
      <p class="home-hero-desc">
        பாரம்பரியக் குருகுல விழுமியங்களும் நவீனக் கல்வியும் இணையும் ஆன்ம வித்யாபீடம். மழலைப் பருவம் முதல் உயர்கல்வி வரை, 7 ஆசிரமப் பாடநூல்கள் மற்றும் 3 Ds (கடமை, கட்டுப்பாடு, கண்ணியம்) நெறிமுறை வழியிலான ஒருங்கிணைந்த முழுமைப் பயில்வு.
      </p>
      <div class="home-hero-actions">
        <a href="#stagesSection" class="hero-action-btn primary">
          <span>🎓</span>
          <span>வகுப்புகள் (Grades 1–12)</span>
        </a>
        <a href="books.html" class="hero-action-btn secondary">
          <span>📚</span>
          <span>7 ஆசிரமப் பாடநூல்கள்</span>
        </a>
        <a href="school.html" class="hero-action-btn tertiary">
          <span>🏛️</span>
          <span>வித்யா குடீரம் பள்ளி அரங்கம்</span>
        </a>
      </div>
    </div>

    <!-- 2. SACRED VISUAL HERITAGE (2 IMAGES SPLIT CARDS) -->
    <div class="home-visual-strip" aria-label="குருகுலக் களம்">
      <article class="home-visual-card">
        <div class="home-visual-media">
          <img src="assets/images/gurukula-banyan-tree-bg.jpg" alt="குருகுல ஆலமர வித்யாபீடம்" loading="lazy">
          <span class="home-visual-tag">தபோவனக் களம்</span>
        </div>
        <div class="home-visual-body">
          <div>
            <h3>குருகுல ஆலமர வித்யாபீடம்</h3>
            <p>இயற்கையின் மடியில் அமைதியான சூழலில் அமைந்த இணையத் தபோவனம். வணிகப் பகட்டுகளின்றி பண்பாட்டுக் கல்வி கற்கும் ஆசிரம வித்யாபீடம்.</p>
          </div>
          <a href="school.html" class="home-card-link">பள்ளிப் போர்டல் காண &rarr;</a>
        </div>
      </article>

      <article class="home-visual-card">
        <div class="home-visual-media">
          <img src="assets/images/lessons/disciples_under_sacred_tree.jpg" alt="குரு சீடர் பாரம்பரியம் & 7 ஆசிரமப் பாடநூல்கள்" loading="lazy">
          <span class="home-visual-tag">சாத்திரப் பெட்டகம்</span>
        </div>
        <div class="home-visual-body">
          <div>
            <h3>குரு சீடர் பாரம்பரியமும் 7 நூல்களும்</h3>
            <p>நன்னெறி முதல் நற்செயல் வரை — விழுமியங்கள், திருமுறைப் பாடல்கள், மற்றும் 3 Ds வாழ்வியல் சாதனா நெறிமுறைகள் அடங்கிய பாடநூல்கள்.</p>
          </div>
          <a href="books.html" class="home-card-link">நூல்கள் அரங்கம் செல்ல &rarr;</a>
        </div>
      </article>
    </div>

    <!-- 3. THE 5 GURUKULA STAGES (FOCUSED CARD-DRIVEN SELECTOR) -->
    <section class="home-stages-section" id="stagesSection" aria-label="ஐந்து குருகுலப் பருவங்கள்">
      <div class="section-title-strip">
        <div>
          <span class="section-pill">கல்விப் பருவங்கள்</span>
          <h2 class="section-main-title">ஐந்து குருகுலப் பருவங்கள் (Educational Stages)</h2>
        </div>
        <span class="section-sub-text">உங்கள் வகுப்பைத் தேர்வு செய்து நேரடியாகக் கற்கத் தொடங்குங்கள்</span>
      </div>

      <div class="home-stages-grid">

        <!-- Stage 1: Primary (1 - 4) -->
        <div class="stage-card stage-primary">
          <div>
            <div class="stage-card-header">
              <div class="stage-card-title-box">
                <span class="stage-card-badge">1. பாலப் பருவம்</span>
                <h3 class="stage-card-title">தொடக்கக் கல்வி (Grades 1 – 4)</h3>
                <span class="stage-card-age">வயது 6 – 9 • 1–2 நூல்கள்</span>
              </div>
              <span class="stage-card-icon">🌱</span>
            </div>
            <p class="stage-card-desc">விளையாடிப் பயிலல், பகிர்தல், நற்பண்புகள், உண்மை பேசுதல் &amp; 3 Ds (கடமை, கட்டுப்பாடு, கண்ணியம்) நெறிமுறை.</p>
          </div>
          <div class="stage-grades-row">
            <a href="tharam-1.html" class="stage-grade-btn" title="தரம் 1 • நற்செயல் (1 நூல்)">தரம் 1</a>
            <a href="tharam-2.html" class="stage-grade-btn" title="தரம் 2 • நற்செயல் (1 நூல்)">தரம் 2</a>
            <a href="tharam-3.html" class="stage-grade-btn" title="தரம் 3 • நற்செயல், நற்பண்பு (2 நூல்கள்)">தரம் 3</a>
            <a href="tharam-4.html" class="stage-grade-btn" title="தரம் 4 • நற்செயல், நற்பண்பு (2 நூல்கள்)">தரம் 4</a>
          </div>
        </div>

        <!-- Stage 2: Middle (5 - 8) -->
        <div class="stage-card stage-middle">
          <div>
            <div class="stage-card-header">
              <div class="stage-card-title-box">
                <span class="stage-card-badge">2. இளம் பருவம்</span>
                <h3 class="stage-card-title">நடுநிலைப் பள்ளி (Grades 5 – 8)</h3>
                <span class="stage-card-age">வயது 10 – 13 • 5 நூல்கள்</span>
              </div>
              <span class="stage-card-icon">🌿</span>
            </div>
            <p class="stage-card-desc">ஒழுக்கம், நல்லறம், நற்பண்பு, திருமுறை பக்தி, இறை சரணாகதி &amp; இல்லற சாதனா நெறிமுறைகள்.</p>
          </div>
          <div class="stage-grades-row">
            <a href="tharam-5.html" class="stage-grade-btn" title="தரம் 5 • 5 நூல்கள்">தரம் 5</a>
            <a href="tharam-6.html" class="stage-grade-btn" title="தரம் 6 • 5 நூல்கள்">தரம் 6</a>
            <a href="tharam-7.html" class="stage-grade-btn" title="தரம் 7 • 5 நூல்கள்">தரம் 7</a>
            <a href="tharam-8.html" class="stage-grade-btn" title="தரம் 8 • 5 நூல்கள்">தரம் 8</a>
          </div>
        </div>

        <!-- Stage 3: Secondary (9 - 10) -->
        <div class="stage-card stage-secondary">
          <div>
            <div class="stage-card-header">
              <div class="stage-card-title-box">
                <span class="stage-card-badge">3. உயர்நிலைப் பருவம்</span>
                <h3 class="stage-card-title">உயர்நிலைப் பள்ளி (Grades 9 – 10)</h3>
                <span class="stage-card-age">வயது 14 – 15 • 6 நூல்கள்</span>
              </div>
              <span class="stage-card-icon">🛡️</span>
            </div>
            <p class="stage-card-desc">திருக்குறள் அறநெறி, வாய்மை, நாவடக்கம், இன்சொல், பஞ்ச மகா யாகங்கள் &amp; சமூகத் தொண்டு.</p>
          </div>
          <div class="stage-grades-row">
            <a href="tharam-9.html" class="stage-grade-btn" title="தரம் 9 • 6 நூல்கள்">தரம் 9</a>
            <a href="tharam-10.html" class="stage-grade-btn" title="தரம் 10 • 6 நூல்கள்">தரம் 10</a>
          </div>
        </div>

        <!-- Stage 4: Senior Secondary (11 - 12) -->
        <div class="stage-card stage-senior">
          <div>
            <div class="stage-card-header">
              <div class="stage-card-title-box">
                <span class="stage-card-badge">4. மேல்நிலைப் பருவம்</span>
                <h3 class="stage-card-title">மேல்நிலைப் பள்ளி (Grades 11 – 12)</h3>
                <span class="stage-card-age">வயது 16 – 17 • 6 நூல்கள்</span>
              </div>
              <span class="stage-card-icon">🏹</span>
            </div>
            <p class="stage-card-desc">பகவத் கீதை யோக நெறி, தைத்திரீய உபநிடதம், தர்ம சிந்தனை &amp; பள்ளி இறுதித் தகுதி.</p>
          </div>
          <div class="stage-grades-row">
            <a href="tharam-11.html" class="stage-grade-btn" title="தரம் 11 • 6 நூல்கள்">தரம் 11</a>
            <a href="tharam-12.html" class="stage-grade-btn" title="தரம் 12 • 6 நூல்கள்">தரம் 12</a>
          </div>
        </div>

        <!-- Stage 5: Higher Studies (BA, MA, PhD) -->
        <div class="stage-card stage-collegiate">
          <div>
            <div class="stage-card-header">
              <div class="stage-card-title-box">
                <span class="stage-card-badge">5. உயர்கல்வி வித்யாபீடம்</span>
                <h3 class="stage-card-title">பட்டப் படிப்புகள் &amp; ஆய்வு</h3>
                <span class="stage-card-age">வயது 18+ • அனைத்து 7 நூல்கள்</span>
              </div>
              <span class="stage-card-icon">⚛️</span>
            </div>
            <p class="stage-card-desc">வேத-நவீன அறிவியல் சங்கமம், குவாண்டம் இயற்பியல், வேதாந்தம் &amp; முனைவர் பட்ட ஆய்வு.</p>
          </div>
          <div class="stage-grades-row">
            <a href="higher-studies.html#tierUG" class="stage-grade-btn" title="இளங்கலை (3 Yrs)">B.A. / B.Sc.</a>
            <a href="higher-studies.html#tierPG" class="stage-grade-btn" title="முதுகலை (2 Yrs)">M.A. முதுகலை</a>
            <a href="higher-studies.html#tierPhD" class="stage-grade-btn" title="முனைவர் ஆய்வு">Ph.D. ஆய்வு</a>
          </div>
        </div>

      </div>
    </section>

    <!-- 4. CORE ASHRAM PILLARS (3 FOCUSED ACTION CARDS) -->
    <section class="home-portals-section" aria-label="ஆசிரமத் தளங்கள்">
      <div class="home-portals-grid">
        <div class="portal-card">
          <div>
            <span class="portal-icon">🏛️</span>
            <h4>வித்யா குடீரம் பள்ளி அரங்கம்</h4>
            <p>12 வார கால அட்டவணை, அத்தியாய வாசிப்பு, வினாடி-வினா, சாதனா புள்ளிகள் &amp; பருவப் பட்டயச் சான்றிதழ்.</p>
          </div>
          <a href="school.html" class="portal-btn">வகுப்பறைக்குச் செல்க &rarr;</a>
        </div>

        <div class="portal-card">
          <div>
            <span class="portal-icon">📚</span>
            <h4>7 ஆசிரமப் பாடநூல்கள் அலமாரி</h4>
            <p>நன்னெறி, நல்லறம், நற்பண்பு, நற்துணை, நற்சிந்தனை, நற்சொல், நற்செயல் — விழுமியக் கல்விப் பெட்டகம்.</p>
          </div>
          <a href="books.html" class="portal-btn">நூலகம் காண்க &rarr;</a>
        </div>

        <div class="portal-card">
          <div>
            <span class="portal-icon">🌿</span>
            <h4>3 Ds தர்ம வாழ்வியல் சாதனா</h4>
            <p>கடமை (Duty), கட்டுப்பாடு (Discipline), கண்ணியம் (Dignity) — அன்றாட வாழ்வில் தர்ம நெறிமுறைகள்.</p>
          </div>
          <a href="grihastha.html" class="portal-btn">வாழ்வியல் நெறி &rarr;</a>
        </div>
      </div>
    </section>

  </main>'''

main_pattern = r'<main class="main-content"[\s\S]*?</main>'
content = re.sub(main_pattern, new_main, content, count=1)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully simplified index.html to card-driven layout with single phrase header!")
