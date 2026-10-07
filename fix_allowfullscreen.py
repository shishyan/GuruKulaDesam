import os
import re

ROOT = r"c:\GitHub\Gurukuladesam"

def process_file(fp):
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()

    orig = content
    # Replace allowfullscreen on modalIframe or any iframe having allow="..."
    content = re.sub(r'(<iframe[^>]*allow="[^"]*fullscreen[^"]*")\s+allowfullscreen(?:\s*=\s*(?:"[^"]*"|\'[^\']*\'))?', r'\1', content)
    # Also handle if allowfullscreen was before allow
    content = re.sub(r'(<iframe[^>]*)allowfullscreen(?:\s*=\s*(?:"[^"]*"|\'[^\']*\'))?\s+([^>]*allow="[^"]*fullscreen[^"]*")', r'\1\2', content)

    # Ensure referrerpolicy is present
    def ensure_refpolicy(match):
        tag = match.group(0)
        if "referrerpolicy" not in tag:
            tag = tag[:-1].rstrip() + ' referrerpolicy="strict-origin-when-cross-origin">'
        return tag

    content = re.sub(r'<iframe[^>]*id="modalIframe"[^>]*>', ensure_refpolicy, content)

    if content != orig:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

count = 0
for folder in [ROOT, os.path.join(ROOT, "docs"), os.path.join(ROOT, "site")]:
    if not os.path.exists(folder):
        continue
    for root_dir, dirs, files in os.walk(folder):
        for fn in files:
            if fn.endswith(".html") or fn.endswith(".js"):
                fp = os.path.join(root_dir, fn)
                if process_file(fp):
                    count += 1

print(f"Cleaned up allowfullscreen across {count} files.")
