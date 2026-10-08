import re

css_path = 'assets/css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

has_crlf = '\r\n' in css
css = css.replace('\r\n', '\n')

# 1. Update main.main-content to include zoom: 1.2
css = re.sub(
    r'main\.main-content\s*\{[^}]*\}',
    '''main.main-content {
  flex: 1;
  width: 100%;
  max-width: 100% !important;
  margin: 0 !important;
  padding: 24px 36px 80px 36px;
  box-sizing: border-box;
  zoom: 1.2;
}''',
    css,
    count=1
)

# 2. Update context-bar-container & header-container for breathing space
css = re.sub(
    r'\.context-bar-container,\s*\.header-container\s*\{[^}]*\}',
    '''.context-bar-container,
.header-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 14px 36px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 28px !important;
  min-height: 64px;
}''',
    css
)

# 3. Add inpage-content-nav & top-bar breathing space styles
inpage_nav_css = """

/* ========================================================================== */
/* CONTENT AREA ZOOM & IN-PAGE SECTION NAVIGATION                             */
/* ========================================================================== */
@media (max-width: 768px) {
  main.main-content {
    padding: 16px 18px 60px 18px;
    zoom: 1.15;
  }
}

/* In-Page Content Navigation (Section & Category Filters moved down into Content Area) */
.inpage-content-nav {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  padding: 14px 20px;
  margin: 20px 0 28px 0;
  background: var(--bg-card);
  border: 1px solid rgba(56, 189, 248, 0.22);
  border-radius: 14px;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
}

.inpage-content-nav .context-tab-pill,
.inpage-content-nav button,
.inpage-content-nav a {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #cbd5e1;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  text-decoration: none;
}

.inpage-content-nav .context-tab-pill:hover,
.inpage-content-nav button:hover,
.inpage-content-nav a:hover {
  background: rgba(56, 189, 248, 0.16);
  border-color: var(--teal-bright);
  color: #ffffff;
  transform: translateY(-1px);
}

.inpage-content-nav .context-tab-pill.active,
.inpage-content-nav button.active,
.inpage-content-nav a.active {
  background: linear-gradient(135deg, rgba(45, 212, 191, 0.25) 0%, rgba(14, 165, 233, 0.25) 100%);
  border-color: var(--teal-bright);
  color: #ffffff;
  font-weight: 700;
  box-shadow: 0 0 12px rgba(45, 212, 191, 0.35);
}

.inpage-content-nav .context-tab-pill-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.inpage-content-nav .context-tab-pill-icon svg {
  width: 18px;
  height: 18px;
}
"""

css += inpage_nav_css

if has_crlf:
    css = css.replace('\n', '\r\n')

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated style.css with 20% content zoom and in-page navigation styles!")
