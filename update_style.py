import json
import os

with open('Site/assets/data/catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Navigation configuration
nav_links = [
    ('index.html', 'முகப்பு (Home)'),
    ('saiva-neri.html', 'சைவ நெறி (Shaivam)'),
    ('thirukkural.html', 'திருக்குறள் (Kural)'),
    ('sanmargam.html', 'சன்மார்க்கம் (Vallalar)'),
    ('murugan.html', 'முருகன் (Kaumaram)'),
    ('sakthi.html', 'சக்தி (Shaktham)'),
    ('vinayagar.html', 'விநாயகர் (Ganapathyam)'),
    ('vaishnava.html', 'வைணவம் (Vaishnavam)'),
    ('about.html', 'வேத & பெரியவா தரிசனம்')
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
          <span>Guru Kula Desam • வேத & சைவ நெறி</span>
        </div>
      </a>
      <button class="mobile-toggle" onclick="toggleMobileNav()">☰</button>
      <nav class="main-nav" id="mainNav">
        {links_html}
        <a href="https://www.youtube.com/@guru-kula-desam?sub_confirmation=1" target="_blank" class="yt-btn-header">
          ▶ YouTube Channel
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
        <p>வேதங்கள், பன்னிரு திருமுறைகள், சைவ சித்தாந்த சாத்திரங்கள், காஞ்சி மகா பெரியவா அருளுரைகள் மற்றும் வள்ளலார் பெருமானின் சுத்த சன்மார்க்க நெறிகளை உலகிற்கு பறைசாற்றும் ஆன்மீக இசைப் பெருவெளி.</p>
        <p style="margin-top: 10px; color: var(--gold); font-weight: 600;">அன்பே சிவம் • யாதும் ஊரே யாவரும் கேளிர் • ஏகன் அநேகன்</p>
      </div>
      <div class="footer-col">
        <h4>புனித நூல்கள் & ஆதாரங்கள்</h4>
        <ul class="footer-links">
          <li><a href="https://shaivam.org" target="_blank">Shaivam.org — பன்னிரு திருமுறைகள் & சைவ சித்தாந்தம்</a></li>
          <li><a href="about.html">தெய்வத்தின் குரல் — காஞ்சி மகா பெரியவா அருளுரைகள்</a></li>
          <li><a href="thirukkural.html">திருக்குறள் — உலகப் பொதுமறை அறவழிகாட்டல்</a></li>
          <li><a href="sanmargam.html">திருவருட்பா — அருட்பெருஞ்சோதி அகவல்</a></li>
          <li><a href="saiva-neri.html">ஸ்ரீ ருத்ரம், சமகம் & உபநிடதங்கள்</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>பக்தி & இசை வழிகள்</h4>
        <ul class="footer-links">
          <li><a href="saiva-neri.html">சிவ நெறி (172 திருமுறைப் பாடல்கள்)</a></li>
          <li><a href="thirukkural.html">திருக்குறள் (185 அதிகாரப் படங்கள் & இசை)</a></li>
          <li><a href="murugan.html">முருக நெறி (கந்த சஷ்டி & திருப்புகழ்)</a></li>
          <li><a href="sakthi.html">சக்தி நெறி (அபிராமி அந்தாதி & போற்றிகள்)</a></li>
          <li><a href="https://www.youtube.com/@guru-kula-desam" target="_blank">YouTube அதிகாரப்பூர்வ தளம்</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      &copy; 2026 குரு குல தேசம் (Guru Kula Desam) | gurukuladesam.com | அனைத்து உரிமைகளும் இறைப்பணிக்கே சமர்ப்பணம்.
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

# Additional CSS for rich textual content
rich_css_snippet = """
/* Sacred Text & Scholarly Content Sections */
.scripture-study-section {
  background: var(--bg-card);
  border: 1px solid var(--border-gold);
  border-radius: 18px;
  padding: 36px 32px;
  margin-bottom: 45px;
  backdrop-filter: blur(12px);
  box-shadow: 0 10px 35px rgba(0,0,0,0.5);
}

.scripture-study-section h2 {
  font-size: 1.8rem;
  color: var(--gold-soft);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.scripture-study-section h3 {
  font-size: 1.3rem;
  color: var(--gold-bright);
  margin: 24px 0 10px 0;
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
  padding-bottom: 6px;
}

.scripture-study-section p {
  color: #d2d8e4;
  font-size: 1.02rem;
  line-height: 1.8;
  margin-bottom: 16px;
}

.source-badge {
  display: inline-block;
  background: rgba(224, 159, 62, 0.15);
  border: 1px solid var(--amber);
  color: var(--gold-soft);
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 4px 12px;
  border-radius: 20px;
  margin-bottom: 12px;
  font-weight: 700;
}

.vedic-verse-box {
  background: rgba(0, 0, 0, 0.4);
  border-left: 4px solid var(--gold);
  border-radius: 0 12px 12px 0;
  padding: 18px 24px;
  margin: 20px 0;
  font-family: 'Mukta Malar', serif;
}

.vedic-verse-box .sanskrit {
  font-size: 1.15rem;
  color: #fff;
  font-weight: 600;
  margin-bottom: 8px;
  letter-spacing: 0.02em;
}

.vedic-verse-box .tamil {
  font-size: 1.05rem;
  color: var(--gold-soft);
  margin-bottom: 8px;
  line-height: 1.6;
}

.vedic-verse-box .meaning {
  font-size: 0.92rem;
  color: var(--text-muted);
  font-style: italic;
  line-height: 1.5;
}

.periyava-quote-box {
  background: rgba(224, 159, 62, 0.07);
  border: 1px dashed rgba(224, 159, 62, 0.4);
  border-radius: 14px;
  padding: 22px 26px;
  margin: 24px 0;
}

.periyava-quote-box .quote-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  color: var(--amber);
  margin-bottom: 10px;
  font-size: 1.05rem;
}

.periyava-quote-box p {
  color: #e5e8f0;
  font-size: 1rem;
  line-height: 1.75;
  margin-bottom: 8px;
}

.canonical-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
  margin: 22px 0;
}

.canonical-card {
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  padding: 16px 20px;
}

.canonical-card h4 {
  color: var(--gold);
  font-size: 1.05rem;
  margin-bottom: 6px;
}

.canonical-card p {
  font-size: 0.88rem;
  color: var(--text-muted);
  line-height: 1.5;
  margin-bottom: 0;
}

.section-divider-title {
  text-align: center;
  font-size: 1.8rem;
  color: var(--gold-soft);
  margin: 45px 0 20px 0;
  position: relative;
}

.section-divider-title::before, .section-divider-title::after {
  content: "";
  display: inline-block;
  width: 60px;
  height: 1px;
  background: var(--gold);
  vertical-align: middle;
  margin: 0 15px;
  opacity: 0.6;
}
"""

with open('Site/assets/css/style.css', 'a', encoding='utf-8') as f:
    f.write("\n" + rich_css_snippet)

print("Appended rich text styles to Site/assets/css/style.css")
