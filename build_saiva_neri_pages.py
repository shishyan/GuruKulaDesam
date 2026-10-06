import json
import os

with open('site_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Definitions of pages tailored for Saiva Neri and the New Age
pages_config = [
    {
        'id': 'saiva_neri',
        'file': 'embed_saiva_neri.html',
        'title_ta': 'சைவ நெறி — புதிய யுகத்திற்கான ஆன்மீக ஒளி',
        'title_en': 'Saiva Neri — Spiritual Light for the New Age',
        'verse': 'அன்பும் சிவமும் இரண்டென்பர் அறிவிலார் | அன்பே சிவமாவது ஆரும் அறிகிலார் — திருமூலர் திருமந்திரம்',
        'subtitle': 'திருவாசகம், தேவாரம், திருமந்திரம், சிவபுராணம் மற்றும் தியான இசைப் பெருவெளி (172 பாடல்கள் & திரைப்படங்கள்)',
        'category_keys': ['shiva'],
        'accent_color': '#e09f3e'
    },
    {
        'id': 'thirukkural',
        'file': 'embed_thirukkural.html',
        'title_ta': 'திருக்குறள் — உலகப் பொதுமறை அறநெறி',
        'title_en': 'Thirukkural — The Universal Ethical Foundation',
        'verse': 'அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு — குறள் 1',
        'subtitle': 'அனைத்து 133 அதிகாரங்களின் திரைப்படங்கள் மற்றும் அதிகாரப் பாடல் வெளியீடுகள் (185 படைப்புகள்)',
        'category_keys': ['thirukkural'],
        'accent_color': '#d4af37'
    },
    {
        'id': 'vallalar_sanmargam',
        'file': 'embed_vallalar_sanmargam.html',
        'title_ta': 'சுத்த சன்மார்க்கம் & வள்ளலார் அருட்பெருஞ்சோதி',
        'title_en': 'Suddha Sanmargam & Vallalar Grace',
        'verse': 'அருட்பெருஞ்சோதி அருட்பெருஞ்சோதி தனிப்பெருங்கருணை அருட்பெருஞ்சோதி — திருவருட்பா',
        'subtitle': 'ஜீவகாருண்ய ஒழுக்கம், அருட்பெருஞ்சோதி அகவல், திருவருட்பா மற்றும் தமிழ் மரபுப் பாடல்கள் (94 படைப்புகள்)',
        'category_keys': ['vallalar_cultural'],
        'accent_color': '#f4a261'
    },
    {
        'id': 'murugan',
        'file': 'embed_murugan.html',
        'title_ta': 'முருக நெறி — ஞானவேல் & பக்தி யோகம்',
        'title_en': 'Muruga Neri — Wisdom, Courage & Devotion',
        'verse': 'யாமிருக்க பயமேன்! உருவாய் அருவாய் உளதாய் இலதாய் மருவாய் மலராய் மணியாய் ஒளியாய் — கந்தர் அநுபூதி',
        'subtitle': 'கந்த சஷ்டி கவசம், திருப்புகழ், கந்தர் அநுபூதி மற்றும் கந்தர் அலங்காரம் (50 படைப்புகள்)',
        'category_keys': ['murugan'],
        'accent_color': '#e76f51'
    },
    {
        'id': 'amman',
        'file': 'embed_amman.html',
        'title_ta': 'சக்தி நெறி — அன்னையின் பேரருள் & போற்றிகள்',
        'title_en': 'Sakthi Neri — Divine Motherhood & Grace',
        'verse': 'தனந்தரும் கல்வி தரும் ஒருநாளும் தளர்வறியா மனந்தரும் — அபிராமி அந்தாதி',
        'subtitle': 'அபிராமி அந்தாதி, 108 சரஸ்வதி/லக்ஷ்மி போற்றி, தாயே கருமாரி மற்றும் மங்களத் துதிகள் (22 படைப்புகள்)',
        'category_keys': ['amman'],
        'accent_color': '#f28482'
    },
    {
        'id': 'vinayagar',
        'file': 'embed_vinayagar.html',
        'title_ta': 'விநாயகர் வழிபாடு — முழுமுதற் கடவுள் & தடைகள் அகற்றும் அருள்',
        'title_en': 'Lord Vinayagar — The Remover of All Obstacles',
        'verse': 'வாக்குண்டாம் நல்ல மனமுண்டாம் மாமலராள் நோக்குண்டாம் மேனி நுடங்காது — ஔவையார்',
        'subtitle': 'மகா கணேச பஞ்சரத்னம், கண நாதா ஓம், திகட சக்கர, பாலும் தெளிர் தேனும் (9 படைப்புகள்)',
        'category_keys': ['vinayagar'],
        'accent_color': '#e9c46a'
    },
    {
        'id': 'vishnu_krishna',
        'file': 'embed_vishnu_krishna.html',
        'title_ta': 'வைணவ நெறி — சரணாகதி & திருப்பாவைத் திருப்பதிகங்கள்',
        'title_en': 'Vaishnava Neri — Absolute Surrender & Divine Love',
        'verse': 'வையத்து வாழ்வீர்காள் நாமும் நம் பாவைக்குச் செய்யும் கிரிசைகள் கேளீரோ — ஆண்டாள் திருப்பாவை',
        'subtitle': 'திருப்பாவை, பெரியாழ்வார் திருமொழி தாலாட்டு, நமோ நாராயணம் மற்றும் நாம சங்கீர்த்தனம் (48 படைப்புகள்)',
        'category_keys': ['vishnu_krishna'],
        'accent_color': '#2a9d8f'
    }
]

template = """<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>__PAGE_TITLE_TA__ | Guru Kula Desam</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Mukta+Malar:wght@400;500;600;700;800&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #090a0d;
      --card-bg: rgba(20, 23, 30, 0.75);
      --card-border: rgba(212, 175, 55, 0.22);
      --card-hover: rgba(212, 175, 55, 0.45);
      --accent: __ACCENT_COLOR__;
      --gold: #d4af37;
      --gold-bright: #ffd700;
      --gold-light: #fef5d1;
      --text-main: #f3f5f8;
      --text-muted: #a0a6b5;
      --badge-film: #e63946;
      --badge-audio: #2a9d8f;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Outfit', 'Mukta Malar', sans-serif;
      background-color: var(--bg);
      background-image: 
        radial-gradient(circle at 50% 0%, rgba(212, 175, 55, 0.08) 0%, transparent 60%),
        radial-gradient(circle at 10% 20%, rgba(224, 159, 62, 0.04) 0%, transparent 40%);
      color: var(--text-main);
      padding: 24px 20px 60px 20px;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }

    .banner {
      text-align: center;
      max-width: 960px;
      margin: 0 auto 30px auto;
      padding: 30px 20px 20px 20px;
      position: relative;
    }

    .sacred-emblem {
      font-size: 2.2rem;
      margin-bottom: 12px;
      filter: drop-shadow(0 0 12px rgba(212, 175, 55, 0.6));
      color: var(--gold-bright);
    }

    .banner h1 {
      font-size: 2.3rem;
      font-weight: 800;
      color: var(--gold-light);
      text-shadow: 0 0 25px rgba(212, 175, 55, 0.35);
      margin-bottom: 8px;
      letter-spacing: -0.01em;
    }

    .banner .sub-en {
      font-size: 1.1rem;
      color: var(--accent);
      font-weight: 500;
      margin-bottom: 14px;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    .verse-box {
      display: inline-block;
      background: rgba(212, 175, 55, 0.07);
      border-left: 3px solid var(--accent);
      border-right: 3px solid var(--accent);
      padding: 10px 24px;
      border-radius: 8px;
      margin: 10px auto 16px auto;
      font-size: 0.98rem;
      color: #e6dfcf;
      font-style: italic;
      font-family: 'Mukta Malar', serif;
      line-height: 1.6;
      box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    .banner p.description {
      color: var(--text-muted);
      font-size: 0.95rem;
      max-width: 780px;
      margin: 0 auto;
      line-height: 1.5;
    }

    /* Video Player */
    .player-container {
      max-width: 960px;
      margin: 0 auto 35px auto;
      background: #000;
      border-radius: 18px;
      overflow: hidden;
      border: 1px solid var(--card-hover);
      box-shadow: 0 15px 40px rgba(0,0,0,0.7), 0 0 25px rgba(212, 175, 55, 0.15);
      display: none;
      animation: fadeIn 0.3s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .player-container.active { display: block; }

    .player-wrapper {
      position: relative;
      padding-bottom: 56.25%;
      height: 0;
    }

    .player-wrapper iframe {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      border: none;
    }

    .player-meta {
      padding: 14px 22px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #11141a;
      border-top: 1px solid rgba(255,255,255,0.08);
    }

    .player-title {
      font-size: 1.05rem;
      font-weight: 600;
      color: var(--gold-light);
    }

    .close-btn {
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.2);
      color: #fff;
      padding: 6px 14px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.85rem;
      transition: background 0.2s;
    }

    .close-btn:hover { background: rgba(255,255,255,0.2); }

    /* Controls Bar */
    .controls {
      max-width: 1300px;
      margin: 0 auto 30px auto;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .filters-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      justify-content: space-between;
      align-items: center;
      background: rgba(20, 23, 30, 0.6);
      padding: 12px 18px;
      border-radius: 14px;
      border: 1px solid rgba(255,255,255,0.06);
    }

    .search-input {
      flex: 1;
      min-width: 280px;
      max-width: 500px;
      padding: 11px 18px;
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.14);
      border-radius: 30px;
      color: #fff;
      font-size: 0.95rem;
      outline: none;
      font-family: inherit;
      transition: border-color 0.2s, box-shadow 0.2s;
    }

    .search-input:focus {
      border-color: var(--gold);
      box-shadow: 0 0 12px rgba(212, 175, 55, 0.25);
    }

    .type-filters {
      display: flex;
      gap: 8px;
    }

    .type-btn {
      padding: 8px 16px;
      border-radius: 20px;
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.12);
      color: var(--text-muted);
      font-size: 0.85rem;
      font-weight: 500;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.2s;
    }

    .type-btn:hover {
      color: #fff;
      border-color: rgba(255,255,255,0.3);
    }

    .type-btn.active {
      background: var(--gold);
      color: #0b0d10;
      border-color: var(--gold);
      font-weight: 700;
    }

    .stats-bar {
      font-size: 0.88rem;
      color: var(--gold-light);
      font-weight: 600;
    }

    /* Grid */
    .media-grid {
      max-width: 1300px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
      gap: 20px;
    }

    .media-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      overflow: hidden;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
      backdrop-filter: blur(8px);
    }

    .media-card:hover {
      transform: translateY(-5px);
      border-color: var(--card-hover);
      box-shadow: 0 10px 28px rgba(212, 175, 55, 0.16);
    }

    .thumb-wrapper {
      position: relative;
      width: 100%;
      padding-bottom: 56.25%;
      background: #14171d;
      overflow: hidden;
    }

    .thumb-wrapper img {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.35s ease;
    }

    .media-card:hover .thumb-wrapper img {
      transform: scale(1.05);
    }

    .badge {
      position: absolute;
      top: 10px;
      right: 10px;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      padding: 3px 9px;
      border-radius: 6px;
      color: #fff;
      box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    }

    .badge-film { background: var(--badge-film); }
    .badge-audio { background: var(--badge-audio); }

    .play-overlay {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 48px;
      height: 48px;
      background: rgba(0,0,0,0.68);
      border: 2px solid var(--gold);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--gold-bright);
      font-size: 1.2rem;
      opacity: 0;
      transition: opacity 0.2s ease, transform 0.2s ease;
      box-shadow: 0 0 16px rgba(212, 175, 55, 0.4);
    }

    .media-card:hover .play-overlay {
      opacity: 1;
      transform: translate(-50%, -50%) scale(1.08);
    }

    .card-info {
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
      justify-content: space-between;
    }

    .card-title {
      font-size: 0.94rem;
      font-weight: 600;
      line-height: 1.45;
      color: var(--text-main);
      margin-bottom: 10px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .card-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.76rem;
      color: var(--text-muted);
      border-top: 1px solid rgba(255,255,255,0.06);
      padding-top: 8px;
    }

    .card-meta span.tag {
      color: var(--gold);
      font-weight: 600;
    }
  </style>
</head>
<body>

  <div class="banner">
    <div class="sacred-emblem">ॐ சிவாய நம ஓம்</div>
    <h1>__PAGE_TITLE_TA__</h1>
    <div class="sub-en">__PAGE_TITLE_EN__</div>
    <div class="verse-box">"__VERSE__"</div>
    <p class="description">__SUBTITLE__</p>
  </div>

  <div class="player-container" id="playerContainer">
    <div class="player-wrapper">
      <iframe id="videoIframe" src="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>
    <div class="player-meta">
      <div class="player-title" id="playerTitle">Now Playing</div>
      <button class="close-btn" onclick="closePlayer()">✕ Close</button>
    </div>
  </div>

  <div class="controls">
    <div class="filters-bar">
      <input type="text" class="search-input" id="searchInput" placeholder="பாடல்கள் & அதிகாரங்களை தேடுக... (Search by title, number, or keyword)" oninput="filterMedia()">
      <div class="type-filters">
        <button class="type-btn active" id="typeAll" onclick="setTypeFilter('all')">அனைத்தும் (All)</button>
        <button class="type-btn" id="typeFilm" onclick="setTypeFilter('film')">🎬 படங்கள் (Films)</button>
        <button class="type-btn" id="typeAudio" onclick="setTypeFilter('audio')">🎵 இசை (Audio)</button>
      </div>
      <div class="stats-bar" id="statsBar">Loading...</div>
    </div>
  </div>

  <div class="media-grid" id="mediaGrid"></div>

  <script>
    const ITEMS = __ITEMS_DATA__;

    let currentType = 'all';
    let searchQuery = '';

    function getFilteredItems() {
      return ITEMS.filter(it => {
        if (currentType !== 'all' && it.type !== currentType) return false;
        if (searchQuery) {
          const q = searchQuery.toLowerCase();
          return it.title.toLowerCase().includes(q) || it.id.includes(q);
        }
        return true;
      });
    }

    function renderGrid() {
      const items = getFilteredItems();
      const grid = document.getElementById('mediaGrid');
      const stats = document.getElementById('statsBar');
      
      stats.innerText = `மொத்தம் ${items.length} பாடல்கள்`;
      
      if (items.length === 0) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 60px; color: #888; font-size: 1.1rem;">பொருத்தமான பாடல்கள் காணப்படவில்லை (No matching items found)</div>';
        return;
      }

      grid.innerHTML = items.map(it => `
        <div class="media-card" onclick="playVideo('${it.id}', '${it.title.replace(/'/g, "\\\\'")}')">
          <div class="thumb-wrapper">
            <img src="https://i.ytimg.com/vi/${it.id}/mqdefault.jpg" loading="lazy" alt="${it.title}">
            <span class="badge ${it.type === 'film' ? 'badge-film' : 'badge-audio'}">${it.type === 'film' ? 'Film' : 'Audio'}</span>
            <div class="play-overlay">▶</div>
          </div>
          <div class="card-info">
            <div class="card-title">${it.title}</div>
            <div class="card-meta">
              <span class="tag">${it.type === 'film' ? '🎬 Full Film' : '🎵 Official Release'}</span>
              <span>Watch on YouTube ↗</span>
            </div>
          </div>
        </div>
      `).join('');
    }

    function setTypeFilter(t) {
      currentType = t;
      document.querySelectorAll('.type-btn').forEach(btn => btn.classList.remove('active'));
      if (t === 'all') document.getElementById('typeAll').classList.add('active');
      if (t === 'film') document.getElementById('typeFilm').classList.add('active');
      if (t === 'audio') document.getElementById('typeAudio').classList.add('active');
      renderGrid();
    }

    function filterMedia() {
      searchQuery = document.getElementById('searchInput').value;
      renderGrid();
    }

    function playVideo(id, title) {
      const container = document.getElementById('playerContainer');
      const iframe = document.getElementById('videoIframe');
      const titleElem = document.getElementById('playerTitle');
      
      iframe.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1`;
      titleElem.innerText = title;
      container.classList.add('active');
      container.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function closePlayer() {
      const container = document.getElementById('playerContainer');
      const iframe = document.getElementById('videoIframe');
      iframe.src = '';
      container.classList.remove('active');
    }

    // Initial render
    renderGrid();
  </script>
</body>
</html>
"""

for page in pages_config:
    items = []
    for k in page['category_keys']:
        items.extend(catalog.get(k, []))
        
    page_html = template.replace('__PAGE_TITLE_TA__', page['title_ta'])
    page_html = page_html.replace('__PAGE_TITLE_EN__', page['title_en'])
    page_html = page_html.replace('__VERSE__', page['verse'])
    page_html = page_html.replace('__SUBTITLE__', page['subtitle'])
    page_html = page_html.replace('__ACCENT_COLOR__', page['accent_color'])
    page_html = page_html.replace('__ITEMS_DATA__', json.dumps(items, ensure_ascii=False))
    
    # Write to site/ and docs/
    filepath = os.path.join('site', page['file'])
    docs_path = os.path.join('docs', page['file'])
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(page_html)
    with open(docs_path, 'w', encoding='utf-8') as f:
        f.write(page_html)
        
    print(f"Generated {filepath} and {docs_path} ({len(items)} items)")

print("All dedicated spiritual pages generated successfully!")
