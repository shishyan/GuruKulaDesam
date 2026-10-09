import os, re, glob

ROOT = r"c:\GitHub\Gurukuladesam"

STANDARD_GEAR_PATH = 'M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z'

OLD_GEAR_PATTERN = re.compile(r'M19\.4 15a1\.65 1\.65[\s\S]*?1\.51 1z', re.DOTALL)

def fix_gear_icon_in_all_files():
    count = 0
    all_files = glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'assets/js/*.js')) + glob.glob(os.path.join(ROOT, 'tools/*.py'))
    for fpath in all_files:
        if 'scrub_grade_pages.py' in fpath:
            continue
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        if OLD_GEAR_PATTERN.search(content):
            new_content = OLD_GEAR_PATTERN.sub(STANDARD_GEAR_PATH, content)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f"Fixed gear icon in {os.path.basename(fpath)}")
    print(f"Total files updated with standard gear icon: {count}")

def scrub_grade_pages_zero_wrapper():
    target_files = ['books.html'] + [f"tharam-{i}.html" for i in range(1, 13)]
    for fname in target_files:
        fpath = os.path.join(ROOT, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            text = f.read()

        # Remove background & border from bottom jump grid
        text = re.sub(
            r'style="margin-top:35px;\s*padding:20px;\s*background:rgba\(11,18,33,0\.85\);\s*border:1px solid rgba\(255,255,255,0\.08\);\s*border-radius:16px;"',
            'style="margin-top:35px; padding:16px 0; background:transparent !important; border:none !important;"',
            text
        )

        # Remove border from banyan hero thumb
        text = re.sub(
            r'border:1\.5px solid rgba\(212,175,55,0\.35\);',
            'border:none !important;',
            text
        )

        # Remove border:1px solid from header tags
        text = re.sub(
            r'border:1px solid rgba\(56, 189, 248, 0\.35\);',
            '',
            text
        )

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Scrubbed wrappers & borders in {fname}")

if __name__ == '__main__':
    fix_gear_icon_in_all_files()
    scrub_grade_pages_zero_wrapper()
