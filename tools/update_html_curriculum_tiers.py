import os
import glob
import re

ROOT = r'c:\GitHub\Gurukuladesam'

def update_left_strip(content):
    # Old stage 1 to stage 4 navigation pattern
    # Find from <!-- 2. பருவம் 1: பாலப் பருவம் up to <!-- 6. பருவம் 5: உயர்கல்வி வித்யாபீடம்
    pattern = r'<!-- 2\. பருவம் 1: பாலப் பருவம்[\s\S]*?<!-- 6\. பருவம் 5: உயர்கல்வி வித்யாபீடம்'
    replacement = '''<!-- 2. பருவம் 1: பாலப் பருவம் (Primary: Grades 1 - 4 • அற அடித்தளம் & நற்பண்பு) -->
      <div class="strip-group" data-group="stage1">
        <a href="tharam-1.html" class="strip-item strip-has-sub" data-tooltip="1. பாலப் பருவம் (1–4)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3 7h-6l3-7z"/><line x1="12" y1="9" x2="12" y2="22"/></svg></span>
          <span class="strip-item-label">1. பாலப் பருவம் (1–4)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color: #38bdf8;">பாலப் பருவம் • தொடக்கக் கல்வி</div>
          <a href="tharam-1.html" class="strip-sub-item"><span class="strip-sub-icon">1️⃣</span><span>தரம் 1 (Grade 1) • 1 நூல் (நற்செயல்)</span></a>
          <a href="tharam-2.html" class="strip-sub-item"><span class="strip-sub-icon">2️⃣</span><span>தரம் 2 (Grade 2) • 1 நூல் (நற்செயல்)</span></a>
          <a href="tharam-3.html" class="strip-sub-item"><span class="strip-sub-icon">3️⃣</span><span>தரம் 3 (Grade 3) • 2 நூல்கள் (நற்செயல், நற்பண்பு)</span></a>
          <a href="tharam-4.html" class="strip-sub-item"><span class="strip-sub-icon">4️⃣</span><span>தரம் 4 (Grade 4) • 2 நூல்கள் (நற்செயல், நற்பண்பு)</span></a>
        </div>
      </div>

      <!-- 3. பருவம் 2: இளம் பருவம் (Middle: Grades 5 - 8 • 5 நூல்கள்) -->
      <div class="strip-group" data-group="stage2">
        <a href="tharam-5.html" class="strip-item strip-has-sub" data-tooltip="2. இளம் பருவம் (5–8)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></span>
          <span class="strip-item-label">2. இளம் பருவம் (5–8)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color: #34d399;">இளம் பருவம் • 5 ஆசிரம நூல்கள்</div>
          <a href="tharam-5.html" class="strip-sub-item"><span class="strip-sub-icon">5️⃣</span><span>தரம் 5 (Grade 5) • 5 நூல்கள்</span></a>
          <a href="tharam-6.html" class="strip-sub-item"><span class="strip-sub-icon">6️⃣</span><span>தரம் 6 (Grade 6) • 5 நூல்கள்</span></a>
          <a href="tharam-7.html" class="strip-sub-item"><span class="strip-sub-icon">7️⃣</span><span>தரம் 7 (Grade 7) • 5 நூல்கள்</span></a>
          <a href="tharam-8.html" class="strip-sub-item"><span class="strip-sub-icon">8️⃣</span><span>தரம் 8 (Grade 8) • 5 நூல்கள்</span></a>
        </div>
      </div>

      <!-- 4. பருவம் 3: உயர்நிலைப் பருவம் (Secondary: Grades 9 - 10 • 6 நூல்கள்) -->
      <div class="strip-group" data-group="stage3">
        <a href="tharam-9.html" class="strip-item strip-has-sub" data-tooltip="3. உயர்நிலைப் பருவம் (9–10)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H4a2 2 0 0 0-2 2v13a3 3 0 0 0 3 3h13a3 3 0 0 0 3-3V5a2 2 0 0 0-2-2h-7"/><path d="M19 18a3 3 0 0 0 0-6H6a2 2 0 0 0 0 4h12"/><line x1="8" y1="7" x2="14" y2="7"/></svg></span>
          <span class="strip-item-label">3. உயர்நிலைப் பருவம் (9–10)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color: #facc15;">உயர்நிலைப் பருவம் • 6 ஆசிரம நூல்கள்</div>
          <a href="tharam-9.html" class="strip-sub-item"><span class="strip-sub-icon">9️⃣</span><span>தரம் 9 (Grade 9) • 6 நூல்கள்</span></a>
          <a href="tharam-10.html" class="strip-sub-item"><span class="strip-sub-icon">🔟</span><span>தரம் 10 (Grade 10) • 6 நூல்கள்</span></a>
        </div>
      </div>

      <!-- 5. பருவம் 4: மேல்நிலைப் பருவம் (Senior Secondary: Grades 11 - 12 • 6 நூல்கள்) -->
      <div class="strip-group" data-group="stage4">
        <a href="tharam-11.html" class="strip-item strip-has-sub" data-tooltip="4. மேல்நிலைப் பருவம் (11–12)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l9 4.9V17L12 22 3 17V6.9L12 2z"/><path d="M12 22V12"/></svg></span>
          <span class="strip-item-label">4. மேல்நிலைப் பருவம் (11–12)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color: #fb923c;">மேல்நிலை • 6 ஆசிரம நூல்கள்</div>
          <a href="tharam-11.html" class="strip-sub-item"><span class="strip-sub-icon">1️⃣1️⃣</span><span>தரம் 11 (Grade 11) • 6 நூல்கள்</span></a>
          <a href="tharam-12.html" class="strip-sub-item"><span class="strip-sub-icon">1️⃣2️⃣</span><span>தரம் 12 (Grade 12) • 6 நூல்கள்</span></a>
        </div>
      </div>

      <!-- 6. பருவம் 5: உயர்கல்வி வித்யாபீடம்'''

    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content, count=1)
    return content

def replace_nalvazhi_everywhere(content):
    # Replace in left strip shelf: 3. நல்வழி (Nalvazhi) -> 3. நற்பண்பு (Narpanbu)
    content = content.replace('<span>3. நல்வழி (Nalvazhi)</span>', '<span>3. நற்பண்பு (Narpanbu)</span>')
    content = content.replace('3. நல்வழி (Nalvazhi - வாய்மை &amp; நேர்மை)', '3. நற்பண்பு (Narpanbu - வாய்மை &amp; நேர்மை)')
    content = content.replace('3. நல்வழி (Nalvazhi - வாய்மை & நேர்மை)', '3. நற்பண்பு (Narpanbu - வாய்மை & நேர்மை)')
    content = content.replace('3. நல்வழி', '3. நற்பண்பு')
    return content

# Process all html files in root
html_files = glob.glob(os.path.join(ROOT, '*.html'))
for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = update_left_strip(content)
    new_content = replace_nalvazhi_everywhere(new_content)

    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated nav & Nalvazhi in: {os.path.basename(fpath)}")

print("Completed general HTML updates.")
