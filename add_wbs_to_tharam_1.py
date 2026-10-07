# -*- coding: utf-8 -*-
import re

for path in ['tharam-1.html', 'site/tharam-1.html', 'docs/tharam-1.html']:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Hero banner
    html = html.replace(
        '<div class="sacred-tag">📖 தரம் 1 • ஆரம்பக் கல்வி • 60 பாடப் படங்கள் 📖</div>',
        '<div class="sacred-tag"><span class="wbs-code">WBS G01</span> 📖 தரம் 1 • ஆரம்பக் கல்வி • 60 பாடப் படங்கள் 📖</div>'
    )

    # 2. Sidebar numbers
    html = re.sub(
        r'<div class="sidebar-chapter-group active" id="side-group-sheets">[\s\S]*?<span class="sidebar-num">.*?</span>',
        '<div class="sidebar-chapter-group active" id="side-group-sheets">\n            <a href="#sheets-section" class="sidebar-chapter-btn active" style="text-decoration:none;">\n              <span class="sidebar-chapter-pill">\n                <span class="sidebar-num">1.1</span>',
        html
    )
    html = re.sub(
        r'<div class="sidebar-chapter-group" id="side-group-highlights">[\s\S]*?<span class="sidebar-num">.*?</span>',
        '<div class="sidebar-chapter-group" id="side-group-highlights">\n            <a href="#syllabus-highlights" class="sidebar-chapter-btn" style="text-decoration:none;">\n              <span class="sidebar-chapter-pill">\n                <span class="sidebar-num">1.2</span>',
        html
    )
    html = re.sub(
        r'<div class="sidebar-chapter-group" id="side-group-virtue">[\s\S]*?<span class="sidebar-num">.*?</span>',
        '<div class="sidebar-chapter-group" id="side-group-virtue">\n            <a href="#virtue-section" class="sidebar-chapter-btn" style="text-decoration:none;">\n              <span class="sidebar-chapter-pill">\n                <span class="sidebar-num">1.3</span>',
        html
    )
    html = re.sub(
        r'<div class="sidebar-chapter-group" id="side-group-google">[\s\S]*?<span class="sidebar-num">.*?</span>',
        '<div class="sidebar-chapter-group" id="side-group-google">\n            <a href="https://sites.google.com/view/wwwgurukuladesamcom/home/%E0%AE%9A%E0%AE%B5-%E0%AE%A8%E0%AE%B1/%E0%AE%A4%E0%AE%B0%E0%AE%AE-1" target="_blank" rel="noopener" class="sidebar-chapter-btn" style="text-decoration:none;">\n              <span class="sidebar-chapter-pill">\n                <span class="sidebar-num">1.4</span>',
        html
    )

    # 3. Sheets section header
    html = html.replace(
        '<div id="sheets-section" style="display:flex; justify-content:space-between; align-items:center; margin-top:30px;">',
        '<div id="sheets-section" style="display:flex; justify-content:space-between; align-items:center; margin-top:30px; flex-wrap:wrap; gap:10px;">\n        <div style="display:flex; align-items:center; gap:8px;"><span class="wbs-code wbs-code-primary">WBS 1.1</span> <strong style="color:#f8fafc;">60 பாடநூல் தாள்கள் (Textbook Sheets)</strong></div>'
    )

    # 4. Each sheet card page
    def replace_sheet_hdr(m):
        p_num = m.group(1)
        return f'<div class="sheet-header">\n          <span><span class="wbs-code">WBS 1.1.{p_num}</span> பக்கம் {p_num}</span>'

    html = re.sub(r'<div class="sheet-header">\s*<span>(?:<span class="wbs-code">[^<]+</span>\s*)?பக்கம் (\d+)</span>', replace_sheet_hdr, html)

    # 5. Highlights section
    if 'WBS 1.2' not in html:
        html = html.replace(
            '<div id="syllabus-highlights" class="scripture-study-section" style="margin-top: 20px;">',
            '<div id="syllabus-highlights" class="scripture-study-section" style="margin-top: 20px;">\n        <div style="margin-bottom:8px;"><span class="wbs-code wbs-code-primary">WBS 1.2</span> <span class="source-badge">பாடத்திட்ட உள்ளடக்கச் சுருக்கம்</span></div>'
        )

    # 6. Virtue section
    if 'WBS 1.3' not in html:
        html = html.replace(
            '<h2 style="color: #ffffff; font-size: 1.35rem; margin-bottom: 8px;">\n        எழுத்துகள் ‘அ’ • ‘ஆ’ • ‘இ’ • ‘ஈ’',
            '<div style="margin-bottom:8px;"><span class="wbs-code wbs-code-primary">WBS 1.3</span> <span class="source-badge">அகர வரிசை நற்பண்புகள் &amp; வாழ்வியல் நெறிமுறைகள்</span></div>\n      <h2 style="color: #ffffff; font-size: 1.35rem; margin-bottom: 8px;">\n        எழுத்துகள் ‘அ’ • ‘ஆ’ • ‘இ’ • ‘ஈ’'
        )

    # 7. Four virtue items
    if 'WBS 1.3.1' not in html:
        html = html.replace(
            '<span style="display: inline-block; background: var(--gold); color: #0a0c10; width: 26px; height: 26px; line-height: 26px; text-align: center; border-radius: 50%; font-weight: 800; margin-right: 8px;">அ</span>\n              அறம்',
            '<span class="wbs-code">WBS 1.3.1</span> <span style="display: inline-block; background: var(--gold); color: #0a0c10; width: 26px; height: 26px; line-height: 26px; text-align: center; border-radius: 50%; font-weight: 800; margin-right: 8px;">அ</span>\n              அறம்'
        )
        html = html.replace(
            '<span style="display: inline-block; background: var(--gold); color: #0a0c10; width: 26px; height: 26px; line-height: 26px; text-align: center; border-radius: 50%; font-weight: 800; margin-right: 8px;">ஆ</span>\n              ஆறுதல்',
            '<span class="wbs-code">WBS 1.3.2</span> <span style="display: inline-block; background: var(--gold); color: #0a0c10; width: 26px; height: 26px; line-height: 26px; text-align: center; border-radius: 50%; font-weight: 800; margin-right: 8px;">ஆ</span>\n              ஆறுதல்'
        )
        html = html.replace(
            '<span style="display: inline-block; background: var(--gold); color: #0a0c10; width: 26px; height: 26px; line-height: 26px; text-align: center; border-radius: 50%; font-weight: 800; margin-right: 8px;">இ</span>\n              இன்சொல்',
            '<span class="wbs-code">WBS 1.3.3</span> <span style="display: inline-block; background: var(--gold); color: #0a0c10; width: 26px; height: 26px; line-height: 26px; text-align: center; border-radius: 50%; font-weight: 800; margin-right: 8px;">இ</span>\n              இன்சொல்'
        )
        html = html.replace(
            '<span style="display: inline-block; background: var(--gold); color: #0a0c10; width: 26px; height: 26px; line-height: 26px; text-align: center; border-radius: 50%; font-weight: 800; margin-right: 8px;">ஈ</span>\n              ஈகை',
            '<span class="wbs-code">WBS 1.3.4</span> <span style="display: inline-block; background: var(--gold); color: #0a0c10; width: 26px; height: 26px; line-height: 26px; text-align: center; border-radius: 50%; font-weight: 800; margin-right: 8px;">ஈ</span>\n              ஈகை'
        )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'WBS successfully updated in {path}')
