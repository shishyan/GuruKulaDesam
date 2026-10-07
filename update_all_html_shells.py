import os
import re
import shutil

ROOT_DIR = r"c:\GitHub\Gurukuladesam"
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
SITE_DIR = os.path.join(ROOT_DIR, "site")

HTML_FILES = [f for f in os.listdir(ROOT_DIR) if f.endswith('.html')]

NEW_TOGGLE_BTN = """<button type="button" class="strip-toggle-btn" id="stripToggleBtn" onclick="closePrimaryMenu()" title="பட்டி மூடுக" aria-label="Close Primary Menu">
        <span class="strip-toggle-icon">✕</span>
      </button>"""

NEW_HAMBURGER_BTN = """<button type="button" class="primary-hamburger-btn" onclick="togglePrimaryMenu()" title="முதன்மை பட்டி (6 பிரிவுகள்)" aria-label="முதன்மை பட்டி">
        <span class="hb-icon">☰</span>
        <span class="hb-emblem">ॐ</span>
        <span class="hb-label">முதன்மை பட்டி</span>
      </button>"""

count = 0
for filename in HTML_FILES:
    filepath = os.path.join(ROOT_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content

    # 1. Replace strip-toggle-btn
    content = re.sub(
        r'<button[^>]*class="strip-toggle-btn"[^>]*>[\s\S]*?</button>',
        NEW_TOGGLE_BTN,
        content
    )

    # 2. Replace backdrop onclick
    content = content.replace('onclick="closeMobileStrip()"', 'onclick="closePrimaryMenu()"')

    # 3. Replace context-mobile-btn with primary-hamburger-btn
    content = re.sub(
        r'<button[^>]*class="context-mobile-btn"[^>]*>[\s\S]*?</button>',
        NEW_HAMBURGER_BTN,
        content
    )

    # 4. Check if dedicated-sub-sidebar is needed for tharam pages
    if filename.startswith('tharam-') and 'class="course-sidebar"' in content:
        content = content.replace('class="course-sidebar"', 'class="course-sidebar dedicated-sub-sidebar"')

    if content != orig:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Sync to docs and site
        docs_path = os.path.join(DOCS_DIR, filename)
        if os.path.exists(DOCS_DIR):
            with open(docs_path, 'w', encoding='utf-8') as f:
                f.write(content)

        site_path = os.path.join(SITE_DIR, filename)
        if os.path.exists(SITE_DIR):
            with open(site_path, 'w', encoding='utf-8') as f:
                f.write(content)

        count += 1
        print(f"Updated {filename}")

print(f"\nSuccessfully updated and synchronized {count} HTML pages across root, docs/, and site/.")
