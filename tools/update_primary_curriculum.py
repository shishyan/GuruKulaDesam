"""
Update Guru Kula Desam Primary Academy (Grades 1 to 5) to 3 Books
and Left Strip Menu to Stage 1 (Grades 1-5) & Stage 2 (Grades 6-8).
"""

import os
import re
import glob

NEW_STAGES_STRIP = """      <!-- 2. பருவம் 1: பாலப் பருவம் (Primary: Grades 1 - 5) -->
      <div class="strip-group" data-group="stage1">
        <a href="tharam-1.html" class="strip-item strip-has-sub" data-tooltip="1. பாலப் பருவம் (1-5)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3 7h-6l3-7z"/><line x1="12" y1="9" x2="12" y2="22"/></svg></span>
          <span class="strip-item-label">1. பாலப் பருவம் (1–5)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color: #38bdf8;">பாலப் பருவம் • 3 ஆசிரம நூல்கள்</div>
          <a href="tharam-1.html" class="strip-sub-item"><span class="strip-sub-icon">1️⃣</span><span>தரம் 1 (Grade 1) • 3 நூல்கள்</span></a>
          <a href="tharam-2.html" class="strip-sub-item"><span class="strip-sub-icon">2️⃣</span><span>தரம் 2 (Grade 2) • 3 நூல்கள்</span></a>
          <a href="tharam-3.html" class="strip-sub-item"><span class="strip-sub-icon">3️⃣</span><span>தரம் 3 (Grade 3) • 3 நூல்கள்</span></a>
          <a href="tharam-4.html" class="strip-sub-item"><span class="strip-sub-icon">4️⃣</span><span>தரம் 4 (Grade 4) • 3 நூல்கள்</span></a>
          <a href="tharam-5.html" class="strip-sub-item"><span class="strip-sub-icon">5️⃣</span><span>தரம் 5 (Grade 5) • 3 நூல்கள்</span></a>
        </div>
      </div>

      <!-- 3. பருவம் 2: இளம் பருவம் (Middle: Grades 6 - 8) -->
      <div class="strip-group" data-group="stage2">
        <a href="tharam-6.html" class="strip-item strip-has-sub" data-tooltip="2. இளம் பருவம் (6-8)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></span>
          <span class="strip-item-label">2. இளம் பருவம் (6–8)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color: #34d399;">இளம் பருவம் • 7 ஆசிரம நூல்கள்</div>
          <a href="tharam-6.html" class="strip-sub-item"><span class="strip-sub-icon">6️⃣</span><span>தரம் 6 (Grade 6) • 7 நூல்கள்</span></a>
          <a href="tharam-7.html" class="strip-sub-item"><span class="strip-sub-icon">7️⃣</span><span>தரம் 7 (Grade 7) • 7 நூல்கள்</span></a>
          <a href="tharam-8.html" class="strip-sub-item"><span class="strip-sub-icon">8️⃣</span><span>தரம் 8 (Grade 8) • 7 நூல்கள்</span></a>
        </div>
      </div>

"""

def update_left_strip(html_text):
    pattern = r'<!-- 2\. பருவம் 1: பாலப் பருவம்.*?<!-- 4\. பருவம் 3:'
    if re.search(pattern, html_text, re.DOTALL):
        return re.sub(pattern, NEW_STAGES_STRIP + '      <!-- 4. பருவம் 3:', html_text, flags=re.DOTALL)
    return html_text

def update_primary_grade_page(filepath, grade):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update strip
    content = update_left_strip(content)

    # 1. Update Title and Description
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>தரம் {grade} — 3 முதன்மை ஆசிரமப் பாடநூல்கள் (Grade {grade} - Primary 3 Books Curriculum) | Guru Kula Desam</title>',
        content
    )
    content = re.sub(
        r'<meta name="description" content=".*?">',
        f'<meta name="description" content="குரு குல தேசம் தரம் {grade} தொடக்கப் பள்ளிப் பாடத்திட்டம். 3 முதன்மை ஆசிரமப் பாடநூல்கள்: நற்செயல் (விளையாடிப் பயிலல் & 3 Ds), நல்வழி (பெரியோர் பணிவு & வாய்மை), நற்துணை (இறைத் துதி & அச்சமின்மை).">',
        content
    )

    # 2. Update Breadcrumb
    content = re.sub(
        r'<a href="school\.html" class="crumb-link">பாலப் பருவம்.*?</a>',
        '<a href="school.html" class="crumb-link">பாலப் பருவம் (1–5)</a>',
        content
    )
    content = re.sub(
        r'<span class="crumb-current" id="topBarCurrentCrumb">.*?</span>',
        f'<span class="crumb-current" id="topBarCurrentCrumb">தரம் {grade} — 3 முதன்மை ஆசிரமப் பாடநூல்கள்</span>',
        content
    )

    # 3. Update Hero Banner
    content = re.sub(
        r'<span style="background:rgba\(56, 189, 248, 0\.18\); color:#38bdf8;\s+font-size:0\.75rem; font-weight:700; padding:2px 8px; border-radius:6px;">பாலப் பருவம்.*?</span>',
        '<span style="background:rgba(56, 189, 248, 0.18); color:#38bdf8; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:6px;">பாலப் பருவம் (1–5)</span>',
        content
    )
    content = re.sub(
        r'<h1 style="color:#ffffff; font-size:2\.2rem; font-weight:800; margin:0 0 6px 0;">\s*தரம் \d+ — \d+ ஆசிரமப் பாடநூல்கள்\s*</h1>',
        f'<h1 style="color:#ffffff; font-size:2.2rem; font-weight:800; margin:0 0 6px 0;">தரம் {grade} — 3 முதன்மை ஆசிரமப் பாடநூல்கள்</h1>',
        content
    )

    # 4. Update Focus Bar
    content = re.sub(
        r'📖 தரம் \d+ — \d+ ஆசிரமப் பாடநூல்கள் மட்டுமே.*?\)',
        f'📖 தரம் {grade} — 3 முதன்மை ஆசிரமப் பாடநூல்கள் மட்டுமே (Primary 3 Books: நற்செயல், நல்வழி, நற்துணை)',
        content
    )

    # 5. Update Shelf Section Heading
    content = re.sub(
        r'<h3 style="color:#ffffff; font-size:1\.15rem; font-weight:800; margin:0;">\s*\d+ ஆசிரமப் பாடநூல்கள்.*?\s*</h3>',
        '<h3 style="color:#ffffff; font-size:1.15rem; font-weight:800; margin:0;">3 முதன்மை ஆசிரமப் பாடநூல்கள் (Primary 3 Books)</h3>',
        content
    )
    content = re.sub(
        r'<span style="color:#94a3b8; font-size:0\.82rem;">நூலைத் தேர்வு செய்து அதிலுள்ள 7 அத்தியாயங்களை வாசிக்கலாம்</span>',
        '<span style="color:#94a3b8; font-size:0.82rem;">விளையாடிப் பயிலல் & 3 Ds வழியே 3 நூல்கள் • 21 அத்தியாயங்கள்</span>',
        content
    )

    # 6. Update Reader top meta badge
    content = re.sub(
        r'<span class="pat-level-code-pill" id="readerBookBadge">.*?</span>',
        f'<span class="pat-level-code-pill" id="readerBookBadge">தரம் {grade} • பாலப் பருவம் (1–5)</span>',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated primary grade page: {filepath}")

def main():
    # Update all HTML files for left-strip navigation
    html_files = glob.glob('*.html')
    updated_strip_count = 0
    for f in html_files:
        with open(f, 'r', encoding='utf-8') as fh:
            orig = fh.read()
        updated = update_left_strip(orig)
        if updated != orig:
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(updated)
            updated_strip_count += 1
    print(f"Updated left-strip navigation in {updated_strip_count} files.")

    # Update Primary Grade Pages (tharam-1 to tharam-5)
    for g in range(1, 6):
        page = f"tharam-{g}.html"
        if os.path.exists(page):
            update_primary_grade_page(page, g)

if __name__ == '__main__':
    main()
