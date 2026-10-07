import os
import glob
import re

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False

    # 1. Add catalog.js before main.js if missing
    if 'assets/js/main.js' in content and 'assets/data/catalog.js' not in content:
        content = content.replace(
            '<script src="assets/js/main.js"></script>',
            '<script src="assets/data/catalog.js"></script>\n  <script src="assets/js/main.js"></script>'
        )
        changed = True

    # 2. Add modalDetails container inside player-modal-box if missing
    if 'playerModal' in content and 'modalDetails' not in content:
        content = re.sub(
            r'(<div class="modal-footer">[\s\S]*?</div>)',
            r'\1\n      <div class="modal-details" id="modalDetails"></div>',
            content,
            count=1
        )
        changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated: {filepath}')

for root_dir in ['.', 'docs', 'site']:
    for f in glob.glob(os.path.join(root_dir, '*.html')):
        update_file(f)

print('Finished updating all HTML files.')
