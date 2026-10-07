import os
import re

print("=== Upgrading Top Menu Bar to Context-Sensitive Tabs (Eliminating Duplication) ===")

# --- 1. CSS UPGRADE ---
CONTEXT_TABS_CSS = """
/* -------------------------------------------------------------------------- */
/* CONTEXT-SENSITIVE TOP MENU TABS (Replacing Duplicate Navbar)               */
/* -------------------------------------------------------------------------- */
.header-container {
  max-width: 100%;
  padding: 10px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.context-tabs-nav {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow-x: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
  padding: 4px 6px;
  flex-grow: 1;
  justify-content: center;
}

.context-tabs-nav::-webkit-scrollbar {
  display: none;
}

.context-tab-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  color: var(--text-muted);
  text-decoration: none;
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
  font-family: inherit;
}

.context-tab-pill:hover {
  background: rgba(212, 175, 55, 0.15);
  border-color: var(--gold);
  color: var(--gold-soft);
  transform: translateY(-1px);
}

.context-tab-pill.active {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.25), rgba(224, 159, 62, 0.15));
  border-color: var(--gold-bright);
  color: var(--gold-bright);
  box-shadow: 0 2px 10px rgba(212, 175, 55, 0.25);
}

.context-tab-pill-icon {
  font-size: 0.95rem;
  line-height: 1;
}

.header-right-tools {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

@media (max-width: 991px) {
  .context-tabs-nav {
    justify-content: flex-start;
  }
}
"""

css_paths = ['assets/css/style.css', 'docs/assets/css/style.css', 'site/assets/css/style.css']
for cp in css_paths:
    if os.path.exists(cp):
        with open(cp, 'r', encoding='utf-8') as fp:
            css_text = fp.read()
        
        # Remove old separate .context-sensitive-bar if present or hide it
        if '/* CONTEXT-SENSITIVE TOP MENU TABS' not in css_text:
            css_text += "\n" + CONTEXT_TABS_CSS
        else:
            print(f"Tabs CSS already in {cp}")

        # Hide any redundant separate context-sensitive-bar if rendered
        css_text = re.sub(
            r'\.context-sensitive-bar\s*\{[^}]*\}',
            '.context-sensitive-bar { display: none !important; }',
            css_text
        )

        with open(cp, 'w', encoding='utf-8') as fp:
            fp.write(css_text)
        print(f"Updated CSS in: {cp}")


# --- 2. JS UPGRADE ---
# In main.js, mountAppShell now populates the top header's navigation area with Context-Sensitive Tabs!
UPGRADED_JS_ENGINE = r'''
/* ========================================================================== */
/* GURUKULA CONTEXT-SENSITIVE TOP MENU TABS & APP SHELL                       */
/* ========================================================================== */

function getContextTabsForPage() {
  const path = window.location.pathname.toLowerCase();
  const filename = path.split('/').pop() || 'index.html';

  // 1. Grade / Tharam Pages (tharam-1.html to tharam-12.html)
  const gradeMatch = filename.match(/^tharam-(\d+)\.html$/);
  if (gradeMatch) {
    const gradeNum = parseInt(gradeMatch[1], 10);
    const prevGrade = gradeNum > 1 ? `tharam-${gradeNum - 1}.html` : null;
    const nextGrade = gradeNum < 12 ? `tharam-${gradeNum + 1}.html` : null;

    return [
      { id: 'tab-units', icon: '📖', label: 'பாட அலகுகள்', action: "scrollToSection('courseUnits', 'lessonUnitPanel1')" },
      { id: 'tab-virtues', icon: '🔤', label: 'நற்பண்பு நெறி', action: "scrollToSection('gradeVirtueBox')" },
      { id: 'tab-diagram', icon: '🎨', label: 'காட்சி விளக்கம்', action: "scrollToSection('visualDiagramCard')" },
      { id: 'tab-quiz', icon: '❓', label: 'சுய வினாடி-வினா', action: "scrollToSection('quizSection')" },
      { id: 'tab-sadhana', icon: '🪔', label: 'தினசரி சாதனை', action: "scrollToSection('sadhanaBox')" },
      ...(prevGrade ? [{ id: 'tab-prev', icon: '⏪', label: `தரம் ${gradeNum - 1}`, href: prevGrade }] : []),
      ...(nextGrade ? [{ id: 'tab-next', icon: '⏩', label: `தரம் ${gradeNum + 1}`, href: nextGrade }] : []),
      { id: 'tab-all-grades', icon: '🎓', label: 'அனைத்து தரங்கள்', href: 'kalvi.html' }
    ];
  }

  // 2. Curriculum Hub (kalvi.html)
  if (filename === 'kalvi.html') {
    return [
      { id: 'tab-overview', icon: '🏛️', label: 'பாடநெறி அறிமுகம்', action: "scrollToSection('kalviOverview')", active: true },
      { id: 'tab-virtues', icon: '🔤', label: 'அகர வரிசை நற்பண்புகள்', href: 'virtues.html' },
      { id: 'tab-tier1', icon: '🌟', label: 'தரம் 1-4 (தொடக்க நிலை)', action: "scrollToSection('tier1Section')" },
      { id: 'tab-tier2', icon: '🪔', label: 'தரம் 5-8 (இடைநிலை)', action: "scrollToSection('tier2Section')" },
      { id: 'tab-tier3', icon: '🔱', label: 'தரம் 9-12 (உயர்நிலை)', action: "scrollToSection('tier3Section')" },
      { id: 'tab-syllabus', icon: '📚', label: 'முழு பாடத்திட்டம்', href: 'syllabus.html' }
    ];
  }

  // 3. Virtues Matrix (virtues.html)
  if (filename === 'virtues.html') {
    return [
      { id: 'tab-all', icon: '🌟', label: 'அனைத்து நற்பண்புகள் (30+)', action: "filterVirtues('all')", active: true },
      { id: 'tab-t1', icon: '🟢', label: 'Tier 1: அறிதல் (தரம் 1-4)', action: "filterVirtues('tier-1')" },
      { id: 'tab-t2', icon: '🟡', label: 'Tier 2: செய்தல் (தரம் 5-8)', action: "filterVirtues('tier-2')" },
      { id: 'tab-t3', icon: '🔴', label: 'Tier 3: காத்தல் (தரம் 9-12)', action: "filterVirtues('tier-3')" },
      { id: 'tab-kalvi', icon: '🎓', label: 'கல்வித் தளம்', href: 'kalvi.html' }
    ];
  }

  // 4. Master Home (index.html)
  if (filename === 'index.html' || filename === '') {
    return [
      { id: 'tab-all-media', icon: '🌟', label: 'அனைத்து வெளியீடுகள் (580)', action: "setTypeFilter('all')", active: true },
      { id: 'tab-films', icon: '🎬', label: 'முழுத் திரைப்படங்கள்', action: "setTypeFilter('film')" },
      { id: 'tab-audio', icon: '🎵', label: 'இசை வெளியீடுகள்', action: "setTypeFilter('audio')" },
      { id: 'tab-phil', icon: '🔱', label: 'தத்துவ சாரம்', action: "scrollToSection('philosophySection')" },
      { id: 'tab-contact', icon: '📍', label: 'மைய முகவரி', action: "scrollToSection('siteFooter')" }
    ];
  }

  // 5. Saiva Neri (saiva-neri.html)
  if (filename === 'saiva-neri.html') {
    return [
      { id: 'tab-all-shiva', icon: '🔱', label: 'அனைத்து சிவப்பதிகங்கள்', action: "setTypeFilter('all')", active: true },
      { id: 'tab-thevaram', icon: '🌿', label: 'தேவாரம்', action: "filterByText('தேவாரம்')" },
      { id: 'tab-thiruvasagam', icon: '💎', label: 'திருவாசகம்', action: "filterByText('திருவாசகம்')" },
      { id: 'tab-thirumandhiram', icon: '🧘', label: 'திருமந்திரம்', action: "filterByText('திருமந்திரம்')" },
      { id: 'tab-rudram', icon: '🔥', label: 'ஸ்ரீ ருத்ரம்', action: "filterByText('ருத்ரம்')" }
    ];
  }

  // 6. Traditions / Deities
  if (['murugan.html', 'sakthi.html', 'vinayagar.html', 'vaishnava.html'].includes(filename)) {
    return [
      { id: 'tab-murugan', icon: '🔱', label: 'முருகன் (Kaumaram)', href: 'murugan.html', active: filename === 'murugan.html' },
      { id: 'tab-sakthi', icon: '🌸', label: 'சக்தி (Shaktham)', href: 'sakthi.html', active: filename === 'sakthi.html' },
      { id: 'tab-vinayagar', icon: '🐘', label: 'விநாயகர் (Ganapathyam)', href: 'vinayagar.html', active: filename === 'vinayagar.html' },
      { id: 'tab-vaishnava', icon: '🪷', label: 'வைணவம் (Vaishnavam)', href: 'vaishnava.html', active: filename === 'vaishnava.html' }
    ];
  }

  // 7. Thirukkural (thirukkural.html)
  if (filename === 'thirukkural.html') {
    return [
      { id: 'tab-all-tk', icon: '📖', label: 'அனைத்து குறள்கள்', action: "setTypeFilter('all')", active: true },
      { id: 'tab-aram', icon: '🌿', label: 'அறத்துப்பால்', action: "filterByText('அறத்துப்பால்')" },
      { id: 'tab-porul', icon: '👑', label: 'பொருட்பால்', action: "filterByText('பொருட்பால்')" },
      { id: 'tab-inbam', icon: '🌺', label: 'காமத்துப்பால்', action: "filterByText('காமத்துப்பால்')" },
      { id: 'tab-films-tk', icon: '🎬', label: 'குறள் திரைப்படங்கள்', action: "setTypeFilter('film')" }
    ];
  }

  // 8. Sanmargam (sanmargam.html)
  if (filename === 'sanmargam.html') {
    return [
      { id: 'tab-all-san', icon: '🪔', label: 'திருவருட்பா படைப்புகள்', action: "setTypeFilter('all')", active: true },
      { id: 'tab-jeeva', icon: '☀️', label: 'ஜீவகாருண்யம்', action: "filterByText('ஜீவகாருண்யம்')" },
      { id: 'tab-jyoti', icon: '🕯️', label: 'ஜோதி வழிபாடு', action: "filterByText('ஜோதி')" },
      { id: 'tab-audio-san', icon: '🎵', label: 'சன்மார்க்க இசை', action: "setTypeFilter('audio')" }
    ];
  }

  // 9. About / Periyava (about.html)
  if (filename === 'about.html') {
    return [
      { id: 'tab-periyava-darshan', icon: '🌟', label: 'மகா பெரியவா தரிசனம்', action: "scrollToSection('darshanSection')", active: true },
      { id: 'tab-deivathin-kural', icon: '📖', label: 'தெய்வத்தின் குரல்', action: "scrollToSection('teachingsSection')" },
      { id: 'tab-vedic-preservation', icon: '🕉️', label: 'வேத சம்ரக்ஷணம்', action: "scrollToSection('vedicSection')" },
      { id: 'tab-hq-address', icon: '📍', label: 'மைய முகவரி', action: "scrollToSection('siteFooter')" }
    ];
  }

  // 10. Syllabus / Classes
  if (filename === 'syllabus.html' || filename === 'classes.html') {
    return [
      { id: 'tab-full-syl', icon: '📚', label: 'முழு பாடத்திட்டம்', href: 'syllabus.html', active: filename === 'syllabus.html' },
      { id: 'tab-classes', icon: '🏛️', label: 'வகுப்புகள் அட்டவணை', href: 'classes.html', active: filename === 'classes.html' },
      { id: 'tab-virtues-map', icon: '🔤', label: 'நற்பண்பு நெறிமுறை', href: 'virtues.html' },
      { id: 'tab-grade-portal', icon: '🎓', label: '12 தரங்கள்', href: 'kalvi.html' }
    ];
  }

  // Default fallback
  return [
    { id: 'tab-home', icon: '🏠', label: 'முகப்பு', href: 'index.html' },
    { id: 'tab-kalvi', icon: '🎓', label: 'கல்வி', href: 'kalvi.html' },
    { id: 'tab-virtues', icon: '🔤', label: 'நற்பண்புகள்', href: 'virtues.html' },
    { id: 'tab-saiva', icon: '🕉️', label: 'சைவ நெறி', href: 'saiva-neri.html' }
  ];
}

function scrollToSection(id, optionalTabId) {
  if (optionalTabId && typeof switchCourseTab === 'function') {
    switchCourseTab(optionalTabId);
  }
  const el = document.getElementById(id) || document.querySelector('.' + id);
  if (el) {
    const yOffset = -75;
    const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset;
    window.scrollTo({ top: Math.max(0, y), behavior: 'smooth' });
  }
}

function filterByText(keyword) {
  const searchInput = document.getElementById('contextQuickSearch') || document.getElementById('searchInput');
  if (searchInput) {
    searchInput.value = keyword;
    handleContextSearch(keyword);
  }
}

function renderContextTabsIntoHeader() {
  const headerContainer = document.querySelector('.header-container');
  if (!headerContainer) return;

  // 1. Remove or hide the old duplicate main-nav
  const oldNav = document.getElementById('mainNav');
  if (oldNav) {
    oldNav.style.display = 'none';
  }

  // 2. Remove any previous context-tabs-nav or right tools
  const existingTabs = document.getElementById('contextTabsNav');
  if (existingTabs) existingTabs.remove();
  const existingTools = document.querySelector('.header-right-tools');
  if (existingTools) existingTools.remove();

  // 3. Build Context-Sensitive Menu Tabs
  const tabs = getContextTabsForPage();
  const tabsNav = document.createElement('nav');
  tabsNav.id = 'contextTabsNav';
  tabsNav.className = 'context-tabs-nav';
  tabsNav.setAttribute('aria-label', 'Context Specific Tabs');

  tabsNav.innerHTML = tabs.map((t, idx) => {
    if (t.href) {
      return `
        <a href="${t.href}" class="context-tab-pill ${t.active ? 'active' : ''}" id="${t.id}">
          <span class="context-tab-pill-icon">${t.icon}</span>
          <span>${t.label}</span>
        </a>
      `;
    } else {
      return `
        <button type="button" class="context-tab-pill ${t.active || idx === 0 ? 'active' : ''}" id="${t.id}" onclick="handleTabClick(this, '${t.action}')">
          <span class="context-tab-pill-icon">${t.icon}</span>
          <span>${t.label}</span>
        </button>
      `;
    }
  }).join('');

  // 4. Build Right Tools Dock
  const rightTools = document.createElement('div');
  rightTools.className = 'header-right-tools';
  rightTools.innerHTML = `
    <div class="context-search-wrapper">
      <span class="context-search-icon">🔍</span>
      <input type="text" id="contextQuickSearch" class="context-search-input" placeholder="தேடுக... [/]" oninput="handleContextSearch(this.value)" autocomplete="off">
      <button type="button" class="context-search-clear" id="contextSearchClear" onclick="clearContextSearch()" style="display: none;">✕</button>
    </div>

    <div class="context-tool-group">
      <button type="button" class="context-tool-btn font-dec-btn" onclick="adjustFontSize(-0.06)" title="எழுத்தளவைக் குறைக்க (A-)">A⁻</button>
      <span class="font-scale-indicator" id="fontScaleIndicator" title="தற்போதைய எழுத்தளவு">100%</span>
      <button type="button" class="context-tool-btn font-inc-btn" onclick="adjustFontSize(0.06)" title="எழுத்தளவை அதிகரிக்க (A+)">A⁺</button>
    </div>

    <button type="button" class="context-tool-btn theme-quick-btn" onclick="cycleTheme()" title="வண்ணக் கருப்பொருள் மாற்று">
      <span class="theme-icon" id="themeQuickIcon">🌓</span>
    </button>

    <button type="button" class="context-profile-pill" onclick="openUserSettingsModal('profile')" title="பயனர் சுயவிவரம் &amp; அமைப்புகள்">
      <span class="pill-avatar" id="pillAvatarIcon">👤</span>
      <span class="pill-name" id="pillUserName">சாதகர்</span>
    </button>
  `;

  headerContainer.appendChild(tabsNav);
  headerContainer.appendChild(rightTools);
}

function handleTabClick(btn, actionStr) {
  // Update active pill state
  const parent = btn.closest('.context-tabs-nav');
  if (parent) {
    parent.querySelectorAll('.context-tab-pill').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }
  // Execute action
  try {
    const fn = new Function(actionStr);
    fn();
  } catch (e) {
    console.error('Error executing tab action:', e);
  }
}
'''

# Update mountAppShell to call renderContextTabsIntoHeader()
js_paths = ['assets/js/main.js', 'docs/assets/js/main.js', 'site/assets/js/main.js']
for jp in js_paths:
    if os.path.exists(jp):
        with open(jp, 'r', encoding='utf-8') as fp:
            js_text = fp.read()
        
        # Replace mountAppShell with updated implementation that sets up context tabs
        if '/* GURUKULA CONTEXT-SENSITIVE TOP MENU TABS' not in js_text:
            # Insert the new tabs engine before mountAppShell
            js_text = js_text.replace('function mountAppShell() {', UPGRADED_JS_ENGINE + '\n\nfunction mountAppShell() {')
        
        # Make sure mountAppShell calls renderContextTabsIntoHeader()
        if 'renderContextTabsIntoHeader();' not in js_text:
            js_text = js_text.replace(
                '// 1. Mobile Backdrop',
                'renderContextTabsIntoHeader();\n\n  // 1. Mobile Backdrop'
            )

        with open(jp, 'w', encoding='utf-8') as fp:
            fp.write(js_text)
        print(f"Updated JS in: {jp}")

print("=== Upgrading Context Tabs Completed ===")
