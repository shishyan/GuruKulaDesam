import os
import re
import glob

print("=== Starting Comprehensive Modal & Lyrics Scrollability Fix ===")

# --- 1. UPDATE CSS ---
css_paths = ['assets/css/style.css', 'docs/assets/css/style.css', 'site/assets/css/style.css']

NEW_MODAL_CSS = """/* Modal Player - Full-Height Smooth Scrollable Container */
.player-modal {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(12px);
  display: none;
  align-items: center;
  justify-content: center;
  padding: 20px;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.player-modal.active { display: flex; }

.player-modal-box {
  background: #0a0d14;
  border: 1px solid var(--border-gold-hover);
  border-radius: 16px;
  width: 100%;
  max-width: 980px;
  max-height: 92vh;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
  scroll-behavior: smooth;
  box-shadow: 0 25px 70px rgba(0, 0, 0, 0.95), 0 0 40px rgba(212, 175, 55, 0.25);
  animation: modalScale 0.25s ease;
  position: relative;
  margin: auto;
}

.player-modal-box::-webkit-scrollbar {
  width: 10px;
}
.player-modal-box::-webkit-scrollbar-track {
  background: #06080d;
}
.player-modal-box::-webkit-scrollbar-thumb {
  background: rgba(212, 175, 55, 0.45);
  border-radius: 5px;
  border: 2px solid #06080d;
}
.player-modal-box::-webkit-scrollbar-thumb:hover {
  background: var(--gold);
}

@keyframes modalScale {
  from { opacity: 0; transform: scale(0.96); }
  to { opacity: 1; transform: scale(1); }
}

/* Sticky Modal Header at Top */
.modal-header {
  position: sticky;
  top: 0;
  z-index: 40;
  flex-shrink: 0;
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  background: #121622;
  border-bottom: 1px solid var(--border-subtle);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
}

.modal-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--gold-soft);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 65%;
  letter-spacing: 0.01em;
}

.modal-header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.modal-scroll-btn {
  background: rgba(212, 175, 55, 0.16);
  border: 1px solid rgba(212, 175, 55, 0.45);
  color: var(--gold-bright);
  padding: 6px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: inherit;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.modal-scroll-btn:hover {
  background: rgba(212, 175, 55, 0.3);
  border-color: var(--gold);
  color: #fff;
  transform: translateY(-1px);
}

.modal-close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.22);
  color: #fff;
  padding: 6px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all 0.2s;
  white-space: nowrap;
  font-family: inherit;
}

.modal-close-btn:hover {
  background: rgba(255, 77, 77, 0.25);
  border-color: #ff6666;
  color: #ffcccc;
}

/* Video Frame */
.modal-iframe-wrapper {
  flex-shrink: 0;
  position: relative;
  padding-bottom: 56.25%; /* 16:9 ratio */
  height: 0;
  background: #000;
}

.modal-iframe-wrapper iframe {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  border: none;
}

/* Clickable Scroll Hint Bar */
.modal-scroll-hint {
  flex-shrink: 0;
  padding: 9px 18px;
  background: linear-gradient(90deg, rgba(212, 175, 55, 0.08), rgba(212, 175, 55, 0.22), rgba(212, 175, 55, 0.08));
  border-bottom: 1px solid rgba(212, 175, 55, 0.25);
  text-align: center;
  color: var(--gold-bright);
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: background 0.2s, color 0.2s;
  user-select: none;
}

.modal-scroll-hint:hover {
  background: rgba(212, 175, 55, 0.3);
  color: #ffffff;
}

/* Modal Details: Lyrics & Meaning Section */
.modal-details {
  flex-shrink: 0;
  padding: 24px 26px 36px;
  background: #0a0d14;
  color: #e0e4ef;
}

.modal-meta-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
}

.modal-meta-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.modal-meta-tag {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(212, 175, 55, 0.25);
  color: var(--gold-soft);
}

.modal-meta-tag strong {
  color: var(--gold-bright);
}

.modal-action-buttons {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.modal-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  font-family: inherit;
  transition: all 0.2s ease;
}

.modal-btn-yt {
  background: #cc0000;
  color: #fff;
  border: 1px solid #ff4d4d;
}

.modal-btn-yt:hover {
  background: #e60000;
  box-shadow: 0 0 12px rgba(255, 0, 0, 0.4);
  color: #fff;
}

.modal-btn-copy {
  background: rgba(212, 175, 55, 0.12);
  color: var(--gold-soft);
  border: 1px solid rgba(212, 175, 55, 0.35);
}

.modal-btn-copy:hover {
  background: rgba(212, 175, 55, 0.25);
  border-color: var(--gold);
  color: #fff;
}

.modal-content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

@media (max-width: 768px) {
  .modal-content-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

.modal-box {
  background: rgba(18, 22, 32, 0.85);
  border: 1px solid var(--border-gold);
  border-radius: 12px;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
}

.modal-box-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
}

.modal-box-icon {
  font-size: 1.1rem;
}

.modal-box-title {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--gold-bright);
}

.modal-box-body {
  flex-grow: 1;
  background: rgba(0, 0, 0, 0.35);
  padding: 14px 16px;
  border-radius: 8px;
}

.lyrics-body {
  font-family: 'Mukta Malar', serif;
  font-size: 1.05rem;
  line-height: 1.9;
  color: #f7f2de;
  border-left: 3px solid var(--gold);
  white-space: normal;
  word-break: break-word;
  user-select: text;
}

.meaning-body {
  font-size: 0.96rem;
  line-height: 1.8;
  color: #d8deeb;
  border-left: 3px solid #ff9933;
  user-select: text;
}

/* Modal Bottom Actions & Mobile Fixes */
.modal-bottom-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  margin-top: 28px;
  padding-top: 18px;
  border-top: 1px solid rgba(212, 175, 55, 0.2);
  flex-wrap: wrap;
}

.modal-btn-top {
  background: rgba(212, 175, 55, 0.14);
  color: var(--gold-soft);
  border: 1px solid rgba(212, 175, 55, 0.35);
}

.modal-btn-top:hover {
  background: rgba(212, 175, 55, 0.28);
  border-color: var(--gold);
  color: #fff;
}

.modal-btn-close-bottom {
  background: rgba(255, 255, 255, 0.1);
  color: #e0e4ef;
  border: 1px solid rgba(255, 255, 255, 0.25);
}

.modal-btn-close-bottom:hover {
  background: rgba(255, 77, 77, 0.2);
  border-color: #ff6666;
  color: #fff;
}

@media (max-width: 768px) {
  .player-modal {
    padding: 8px;
    align-items: flex-start;
  }
  .player-modal-box {
    max-height: 96vh;
    border-radius: 12px;
  }
  .modal-header {
    padding: 10px 14px;
  }
  .modal-title {
    max-width: 55%;
    font-size: 0.92rem;
  }
  .modal-scroll-btn {
    padding: 4px 8px;
    font-size: 0.74rem;
  }
  .modal-close-btn {
    padding: 5px 10px;
    font-size: 0.78rem;
  }
  .modal-details {
    padding: 16px 14px 28px;
  }
}"""

for cp in css_paths:
    if os.path.exists(cp):
        with open(cp, 'r', encoding='utf-8') as fp:
            css_text = fp.read()

        # Find block starting from /* Modal Player to /* Controls & Filters
        pattern = re.compile(r'/\* Modal Player.*?(?=/\* Controls & Filters)', re.DOTALL)
        if pattern.search(css_text):
            css_text = pattern.sub(NEW_MODAL_CSS + "\n\n", css_text)
            print(f"Replaced modal CSS section in {cp}")
        else:
            print(f"Pattern not found in {cp}, checking alternative")

        # In-card drawer max-height updates
        css_text = re.sub(
            r'(\.card-lyrics-drawer\s+\.drawer-lyrics-text\s*\{[^}]*max-height:\s*)\d+px;',
            r'\g<1>280px; overscroll-behavior: contain; -webkit-overflow-scrolling: touch;',
            css_text
        )
        css_text = re.sub(
            r'(\.card-lyrics-drawer\s+\.drawer-meaning-text\s*\{[^}]*max-height:\s*)\d+px;',
            r'\g<1>240px; overscroll-behavior: contain; -webkit-overflow-scrolling: touch;',
            css_text
        )

        with open(cp, 'w', encoding='utf-8') as fp:
            fp.write(css_text)
        print(f"Saved updated CSS: {cp}")


# --- 2. UPDATE JS IN main.js, docs/assets/js/main.js, site/assets/js/main.js ---
js_paths = ['assets/js/main.js', 'docs/assets/js/main.js', 'site/assets/js/main.js']

NEW_OPEN_PLAYER_JS = """function openPlayer(videoId, title) {
  let modal = document.getElementById('playerModal');
  let iframe = document.getElementById('modalIframe');
  let titleEl = document.getElementById('modalTitle');

  // If modal doesn't exist on page, create dynamically
  if (!modal) {
    modal = createPlayerModalElement();
    document.body.appendChild(modal);
    iframe = document.getElementById('modalIframe');
    titleEl = document.getElementById('modalTitle');
  }

  if (!iframe) return;

  iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1`;
  if (titleEl) titleEl.innerText = title;

  // Resolve item details
  let item = (window.GURUKULA_ITEMS_BY_ID && window.GURUKULA_ITEMS_BY_ID[videoId]) ||
             (window.pageItems && window.pageItems.find(x => x.id === videoId)) ||
             { id: videoId, title: title };
  item = enrichItem(item);

  // Render modal details section below the video
  let detailsEl = document.getElementById('modalDetails');
  if (!detailsEl) {
    detailsEl = document.createElement('div');
    detailsEl.id = 'modalDetails';
    detailsEl.className = 'modal-details';
    const box = document.getElementById('playerModalBox') || modal.querySelector('.player-modal-box');
    if (box) box.appendChild(detailsEl);
  }

  const safeTitle = escapeHtml(item.title || title);
  const safeAuthor = escapeHtml(item.author || '');
  const safeSource = escapeHtml(item.source || '');
  const formattedLyrics = item.lyrics ? escapeHtml(item.lyrics).replace(/\\n/g, '<br>') : 'இப்பாடலின் வரிகள் சேகரிக்கப்பட்டு வருகின்றன.';
  const safeMeaning = escapeHtml(item.meaning || 'இப்பாடலின் தத்துவப் பொருள் விளக்கம் சேகரிக்கப்பட்டு வருகிறது.');
  const rawLyrics = item.lyrics || '';

  detailsEl.innerHTML = `
    <div class="modal-meta-row">
      <div class="modal-meta-tags">
        <span class="modal-meta-tag badge-${item.type === 'film' ? 'film' : 'audio'}">
          ${item.type === 'film' ? '🎬 முழுப் படம் (Cinematic Film)' : '🎵 இசை வெளியீடு (Sacred Audio)'}
        </span>
        ${safeAuthor ? `<span class="modal-meta-tag">✍️ ஆசிரியர்: <strong>${safeAuthor}</strong></span>` : ''}
        ${safeSource ? `<span class="modal-meta-tag">📖 மூலம்: <strong>${safeSource}</strong></span>` : ''}
      </div>

      <div class="modal-action-buttons">
        <a href="https://www.youtube.com/watch?v=${videoId}" target="_blank" rel="noopener noreferrer" class="modal-btn modal-btn-yt">
          ▶ YouTube-ல் காண்க ↗
        </a>
        ${rawLyrics ? `
          <button type="button" class="modal-btn modal-btn-copy" onclick="copyLyricsText(this, ${JSON.stringify(rawLyrics)})">
            📋 வரிகளை நகலெடு
          </button>
        ` : ''}
      </div>
    </div>

    <div class="modal-content-grid">
      <div class="modal-box modal-lyrics-box">
        <div class="modal-box-header">
          <span class="modal-box-icon">📜</span>
          <h4 class="modal-box-title">பாடல் வரிகள் (Sacred Lyrics)</h4>
        </div>
        <div class="modal-box-body lyrics-body">${formattedLyrics}</div>
      </div>

      <div class="modal-box modal-meaning-box">
        <div class="modal-box-header">
          <span class="modal-box-icon">💡</span>
          <h4 class="modal-box-title">பொருள் விளக்கம் &amp; தத்துவம் (Spiritual Meaning)</h4>
        </div>
        <div class="modal-box-body meaning-body">${safeMeaning}</div>
      </div>
    </div>

    <div class="modal-bottom-actions">
      <button type="button" class="modal-btn modal-btn-top" onclick="scrollToModalTop()">
        ▲ காணொளிக்குத் திரும்புக (Back to Video)
      </button>
      <button type="button" class="modal-btn modal-btn-close-bottom" onclick="closePlayer()">
        ✕ மூடுக (Close Player)
      </button>
    </div>
  `;

  modal.classList.add('active');
  document.body.style.overflow = 'hidden';

  // Scroll modal box to top when opening
  const modalBox = document.getElementById('playerModalBox') || modal.querySelector('.player-modal-box');
  if (modalBox) {
    modalBox.scrollTop = 0;
  }
}

function scrollToModalDetails() {
  const details = document.getElementById('modalDetails');
  const box = document.getElementById('playerModalBox') || document.querySelector('.player-modal-box');
  if (details && box) {
    const topPos = details.offsetTop - 55;
    box.scrollTo({ top: Math.max(0, topPos), behavior: 'smooth' });
  }
}

function scrollToModalTop() {
  const box = document.getElementById('playerModalBox') || document.querySelector('.player-modal-box');
  if (box) {
    box.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

function createPlayerModalElement() {
  const modal = document.createElement('div');
  modal.className = 'player-modal';
  modal.id = 'playerModal';
  modal.onclick = function(e) { if (e.target === this) closePlayer(); };
  modal.innerHTML = `
    <div class="player-modal-box" id="playerModalBox">
      <div class="modal-header">
        <div class="modal-title" id="modalTitle">Now Playing</div>
        <div class="modal-header-actions">
          <button type="button" class="modal-scroll-btn" onclick="scrollToModalDetails()" title="வரிகளுக்குச் செல்க">
            📜 வரிகள் &amp; பொருள் ↓
          </button>
          <button type="button" class="modal-close-btn" onclick="closePlayer()" title="மூடுக">✕ மூடுக (Close)</button>
        </div>
      </div>
      <div class="modal-iframe-wrapper" id="modalIframeWrapper">
        <iframe id="modalIframe" src="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      </div>
      <div class="modal-scroll-hint" onclick="scrollToModalDetails()">
        <span>▼ கீழே பாடல் வரிகள் &amp; தத்துவப் பொருள் விளக்கம் (Scroll down for Lyrics &amp; Meaning) ▼</span>
      </div>
      <div class="modal-details" id="modalDetails"></div>
    </div>
  `;
  return modal;
}

// Global escape key listener
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closePlayer();
  }
});"""

for jp in js_paths:
    if os.path.exists(jp):
        with open(jp, 'r', encoding='utf-8') as fp:
            js_text = fp.read()

        # Find openPlayer function through closing of copyLyricsText or closePlayer
        pattern = re.compile(r'function openPlayer\(videoId,\s*title\)\s*\{.*?(?=function copyLyricsText)', re.DOTALL)
        if pattern.search(js_text):
            js_text = pattern.sub(NEW_OPEN_PLAYER_JS + "\n\n", js_text)
            print(f"Replaced openPlayer JS in {jp}")
        else:
            print(f"Pattern for openPlayer not found in {jp}")

        with open(jp, 'w', encoding='utf-8') as fp:
            fp.write(js_text)
        print(f"Saved updated JS: {jp}")


# --- 3. UPDATE HTML FILES ---
NEW_MODAL_HTML = """  <div class="player-modal" id="playerModal" onclick="if(event.target === this) closePlayer()">
    <div class="player-modal-box" id="playerModalBox">
      <div class="modal-header">
        <div class="modal-title" id="modalTitle">Now Playing</div>
        <div class="modal-header-actions">
          <button type="button" class="modal-scroll-btn" onclick="scrollToModalDetails()" title="வரிகளுக்குச் செல்க">
            📜 வரிகள் &amp; பொருள் ↓
          </button>
          <button type="button" class="modal-close-btn" onclick="closePlayer()" title="மூடுக">✕ மூடுக (Close)</button>
        </div>
      </div>
      <div class="modal-iframe-wrapper" id="modalIframeWrapper">
        <iframe id="modalIframe" src="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      </div>
      <div class="modal-scroll-hint" onclick="scrollToModalDetails()">
        <span>▼ கீழே பாடல் வரிகள் &amp; தத்துவப் பொருள் விளக்கம் (Scroll down for Lyrics &amp; Meaning) ▼</span>
      </div>
      <div class="modal-details" id="modalDetails"></div>
    </div>
  </div>"""

html_files = []
for pat in ['*.html', 'docs/*.html', 'site/*.html']:
    for f in glob.glob(pat):
        with open(f, 'r', encoding='utf-8') as fp:
            c = fp.read()
            if 'playerModal' in c:
                html_files.append(f)

print(f"Found {len(html_files)} HTML files containing playerModal.")

for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as fp:
        content = fp.read()

    # Regex replace old modal structure
    pattern = re.compile(
        r'<div class="player-modal"\s+id="playerModal"[^>]*>.*?</div>\s*</div>\s*</div>',
        re.DOTALL
    )
    if pattern.search(content):
        content = pattern.sub(NEW_MODAL_HTML, content)
        with open(hf, 'w', encoding='utf-8') as fp:
            fp.write(content)
        print(f"Updated HTML modal in: {hf}")
    else:
        print(f"Modal regex match failed for: {hf}")

# Also update generate_entire_site.py
if os.path.exists('generate_entire_site.py'):
    with open('generate_entire_site.py', 'r', encoding='utf-8') as fp:
        ges = fp.read()
    
    ges_pattern = re.compile(r'def build_player_modal\(\):\s*return """.*?"""', re.DOTALL)
    if ges_pattern.search(ges):
        ges = ges_pattern.sub(f'def build_player_modal():\n    return """{NEW_MODAL_HTML}\n"""', ges)
        with open('generate_entire_site.py', 'w', encoding='utf-8') as fp:
            fp.write(ges)
        print("Updated generate_entire_site.py build_player_modal()")

print("=== Modal & Lyrics Scrollability Fix Finished ===")
