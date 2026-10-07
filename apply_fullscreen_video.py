import os
import re
import glob

print("=== Starting Fullscreen Video Maximization ===")

# --- 1. CSS UPGRADE ---
NEW_CSS_SNIPPET = """/* Modal Player - Expansive Cinema & Fullscreen Maximized Layout */
.player-modal {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.94);
  backdrop-filter: blur(14px);
  display: none;
  align-items: center;
  justify-content: center;
  padding: 10px;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.player-modal.active { display: flex; }

.player-modal-box {
  background: #07090f;
  border: 1px solid var(--border-gold-hover);
  border-radius: 14px;
  width: 100%;
  max-width: 96vw;
  max-height: 96vh;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
  scroll-behavior: smooth;
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.98), 0 0 50px rgba(212, 175, 55, 0.3);
  animation: modalScale 0.25s ease;
  position: relative;
  margin: auto;
}

.player-modal-box::-webkit-scrollbar {
  width: 10px;
}
.player-modal-box::-webkit-scrollbar-track {
  background: #04060a;
}
.player-modal-box::-webkit-scrollbar-thumb {
  background: rgba(212, 175, 55, 0.5);
  border-radius: 5px;
  border: 2px solid #04060a;
}
.player-modal-box::-webkit-scrollbar-thumb:hover {
  background: var(--gold);
}

@keyframes modalScale {
  from { opacity: 0; transform: scale(0.97); }
  to { opacity: 1; transform: scale(1); }
}

/* Sticky Modal Header at Top */
.modal-header {
  position: sticky;
  top: 0;
  z-index: 40;
  flex-shrink: 0;
  padding: 10px 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  background: #10141f;
  border-bottom: 1px solid var(--border-subtle);
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.7);
}

.modal-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--gold-soft);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 55%;
  letter-spacing: 0.01em;
}

.modal-header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.modal-fullscreen-btn,
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

.modal-fullscreen-btn:hover,
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

/* Maximized Video Frame - Uses Maximum Available Screen Height and Width */
.modal-iframe-wrapper {
  flex-shrink: 0;
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  height: min(78vh, calc(96vw * 9 / 16));
  max-height: 82vh;
  background: #000;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
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
  padding: 8px 16px;
  background: linear-gradient(90deg, rgba(212, 175, 55, 0.08), rgba(212, 175, 55, 0.22), rgba(212, 175, 55, 0.08));
  border-bottom: 1px solid rgba(212, 175, 55, 0.25);
  text-align: center;
  color: var(--gold-bright);
  font-size: 0.82rem;
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

/* Hardware Fullscreen & Theater Mode */
.player-modal-box.modal-theater-mode,
.player-modal-box:fullscreen {
  max-width: 100vw !important;
  width: 100vw !important;
  max-height: 100vh !important;
  height: 100vh !important;
  border-radius: 0 !important;
  border: none !important;
  margin: 0 !important;
  background: #000 !important;
}

.player-modal-box.modal-theater-mode .modal-iframe-wrapper,
.player-modal-box:fullscreen .modal-iframe-wrapper {
  height: calc(100vh - 90px) !important;
  max-height: calc(100vh - 90px) !important;
  aspect-ratio: auto !important;
}

/* Modal Details: Lyrics & Meaning Section */
.modal-details {
  flex-shrink: 0;
  padding: 24px 28px 40px;
  background: #07090f;
  color: #e0e4ef;
}"""

MOBILE_CSS_SNIPPET = """@media (max-width: 768px) {
  .player-modal {
    padding: 0 !important;
    align-items: flex-start !important;
  }
  .player-modal-box {
    max-width: 100vw !important;
    width: 100vw !important;
    max-height: 100vh !important;
    border-radius: 0 !important;
    border: none !important;
    margin: 0 !important;
  }
  .modal-iframe-wrapper {
    width: 100% !important;
    aspect-ratio: 16 / 9 !important;
    height: auto !important;
    min-height: 220px !important;
    max-height: none !important;
  }
  .modal-header {
    padding: 8px 12px !important;
  }
  .modal-title {
    max-width: 44% !important;
    font-size: 0.88rem !important;
  }
  .modal-fullscreen-btn,
  .modal-scroll-btn {
    padding: 4px 6px !important;
    font-size: 0.72rem !important;
  }
  .modal-close-btn {
    padding: 4px 8px !important;
    font-size: 0.75rem !important;
  }
  .modal-details {
    padding: 16px 14px 28px !important;
  }
}"""

css_paths = ['assets/css/style.css', 'docs/assets/css/style.css', 'site/assets/css/style.css']
for cp in css_paths:
    if os.path.exists(cp):
        with open(cp, 'r', encoding='utf-8') as fp:
            css_text = fp.read()
        
        # Replace the modal CSS block up to .modal-meta-row
        pat = re.compile(r'/\* Modal Player.*?(?=\.modal-meta-row)', re.DOTALL)
        if pat.search(css_text):
            css_text = pat.sub(NEW_CSS_SNIPPET + "\n\n", css_text)
            print(f"Replaced modal cinema CSS in {cp}")
        else:
            print(f"Pattern not found in {cp}")

        # Replace mobile media query for modal if present
        mob_pat = re.compile(r'@media \(max-width: 768px\) \{\s*\.player-modal\s*\{.*?\}\s*\}', re.DOTALL)
        if mob_pat.search(css_text):
            css_text = mob_pat.sub(MOBILE_CSS_SNIPPET, css_text)
            print(f"Replaced mobile media query in {cp}")

        with open(cp, 'w', encoding='utf-8') as fp:
            fp.write(css_text)
        print(f"Saved: {cp}")


# --- 2. JS UPGRADE: toggleModalFullscreen & Updated openPlayer ---
NEW_JS_FUNCTIONS = """function toggleModalFullscreen() {
  const modalBox = document.getElementById('playerModalBox') || document.querySelector('.player-modal-box');
  const btn = document.querySelector('.modal-fullscreen-btn');
  
  if (!document.fullscreenElement && !document.webkitFullscreenElement) {
    const target = modalBox || document.documentElement;
    if (target.requestFullscreen) {
      target.requestFullscreen().catch(() => {
        if (modalBox) modalBox.classList.toggle('modal-theater-mode');
      });
    } else if (target.webkitRequestFullscreen) {
      target.webkitRequestFullscreen();
    } else {
      if (modalBox) modalBox.classList.toggle('modal-theater-mode');
    }
    if (btn) btn.innerHTML = '⛶ இயல்பு (Exit)';
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen().catch(() => {});
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    }
    if (modalBox) modalBox.classList.remove('modal-theater-mode');
    if (btn) btn.innerHTML = '⛶ முழுத்திரை';
  }
}

document.addEventListener('fullscreenchange', function() {
  const btn = document.querySelector('.modal-fullscreen-btn');
  const modalBox = document.getElementById('playerModalBox') || document.querySelector('.player-modal-box');
  if (!document.fullscreenElement) {
    if (modalBox) modalBox.classList.remove('modal-theater-mode');
    if (btn) btn.innerHTML = '⛶ முழுத்திரை';
  } else {
    if (btn) btn.innerHTML = '⛶ இயல்பு (Exit)';
  }
});"""

js_paths = ['assets/js/main.js', 'docs/assets/js/main.js', 'site/assets/js/main.js']
for jp in js_paths:
    if os.path.exists(jp):
        with open(jp, 'r', encoding='utf-8') as fp:
            js_text = fp.read()
        
        # Add toggleModalFullscreen if not already in file
        if 'function toggleModalFullscreen()' not in js_text:
            # Add before scrollToModalDetails
            js_text = js_text.replace(
                'function scrollToModalDetails()',
                NEW_JS_FUNCTIONS + "\n\nfunction scrollToModalDetails()"
            )
            print(f"Added toggleModalFullscreen to {jp}")

        # Update createPlayerModalElement to include the fullscreen button
        js_text = re.sub(
            r'<div class="modal-header-actions">\s*<button type="button" class="modal-scroll-btn"',
            r'<div class="modal-header-actions">\n          <button type="button" class="modal-fullscreen-btn" onclick="toggleModalFullscreen()" title="முழுத்திரை (Fullscreen)">⛶ முழுத்திரை</button>\n          <button type="button" class="modal-scroll-btn"',
            js_text
        )

        # In closePlayer, exit fullscreen if active
        if 'if (document.fullscreenElement)' not in js_text:
            js_text = js_text.replace(
                'function closePlayer() {\n  const modal = document.getElementById(\'playerModal\');',
                'function closePlayer() {\n  if (document.fullscreenElement) { document.exitFullscreen().catch(() => {}); }\n  const modal = document.getElementById(\'playerModal\');'
            )

        with open(jp, 'w', encoding='utf-8') as fp:
            fp.write(js_text)
        print(f"Saved: {jp}")


# --- 3. HTML UPGRADE: Include Fullscreen button in player modal ---
NEW_MODAL_HTML = """  <div class="player-modal" id="playerModal" onclick="if(event.target === this) closePlayer()">
    <div class="player-modal-box" id="playerModalBox">
      <div class="modal-header">
        <div class="modal-title" id="modalTitle">Now Playing</div>
        <div class="modal-header-actions">
          <button type="button" class="modal-fullscreen-btn" onclick="toggleModalFullscreen()" title="முழுத்திரை (Toggle Fullscreen)">
            ⛶ முழுத்திரை
          </button>
          <button type="button" class="modal-scroll-btn" onclick="scrollToModalDetails()" title="வரிகளுக்குச் செல்க">
            📜 வரிகள் &amp; பொருள் ↓
          </button>
          <button type="button" class="modal-close-btn" onclick="closePlayer()" title="மூடுக">✕ மூடுக (Close)</button>
        </div>
      </div>
      <div class="modal-iframe-wrapper" id="modalIframeWrapper">
        <iframe id="modalIframe" src="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share; fullscreen" allowfullscreen></iframe>
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

print(f"Updating {len(html_files)} HTML files with fullscreen-enabled modal...")
for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as fp:
        content = fp.read()

    pattern = re.compile(
        r'<div class="player-modal"\s+id="playerModal"[^>]*>.*?</div>\s*</div>\s*</div>',
        re.DOTALL
    )
    if pattern.search(content):
        content = pattern.sub(NEW_MODAL_HTML, content)
        with open(hf, 'w', encoding='utf-8') as fp:
            fp.write(content)
        print(f"Updated HTML in: {hf}")

# Update generate_entire_site.py
if os.path.exists('generate_entire_site.py'):
    with open('generate_entire_site.py', 'r', encoding='utf-8') as fp:
        ges = fp.read()
    
    ges_pattern = re.compile(r'def build_player_modal\(\):\s*return """.*?"""', re.DOTALL)
    if ges_pattern.search(ges):
        ges = ges_pattern.sub(f'def build_player_modal():\n    return """{NEW_MODAL_HTML}\n"""', ges)
        with open('generate_entire_site.py', 'w', encoding='utf-8') as fp:
            fp.write(ges)
        print("Updated generate_entire_site.py build_player_modal()")

print("=== Fullscreen Video Maximization Complete ===")
