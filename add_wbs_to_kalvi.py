# -*- coding: utf-8 -*-
"""
Add WBS codes to Grade Cards and Virtue Table in kalvi.html
"""
import re

for path in ['kalvi.html', 'site/kalvi.html', 'docs/kalvi.html']:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Grade Cards with WBS G01 to WBS G12
    for g in range(1, 13):
        wbs_str = f"WBS G{g:02d}"
        target_needle = f'href="tharam-{g}.html" class="grade-card">'
        if target_needle in html and wbs_str not in html:
            # Add WBS badge in the badge row
            badge_target = f'href="tharam-{g}.html" class="grade-card">\n          <div>\n            <div class="grade-card-badge-row"'
            replacement = f'href="tharam-{g}.html" class="grade-card">\n          <div>\n            <div class="grade-card-badge-row" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">\n              <span class="wbs-code wbs-code-primary">{wbs_str}</span>'
            html = html.replace(badge_target, replacement)

    # 2. Update Table rows in virtue table with WBS codes
    for g in range(1, 13):
        old_td = f'<a href="tharam-{g}.html" style="color: var(--gold-bright); text-decoration: none;">தரம் {g}'
        new_td = f'<a href="tharam-{g}.html" style="color: var(--gold-bright); text-decoration: none;"><span class="wbs-code">G{g:02d}</span> தரம் {g}'
        if old_td in html and f'G{g:02d}' not in html:
            html = html.replace(old_td, new_td)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Updated WBS in {path}")
