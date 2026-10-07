import os
import re
import glob

print("=== Physical Replacement of Old Header with Left Strip Bar & Context-Only Top Bar ===")

# Definition of the Left Strip Bar HTML
def get_left_strip_html(current_page):
    nav_items = [
        ('index.html', '🏠', 'முகப்பு'),
        ('kalvi.html', '🎓', 'கல்வி நெறி'),
        ('virtues.html', '🔤', 'நற்பண்புகள்'),
        ('saiva-neri.html', '🕉️', 'சைவ நெறி'),
        ('irai-isai-virundhu.html', '🎵', 'இறை இசை'),
        ('thirukkural.html', '📖', 'திருக்குறள்'),
        ('sanmargam.html', '🪔', 'சன்மார்க்கம்'),
        ('murugan.html', '🔱', 'முருகன்'),
        ('sakthi.html', '🌸', 'சக்தி நெறி'),
        ('vinayagar.html', '🐘', 'விநாயகர்'),
        ('vaishnava.html', '🪷', 'வைணவம்'),
        ('syllabus.html', '📚', 'பாடத்திட்டம்'),
        ('about.html', '🏛️', 'பெரியவா')
    ]

    items_html = []
    for href, icon, label in nav_items:
        # Match active
        is_active = (current_page == href)
        if not is_active and current_page.startswith('tharam-') and href == 'kalvi.html':
            is_active = True
        active_cls = ' active' if is_active else ''
        items_html.append(f'''      <a href="{href}" class="strip-item{active_cls}" data-tooltip="{label}">
        <span class="strip-item-icon">{icon}</span>
        <span class="strip-item-label">{label}</span>
      </a>''')

    return f'''  <!-- LEFT STRIP BAR (PRIMARY GLOBAL SHELL) -->
  <aside class="left-strip-bar" id="leftStripBar" aria-label="Quick Access Sidebar">
    <div class="strip-header">
      <a href="index.html" class="strip-brand-link" title="குரு குல தேசம்">
        <span class="strip-emblem">ॐ</span>
        <span class="strip-brand-text">குரு குல தேசம்</span>
      </a>
      <button type="button" class="strip-toggle-btn" id="stripToggleBtn" onclick="toggleLeftStrip()" title="விரிவுபடுத்து / சுருக்கு" aria-label="Toggle Sidebar">
        <span class="strip-toggle-icon">⇤</span>
      </button>
    </div>

    <nav class="strip-nav-list" id="stripNavList">
{chr(10).join(items_html)}
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

  <div class="strip-backdrop" id="stripBackdrop" onclick="closeMobileStrip()"></div>'''

# Context-Sensitive Top Bar HTML: Only generated if page has relevant sub-items!
def get_context_top_bar_html(current_page):
    # Check Grade pages (tharam-1 to tharam-12)
    m = re.match(r'^tharam-(\d+)\.html$', current_page)
    if m:
        num = int(m.group(1))
        prev_h = f'<a href="tharam-{num-1}.html" class="context-tab-pill"><span class="context-tab-pill-icon">⏪</span><span>தரம் {num-1}</span></a>' if num > 1 else ''
        next_h = f'<a href="tharam-{num+1}.html" class="context-tab-pill"><span class="context-tab-pill-icon">⏩</span><span>தரம் {num+1}</span></a>' if num < 12 else ''
        tabs = f'''        <button type="button" class="context-tab-pill active" onclick="scrollToSection('courseUnits', 'lessonUnitPanel1')"><span class="context-tab-pill-icon">📖</span><span>பாட அலகுகள் 1-5</span></button>
        <button type="button" class="context-tab-pill" onclick="scrollToSection('gradeVirtueBox')"><span class="context-tab-pill-icon">🔤</span><span>நற்பண்பு நெறி</span></button>
        <button type="button" class="context-tab-pill" onclick="scrollToSection('visualDiagramCard')"><span class="context-tab-pill-icon">🎨</span><span>காட்சி விளக்கம்</span></button>
        <button type="button" class="context-tab-pill" onclick="scrollToSection('quizSection')"><span class="context-tab-pill-icon">❓</span><span>சுய வினாடி-வினா</span></button>
        <button type="button" class="context-tab-pill" onclick="scrollToSection('sadhanaBox')"><span class="context-tab-pill-icon">🪔</span><span>தினசரி சாதனை</span></button>
        {prev_h}
        {next_h}
        <a href="kalvi.html" class="context-tab-pill"><span class="context-tab-pill-icon">🎓</span><span>அனைத்து தரங்கள்</span></a>'''
    elif current_page == 'kalvi.html':
        tabs = '''        <button type="button" class="context-tab-pill active" onclick="scrollToSection('kalviOverview')"><span class="context-tab-pill-icon">🏛️</span><span>பாடநெறி அறிமுகம்</span></button>
        <a href="virtues.html" class="context-tab-pill"><span class="context-tab-pill-icon">🔤</span><span>அகர வரிசை நற்பண்புகள்</span></a>
        <button type="button" class="context-tab-pill" onclick="scrollToSection('tier1Section')"><span class="context-tab-pill-icon">🌟</span><span>தரம் 1-4 (தொடக்க நிலை)</span></button>
        <button type="button" class="context-tab-pill" onclick="scrollToSection('tier2Section')"><span class="context-tab-pill-icon">🪔</span><span>தரம் 5-8 (இடைநிலை)</span></button>
        <button type="button" class="context-tab-pill" onclick="scrollToSection('tier3Section')"><span class="context-tab-pill-icon">🔱</span><span>தரம் 9-12 (உயர்நிலை)</span></button>
        <a href="syllabus.html" class="context-tab-pill"><span class="context-tab-pill-icon">📚</span><span>முழு பாடத்திட்டம்</span></a>'''
    elif current_page == 'virtues.html':
        tabs = '''        <button type="button" class="context-tab-pill active" onclick="filterVirtues('all')"><span class="context-tab-pill-icon">🌟</span><span>அனைத்து நற்பண்புகள் (30+)</span></button>
        <button type="button" class="context-tab-pill" onclick="filterVirtues('tier-1')"><span class="context-tab-pill-icon">🟢</span><span>Tier 1: அறிதல் (தரம் 1-4)</span></button>
        <button type="button" class="context-tab-pill" onclick="filterVirtues('tier-2')"><span class="context-tab-pill-icon">🟡</span><span>Tier 2: செய்தல் (தரம் 5-8)</span></button>
        <button type="button" class="context-tab-pill" onclick="filterVirtues('tier-3')"><span class="context-tab-pill-icon">🔴</span><span>Tier 3: காத்தல் (தரம் 9-12)</span></button>
        <a href="kalvi.html" class="context-tab-pill"><span class="context-tab-pill-icon">🎓</span><span>கல்வித் தளம்</span></a>'''
    elif current_page in ('index.html', ''):
        tabs = '''        <button type="button" class="context-tab-pill active" onclick="setTypeFilter('all')"><span class="context-tab-pill-icon">🌟</span><span>அனைத்து வெளியீடுகள் (580)</span></button>
        <button type="button" class="context-tab-pill" onclick="setTypeFilter('film')"><span class="context-tab-pill-icon">🎬</span><span>முழுத் திரைப்படங்கள்</span></button>
        <button type="button" class="context-tab-pill" onclick="setTypeFilter('audio')"><span class="context-tab-pill-icon">🎵</span><span>இசை வெளியீடுகள்</span></button>
        <button type="button" class="context-tab-pill" onclick="scrollToSection('scriptureStudySection')"><span class="context-tab-pill-icon">🔱</span><span>வேத சைவ நெறி</span></button>
        <button type="button" class="context-tab-pill" onclick="scrollToSection('siteFooter')"><span class="context-tab-pill-icon">📍</span><span>மைய முகவரி</span></button>'''
    elif current_page == 'saiva-neri.html':
        tabs = '''        <button type="button" class="context-tab-pill active" onclick="setTypeFilter('all')"><span class="context-tab-pill-icon">🔱</span><span>அனைத்து சிவப்பதிகங்கள்</span></button>
        <button type="button" class="context-tab-pill" onclick="filterByText('தேவாரம்')"><span class="context-tab-pill-icon">🌿</span><span>தேவாரம்</span></button>
        <button type="button" class="context-tab-pill" onclick="filterByText('திருவாசகம்')"><span class="context-tab-pill-icon">💎</span><span>திருவாசகம்</span></button>
        <button type="button" class="context-tab-pill" onclick="filterByText('திருமந்திரம்')"><span class="context-tab-pill-icon">🧘</span><span>திருமந்திரம்</span></button>
        <button type="button" class="context-tab-pill" onclick="filterByText('ருத்ரம்')"><span class="context-tab-pill-icon">🔥</span><span>ஸ்ரீ ருத்ரம்</span></button>'''
    elif current_page in ('murugan.html', 'sakthi.html', 'vinayagar.html', 'vaishnava.html'):
        tabs = f'''        <a href="murugan.html" class="context-tab-pill{' active' if current_page == 'murugan.html' else ''}"><span class="context-tab-pill-icon">🔱</span><span>முருகன் (Kaumaram)</span></a>
        <a href="sakthi.html" class="context-tab-pill{' active' if current_page == 'sakthi.html' else ''}"><span class="context-tab-pill-icon">🌸</span><span>சக்தி (Shaktham)</span></a>
        <a href="vinayagar.html" class="context-tab-pill{' active' if current_page == 'vinayagar.html' else ''}"><span class="context-tab-pill-icon">🐘</span><span>விநாயகர் (Ganapathyam)</span></a>
        <a href="vaishnava.html" class="context-tab-pill{' active' if current_page == 'vaishnava.html' else ''}"><span class="context-tab-pill-icon">🪷</span><span>வைணவம் (Vaishnavam)</span></a>'''
    elif current_page == 'thirukkural.html':
        tabs = '''        <button type="button" class="context-tab-pill active" onclick="setTypeFilter('all')"><span class="context-tab-pill-icon">📖</span><span>அனைத்து குறள்கள்</span></button>
        <button type="button" class="context-tab-pill" onclick="filterByText('அறத்துப்பால்')"><span class="context-tab-pill-icon">🌿</span><span>அறத்துப்பால்</span></button>
        <button type="button" class="context-tab-pill" onclick="filterByText('பொருட்பால்')"><span class="context-tab-pill-icon">👑</span><span>பொருட்பால்</span></button>
        <button type="button" class="context-tab-pill" onclick="filterByText('காமத்துப்பால்')"><span class="context-tab-pill-icon">🌺</span><span>காமத்துப்பால்</span></button>
        <button type="button" class="context-tab-pill" onclick="setTypeFilter('film')"><span class="context-tab-pill-icon">🎬</span><span>குறள் திரைப்படங்கள்</span></button>'''
    elif current_page == 'sanmargam.html':
        tabs = '''        <button type="button" class="context-tab-pill active" onclick="setTypeFilter('all')"><span class="context-tab-pill-icon">🪔</span><span>திருவருட்பா படைப்புகள்</span></button>
        <button type="button" class="context-tab-pill" onclick="filterByText('ஜீவகாருண்யம்')"><span class="context-tab-pill-icon">☀️</span><span>ஜீவகாருண்யம்</span></button>
        <button type="button" class="context-tab-pill" onclick="filterByText('ஜோதி')"><span class="context-tab-pill-icon">🕯️</span><span>ஜோதி வழிபாடு</span></button>
        <button type="button" class="context-tab-pill" onclick="setTypeFilter('audio')"><span class="context-tab-pill-icon">🎵</span><span>சன்மார்க்க இசை</span></button>'''
    elif current_page == 'about.html':
        tabs = '''        <button type="button" class="context-tab-pill active" onclick="scrollToSection('darshanSection')"><span class="context-tab-pill-icon">🌟</span><span>மகா பெரியவா தரிசனம்</span></button>
        <button type="button" class="context-tab-pill" onclick="scrollToSection('teachingsSection')"><span class="context-tab-pill-icon">📖</span><span>தெய்வத்தின் குரல்</span></button>
        <button type="button" class="context-tab-pill" onclick="scrollToSection('vedicSection')"><span class="context-tab-pill-icon">🕉️</span><span>வேத சம்ரக்ஷணம்</span></button>
        <button type="button" class="context-tab-pill" onclick="scrollToSection('siteFooter')"><span class="context-tab-pill-icon">📍</span><span>மைய முகவரி</span></button>'''
    elif current_page in ('syllabus.html', 'classes.html'):
        tabs = f'''        <a href="syllabus.html" class="context-tab-pill{' active' if current_page == 'syllabus.html' else ''}"><span class="context-tab-pill-icon">📚</span><span>முழு பாடத்திட்டம்</span></a>
        <a href="classes.html" class="context-tab-pill{' active' if current_page == 'classes.html' else ''}"><span class="context-tab-pill-icon">🏛️</span><span>வகுப்புகள் அட்டவணை</span></a>
        <a href="virtues.html" class="context-tab-pill"><span class="context-tab-pill-icon">🔤</span><span>நற்பண்பு நெறிமுறை</span></a>
        <a href="kalvi.html" class="context-tab-pill"><span class="context-tab-pill-icon">🎓</span><span>12 தரங்கள்</span></a>'''
    else:
        # No context tabs for this page -> Top bar does not exist!
        return ''

    return f'''  <!-- CONTEXT-SENSITIVE TOP BAR (Sub-items for active section only) -->
  <header class="context-top-bar" id="contextTopBar">
    <div class="context-bar-container">
      <button type="button" class="context-mobile-btn" onclick="toggleLeftStrip()" title="பக்கப்பட்டி">☰</button>
      <nav class="context-tabs-nav" id="contextTabsNav" aria-label="Section Tabs">
{tabs}
      </nav>
      <div class="header-right-tools">
        <div class="context-search-wrapper">
          <span class="context-search-icon">🔍</span>
          <input type="text" id="contextQuickSearch" class="context-search-input" placeholder="தேடுக... [/]" oninput="handleContextSearch(this.value)" autocomplete="off">
          <button type="button" class="context-search-clear" id="contextSearchClear" onclick="clearContextSearch()" style="display: none;">✕</button>
        </div>
        <div class="context-tool-group">
          <button type="button" class="context-tool-btn font-dec-btn" onclick="adjustFontSize(-0.06)" title="எழுத்தளவைக் குறைக்க (A-)">A⁻</button>
          <span class="font-scale-indicator" id="fontScaleIndicator">100%</span>
          <button type="button" class="context-tool-btn font-inc-btn" onclick="adjustFontSize(0.06)" title="எழுத்தளவை அதிகரிக்க (A+)">A⁺</button>
        </div>
        <button type="button" class="context-tool-btn theme-quick-btn" onclick="cycleTheme()" title="வண்ணக் கருப்பொருள்">
          <span class="theme-icon" id="themeQuickIcon">🌓</span>
        </button>
        <button type="button" class="context-profile-pill" onclick="openUserSettingsModal('profile')" title="சுயவிவரம் &amp; அமைப்புகள்">
          <span class="pill-avatar" id="pillAvatarIcon">👤</span>
          <span class="pill-name" id="pillUserName">சாதகர்</span>
        </button>
      </div>
    </div>
  </header>'''

# Process HTML files
all_html_files = []
for pat in ['*.html', 'docs/*.html', 'site/*.html']:
    for f in glob.glob(pat):
        # Exclude raw scraped and embed files
        if not f.startswith('scraped_') and not f.startswith('embed_'):
            all_html_files.append(f)

print(f"Targeting {len(all_html_files)} production HTML files...")

for filepath in all_html_files:
    fname = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as fp:
        html = fp.read()

    # 1. Ensure <body> has class="has-left-strip"
    html = re.sub(r'<body([^>]*)>', lambda m: f'<body{m.group(1)}>' if 'has-left-strip' in m.group(1) else f'<body class="has-left-strip"{m.group(1)}>', html)

    # 2. Generate Left Strip & Context Bar HTML
    strip_html = get_left_strip_html(fname)
    top_bar_html = get_context_top_bar_html(fname)
    combined_nav_replacement = strip_html + ("\n\n" + top_bar_html if top_bar_html else "")

    # 3. Replace the entire old <header class="site-header">...</header>
    old_header_pat = re.compile(r'<header class="site-header".*?</header>', re.DOTALL)
    if old_header_pat.search(html):
        html = old_header_pat.sub(combined_nav_replacement, html)
        print(f"Replaced old header with Left Strip & Context Bar in: {filepath}")
    else:
        # Check if already has left-strip-bar
        if 'left-strip-bar' not in html:
            # Insert right after <body...>
            html = re.sub(r'(<body[^>]*>)', r'\1\n' + combined_nav_replacement, html)
            print(f"Inserted Left Strip into: {filepath}")

    with open(filepath, 'w', encoding='utf-8') as fp:
        fp.write(html)

print("=== Physical Replacement Finished Successfully ===")
