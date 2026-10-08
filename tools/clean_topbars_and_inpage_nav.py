#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/clean_topbars_and_inpage_nav.py

Cleans topbars across all pages in Gurukula Desam:
1. Replaces topbars with clean, spacious breadcrumb topbars containing strictly:
   - Mobile hamburger button
   - Back button ("பின்னே")
   - Breadcrumb pathway ("முகப்பு / [Category] / [Page Title]")
   - Tools (quick search, font zoom, theme switcher, profile pill)
2. Removes all in-page navigation tabs/pills from header and relocates them into the content area (<main>) in appropriate sections.
3. Eliminates duplicate legacy <header class="site-header"> from tharam-2.html through tharam-12.html.
4. Adds static breadcrumb-back-btn to all non-home topbars for instant no-FOUC rendering.
"""

import os
import re

HEADER_RIGHT_TOOLS = '''      <div class="header-right-tools">
        <div class="context-search-wrapper">
          <span class="context-search-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></span>
          <input type="text" id="contextQuickSearch" class="context-search-input" placeholder="தேடுக... [/]" oninput="handleContextSearch(this.value)" autocomplete="off">
          <button type="button" class="context-search-clear" id="contextSearchClear" onclick="clearContextSearch()" style="display: none;"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>
        </div>
        <div class="context-tool-group">
          <button type="button" class="context-tool-btn font-dec-btn" onclick="adjustFontSize(-0.06)" title="எழுத்தளவைக் குறைக்க (A-)"><span style="font-size:0.9em; font-weight:700">A</span><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" style="width:0.7em; height:0.7em; vertical-align:0.35em"><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
          <span class="font-scale-indicator" id="fontScaleIndicator">100%</span>
          <button type="button" class="context-tool-btn font-inc-btn" onclick="adjustFontSize(0.06)" title="எழுத்தளவை அதிகரிக்க (A+)"><span style="font-size:0.9em; font-weight:700">A</span><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" style="width:0.7em; height:0.7em; vertical-align:0.35em"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
        </div>
        <button type="button" class="context-tool-btn theme-quick-btn" onclick="cycleTheme()" title="வண்ணக் கருப்பொருள்">
          <span class="theme-icon" id="themeQuickIcon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg></span>
        </button>
        <button type="button" class="context-profile-pill" onclick="openUserSettingsModal('profile')" title="சுயவிவரம் &amp; அமைப்புகள்">
          <span class="pill-avatar" id="pillAvatarIcon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span>
          <span class="pill-name" id="pillUserName">சாதகர்</span>
        </button>
      </div>'''

def make_top_bar(back_fallback, parent_href, parent_title, current_title):
    parent_part = ""
    if parent_href and parent_title:
        parent_part = f'''
          <span class="crumb-sep">/</span>
          <a href="{parent_href}" class="crumb-link">{parent_title}</a>'''
    
    return f'''  <!-- CONTEXT-SENSITIVE TOP BAR -->
  <header class="context-top-bar" id="contextTopBar">
    <div class="context-bar-container">
      <div class="context-bar-left">
        <button type="button" class="mobile-hamburger-btn" onclick="togglePrimaryMenu()" title="பட்டி திறக்க" aria-label="முதன்மை பட்டி">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
        <button type="button" class="breadcrumb-back-btn" onclick="if(window.history.length > 1){{ window.history.back(); }} else {{ window.location.href='{back_fallback}'; }}" title="பின்னே செல்ல (Go Back)">
          <svg class="gkd-icon gkd-arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          <span>பின்னே</span>
        </button>
        <nav class="context-breadcrumbs" id="contextBreadcrumbs" aria-label="தள வழிகாட்டல்">
          <a href="index.html" class="crumb-link crumb-home" title="முகப்பு">
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
            <span class="crumb-text">முகப்பு</span>
          </a>{parent_part}
          <span class="crumb-sep">/</span>
          <span class="crumb-current" id="topBarCurrentCrumb">{current_title}</span>
        </nav>
      </div>
{HEADER_RIGHT_TOOLS}
    </div>
  </header>'''

def process_tharam(grade_num):
    fname = f"tharam-{grade_num}.html"
    if not os.path.exists(fname):
        return
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove duplicate <header class="site-header">
    content = re.sub(r'<!--\s*Site Header\s*-->\s*<header class="site-header">[\s\S]*?<\/header>', '', content)
    content = re.sub(r'<header class="site-header">[\s\S]*?<\/header>', '', content)

    # 2. Replace context-top-bar
    new_top_bar = make_top_bar(
        back_fallback="kalvi.html",
        parent_href="kalvi.html",
        parent_title="வாழ்வியல் நெறி",
        current_title=f"தரம் {grade_num} (Grade {grade_num})"
    )
    content = re.sub(r'<!--\s*CONTEXT-SENSITIVE TOP BAR\s*-->\s*<header class="context-top-bar" id="contextTopBar">[\s\S]*?<\/header>', new_top_bar, content)

    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Processed {fname}")

def process_saiva_neri():
    fname = "saiva-neri.html"
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()

    new_top_bar = make_top_bar(
        back_fallback="index.html",
        parent_href="",
        parent_title="",
        current_title="சைவ நெறி &amp; தெய்வங்கள்"
    )
    content = re.sub(r'<!--\s*CONTEXT-SENSITIVE TOP BAR[^>]*-->\s*<header class="context-top-bar" id="contextTopBar">[\s\S]*?<\/header>', new_top_bar, content)

    inpage_nav = '''    <!-- In-Page Hymn Category Navigation -->
    <div class="inpage-content-nav" aria-label="சிவப்பதிகப் பிரிவுகள்">
      <button type="button" class="context-tab-pill active" onclick="setTypeFilter('all')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="M12 6c-3.5 0-6 2.5-6 6v3h2v-3c0-2.5 1.8-4 4-4s4 1.5 4 4v3h2v-3c0-3.5-2.5-6-6-6z"/><path d="M9 16h6"/><polygon points="12 2 10.5 5 13.5 5 12 2" fill="currentColor"/></svg></span><span>அனைத்து சிவப்பதிகங்கள்</span></button>
      <button type="button" class="context-tab-pill" onclick="filterByText('தேவாரம்')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 4 13a8.9 8.9 0 0 1 8.2-8.9 7 7 0 0 1 7.8 7.8A8.9 8.9 0 0 1 11 20z"/><path d="M12.5 4.5c.5 4.5-1 7.5-5 9.5"/></svg></span><span>தேவாரம்</span></button>
      <button type="button" class="context-tab-pill" onclick="filterByText('திருவாசகம்')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12l4 6-10 12L2 9z"/><path d="M11 3v6l-5-6"/><path d="M13 3v6l5-6"/></svg></span><span>திருவாசகம்</span></button>
      <button type="button" class="context-tab-pill" onclick="filterByText('திருமந்திரம்')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="5" r="2.5"/><path d="M4 18c0-3.5 3.5-5 8-5s8 1.5 8 5"/><path d="M6 14l2 4 4-2 4 2 2-4"/></svg></span><span>திருமந்திரம்</span></button>
      <button type="button" class="context-tab-pill" onclick="filterByText('ருத்ரம்')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c1 3 3 4.5 4.5 7 1.5 2.5 1.5 5.5 0 8s-4 4-6.5 4c-3 0-5.5-2.5-5.5-6 0-3.5 2-6 4-8.5.5 1.5 1.5 2.5 2.5 2.5.5-2 .5-4.5 1-7z"/></svg></span><span>ஸ்ரீ ருத்ரம்</span></button>
    </div>\n\n'''

    if '<div class="inpage-content-nav"' not in content:
        content = content.replace('<div class="controls-panel">', inpage_nav + '    <div class="controls-panel">', 1)

    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Processed {fname}")

def process_sanmargam():
    fname = "sanmargam.html"
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()

    new_top_bar = make_top_bar(
        back_fallback="thirukkural.html",
        parent_href="thirukkural.html",
        parent_title="அறநெறி &amp; தத்துவம்",
        current_title="சுத்த சன்மார்க்கம் (வள்ளலார்)"
    )
    content = re.sub(r'<!--\s*CONTEXT-SENSITIVE TOP BAR[^>]*-->\s*<header class="context-top-bar" id="contextTopBar">[\s\S]*?<\/header>', new_top_bar, content)

    inpage_nav = '''    <!-- In-Page Sanmargam Category Navigation -->
    <div class="inpage-content-nav" aria-label="சன்மார்க்கப் பிரிவுகள்">
      <button type="button" class="context-tab-pill active" onclick="setTypeFilter('all')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c-.8 2-1.5 3.5-1.5 5a1.5 1.5 0 0 0 3 0c0-1.5-.7-3-1.5-5z" fill="currentColor"/><path d="M5 13c0 4 3 6 7 6s7-2 7-6H5z"/><path d="M10 19v2h4v-2"/></svg></span><span>திருவருட்பா படைப்புகள்</span></button>
      <button type="button" class="context-tab-pill" onclick="filterByText('ஜீவகாருண்யம்')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg></span><span>ஜீவகாருண்யம்</span></button>
      <button type="button" class="context-tab-pill" onclick="filterByText('ஜோதி')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c-.8 2-1.5 3.5-1.5 5a1.5 1.5 0 0 0 3 0c0-1.5-.7-3-1.5-5z" fill="currentColor"/><path d="M5 13c0 4 3 6 7 6s7-2 7-6H5z"/><path d="M10 19v2h4v-2"/></svg></span><span>ஜோதி வழிபாடு</span></button>
      <button type="button" class="context-tab-pill" onclick="setTypeFilter('audio')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg></span><span>சன்மார்க்க இசை</span></button>
    </div>\n\n'''

    if '<div class="inpage-content-nav"' not in content:
        content = content.replace('<div class="controls-panel">', inpage_nav + '    <div class="controls-panel">', 1)

    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Processed {fname}")

def process_deity_page(fname, title, active_key):
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()

    new_top_bar = make_top_bar(
        back_fallback="saiva-neri.html",
        parent_href="saiva-neri.html",
        parent_title="சைவ நெறி &amp; தெய்வங்கள்",
        current_title=title
    )
    content = re.sub(r'<!--\s*CONTEXT-SENSITIVE TOP BAR[^>]*-->\s*<header class="context-top-bar" id="contextTopBar">[\s\S]*?<\/header>', new_top_bar, content)

    m_act = " active" if active_key == "murugan" else ""
    s_act = " active" if active_key == "sakthi" else ""
    v_act = " active" if active_key == "vinayagar" else ""
    va_act = " active" if active_key == "vaishnava" else ""

    inpage_nav = f'''    <!-- Cross-Deity Section Switcher Navigation -->
    <div class="inpage-content-nav" aria-label="தெய்வப் பிரிவுகள்">
      <a href="murugan.html" class="context-tab-pill{m_act}"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="M12 6c-3.5 0-6 2.5-6 6v3h2v-3c0-2.5 1.8-4 4-4s4 1.5 4 4v3h2v-3c0-3.5-2.5-6-6-6z"/><path d="M9 16h6"/><polygon points="12 2 10.5 5 13.5 5 12 2" fill="currentColor"/></svg></span><span>முருகன் (Kaumaram)</span></a>
      <a href="sakthi.html" class="context-tab-pill{s_act}"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4c-1.5 3-2 6-2 9 1 0 2-1 2-2 0 1 1 2 2 2 0-3-.5-6-2-9z"/><path d="M7 10c0 3 1.5 5 3 6-2 0-4-1.5-4.5-4 .5-.7 1-1.3 1.5-2z"/><path d="M17 10c0 3-1.5 5-3 6 2 0 4-1.5 4.5-4-.5-.7-1-1.3-1.5-2z"/><path d="M4 15c2 3 5 4 8 4s6-1 8-4c-2.5 0-4.5 1-8 1s-5.5-1-8-1z"/></svg></span><span>சக்தி (Shaktham)</span></a>
      <a href="vinayagar.html" class="context-tab-pill{v_act}"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3c-4 0-7 3.5-7 7.5 0 2.5 1.2 4.7 3 6l1 4.5h6l1-4.5c1.8-1.3 3-3.5 3-6C19 6.5 16 3 12 3z"/><path d="M12 9v5a1.5 1.5 0 0 1-3 0"/><circle cx="9" cy="8" r="1" fill="currentColor"/><circle cx="15" cy="8" r="1" fill="currentColor"/></svg></span><span>விநாயகர் (Ganapathyam)</span></a>
      <a href="vaishnava.html" class="context-tab-pill{va_act}"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><line x1="12" y1="3" x2="12" y2="9"/><line x1="12" y1="15" x2="12" y2="21"/><line x1="3" y1="12" x2="9" y2="12"/><line x1="15" y1="12" x2="21" y2="12"/><line x1="5.6" y1="5.6" x2="9.9" y2="9.9"/><line x1="14.1" y1="14.1" x2="18.4" y2="18.4"/><line x1="18.4" y1="5.6" x2="14.1" y2="9.9"/><line x1="9.9" y1="14.1" x2="5.6" y2="18.4"/></svg></span><span>வைணவம் (Vaishnavam)</span></a>
    </div>\n\n'''

    if '<div class="inpage-content-nav"' not in content:
        content = content.replace('<div class="controls-panel">', inpage_nav + '    <div class="controls-panel">', 1)

    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Processed {fname}")

def process_virtues():
    fname = "virtues.html"
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()

    new_top_bar = make_top_bar(
        back_fallback="kalvi.html",
        parent_href="kalvi.html",
        parent_title="வாழ்வியல் நெறி",
        current_title="அகர வரிசை நற்பண்புகள்"
    )
    content = re.sub(r'<!--\s*CONTEXT-SENSITIVE TOP BAR[^>]*-->\s*<header class="context-top-bar" id="contextTopBar">[\s\S]*?<\/header>', new_top_bar, content)

    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Processed {fname}")

def process_school():
    fname = "school.html"
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()

    new_top_bar = make_top_bar(
        back_fallback="kalvi.html",
        parent_href="kalvi.html",
        parent_title="வாழ்வியல் நெறி",
        current_title="இணையப் பள்ளி போர்டல்"
    )
    content = re.sub(r'<!--\s*CONTEXT-SENSITIVE TOP BAR[^>]*-->\s*<header class="context-top-bar" id="contextTopBar">[\s\S]*?<\/header>', new_top_bar, content)

    inpage_nav = '''    <!-- In-Page School Portal Section Navigation -->
    <div class="inpage-content-nav" aria-label="பள்ளிப் பிரிவு வழிகாட்டல்">
      <button type="button" class="context-tab-pill active" onclick="scrollToId('portalDashboard')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg></span><span>மாணவர் போர்டல்</span></button>
      <button type="button" class="context-tab-pill" onclick="scrollToId('stemFusionSection')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="2" fill="currentColor"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(30 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(-30 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(90 12 12)"/></svg></span><span>அறிவியல்-வேத சங்கமம்</span></button>
      <button type="button" class="context-tab-pill" onclick="scrollToId('focusStudyHall')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></span><span>தியான &amp; படிப்பு அரங்கம்</span></button>
    </div>\n\n'''

    if '<div class="inpage-content-nav"' not in content:
        # Place before school-stats-row
        content = content.replace('<div class="school-stats-row">', inpage_nav + '    <div class="school-stats-row">', 1)

    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Processed {fname}")

def process_higher_studies():
    fname = "higher-studies.html"
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()

    new_top_bar = make_top_bar(
        back_fallback="kalvi.html",
        parent_href="kalvi.html",
        parent_title="வாழ்வியல் நெறி",
        current_title="வேத-நவீன உயர்கல்வி"
    )
    content = re.sub(r'<!--\s*CONTEXT-SENSITIVE TOP BAR[^>]*-->\s*<header class="context-top-bar" id="contextTopBar">[\s\S]*?<\/header>', new_top_bar, content)

    inpage_nav = '''    <!-- In-Page Collegiate Faculty Section Navigation -->
    <div class="inpage-content-nav" aria-label="உயர்கல்விப் பிரிவு வழிகாட்டல்">
      <button type="button" class="context-tab-pill active" onclick="scrollToId('vidyaHero')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v3"/><path d="M7 5h10l-1.5 4H8.5L7 5z"/><path d="M5 9h14l-1.5 5H6.5L5 9z"/><path d="M3 14h18v7H3v-7z"/><path d="M10 21v-4a2 2 0 0 1 4 0v4"/></svg></span><span>பீட அறிமுகம்</span></button>
      <button type="button" class="context-tab-pill" onclick="scrollToId('dharmaUltimateBanner')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9.5z"/><polyline points="9 21 9 12 15 12 15 21"/></svg></span><span>இல்லற தர்மம்</span></button>
      <button type="button" class="context-tab-pill" onclick="scrollToId('tierUG')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 2 3 3 6 3s6-1 6-3v-5"/></svg></span><span>இளங்கலை B.A./B.Sc.</span></button>
      <button type="button" class="context-tab-pill" onclick="scrollToId('tierPG')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H4a2 2 0 0 0-2 2v13a3 3 0 0 0 3 3h13a3 3 0 0 0 3-3V5a2 2 0 0 0-2-2h-7"/><path d="M19 18a3 3 0 0 0 0-6H6a2 2 0 0 0 0 4h12"/><line x1="8" y1="7" x2="14" y2="7"/><line x1="8" y1="11" x2="12" y2="11"/></svg></span><span>முதுகலை M.A./Acharya</span></button>
      <button type="button" class="context-tab-pill" onclick="scrollToId('tierPhD')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="2" fill="currentColor"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(30 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(-30 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(90 12 12)"/></svg></span><span>முனைவர் Ph.D.</span></button>
      <button type="button" class="context-tab-pill" onclick="scrollToId('tierFellowship')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h2"/><path d="M18 9h2a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2h-2"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.45 1-1 1H7v4h10v-4h-2c-.55 0-1-.45-1-1v-2.34"/><path d="M6 3h12a2 2 0 0 1 2 2v6a6 6 0 0 1-12 0V5a2 2 0 0 1 2-2z"/></svg></span><span>உயர் பட்டயங்கள்</span></button>
      <button type="button" class="context-tab-pill" onclick="scrollToId('glossarySection')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></span><span>சாத்திர கலைச்சொற்கள்</span></button>
      <button type="button" class="context-tab-pill" onclick="scrollToId('fellowshipSection')"><span class="context-tab-pill-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg></span><span>பட்டயச் சான்றிதழ்</span></button>
    </div>\n\n'''

    if '<div class="inpage-content-nav"' not in content:
        # Place right after </section> of vidyaHero
        content = re.sub(r'(</section>\s*(?:<!--\s*2\.\s*ADMISSION)?)', inpage_nav + r'\1', content, count=1)

    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Processed {fname}")

def ensure_back_button(fname, fallback_url):
    if not os.path.exists(fname):
        return
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()

    if "breadcrumb-back-btn" in content:
        return

    pattern = r'(<button type="button" class="mobile-hamburger-btn"[^>]*>[\s\S]*?<\/button>\s*)(<nav class="context-breadcrumbs")'
    replacement = rf'\1<button type="button" class="breadcrumb-back-btn" onclick="if(window.history.length > 1){{ window.history.back(); }} else {{ window.location.href=\'{fallback_url}\'; }}" title="பின்னே செல்ல (Go Back)">\n        <svg class="gkd-icon gkd-arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>\n        <span>பின்னே</span>\n      </button>\n      \2'

    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content, count=1)
        with open(fname, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Added back button to {fname}")

def main():
    print("=== Gurukula Desam Topbar Cleaner & In-Page Nav Relocator ===")
    
    # 1. Tharam 2 through 12
    for g in range(2, 13):
        process_tharam(g)

    # 2. Saiva Neri & Sanmargam
    process_saiva_neri()
    process_sanmargam()

    # 3. Deities
    process_deity_page("murugan.html", "தமிழ் தெய்வம் முருகன்", "murugan")
    process_deity_page("sakthi.html", "அம்பிகை சக்தி நெறி", "sakthi")
    process_deity_page("vinayagar.html", "முழுமுதற் கடவுள் விநாயகர்", "vinayagar")
    process_deity_page("vaishnava.html", "அரங்கன் &amp; கிருஷ்ணர் வைணவம்", "vaishnava")

    # 4. Virtues, School, Higher Studies
    process_virtues()
    process_school()
    process_higher_studies()

    # 5. Ensure static back buttons on remaining topbar pages
    ensure_back_button("tharam-1.html", "kalvi.html")
    ensure_back_button("kalvi.html", "index.html")
    ensure_back_button("about.html", "index.html")
    ensure_back_button("classes.html", "kalvi.html")
    ensure_back_button("syllabus.html", "kalvi.html")
    ensure_back_button("thirukkural.html", "index.html")

    print("[SUCCESS] All files updated!")

if __name__ == "__main__":
    main()
