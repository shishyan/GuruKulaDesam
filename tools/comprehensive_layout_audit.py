import os
import re

files = [f for f in os.listdir('.') if f.endswith('.html') and not f.startswith('scraped_') and not f.startswith('embed_')]

print("=== CHECKING ALL HTML PAGES FOR UNBALANCED TAGS OR NESTED CARDS ===")

for fname in sorted(files):
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check overall div balance
    opens = len(re.findall(r'<div[\s>]', content))
    closes = len(re.findall(r'</div>', content))
    if opens != closes:
        print(f"PAGE DIV MISMATCH: {fname} (opens={opens}, closes={closes}, diff={opens-closes})")

    # Check main tag balance
    m_open = len(re.findall(r'<main[\s>]', content))
    m_close = len(re.findall(r'</main>', content))
    if m_open != m_close:
        print(f"PAGE MAIN MISMATCH: {fname} (opens={m_open}, closes={m_close})")

    # Check section tag balance
    s_open = len(re.findall(r'<section[\s>]', content))
    s_close = len(re.findall(r'</section>', content))
    if s_open != s_close:
        print(f"PAGE SECTION MISMATCH: {fname} (opens={s_open}, closes={s_close})")

    # Check header tag balance
    h_open = len(re.findall(r'<header[\s>]', content))
    h_close = len(re.findall(r'</header>', content))
    if h_open != h_close:
        print(f"PAGE HEADER MISMATCH: {fname} (opens={h_open}, closes={h_close})")

print("\n=== CHECKING FOR IFRAMES / VIDEO CONTAINERS ACROSS ALL PAGES ===")
for fname in sorted(files):
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if '<iframe' in content:
        # find each iframe and its immediate parent
        for m in re.finditer(r'(<div[^>]*class="([^"]*)"[^>]*>[\s\S]{0,200}<iframe[\s\S]{0,300}</iframe>[\s\S]{0,100}</div>)', content):
            print(f"{fname}: iframe with class '{m.group(2)}'")
