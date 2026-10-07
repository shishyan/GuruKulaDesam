#!/usr/bin/env python3
"""
tools/maintenance/modernize_all_icons_and_symbols.py
Systematically modernizes all UI icons and removes leftover unicode symbols:
1. Strips all \ufe0f emoji variation selectors.
2. Removes/replaces literal down arrows \u2193 in buttons and badges.
3. Replaces raw circle bullets \u25cb in LMS completion buttons with <span class="gkd-status-circle"></span>.
4. Modernizes palm leaf hole markers in style.css from \u25ce to pure CSS circle styling.
5. Replaces decorative/watermark \u0950 in UI tags, seals, logos, and CSS pseudoelements with crisp vector SVG Om icons.
6. Fixes review_quality.html href="#download" anchor to a valid semantic button.
"""

import os
import sys
import glob
import re

OM_SVG_INLINE = (
    '<svg class="gkd-icon gkd-om-icon" viewBox="0 0 24 24" fill="currentColor" '
    'style="width:16px;height:16px;margin-right:6px;vertical-align:middle;">'
    '<circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.8"/>'
    '<path d="M8.2 10.5c-.3-.7-.2-1.5.3-2.1.8-.9 2.2-.9 3 .1.4.5.5 1.2.2 1.8-.4.7-1.1 1.2-1.7 1.7.9.3 '
    '1.7.9 2 1.7.4 1.1 0 2.4-1 3.1-1.2.9-2.9.7-3.9-.4-.4-.5-.6-1.1-.6-1.7h1.4c0 .4.2.8.5 1 .6.5 1.5.4 2-.1'
    '.4-.4.5-1 .2-1.5-.4-.7-1.2-1-2-1v-1.2c.6 0 1.2-.2 1.5-.7.3-.4.3-.9 0-1.3-.4-.5-1.1-.6-1.6-.2-.3.2-.5.6'
    '-.5 1H8.2zm6.3-2.5c.8 0 1.5.5 1.8 1.2l-1.2.5c-.2-.4-.5-.6-.8-.6-.6 0-1 .4-1 1s.4 1 1 1c.5 0 .9-.3 1.1-.7'
    'l1.1.6c-.4.8-1.2 1.3-2.2 1.3-1.4 0-2.4-1-2.4-2.4 0-1.3 1-2.4 2.4-2.4zm1.5-1.5c.3 0 .5.2.5.5s-.2.5-.5.5'
    '-.5-.2-.5-.5.2-.5.5-.5z"/></svg>'
)

OM_SVG_LARGE = (
    '<svg class="gkd-icon gkd-om-icon" viewBox="0 0 24 24" fill="currentColor" '
    'style="width:24px;height:24px;vertical-align:middle;">'
    '<circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.8"/>'
    '<path d="M8.2 10.5c-.3-.7-.2-1.5.3-2.1.8-.9 2.2-.9 3 .1.4.5.5 1.2.2 1.8-.4.7-1.1 1.2-1.7 1.7.9.3 '
    '1.7.9 2 1.7.4 1.1 0 2.4-1 3.1-1.2.9-2.9.7-3.9-.4-.4-.5-.6-1.1-.6-1.7h1.4c0 .4.2.8.5 1 .6.5 1.5.4 2-.1'
    '.4-.4.5-1 .2-1.5-.4-.7-1.2-1-2-1v-1.2c.6 0 1.2-.2 1.5-.7.3-.4.3-.9 0-1.3-.4-.5-1.1-.6-1.6-.2-.3.2-.5.6'
    '-.5 1H8.2zm6.3-2.5c.8 0 1.5.5 1.8 1.2l-1.2.5c-.2-.4-.5-.6-.8-.6-.6 0-1 .4-1 1s.4 1 1 1c.5 0 .9-.3 1.1-.7'
    'l1.1.6c-.4.8-1.2 1.3-2.2 1.3-1.4 0-2.4-1-2.4-2.4 0-1.3 1-2.4 2.4-2.4zm1.5-1.5c.3 0 .5.2.5.5s-.2.5-.5.5'
    '-.5-.2-.5-.5.2-.5.5-.5z"/></svg>'
)

def modernize_docs():
    # File is in tools/maintenance/, so dirname 3 times reaches repo root
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    docs_dir = os.path.join(repo_root, 'docs')
    updated_files = 0

    # 1. Update style.css
    css_path = os.path.join(docs_dir, 'assets', 'css', 'style.css')
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            css_text = f.read()
        
        orig_css = css_text
        # Replace content: "◎"; with pure CSS styling
        css_text = re.sub(
            r'content:\s*["\']◎["\'];',
            'content: ""; width: 12px; height: 12px; border: 2px solid #b45309; border-radius: 50%; display: inline-block;',
            css_text
        )
        if css_text != orig_css:
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(css_text)
            print(f"Updated {css_path}")
            updated_files += 1

    # 2. Update HTML pages
    html_files = sorted(glob.glob(os.path.join(docs_dir, '*.html')))
    for hf in html_files:
        with open(hf, 'r', encoding='utf-8') as f:
            text = f.read()

        orig = text

        # 1. Strip \ufe0f
        text = text.replace('\ufe0f', '')

        # 2. Down arrows \u2193
        text = text.replace('வரிகள் &amp; பொருள் ↓', 'வரிகள் &amp; பொருள்')
        text = text.replace('12 வகுப்புகள் பாடநூல்கள் காண்க ↓', '12 வகுப்புகள் பாடநூல்கள் காண்க')
        text = text.replace('4 வாழ்வியல் பருவங்கள் ↓', '4 வாழ்வியல் பருவங்கள்')
        text = text.replace('பஞ்ச மகா யக்ஞ சாதனை ↓', 'பஞ்ச மகா யக்ஞ சாதனை')

        # 3. LMS circles \u25cb
        text = re.sub(
            r'<span class="lms-icon" id="([^"]+)">○</span>',
            r'<span class="lms-icon" id="\1"><span class="gkd-status-circle"></span></span>',
            text
        )
        text = text.replace('"○ பாடம் முடிந்தது எனக் குறிக்கவும்"', '"பாடம் முடிந்தது எனக் குறிக்கவும்"')

        # 4. CSS watermarks content: "ॐ";
        text = re.sub(r'content:\s*["\']\u0950["\'];', 'content: "";', text)

        # 5. UI Om usages (excluding <div class="sanskrit">)
        # Handle .sacred-tag
        text = re.sub(r'<div class="sacred-tag">\u0950\s*', f'<div class="sacred-tag">{OM_SVG_INLINE} ', text)
        text = text.replace(' \u0950</div>', '</div>')

        # Handle .sacred-emblem
        text = re.sub(r'<div class="sacred-emblem">\u0950\s*', f'<div class="sacred-emblem">{OM_SVG_LARGE} ', text)
        text = text.replace(' \u0950</div>', '</div>')

        # Handle .charter-corner-emblem
        text = re.sub(r'<span class="charter-corner-emblem([^"]*)">\u0950</span>', rf'<span class="charter-corner-emblem\1">{OM_SVG_LARGE}</span>', text)

        # Handle .footer-logo
        text = re.sub(r'<span class="footer-logo">\u0950</span>', rf'<span class="footer-logo">{OM_SVG_LARGE}</span>', text)

        # Handle .certificate-seal
        text = re.sub(r'<div class="certificate-seal">\u0950</div>', rf'<div class="certificate-seal">{OM_SVG_LARGE}</div>', text)

        # Handle index.html header subtitle and kalvi mantra
        text = text.replace('\u0950 ஸ்ரீ குருகுல ஆசிரமம் • தொன்மையான தபோவனப் போதனை மரபு \u0950', f'{OM_SVG_INLINE} ஸ்ரீ குருகுல ஆசிரமம் • தொன்மையான தபோவனப் போதனை மரபு')
        text = text.replace('ஸ்ரீ குருப்யோ நமஹ \u0950', 'ஸ்ரீ குருப்யோ நமஹ')

        # 6. Specific fix for review_quality.html download button
        if 'review_quality.html' in hf:
            text = text.replace(
                '<a id="downloadBtn" href="#download" onclick="alert(\'பதிவிறக்கக் கோப்பு தயாராகிறது (Preparing high-definition release...)\');" class="btn btn-gold">',
                '<button id="downloadBtn" type="button" onclick="alert(\'பதிவிறக்கக் கோப்பு தயாராகிறது (Preparing high-definition release...)\');" class="btn btn-gold">'
            )
            # Find and match the closing tag for downloadBtn
            text = text.replace(
                '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg> தரவிறக்கம் (Download Full Release)\n            </a>',
                '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg> தரவிறக்கம் (Download Full Release)\n            </button>'
            )

        if text != orig:
            with open(hf, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Updated {os.path.basename(hf)}")
            updated_files += 1

    print(f"\nDone! Modernized {updated_files} files in docs/.")

if __name__ == '__main__':
    modernize_docs()
