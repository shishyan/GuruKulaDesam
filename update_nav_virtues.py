import os
import glob
import re

new_nav_item = """            <a href="virtues.html" class="dropdown-item" style="grid-column: 1 / -1; border-bottom: 1px solid var(--border-subtle); margin-bottom: 4px;">
              <span class="dropdown-item-icon">🔤</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">அகர வரிசை நற்பண்பு நெறி (Virtues Mapping)</div>
                <div class="dropdown-item-desc">தமிழ் எழுத்து முதல் தர்மம் வரை — 12 தரங்களின் நற்பண்பு வளர்ச்சி</div>
              </div>
            </a>"""

def update_nav(filepath):
    if not os.path.exists(filepath):
        return False
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'href="virtues.html"' in content:
        return False

    target = '<div class="dropdown-item-desc">தரம் 1 முதல் 12 வரையிலான முழுமையான பாடநெறி</div>\n              </div>\n            </a>'
    if target in content:
        content = content.replace(target, target + '\n' + new_nav_item)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

count = 0
for root_dir in ['.', 'docs', 'site']:
    for f in glob.glob(os.path.join(root_dir, '*.html')):
        if update_nav(f):
            count += 1

print(f"Updated navigation with Virtues Mapping link in {count} HTML files.")
