#!/usr/bin/env python3
"""
tools/curriculum/remove_all_borders.py
Removes all inline border styles from every HTML file in docs/,
preserving border-radius for sleek curved geometry.
"""

import os
import re
import glob

def clean_inline_borders(repo_root):
    docs_dir = os.path.join(repo_root, 'docs')
    total_stripped = 0

    # Pattern matches border, border-top, border-bottom, border-left, border-right, border-color
    # but NOT border-radius or border-collapse
    border_prop_pattern = re.compile(r'(?<![a-zA-Z-])border(?:-(?:top|bottom|left|right|color|style|width|image))?\s*:\s*[^;"]+;?', re.IGNORECASE)

    for hf in sorted(glob.glob(os.path.join(docs_dir, '*.html'))):
        with open(hf, 'r', encoding='utf-8') as f:
            content = f.read()

        def clean_style_attr(match):
            nonlocal total_stripped
            style_content = match.group(1)
            new_style, n = border_prop_pattern.subn('', style_content)
            total_stripped += n
            # Clean any double semicolons or extra spaces
            new_style = re.sub(r';\s*;+', ';', new_style).strip()
            if new_style.endswith(';'):
                new_style = new_style[:-1].strip()
            if not new_style:
                return ''
            return f'style="{new_style}"'

        new_content = re.sub(r'style="([^"]*)"', clean_style_attr, content)

        if new_content != content:
            with open(hf, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[OK] Cleaned inline borders from {os.path.basename(hf)}")

    print(f"\nTotal inline border declarations removed across all HTML files: {total_stripped}")

def ensure_css_borderless(repo_root):
    css_path = os.path.join(repo_root, 'docs', 'assets', 'css', 'style.css')
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()

    universal_override = """
/* UNIVERSAL COMPREHENSIVE BORDER REMOVAL OVERRIDE */
*, *::before, *::after, [style*="border"], [class*="border"] {
  border: none !important;
  border-top: none !important;
  border-bottom: none !important;
  border-left: none !important;
  border-right: none !important;
  border-color: transparent !important;
  outline: none !important;
}
"""
    if "UNIVERSAL COMPREHENSIVE BORDER REMOVAL OVERRIDE" not in content:
        content += universal_override
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("[OK] Appended universal comprehensive border override to style.css")

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    clean_inline_borders(repo_root)
    ensure_css_borderless(repo_root)

if __name__ == '__main__':
    main()
