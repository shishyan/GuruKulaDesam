#!/usr/bin/env python3
"""
tools/curriculum/apply_navigation_upgrade.py
Updates main.js to implement:
1. Universal Back button + Breadcrumb trail in sticky header
2. Dedicated tabs container inside page header content (replacing top bar pills)
3. Full breadcrumb hierarchy generator
"""

import re
import subprocess
import sys

def upgrade_main_js(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update GKD_ICONS with back, theme, menu if missing
    icon_additions = """  user: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
  back: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>',
  theme: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>',
  menu: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>'"""

    old_user_icon = re.search(r'  user: [^\r\n]+', content)
    if old_user_icon and 'back:' not in content:
        content = content[:old_user_icon.start()] + icon_additions + content[old_user_icon.end():]

    # 2. Add getBreadcrumbsForPage and handleUniversalBack
    nav_helpers = """
function getBreadcrumbsForPage() {
  const path = window.location.pathname.toLowerCase();
  const filename = path.split('/').pop() || 'index.html';

  if (filename === 'index.html' || filename === '') {
    return [{ label: 'ஆசிரம முகப்பு', href: 'index.html' }];
  }

  const gradeMatch = filename.match(/^tharam-(\\d+)\\.html$/);
  if (gradeMatch) {
    const num = gradeMatch[1];
    return [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'வாழ்வியல் நெறி', href: 'kalvi.html' },
      { label: 'தரம் ' + num, href: filename }
    ];
  }

  const map = {
    'kalvi.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'வாழ்வியல் மையம் (12 நிலைகள்)', href: 'kalvi.html' }
    ],
    'school.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'கல்வி', href: 'kalvi.html' },
      { label: 'இணையப் பள்ளி போர்டல்', href: 'school.html' }
    ],
    'higher-studies.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'கல்வி', href: 'kalvi.html' },
      { label: 'வேதாந்த உயர்கல்வி', href: 'higher-studies.html' }
    ],
    'virtues.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'வாழ்வியல்', href: 'kalvi.html' },
      { label: 'அகர வரிசை நற்பண்புகள்', href: 'virtues.html' }
    ],
    'syllabus.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'கல்வி', href: 'kalvi.html' },
      { label: 'சைவ சித்தாந்த பாடத்திட்டம்', href: 'syllabus.html' }
    ],
    'classes.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'கல்வி', href: 'kalvi.html' },
      { label: 'வகுப்புகள் & அட்டவணை', href: 'classes.html' }
    ],
    'saiva-neri.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'சைவ நெறி (172 திருப்பதிகங்கள்)', href: 'saiva-neri.html' }
    ],
    'murugan.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'வழிபாட்டு நெறி', href: 'saiva-neri.html' },
      { label: 'முருகப் பெருமான்', href: 'murugan.html' }
    ],
    'sakthi.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'வழிபாட்டு நெறி', href: 'saiva-neri.html' },
      { label: 'சக்தி நெறி', href: 'sakthi.html' }
    ],
    'vinayagar.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'வழிபாட்டு நெறி', href: 'saiva-neri.html' },
      { label: 'விநாயகர் பெருமான்', href: 'vinayagar.html' }
    ],
    'vaishnava.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'வழிபாட்டு நெறி', href: 'saiva-neri.html' },
      { label: 'வைணவ நெறி', href: 'vaishnava.html' }
    ],
    'thirukkural.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'தமிழ்மறை திருக்குறள் (185)', href: 'thirukkural.html' }
    ],
    'review_quality.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'திருக்குறள்', href: 'thirukkural.html' },
      { label: 'திரைத் தர ஆய்வு அரங்கம்', href: 'review_quality.html' }
    ],
    'sanmargam.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'வள்ளலார் சுத்த சன்மார்க்கம்', href: 'sanmargam.html' }
    ],
    'irai-isai-virundhu.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'இறை இசை விருந்து', href: 'irai-isai-virundhu.html' }
    ],
    'youtube.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'YouTube காணொளி அரங்கம் (580)', href: 'youtube.html' }
    ],
    'about.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'காஞ்சி மகா பெரியவா', href: 'about.html' }
    ],
    'help.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'உதவி & வழிகாட்டல் மையம்', href: 'help.html' }
    ],
    'google-site.html': [
      { label: 'முகப்பு', href: 'index.html' },
      { label: 'கூகிள் தளம் நேரடி இணைப்பு', href: 'google-site.html' }
    ]
  };

  return map[filename] || [
    { label: 'முகப்பு', href: 'index.html' },
    { label: 'பக்கம்', href: filename }
  ];
}

function handleUniversalBack() {
  if (window.history.length > 1 && document.referrer && document.referrer.includes(window.location.hostname)) {
    window.history.back();
  } else {
    const crumbs = getBreadcrumbsForPage();
    if (crumbs && crumbs.length > 1) {
      window.location.href = crumbs[crumbs.length - 2].href;
    } else {
      window.location.href = 'index.html';
    }
  }
}

function renderDedicatedPageTabs() {
  const tabs = getContextTabsForPage();
  if (!tabs || tabs.length === 0) return;

  if (document.querySelector('.dedicated-page-tabs-container')) return;

  const main = document.querySelector('main.main-content, main.page-container, main');
  if (!main) return;

  const hero = main.querySelector('.hero-banner, .ashram-hero-artwork, .vidya-hero-art, .page-header, .portal-hero, .grade-lms-tracker-banner');

  const container = document.createElement('div');
  container.className = 'dedicated-page-tabs-container';
  container.innerHTML = `
    <div class="dedicated-tabs-label">
      <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h7"/></svg>
      <span>பிரிவுகள் &amp; நேரடிச் சுவடிகள் (Sections &amp; Quick Access):</span>
    </div>
    <nav class="dedicated-page-tabs-bar" aria-label="பக்கத்தின் பிரிவுகள்">
      ${tabs.map((t, idx) => {
        if (t.href) {
          return `
            <a href="${t.href}" class="dedicated-tab-pill ${t.active ? 'active' : ''}" id="${t.id}">
              <span class="dedicated-tab-pill-icon">${getModernIcon(t.icon)}</span>
              <span>${t.label}</span>
            </a>
          `;
        } else {
          return `
            <button type="button" class="dedicated-tab-pill ${t.active || idx === 0 ? 'active' : ''}" id="${t.id}" onclick="handleTabClick(this, '${t.action}')">
              <span class="dedicated-tab-pill-icon">${getModernIcon(t.icon)}</span>
              <span>${t.label}</span>
            </button>
          `;
        }
      }).join('')}
    </nav>
  `;

  if (hero && hero.parentNode) {
    if (hero.classList.contains('hero-banner')) {
      hero.appendChild(container);
    } else {
      hero.parentNode.insertBefore(container, hero.nextSibling);
    }
  } else {
    main.prepend(container);
  }
}
"""

    # 3. Replace renderContextTabsIntoHeader
    new_render_header = """function renderContextTabsIntoHeader() {
  const headerContainer = document.querySelector('.context-bar-container') || document.querySelector('.header-container');
  if (!headerContainer) return;

  // 1. Hide legacy redundant navigation
  const oldNav = document.getElementById('mainNav');
  if (oldNav) oldNav.style.display = 'none';

  // 2. Remove loose pills from top bar if present
  const existingTabs = document.getElementById('contextTabsNav');
  if (existingTabs && existingTabs.parentNode === headerContainer) {
    existingTabs.parentNode.removeChild(existingTabs);
  }
  const existingTools = document.querySelector('.header-right-tools');
  if (existingTools && existingTools.parentNode) existingTools.parentNode.removeChild(existingTools);

  // 3. Ensure Primary Hamburger Trigger is present
  let hamburgerBtn = headerContainer.querySelector('.primary-hamburger-btn');
  if (!hamburgerBtn) {
    hamburgerBtn = document.createElement('button');
    hamburgerBtn.type = 'button';
    hamburgerBtn.className = 'primary-hamburger-btn';
    hamburgerBtn.onclick = togglePrimaryMenu;
    hamburgerBtn.title = 'முதன்மை பட்டி (6 பிரிவுகள்)';
    hamburgerBtn.setAttribute('aria-label', 'முதன்மை பட்டி');
    hamburgerBtn.innerHTML = `
      <span class="hb-icon">${GKD_ICONS.menu}</span>
      <span class="hb-emblem">ॐ</span>
      <span class="hb-label">முதன்மை பட்டி</span>
    `;
    headerContainer.appendChild(hamburgerBtn);
  }

  // 4. Universal Back Button
  let backBtn = headerContainer.querySelector('.header-back-btn');
  if (!backBtn) {
    backBtn = document.createElement('button');
    backBtn.type = 'button';
    backBtn.className = 'header-back-btn';
    backBtn.onclick = handleUniversalBack;
    backBtn.title = 'பின்னே செல்ல (Go Back)';
    backBtn.setAttribute('aria-label', 'பின்னே');
    backBtn.innerHTML = `
      <span class="back-btn-icon">${GKD_ICONS.back}</span>
      <span class="back-btn-text">பின்னே</span>
    `;
    headerContainer.appendChild(backBtn);
  }

  // 5. Breadcrumb Trail
  let breadcrumbs = headerContainer.querySelector('.header-breadcrumbs');
  if (!breadcrumbs) {
    breadcrumbs = document.createElement('nav');
    breadcrumbs.className = 'header-breadcrumbs';
    breadcrumbs.setAttribute('aria-label', 'தள வழிசெலுத்தல் (Breadcrumbs)');
    headerContainer.appendChild(breadcrumbs);
  }
  const crumbs = getBreadcrumbsForPage();
  breadcrumbs.innerHTML = crumbs.map((c, i) => {
    if (i === crumbs.length - 1) {
      return `<span class="crumb-current">${c.label}</span>`;
    } else {
      return `<a href="${c.href}" class="crumb-link">${c.label}</a><span class="crumb-sep">/</span>`;
    }
  }).join('');

  // 6. Right Tools Dock (Search, Font Scale, Drone, Theme, User Profile)
  const rightTools = document.createElement('div');
  rightTools.className = 'header-right-tools';
  rightTools.innerHTML = `
    <div class="context-search-wrapper">
      <span class="context-search-icon">${GKD_ICONS.search}</span>
      <input type="text" id="contextQuickSearch" class="context-search-input" placeholder="தேடுக... [/]" oninput="handleContextSearch(this.value)" autocomplete="off">
      <button type="button" class="context-search-clear" id="contextSearchClear" onclick="clearContextSearch()" style="display: none;">${GKD_ICONS.close}</button>
    </div>

    <div class="context-tool-group">
      <button type="button" class="context-tool-btn font-dec-btn" onclick="adjustFontSize(-0.06)" title="எழுத்தளவைக் குறைக்க (A-)">A⁻</button>
      <span class="font-scale-indicator" id="fontScaleIndicator" title="தற்போதைய எழுத்தளவு">100%</span>
      <button type="button" class="context-tool-btn font-inc-btn" onclick="adjustFontSize(0.06)" title="எழுத்தளவை அதிகரிக்க (A+)">A⁺</button>
    </div>

    <button type="button" class="context-tool-btn ambient-drone-btn" id="ambientDroneBtn" onclick="toggleAmbientDrone()" title="நாத தியான ஒலி (Ambient Tanpura Drone)"><span class="drone-icon" id="ambientDroneIcon">${GKD_ICONS.deepam}</span></button>
    <button type="button" class="context-tool-btn theme-quick-btn" onclick="cycleTheme()" title="வண்ணக் கருப்பொருள் மாற்று">
      <span class="theme-icon" id="themeQuickIcon">${GKD_ICONS.theme}</span>
    </button>

    <button type="button" class="context-profile-pill" onclick="openUserSettingsModal('profile')" title="பயனர் சுயவிவரம் &amp; அமைப்புகள்">
      <span class="pill-avatar" id="pillAvatarIcon">${GKD_ICONS.user}</span>
      <span class="pill-name" id="pillUserName">சாதகர்</span>
    </button>
  `;
  headerContainer.appendChild(rightTools);

  // 7. Render dedicated tabs inside the page hero content
  renderDedicatedPageTabs();
}

function handleTabClick(btn, actionStr) {
  const parent = btn.closest('.dedicated-page-tabs-bar') || btn.closest('.context-tabs-nav');
  if (parent) {
    parent.querySelectorAll('.dedicated-tab-pill, .context-tab-pill').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }
  try {
    const fn = new Function(actionStr);
    fn();
  } catch (e) {
    console.error('Error executing tab action:', e);
  }
}
"""

    # Replace renderContextTabsIntoHeader and handleTabClick block
    old_fn_pattern = re.compile(r'function renderContextTabsIntoHeader\(\)\s*\{.*?\n\}\n\nfunction handleTabClick\(btn, actionStr\)\s*\{.*?\n\}', re.DOTALL)
    if old_fn_pattern.search(content):
        content = old_fn_pattern.sub(new_render_header, content)
    else:
        print("[WARN] Could not match old renderContextTabsIntoHeader with regex, attempting alternate replacement.")
        idx1 = content.find('function renderContextTabsIntoHeader()')
        idx2 = content.find('function mountAppShell()')
        if idx1 != -1 and idx2 != -1:
            content = content[:idx1] + new_render_header + "\n\n" + content[idx2:]

    # Also add nav_helpers before renderContextTabsIntoHeader if not present
    if 'function getBreadcrumbsForPage()' not in content:
        target_pos = content.find('function renderContextTabsIntoHeader()')
        content = content[:target_pos] + nav_helpers + "\n\n" + content[target_pos:]

    # Also inside mountAppShell, ensure renderDedicatedPageTabs is called
    if 'renderDedicatedPageTabs();' not in content:
        content = content.replace('renderContextTabsIntoHeader();', 'renderContextTabsIntoHeader();\n  renderDedicatedPageTabs();')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Successfully upgraded {filepath}")

if __name__ == '__main__':
    upgrade_main_js('docs/assets/js/main.js')
