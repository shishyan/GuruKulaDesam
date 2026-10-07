# -*- coding: utf-8 -*-
"""
Upgrade Tharam 1 to include the Course Sidebar and Section Navigation
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

sidebar_html = """
    <!-- Two-Column Layout Container: Sticky Sidebar + Main Content Column -->
    <div class="course-layout-container">
      
      <!-- Left Course Navigation Sidebar -->
      <aside class="course-sidebar" id="courseSidebar">
        <div class="sidebar-header">
          <span class="sidebar-grade-badge">தரம் 1 பாடநெறி</span>
          <h3 class="sidebar-title">பாடப் பொருளடக்கம்</h3>
          <p class="sidebar-sub">அத்தியாயங்கள் &amp; உட்பிரிவுகள்</p>
        </div>

        <nav class="sidebar-nav" aria-label="Course Sections">
          <div class="sidebar-chapter-group active" id="side-group-sheets">
            <a href="#sheets-section" class="sidebar-chapter-btn active" style="text-decoration:none;">
              <span class="sidebar-chapter-pill">
                <span class="sidebar-num">📖</span>
                <span>60 பாடநூல் தாள்கள்</span>
              </span>
            </a>
          </div>

          <div class="sidebar-chapter-group" id="side-group-highlights">
            <a href="#syllabus-highlights" class="sidebar-chapter-btn" style="text-decoration:none;">
              <span class="sidebar-chapter-pill">
                <span class="sidebar-num">🎯</span>
                <span>பாடத்திட்ட உள்ளடக்கம்</span>
              </span>
            </a>
          </div>

          <div class="sidebar-chapter-group" id="side-group-virtue">
            <a href="#virtue-section" class="sidebar-chapter-btn" style="text-decoration:none;">
              <span class="sidebar-chapter-pill">
                <span class="sidebar-num">✨</span>
                <span>அகர வரிசை நற்பண்புகள்</span>
              </span>
            </a>
          </div>

          <div class="sidebar-chapter-group" id="side-group-google">
            <a href="https://sites.google.com/view/wwwgurukuladesamcom/home/%E0%AE%9A%E0%AE%B5-%E0%AE%A8%E0%AE%B1/%E0%AE%A4%E0%AE%B0%E0%AE%AE-1" target="_blank" rel="noopener" class="sidebar-chapter-btn" style="text-decoration:none;">
              <span class="sidebar-chapter-pill">
                <span class="sidebar-num">🌐</span>
                <span>கூகிள் தளம் நேரடி ↗</span>
              </span>
            </a>
          </div>
        </nav>

        <!-- Quick Grade Switcher in Sidebar -->
        <div class="sidebar-other-grades">
          <div class="sidebar-other-grades-title">அனைத்து 12 தரங்கள் (Jump to Grade):</div>
          <div class="sidebar-grades-grid">
            <a href="tharam-1.html" class="sidebar-grade-pill active">1</a>
            <a href="tharam-2.html" class="sidebar-grade-pill">2</a>
            <a href="tharam-3.html" class="sidebar-grade-pill">3</a>
            <a href="tharam-4.html" class="sidebar-grade-pill">4</a>
            <a href="tharam-5.html" class="sidebar-grade-pill">5</a>
            <a href="tharam-6.html" class="sidebar-grade-pill">6</a>
            <a href="tharam-7.html" class="sidebar-grade-pill">7</a>
            <a href="tharam-8.html" class="sidebar-grade-pill">8</a>
            <a href="tharam-9.html" class="sidebar-grade-pill">9</a>
            <a href="tharam-10.html" class="sidebar-grade-pill">10</a>
            <a href="tharam-11.html" class="sidebar-grade-pill">11</a>
            <a href="tharam-12.html" class="sidebar-grade-pill">12</a>
          </div>
        </div>
      </aside>

      <!-- Main Course Column -->
      <div class="course-main-column">
"""

footer_drawer_html = """
  <!-- Mobile Floating Drawer Toggle Button & Backdrop -->
  <button type="button" class="course-sidebar-mobile-toggle" onclick="toggleCourseSidebar()" aria-label="பொருளடக்கம் காண்க">
    📋 பொருளடக்கம் (Sections)
  </button>
  <div class="course-sidebar-overlay" id="courseSidebarOverlay" onclick="closeCourseSidebar()"></div>
"""

sidebar_script = """
  <script>
    function toggleCourseSidebar() {
      const sidebar = document.getElementById('courseSidebar');
      const overlay = document.getElementById('courseSidebarOverlay');
      if (sidebar && overlay) {
        const isOpen = sidebar.classList.contains('open');
        if (isOpen) {
          sidebar.classList.remove('open');
          overlay.classList.remove('active');
          document.body.style.overflow = '';
        } else {
          sidebar.classList.add('open');
          overlay.classList.add('active');
          document.body.style.overflow = 'hidden';
        }
      }
    }

    function closeCourseSidebar() {
      const sidebar = document.getElementById('courseSidebar');
      const overlay = document.getElementById('courseSidebarOverlay');
      if (sidebar && overlay) {
        sidebar.classList.remove('open');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
      }
    }
  </script>
"""

for path in ['tharam-1.html', 'site/tharam-1.html', 'docs/tharam-1.html']:
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # If already updated, skip
    if 'class="course-layout-container"' in content:
        print(f"{path} already has course-layout-container")
        continue

    # Add id to highlights and sheets sections
    content = content.replace('<div class="scripture-study-section" style="margin-top: 20px;">', '<div id="syllabus-highlights" class="scripture-study-section" style="margin-top: 20px;">')
    content = content.replace('<div style="display:flex; justify-content:space-between; align-items:center; margin-top:30px;">', '<div id="sheets-section" style="display:flex; justify-content:space-between; align-items:center; margin-top:30px;">')
    content = content.replace('<section class="scripture-study-section" style="margin-top: 40px;', '<section id="virtue-section" class="scripture-study-section" style="margin-top: 40px;')

    # Insert sidebar after quick nav bar
    target = '<!-- Quick Navigation Between Grades -->'
    pos = content.find(target)
    if pos != -1:
        # find the end of the quick nav div
        end_div = content.find('</div>', pos) + len('</div>')
        content = content[:end_div] + "\n" + sidebar_html + content[end_div:]

    # Close the two-column container before </main>
    content = content.replace('</main>', '      </div>\n    </div>\n  </main>\n' + footer_drawer_html)

    # Append sidebar script before </body>
    content = content.replace('</body>', sidebar_script + '\n</body>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {path} with sidebar and sections")

print("Tharam 1 upgrade complete!")
