import json
import os
import shutil
import re

# 1. Load 60 images for Grade 1
grade1_images = []
if os.path.exists('grade1_images.json'):
    with open('grade1_images.json', 'r', encoding='utf-8') as f:
        grade1_images = json.load(f)

print(f"Loaded {len(grade1_images)} Grade 1 images.")

# 2. Update CSS with new component classes
css_path = 'assets/css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

new_css = """
/* ==========================================================================
   Google Sites Imported Pages & Education Styles (Guru Kula Desam)
   ========================================================================== */

/* Multi-column Kalvi Dropdown Menu */
.kalvi-menu {
  min-width: 440px !important;
  display: none;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
  max-height: 520px;
  overflow-y: auto;
}

@media (min-width: 1101px) {
  .nav-dropdown:hover .kalvi-menu,
  .nav-dropdown.open .kalvi-menu {
    display: grid !important;
    opacity: 1;
    transform: translateY(0);
    pointer-events: auto;
  }
}

@media (max-width: 1100px) {
  .kalvi-menu {
    min-width: 100% !important;
    grid-template-columns: 1fr !important;
    max-height: none;
  }
}

/* Grades Hub Grid */
.grades-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin: 30px 0;
}

.grade-card {
  background: var(--bg-card);
  border: 1px solid var(--border-gold);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 14px;
  text-decoration: none;
  color: inherit;
  position: relative;
  overflow: hidden;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
}

.grade-card:hover {
  transform: translateY(-4px);
  border-color: var(--gold-bright);
  box-shadow: 0 14px 32px rgba(0, 0, 0, 0.6), var(--shadow-gold);
  background: rgba(24, 29, 39, 0.95);
}

.grade-card-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  align-self: flex-start;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 700;
  background: rgba(212, 175, 55, 0.15);
  color: var(--gold-bright);
  border: 1px solid rgba(212, 175, 55, 0.3);
}

.grade-card-header {
  display: flex;
  align-items: center;
  gap: 14px;
}

.grade-card-icon {
  font-size: 2.2rem;
  line-height: 1;
  filter: drop-shadow(0 0 6px rgba(212, 175, 55, 0.4));
}

.grade-card-title h3 {
  font-size: 1.25rem;
  color: var(--gold-soft);
  font-weight: 700;
  margin-bottom: 2px;
}

.grade-card-title span {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.grade-card-desc {
  font-size: 0.88rem;
  color: var(--text-main);
  line-height: 1.5;
}

.grade-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--gold);
  border-top: 1px solid var(--border-subtle);
  padding-top: 12px;
  margin-top: 4px;
}

/* 60 Sheets Grid for Grade 1 */
.sheets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 18px;
  margin: 28px 0;
}

.sheet-card {
  background: var(--bg-card);
  border: 1px solid var(--border-gold);
  border-radius: 14px;
  overflow: hidden;
  transition: all 0.25s ease;
  display: flex;
  flex-direction: column;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
}

.sheet-card:hover {
  transform: translateY(-4px);
  border-color: var(--gold-bright);
  box-shadow: 0 10px 24px rgba(212, 175, 55, 0.3);
}

.sheet-header {
  padding: 10px 14px;
  background: rgba(12, 15, 21, 0.95);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--gold-bright);
}

.sheet-thumb {
  width: 100%;
  aspect-ratio: 3 / 4;
  background: #0f1218;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.sheet-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.sheet-thumb:hover img {
  transform: scale(1.05);
}

.sheet-zoom-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
  font-size: 1.8rem;
  color: #fff;
}

.sheet-thumb:hover .sheet-zoom-overlay {
  opacity: 1;
}

.sheet-actions {
  padding: 10px 12px;
  background: rgba(12, 15, 21, 0.85);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.sheet-btn {
  padding: 6px 10px;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s ease;
}

.sheet-btn-view {
  background: rgba(212, 175, 55, 0.18);
  color: var(--gold-bright);
  border: 1px solid rgba(212, 175, 55, 0.4);
}

.sheet-btn-view:hover {
  background: var(--gold);
  color: #07080b;
}

.sheet-btn-direct {
  background: transparent;
  color: var(--text-muted);
}

.sheet-btn-direct:hover {
  color: var(--gold-soft);
}

/* Music Feast (இறை இசை விருந்து) */
.music-feast-card {
  background: var(--bg-card);
  border: 1px solid var(--border-gold);
  border-radius: 18px;
  padding: 26px;
  margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 28px;
  align-items: start;
}

@media (max-width: 960px) {
  .music-feast-card {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}

.feast-media-frame {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--border-gold);
  background: #000;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
}

.feast-media-frame iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.feast-details {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.feast-badge-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.feast-title {
  font-size: 1.45rem;
  font-weight: 700;
  color: var(--gold-bright);
  line-height: 1.3;
}

.feast-meta {
  font-size: 0.85rem;
  color: var(--amber);
  font-weight: 600;
}

.feast-lyrics-box {
  background: rgba(10, 13, 18, 0.9);
  border-left: 3px solid var(--gold);
  padding: 14px 16px;
  border-radius: 0 8px 8px 0;
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--gold-soft);
  white-space: pre-line;
  font-family: inherit;
}

.feast-meaning {
  font-size: 0.88rem;
  color: var(--text-muted);
  line-height: 1.6;
}

/* Google Sites Mirror Banner */
.google-site-banner {
  background: linear-gradient(135deg, rgba(30, 42, 60, 0.95) 0%, rgba(15, 20, 30, 0.95) 100%);
  border: 1px solid var(--border-gold);
  border-radius: 16px;
  padding: 24px 30px;
  margin: 30px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
}

@media (max-width: 768px) {
  .google-site-banner {
    flex-direction: column;
    text-align: center;
  }
}

.gs-banner-content h3 {
  font-size: 1.25rem;
  color: var(--gold-bright);
  margin-bottom: 6px;
}

.gs-banner-content p {
  font-size: 0.9rem;
  color: var(--text-muted);
}

.gs-banner-btn {
  padding: 10px 22px;
  background: var(--gold);
  color: #07080b;
  border-radius: 24px;
  font-size: 0.9rem;
  font-weight: 700;
  text-decoration: none;
  white-space: nowrap;
  transition: all 0.2s ease;
  box-shadow: 0 4px 14px rgba(212, 175, 55, 0.35);
}

.gs-banner-btn:hover {
  background: var(--gold-bright);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
}

/* Image Sheet Modal */
.sheet-modal {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.92);
  backdrop-filter: blur(12px);
  display: none;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.sheet-modal.active {
  display: flex;
}

.sheet-modal-box {
  max-width: 900px;
  width: 100%;
  max-height: 94vh;
  display: flex;
  flex-direction: column;
  background: #0d1017;
  border: 1px solid var(--border-gold);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85);
}

.sheet-modal-header {
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(12, 15, 21, 0.95);
  border-bottom: 1px solid var(--border-gold);
}

.sheet-modal-title {
  color: var(--gold-bright);
  font-weight: 700;
  font-size: 1.05rem;
}

.sheet-modal-body {
  flex: 1;
  overflow-y: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  background: #08090d;
}

.sheet-modal-body img {
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
  border-radius: 8px;
}
"""

if "Google Sites Imported Pages" not in css_content:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write(new_css)
    print("Updated assets/css/style.css with new styles.")

# 3. Update main.js
js_path = 'assets/js/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

new_js = """
// Sheet Modal Handlers
function openSheetModal(imgSrc, pageNum, pageTitle) {
  const modal = document.getElementById('sheetModal');
  const modalImg = document.getElementById('sheetModalImg');
  const modalTitle = document.getElementById('sheetModalTitle');
  if (modal && modalImg) {
    modalImg.src = imgSrc;
    if (modalTitle) modalTitle.innerText = `தரம் 1 — பக்கம் ${pageNum} ${pageTitle ? '• ' + pageTitle : ''}`;
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeSheetModal() {
  const modal = document.getElementById('sheetModal');
  const modalImg = document.getElementById('sheetModalImg');
  if (modal) {
    modal.classList.remove('active');
    if (modalImg) modalImg.src = '';
    document.body.style.overflow = '';
  }
}

// Multi-dropdown support
function toggleDropdown(e, dropdownId) {
  if (e) {
    e.preventDefault();
    e.stopPropagation();
  }
  const targetId = dropdownId || (e && e.currentTarget && e.currentTarget.id ? e.currentTarget.id.replace('Btn', '') : null);
  const dropdown = targetId ? document.getElementById(targetId) : (e ? e.currentTarget.closest('.nav-dropdown') : document.querySelector('.nav-dropdown'));
  if (!dropdown) return;
  const wasOpen = dropdown.classList.contains('open');
  document.querySelectorAll('.nav-dropdown').forEach(d => {
    if (d !== dropdown) d.classList.remove('open');
  });
  dropdown.classList.toggle('open', !wasOpen);
  const toggleBtn = dropdown.querySelector('.dropdown-toggle');
  if (toggleBtn) toggleBtn.setAttribute('aria-expanded', !wasOpen ? 'true' : 'false');
}

document.addEventListener('click', (e) => {
  document.querySelectorAll('.nav-dropdown').forEach(dropdown => {
    if (!dropdown.contains(e.target)) {
      dropdown.classList.remove('open');
      const toggleBtn = dropdown.querySelector('.dropdown-toggle');
      if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'false');
    }
  });
});
"""

if "openSheetModal" not in js_content:
    with open(js_path, 'a', encoding='utf-8') as f:
        f.write(new_js)
    print("Updated assets/js/main.js with modal & multi-dropdown handlers.")

# 4. Standard Nav & Footer Generators
def get_header(active_page=""):
    def act(p):
        return "active" if active_page == p else ""

    return f"""  <header class="site-header">
    <div class="header-container">
      <a href="index.html" class="brand" aria-label="Guru Kula Desam Home">
        <div class="brand-emblem">ॐ</div>
        <div class="brand-text">
          <h1>குரு குல தேசம்</h1>
          <span>Guru Kula Desam <span class="brand-sub-extra">• வேத &amp; சைவ நெறி</span></span>
        </div>
      </a>
      <button class="mobile-toggle" id="mobileNavToggle" onclick="toggleMobileNav()" aria-label="பட்டி (Menu)" aria-expanded="false">☰</button>
      <div class="nav-overlay" id="navOverlay" onclick="closeMobileNav()"></div>
      <nav class="main-nav" id="mainNav">
        <a href="index.html" class="nav-link {act('home')}">முகப்பு</a>
        <a href="saiva-neri.html" class="nav-link {act('saiva')}">சைவ நெறி</a>

        <!-- Kalvi (Grades 1-12) Dropdown -->
        <div class="nav-dropdown {act('kalvi_group')}" id="kalviDropdown">
          <button class="nav-link dropdown-toggle {act('kalvi')}" id="kalviDropdownBtn" onclick="toggleDropdown(event, 'kalviDropdown')" aria-haspopup="true" aria-expanded="false">
            <span>கல்வி (Grades 1-12)</span>
            <span class="dropdown-arrow">▾</span>
          </button>
          <div class="dropdown-menu kalvi-menu" id="kalviDropdownMenu">
            <a href="kalvi.html" class="dropdown-item {act('kalvi_hub')}" style="grid-column: 1 / -1; border-bottom: 1px solid var(--border-subtle); margin-bottom: 4px;">
              <span class="dropdown-item-icon">🏛️</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">சைவ நெறி கல்வித் தளம் (Curriculum Hub)</div>
                <div class="dropdown-item-desc">தரம் 1 முதல் 12 வரையிலான முழுமையான பாடநெறி</div>
              </div>
            </a>
            <a href="tharam-1.html" class="dropdown-item {act('tharam-1')}">
              <span class="dropdown-item-icon">📖</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">தரம் 1 (Grade 1)</div>
                <div class="dropdown-item-desc">60 பாடப் படங்கள் &amp; நூல்கள்</div>
              </div>
            </a>
            <a href="tharam-2.html" class="dropdown-item {act('tharam-2')}">
              <span class="dropdown-item-icon">🪔</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 2 (Grade 2)</div></div>
            </a>
            <a href="tharam-3.html" class="dropdown-item {act('tharam-3')}">
              <span class="dropdown-item-icon">🔱</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 3 (Grade 3)</div></div>
            </a>
            <a href="tharam-4.html" class="dropdown-item {act('tharam-4')}">
              <span class="dropdown-item-icon">📜</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 4 (Grade 4)</div></div>
            </a>
            <a href="tharam-5.html" class="dropdown-item {act('tharam-5')}">
              <span class="dropdown-item-icon">🌺</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 5 (Grade 5)</div></div>
            </a>
            <a href="tharam-6.html" class="dropdown-item {act('tharam-6')}">
              <span class="dropdown-item-icon">🕉️</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 6 (Grade 6)</div></div>
            </a>
            <a href="tharam-7.html" class="dropdown-item {act('tharam-7')}">
              <span class="dropdown-item-icon">🔔</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 7 (Grade 7)</div></div>
            </a>
            <a href="tharam-8.html" class="dropdown-item {act('tharam-8')}">
              <span class="dropdown-item-icon">✨</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 8 (Grade 8)</div></div>
            </a>
            <a href="tharam-9.html" class="dropdown-item {act('tharam-9')}">
              <span class="dropdown-item-icon">⚜️</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 9 (Grade 9)</div></div>
            </a>
            <a href="tharam-10.html" class="dropdown-item {act('tharam-10')}">
              <span class="dropdown-item-icon">🌟</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 10 (Grade 10)</div></div>
            </a>
            <a href="tharam-11.html" class="dropdown-item {act('tharam-11')}">
              <span class="dropdown-item-icon">🔱</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 11 (Grade 11)</div></div>
            </a>
            <a href="tharam-12.html" class="dropdown-item {act('tharam-12')}">
              <span class="dropdown-item-icon">👑</span>
              <div class="dropdown-item-content"><div class="dropdown-item-title">தரம் 12 (Grade 12)</div></div>
            </a>
          </div>
        </div>

        <!-- Traditions Dropdown -->
        <div class="nav-dropdown {act('traditions')}" id="traditionsDropdown">
          <button class="nav-link dropdown-toggle" id="traditionsDropdownBtn" onclick="toggleDropdown(event, 'traditionsDropdown')" aria-haspopup="true" aria-expanded="false">
            <span>வழிபாட்டு நெறிகள்</span>
            <span class="dropdown-arrow">▾</span>
          </button>
          <div class="dropdown-menu" id="traditionsDropdownMenu">
            <a href="murugan.html" class="dropdown-item {act('murugan')}">
              <span class="dropdown-item-icon">🔱</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">முருகன் (Kaumaram)</div>
                <div class="dropdown-item-desc">கந்த சஷ்டி, திருப்புகழ் &amp; கானங்கள்</div>
              </div>
            </a>
            <a href="sakthi.html" class="dropdown-item {act('sakthi')}">
              <span class="dropdown-item-icon">🌸</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">சக்தி (Shaktham)</div>
                <div class="dropdown-item-desc">அபிராமி அந்தாதி &amp; லலிதா போற்றிகள்</div>
              </div>
            </a>
            <a href="vinayagar.html" class="dropdown-item {act('vinayagar')}">
              <span class="dropdown-item-icon">🐘</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">விநாயகர் (Ganapathyam)</div>
                <div class="dropdown-item-desc">விநாயகர் அகவல் &amp; மூல கணபதி பதிகங்கள்</div>
              </div>
            </a>
            <a href="vaishnava.html" class="dropdown-item {act('vaishnava')}">
              <span class="dropdown-item-icon">🪷</span>
              <div class="dropdown-item-content">
                <div class="dropdown-item-title">வைணவம் (Vaishnavam)</div>
                <div class="dropdown-item-desc">விஷ்ணு, கிருஷ்ணர் &amp; திவ்வியப் பிரபந்தம்</div>
              </div>
            </a>
          </div>
        </div>

        <a href="thirukkural.html" class="nav-link {act('thirukkural')}">திருக்குறள்</a>
        <a href="sanmargam.html" class="nav-link {act('sanmargam')}">சன்மார்க்கம்</a>
        <a href="irai-isai-virundhu.html" class="nav-link {act('irai-isai')}">இறை இசை</a>
        <a href="syllabus.html" class="nav-link {act('syllabus')}">பாடத்திட்டம்</a>
        <a href="classes.html" class="nav-link {act('classes')}">வகுப்புகள்</a>
        <a href="about.html" class="nav-link {act('about')}">பெரியவா தரிசனம்</a>
        <a href="https://sites.google.com/view/wwwgurukuladesamcom" target="_blank" rel="noopener" class="nav-link" style="border: 1px solid var(--border-gold); padding: 5px 12px; border-radius: 16px; color: var(--gold-bright);">🌐 கூகிள் தளம் ↗</a>
        <a href="https://www.youtube.com/@guru-kula-desam?sub_confirmation=1" target="_blank" rel="noopener noreferrer" class="yt-btn-header">
          ▶ YouTube
        </a>
      </nav>
    </div>
  </header>"""

def get_footer():
    return """  <footer class="site-footer">
    <div class="footer-container">
      <div class="footer-col">
        <h4>குரு குல தேசம் (Guru Kula Desam)</h4>
        <p>வேதங்கள், பன்னிரு திருமுறைகள், சைவ சித்தாந்த சாத்திரங்கள், காஞ்சி மகா பெரியவா அருளுரைகள் மற்றும் வள்ளலார் பெருமானின் சுத்த சன்மார்க்க நெறிகளை உலகிற்கு பறைசாற்றும் ஆன்மீக இசை &amp; கல்விப் பெருவெளி.</p>
        <p style="margin-top: 10px; color: var(--gold); font-weight: 600;">அன்பே சிவம் • யாதும் ஊரே யாவரும் கேளிர் • ஏகன் அநேகன்</p>
        <div style="margin-top: 14px; font-size: 0.84rem; color: var(--gold-soft); line-height: 1.6; border-left: 2px solid var(--gold); padding-left: 12px; background: rgba(212, 175, 55, 0.05); padding-top: 6px; padding-bottom: 6px; border-radius: 0 8px 8px 0;">
          📍 <strong>மைய முகவரி (Headquarters):</strong><br>
          32, SSS Jaya Enclave, Kovaipudur,<br>
          Coimbatore, 641042, Tamil Nadu, India.
        </div>
      </div>
      <div class="footer-col">
        <h4>சைவ நெறி கல்வி &amp; பாடங்கள்</h4>
        <ul class="footer-links">
          <li><a href="kalvi.html">சைவ நெறி கல்வித் தளம் (Grades 1 - 12)</a></li>
          <li><a href="tharam-1.html">தரம் 1 — 60 பாடப் படங்கள் &amp; நூல்கள்</a></li>
          <li><a href="tharam-2.html">தரம் 2 — சிவ சின்னங்கள் &amp; ஆலய வழிபாடு</a></li>
          <li><a href="tharam-3.html">தரம் 3 முதல் தரம் 12 வரை</a></li>
          <li><a href="irai-isai-virundhu.html">இறை இசை விருந்து (5 சிறப்புப் பாடல்கள்)</a></li>
          <li><a href="syllabus.html">பாடத்திட்டம் (Comprehensive Syllabus)</a></li>
          <li><a href="classes.html">வகுப்புகள் (Online Classes &amp; Timetable)</a></li>
          <li><a href="https://sites.google.com/view/wwwgurukuladesamcom" target="_blank" rel="noopener">அதிகாரப்பூர்வ கூகிள் தளம் (Google Sites Mirror) ↗</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>ஆன்மீக வழிகள் &amp; இசை</h4>
        <ul class="footer-links">
          <li><a href="saiva-neri.html">சிவ நெறி (172 திருமுறைப் பாடல்கள்)</a></li>
          <li><a href="thirukkural.html">திருக்குறள் (185 அதிகாரப் படங்கள் &amp; இசை)</a></li>
          <li><a href="sanmargam.html">சன்மார்க்கம் (94 அருட்பெருஞ்சோதிப் பாடல்கள்)</a></li>
          <li><a href="murugan.html">முருக நெறி (கந்த சஷ்டி &amp; திருப்புகழ்)</a></li>
          <li><a href="sakthi.html">சக்தி நெறி (அபிராமி அந்தாதி &amp; போற்றிகள்)</a></li>
          <li><a href="vinayagar.html">விநாயகர் நெறி &amp; வைணவம்</a></li>
          <li><a href="youtube.html">YouTube இசை &amp; படக் களஞ்சியம்</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      &copy; 2026 குரு குல தேசம் (Guru Kula Desam) | gurukuladesam.com | 32, SSS Jaya Enclave, Kovaipudur, Coimbatore, Tamil Nadu, India | அனைத்து உரிமைகளும் இறைப்பணிக்கே சமர்ப்பணம்.
    </div>
  </footer>"""

print("Helper templates ready.")
