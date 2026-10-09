import re, os

ROOT = r"c:\GitHub\Gurukuladesam"

for i in range(1, 13):
    fname = f"tharam-{i}.html"
    fpath = os.path.join(ROOT, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    adm_btn = f'<a href="admissions.html?grade={i}" class="sheet-btn" style="background: rgba(245, 158, 11, 0.22) !important; color: #fbbf24 !important; border: 1px solid rgba(245, 158, 11, 0.5) !important; font-size:0.8rem; padding:6px 12px; text-decoration:none; font-weight:700;">🎒 சேர்க்கை (Enroll) &rarr;</a>\n          '

    if "admissions.html?grade=" not in content:
        new_content = re.sub(
            r'(<div style="display:flex; align-items:center; gap:8px;">\s*)(<a href="school\.html")',
            r'\1' + adm_btn + r'\2',
            content
        )
        if new_content != content:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Added admission button in {fname}")
        else:
            print(f"Could not match switcher strip in {fname}")
    else:
        print(f"Already present in {fname}")

