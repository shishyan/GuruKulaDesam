#!/usr/bin/env python3
"""
tools/curriculum/apply_static_header_upgrade.py
Upgrades all HTML files in docs/:
1. Replaces top-bar pills with Back Button + Breadcrumbs in #contextTopBar
2. Places dedicated tabs container inside the page hero/header content
"""

import os
import re
import glob

BREADCRUMBS_MAP = {
    'index.html': [('ஆசிரம முகப்பு', 'index.html')],
    'kalvi.html': [('முகப்பு', 'index.html'), ('வாழ்வியல் மையம் (12 நிலைகள்)', 'kalvi.html')],
    'school.html': [('முகப்பு', 'index.html'), ('கல்வி', 'kalvi.html'), ('இணையப் பள்ளி போர்டல்', 'school.html')],
    'higher-studies.html': [('முகப்பு', 'index.html'), ('கல்வி', 'kalvi.html'), ('வேதாந்த உயர்கல்வி', 'higher-studies.html')],
    'virtues.html': [('முகப்பு', 'index.html'), ('வாழ்வியல்', 'kalvi.html'), ('அகர வரிசை நற்பண்புகள்', 'virtues.html')],
    'syllabus.html': [('முகப்பு', 'index.html'), ('கல்வி', 'kalvi.html'), ('சைவ சித்தாந்த பாடத்திட்டம்', 'syllabus.html')],
    'classes.html': [('முகப்பு', 'index.html'), ('கல்வி', 'kalvi.html'), ('வகுப்புகள் & அட்டவணை', 'classes.html')],
    'saiva-neri.html': [('முகப்பு', 'index.html'), ('சைவ நெறி (172 திருப்பதிகங்கள்)', 'saiva-neri.html')],
    'murugan.html': [('முகப்பு', 'index.html'), ('வழிபாட்டு நெறி', 'saiva-neri.html'), ('முருகப் பெருமான்', 'murugan.html')],
    'sakthi.html': [('முகப்பு', 'index.html'), ('வழிபாட்டு நெறி', 'saiva-neri.html'), ('சக்தி நெறி', 'sakthi.html')],
    'vinayagar.html': [('முகப்பு', 'index.html'), ('வழிபாட்டு நெறி', 'saiva-neri.html'), ('விநாயகர் பெருமான்', 'vinayagar.html')],
    'vaishnava.html': [('முகப்பு', 'index.html'), ('வழிபாட்டு நெறி', 'saiva-neri.html'), ('வைணவ நெறி', 'vaishnava.html')],
    'thirukkural.html': [('முகப்பு', 'index.html'), ('தமிழ்மறை திருக்குறள் (185)', 'thirukkural.html')],
    'review_quality.html': [('முகப்பு', 'index.html'), ('திருக்குறள்', 'thirukkural.html'), ('திரைத் தர ஆய்வு அரங்கம்', 'review_quality.html')],
    'sanmargam.html': [('முகப்பு', 'index.html'), ('வள்ளலார் சுத்த சன்மார்க்கம்', 'sanmargam.html')],
    'irai-isai-virundhu.html': [('முகப்பு', 'index.html'), ('இறை இசை விருந்து', 'irai-isai-virundhu.html')],
    'youtube.html': [('முகப்பு', 'index.html'), ('YouTube காணொளி அரங்கம் (580)', 'youtube.html')],
    'about.html': [('முகப்பு', 'index.html'), ('காஞ்சி மகா பெரியவா', 'about.html')],
    'help.html': [('முகப்பு', 'index.html'), ('உதவி & வழிகாட்டல் மையம்', 'help.html')],
    'google-site.html': [('முகப்பு', 'index.html'), ('கூகிள் தளம் நேரடி இணைப்பு', 'google-site.html')]
}

BACK_BTN_HTML = """      <button type="button" class="header-back-btn" onclick="handleUniversalBack()" title="பின்னே செல்ல (Go Back)" aria-label="பின்னே">
        <span class="back-btn-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg></span>
        <span class="back-btn-text">பின்னே</span>
      </button>"""

def get_breadcrumbs(filename):
    if filename in BREADCRUMBS_MAP:
        return BREADCRUMBS_MAP[filename]
    m = re.match(r'tharam-(\d+)\.html', filename)
    if m:
        num = m.group(1)
        return [('முகப்பு', 'index.html'), ('வாழ்வியல் நெறி', 'kalvi.html'), (f'தரம் {num}', filename)]
    return [('முகப்பு', 'index.html'), ('பக்கம்', filename)]

def build_breadcrumbs_html(crumbs):
    parts = []
    for idx, (label, href) in enumerate(crumbs):
        if idx == len(crumbs) - 1:
            parts.append(f'<span class="crumb-current">{label}</span>')
        else:
            parts.append(f'<a href="{href}" class="crumb-link">{label}</a><span class="crumb-sep">/</span>')
    return f"""      <nav class="header-breadcrumbs" aria-label="தள வழிசெலுத்தல் (Breadcrumbs)">
        {' '.join(parts)}
      </nav>"""

def upgrade_file(filepath):
    filename = os.path.basename(filepath)
    if filename.startswith('embed_'):
        return False
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the top bar: <header class="context-top-bar" id="contextTopBar"> ... </header>
    topbar_match = re.search(r'(<header class="context-top-bar"[^>]*>.*?</header>)', content, re.DOTALL)
    if not topbar_match:
        return False

    topbar_html = topbar_match.group(1)
    
    # Check if back button already present in topbar
    if 'class="header-back-btn"' in topbar_html:
        print(f"[SKIP] Header already upgraded in {filename}")
        return False

    crumbs = get_breadcrumbs(filename)
    breadcrumbs_html = build_breadcrumbs_html(crumbs)

    # Extract tabs from <nav class="context-tabs-nav"...>...</nav>
    tabs_match = re.search(r'<nav class="context-tabs-nav"[^>]*>(.*?)</nav>', topbar_html, re.DOTALL)
    tabs_inner = tabs_match.group(1) if tabs_match else ''
    
    # Convert tabs_inner to dedicated tabs format
    dedicated_tabs_html = ""
    if tabs_inner.strip():
        # Replace context-tab-pill with dedicated-tab-pill
        pills_html = tabs_inner.replace('context-tab-pill', 'dedicated-tab-pill')
        dedicated_tabs_html = f"""
    <!-- Dedicated Page Section Tabs (Relevant to this page) -->
    <div class="dedicated-page-tabs-container">
      <div class="dedicated-tabs-label">
        <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h7"/></svg>
        <span>பிரிவுகள் &amp; நேரடிச் சுவடிகள் (Sections &amp; Quick Access):</span>
      </div>
      <nav class="dedicated-page-tabs-bar" aria-label="பக்கத்தின் பிரிவுகள்">
{pills_html}
      </nav>
    </div>
"""

    # In topbar_html: replace the <nav class="context-tabs-nav"...>...</nav> with Back button + Breadcrumbs
    if tabs_match:
        new_topbar_nav = f"{BACK_BTN_HTML}\n{breadcrumbs_html}"
        new_topbar = topbar_html[:tabs_match.start()] + new_topbar_nav + topbar_html[tabs_match.end():]
    else:
        # If no tabs nav, inject after hamburger
        hb_match = re.search(r'</button>', topbar_html)
        if hb_match:
            insert_pos = hb_match.end()
            new_topbar = topbar_html[:insert_pos] + "\n" + BACK_BTN_HTML + "\n" + breadcrumbs_html + topbar_html[insert_pos:]
        else:
            new_topbar = topbar_html

    # Replace topbar in content
    new_content = content[:topbar_match.start()] + new_topbar + content[topbar_match.end():]

    # Now inject dedicated_tabs_html into the page hero banner or main
    if dedicated_tabs_html and 'class="dedicated-page-tabs-container"' not in new_content:
        # Try finding hero banner closing tag
        hero_match = re.search(r'(<div class="hero-banner"[^>]*>.*?</div>)', new_content, re.DOTALL)
        if hero_match:
            insert_pos = hero_match.end()
            new_content = new_content[:insert_pos] + dedicated_tabs_html + new_content[insert_pos:]
        else:
            # Try ashram hero artwork, vidya hero, or main
            alt_hero_match = re.search(r'(<div class="(?:ashram-hero-artwork|vidya-hero-art|grade-lms-tracker-banner)"[^>]*>.*?</div>)', new_content, re.DOTALL)
            if alt_hero_match:
                insert_pos = alt_hero_match.end()
                new_content = new_content[:insert_pos] + dedicated_tabs_html + new_content[insert_pos:]
            else:
                main_match = re.search(r'(<main[^>]*>)', new_content)
                if main_match:
                    insert_pos = main_match.end()
                    new_content = new_content[:insert_pos] + dedicated_tabs_html + new_content[insert_pos:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] Upgraded static header & dedicated tabs in {filename}")
    return True

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    docs_dir = os.path.join(repo_root, 'docs')
    count = 0
    for hf in sorted(glob.glob(os.path.join(docs_dir, '*.html'))):
        if upgrade_file(hf):
            count += 1
    print(f"\nCompleted! Upgraded {count} HTML files in docs/.")

if __name__ == '__main__':
    main()
