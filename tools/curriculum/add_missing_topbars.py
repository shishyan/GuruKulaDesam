#!/usr/bin/env python3
"""
tools/curriculum/add_missing_topbars.py
Adds standard #contextTopBar with Back button, breadcrumbs, and right tools
to the 5 pages that previously lacked static headers.
"""

import os
import re

files = ['google-site.html', 'help.html', 'irai-isai-virundhu.html', 'review_quality.html', 'youtube.html']
from apply_static_header_upgrade import get_breadcrumbs, build_breadcrumbs_html, BACK_BTN_HTML

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    docs_dir = os.path.join(repo_root, 'docs')
    for f in files:
        path = os.path.join(docs_dir, f)
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as fl:
            content = fl.read()
        if 'id="contextTopBar"' in content:
            continue
        crumbs = get_breadcrumbs(f)
        b_html = build_breadcrumbs_html(crumbs)
        header_html = f'''
  <!-- CONTEXT-SENSITIVE TOP BAR -->
  <header class="context-top-bar" id="contextTopBar">
    <div class="context-bar-container">
      <button type="button" class="primary-hamburger-btn" onclick="togglePrimaryMenu()" title="முதன்மை பட்டி (6 பிரிவுகள்)" aria-label="முதன்மை பட்டி">
        <span class="hb-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg></span>
        <span class="hb-emblem">ॐ</span>
        <span class="hb-label">முதன்மை பட்டி</span>
      </button>
{BACK_BTN_HTML}
{b_html}
      <div class="header-right-tools">
        <div class="context-search-wrapper">
          <span class="context-search-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></span>
          <input type="text" id="contextQuickSearch" class="context-search-input" placeholder="தேடுக... [/]" oninput="handleContextSearch(this.value)" autocomplete="off">
          <button type="button" class="context-search-clear" id="contextSearchClear" onclick="clearContextSearch()" style="display: none;"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>
        </div>
        <div class="context-tool-group">
          <button type="button" class="context-tool-btn font-dec-btn" onclick="adjustFontSize(-0.06)" title="எழுத்தளவைக் குறைக்க (A-)">A⁻</button>
          <span class="font-scale-indicator" id="fontScaleIndicator">100%</span>
          <button type="button" class="context-tool-btn font-inc-btn" onclick="adjustFontSize(0.06)" title="எழுத்தளவை அதிகரிக்க (A+)">A⁺</button>
        </div>
        <button type="button" class="context-tool-btn ambient-drone-btn" id="ambientDroneBtn" onclick="toggleAmbientDrone()" title="நாத தியான ஒலி (Ambient Tanpura Drone)"><span class="drone-icon" id="ambientDroneIcon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c-.8 2-1.5 3.5-1.5 5a1.5 1.5 0 0 0 3 0c0-1.5-.7-3-1.5-5z" fill="currentColor"/><path d="M5 13c0 4 3 6 7 6s7-2 7-6H5z"/><path d="M10 19v2h4v-2"/></svg></span></button>
        <button type="button" class="context-tool-btn theme-quick-btn" onclick="cycleTheme()" title="வண்ணக் கருப்பொருள்">
          <span class="theme-icon" id="themeQuickIcon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg></span>
        </button>
        <button type="button" class="context-profile-pill" onclick="openUserSettingsModal('profile')" title="சுயவிவரம் &amp; அமைப்புகள்">
          <span class="pill-avatar" id="pillAvatarIcon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span>
          <span class="pill-name" id="pillUserName">சாதகர்</span>
        </button>
      </div>
    </div>
  </header>
'''
        main_match = re.search(r'<main', content)
        if main_match:
            pos = main_match.start()
            new_content = content[:pos] + header_html + '\n  ' + content[pos:]
            with open(path, 'w', encoding='utf-8') as fl:
                fl.write(new_content)
            print('Inserted header into', f)

if __name__ == '__main__':
    main()
