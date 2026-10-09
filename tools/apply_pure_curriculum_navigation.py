import os, re, glob, sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"c:\GitHub\Gurukuladesam"

PURE_CURRICULUM_STRIP_BAR = """  <!-- LEFT STRIP BAR (PRIMARY GLOBAL SHELL - CURRICULUM ACADEMY SANCTUARY) -->
  <aside class="left-strip-bar" id="leftStripBar" aria-label="குருகுல முதன்மை பட்டி">
    <div class="strip-header">
      <a href="index.html" class="strip-brand-link" title="குரு குல ஆசிரமம்">
        <span class="strip-emblem"><svg class="gkd-icon gkd-om-icon" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8.2 10.5c-.3-.7-.2-1.5.3-2.1.8-.9 2.2-.9 3 .1.4.5.5 1.2.2 1.8-.4.7-1.1 1.2-1.7 1.7.9.3 1.7.9 2 1.7.4 1.1 0 2.4-1 3.1-1.2.9-2.9.7-3.9-.4-.4-.5-.6-1.1-.6-1.7h1.4c0 .4.2.8.5 1 .6.5 1.5.4 2-.1.4-.4.5-1 .2-1.5-.4-.7-1.2-1-2-1v-1.2c.6 0 1.2-.2 1.5-.7.3-.4.3-.9 0-1.3-.4-.5-1.1-.6-1.6-.2-.3.2-.5.6-.5 1H8.2zm6.3-2.5c.8 0 1.5.5 1.8 1.2l-1.2.5c-.2-.4-.5-.6-.8-.6-.6 0-1 .4-1 1s.4 1 1 1c.5 0 .9-.3 1.1-.7l1.1.6c-.4.8-1.2 1.3-2.2 1.3-1.4 0-2.4-1-2.4-2.4 0-1.3 1-2.4 2.4-2.4zm1.5-1.5c.3 0 .5.2.5.5s-.2.5-.5.5-.5-.2-.5-.5.2-.5.5-.5z"/></svg></span>
        <div style="display: flex; flex-direction: column;">
          <span class="strip-brand-text">குரு குல ஆசிரமம்</span>
          <span style="font-size: 0.68rem; color: #2dd4bf; letter-spacing: 0.05em; font-weight: 600;">பள்ளிப் பாடத்திட்டம்</span>
        </div>
      </a>
      <button type="button" class="strip-toggle-btn" id="stripToggleBtn" onclick="togglePrimaryMenu()" data-tooltip="பட்டி விரிவாக்குக / சுருக்குக" title="முதன்மை பட்டி" aria-label="பட்டி மாற்று">
        <span class="strip-toggle-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg></span>
      </button>
    </div>

    <nav class="strip-nav-list" id="stripNavList">

      <!-- 1. பாடத்திட்ட முகப்பு (Curriculum Sanctuary Home) -->
      <div class="strip-group" data-group="home">
        <a href="index.html" class="strip-item" data-tooltip="பாடத்திட்ட முகப்பு">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v3"/><path d="M7 5h10l-1.5 4H8.5L7 5z"/><path d="M5 9h14l-1.5 5H6.5L5 9z"/><path d="M3 14h18v7H3v-7z"/><path d="M10 21v-4a2 2 0 0 1 4 0v4"/></svg></span>
          <span class="strip-item-label">பாடத்திட்ட முகப்பு</span>
        </a>
      </div>

      <!-- 2. பருவம் 1: பாலப் பருவம் (Primary: Grades 1 - 4) -->
      <div class="strip-group" data-group="stage1">
        <a href="tharam-1.html" class="strip-item strip-has-sub" data-tooltip="1. பாலப் பருவம் (1-4)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3 7h-6l3-7z"/><line x1="12" y1="9" x2="12" y2="22"/></svg></span>
          <span class="strip-item-label">1. பாலப் பருவம் (1–4)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color: #38bdf8;">பாலப் பருவம் • அற அடித்தளம்</div>
          <a href="tharam-1.html" class="strip-sub-item"><span class="strip-sub-icon">1️⃣</span><span>தரம் 1 (Grade 1) • 7 நூல்கள்</span></a>
          <a href="tharam-2.html" class="strip-sub-item"><span class="strip-sub-icon">2️⃣</span><span>தரம் 2 (Grade 2) • 7 நூல்கள்</span></a>
          <a href="tharam-3.html" class="strip-sub-item"><span class="strip-sub-icon">3️⃣</span><span>தரம் 3 (Grade 3) • 7 நூல்கள்</span></a>
          <a href="tharam-4.html" class="strip-sub-item"><span class="strip-sub-icon">4️⃣</span><span>தரம் 4 (Grade 4) • 7 நூல்கள்</span></a>
        </div>
      </div>

      <!-- 3. பருவம் 2: இளம் பருவம் (Middle: Grades 5 - 8) -->
      <div class="strip-group" data-group="stage2">
        <a href="tharam-5.html" class="strip-item strip-has-sub" data-tooltip="2. இளம் பருவம் (5-8)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></span>
          <span class="strip-item-label">2. இளம் பருவம் (5–8)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color: #34d399;">இளம் பருவம் • திருமுறைகள் &amp; பண்பாடு</div>
          <a href="tharam-5.html" class="strip-sub-item"><span class="strip-sub-icon">5️⃣</span><span>தரம் 5 (Grade 5) • 7 நூல்கள்</span></a>
          <a href="tharam-6.html" class="strip-sub-item"><span class="strip-sub-icon">6️⃣</span><span>தரம் 6 (Grade 6) • 7 நூல்கள்</span></a>
          <a href="tharam-7.html" class="strip-sub-item"><span class="strip-sub-icon">7️⃣</span><span>தரம் 7 (Grade 7) • 7 நூல்கள்</span></a>
          <a href="tharam-8.html" class="strip-sub-item"><span class="strip-sub-icon">8️⃣</span><span>தரம் 8 (Grade 8) • 7 நூல்கள்</span></a>
        </div>
      </div>

      <!-- 4. பருவம் 3: உயர்நிலைப் பருவம் (Secondary: Grades 9 - 10) -->
      <div class="strip-group" data-group="stage3">
        <a href="tharam-9.html" class="strip-item strip-has-sub" data-tooltip="3. உயர்நிலைப் பருவம் (9-10)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H4a2 2 0 0 0-2 2v13a3 3 0 0 0 3 3h13a3 3 0 0 0 3-3V5a2 2 0 0 0-2-2h-7"/><path d="M19 18a3 3 0 0 0 0-6H6a2 2 0 0 0 0 4h12"/><line x1="8" y1="7" x2="14" y2="7"/></svg></span>
          <span class="strip-item-label">3. உயர்நிலைப் பருவம் (9–10)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color: #facc15;">உயர்நிலைப் பருவம் • அறநெறி &amp; ஆகமங்கள்</div>
          <a href="tharam-9.html" class="strip-sub-item"><span class="strip-sub-icon">9️⃣</span><span>தரம் 9 (Grade 9) • 7 நூல்கள்</span></a>
          <a href="tharam-10.html" class="strip-sub-item"><span class="strip-sub-icon">🔟</span><span>தரம் 10 (Grade 10) • 7 நூல்கள்</span></a>
        </div>
      </div>

      <!-- 5. பருவம் 4: மேல்நிலைப் பருவம் (Senior Secondary: Grades 11 - 12 • பள்ளி இறுதி) -->
      <div class="strip-group" data-group="stage4">
        <a href="tharam-11.html" class="strip-item strip-has-sub" data-tooltip="4. மேல்நிலைப் பருவம் (11-12)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l9 4.9V17L12 22 3 17V6.9L12 2z"/><path d="M12 22V12"/></svg></span>
          <span class="strip-item-label">4. மேல்நிலைப் பருவம் (11–12)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color: #fb923c;">மேல்நிலை • கீதை &amp; பள்ளி இறுதி</div>
          <a href="tharam-11.html" class="strip-sub-item"><span class="strip-sub-icon">1️⃣1️⃣</span><span>தரம் 11 (Grade 11) • 7 நூல்கள்</span></a>
          <a href="tharam-12.html" class="strip-sub-item"><span class="strip-sub-icon">1️⃣2️⃣</span><span>தரம் 12 (Grade 12) • 7 நூல்கள்</span></a>
        </div>
      </div>

      <!-- 6. பருவம் 5: உயர்கல்வி வித்யாபீடம் (Collegiate & Higher Studies: BA, MA, Ph.D. • வயது 18+) -->
      <div class="strip-group" data-group="higher_studies">
        <a href="higher-studies.html" class="strip-item strip-has-sub" data-tooltip="5. உயர்கல்வி (BA, MA, PhD)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="2" fill="currentColor"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(30 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(-30 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(90 12 12)"/></svg></span>
          <span class="strip-item-label">5. உயர்கல்வி (BA, MA, PhD)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color: #ffd700;">பட்டப் படிப்புகள் &amp; உயர் ஆய்வு</div>
          <a href="higher-studies.html#tierUG" class="strip-sub-item"><span class="strip-sub-icon">🎓</span><span>1. இளங்கலை (B.A. / B.Sc. • 3 Yrs)</span></a>
          <a href="higher-studies.html#tierPG" class="strip-sub-item"><span class="strip-sub-icon">📜</span><span>2. முதுகலை (M.A. / Acharya • 2 Yrs)</span></a>
          <a href="higher-studies.html#tierPhD" class="strip-sub-item"><span class="strip-sub-icon">⚛️</span><span>3. முனைவர் ஆய்வு (Ph.D. / Doctoral)</span></a>
          <a href="higher-studies.html#tierFel" class="strip-sub-item"><span class="strip-sub-icon">🏛️</span><span>4. உயர் பட்டயங்கள் (Fellowships)</span></a>
        </div>
      </div>

      <!-- 7. 7 ஆசிரமப் பாடநூல்கள் அலமாரி (The 7 Ashram Books Shelf) -->
      <div class="strip-group" data-group="books">
        <a href="books.html" class="strip-item strip-has-sub" data-tooltip="7 ஆசிரமப் பாடநூல்கள்">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></span>
          <span class="strip-item-label">7 ஆசிரமப் பாடநூல்கள்</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header">7 ஆசிரமப் பாடநூல்கள் அலமாரி</div>
          <a href="books.html?book=nanneri" class="strip-sub-item"><span class="strip-sub-icon">📜</span><span>1. நன்னெறி (Nanneri)</span></a>
          <a href="books.html?book=nallaram" class="strip-sub-item"><span class="strip-sub-icon">🌿</span><span>2. நல்லறம் (Nallaram)</span></a>
          <a href="books.html?book=nalvazhi" class="strip-sub-item"><span class="strip-sub-icon">⭐</span><span>3. நல்வழி (Nalvazhi)</span></a>
          <a href="books.html?book=narthunai" class="strip-sub-item"><span class="strip-sub-icon">🪔</span><span>4. நற்துணை (Narthunai)</span></a>
          <a href="books.html?book=narchinthanai" class="strip-sub-item"><span class="strip-sub-icon">⚛️</span><span>5. நற்சிந்தனை (Narchinthanai)</span></a>
          <a href="books.html?book=narchol" class="strip-sub-item"><span class="strip-sub-icon">🌸</span><span>6. நற்சொல் (Narchol)</span></a>
          <a href="books.html?book=narcheyal" class="strip-sub-item"><span class="strip-sub-icon">☀️</span><span>7. நற்செயல் (Narcheyal)</span></a>
      </div>

      <!-- 8. வித்யா குடீரம் பள்ளி போர்டல் (Vidya Kudiram Online School) -->
      <div class="strip-group" data-group="school">
        <a href="school.html" class="strip-item" data-tooltip="வித்யா குடீரம் பள்ளி போர்டல்">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 2 3 3 6 3s6-1 6-3v-5"/></svg></span>
          <span class="strip-item-label">வித்யா குடீரம் பள்ளி போர்டல்</span>
        </a>
      </div>

    </nav>

    <div class="strip-footer-dock">
      <button type="button" class="strip-dock-btn" onclick="openUserSettingsModal('preferences')" title="அமைப்புகள்" data-tooltip="அமைப்புகள்">
        <span class="strip-dock-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/></svg></span>
        <span class="strip-dock-label">அமைப்புகள்</span>
      </button>
      <button type="button" class="strip-dock-btn profile-dock-btn" onclick="openUserSettingsModal('profile')" title="சுயவிவரம்" data-tooltip="சுயவிவரம்">
        <span class="strip-dock-avatar" id="stripAvatarIcon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span>
        <span class="strip-dock-label" id="stripUserName">மாணவர்</span>
      </button>
    </div>
  </aside>

  <div class="strip-backdrop" id="stripBackdrop" onclick="closePrimaryMenu()"></div>"""

def apply_strip_bar_everywhere():
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
            new_content = pattern.sub(PURE_CURRICULUM_STRIP_BAR, content)
        elif fallback_pattern.search(content):
            new_content = fallback_pattern.sub(PURE_CURRICULUM_STRIP_BAR, content)
        else:
            continue

        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f"Applied pure curriculum navigation in {fname}")

    print(f"Total HTML files updated: {count}")

if __name__ == '__main__':
    apply_strip_bar_everywhere()
