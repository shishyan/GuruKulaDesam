#!/usr/bin/env python3
"""
tools/test_section_scroll_targets.py
Verifies that all scrollToId('xyz') and scrollToSection('xyz') calls across all pages
have corresponding matching elements with id="xyz".
"""

import os
import sys
import glob
import re

def test_scroll_targets():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(repo_root, 'docs')
    html_files = sorted(glob.glob(os.path.join(docs_dir, '*.html')))

    mismatches = []
    total_calls = 0

    for hf in html_files:
        page_name = os.path.basename(hf)
        with open(hf, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Find all element IDs
        page_ids = set(re.findall(r'id=[\'"]([a-zA-Z0-9_\-]+)[\'"]', content))

        # Find scrollToId('...') and scrollToSection('...')
        scroll_calls = re.findall(r'scrollTo(?:Id|Section)\([\'"]([a-zA-Z0-9_\-]+)[\'"]\)', content)
        for target_id in scroll_calls:
            total_calls += 1
            if target_id not in page_ids:
                mismatches.append((page_name, target_id))

    if mismatches:
        print(f"[FAIL] Found {len(mismatches)} scroll targets without matching ID:")
        for p, tid in mismatches:
            print(f"  - {p}: target ID '{tid}' not found")
        return False
    else:
        print(f"[PASS] All {total_calls} scroll-to-ID targets verified and resolve to valid elements.")
        return True

if __name__ == '__main__':
    if not test_scroll_targets():
        sys.exit(1)
