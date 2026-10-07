import os
import re

ROOT = r"c:\GitHub\Gurukuladesam"
filepath = os.path.join(ROOT, "about.html")

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

sidebar_html = """
    <!-- Dedicated Sub-Menu Sidebar for Guru Group -->
    <aside class="course-sidebar dedicated-sub-sidebar" id="guruSidebar">
      <div class="sidebar-header">
        <div class="dedicated-sub-header">
          <span class="dedicated-group-pill">🏛️ குருவருள் (Guru Sub-menu)</span>
        </div>
        <h3 class="sidebar-title">குருவருள் &amp; அறிமுகம்</h3>
        <p class="sidebar-sub">காஞ்சி மகா பெரியவா அருளுரைகள்</p>
      </div>

      <nav class="sidebar-nav" aria-label="Guru Sections">
        <div class="sidebar-chapter-group active">
          <a href="about.html" class="sidebar-chapter-btn active">
            <span class="sidebar-chapter-pill">
              <span class="sidebar-num">🙏</span>
              <span>மகா பெரியவா தத்துவம்</span>
            </span>
          </a>
        </div>
        <div class="sidebar-chapter-group">
          <a href="google-site.html" class="sidebar-chapter-btn">
            <span class="sidebar-chapter-pill">
              <span class="sidebar-num">🌐</span>
              <span>கூகிள் தளம் நேரடி இணைப்பு</span>
            </span>
          </a>
        </div>
      </nav>

      <div style="margin-top:16px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.08);">
        <div style="font-size:0.76rem; color:#38bdf8; font-weight:700; text-transform:uppercase; margin-bottom:8px;">அருளுரை பகுதிகள்:</div>
        <div style="display:flex; flex-direction:column; gap:6px;">
          <button type="button" class="sidebar-chapter-btn" onclick="scrollToSection('teachingsSection')"><span class="sidebar-chapter-pill"><span class="sidebar-num">📖</span><span>தெய்வத்தின் குரல் சாரம்</span></span></button>
          <button type="button" class="sidebar-chapter-btn" onclick="scrollToSection('vedicSection')"><span class="sidebar-chapter-pill"><span class="sidebar-num">🕉️</span><span>வேத சம்ரக்ஷண இயக்கம்</span></span></button>
          <button type="button" class="sidebar-chapter-btn" onclick="scrollToSection('darshanSection')"><span class="sidebar-chapter-pill"><span class="sidebar-num">🌟</span><span>நேரடி தரிசன பதிவுகள்</span></span></button>
        </div>
      </div>
    </aside>
"""

m = re.search(r'(<main[^>]*>)([\s\S]*?)(</main>)', content)
if m:
    inner_content = m.group(2)
    new_main = f"""<main class="main-content">
    <div class="course-layout-container">
      {sidebar_html}
      <div class="course-main-column">
        {inner_content}
      </div>
    </div>
  </main>"""
    content = content[:m.start()] + new_main + content[m.end():]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    for dest_dir in [os.path.join(ROOT, "docs"), os.path.join(ROOT, "site")]:
        dest_path = os.path.join(dest_dir, "about.html")
        if os.path.exists(dest_dir):
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(content)

    print("Updated about.html across root, docs, and site")
