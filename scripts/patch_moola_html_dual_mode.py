import re

with open('moola-nool.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add authentic-srilanka-canon.js script tag before moola-nool-data.js
if 'assets/js/authentic-srilanka-canon.js' not in html:
    html = html.replace(
        '<script src="assets/js/moola-nool-data.js"></script>',
        '<script src="assets/js/authentic-srilanka-canon.js"></script>\n  <script src="assets/js/moola-nool-data.js"></script>'
    )

# 2. Add Dual-Mode CSS Styles and Kid-Friendly Reader Styling
dual_mode_css = '''
    /* Dual Mode Switch & Children-Friendly Reader Enhancement */
    .view-mode-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      margin: 16px 0 24px;
      padding: 12px 18px;
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.95));
      border: 1px solid rgba(212, 175, 55, 0.35);
      border-radius: 14px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .view-mode-tabs {
      display: inline-flex;
      background: rgba(10, 15, 30, 0.8);
      padding: 4px;
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.12);
    }
    .view-mode-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: transparent;
      border: none;
      color: #94a3b8;
      padding: 8px 16px;
      font-size: 0.9rem;
      font-weight: 600;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.25s ease;
    }
    .view-mode-btn:hover {
      color: #fff;
    }
    .view-mode-btn.active {
      background: rgba(212, 175, 55, 0.25);
      color: #ffd700;
      border: 1px solid rgba(212, 175, 55, 0.4);
      box-shadow: 0 0 12px rgba(212, 175, 55, 0.2);
    }
    .kid-friendly-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(16, 185, 129, 0.18);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: #34d399;
      font-size: 0.82rem;
      font-weight: 700;
      padding: 4px 12px;
      border-radius: 16px;
    }
    .kid-story-box {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(30, 41, 59, 0.7) 100%);
      border-left: 4px solid #f59e0b;
      border-radius: 0 12px 12px 0;
      padding: 14px 18px;
      margin: 14px 0 8px;
    }
    .kid-story-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 700;
      font-size: 0.95rem;
      color: #fbbf24;
      margin-bottom: 6px;
    }
    .archive-doc-viewer {
      width: 100%;
      height: 750px;
      border: 1px solid rgba(212, 175, 55, 0.35);
      border-radius: 14px;
      background: #0f172a;
      overflow: hidden;
      margin-top: 16px;
    }
    .archive-meta-banner {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid rgba(212, 175, 55, 0.3);
      border-radius: 12px;
      padding: 12px 18px;
      margin-bottom: 14px;
    }
'''

if '.view-mode-bar' not in html:
    html = html.replace('</style>', dual_mode_css + '\n</style>')

# 3. Update JavaScript logic inside moola-nool.html to support Dual Modes and Kids Story Box
js_extension = '''
    // Current Reader Display Mode: 'readable' (Clean Kids/Verse View) vs 'archive' (Authentic Scan View)
    var currentViewMode = 'readable';

    function setViewMode(mode) {
      currentViewMode = mode;
      var btnReadable = document.getElementById('viewModeBtnReadable');
      var btnArchive = document.getElementById('viewModeBtnArchive');
      if (btnReadable) btnReadable.classList.toggle('active', mode === 'readable');
      if (btnArchive) btnArchive.classList.toggle('active', mode === 'archive');

      var readableSec = document.getElementById('readableContentBlock');
      var archiveSec = document.getElementById('archiveContentBlock');
      if (readableSec) readableSec.style.display = (mode === 'readable') ? 'block' : 'none';
      if (archiveSec) archiveSec.style.display = (mode === 'archive') ? 'block' : 'none';
    }
'''

if 'var currentViewMode' not in html:
    html = html.replace('var currentSectionId = \'\';', 'var currentSectionId = \'\';\n' + js_extension)

# Write updated HTML
with open('moola-nool.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated moola-nool.html with Dual Mode and Kid-friendly styling & controls.")
