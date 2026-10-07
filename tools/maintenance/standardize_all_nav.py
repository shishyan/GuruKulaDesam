import os
import re

ROOT = r"c:\GitHub\Gurukuladesam"
DOCS = os.path.join(ROOT, "docs")
SITE = os.path.join(ROOT, "site")

STANDARD_STRIP_BAR = """  <!-- LEFT STRIP BAR (PRIMARY MOBILE-STYLE MENU OVERLAY) -->
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
      <div class="strip-group" data-group="kalvi">
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

  <div class="strip-backdrop" id="stripBackdrop" onclick="closePrimaryMenu()"></div>"""

HTML_FILES = [f for f in os.listdir(ROOT) if f.endswith('.html')]

count = 0
for fn in HTML_FILES:
    fp = os.path.join(ROOT, fn)
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()

    # Match existing aside#leftStripBar and optional following strip-backdrop
    pattern = r'<aside class="left-strip-bar"[\s\S]*?</aside>(?:\s*<div class="strip-backdrop"[^>]*></div>)?'
    if re.search(pattern, content):
        content = re.sub(pattern, STANDARD_STRIP_BAR, content)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        
        for dest in [DOCS, SITE]:
            dfp = os.path.join(dest, fn)
            if os.path.exists(dest):
                with open(dfp, "w", encoding="utf-8") as f:
                    f.write(content)
        count += 1
        print(f"Updated {fn}")

print(f"Standardized menu overlay across {count} HTML files.")
