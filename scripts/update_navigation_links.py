#!/usr/bin/env python3
"""
scripts/update_navigation_links.py
Ensures moola-nool.html is present in navigation menus across key pages:
index.html, kalvi.html, higher-studies.html, syllabus.html
"""

import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

MOOLA_SUB_ITEM = (
    '          <a href="moola-nool.html" class="strip-sub-item">'
    '<span class="strip-sub-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></span>'
    '<span>மூல நூல் களஞ்சியம்</span></a>\n'
)

pages = ['index.html', 'kalvi.html', 'higher-studies.html', 'syllabus.html']

for page in pages:
    path = os.path.join(REPO_ROOT, page)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    if 'href="moola-nool.html"' in c:
        print(f"moola-nool.html already in {page}")
        continue
        
    # Insert after higher-studies.html or syllabus.html
    target = 'href="higher-studies.html"'
    if target in c:
        # Find the </a> ending that item
        idx = c.find(target)
        end_a = c.find('</a>', idx) + 4
        c = c[:end_a] + '\n' + MOOLA_SUB_ITEM + c[end_a:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Added moola-nool.html to {page}")
    else:
        print(f"Could not find target in {page}")

