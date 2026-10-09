"""
Gurukula Desam - Curriculum Redesign & Zero-Wrapper Engine
1. Enforces pure curriculum-driven navigation across all HTML files (removes loose archives/dumps group).
2. Updates books.html and tharam-1..12.html to pure zero-wrapper & zero-border with catalog.js inclusion.
3. Cleans kalvi.html to eliminate obsolete sheets cards and showcase the 4 Gurukula Stages & 7 Books.
"""

import os
import re

ROOT = r"c:\GitHub\Gurukuladesam"

STANDARD_STRIP_BAR = """  <!-- LEFT STRIP BAR (PRIMARY GLOBAL SHELL - CURRICULUM ACADEMY SANCTUARY) -->
  <aside class="left-strip-bar" id="leftStripBar" aria-label="குருகுல முதன்மை பட்டி">
    <div class="strip-header">
      <a href="index.html" class="strip-brand-link" title="குரு குல ஆசிரமம்">
        <span class="strip-emblem"><svg class="gkd-icon gkd-om-icon" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8.2 10.5c-.3-.7-.2-1.5.3-2.1.8-.9 2.2-.9 3 .1.4.5.5 1.2.2 1.8-.4.7-1.1 1.2-1.7 1.7.9.3 1.7.9 2 1.7.4 1.1 0 2.4-1 3.1-1.2.9-2.9.7-3.9-.4-.4-.5-.6-1.1-.6-1.7h1.4c0 .4.2.8.5 1 .6.5 1.5.4 2-.1.4-.4.5-1 .2-1.5-.4-.7-1.2-1-2-1v-1.2c.6 0 1.2-.2 1.5-.7.3-.4.3-.9 0-1.3-.4-.5-1.1-.6-1.6-.2-.3.2-.5.6-.5 1H8.2zm6.3-2.5c.8 0 1.5.5 1.8 1.2l-1.2.5c-.2-.4-.5-.6-.8-.6-.6 0-1 .4-1 1s.4 1 1 1c.5 0 .9-.3 1.1-.7l1.1.6c-.4.8-1.2 1.3-2.2 1.3-1.4 0-2.4-1-2.4-2.4 0-1.3 1-2.4 2.4-2.4zm1.5-1.5c.3 0 .5.2.5.5s-.2.5-.5.5-.5-.2-.5-.5.2-.5.5-.5z"/></svg></span>
        <div style="display: flex; flex-direction: column;">
          <span class="strip-brand-text">குரு குல ஆசிரமம்</span>
          <span style="font-size: 0.68rem; color: #2dd4bf; letter-spacing: 0.05em; font-weight: 600;">வேத-நவீன வித்யாபீடம்</span>
        </div>
      </a>
      <button type="button" class="strip-toggle-btn" id="stripToggleBtn" onclick="togglePrimaryMenu()" data-tooltip="பட்டி விரிவாக்குக / சுருக்குக" title="முதன்மை பட்டி" aria-label="பட்டி மாற்று">
        <span class="strip-toggle-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg></span>
      </button>
    </div>

    <nav class="strip-nav-list" id="stripNavList">

      <!-- 1. ஆசிரம முகப்பு (Ashram Sanctuary Home) -->
      <div class="strip-group" data-group="home">
        <a href="index.html" class="strip-item" data-tooltip="ஆசிரம முகப்பு">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v3"/><path d="M7 5h10l-1.5 4H8.5L7 5z"/><path d="M5 9h14l-1.5 5H6.5L5 9z"/><path d="M3 14h18v7H3v-7z"/><path d="M10 21v-4a2 2 0 0 1 4 0v4"/></svg></span>
          <span class="strip-item-label">ஆசிரம முகப்பு (Sanctuary)</span>
        </a>
      </div>

      <!-- 2. வித்யா குடீரம் & பாடத்திட்டம் (Academy Portal & Core Curriculum) -->
      <div class="strip-group" data-group="curriculum">
        <a href="school.html" class="strip-item strip-has-sub" data-tooltip="வித்யா குடீரம்">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 2 3 3 6 3s6-1 6-3v-5"/></svg></span>
          <span class="strip-item-label">இணையப் பள்ளி &amp; பாடத்திட்டம்</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header">பள்ளி &amp; பாடத்திட்ட மையம்</div>
          <a href="school.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 2 3 3 6 3s6-1 6-3v-5"/></svg></span><span>வித்யா குடீரம் (இணையப் பள்ளி)</span></a>
          <a href="books.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></span><span>7 ஆசிரமப் பாடநூல்கள் அரங்கம்</span></a>
          <a href="syllabus.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg></span><span>பாடத்திட்டம் &amp; வரைபடம் (Syllabus)</span></a>
          <a href="classes.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></span><span>வகுப்புகள் &amp; நேர அட்டவணை</span></a>
          <a href="virtues.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L3 12.5V21h8.5z"/><line x1="16" y1="8" x2="2" y2="22"/><line x1="17.5" y1="15" x2="9" y2="15"/></svg></span><span>அகர வரிசை நற்பண்புகள்</span></a>
        </div>
      </div>

      <!-- 3. நான்கு குருகுலப் பருவங்கள் (The 4 Classical Gurukula Stages - Grades 1 to 12 & Collegiate) -->
      <div class="strip-group" data-group="stages">
        <a href="kalvi.html" class="strip-item strip-has-sub" data-tooltip="4 குருகுலப் பருவங்கள்">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 4 13a8.9 8.9 0 0 1 8.2-8.9 7 7 0 0 1 7.8 7.8A8.9 8.9 0 0 1 11 20z"/><path d="M12.5 4.5c.5 4.5-1 7.5-5 9.5"/></svg></span>
          <span class="strip-item-label">4 குருகுலப் பருவங்கள் (1-12)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <!-- STAGE 1: PRIMARY ACADEMY -->
          <div class="strip-sub-header" style="color: #38bdf8;">1. பாலப் பருவம் (Grades 1 - 4 • அற அடித்தளம் &amp; புராணங்கள்)</div>
          <div class="strip-grades-mini-grid">
            <a href="tharam-1.html" class="strip-grade-mini-pill" title="தரம் 1">1</a>
            <a href="tharam-2.html" class="strip-grade-mini-pill" title="தரம் 2">2</a>
            <a href="tharam-3.html" class="strip-grade-mini-pill" title="தரம் 3">3</a>
            <a href="tharam-4.html" class="strip-grade-mini-pill" title="தரம் 4">4</a>
          </div>
          <a href="vinayagar.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v3"/><path d="M7 5h10l-1.5 4H8.5L7 5z"/><path d="M5 9h14l-1.5 5H6.5L5 9z"/><path d="M3 14h18v7H3v-7z"/><path d="M10 21v-4a2 2 0 0 1 4 0v4"/></svg></span><span>விநாயகர் அகவல் &amp; தொடக்க அறநெறி</span></a>
          <a href="murugan.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3 7h-6l3-7z"/><line x1="12" y1="9" x2="12" y2="22"/></svg></span><span>முருகன் கவசம் &amp; வீரப் பண்பு</span></a>

          <!-- STAGE 2: MIDDLE ACADEMY -->
          <div class="strip-sub-header" style="color: #34d399; margin-top: 8px;">2. இளம் பருவம் (Grades 5 - 8 • திருமுறைகள் &amp; பண்பாடு)</div>
          <div class="strip-grades-mini-grid">
            <a href="tharam-5.html" class="strip-grade-mini-pill" title="தரம் 5">5</a>
            <a href="tharam-6.html" class="strip-grade-mini-pill" title="தரம் 6">6</a>
            <a href="tharam-7.html" class="strip-grade-mini-pill" title="தரம் 7">7</a>
            <a href="tharam-8.html" class="strip-grade-mini-pill" title="தரம் 8">8</a>
          </div>
          <a href="panpaadu.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></span><span>தமிழர் பண்பாடு &amp; 12 மாத விழாக்கள்</span></a>
          <a href="vaishnava.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><line x1="12" y1="3" x2="12" y2="9"/><line x1="12" y1="15" x2="12" y2="21"/><line x1="3" y1="12" x2="9" y2="12"/><line x1="15" y1="12" x2="21" y2="12"/></svg></span><span>வைணவ பக்தி &amp; பிரபந்தம்</span></a>
          <a href="sakthi.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 4c-1.5 3-2 6-2 9 1 0 2-1 2-2 0 1 1 2 2 2 0-3-.5-6-2-9z"/><path d="M7 10c0 3 1.5 5 3 6-2 0-4-1.5-4.5-4 .5-.7 1-1.3 1.5-2z"/><path d="M17 10c0 3-1.5 5-3 6 2 0 4-1.5 4.5-4-.5-.7-1-1.3-1.5-2z"/></svg></span><span>அம்பிகை சக்தி நெறி &amp; தாய்மை</span></a>

          <!-- STAGE 3: SECONDARY ACADEMY -->
          <div class="strip-sub-header" style="color: #facc15; margin-top: 8px;">3. உயர்நிலைப் பருவம் (Grades 9 - 10 • அறநெறி &amp; தத்துவம்)</div>
          <div class="strip-grades-mini-grid">
            <a href="tharam-9.html" class="strip-grade-mini-pill" title="தரம் 9">9</a>
            <a href="tharam-10.html" class="strip-grade-mini-pill" title="தரம் 10">10</a>
          </div>
          <a href="thirukkural.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3H4a2 2 0 0 0-2 2v13a3 3 0 0 0 3 3h13a3 3 0 0 0 3-3V5a2 2 0 0 0-2-2h-7"/><path d="M19 18a3 3 0 0 0 0-6H6a2 2 0 0 0 0 4h12"/><line x1="8" y1="7" x2="14" y2="7"/></svg></span><span>திருக்குறள் (1330 அறநெறி ஆய்வு)</span></a>
          <a href="saiva-neri.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20"/><path d="M12 6c-3.5 0-6 2.5-6 6v3h2v-3c0-2.5 1.8-4 4-4s4 1.5 4 4v3h2v-3c0-3.5-2.5-6-6-6z"/><polygon points="12 2 10.5 5 13.5 5 12 2" fill="currentColor"/></svg></span><span>சைவ சித்தாந்தம் &amp; 172 பதிகங்கள்</span></a>
          <a href="sanmargam.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2c1 3 3 4.5 4.5 7 1.5 2.5 1.5 5.5 0 8s-4 4-6.5 4c-3 0-5.5-2.5-5.5-6 0-3.5 2-6 4-8.5.5 1.5 1.5 2.5 2.5 2.5.5-2 .5-4.5 1-7z"/></svg></span><span>வள்ளலார் திருவருட்பா &amp; சன்மார்க்கம்</span></a>

          <!-- STAGE 4: SENIOR & COLLEGIATE ACADEMY -->
          <div class="strip-sub-header" style="color: #fb923c; margin-top: 8px;">4. மேல்நிலை &amp; உயர்கல்வி (Grades 11 - 12 &amp; கல்லூரி ஆய்வு)</div>
          <div class="strip-grades-mini-grid">
            <a href="tharam-11.html" class="strip-grade-mini-pill" title="தரம் 11">11</a>
            <a href="tharam-12.html" class="strip-grade-mini-pill" title="தரம் 12">12</a>
          </div>
          <a href="higher-studies.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="2" fill="currentColor"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(30 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(-30 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(90 12 12)"/></svg></span><span>வேத-நவீன உயர்கல்வி (STEM &amp; வேதாந்தம்)</span></a>
          <a href="about.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 11V6a2 2 0 0 0-2-2 2 2 0 0 0-2 2v3"/><path d="M14 10V4a2 2 0 0 0-2-2 2 2 0 0 0-2 2v6"/><path d="M10 10.5V6a2 2 0 0 0-2-2 2 2 0 0 0-2 2v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.83L7 15"/></svg></span><span>மகா பெரியவா அருளுரைகள் (தெய்வத்தின் குரல்)</span></a>
        </div>
      </div>

      <!-- 4. வாழ்வியல் சாதனா & இல்லற தர்மம் (Applied Living & Daily Sadhana) -->
      <div class="strip-group" data-group="living">
        <a href="grihastha.html" class="strip-item strip-has-sub" data-tooltip="வாழ்வியல் சாதனா">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c-.8 2-1.5 3.5-1.5 5a1.5 1.5 0 0 0 3 0c0-1.5-.7-3-1.5-5z" fill="currentColor"/><path d="M5 13c0 4 3 6 7 6s7-2 7-6H5z"/><path d="M10 19v2h4v-2"/></svg></span>
          <span class="strip-item-label">தினசரி சாதனா &amp; இல்லறம்</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header">இல்லற நெறி &amp; நலம்</div>
          <a href="grihastha.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg></span><span>இல்லற தர்மம் &amp; குடும்ப சாசனம்</span></a>
          <a href="siddha.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 20A7 7 0 0 1 4 13a8.9 8.9 0 0 1 8.2-8.9 7 7 0 0 1 7.8 7.8A8.9 8.9 0 0 1 11 20z"/><path d="M12.5 4.5c.5 4.5-1 7.5-5 9.5"/></svg></span><span>பதினெண் சித்தர் வாழ்வியல் &amp; மூலிகை</span></a>
          <a href="kalvi.html" class="strip-sub-item"><span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v3"/><path d="M7 5h10l-1.5 4H8.5L7 5z"/><path d="M5 9h14l-1.5 5H6.5L5 9z"/><path d="M3 14h18v7H3v-7z"/><path d="M10 21v-4a2 2 0 0 1 4 0v4"/></svg></span><span>வாழ்வியல் மையம் (12 நிலைகள் வழிகாட்டி)</span></a>
        </div>
      </div>

    </nav>

    <div class="strip-footer-dock">
      <button type="button" class="strip-dock-btn" onclick="openUserSettingsModal('preferences')" title="அமைப்புகள்" data-tooltip="அமைப்புகள்">
        <span class="strip-dock-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/></svg></span>
        <span class="strip-dock-label">அமைப்புகள்</span>
      </button>
      <button type="button" class="strip-dock-btn profile-dock-btn" onclick="openUserSettingsModal('profile')" title="சுயவிவரம்" data-tooltip="சுயவிவரம்">
        <span class="strip-dock-avatar" id="stripAvatarIcon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span>
        <span class="strip-dock-label" id="stripUserName">சாதகர்</span>
      </button>
    </div>
  </aside>

  <div class="strip-backdrop" id="stripBackdrop" onclick="closePrimaryMenu()"></div>"""

GRADE_STYLE_ZERO_WRAPPER = """  <style>
    /* Focused Grade Curriculum Container - Zero-Wrapper & Zero-Border Architecture */
    .grade-curriculum-container,
    .books-library-container {
      max-width: 1280px;
      margin: 0 auto;
      padding: 10px 0 60px;
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
    }
    .grade-hero-banner,
    .library-hero-banner {
      background: transparent !important;
      border: none !important;
      border-radius: 0 !important;
      padding: 16px 0 20px !important;
      margin-bottom: 16px !important;
      box-shadow: none !important;
      position: relative;
    }
    .grade-hero-banner::after,
    .library-hero-banner::after {
      content: "" !important;
      display: none !important;
    }
    .grade-switch-strip {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      margin: 8px 0 16px 0;
      padding: 8px 0;
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
    }
  </style>"""

def update_all_html_navigation():
    count = 0
    pattern = re.compile(r'<!--\s*LEFT STRIP BAR[\s\S]*?</aside>(?:\s*<div class="strip-backdrop"[^>]*></div>)?', re.DOTALL)
    fallback_pattern = re.compile(r'<aside class="left-strip-bar"[\s\S]*?</aside>(?:\s*<div class="strip-backdrop"[^>]*></div>)?', re.DOTALL)

    for fname in os.listdir(ROOT):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(ROOT, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        if pattern.search(content):
            new_content = pattern.sub(STANDARD_STRIP_BAR, content)
        elif fallback_pattern.search(content):
            new_content = fallback_pattern.sub(STANDARD_STRIP_BAR, content)
        else:
            continue

        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f"Updated navigation in {fname}")

    print(f"Total HTML files with updated navigation: {count}")

def update_grade_pages_zero_wrapper_and_catalog():
    target_files = ['books.html'] + [f"tharam-{i}.html" for i in range(1, 13)]
    for fname in target_files:
        fpath = os.path.join(ROOT, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Replace <style> block with zero wrapper style
        style_pattern = re.compile(r'<style>[\s\S]*?</style>', re.DOTALL)
        if style_pattern.search(content):
            content = style_pattern.sub(GRADE_STYLE_ZERO_WRAPPER, content)

        # 2. Ensure catalog.js is included before books-reader.js
        if 'assets/data/catalog.js' not in content:
            content = content.replace(
                '<script src="assets/js/books-reader.js',
                '<script src="assets/data/catalog.js"></script>\n  <script src="assets/js/books-reader.js'
            )

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated zero-wrapper styles & catalog.js in {fname}")

if __name__ == '__main__':
    update_all_html_navigation()
    update_grade_pages_zero_wrapper_and_catalog()
