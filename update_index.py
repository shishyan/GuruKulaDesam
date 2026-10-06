import json
from update_style import build_header, build_footer, build_player_modal

with open('Site/assets/data/catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Build deep homepage
home_html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>குரு குல தேசம் (Guru Kula Desam) — வேத & சைவ நெறி உலகளாவிய ஆன்மீக தளம்</title>
  <meta name="description" content="வேதங்கள், காஞ்சி மகா பெரியவா அருளுரைகள், Shaivam.org பன்னிரு திருமுறைகள் மற்றும் 580 இசைத் திரைப்படங்களின் முழுமையான அதிகாரப்பூர்வ களஞ்சியம்.">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

  {build_header('index.html')}

  <main class="main-content">
    <div class="hero-banner">
      <div class="sacred-tag">ॐ புதிய யுகத்திற்கான சைவ நெறி ஆன்மீக மறுமலர்ச்சி ॐ</div>
      <h1>குரு குல தேசம்</h1>
      <h2>Global Spiritual Renaissance through Vedic Wisdom, Saiva Neri & Thirukkural</h2>
      <div class="verse-quote">"அன்பும் சிவமும் இரண்டென்பர் அறிவிலார்; அன்பே சிவமாவது ஆரும் அறிகிலார்" — திருமந்திரம்</div>
      <p class="hero-desc">
        வேதங்களின் சாரம், பன்னிரு திருமுறைகள், சைவ சித்தாந்த சாத்திரங்கள், காஞ்சி மகா பெரியவா அருளிய 'தெய்வத்தின் குரல்' மற்றும் வள்ளலார் பெருமானின் சுத்த சன்மார்க்க வழிகாட்டலில் உலகை நல்வழிப்படுத்தும் 580 பக்தி, ஆன்மீக, தத்துவ இசைப் படைப்புகளின் அதிகாரப்பூர்வ தளம்.
      </p>
    </div>

    <!-- Sacred Authority & Source Foundations -->
    <div class="scripture-study-section" style="margin-top: 20px;">
      <span class="source-badge">வேத, திருமுறை & பெரியவா தத்துவ சங்கமம்</span>
      <h2>புதிய யுகத்தில் ஆன்ம விழிப்புணர்வு (The New Age Paradigm)</h2>
      <p>
        உலக நாகரிகம் பொருள்முதல்வாதத்தில் மூழ்கித் தவிக்கும் இக்காலகட்டத்தில், மனிதகுலத்தின் உள்ளொளியை மீட்கும் மகாசக்தியாக விளங்குவது நமது <strong>வேத நெறியும், தமிழ் சைவப் பெருநெறியும்</strong> ஆகும்.
      </p>

      <div class="canonical-grid">
        <div class="canonical-card" onclick="location.href='saiva-neri.html'" style="cursor: pointer;">
          <h4>🔱 சைவ நெறி (Shaivam.org)</h4>
          <p>ஸ்ரீ ருத்ரம், அப்பர் தேவாரம், மாணிக்கவாசகர் திருவாசகம், திருமூலர் திருமந்திரம் — 172 சிவத் திருப்பதிகங்கள்.</p>
          <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">ஆராய்ச்சி & பாடல்கள் ↗</span>
        </div>

        <div class="canonical-card" onclick="location.href='thirukkural.html'" style="cursor: pointer;">
          <h4>📜 திருக்குறள் உலக தர்மம்</h4>
          <p>சாதி, மதம் கடந்த உலகப் பொதுமறை. 133 அதிகாரங்களின் சினிமா இசைத் திரைப்படங்கள் மற்றும் அதிகார வெளியீடுகள் (185 படைப்புகள்).</p>
          <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">அறநெறிக் களஞ்சியம் ↗</span>
        </div>

        <div class="canonical-card" onclick="location.href='sanmargam.html'" style="cursor: pointer;">
          <h4>✨ சுத்த சன்மார்க்கம் (வள்ளலார்)</h4>
          <p>ஜீவகாருண்யம், அருட்பெருஞ்சோதி அகவல், தனிப்பெருங்கருணை மற்றும் ஆன்மநேய ஒருமைப்பாடு (94 படைப்புகள்).</p>
          <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">ஜோதி தரிசனம் ↗</span>
        </div>

        <div class="canonical-card" onclick="location.href='about.html'" style="cursor: pointer;">
          <h4>⚜️ தெய்வத்தின் குரல் (மகா பெரியவா)</h4>
          <p>காஞ்சி முனிவர் அருளிய சனாதன தர்மம், சிவ-விஷ்ணு ஐக்கியம், கோசம்ரக்ஷணம் மற்றும் மன அமைதிக்கான சாதனை நெறி.</p>
          <span style="color: var(--gold); font-size: 0.8rem; font-weight: 700; margin-top: 6px; display: inline-block;">தத்துவ தரிசனம் ↗</span>
        </div>
      </div>
    </div>

    <!-- Full 580 Music Catalog Section -->
    <h2 class="section-divider-title">முழுமையான இசைத் தேடல் (All 580 Works Explorer)</h2>

    <div class="controls-panel">
      <div class="search-box">
        <input type="text" placeholder="580 பாடல்கள் & அதிகாரங்களிலும் தேடுக... (Search across all 580 works)" oninput="onSearchInput(this.value)">
      </div>
      <div class="filter-actions">
        <button class="filter-btn active" id="filter-all" onclick="setTypeFilter('all')">அனைத்தும் (580)</button>
        <button class="filter-btn" id="filter-film" onclick="setTypeFilter('film')">🎬 படங்கள் (Films)</button>
        <button class="filter-btn" id="filter-audio" onclick="setTypeFilter('audio')">🎵 இசை (Audio)</button>
      </div>
      <div class="item-count-badge" id="itemCountBadge">காட்டப்படும் பாடல்கள்: 580</div>
    </div>

    <div class="cards-grid" id="cardsGrid"></div>
  </main>

  {build_player_modal()}
  {build_footer()}

  <script src="assets/js/main.js"></script>
  <script>
    const ALL_ITEMS = {json.dumps([item for cat_list in catalog.values() for item in cat_list], ensure_ascii=False)};
    initPage(ALL_ITEMS);
  </script>
</body>
</html>"""

with open('Site/index.html', 'w', encoding='utf-8') as f:
    f.write(home_html)
with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(home_html)

print("Updated Site/index.html and docs/index.html with deep Vedic & Periyava content!")
