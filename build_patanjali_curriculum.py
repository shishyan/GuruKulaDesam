# -*- coding: utf-8 -*-
"""
build_patanjali_curriculum.py
Generates the comprehensive Patanjali 7-Level Formal Curriculum,
Progression of Self-Realization Rating, Way of Life, Leading Life,
and Leaving Legacy framework in syllabus.html, then synchronizes
across root, site/, and docs/.
"""

import os
import shutil

def build_patanjali_html():
    css_block = '''
  <style>
    /* Patanjali 7-Level Framework Styles */
    .pat-framework-container {
      margin: 40px 0;
    }
    .pat-hero-banner {
      background: linear-gradient(135deg, rgba(8, 14, 26, 0.98) 0%, rgba(15, 23, 42, 0.95) 50%, rgba(13, 31, 56, 0.98) 100%);
      border: 1px solid rgba(212, 175, 55, 0.35);
      border-radius: 20px;
      padding: 36px 30px;
      margin-bottom: 30px;
      box-shadow: 0 16px 45px rgba(0, 0, 0, 0.65), 0 0 35px rgba(212, 175, 55, 0.1);
      position: relative;
      overflow: hidden;
    }
    .pat-hero-banner::after {
      content: "ॐ";
      position: absolute;
      right: 25px;
      top: -25px;
      font-size: 14rem;
      color: rgba(212, 175, 55, 0.03);
      font-family: serif;
      pointer-events: none;
    }
    .pat-filter-nav {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin: 24px 0 28px;
      justify-content: center;
    }
    .pat-pill-btn {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.14);
      color: #cbd5e1;
      padding: 8px 18px;
      border-radius: 20px;
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.25s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .pat-pill-btn:hover, .pat-pill-btn.active {
      background: rgba(212, 175, 55, 0.18);
      border-color: var(--gold, #d4af37);
      color: var(--gold-bright, #ffd700);
      box-shadow: 0 0 16px rgba(212, 175, 55, 0.2);
    }
    .pat-level-card {
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 18px;
      padding: 28px 30px;
      margin-bottom: 26px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      transition: all 0.25s ease;
    }
    .pat-level-card:hover {
      border-color: rgba(212, 175, 55, 0.5);
      box-shadow: 0 14px 35px rgba(0,0,0,0.65), 0 0 20px rgba(212, 175, 55, 0.1);
    }
    .pat-level-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      flex-wrap: wrap;
      gap: 14px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 16px;
      margin-bottom: 18px;
    }
    .pat-level-code-pill {
      font-family: monospace;
      font-size: 0.8rem;
      background: rgba(212, 175, 55, 0.15);
      color: var(--gold-bright, #ffd700);
      border: 1px solid rgba(212, 175, 55, 0.35);
      padding: 3px 10px;
      border-radius: 6px;
      font-weight: 700;
      letter-spacing: 0.5px;
    }
    .pat-rating-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      border-radius: 16px;
      font-size: 0.82rem;
      font-weight: 700;
      letter-spacing: 0.5px;
    }
    .pat-rating-badge.l1 { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.35); }
    .pat-rating-badge.l2 { background: rgba(45, 212, 191, 0.15); color: #2dd4bf; border: 1px solid rgba(45, 212, 191, 0.35); }
    .pat-rating-badge.l3 { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.35); }
    .pat-rating-badge.l4 { background: rgba(234, 179, 8, 0.15); color: #facc15; border: 1px solid rgba(234, 179, 8, 0.35); }
    .pat-rating-badge.l5 { background: rgba(249, 115, 22, 0.15); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.35); }
    .pat-rating-badge.l6 { background: rgba(236, 72, 153, 0.15); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.35); }
    .pat-rating-badge.l7 { background: rgba(212, 175, 55, 0.2); color: var(--gold-bright, #ffd700); border: 1px solid var(--gold, #d4af37); box-shadow: 0 0 12px rgba(212, 175, 55, 0.3); }

    .pat-level-title {
      font-size: 1.45rem;
      font-weight: 800;
      color: #ffffff;
      margin: 6px 0 4px;
    }
    .pat-level-sanskrit {
      color: var(--gold-soft, #f6e05e);
      font-size: 0.98rem;
      font-weight: 600;
    }
    .pat-sutra-quote {
      background: rgba(0, 0, 0, 0.35);
      border-left: 3px solid var(--gold);
      padding: 8px 14px;
      border-radius: 0 8px 8px 0;
      font-size: 0.85rem;
      color: #cbd5e1;
      font-style: italic;
      margin-top: 10px;
    }
    .pat-grid-4 {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
      gap: 16px;
      margin-top: 20px;
    }
    .pat-quadrant {
      background: rgba(0, 0, 0, 0.28);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 18px 20px;
      position: relative;
    }
    .pat-quadrant.curriculum { border-top: 3px solid #38bdf8; }
    .pat-quadrant.rating { border-top: 3px solid #2dd4bf; }
    .pat-quadrant.lifestyle { border-top: 3px solid #facc15; }
    .pat-quadrant.legacy { border-top: 3px solid #c084fc; }

    .pat-quadrant-title {
      font-size: 0.92rem;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .pat-quadrant-body {
      font-size: 0.86rem;
      color: #cbd5e1;
      line-height: 1.65;
    }
    .pat-quadrant-body ul {
      margin: 6px 0 0 16px;
      padding: 0;
    }
    .pat-quadrant-body li {
      margin-bottom: 4px;
    }

    /* Assessment Engine */
    .pat-assessment-box {
      background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(24, 38, 64, 0.95));
      border: 1px solid rgba(212, 175, 55, 0.4);
      border-radius: 18px;
      padding: 30px;
      margin: 40px 0;
      box-shadow: 0 12px 35px rgba(0,0,0,0.6);
    }
    .pat-q-item {
      background: rgba(0,0,0,0.3);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 10px;
      padding: 14px 18px;
      margin-bottom: 14px;
    }
    .pat-q-title {
      font-size: 0.92rem;
      font-weight: 700;
      color: #f1f5f9;
      margin-bottom: 8px;
    }
    .pat-q-radios {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      font-size: 0.82rem;
      color: #94a3b8;
    }
    .pat-q-radios label {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      cursor: pointer;
    }
    .pat-score-display {
      background: rgba(0,0,0,0.5);
      border: 1px solid var(--gold);
      border-radius: 14px;
      padding: 22px;
      text-align: center;
      margin-top: 20px;
      display: none;
    }
  </style>
'''

    content_html = '''
    <!-- ========================================== -->
    <!-- PATANJALI 7-LEVEL FORMAL CURRICULUM & SELF-REALIZATION PROGRESSION -->
    <!-- ========================================== -->
    <section class="pat-framework-container" id="patanjaliSyllabus">
      
      <!-- HERO BANNER -->
      <div class="pat-hero-banner">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px; flex-wrap:wrap;">
          <span style="background:rgba(212,175,55,0.18); color:var(--gold-bright, #ffd700); border:1px solid rgba(212,175,55,0.4); font-size:0.82rem; font-weight:800; text-transform:uppercase; letter-spacing:1px; padding:5px 14px; border-radius:20px;">
            🧘 பதஞ்சலி சப்த ஞான பூமிகை • The Sevenfold Patanjali Prajna Rule
          </span>
          <span style="color:#38bdf8; font-size:0.86rem; font-weight:600;">
            யோக சூத்திரம் 2.27 • யோக வாசிஷ்டம் • திருக்குறள் வாழ்வியல்
          </span>
        </div>

        <h2 style="color:#ffffff; font-size:2rem; font-weight:800; line-height:1.3; margin:0 0 14px 0;">
          பதஞ்சலி 7 படிநிலை முறைசார் பாடத்திட்டம் &amp; சுய-தரிசன ஆன்ம மதிப்பீடு
        </h2>
        <div style="font-family:'Mukta Malar', serif; font-size:1.15rem; color:var(--gold-soft, #f6e05e); font-style:italic; margin-bottom:14px; border-left:3px solid var(--gold); padding-left:14px;">
          "तस्य सप्तधा प्रान्तभूमिः प्रज्ञा" — பதஞ்சலி யோக சூத்திரம் (சாதன பாதம் 2.27)<br>
          <span style="font-size:0.92rem; color:#cbd5e1; font-style:normal;">பொருள்: விவேக ஞானத்தை வளர்க்கும் சாதகனுக்கு, மெய்யுணர்வின் (Prajna) விழிப்புணர்வு ஏழு முற்போக்கு படிநிலைகளில் (சப்த ஞான பூமிகைகளில்) படிப்படியாக மலர்கிறது.</span>
        </div>

        <p style="color:#e2e8f0; font-size:0.98rem; line-height:1.8; margin-bottom:20px;">
          குரு குல தேசம் வகுத்துள்ள இம்முறைசார் பாடத்திட்டம் வெறும் தேர்வுக்கான ஏட்டுக் கல்வி அல்ல. 
          <strong>1. முறைசார் பாடநெறி (Formal Curriculum), 2. சுய-தரிசன ஆன்ம மதிப்பீடு (Progression Rating: Level 1.0 to 7.0), 3. அன்றாட வாழ்வியல் நெறிமுறை (Way of Life), 4. நற்குடும்பத்தை வழிநடத்துதல் (Leading the Life), 5. தலைமுறைக்கான அழியாத அறக்கொடை (Leaving Legacy)</strong> ஆகிய ஐந்து பரிமாணங்களையும் உள்ளடக்கி, இல்லறத்தில் வாழ்ந்தே நிர்வாணம் (ஆன்ம முக்தி) அடையும் முழுமையான வாழ்வியல் வரைபடம்.
        </p>

        <!-- Quick Matrix Filter Pills -->
        <div class="pat-filter-nav">
          <button type="button" class="pat-pill-btn active" onclick="filterPatLevel('all')">📚 அனைத்து 7 படிநிலைகள்</button>
          <button type="button" class="pat-pill-btn" onclick="filterPatLevel('L1')">1. சுபேச்சை (1.0)</button>
          <button type="button" class="pat-pill-btn" onclick="filterPatLevel('L2')">2. விசாரணை (2.0)</button>
          <button type="button" class="pat-pill-btn" onclick="filterPatLevel('L3')">3. தனுமானசி (3.0)</button>
          <button type="button" class="pat-pill-btn" onclick="filterPatLevel('L4')">4. சத்துவாபத்தி (4.0)</button>
          <button type="button" class="pat-pill-btn" onclick="filterPatLevel('L5')">5. அசம்சக்தி (5.0)</button>
          <button type="button" class="pat-pill-btn" onclick="filterPatLevel('L6')">6. பதார்த்த பாவனை (6.0)</button>
          <button type="button" class="pat-pill-btn" onclick="filterPatLevel('L7')">7. துரியகா (7.0)</button>
        </div>
      </div>

      <!-- LEVEL 1 CARD -->
      <article class="pat-level-card" data-pat-level="L1" style="border-left: 5px solid #38bdf8;">
        <div class="pat-level-header">
          <div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="pat-level-code-pill">WBS: CUR-PAT-L1</span>
              <span class="pat-rating-badge l1">⭐️ சுய-தரிசன மதிப்பீடு: Level 1.0 / 7.0</span>
              <span style="font-size:0.75rem; color:#94a3b8;">பருவம்: பால பருவம் &amp; தொடக்க சாதனை</span>
            </div>
            <h3 class="pat-level-title">படிநிலை 1: சுபேச்சை (Śubhecchā) — அறநெறி நாட்டம் &amp; தர்ம விழிப்புணர்வு</h3>
            <div class="pat-level-sanskrit">The Noble Aspiration &amp; Moral Awakening to Dharma</div>
            <div class="pat-sutra-quote">
              "அவித்யா அஸ்மிதா ராகத்வேஷாபிநிவேசாஃ க்லேசாஃ" (YS 2.3) — உலக மயக்கத்தின் அநித்தியத்தை உணர்ந்து, அறவழியில் செல்லத் துடிக்கும் ஆத்ம தாகத்தின் முதல் விழிப்புணர்வு.
            </div>
          </div>
        </div>

        <div class="pat-grid-4">
          <div class="pat-quadrant curriculum">
            <div class="pat-quadrant-title"><span>📚</span> 1. முறைசார் பாடத்திட்டம் (Formal Curriculum)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>ஆத்திசூடி &amp; கொன்றை வேந்தன்</strong>: ஔவையாரின் அடிப்படை அறநெறிச் சூத்திரங்கள்.</li>
                <li><strong>திருக்குறள் பாயிரவியல்</strong>: கடவுள் வாழ்த்து, வான்சிறப்பு, நீத்தார் பெருமை, அறன் வலியுறுத்தல்.</li>
                <li><strong>எளிய பக்தி தோத்திரங்கள்</strong>: விநாயகர் அகவல், தேவாரம் முதல் திருமுறை பதிகங்கள்.</li>
                <li><strong>அடிப்படைப் பண்பாட்டியல்</strong>: பெரியாரைத் துணைக் கோடல், பொய் கூறாமை, திருடாமை.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant rating">
            <div class="pat-quadrant-title"><span>🔍</span> 2. சுய-தரிசன ஆன்ம மதிப்பீடு (Progression Rating)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>மதிப்பீடு</strong>: 1.0 / 7.0 (விழிப்படைந்த சாதகர் / Awakened Seeker).</li>
                <li><strong>மனோநிலை</strong>: உலக ஆசைகளின் மாயையை உணர்ந்து, நல்லவற்றின் மீது நாட்டம் கொள்ளுதல் (விருப்ப மாற்றம்).</li>
                <li><strong>அகந்தை நிலை (Ego Index)</strong>: பருவுடல் சார்ந்த அகந்தை இருந்தாலும், அதைக் கட்டுப்படுத்த வேண்டும் என்ற உணர்வு மலருதல்.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant lifestyle">
            <div class="pat-quadrant-title"><span>🌿</span> 3. அன்றாட வாழ்வியல் நெறிமுறை (Way of Life)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>விடியற்காலை ஆசாரம்</strong>: பிரம்ம முகூர்த்தத்தில் விழித்தல், உடல் தூய்மை, திருநீறு அணிதல்.</li>
                <li><strong>உணவு &amp; ஒழுக்கம்</strong>: சாத்விக சைவ உணவு, புலால் தவிர்த்தல், ஜீவகாருண்யம்.</li>
                <li><strong>அன்றாடக் கடமை</strong>: பெற்றோரிடம் ஆசி பெறுதல், ஆசிரியரை வணங்குதல், தினசரி 10 நிமிடம் இறை வழிபாடு.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant legacy">
            <div class="pat-quadrant-title"><span>🏡</span> 4. வாழ்வை நடத்துதலும் அறக்கொடையும் (Legacy)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>குடும்பப் பங்கு</strong>: பெற்றோரின் சொல் கேட்டு நடக்கும் கீழ்ப்படிதல் உள்ள நன்மகனாக/நன்மகளாகத் திகழ்தல்.</li>
                <li><strong>சமூகப் பழக்கம்</strong>: உடன்பிறந்தவர்கள், நண்பர்களிடம் பகிரும் (ஈகை) மனப்பான்மை.</li>
                <li><strong>தலைமுறை விதை</strong>: குடும்பத்தின் அடுத்த தலைமுறைக்கு ஒழுக்கத்தின் முதல் வித்தாக மாறுதல்.</li>
              </ul>
            </div>
          </div>
        </div>
      </article>

      <!-- LEVEL 2 CARD -->
      <article class="pat-level-card" data-pat-level="L2" style="border-left: 5px solid #2dd4bf;">
        <div class="pat-level-header">
          <div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="pat-level-code-pill">WBS: CUR-PAT-L2</span>
              <span class="pat-rating-badge l2">⭐️ சுய-தரிசன மதிப்பீடு: Level 2.0 / 7.0</span>
              <span style="font-size:0.75rem; color:#94a3b8;">பருவம்: மாணவப் பருவம் &amp; தத்துவப் பகுப்பாய்வு</span>
            </div>
            <h3 class="pat-level-title">படிநிலை 2: விசாரணை (Vicāraṇā) — சாத்திர ஆய்வு &amp; விவேகப் பகுத்தறிவு</h3>
            <div class="pat-level-sanskrit">Systematic Inquisitive Study &amp; Shastric Discrimination</div>
            <div class="pat-sutra-quote">
              "சுவாத்யாய ஈஸ்வரபிரணிதானானி" (YS 2.1) — "நான் யார்? எது நிலையானது? எது அழியக்கூடியது?" என்று சாத்திரங்கள் மூலமும் பெரியோர் உரை வழியும் ஆன்மாவை ஆராய்தல்.
            </div>
          </div>
        </div>

        <div class="pat-grid-4">
          <div class="pat-quadrant curriculum">
            <div class="pat-quadrant-title"><span>📚</span> 1. முறைசார் பாடத்திட்டம் (Formal Curriculum)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>தத்வ போதம் (சங்கரர்)</strong>: ஸ்தூல, சூக்ஷ்ம, காரண சரீரப் பகுப்பாய்வு; அவஸ்தா த்ரய விவேகம்.</li>
                <li><strong>திருக்குறள் இல்லறவியல் (1-10 அதிகாரங்கள்)</strong>: இல்வாழ்க்கை, வாழ்க்கைத்துணை நலம், புதல்வரைப் பெறுதல், அன்புடைமை, விருந்தோம்பல்.</li>
                <li><strong>சைவ சித்தாந்த முப்பொருள் உண்மை</strong>: பதி, பசு, பாசம்; ஆணவ, கன்ம, மாயா மும்மலங்கள்.</li>
                <li><strong>பதஞ்சலி அஷ்டாங்க யோகம்</strong>: யமம் (அஹிம்சை, சத்யம், அஸ்தேயம், பிரம்மச்சர்யம், அபரிக்கிரஹம்) &amp; நியமங்கள்.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant rating">
            <div class="pat-quadrant-title"><span>🔍</span> 2. சுய-தரிசன ஆன்ம மதிப்பீடு (Progression Rating)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>மதிப்பீடு</strong>: 2.0 / 7.0 (பகுத்தறியும் சாதகர் / Discerning Thinker).</li>
                <li><strong>மனோநிலை</strong>: எதையும் கண்மூடித்தனமாக ஏற்காமல், சாத்திர விவேகத்தோடு தர்மத்தின் உண்மையை உறுதிசெய்தல்.</li>
                <li><strong>அகந்தை நிலை (Ego Index)</strong>: அறிவு சார்ந்த அகந்தை (Intellectual Ego) தலைதூக்காமல், அடக்கத்துடன் சான்றோரை அணுகுதல்.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant lifestyle">
            <div class="pat-quadrant-title"><span>🌿</span> 3. அன்றாட வாழ்வியல் நெறிமுறை (Way of Life)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>சுவாத்யாயம்</strong>: தினமும் 30 நிமிடங்கள் சாத்திர நூல்களை ஆழமாக வாசித்தல் &amp; சிந்தித்தல் (மநனம்).</li>
                <li><strong>பஞ்ச யக்ஞ ஆரம்பம்</strong>: பிரம்ம யக்ஞம் (நூல் ஓதுதல்) மற்றும் தேவ யக்ஞம் (தீபாராதனை) செய்தல்.</li>
                <li><strong>பேச்சு &amp; குணம்</strong>: வீண் வம்புகளைத் தவிர்த்து, இனியவை கூறல், செய்ந்நன்றி மறவாமை.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant legacy">
            <div class="pat-quadrant-title"><span>🏡</span> 4. வாழ்வை நடத்துதலும் அறக்கொடையும் (Legacy)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>குடும்பத்தில் ஆக்கம்</strong>: குடும்ப உறுப்பினர்களிடையே அறிவுப்பூர்வமான விவாதங்களையும் ஆன்மீக நல்லிணக்கத்தையும் பேணுதல்.</li>
                <li><strong>திருமண பந்தத்திற்குத் தயார்</strong>: காமக் கவர்ச்சியைக் கடந்து, அறத்துணையாகிய வாழ்க்கைத்துணையைத் தேர்ந்தெடுக்கும் முதிர்ச்சி.</li>
                <li><strong>தலைமுறை விதை</strong>: படிப்பும் சிந்தனையும் உள்ள தலைமுறையாக குடும்பத்தை நிலைநிறுத்துதல்.</li>
              </ul>
            </div>
          </div>
        </div>
      </article>

      <!-- LEVEL 3 CARD -->
      <article class="pat-level-card" data-pat-level="L3" style="border-left: 5px solid #c084fc;">
        <div class="pat-level-header">
          <div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="pat-level-code-pill">WBS: CUR-PAT-L3</span>
              <span class="pat-rating-badge l3">⭐️ சுய-தரிசன மதிப்பீடு: Level 3.0 / 7.0</span>
              <span style="font-size:0.75rem; color:#94a3b8;">பருவம்: இளமை முதிர்ச்சி &amp; மனவடக்க சாதனை</span>
            </div>
            <h3 class="pat-level-title">படிநிலை 3: தனுமானசி (Tanumānasī) — மன அடக்கம் &amp; உணர்ச்சி மேலாண்மை</h3>
            <div class="pat-level-sanskrit">Subtlety of Mind, Emotional Mastery &amp; Ego-Thinning</div>
            <div class="pat-sutra-quote">
              "யோக சித்தவிருத்தி நிரோதஃ" (YS 1.2) — 'தனு' என்றால் மெல்லிய; அலைபாயும் மனதை மெல்லியதாக இழையோடச் செய்து, ஆசை, கோபம், காமத்தின் தீவிரத்தைக் குறைத்தல்.
            </div>
          </div>
        </div>

        <div class="pat-grid-4">
          <div class="pat-quadrant curriculum">
            <div class="pat-quadrant-title"><span>📚</span> 1. முறைசார் பாடத்திட்டம் (Formal Curriculum)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>பகவத் கீதை 2-ஆம் அத்தியாயம்</strong>: சாங்கிய யோகம், ஸ்திதப்பிரக்ஞன் இலக்கணம் (மனோ அமைதி).</li>
                <li><strong>விவேகசூடாமணி</strong>: ஆவரண-விக்ஷேப மாயா சக்திகள் &amp; மனோநாச உபாயங்கள்.</li>
                <li><strong>திருக்குறள் சினமின்மை &amp; அடக்கமுடைமை</strong>: வெகுளாமை, பொறையுடைமை, அழுக்காறாமை அதிகாரங்கள்.</li>
                <li><strong>நவீன உணர்வுநிலை அறிவியல்</strong>: பிராணாயாமமும் நரம்பியல் சமநிலையும் (Vagus Nerve Stimulation).</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant rating">
            <div class="pat-quadrant-title"><span>🔍</span> 2. சுய-தரிசன ஆன்ம மதிப்பீடு (Progression Rating)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>மதிப்பீடு</strong>: 3.0 / 7.0 (புலனடக்கிய சாதகர் / Sense-Restrained Seeker).</li>
                <li><strong>மனோநிலை</strong>: கோபமோ, அவசரமோ எழும்போது அதை உடனே கவனித்து சாந்தப்படுத்தும் விழிப்புணர்வு.</li>
                <li><strong>அகந்தை நிலை (Ego Index)</strong>: 'நான் பெரியவன்' என்ற தற்பெருமை உதிர்ந்து, உண்மையான பணிவு இயல்பாகுதல்.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant lifestyle">
            <div class="pat-quadrant-title"><span>🌿</span> 3. அன்றாட வாழ்வியல் நெறிமுறை (Way of Life)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>தியானப் பயிற்சி</strong>: தினமும் 20 நிமிடங்கள் சுவாச கவனிப்பு (பிராணாயாமம்) &amp; மௌனத் தியானம்.</li>
                <li><strong>மன்னிக்கும் ஆற்றல்</strong>: தனக்குத் தீங்கு செய்தவரையும் உடனே மன்னிக்கும் பேருள்ளம்.</li>
                <li><strong>மித வாழ்வு</strong>: தேவைகளைக் குறைத்துக் கொள்ளுதல், வீண் செலவு மற்றும் ஆடம்பர மோகத்தை நீக்குதல்.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant legacy">
            <div class="pat-quadrant-title"><span>🏡</span> 4. வாழ்வை நடத்துதலும் அறக்கொடையும் (Legacy)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>இல்லறத்தில் சினம் தவிர்த்தல்</strong>: மனைவி/கணவன், குழந்தைகளிடம் ஒருபோதும் ஆத்திரப்படாமல் சாந்தமாகப் பேசுதல்.</li>
                <li><strong>முரண்பாடுகளைத் தீர்த்தல்</strong>: குடும்பப் பிரச்சனைகளை தியாகத்தாலும் அன்பாலும் சரிசெய்தல்.</li>
                <li><strong>தலைமுறை விதை</strong>: சண்டை சச்சரவற்ற, ஆனந்தமான குடும்பச் சூழலை அடுத்த தலைமுறைக்கு வழங்குதல்.</li>
              </ul>
            </div>
          </div>
        </div>
      </article>

      <!-- LEVEL 4 CARD -->
      <article class="pat-level-card" data-pat-level="L4" style="border-left: 5px solid #facc15;">
        <div class="pat-level-header">
          <div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="pat-level-code-pill">WBS: CUR-PAT-L4</span>
              <span class="pat-rating-badge l4">⭐️ சுய-தரிசன மதிப்பீடு: Level 4.0 / 7.0</span>
              <span style="font-size:0.75rem; color:#94a3b8;">பருவம்: இல்லறத் தலைமை &amp; சத்துவ சான்றாண்மை</span>
            </div>
            <h3 class="pat-level-title">படிநிலை 4: சத்துவாபத்தி (Sattvāpatti) — சத்துவ நிலை பேறு &amp; இல்லற மாண்பு</h3>
            <div class="pat-level-sanskrit">Abidance in Pure Light, Steadfast Virtue &amp; Noble Character</div>
            <div class="pat-sutra-quote">
              "சத்வபுருஷயோஃ சுத்திசாம்யே கைவல்யமிதி" (YS 3.55) — ரஜோ-தமோ குணங்கள் அடங்கி, அகம் முழுவதும் சத்துவ ஒளியால் நிறைந்து, அறநெறியே வாழ்வாக மாறுதல்.
            </div>
          </div>
        </div>

        <div class="pat-grid-4">
          <div class="pat-quadrant curriculum">
            <div class="pat-quadrant-title"><span>📚</span> 1. முறைசார் பாடத்திட்டம் (Formal Curriculum)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>திருக்குறள் சான்றாண்மை (அதிகாரம் 99)</strong>: அன்பு, நாண், ஒப்புரவு, கண்ணோட்டம், வாய்மை என்னும் ஐந்து தூண்கள்.</li>
                <li><strong>பகவத் கீதை 12-ஆம் அத்தியாயம் (பக்தி யோகம்)</strong>: ஈசனிடம் பூரண சரணாகதி அடைந்த பக்தனின் குணங்கள்.</li>
                <li><strong>சிவஞானபோதம் &amp; திருவருட்பயன்</strong>: ஆன்மா சிவத்தோடு அத்துவிதமாய் இரண்டறக் கலக்கும் நெறிமுறை.</li>
                <li><strong>காஞ்சி மகா பெரியவாவின் தெய்வத்தின் குரல்</strong>: பஞ்ச மகா யக்ஞங்களின் குடும்ப விஞ்ஞானம்.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant rating">
            <div class="pat-quadrant-title"><span>🔍</span> 2. சுய-தரிசன ஆன்ம மதிப்பீடு (Progression Rating)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>மதிப்பீடு</strong>: 4.0 / 7.0 (ஒளிபடைத்த சான்றோன் / Illuminated Noble Soul).</li>
                <li><strong>மனோநிலை</strong>: எந்நிலையிலும் தர்மத்தை விட்டு விலகாத அசைக்க முடியாத உள்அமைதி.</li>
                <li><strong>அகந்தை நிலை (Ego Index)</strong>: சுயநல ஆசைகள் முற்றிலும் கரையத் தொடங்குதல்; 'நான்' என்பது இறைவனின் கருவி என்றாகிறது.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant lifestyle">
            <div class="pat-quadrant-title"><span>🌿</span> 3. அன்றாட வாழ்வியல் நெறிமுறை (Way of Life)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>பஞ்ச மகா யக்ஞ அனுஷ்டானம்</strong>: 1. பிரம்ம, 2. தேவ, 3. பித்ரு, 4. மனுஷ்ய (விருந்தோம்பல்), 5. பூத யக்ஞங்களை அனுதினமும் செய்தல்.</li>
                <li><strong>அதிதி சத்காரம்</strong>: வீட்டிற்கு வரும் எவரையும் முகம் மலர்ந்து வரவேற்று உணவளித்தல்.</li>
                <li><strong>தூய உழைப்பு</strong>: நேர்மையான வழியில் மட்டுமே பொருள் ஈட்டுதல் (தர்ம சம்பாதனை).</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant legacy">
            <div class="pat-quadrant-title"><span>🏡</span> 4. வாழ்வை நடத்துதலும் அறக்கொடையும் (Legacy)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>சான்றோனாக்குதல்</strong>: 'தன்மகனைச் சான்றோன் எனக்கேட்ட தாய்' போல, தன் பிள்ளைகளை நற்குணத்தின் சிகரங்களாக உருவாக்குதல்.</li>
                <li><strong>சமூக வழிகாட்டுதல்</strong>: குடும்பப் பெரியவராக ஊருக்கும் உறவுக்கும் நடுவுநிலைமை காத்து வழிகாட்டுதல்.</li>
                <li><strong>தலைமுறை விதை</strong>: தர்மத்தை வாழ்ந்து காட்டும் ஒரு மாபெரும் குலப்பாரம்பரியத்தை நிறுவுதல்.</li>
              </ul>
            </div>
          </div>
        </div>
      </article>

      <!-- LEVEL 5 CARD -->
      <article class="pat-level-card" data-pat-level="L5" style="border-left: 5px solid #fb923c;">
        <div class="pat-level-header">
          <div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="pat-level-code-pill">WBS: CUR-PAT-L5</span>
              <span class="pat-rating-badge l5">⭐️ சுய-தரிசன மதிப்பீடு: Level 5.0 / 7.0</span>
              <span style="font-size:0.75rem; color:#94a3b8;">பருவம்: பற்றற்ற இல்லற ஞானம் &amp; கர்ம யோகம்</span>
            </div>
            <h3 class="pat-level-title">படிநிலை 5: அசம்சக்தி (Asaṁśakti) — பற்றற்ற இல்லறத் தலைமை &amp; கர்ம யோகம்</h3>
            <div class="pat-level-sanskrit">Detached Noble Engagement &amp; Effortless Grihastha Mastery</div>
            <div class="pat-sutra-quote">
              "கர்மண்யேவாதிகாரஸ்தே மா பலேஷு கதாசன" — கடமைகளை முழு வீச்சுடன் ஆற்றுதல், ஆனால் பலனில் துளியும் பற்றற்றிருத்தல்; தாமரை இலைத் தண்ணீர் போல குடும்பத்தில் வாழ்தல்.
            </div>
          </div>
        </div>

        <div class="pat-grid-4">
          <div class="pat-quadrant curriculum">
            <div class="pat-quadrant-title"><span>📚</span> 1. முறைசார் பாடத்திட்டம் (Formal Curriculum)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>63 நாயன்மார் இல்லற மாண்பு (பெரியபுராணம்)</strong>: இளையான்குடி மாறனார், இயற்பகையார், அமர்நீதியார் வாழ்வியல் ஒப்பாய்வு.</li>
                <li><strong>அஷ்டாவக்ர கீதை &amp; ஜனக மகாராஜா தத்துவம்</strong>: அரசாண்ட போதும், குடும்பத்தை நடத்திய போதும் பற்றற்று நின்ற ராஜரிஷி யோகம்.</li>
                <li><strong>திருக்குறள் அவாவறுத்தல் &amp; துறவு</strong>: இல்லறத்தில் நின்றே ஆசையை அறுக்கும் பரம ஞானம் (குறள் 361-370).</li>
                <li><strong>ஆதிசங்கரரின் உபதேச சஹஸ்ரி</strong>: கர்த்தா-போக்தா பாவத்தைக் கழிக்கும் விவேகம்.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant rating">
            <div class="pat-quadrant-title"><span>🔍</span> 2. சுய-தரிசன ஆன்ம மதிப்பீடு (Progression Rating)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>மதிப்பீடு</strong>: 5.0 / 7.0 (பற்றற்ற இல்லற யோகி / Unattached Master Grihastha).</li>
                <li><strong>மனோநிலை</strong>: குடும்பப் பொறுப்புகளைத் தலையேற்று நடத்தினாலும், உள்ளத்தில் பற்றின்மை; வெற்றி-தோல்வியில் சமநிலை.</li>
                <li><strong>அகந்தை நிலை (Ego Index)</strong>: "நான் செய்கிறேன்" என்ற கர்த்ருத்துவ அகந்தை முழுமையாக சிதைந்து போதல்.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant lifestyle">
            <div class="pat-quadrant-title"><span>🌿</span> 3. அன்றாட வாழ்வியல் நெறிமுறை (Way of Life)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>அகத்தில் மௌனம், புறத்தில் சுறுசுறுப்பு</strong>: தொழிலிலும் இல்லத்திலும் கடமைகளை முழு ஈடுபாட்டுடன், ஆனால் பற்றின்றி செய்தல்.</li>
                <li><strong>இறை அர்ப்பணம்</strong>: குடும்பத்தின் சகல செல்வங்களையும் ஈசனின் சொத்தாக பாவித்து காவல் காத்தல்.</li>
                <li><strong>ரகசிய தானம்</strong>: வலது கை கொடுப்பது இடது கைக்குத் தெரியாத அளவிற்கு ஏழைகளுக்கு உதவுதல்.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant legacy">
            <div class="pat-quadrant-title"><span>🏡</span> 4. வாழ்வை நடத்துதலும் அறக்கொடையும் (Legacy)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>அசைக்க முடியாத தூண்</strong>: குடும்பத்தில் வறுமையோ, இழப்போ வந்தாலும் மலையென நின்று அனைவரையும் காக்கும் ஆன்ம பலம்.</li>
                <li><strong>தியாக மரபு</strong>: பிள்ளைகளுக்கு வார்த்தைகளால் அல்லாமல், தன் தியாக வாழ்வால் உண்மை வேதாந்தத்தைக் கற்பித்தல்.</li>
                <li><strong>தலைமுறை விதை</strong>: இன்ப-துன்பங்களில் கலங்காத ஒரு தீரமிக்க வம்சத்தை உருவாக்குதல்.</li>
              </ul>
            </div>
          </div>
        </div>
      </article>

      <!-- LEVEL 6 CARD -->
      <article class="pat-level-card" data-pat-level="L6" style="border-left: 5px solid #f472b6;">
        <div class="pat-level-header">
          <div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="pat-level-code-pill">WBS: CUR-PAT-L6</span>
              <span class="pat-rating-badge l6">⭐️ சுய-தரிசன மதிப்பீடு: Level 6.0 / 7.0</span>
              <span style="font-size:0.75rem; color:#94a3b8;">பருவம்: லோகசங்கிரகம் &amp; பிரபஞ்ச ஆன்ம பார்வை</span>
            </div>
            <h3 class="pat-level-title">படிநிலை 6: பதார்த்த பாவனை (Padārtha Bhāvanā) — பிரபஞ்சக் கருணை &amp; லோகசங்கிரகம்</h3>
            <div class="pat-level-sanskrit">Universal Cosmic Vision &amp; Generational Dharmic Benefaction</div>
            <div class="pat-sutra-quote">
              "தர்மமேக சமாதி" (YS 4.29) — எங்கும் நீக்கமற நிறைந்திருக்கும் பரம்பொருளை மட்டுமே காணுதல் (பிரம்ம பாவனை); உலகிலுள்ள அனைத்து உயிர்களையும் தன் உயிராகவே கருதுதல்.
            </div>
          </div>
        </div>

        <div class="pat-grid-4">
          <div class="pat-quadrant curriculum">
            <div class="pat-quadrant-title"><span>📚</span> 1. முறைசார் பாடத்திட்டம் (Formal Curriculum)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>பிரம்ம சூத்திர சதுஸ்-சூத்ரி &amp; சாங்கர பாஷ்யம்</strong>: மாயையைக் கடந்து எங்கும் சச்சிதானந்த பரம்பொருளைக் காணும் தரிசனம்.</li>
                <li><strong>வள்ளலாரின் ஜீவகாருண்ய ஒழுக்கம்</strong>: "வாடிய பயிரைக் கண்டபோதெல்லாம் வாடினேன்" என்ற உன்னத ஆன்மநேய ஒருமைப்பாடு.</li>
                <li><strong>திருமந்திரம் 7-ஆம் தந்திரம்</strong>: 'யான் பெற்ற இன்பம் பெறுக இவ்வையகம்' என்ற உலக நல வேள்வி.</li>
                <li><strong>மாண்டூக்ய உபநிடதம் &amp; கௌடபாத காரிகை</strong>: துரிய உணர்வின் அஜாத வாத ஆய்வு.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant rating">
            <div class="pat-quadrant-title"><span>🔍</span> 2. சுய-தரிசன ஆன்ம மதிப்பீடு (Progression Rating)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>மதிப்பீடு</strong>: 6.0 / 7.0 (பிரபஞ்சப் பேரறிஞர் / Cosmic Sage of Dharma).</li>
                <li><strong>மனோநிலை</strong>: நண்பன்-பகைவன், எனது-பிறரது என்ற பேதங்கள் முற்றிலும் மறைந்து, அகிலமே தன் குடும்பமாதல்.</li>
                <li><strong>அகந்தை நிலை (Ego Index)</strong>: தனிமனித அகந்தை கரைந்து, அகில உணர்வில் (Universal Self) நிலைபெறுதல்.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant lifestyle">
            <div class="pat-quadrant-title"><span>🌿</span> 3. அன்றாட வாழ்வியல் நெறிமுறை (Way of Life)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>சதா சர்வ காலமும் சிவானந்தம்</strong>: உண்ணும் போதும், உறங்கும் போதும் இடைவிடாத ஆன்ம விழிப்புணர்வு.</li>
                <li><strong>பொதுத்தொண்டு</strong>: தன் நேரம், உடல், செல்வம் அனைத்தையும் மக்கள் பசி தீர்க்கவும் கல்வி புகட்டவும் அர்ப்பணித்தல்.</li>
                <li><strong>சாந்தப் பெருவெளி</strong>: தன்னை அணுகும் எவருக்கும் அச்சமின்மையையும் (அபயம்) பேரமைதியையும் வழங்குதல்.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant legacy">
            <div class="pat-quadrant-title"><span>🏡</span> 4. வாழ்வை நடத்துதலும் அறக்கொடையும் (Legacy)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>யாதும் ஊரே யாவரும் கேளிர்</strong>: தன் குடும்பத்தைக் கடந்து ஊரையே தன் குடும்பமாகப் பேணிப் பாதுகாத்தல்.</li>
                <li><strong>அற நிறுவனங்கள் நிறுவுதல்</strong>: அன்ன சத்திரங்கள், வேத பாடசாலைகள், மருத்துவ உதவிக் கூடங்களை அமைத்தல்.</li>
                <li><strong>தலைமுறை விதை</strong>: நூற்றாண்டு காலம் நிலைத்து நின்று மக்களுக்கு வழிகாட்டும் தர்ம ஸ்தாபனங்களை விட்டுச் செல்லுதல்.</li>
              </ul>
            </div>
          </div>
        </div>
      </article>

      <!-- LEVEL 7 CARD -->
      <article class="pat-level-card" data-pat-level="L7" style="border-left: 5px solid var(--gold-bright, #ffd700);">
        <div class="pat-level-header">
          <div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="pat-level-code-pill">WBS: CUR-PAT-L7</span>
              <span class="pat-rating-badge l7">⭐️⭐️⭐️ சுய-தரிசன மதிப்பீடு: Level 7.0 / 7.0 (முழுமை)</span>
              <span style="font-size:0.75rem; color:var(--gold-soft);">பருவம்: ஜீவன்முக்தி &amp; சகஜ நிர்வாணம்</span>
            </div>
            <h3 class="pat-level-title">படிநிலை 7: துரியகா (Turyagā) — சகஜ சமாதி, ஜீவன்முக்தி &amp; அழியாத வாழ்வியல் மாண்பு</h3>
            <div class="pat-level-sanskrit">Sahaja Samadhi, Jivanmukti &amp; Eternal Living Legacy</div>
            <div class="pat-sutra-quote">
              "வையத்துள் வாழ்வாங்கு வாழ்பவன் வான்உறையும் தெய்வத்துள் வைக்கப் படும்" (திருக்குறள் 50) — குடும்பத்தில் வாழ்ந்தே மரணமிலாப் பெருவாழ்வையும், அழியாத நிர்வாணத்தையும் எய்திய நடமாடும் தெய்வம்.
            </div>
          </div>
        </div>

        <div class="pat-grid-4">
          <div class="pat-quadrant curriculum">
            <div class="pat-quadrant-title"><span>📚</span> 1. முறைசார் பாடத்திட்டம் (Formal Curriculum)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>மகா வாக்கிய அனுபூதி</strong>: பிரக்ஞானம் பிரம்ம, தத்வமஸி, அஹம் பிரம்மாஸ்மி, அயம் ஆத்மா பிரம்ம.</li>
                <li><strong>சிவஞான சித்தியார் சுபக்கம் (முத்தி நிச்சயம்)</strong>: மலபரிபாகம், சத்தினிபாதம் கடந்து சிவானந்த அனுபவம்.</li>
                <li><strong>ரமண மகரிஷியின் உபதேச சாரம்</strong>: அகந்தை அழிந்த சாட்சி நிலை.</li>
                <li><strong>காஞ்சி மகா பெரியவா அருளிய சனாதன ஜீவன்முக்தி நெறி</strong>: விதேக முக்தி வரை நீடிக்கும் தர்ம வாழ்வு.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant rating">
            <div class="pat-quadrant-title"><span>🔍</span> 2. சுய-தரிசன ஆன்ம மதிப்பீடு (Progression Rating)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>மதிப்பீடு</strong>: 7.0 / 7.0 (ஜீவன்முக்தர் / Living Liberated Soul).</li>
                <li><strong>மனோநிலை</strong>: சகஜ சமாதி; விழிப்பு, கனவு, உறக்கம் மூன்றையும் கடந்த துரிய நிலையில் இடைவிடாது நிலைகொள்ளுதல்.</li>
                <li><strong>அகந்தை நிலை (Ego Index)</strong>: பூஜ்யம் (Zero Ego); சிவமே தானாய் விளங்குதல்.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant lifestyle">
            <div class="pat-quadrant-title"><span>🌿</span> 3. அன்றாட வாழ்வியல் நெறிமுறை (Way of Life)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>சுவாசமே தர்மம்</strong>: எவ்வித முயற்சியும் இன்றி இயல்பாகவே அறவழியில் இயங்குதல்.</li>
                <li><strong>அதிஅற்புத அமைதி</strong>: அவரைச் சுற்றி இருப்பவர்கள் தங்கள் மனக் கவலைகள் யாவும் பறந்தோட உணர்தல்.</li>
                <li><strong>உலகப் பேரொளி</strong>: சொல், பார்வை, மூச்சு யாவும் உலகிற்கு நல்வாழ்வையும் முக்தியையும் வழங்குதல்.</li>
              </ul>
            </div>
          </div>

          <div class="pat-quadrant legacy">
            <div class="pat-quadrant-title"><span>🏡</span> 4. வாழ்வை நடத்துதலும் அறக்கொடையும் (Legacy)</div>
            <div class="pat-quadrant-body">
              <ul>
                <li><strong>தெய்வத்துள் வைக்கப்படும் பெருவாழ்வு</strong>: குடும்பத்தையும் சமூகத்தையும் உய்விக்கும் அழியாத ஆன்ம ஒளி.</li>
                <li><strong>அழியாத வரலாறு</strong>: அவரது வாழ்ந்த முறை தலைமுறை தலைமுறையாக உலகிற்கு வழிகாட்டும் கலங்கரை விளக்கமாக மாறுதல்.</li>
                <li><strong>தலைமுறை விதை</strong>: நிர்வாணத்தின் முழுமையை இவ்வுலகிற்கு உணர்த்திச் சென்ற பரம சான்றோன் மரபு.</li>
              </ul>
            </div>
          </div>
        </div>
      </article>

      <!-- ========================================== -->
      <!-- INTERACTIVE SELF-REALIZATION ASSESSMENT ENGINE -->
      <!-- ========================================== -->
      <div class="pat-assessment-box" id="patanjaliAssessmentTool">
        <div style="text-align:center; max-width:820px; margin:0 auto 24px;">
          <div style="font-size:0.8rem; font-weight:700; color:var(--gold); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">
            Self-Realization Epistemic Meter
          </div>
          <h3 style="color:#ffffff; font-size:1.65rem; font-weight:800; margin-bottom:10px;">
            🪞 சுய-தரிசன ஆன்மப் படிநிலை மதிப்பீட்டு இயற்றி
          </h3>
          <p style="color:#cbd5e1; font-size:0.92rem; line-height:1.7;">
            கீழ்க்கண்ட 7 எளிய வாழ்வியல் கேள்விகளுக்கு உங்கள் மனசாட்சிப்படி விடையளித்து, பதஞ்சலி சப்த ஞான பூமிகைகளில் உங்கள் தற்போதைய ஆன்ம முதிர்ச்சி நிலையையும், அடுத்த நிலைக்குச் செல்வதற்கான வழிகாட்டலையும் உடனே அறிந்து கொள்ளுங்கள்.
          </p>
        </div>

        <div style="max-width:850px; margin:0 auto;">
          <!-- Q1 -->
          <div class="pat-q-item">
            <div class="pat-q-title">1. வாழ்வின் மெய்நோக்கம் &amp; தர்ம நாட்டம் (Noble Yearning):</div>
            <div class="pat-q-radios">
              <label><input type="radio" name="pq1" value="1" checked> உலகியல் சுகங்களில் மட்டுமே ஆசை உள்ளது</label>
              <label><input type="radio" name="pq1" value="2"> நிலையான அமைதியை நாட வேண்டும் என்ற தாகம் வந்துள்ளது</label>
              <label><input type="radio" name="pq1" value="3"> தர்ம வாழ்வே என் வாழ்வின் ஒரே இலட்சியம்</label>
            </div>
          </div>

          <!-- Q2 -->
          <div class="pat-q-item">
            <div class="pat-q-title">2. சாத்திர வாசிப்பும் விவேகப் பகுத்தறிவும் (Study &amp; Discernment):</div>
            <div class="pat-q-radios">
              <label><input type="radio" name="pq2" value="1" checked> சாத்திரங்களைப் படிப்பதில் ஆர்வம் இல்லை</label>
              <label><input type="radio" name="pq2" value="2"> திருக்குறள், கீதை, திருமுறை வாசித்து சிந்திக்கிறேன்</label>
              <label><input type="radio" name="pq2" value="3"> நித்திய-அநித்திய பகுத்தறிவுடன் வாழ்வின் முடிவுகளை எடுக்கிறேன்</label>
            </div>
          </div>

          <!-- Q3 -->
          <div class="pat-q-item">
            <div class="pat-q-title">3. சினம் &amp; உணர்ச்சி மேலாண்மை (Emotional Subtlety):</div>
            <div class="pat-q-radios">
              <label><input type="radio" name="pq3" value="1" checked> அடிக்கடி கோபமும் பதற்றமும் வந்து விடுகிறது</label>
              <label><input type="radio" name="pq3" value="2"> கோபம் வந்தாலும் உடனே உணர்ந்து கட்டுப்படுத்துகிறேன்</label>
              <label><input type="radio" name="pq3" value="3"> யார் எதைச் சொன்னாலும் என் மன அமைதி குலைவதில்லை, எளிதில் மன்னிக்கிறேன்</label>
            </div>
          </div>

          <!-- Q4 -->
          <div class="pat-q-item">
            <div class="pat-q-title">4. அன்றாட பஞ்ச மகா யக்ஞ ஆசாரம் (Daily Duty &amp; Habits):</div>
            <div class="pat-q-radios">
              <label><input type="radio" name="pq4" value="1" checked> அன்றாட கடமைகளை மட்டுமே செய்கிறேன், வழிபாடோ சேவையோ இல்லை</label>
              <label><input type="radio" name="pq4" value="2"> தினசரி வழிபாடு, பெற்றோர் மரியாதை, எளிய தானம் செய்கிறேன்</label>
              <label><input type="radio" name="pq4" value="3"> பஞ்ச மகா யக்ஞங்களையும் அதிதி உபசரிப்பையும் தவறாது நடத்துகிறேன்</label>
            </div>
          </div>

          <!-- Q5 -->
          <div class="pat-q-item">
            <div class="pat-q-title">5. இல்லறத்தில் பற்றற்ற தியாகக் தலைமை (Family Detachment in Duty):</div>
            <div class="pat-q-radios">
              <label><input type="radio" name="pq5" value="1" checked> என் குடும்பம், என் பொருள் என்ற தீவிர பற்றும் சுயநலமும் உள்ளது</label>
              <label><input type="radio" name="pq5" value="2"> குடும்பக் கடமைகளைச் செய்கிறேன், ஆனால் எதிர்பார்ப்பு உள்ளது</label>
              <label><input type="radio" name="pq5" value="3"> தாமரை இலைத் தண்ணீர் போல எவ்வித பற்றுமின்றி ஈசன் வழிநடத்துகிறார் என வாழ்கிறேன்</label>
            </div>
          </div>

          <!-- Q6 -->
          <div class="pat-q-item">
            <div class="pat-q-title">6. சமூகம் &amp; தலைமுறைக்கான அறக்கொடை (Leaving Legacy):</div>
            <div class="pat-q-radios">
              <label><input type="radio" name="pq6" value="1" checked> அடுத்த தலைமுறையோ சமூகமோ என் சிந்தனையில் இல்லை</label>
              <label><input type="radio" name="pq6" value="2"> என் பிள்ளைகளை நல்லவர்களாக வளர்க்க முயல்கிறேன்</label>
              <label><input type="radio" name="pq6" value="3"> சமூகத்திற்கு உதவும் கல்வி, அறப்பணிகள் மற்றும் சான்றோன் மரபை விட்டுச் செல்கிறேன்</label>
            </div>
          </div>

          <!-- Q7 -->
          <div class="pat-q-item">
            <div class="pat-q-title">7. அக அமைதியும் ஆன்ம முக்தி உணர்வும் (Sahaja Peace / Turiya):</div>
            <div class="pat-q-radios">
              <label><input type="radio" name="pq7" value="1" checked> மரண பயமும் எதிர்காலக் கவலையும் என்னை ஆட்டுகிறது</label>
              <label><input type="radio" name="pq7" value="2"> இறை நம்பிக்கையினால் ஓரளவுக்கு நிம்மதி உள்ளது</label>
              <label><input type="radio" name="pq7" value="3"> எந்நிலையிலும் அசைக்க முடியாத சச்சிதானந்தப் பேரமைதியில் திளைக்கிறேன்</label>
            </div>
          </div>

          <div style="text-align:center; margin-top:20px;">
            <button type="button" onclick="calculatePatanjaliScore()" class="sheet-btn sheet-btn-view" style="padding:12px 28px; font-size:1rem; font-weight:700;">
              ✨ என் ஆன்மப் படிநிலையைக் கணிக்குக (Calculate My Level)
            </button>
          </div>

          <!-- Score Result Box -->
          <div id="patScoreResultBox" class="pat-score-display">
            <div style="font-size:0.85rem; color:#94a3b8; text-transform:uppercase; letter-spacing:1px;">உங்கள் தற்போதைய ஆன்ம முதிர்ச்சி நிலை</div>
            <div id="patResultLevelName" style="color:var(--gold-bright); font-size:1.6rem; font-weight:800; margin:8px 0;">Level 3.5: தனுமானசி - சத்துவாபத்தி இடைநிலை</div>
            <div id="patResultStars" style="font-size:1.3rem; margin-bottom:10px;">⭐️⭐️⭐️⭐️</div>
            <p id="patResultDesc" style="color:#cbd5e1; font-size:0.95rem; line-height:1.7; max-width:700px; margin:0 auto 14px;">
              நீங்கள் தத்துவ ஆய்விலும் மனவடக்கத்திலும் நல்ல முன்னேற்றம் அடைந்து வருகிறீர்கள். அடுத்த கட்டமாக இல்லறத்தில் பஞ்ச மகா யக்ஞங்களையும், சினம் முழுமையாக ஒழித்த சான்றாண்மையையும் நிலைநிறுத்த முயற்சி செய்யுங்கள்.
            </p>
            <div id="patResultAction" style="margin-top:12px;">
              <a href="#patanjaliSyllabus" class="tag" style="background:rgba(212,175,55,0.2); border:1px solid var(--gold); color:#ffffff; padding:6px 16px; border-radius:12px; text-decoration:none;">
                அடுத்த படிநிலைப் பாடநெறியைக் காண்க ↗
              </a>
            </div>
          </div>
        </div>
      </div>

    </section>
'''

    js_block = '''
  <script>
    // Patanjali Level Filter
    function filterPatLevel(lvl) {
      document.querySelectorAll('.pat-pill-btn').forEach(function(btn) {
        btn.classList.remove('active');
      });
      if (event && event.target) event.target.classList.add('active');

      var cards = document.querySelectorAll('.pat-level-card');
      cards.forEach(function(card) {
        if (lvl === 'all' || card.getAttribute('data-pat-level') === lvl) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    }

    // Patanjali Self-Realization Score Calculator
    function calculatePatanjaliScore() {
      var total = 0;
      for (var i = 1; i <= 7; i++) {
        var radios = document.getElementsByName('pq' + i);
        for (var j = 0; j < radios.length; j++) {
          if (radios[j].checked) {
            total += parseInt(radios[j].value, 10);
            break;
          }
        }
      }

      // Min 7 (all 1), Max 21 (all 3) -> scale to 1.0 to 7.0
      var rawLevel = 1.0 + ((total - 7) / 14.0) * 6.0;
      var level = Math.round(rawLevel * 10) / 10;

      var resBox = document.getElementById('patScoreResultBox');
      var nameEl = document.getElementById('patResultLevelName');
      var starsEl = document.getElementById('patResultStars');
      var descEl = document.getElementById('patResultDesc');

      var name = "";
      var stars = "";
      var desc = "";

      if (level < 2.0) {
        name = "படிநிலை 1: சுபேச்சை (Śubhecchā) — Level " + level.toFixed(1) + " / 7.0";
        stars = "⭐️";
        desc = "நீங்கள் வாழ்வின் உண்மையான அர்த்தத்தை நாடத் தொடங்கியுள்ளீர்கள். ஆத்திசூடி, திருக்குறள் பாயிரவியல் மற்றும் தினசரி எளிய வழிபாட்டைத் தொடங்குங்கள். உங்கள் நற்குடும்பத்தின் தொடக்கப் புள்ளி இதுவே!";
      } else if (level < 3.0) {
        name = "படிநிலை 2: விசாரணை (Vicāraṇā) — Level " + level.toFixed(1) + " / 7.0";
        stars = "⭐️⭐️";
        desc = "சாத்திரங்களை பகுத்தறிவோடு கற்றுணரும் பக்குவம் உங்களிடம் மலர்ந்துள்ளது. தத்வ போதம், திருக்குறள் இல்லறவியல் மற்றும் பதி-பசு-பாச உண்மைகளை ஆழமாகப் படியுங்கள்.";
      } else if (level < 4.0) {
        name = "படிநிலை 3: தனுமானசி (Tanumānasī) — Level " + level.toFixed(1) + " / 7.0";
        stars = "⭐️⭐️⭐️";
        desc = "மன அடக்கமும் உணர்ச்சிப் பக்குவமும் உங்களிடம் வளரத் தொடங்கியுள்ளது. கோபத்தை அடியோடு நீக்குதல், சகிப்புத்தன்மை மற்றும் பகவத் கீதை கர்ம யோகத்தை அன்றாட வாழ்வில் கடைப்பிடியுங்கள்.";
      } else if (level < 5.0) {
        name = "படிநிலை 4: சத்துவாபத்தி (Sattvāpatti) — Level " + level.toFixed(1) + " / 7.0";
        stars = "⭐️⭐️⭐️⭐️";
        desc = "உங்கள் உள்ளத்தில் சத்துவக் குணம் நிலைபெற்றுள்ளது. பஞ்ச மகா யக்ஞங்களை தவறாது ஆற்றுங்கள். குடும்பத்தில் சான்றாண்மையை நிலைநிறுத்தி, நன்மக்களை உருவாக்கும் தலைமைத்துவத்தை முழுமையாகச் செயல்படுத்துங்கள்.";
      } else if (level < 6.0) {
        name = "படிநிலை 5: அசம்சக்தி (Asaṁśakti) — Level " + level.toFixed(1) + " / 7.0";
        stars = "⭐️⭐️⭐️⭐️⭐️";
        desc = "இல்லறக் கடமைகளைச் செய்தாலும் உள்ளத்தில் தாமரை இலைத் தண்ணீர் போன்ற உன்னதப் பற்றின்மையை எய்தியுள்ளீர்கள். 63 நாயன்மார்களின் வரலாற்று வழியில் நின்று தியாக வாழ்வை முன்னெடுத்துச் செல்லுங்கள்.";
      } else if (level < 6.8) {
        name = "படிநிலை 6: பதார்த்த பாவனை (Padārtha Bhāvanā) — Level " + level.toFixed(1) + " / 7.0";
        stars = "⭐️⭐️⭐️⭐️⭐️⭐️";
        desc = "எங்கும் பரம்பொருளை மட்டுமே காணும் பிரபஞ்சப் பார்வை உங்களிடம் மிளிர்கிறது. சமூகத்திற்கு உதவும் கல்வி மற்றும் தர்ம ஸ்தாபனங்களை நிறுவி, தலைமுறை கடந்து நிற்கும் அறக்கொடையை வழங்குங்கள்.";
      } else {
        name = "படிநிலை 7: துரியகா (Turyagā) — Level " + level.toFixed(1) + " / 7.0 (சகஜ நிர்வாணம்)";
        stars = "⭐️⭐️⭐️⭐️⭐️⭐️⭐️";
        desc = "'வையத்துள் வாழ்வாங்கு வாழ்பவன் வான்உறையும் தெய்வத்துள் வைக்கப் படும்' — குடும்பத்தில் வாழ்ந்தே முக்தி பெற்ற ஜீவன்முக்தர் நிலை! உங்கள் வாழ்வும் வாக்கும் மனிதகுலத்திற்கே வழிகாட்டும் கலங்கரை விளக்கம்.";
      }

      if (nameEl) nameEl.textContent = name;
      if (starsEl) starsEl.textContent = stars;
      if (descEl) descEl.textContent = desc;
      if (resBox) {
        resBox.style.display = 'block';
        resBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    }
  </script>
'''

    with open('syllabus.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Insert CSS before </head>
    if '</head>' in html and 'pat-framework-container' not in html:
        html = html.replace('</head>', css_block + '\n</head>')

    # 2. Insert Nav Pill in context-tabs-nav
    target_nav = '<a href="syllabus.html" class="context-tab-pill active"><span class="context-tab-pill-icon">📚</span><span>முழு பாடத்திட்டம்</span></a>'
    new_nav = target_nav + '\n        <a href="#patanjaliSyllabus" class="context-tab-pill"><span class="context-tab-pill-icon">🧘</span><span>பதஞ்சலி 7 படிநிலைகள்</span></a>'
    if target_nav in html and '#patanjaliSyllabus' not in html:
        html = html.replace(target_nav, new_nav)

    # 3. Insert Main Content before the school sections (before '<div class="scripture-study-section">')
    target_section = '    <!-- Syllabus Sections -->\n    <div class="scripture-study-section">'
    if target_section in html and 'id="patanjaliSyllabus"' not in html:
        html = html.replace(target_section, content_html + '\n\n' + target_section)

    # 4. Insert JS before </body>
    if '</body>' in html and 'filterPatLevel' not in html:
        html = html.replace('</body>', js_block + '\n</body>')

    with open('syllabus.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Updated syllabus.html successfully!")

    # 5. Synchronize across site/ and docs/
    targets = ['site/syllabus.html', 'docs/syllabus.html']
    for t in targets:
        os.makedirs(os.path.dirname(t), exist_ok=True)
        shutil.copy2('syllabus.html', t)
        print(f"Synchronized syllabus.html -> {t}")

if __name__ == '__main__':
    build_patanjali_html()
