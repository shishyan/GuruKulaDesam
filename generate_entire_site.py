import json
import os

with open('site_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Ensure directory structure
os.makedirs('Site', exist_ok=True)
os.makedirs('Site/assets/css', exist_ok=True)
os.makedirs('Site/assets/js', exist_ok=True)
os.makedirs('Site/assets/data', exist_ok=True)

# 1. Save data
with open('Site/assets/data/catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

# 2. CNAME file for custom domain
with open('Site/CNAME', 'w', encoding='utf-8') as f:
    f.write('gurukuladesam.com\n')

# 3. Write Shared CSS
css_content = """/* Guru Kula Desam - Modern Saiva Neri Spiritual Design System */
@import url('https://fonts.googleapis.com/css2?family=Mukta+Malar:wght@300;400;500;600;700;800&family=Outfit:wght@300;400;500;600;700;800&display=swap');

:root {
  --bg-dark: #07080b;
  --bg-surface: #0f1218;
  --bg-card: rgba(19, 23, 31, 0.8);
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-gold: rgba(212, 175, 55, 0.25);
  --border-gold-hover: rgba(212, 175, 55, 0.55);
  --gold: #d4af37;
  --gold-bright: #ffd700;
  --gold-soft: #fbf2d3;
  --amber: #e09f3e;
  --text-main: #f3f5f8;
  --text-muted: #9aa2b1;
  --badge-film: #e63946;
  --badge-audio: #2a9d8f;
  --shadow-card: 0 10px 30px rgba(0, 0, 0, 0.45);
  --shadow-gold: 0 0 25px rgba(212, 175, 55, 0.2);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Outfit', 'Mukta Malar', sans-serif;
  background-color: var(--bg-dark);
  background-image: 
    radial-gradient(circle at 50% 0%, rgba(212, 175, 55, 0.08) 0%, transparent 50%),
    radial-gradient(circle at 10% 30%, rgba(224, 159, 62, 0.05) 0%, transparent 40%),
    radial-gradient(circle at 90% 70%, rgba(230, 57, 70, 0.03) 0%, transparent 40%);
  color: var(--text-main);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

/* Header & Navigation */
header.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(7, 8, 11, 0.92);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--border-gold);
}

.header-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 14px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: inherit;
}

.brand-emblem {
  font-size: 1.8rem;
  color: var(--gold-bright);
  filter: drop-shadow(0 0 8px rgba(212, 175, 55, 0.5));
}

.brand-text h1 {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--gold-soft);
  letter-spacing: -0.01em;
}

.brand-text span {
  font-size: 0.75rem;
  color: var(--amber);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-weight: 600;
}

nav.main-nav {
  display: flex;
  gap: 6px;
  align-items: center;
}

.nav-link {
  color: var(--text-muted);
  text-decoration: none;
  padding: 8px 14px;
  border-radius: 20px;
  font-size: 0.88rem;
  font-weight: 500;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.nav-link:hover {
  color: var(--gold-soft);
  background: rgba(212, 175, 55, 0.1);
}

.nav-link.active {
  color: #07080b;
  background: var(--gold);
  font-weight: 700;
}

.yt-btn-header {
  background: #ff0000;
  color: #fff;
  padding: 7px 15px;
  border-radius: 20px;
  text-decoration: none;
  font-size: 0.82rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  margin-left: 8px;
  transition: transform 0.2s, background 0.2s;
}

.yt-btn-header:hover {
  background: #cc0000;
  transform: translateY(-1px);
}

/* Mobile Nav Toggle */
.mobile-toggle {
  display: none;
  background: none;
  border: none;
  color: var(--gold);
  font-size: 1.6rem;
  cursor: pointer;
}

@media (max-width: 1080px) {
  .mobile-toggle { display: block; }
  nav.main-nav {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: #0f1218;
    flex-direction: column;
    padding: 16px;
    border-bottom: 1px solid var(--border-gold);
    gap: 8px;
  }
  nav.main-nav.open { display: flex; }
  .nav-link { width: 100%; text-align: left; }
}

/* Main Container */
main.main-content {
  flex: 1;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  padding: 30px 24px 60px 24px;
}

/* Page Hero */
.hero-banner {
  text-align: center;
  max-width: 900px;
  margin: 0 auto 35px auto;
  padding: 20px 10px;
}

.hero-banner .sacred-tag {
  color: var(--amber);
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin-bottom: 8px;
}

.hero-banner h1 {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--gold-soft);
  text-shadow: 0 0 25px rgba(212, 175, 55, 0.35);
  margin-bottom: 8px;
}

.hero-banner h2 {
  font-size: 1.15rem;
  color: var(--amber);
  font-weight: 500;
  margin-bottom: 16px;
}

.verse-quote {
  display: inline-block;
  background: rgba(212, 175, 55, 0.08);
  border-left: 3px solid var(--gold);
  border-right: 3px solid var(--gold);
  padding: 12px 28px;
  border-radius: 8px;
  font-size: 1.02rem;
  color: #efe8d6;
  font-style: italic;
  font-family: 'Mukta Malar', serif;
  line-height: 1.6;
  margin-bottom: 14px;
}

.hero-banner p.hero-desc {
  color: var(--text-muted);
  font-size: 0.96rem;
  max-width: 760px;
  margin: 0 auto;
}

/* Modal Player */
.player-modal {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.88);
  backdrop-filter: blur(10px);
  display: none;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.player-modal.active { display: flex; }

.player-modal-box {
  background: #11141c;
  border: 1px solid var(--border-gold-hover);
  border-radius: 18px;
  width: 100%;
  max-width: 960px;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0,0,0,0.8), 0 0 35px rgba(212,175,55,0.25);
  animation: modalScale 0.25s ease;
}

@keyframes modalScale {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

.modal-iframe-wrapper {
  position: relative;
  padding-bottom: 56.25%;
  height: 0;
  background: #000;
}

.modal-iframe-wrapper iframe {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  border: none;
}

.modal-footer {
  padding: 14px 22px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #151822;
  border-top: 1px solid var(--border-subtle);
}

.modal-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--gold-soft);
}

.modal-close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  padding: 6px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background 0.2s;
}

.modal-close-btn:hover { background: rgba(255, 255, 255, 0.25); }

/* Controls & Filters */
.controls-panel {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-card);
  padding: 14px 20px;
  border-radius: 16px;
  border: 1px solid var(--border-subtle);
  margin-bottom: 30px;
  backdrop-filter: blur(10px);
}

.search-box {
  flex: 1;
  min-width: 280px;
  max-width: 480px;
  position: relative;
}

.search-box input {
  width: 100%;
  padding: 11px 18px 11px 40px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 30px;
  color: #fff;
  font-size: 0.95rem;
  outline: none;
  font-family: inherit;
  transition: all 0.2s;
}

.search-box input:focus {
  border-color: var(--gold);
  box-shadow: 0 0 14px rgba(212, 175, 55, 0.25);
  background: rgba(255, 255, 255, 0.08);
}

.search-box::before {
  content: "🔍";
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.9rem;
  opacity: 0.6;
}

.filter-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.filter-btn {
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: var(--text-muted);
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.2s;
}

.filter-btn:hover {
  color: #fff;
  border-color: rgba(255, 255, 255, 0.25);
}

.filter-btn.active {
  background: var(--gold);
  color: #07080b;
  border-color: var(--gold);
  font-weight: 700;
}

.item-count-badge {
  font-size: 0.88rem;
  color: var(--gold-soft);
  font-weight: 600;
  white-space: nowrap;
}

/* Media Cards Grid */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: 22px;
}

.video-card {
  background: var(--bg-card);
  border: 1px solid var(--border-gold);
  border-radius: 14px;
  overflow: hidden;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
  backdrop-filter: blur(8px);
}

.video-card:hover {
  transform: translateY(-5px);
  border-color: var(--border-gold-hover);
  box-shadow: 0 12px 30px rgba(212, 175, 55, 0.18);
}

.card-thumbnail {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%;
  background: #14171d;
  overflow: hidden;
}

.card-thumbnail img {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  transition: transform 0.35s ease;
}

.video-card:hover .card-thumbnail img {
  transform: scale(1.06);
}

.card-badge {
  position: absolute;
  top: 10px; right: 10px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  padding: 3px 9px;
  border-radius: 6px;
  color: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.5);
}

.badge-film { background: var(--badge-film); }
.badge-audio { background: var(--badge-audio); }

.card-play-btn {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 50px; height: 50px;
  background: rgba(0, 0, 0, 0.72);
  border: 2px solid var(--gold);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gold-bright);
  font-size: 1.3rem;
  opacity: 0;
  transition: opacity 0.2s ease, transform 0.2s ease;
  box-shadow: 0 0 18px rgba(212, 175, 55, 0.45);
}

.video-card:hover .card-play-btn {
  opacity: 1;
  transform: translate(-50%, -50%) scale(1.08);
}

.card-body {
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  justify-content: space-between;
}

.card-title {
  font-size: 0.95rem;
  font-weight: 600;
  line-height: 1.45;
  color: var(--text-main);
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.76rem;
  color: var(--text-muted);
  border-top: 1px solid var(--border-subtle);
  padding-top: 8px;
}

.card-footer .tag {
  color: var(--gold);
  font-weight: 600;
}

/* Home Highlights / Philosophy Sections */
.philosophy-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-top: 40px;
}

.philosophy-card {
  background: var(--bg-card);
  border: 1px solid var(--border-gold);
  border-radius: 16px;
  padding: 26px;
  transition: transform 0.2s, border-color 0.2s;
}

.philosophy-card:hover {
  transform: translateY(-4px);
  border-color: var(--gold);
}

.philosophy-card .card-icon {
  font-size: 2.2rem;
  margin-bottom: 12px;
  color: var(--gold-bright);
}

.philosophy-card h3 {
  font-size: 1.3rem;
  color: var(--gold-soft);
  margin-bottom: 8px;
}

.philosophy-card p {
  color: var(--text-muted);
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Footer */
footer.site-footer {
  background: #050608;
  border-top: 1px solid var(--border-gold);
  padding: 40px 24px;
  margin-top: auto;
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 30px;
}

.footer-col { flex: 1; min-width: 250px; }

.footer-col h4 {
  color: var(--gold-soft);
  font-size: 1.1rem;
  margin-bottom: 14px;
}

.footer-col p {
  color: var(--text-muted);
  font-size: 0.9rem;
  line-height: 1.6;
}

.footer-links {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.footer-links a {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 0.88rem;
  transition: color 0.2s;
}

.footer-links a:hover { color: var(--gold); }

.footer-bottom {
  max-width: 1400px;
  margin: 30px auto 0 auto;
  padding-top: 20px;
  border-top: 1px solid var(--border-subtle);
  text-align: center;
  font-size: 0.82rem;
  color: var(--text-muted);
}
"""

with open('Site/assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

# 4. Write Shared JavaScript
js_content = """// Guru Kula Desam - Modern Video Portal Logic
let currentFilter = 'all';
let currentSearch = '';

function initPage(itemsData) {
  window.pageItems = itemsData;
  renderCards();
}

function getFilteredItems() {
  if (!window.pageItems) return [];
  return window.pageItems.filter(it => {
    if (currentFilter !== 'all' && it.type !== currentFilter) return false;
    if (currentSearch) {
      const q = currentSearch.toLowerCase();
      return it.title.toLowerCase().includes(q) || it.id.includes(q);
    }
    return true;
  });
}

function renderCards() {
  const items = getFilteredItems();
  const grid = document.getElementById('cardsGrid');
  const countBadge = document.getElementById('itemCountBadge');

  if (countBadge) {
    countBadge.innerText = `காட்டப்படும் பாடல்கள்: ${items.length}`;
  }

  if (!grid) return;

  if (items.length === 0) {
    grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 70px 20px; color: var(--text-muted); font-size: 1.15rem;">பொருத்தமான பாடல்கள் காணப்படவில்லை (No matching items found)</div>';
    return;
  }

  grid.innerHTML = items.map(it => `
    <div class="video-card" onclick="openPlayer('${it.id}', '${it.title.replace(/'/g, "\\\\'")}')">
      <div class="card-thumbnail">
        <img src="https://i.ytimg.com/vi/${it.id}/mqdefault.jpg" loading="lazy" alt="${it.title}">
        <span class="card-badge ${it.type === 'film' ? 'badge-film' : 'badge-audio'}">${it.type === 'film' ? 'Film' : 'Audio'}</span>
        <div class="card-play-btn">▶</div>
      </div>
      <div class="card-body">
        <div class="card-title">${it.title}</div>
        <div class="card-footer">
          <span class="tag">${it.type === 'film' ? '🎬 முழுப் படம் (Film)' : '🎵 இசை வெளியீடு (Audio)'}</span>
          <span>YouTube ↗</span>
        </div>
      </div>
    </div>
  `).join('');
}

function setTypeFilter(type) {
  currentFilter = type;
  document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
  const target = document.getElementById('filter-' + type);
  if (target) target.classList.add('active');
  renderCards();
}

function onSearchInput(val) {
  currentSearch = val;
  renderCards();
}

function openPlayer(videoId, title) {
  const modal = document.getElementById('playerModal');
  const iframe = document.getElementById('modalIframe');
  const titleEl = document.getElementById('modalTitle');

  if (modal && iframe) {
    iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1`;
    if (titleEl) titleEl.innerText = title;
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closePlayer() {
  const modal = document.getElementById('playerModal');
  const iframe = document.getElementById('modalIframe');

  if (modal && iframe) {
    iframe.src = '';
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

function toggleMobileNav() {
  const nav = document.getElementById('mainNav');
  if (nav) nav.classList.toggle('open');
}

// Close player on ESC key
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closePlayer();
});
"""

with open('Site/assets/js/main.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Generated assets/css and assets/js!")

# 5. Page generator with global navigation
nav_links = [
    ('index.html', 'முகப்பு (Home)'),
    ('saiva-neri.html', 'சிவ நெறி'),
    ('thirukkural.html', 'திருக்குறள்'),
    ('sanmargam.html', 'சன்மார்க்கம்'),
    ('murugan.html', 'முருகன்'),
    ('sakthi.html', 'சக்தி'),
    ('vinayagar.html', 'விநாயகர்'),
    ('vaishnava.html', 'வைணவம்'),
    ('about.html', 'தத்துவ தரிசனம்')
]

def build_header(active_file):
    links_html = "".join([
        f'<a href="{f}" class="nav-link {"active" if f == active_file else ""}">{label}</a>'
        for f, label in nav_links
    ])
    return f"""
  <header class="site-header">
    <div class="header-container">
      <a href="index.html" class="brand">
        <div class="brand-emblem">ॐ</div>
        <div class="brand-text">
          <h1>குரு குல தேசம்</h1>
          <span>Guru Kula Desam</span>
        </div>
      </a>
      <button class="mobile-toggle" onclick="toggleMobileNav()">☰</button>
      <nav class="main-nav" id="mainNav">
        {links_html}
        <a href="https://www.youtube.com/@guru-kula-desam?sub_confirmation=1" target="_blank" class="yt-btn-header">
          ▶ Subscribe
        </a>
      </nav>
    </div>
  </header>
"""

def build_footer():
    return """
  <footer class="site-footer">
    <div class="footer-container">
      <div class="footer-col">
        <h4>குரு குல தேசம் (Guru Kula Desam)</h4>
        <p>சைவ நெறி, திருக்குறள், திருவருட்பா மற்றும் தமிழ் பக்தி இலக்கியப் பெருவெளி உலகிற்கு வழங்கும் புதிய யுக இசைப்படைப்புகள்.</p>
        <p style="margin-top: 10px; color: var(--gold);">அன்பே சிவம் | யாதும் ஊரே யாவரும் கேளிர்</p>
      </div>
      <div class="footer-col">
        <h4>வழிபாட்டு நெறிகள்</h4>
        <ul class="footer-links">
          <li><a href="saiva-neri.html">சைவ நெறி (சிவ பெருமான் பாடல்கள்)</a></li>
          <li><a href="thirukkural.html">திருக்குறள் மாஸ்டர் கலெக்ஷன்</a></li>
          <li><a href="sanmargam.html">வள்ளலார் சுத்த சன்மார்க்கம்</a></li>
          <li><a href="murugan.html">முருக நெறி & கந்த சஷ்டி</a></li>
          <li><a href="sakthi.html">சக்தி நெறி & அபிராமி அந்தாதி</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>நேரலை இணைப்புகள்</h4>
        <ul class="footer-links">
          <li><a href="https://www.youtube.com/@guru-kula-desam" target="_blank">YouTube அதிகாரப்பூர்வ தளம்</a></li>
          <li><a href="https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro" target="_blank">திருக்குறள் மாஸ்டர் பிளேலிஸ்ட்</a></li>
          <li><a href="https://www.youtube.com/playlist?list=PLeqSbdtlRtmc" target="_blank">சிவ பெருமான் பிளேலிஸ்ட்</a></li>
          <li><a href="about.html">புதிய யுக சைவ நெறி தரிசனம்</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      &copy; 2026 குரு குல தேசம் (Guru Kula Desam) | gurukuladesam.com | அனைத்து உரிமைகளும் பாதுகாக்கப்பட்டவை.
    </div>
  </footer>
"""

def build_player_modal():
    return """
  <div class="player-modal" id="playerModal" onclick="if(event.target === this) closePlayer()">
    <div class="player-modal-box">
      <div class="modal-iframe-wrapper">
        <iframe id="modalIframe" src="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      </div>
      <div class="modal-footer">
        <div class="modal-title" id="modalTitle">Now Playing</div>
        <button class="modal-close-btn" onclick="closePlayer()">✕ மூடுக (Close)</button>
      </div>
    </div>
  </div>
"""

# 6. Page configurations for generation
site_pages = [
    {
        'file': 'saiva-neri.html',
        'title': 'சைவ நெறி — புதிய யுகத்திற்கான ஆன்மீக ஒளி',
        'sub_en': 'Saiva Neri — Spiritual Light for the New Age',
        'verse': 'அன்பும் சிவமும் இரண்டென்பர் அறிவிலார் | அன்பே சிவமாவது ஆரும் அறிகிலார் — திருமந்திரம்',
        'desc': 'திருவாசகம், தேவாரம், திருமந்திரம், சிவபுராணம் மற்றும் தியான இசைப் பெருவெளி (172 பாடல்கள் & திரைப்படங்கள்)',
        'category_keys': ['shiva'],
        'tag': 'சிவ தரிசனம்'
    },
    {
        'file': 'thirukkural.html',
        'title': 'திருக்குறள் — உலகப் பொதுமறை அறநெறி',
        'sub_en': 'Thirukkural — The Universal Ethical Foundation',
        'verse': 'அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு — திருக்குறள் 1',
        'desc': 'அனைத்து 133 அதிகாரங்களின் முழுத் திரைப்படங்கள் மற்றும் அதிகாரப் பாடல் வெளியீடுகள் (185 படைப்புகள்)',
        'category_keys': ['thirukkural'],
        'tag': 'அறநெறிப் பெருவெளி'
    },
    {
        'file': 'sanmargam.html',
        'title': 'சுத்த சன்மார்க்கம் & வள்ளலார் அருட்பெருஞ்சோதி',
        'sub_en': 'Suddha Sanmargam & Vallalar Grace',
        'verse': 'அருட்பெருஞ்சோதி அருட்பெருஞ்சோதி தனிப்பெருங்கருணை அருட்பெருஞ்சோதி — திருவருட்பா',
        'desc': 'ஜீவகாருண்ய ஒழுக்கம், அருட்பெருஞ்சோதி அகவல், திருவருட்பா மற்றும் தமிழ் மரபுப் பாடல்கள் (94 படைப்புகள்)',
        'category_keys': ['vallalar_cultural'],
        'tag': 'தனிப்பெருங்கருணை'
    },
    {
        'file': 'murugan.html',
        'title': 'முருக நெறி — ஞானவேல் & பக்தி யோகம்',
        'sub_en': 'Muruga Neri — Wisdom, Courage & Devotion',
        'verse': 'யாமிருக்க பயமேன்! உருவாய் அருவாய் உளதாய் இலதாய் மருவாய் மலராய் — கந்தர் அநுபூதி',
        'desc': 'கந்த சஷ்டி கவசம், திருப்புகழ், கந்தர் அநுபூதி மற்றும் கந்தர் அலங்காரம் (50 படைப்புகள்)',
        'category_keys': ['murugan'],
        'tag': 'ஞானவேல்'
    },
    {
        'file': 'sakthi.html',
        'title': 'சக்தி நெறி — அன்னையின் பேரருள் & போற்றிகள்',
        'sub_en': 'Sakthi Neri — Divine Motherhood & Grace',
        'verse': 'தனந்தரும் கல்வி தரும் ஒருநாளும் தளர்வறியா மனந்தரும் — அபிராமி அந்தாதி',
        'desc': 'அபிராமி அந்தாதி, 108 சரஸ்வதி/லக்ஷ்மி போற்றி, தாயே கருமாரி மற்றும் மங்களத் துதிகள் (22 படைப்புகள்)',
        'category_keys': ['amman'],
        'tag': 'அன்னை அருள்'
    },
    {
        'file': 'vinayagar.html',
        'title': 'முழுமுதற் கடவுள் விநாயகர் வழிபாடு',
        'sub_en': 'Lord Vinayagar — The Remover of All Obstacles',
        'verse': 'வாக்குண்டாம் நல்ல மனமுண்டாம் மாமலராள் நோக்குண்டாம் மேனி நுடங்காது — ஔவையார்',
        'desc': 'மகா கணேச பஞ்சரத்னம், கண நாதா ஓம், திகட சக்கர, பாலும் தெளிர் தேனும் (9 படைப்புகள்)',
        'category_keys': ['vinayagar'],
        'tag': 'முழுமுதற் கடவுள்'
    },
    {
        'file': 'vaishnava.html',
        'title': 'வைணவ நெறி — சரணாகதி & திருப்பாவைத் திருப்பதிகங்கள்',
        'sub_en': 'Vaishnava Neri — Absolute Surrender & Divine Love',
        'verse': 'வையத்து வாழ்வீர்காள் நாமும் நம் பாவைக்குச் செய்யும் கிரிசைகள் கேளீரோ — திருப்பாவை',
        'desc': 'திருப்பாவை, பெரியாழ்வார் திருமொழி தாலாட்டு, நமோ நாராயணம் மற்றும் நாம சங்கீர்த்தனம் (48 படைப்புகள்)',
        'category_keys': ['vishnu_krishna'],
        'tag': 'சரணாகதி'
    }
]

# Generate each category page
for pg in site_pages:
    items = []
    for k in pg['category_keys']:
        items.extend(catalog.get(k, []))
        
    html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{pg['title']} | Guru Kula Desam</title>
  <meta name="description" content="{pg['desc']}">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

  {build_header(pg['file'])}

  <main class="main-content">
    <div class="hero-banner">
      <div class="sacred-tag">ॐ {pg['tag']} ॐ</div>
      <h1>{pg['title']}</h1>
      <h2>{pg['sub_en']}</h2>
      <div class="verse-quote">"{pg['verse']}"</div>
      <p class="hero-desc">{pg['desc']}</p>
    </div>

    <div class="controls-panel">
      <div class="search-box">
        <input type="text" placeholder="பாடல்கள் & அதிகாரங்களை தேடுக... (Search by title or number)" oninput="onSearchInput(this.value)">
      </div>
      <div class="filter-actions">
        <button class="filter-btn active" id="filter-all" onclick="setTypeFilter('all')">அனைத்தும் (All)</button>
        <button class="filter-btn" id="filter-film" onclick="setTypeFilter('film')">🎬 படங்கள் (Films)</button>
        <button class="filter-btn" id="filter-audio" onclick="setTypeFilter('audio')">🎵 இசை (Audio)</button>
      </div>
      <div class="item-count-badge" id="itemCountBadge">காட்டப்படும் பாடல்கள்: {len(items)}</div>
    </div>

    <div class="cards-grid" id="cardsGrid"></div>
  </main>

  {build_player_modal()}
  {build_footer()}

  <script src="assets/js/main.js"></script>
  <script>
    const PAGE_ITEMS = {json.dumps(items, ensure_ascii=False)};
    initPage(PAGE_ITEMS);
  </script>
</body>
</html>"""

    with open(f"Site/{pg['file']}", 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated Site/{pg['file']}")

# 7. Generate Home Page (index.html)
home_html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>குரு குல தேசம் (Guru Kula Desam) — சைவ நெறி & உலகப் பொதுமறை இசைப் பெருவெளி</title>
  <meta name="description" content="580 பக்தி, ஆன்மீக, தத்துவ மற்றும் திருக்குறள் இசைத் திரைப்படங்கள். புதிய யுகத்திற்கான சைவ நெறி ஆன்மீக மறுமலர்ச்சி.">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

  {build_header('index.html')}

  <main class="main-content">
    <div class="hero-banner">
      <div class="sacred-tag">ॐ புதிய யுகத்திற்கான சைவ நெறி ॐ</div>
      <h1>குரு குல தேசம்</h1>
      <h2>Universal Spiritual Renaissance through Saiva Neri & Thirukkural</h2>
      <div class="verse-quote">"அன்பும் சிவமும் இரண்டென்பர் அறிவிலார்; அன்பே சிவமாவது ஆரும் அறிகிலார்" — திருமந்திரம்</div>
      <p class="hero-desc">
        உலகை அமைதி, அறநெறி மற்றும் இறைப்பேரின்பத்தில் திளைக்கச் செய்யும் 580 பக்தி, ஆன்மீக மற்றும் திருக்குறள் இசைப் படைப்புகளின் முழுமையான அதிகாரப்பூர்வ தளம்.
      </p>
    </div>

    <div class="philosophy-grid">
      <div class="philosophy-card" onclick="location.href='saiva-neri.html'" style="cursor: pointer;">
        <div class="card-icon">🔱</div>
        <h3>சைவ நெறி (172 பாடல்கள்)</h3>
        <p>மாணிக்கவாசகரின் திருவாசகம், அப்பர் தேவாரம், திருமூலர் திருமந்திரம், சிவபுராணம் மற்றும் தியான இசைப் பெருவெளி.</p>
        <span style="color: var(--gold); font-size: 0.85rem; font-weight: 700; margin-top: 10px; display: inline-block;">பார்வையிடுக ↗</span>
      </div>

      <div class="philosophy-card" onclick="location.href='thirukkural.html'" style="cursor: pointer;">
        <div class="card-icon">📜</div>
        <h3>திருக்குறள் அறநெறி (185 படைப்புகள்)</h3>
        <p>133 அதிகாரங்களின் முழுமையான சினிமா இசைத் திரைப்படங்கள் மற்றும் அதிகாரப் பாடல் வெளியீடுகளின் மாபெரும் தொகுப்பு.</p>
        <span style="color: var(--gold); font-size: 0.85rem; font-weight: 700; margin-top: 10px; display: inline-block;">பார்வையிடுக ↗</span>
      </div>

      <div class="philosophy-card" onclick="location.href='sanmargam.html'" style="cursor: pointer;">
        <div class="card-icon">✨</div>
        <h3>சுத்த சன்மார்க்கம் (94 பாடல்கள்)</h3>
        <p>வள்ளலார் அருளிய அருட்பெருஞ்சோதி அகவல், தனிப்பெருங்கருணை, திருவருட்பா மற்றும் தமிழ் பண்பாட்டு இசைப் பாடல்கள்.</p>
        <span style="color: var(--gold); font-size: 0.85rem; font-weight: 700; margin-top: 10px; display: inline-block;">பார்வையிடுக ↗</span>
      </div>

      <div class="philosophy-card" onclick="location.href='murugan.html'" style="cursor: pointer;">
        <div class="card-icon">⚡</div>
        <h3>முருக நெறி (50 பாடல்கள்)</h3>
        <p>கந்த சஷ்டி கவசம், அருணகிரிநாதரின் திருப்புகழ், கந்தர் அநுபூதி மற்றும் கந்தர் அலங்கார பக்திப் பெருவெளி.</p>
        <span style="color: var(--gold); font-size: 0.85rem; font-weight: 700; margin-top: 10px; display: inline-block;">பார்வையிடுக ↗</span>
      </div>

      <div class="philosophy-card" onclick="location.href='sakthi.html'" style="cursor: pointer;">
        <div class="card-icon">🌺</div>
        <h3>சக்தி நெறி (22 பாடல்கள்)</h3>
        <p>அபிராமி அந்தாதி, 108 சரஸ்வதி மற்றும் லக்ஷ்மி போற்றி, தாயே கருமாரி மங்கள பக்திப் பாடல்கள்.</p>
        <span style="color: var(--gold); font-size: 0.85rem; font-weight: 700; margin-top: 10px; display: inline-block;">பார்வையிடுக ↗</span>
      </div>

      <div class="philosophy-card" onclick="location.href='vaishnava.html'" style="cursor: pointer;">
        <div class="card-icon">🪷</div>
        <h3>வைணவ நெறி (48 பாடல்கள்)</h3>
        <p>ஆண்டாள் திருப்பாவை, பெரியாழ்வார் தாலாட்டு, தசாவதாரம் மற்றும் ஹரே கிருஷ்ணா நாம சங்கீர்த்தனம்.</p>
        <span style="color: var(--gold); font-size: 0.85rem; font-weight: 700; margin-top: 10px; display: inline-block;">பார்வையிடுக ↗</span>
      </div>
    </div>

    <div style="margin-top: 50px;">
      <h2 style="text-align: center; color: var(--gold-soft); margin-bottom: 20px;">முழுமையான இசைத் தேடல் (All 580 Works Explorer)</h2>
      <div class="controls-panel">
        <div class="search-box">
          <input type="text" placeholder="580 பாடல்களிலும் தேடுக... (Search all 580 titles)" oninput="onSearchInput(this.value)">
        </div>
        <div class="filter-actions">
          <button class="filter-btn active" id="filter-all" onclick="setTypeFilter('all')">அனைத்தும் (580)</button>
          <button class="filter-btn" id="filter-film" onclick="setTypeFilter('film')">🎬 படங்கள் (Films)</button>
          <button class="filter-btn" id="filter-audio" onclick="setTypeFilter('audio')">🎵 இசை (Audio)</button>
        </div>
        <div class="item-count-badge" id="itemCountBadge">காட்டப்படும் பாடல்கள்: 580</div>
      </div>
      <div class="cards-grid" id="cardsGrid"></div>
    </div>
  </main>

  {build_player_modal()}
  {build_footer()}

  <script src="assets/js/main.js"></script>
  <script>
    // Load all items for home page
    const ALL_ITEMS = {json.dumps([item for cat_list in catalog.values() for item in cat_list], ensure_ascii=False)};
    initPage(ALL_ITEMS);
  </script>
</body>
</html>"""

with open("Site/index.html", 'w', encoding='utf-8') as f:
    f.write(home_html)
print("Generated Site/index.html")

# 8. Generate About Page (about.html)
about_html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>தத்துவ தரிசனம் & எம்மைப் பற்றி | Guru Kula Desam</title>
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

  {build_header('about.html')}

  <main class="main-content" style="max-width: 900px;">
    <div class="hero-banner">
      <div class="sacred-tag">ॐ சைவ நெறி — புதிய யுக விடியல் ॐ</div>
      <h1>குரு குல தேசம் தத்துவ தரிசனம்</h1>
      <h2>Preparing the World for the New Age using Saiva Neri</h2>
      <div class="verse-quote">"யாதும் ஊரே யாவரும் கேளிர்; தீதும் நன்றும் பிறர்தர வாரா" — கணியன் பூங்குன்றனார்</div>
    </div>

    <div style="background: var(--bg-card); border: 1px solid var(--border-gold); border-radius: 18px; padding: 35px; line-height: 1.8; color: #d0d6e2; font-size: 1.05rem;">
      <h3 style="color: var(--gold-soft); font-size: 1.4rem; margin-bottom: 12px;">புதிய யுகத்திற்கான சைவ நெறி (Saiva Neri for the New Age)</h3>
      <p style="margin-bottom: 20px;">
        சைவ நெறி என்பது வெறுமனே ஒரு மதம் அல்ல; அது வாழ்வியல் தத்துவம், இயற்கை வழிபாடு, உலகளாவிய கருணை மற்றும் பரம்பொருளுடன் ஒன்றிணையும் ஆத்ம சாதனை. 
        "அன்பே சிவம்" என்ற திருமூலரின் பெருவாக்கே மனித குலத்தின் அடுத்த பரிணாம வளர்ச்சிக்கான அடித்தளம்.
      </p>

      <h3 style="color: var(--gold-soft); font-size: 1.4rem; margin-bottom: 12px;">ஐம்பெரும் நெறிமுறைகள் (The 5 Universal Pillars)</h3>
      <ul style="margin-left: 20px; margin-bottom: 25px;">
        <li style="margin-bottom: 10px;"><strong style="color: var(--gold);">1. அன்பே சிவம்:</strong> சக மனிதர்கள் மற்றும் அனைத்து உயிர்கள் மீதும் எல்லையற்ற அன்பு செலுத்துவதே இறை வழிபாடு.</li>
        <li style="margin-bottom: 10px;"><strong style="color: var(--gold);">2. திருக்குறள் வாழ்வியல்:</strong> தர்மம், நீதி, வாய்மை, பொறுமை, கல்லாமை தவிர்த்தல் மற்றும் நல்ல நட்பு ஆகிய உலகளாவிய ஒழுக்கங்கள்.</li>
        <li style="margin-bottom: 10px;"><strong style="color: var(--gold);">3. ஜீவகாருண்யம்:</strong> வள்ளலார் காட்டிய வழியில் உயிர்க்கொலை தவிர்த்து, பசித்திரு, தனித்திரு, விழித்திரு என்ற ஆன்ம நேய ஒருமைப்பாடு.</li>
        <li style="margin-bottom: 10px;"><strong style="color: var(--gold);">4. திருமுறை இசை யோகம்:</strong> திருவாசகம் மற்றும் தேவாரப் பதிகங்களை இசையோடு பாடி தியானிப்பதன் மூலம் மன அமைதியும் இறையனுபவமும் பெறுதல்.</li>
        <li style="margin-bottom: 10px;"><strong style="color: var(--gold);">5. யாவரும் கேளிர்:</strong> சாதி, மத, தேச பேதங்களை கடந்து உலக மக்கள் அனைவரும் ஒரே இறைவனின் குழந்தைகள் என்ற ஒருமைப்பாடு.</li>
      </ul>

      <h3 style="color: var(--gold-soft); font-size: 1.4rem; margin-bottom: 12px;">இசைத் தொகுப்பின் சிறப்பம்சங்கள்</h3>
      <p style="margin-bottom: 20px;">
        குரு குல தேசம் யூடியூப் தளத்தில் வெளியிடப்பட்டுள்ள 580 பாடல்கள் மற்றும் காணொளிகள் நவீன இசை, பக்தி தத்துவம் மற்றும் சினிமா கலைவடிவத்தை ஒன்றிணைத்து உருவாக்கப்பட்டுள்ளன.
      </p>

      <div style="text-align: center; margin-top: 30px;">
        <a href="https://www.youtube.com/@guru-kula-desam?sub_confirmation=1" target="_blank" class="yt-btn-header" style="display: inline-flex; font-size: 1rem; padding: 10px 24px;">
          ▶ Subscribe on YouTube (@guru-kula-desam)
        </a>
      </div>
    </div>
  </main>

  {build_player_modal()}
  {build_footer()}

  <script src="assets/js/main.js"></script>
</body>
</html>"""

with open("Site/about.html", 'w', encoding='utf-8') as f:
    f.write(about_html)
print("Generated Site/about.html")

print("\n--- Entire Site Built Successfully in Site/ ---")
