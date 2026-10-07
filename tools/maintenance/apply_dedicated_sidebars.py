import os
import re

ROOT = r"c:\GitHub\Gurukuladesam"
DOCS = os.path.join(ROOT, "docs")
SITE = os.path.join(ROOT, "site")

PAGES_CONFIG = {
    "kalvi.html": {
        "id": "kalviSidebar",
        "pill": "🎓 கல்வி நெறி (Academy Sub-menu)",
        "title": "கல்வி &amp; பள்ளிக் கூடம்",
        "sub": "12 தரங்கள் &amp; பாடப்பிரிவுகள்",
        "items": [
            ("kalvi.html", "🏛️", "கல்வி மையம் (12 தரங்கள்)", True),
            ("school.html", "🏫", "இணையப் பள்ளி போர்டல்", False),
            ("higher-studies.html", "🔬", "வேத-நவீன உயர்கல்வி", False),
            ("virtues.html", "🔤", "அகர வரிசை நற்பண்புகள்", False),
            ("syllabus.html", "📚", "முழு பாடத்திட்டம்", False)
        ],
        "has_grades": True
    },
    "saiva-neri.html": {
        "id": "saivaSidebar",
        "pill": "🕉️ சைவ நெறி (Tradition Sub-menu)",
        "title": "சைவ நெறி &amp; தெய்வங்கள்",
        "sub": "சிவ சித்தாந்தம் &amp; பன்னிரு திருமுறைகள்",
        "items": [
            ("saiva-neri.html", "🔱", "சைவ சித்தாந்தம் &amp; நெறி", True),
            ("vinayagar.html", "🐘", "முழுமுதற் கடவுள் விநாயகர்", False),
            ("murugan.html", "🪶", "தமிழ் தெய்வம் முருகன்", False),
            ("sakthi.html", "🌸", "அம்பிகை சக்தி நெறி", False),
            ("vaishnava.html", "🪷", "அரங்கன் &amp; கிருஷ்ணர் வைணவம்", False)
        ],
        "custom_footer": """
        <div style="margin-top:16px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.08);">
          <div style="font-size:0.76rem; color:#38bdf8; font-weight:700; text-transform:uppercase; margin-bottom:8px;">சிவத் திருப்பதிக வடிகட்டி:</div>
          <div style="display:flex; flex-direction:column; gap:6px;">
            <button type="button" class="sidebar-chapter-btn" onclick="filterByText('தேவாரம்')"><span class="sidebar-chapter-pill"><span class="sidebar-num">🌿</span><span>தேவாரம்</span></span></button>
            <button type="button" class="sidebar-chapter-btn" onclick="filterByText('திருவாசகம்')"><span class="sidebar-chapter-pill"><span class="sidebar-num">💎</span><span>திருவாசகம்</span></span></button>
            <button type="button" class="sidebar-chapter-btn" onclick="filterByText('திருமந்திரம்')"><span class="sidebar-chapter-pill"><span class="sidebar-num">🧘</span><span>திருமந்திரம்</span></span></button>
            <button type="button" class="sidebar-chapter-btn" onclick="filterByText('ருத்ரம்')"><span class="sidebar-chapter-pill"><span class="sidebar-num">🔥</span><span>ஸ்ரீ ருத்ரம்</span></span></button>
          </div>
        </div>
        """
    },
    "irai-isai-virundhu.html": {
        "id": "isaiSidebar",
        "pill": "🎵 இறை இசை (Music Sub-menu)",
        "title": "இறை இசை &amp; பாடல்கள்",
        "sub": "580 பக்தி இசை வெளியீடுகள்",
        "items": [
            ("irai-isai-virundhu.html", "🎶", "அனைத்து பாடல்கள் (580)", True),
            ("youtube.html", "▶️", "காணொளிகள் களஞ்சியம்", False)
        ],
        "custom_footer": """
        <div style="margin-top:16px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.08);">
          <div style="font-size:0.76rem; color:#38bdf8; font-weight:700; text-transform:uppercase; margin-bottom:8px;">வகைப்பாட்டு வடிகட்டி:</div>
          <div style="display:flex; flex-direction:column; gap:6px;">
            <button type="button" class="sidebar-chapter-btn" onclick="setTypeFilter('all')"><span class="sidebar-chapter-pill"><span class="sidebar-num">🌟</span><span>அனைத்தும் (580)</span></span></button>
            <button type="button" class="sidebar-chapter-btn" onclick="setTypeFilter('film')"><span class="sidebar-chapter-pill"><span class="sidebar-num">🎬</span><span>திரைப்படங்கள்</span></span></button>
            <button type="button" class="sidebar-chapter-btn" onclick="setTypeFilter('audio')"><span class="sidebar-chapter-pill"><span class="sidebar-num">🎵</span><span>இசை வெளியீடுகள்</span></span></button>
          </div>
        </div>
        """
    },
    "thirukkural.html": {
        "id": "dharmaSidebar",
        "pill": "📖 அறநெறி (Dharma Sub-menu)",
        "title": "அறநெறி &amp; வாழ்வியல்",
        "sub": "திருக்குறள் &amp; சுத்த சன்மார்க்கம்",
        "items": [
            ("thirukkural.html", "📜", "திருக்குறள் (1330 குறள்கள்)", True),
            ("sanmargam.html", "🪔", "சுத்த சன்மார்க்கம் (வள்ளலார்)", False)
        ],
        "custom_footer": """
        <div style="margin-top:16px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.08);">
          <div style="font-size:0.76rem; color:#38bdf8; font-weight:700; text-transform:uppercase; margin-bottom:8px;">முப்பால் பகுப்பு:</div>
          <div style="display:flex; flex-direction:column; gap:6px;">
            <button type="button" class="sidebar-chapter-btn" onclick="filterByText('அறத்துப்பால்')"><span class="sidebar-chapter-pill"><span class="sidebar-num">🌿</span><span>அறத்துப்பால் (380)</span></span></button>
            <button type="button" class="sidebar-chapter-btn" onclick="filterByText('பொருட்பால்')"><span class="sidebar-chapter-pill"><span class="sidebar-num">👑</span><span>பொருட்பால் (700)</span></span></button>
            <button type="button" class="sidebar-chapter-btn" onclick="filterByText('காமத்துப்பால்')"><span class="sidebar-chapter-pill"><span class="sidebar-num">🌺</span><span>காமத்துப்பால் (250)</span></span></button>
          </div>
        </div>
        """
    },
    "about.html": {
        "id": "guruSidebar",
        "pill": "🏛️ குருவருள் (Guru Sub-menu)",
        "title": "குருவருள் &amp; அறிமுகம்",
        "sub": "காஞ்சி மகா பெரியவா அருளுரைகள்",
        "items": [
            ("about.html", "🙏", "மகா பெரியவா தத்துவம்", True),
            ("google-site.html", "🌐", "கூகிள் தளம் நேரடி இணைப்பு", False)
        ],
        "custom_footer": """
        <div style="margin-top:16px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.08);">
          <div style="font-size:0.76rem; color:#38bdf8; font-weight:700; text-transform:uppercase; margin-bottom:8px;">அருளுரை பகுதிகள்:</div>
          <div style="display:flex; flex-direction:column; gap:6px;">
            <button type="button" class="sidebar-chapter-btn" onclick="scrollToSection('teachingsSection')"><span class="sidebar-chapter-pill"><span class="sidebar-num">📖</span><span>தெய்வத்தின் குரல் சாரம்</span></span></button>
            <button type="button" class="sidebar-chapter-btn" onclick="scrollToSection('vedicSection')"><span class="sidebar-chapter-pill"><span class="sidebar-num">🕉️</span><span>வேத சம்ரக்ஷண இயக்கம்</span></span></button>
            <button type="button" class="sidebar-chapter-btn" onclick="scrollToSection('darshanSection')"><span class="sidebar-chapter-pill"><span class="sidebar-num">🌟</span><span>நேரடி தரிசன பதிவுகள்</span></span></button>
          </div>
        </div>
        """
    },
    "index.html": {
        "id": "homeSidebar",
        "pill": "🏠 முதன்மை தளங்கள் (Quick Portals)",
        "title": "குரு குல தேசம்",
        "sub": "ஆன்மீக &amp; கல்வி நெறிக்களங்கள்",
        "items": [
            ("index.html", "🏠", "முகப்பு (580 வெளியீடுகள்)", True),
            ("kalvi.html", "🎓", "சைவ நெறி கல்வி (12 தரங்கள்)", False),
            ("school.html", "🏫", "இணையப் பள்ளி போர்டல்", False),
            ("saiva-neri.html", "🕉️", "சைவ நெறி &amp; தேவாரம்", False),
            ("irai-isai-virundhu.html", "🎵", "இறை இசை விருந்து", False),
            ("thirukkural.html", "📖", "திருக்குறள் &amp; சன்மார்க்கம்", False),
            ("about.html", "🏛️", "காஞ்சி மகா பெரியவா", False)
        ],
        "has_grades": True
    }
}

GRADES_GRID = """
      <div class="sidebar-other-grades" style="margin-top:16px;">
        <div class="sidebar-other-grades-title">12 தரப் பாடநூல்கள் (Grade Portals):</div>
        <div class="sidebar-grades-grid">
          <a href="tharam-1.html" class="sidebar-grade-pill">1</a>
          <a href="tharam-2.html" class="sidebar-grade-pill">2</a>
          <a href="tharam-3.html" class="sidebar-grade-pill">3</a>
          <a href="tharam-4.html" class="sidebar-grade-pill">4</a>
          <a href="tharam-5.html" class="sidebar-grade-pill">5</a>
          <a href="tharam-6.html" class="sidebar-grade-pill">6</a>
          <a href="tharam-7.html" class="sidebar-grade-pill">7</a>
          <a href="tharam-8.html" class="sidebar-grade-pill">8</a>
          <a href="tharam-9.html" class="sidebar-grade-pill">9</a>
          <a href="tharam-10.html" class="sidebar-grade-pill">10</a>
          <a href="tharam-11.html" class="sidebar-grade-pill">11</a>
          <a href="tharam-12.html" class="sidebar-grade-pill">12</a>
        </div>
      </div>
"""

def generate_sidebar_html(cfg):
    items_html = ""
    for href, icon, label, is_active in cfg["items"]:
        act_group = "active" if is_active else ""
        act_btn = "active" if is_active else ""
        items_html += f"""
        <div class="sidebar-chapter-group {act_group}">
          <a href="{href}" class="sidebar-chapter-btn {act_btn}">
            <span class="sidebar-chapter-pill">
              <span class="sidebar-num">{icon}</span>
              <span>{label}</span>
            </span>
          </a>
        </div>
        """

    grades_html = GRADES_GRID if cfg.get("has_grades") else ""
    custom_footer = cfg.get("custom_footer", "")

    return f"""
    <!-- Dedicated Sub-Menu Sidebar for Chosen Group -->
    <aside class="course-sidebar dedicated-sub-sidebar" id="{cfg['id']}">
      <div class="sidebar-header">
        <div class="dedicated-sub-header">
          <span class="dedicated-group-pill">{cfg['pill']}</span>
        </div>
        <h3 class="sidebar-title">{cfg['title']}</h3>
        <p class="sidebar-sub">{cfg['sub']}</p>
      </div>

      <nav class="sidebar-nav" aria-label="Group Sub-menu">
        {items_html}
      </nav>

      {grades_html}
      {custom_footer}
    </aside>
    """

for filename, cfg in PAGES_CONFIG.items():
    filepath = os.path.join(ROOT, filename)
    if not os.path.exists(filepath):
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # If already has course-layout-container, skip
    if 'course-layout-container' in content:
        print(f"{filename} already has course-layout-container")
        continue

    # Find <main class="main-content"> ... </main>
    m = re.search(r'(<main class="main-content">)([\s\S]*?)(</main>)', content)
    if not m:
        print(f"Could not find main tag in {filename}")
        continue

    sidebar_html = generate_sidebar_html(cfg)
    inner_content = m.group(2)

    new_main = f"""{m.group(1)}
    <div class="course-layout-container">
      {sidebar_html}
      <div class="course-main-column">
        {inner_content}
      </div>
    </div>
  {m.group(3)}"""

    content = content[:m.start()] + new_main + content[m.end():]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    # Sync to docs and site
    for dest_dir in [DOCS, SITE]:
        dest_path = os.path.join(dest_dir, filename)
        if os.path.exists(dest_dir):
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(content)

    print(f"Successfully added dedicated sidebar to {filename} across root, docs, and site")
