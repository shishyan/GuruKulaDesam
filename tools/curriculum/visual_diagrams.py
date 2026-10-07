# -*- coding: utf-8 -*-
"""
Visual Diagrams & Infographics Generator for Guru Kula Desam Curriculum
Produces responsive SVG illustrations matching a balanced, elegant, high-contrast palette.
Avoids excessive yellow/orange text; uses crisp white (#f8fafc), cool slate (#cbd5e1),
calm teal (#2dd4bf), and subtle gold accents for true spiritual elegance.
"""

def generate_svg_thiruneeru():
    """Diagram showing 3 lines of Thiruneeru, meaning of 3 Malas burnt, and fingers used."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>திருநீறு (விபூதி) தத்துவம் & திரிபுண்டர விளக்கம்</h4>
      </div>
      <svg viewBox="0 0 700 240" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="240" rx="12" fill="rgba(11,15,22,0.9)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        <path d="M 80 190 Q 80 60 220 60 Q 360 60 360 190 Z" fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
        
        <!-- 3 Horizontal Lines (Tripundram) -->
        <rect x="130" y="100" width="180" height="10" rx="5" fill="#f8f9fa" filter="drop-shadow(0 0 6px rgba(255,255,255,0.7))"/>
        <rect x="130" y="125" width="180" height="10" rx="5" fill="#f8f9fa" filter="drop-shadow(0 0 6px rgba(255,255,255,0.7))"/>
        <rect x="130" y="150" width="180" height="10" rx="5" fill="#f8f9fa" filter="drop-shadow(0 0 6px rgba(255,255,255,0.7))"/>
        
        <circle cx="220" cy="130" r="7" fill="#e63946" filter="drop-shadow(0 0 8px rgba(230,57,70,0.8))"/>

        <line x1="315" y1="105" x2="420" y2="90" stroke="rgba(255,255,255,0.3)" stroke-width="1.5" stroke-dasharray="3,3"/>
        <line x1="315" y1="130" x2="420" y2="130" stroke="rgba(255,255,255,0.3)" stroke-width="1.5" stroke-dasharray="3,3"/>
        <line x1="315" y1="155" x2="420" y2="170" stroke="rgba(255,255,255,0.3)" stroke-width="1.5" stroke-dasharray="3,3"/>

        <!-- Crisp, balanced white and slate text -->
        <text x="430" y="94" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="14" font-weight="bold">1. ஆணவ மலம் நீங்குதல் <tspan fill="#94a3b8" font-weight="normal">(அகங்காரம் ஒழிதல்)</tspan></text>
        <text x="430" y="134" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="14" font-weight="bold">2. கன்ம மலம் நீங்குதல் <tspan fill="#94a3b8" font-weight="normal">(பாவ வினைகள் எரிதல்)</tspan></text>
        <text x="430" y="174" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="14" font-weight="bold">3. மாயா மலம் நீங்குதல் <tspan fill="#94a3b8" font-weight="normal">(மெய்யறிவு பெறுதல்)</tspan></text>
        
        <text x="220" y="215" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="12">வலது கையின் நடு 3 விரல்களால் (மோதிர, நடு, பெருவிரல் உதவி) அணியும் நெறி</text>
      </svg>
      <div class="diagram-footer">
        <p><strong>பயிற்சி விளக்கம்:</strong> பசுஞ்சாணத்தை அக்னியில் சுட்டு எடுக்கப்படும் திருநீறு தூய்மையானது. அது நமது மும்மலங்களையும் எரித்து சிவபெருமானின் திருவடிப் பேற்றைத் தரும் சங்கற்பக் குறியீடாகும்.</p>
      </div>
    </div>
    """

def generate_svg_temple():
    """Diagram showing Temple Architecture and Human Body Correspondence."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>திருக்கோயில் அமைப்பு & மனித உடல் தத்துவ விளக்கம்</h4>
      </div>
      <svg viewBox="0 0 700 250" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="250" rx="12" fill="rgba(11,15,22,0.9)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- Step 1: Gopuram -->
        <g transform="translate(60, 40)">
          <polygon points="40,20 10,140 70,140" fill="rgba(255,255,255,0.05)" stroke="#cbd5e1" stroke-width="1.8"/>
          <text x="40" y="165" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="14" font-weight="bold">ராஜகோபுரம்</text>
          <text x="40" y="185" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="12">பாதம் (Feet)</text>
        </g>
        
        <line x1="150" y1="100" x2="180" y2="100" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>
        
        <!-- Step 2: Kodimaram & Balipitham -->
        <g transform="translate(200, 40)">
          <line x1="30" y1="20" x2="30" y2="140" stroke="#cbd5e1" stroke-width="3"/>
          <circle cx="30" cy="20" r="5" fill="#f8fafc"/>
          <rect x="55" y="110" width="30" height="30" rx="3" fill="rgba(230,57,70,0.2)" stroke="#e63946" stroke-width="1.5"/>
          <text x="45" y="165" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">கொடிமரம் & பலிபீடம்</text>
          <text x="45" y="185" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="12">சுழுமுனை & ஆணவப் பலி</text>
        </g>

        <line x1="310" y1="100" x2="340" y2="100" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>

        <!-- Step 3: Nandi -->
        <g transform="translate(360, 50)">
          <ellipse cx="40" cy="80" rx="25" ry="18" fill="rgba(255,255,255,0.08)" stroke="#cbd5e1" stroke-width="1.5"/>
          <circle cx="58" cy="72" r="10" fill="rgba(255,255,255,0.15)" stroke="#cbd5e1" stroke-width="1"/>
          <text x="40" y="155" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="14" font-weight="bold">நந்தி தேவர்</text>
          <text x="40" y="175" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="12">ஆன்மா (ஜீவாத்மா)</text>
        </g>

        <line x1="450" y1="100" x2="480" y2="100" stroke="rgba(255,255,255,0.25)" stroke-width="2"/>

        <!-- Step 4: Garbhagriha / Sivalinga -->
        <g transform="translate(500, 35)">
          <rect x="20" y="25" width="70" height="115" rx="6" fill="rgba(212,175,55,0.1)" stroke="rgba(212,175,55,0.4)" stroke-width="1.5"/>
          <ellipse cx="55" cy="100" rx="22" ry="8" fill="#334155"/>
          <path d="M 43 100 L 43 75 Q 55 60 67 75 L 67 100 Z" fill="#1e293b" stroke="#cbd5e1" stroke-width="1"/>
          <circle cx="55" cy="45" r="4" fill="#ffd700" filter="drop-shadow(0 0 6px #ffd700)"/>
          <text x="55" y="170" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="14" font-weight="bold">கருவறை (சிவலிங்கம்)</text>
          <text x="55" y="190" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="12">இதயம் / சிவ பரம்பொருள்</text>
        </g>

        <text x="350" y="230" text-anchor="middle" fill="#e2e8f0" font-family="'Mukta Malar', sans-serif" font-size="13">"உடம்பே ஆலயம், வாய் கோபுர வாசல், ஜீவனே சிவலிங்கம்" — திருமூலர் திருமந்திரம்</text>
      </svg>
      <div class="diagram-footer">
        <p><strong>விளக்கம்:</strong> கோயிலின் வெளிப்புற ராஜகோபுரத்தைக் கண்டு வணங்குவது பாதம் தொழுவதாகும். பலிபீடத்தில் நம் சுயநலத்தை பலியிட்டு, நந்தியின் பணிவோடு கருவறையில் உள்ள சிவனைத் தரிசிக்க வேண்டும்.</p>
      </div>
    </div>
    """

def generate_svg_ganesha():
    """Diagram showing Pranava Omkara & Ganesha Iconography."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>விநாயகப் பெருமானின் பிரணவ (ஓம்) தத்துவ விளக்கம்</h4>
      </div>
      <svg viewBox="0 0 700 240" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="240" rx="12" fill="rgba(11,15,22,0.9)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- Large Omkara Silhouette -->
        <g transform="translate(80, 20)">
          <circle cx="100" cy="90" r="60" fill="rgba(255,255,255,0.03)" stroke="rgba(212,175,55,0.3)" stroke-width="1.5"/>
          <text x="100" y="115" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="65" font-weight="bold">ௐ</text>
          <text x="100" y="175" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="13">பிரணவ வடிவம்</text>
        </g>

        <!-- Right Side: 4 Pillars of Iconography -->
        <g transform="translate(290, 30)">
          <rect x="0" y="0" width="370" height="35" rx="6" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.08)"/>
          <text x="15" y="23" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">🐘 யானை முகம்:</text>
          <text x="125" y="23" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="12">மகத்தான ஞானம் & பேராற்றலின் குறியீடு</text>

          <rect x="0" y="45" width="370" height="35" rx="6" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.08)"/>
          <text x="15" y="68" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">👂 முறம் போன்ற காதுகள்:</text>
          <text x="160" y="68" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="12">நல்ல சொற்களை மட்டுமே கேட்டல் (சிரவணம்)</text>

          <rect x="0" y="90" width="370" height="35" rx="6" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.08)"/>
          <text x="15" y="113" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">✒️ ஒடிந்த தந்தம்:</text>
          <text x="135" y="113" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="12">தன்னலத்தை ஈந்து பாரதம் எழுதிய தியாகம்</text>

          <rect x="0" y="135" width="370" height="35" rx="6" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.08)"/>
          <text x="15" y="158" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">🍯 திருக்கரத்து மோதகம்:</text>
          <text x="165" y="158" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="12">ஆன்மாவின் அக இன்பம் (பேரானந்தம்)</text>
        </g>
        
        <text x="350" y="220" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="12">"ஐந்து கரத்தனை ஆனை முகத்தனை இந்தின் இளம்பிறை போலும் எயிற்றனை" — திருமந்திரம்</text>
      </svg>
      <div class="diagram-footer">
        <p><strong>பாடப் பயன்:</strong> முழுமுதற் கடவுளான விநாயகரை வணங்குவது கல்வியில் தொடக்கத் தடைகளை நீக்கி, கூர்மையான புத்தியையும் தியாக உள்ளத்தையும் உருவாக்குகிறது.</p>
      </div>
    </div>
    """

def generate_svg_panchakshara():
    """Diagram showing Panchakshara (Na-Ma-Si-Va-Ya) and 5 Elements."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>திருவைந்தெழுத்து (நமசிவாய) & பஞ்சபூத தத்துவ விளக்கம்</h4>
      </div>
      <svg viewBox="0 0 700 240" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="240" rx="12" fill="rgba(11,15,22,0.9)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- 5 Circles for Na-Ma-Si-Va-Ya with balanced semantic colors -->
        <!-- 1: Na -->
        <g transform="translate(50, 40)">
          <circle cx="50" cy="50" r="42" fill="rgba(255,255,255,0.04)" stroke="#94a3b8" stroke-width="1.8"/>
          <text x="50" y="58" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="28" font-weight="bold">ந</text>
          <text x="50" y="115" text-anchor="middle" fill="#e2e8f0" font-family="'Mukta Malar', sans-serif" font-size="13">திரோதான சக்தி</text>
          <text x="50" y="135" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">நிலம் (பூமி)</text>
        </g>

        <!-- 2: Ma -->
        <g transform="translate(170, 40)">
          <circle cx="50" cy="50" r="42" fill="rgba(230,57,70,0.15)" stroke="#e63946" stroke-width="1.8"/>
          <text x="50" y="58" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="28" font-weight="bold">ம</text>
          <text x="50" y="115" text-anchor="middle" fill="#e2e8f0" font-family="'Mukta Malar', sans-serif" font-size="13">மலம் (ஆணவம்)</text>
          <text x="50" y="135" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">நீர் (அப்பு)</text>
        </g>

        <!-- 3: Si -->
        <g transform="translate(290, 40)">
          <circle cx="50" cy="50" r="44" fill="rgba(255,255,255,0.1)" stroke="#f8fafc" stroke-width="2.5" filter="drop-shadow(0 0 10px rgba(255,255,255,0.4))"/>
          <text x="50" y="60" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="32" font-weight="bold">சி</text>
          <text x="50" y="115" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="14" font-weight="bold">சிவபெருமான்</text>
          <text x="50" y="135" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">தீ (தேயு)</text>
        </g>

        <!-- 4: Va -->
        <g transform="translate(410, 40)">
          <circle cx="50" cy="50" r="42" fill="rgba(42,157,143,0.15)" stroke="#2a9d8f" stroke-width="1.8"/>
          <text x="50" y="58" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="28" font-weight="bold">வா</text>
          <text x="50" y="115" text-anchor="middle" fill="#e2e8f0" font-family="'Mukta Malar', sans-serif" font-size="13">திருவருள் சக்தி</text>
          <text x="50" y="135" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">காற்று (வாயு)</text>
        </g>

        <!-- 5: Ya -->
        <g transform="translate(530, 40)">
          <circle cx="50" cy="50" r="42" fill="rgba(100,149,237,0.15)" stroke="#6495ed" stroke-width="1.8"/>
          <text x="50" y="58" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="28" font-weight="bold">ய</text>
          <text x="50" y="115" text-anchor="middle" fill="#e2e8f0" font-family="'Mukta Malar', sans-serif" font-size="13">ஆன்மா (ஜீவன்)</text>
          <text x="50" y="135" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">ஆகாயம் (வெளி)</text>
        </g>

        <text x="350" y="215" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="13">"நமச்சிவாய வாழ்க நாதன் தாள் வாழ்க" — திருவாசகம் சிவபுராணம்</text>
      </svg>
      <div class="diagram-footer">
        <p><strong>தியான முறை:</strong> 'சி' மற்றும் 'வா' ஆகியவை இறைவனையும் அருளையும் குறிக்கின்றன. 'ய' ஆகிய ஆன்மா 'ந' மற்றும் 'ம' என்ற மாயை மலங்களை விடுத்து, 'சி'யோடு இணைய வேண்டும்.</p>
      </div>
    </div>
    """

def generate_svg_pancha_yajna():
    """Diagram showing the 5 Great Daily Vedic Sacrifices (Pancha Maha Yajna)."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>பஞ்ச மகா யாகங்கள் — மாணவரின் 5 அன்றாட அறக்கடமைகள்</h4>
      </div>
      <svg viewBox="0 0 700 240" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="240" rx="12" fill="rgba(11,15,22,0.9)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <g transform="translate(25, 30)">
          <!-- 1. Deva Yajna -->
          <rect x="0" y="0" width="120" height="140" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.15)"/>
          <text x="60" y="28" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">1. தேவ யாகம்</text>
          <text x="60" y="55" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">இறை வழிபாடு</text>
          <text x="60" y="75" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">விளக்கேற்றுதல்,</text>
          <text x="60" y="92" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">மந்திரம் &amp; பூசை</text>
          <text x="60" y="120" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="10">கடவுள் நன்றி</text>

          <!-- 2. Pitru Yajna -->
          <rect x="130" y="0" width="120" height="140" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.15)"/>
          <text x="190" y="28" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">2. பித்ரு யாகம்</text>
          <text x="190" y="55" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">பெற்றோர் சேவை</text>
          <text x="190" y="75" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">முன்னோர் வழிபாடு,</text>
          <text x="190" y="92" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">முதியோர் நலம்</text>
          <text x="190" y="120" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="10">குடும்ப அறம்</text>

          <!-- 3. Brahma Yajna -->
          <rect x="260" y="0" width="120" height="140" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.15)"/>
          <text x="320" y="28" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">3. பிரம்ம யாகம்</text>
          <text x="320" y="55" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">வேத &amp; நூல் கற்றல்</text>
          <text x="320" y="75" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">நூல்கள் ஓதுதல்,</text>
          <text x="320" y="92" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">ஞானம் பகிர்தல்</text>
          <text x="320" y="120" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="10">ரிஷி கடன்</text>

          <!-- 4. Manushya Yajna -->
          <rect x="390" y="0" width="120" height="140" rx="8" fill="rgba(42,157,143,0.1)" stroke="rgba(42,157,143,0.3)"/>
          <text x="450" y="28" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">4. மனுஷ்ய யாகம்</text>
          <text x="450" y="55" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">விருந்தோம்பல்</text>
          <text x="450" y="75" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">வறியவர்க்கு உணவு,</text>
          <text x="450" y="92" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">இன்சொல் கூறல்</text>
          <text x="450" y="120" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="10">மனிதநேயம்</text>

          <!-- 5. Bhuta Yajna -->
          <rect x="520" y="0" width="120" height="140" rx="8" fill="rgba(42,157,143,0.1)" stroke="rgba(42,157,143,0.3)"/>
          <text x="580" y="28" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">5. பூத யாகம்</text>
          <text x="580" y="55" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">உயிர் கருணை</text>
          <text x="580" y="75" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">பறவை, பசு, எறும்பு</text>
          <text x="580" y="92" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">மரம் வளர்த்தல்</text>
          <text x="580" y="120" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="10">சுற்றுச்சூழல்</text>
        </g>

        <text x="350" y="210" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="12">இந்த ஐந்து யாகங்களை நாள்தோறும் செய்யும் மனிதனுக்கு எந்தப் பாவமும் அண்டாது — வேத நீதி</text>
      </svg>
      <div class="diagram-footer">
        <p><strong>தினசரி கடமை:</strong> யாகம் என்பது வெறும் தீ வளர்ப்பது மட்டுமல்ல; நம் வாழ்வை பிற உயிர்களின் நன்மைக்காக அர்ப்பணிப்பதே உண்மையான வேத யாகமாகும்.</p>
      </div>
    </div>
    """

def generate_svg_pati_pasu_pasam():
    """Diagram showing Pati-Pasu-Pasam Triangle and Grace."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>சைவ சித்தாந்த முப்பொருள் உண்மை — பதி, பசு, பாசம் வரைபடம்</h4>
      </div>
      <svg viewBox="0 0 700 260" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="260" rx="12" fill="rgba(11,15,22,0.9)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        <polygon points="350,45 160,205 540,205" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2" stroke-dasharray="4,4"/>
        
        <!-- Pati -->
        <circle cx="350" cy="45" r="32" fill="rgba(255,255,255,0.08)" stroke="#f8fafc" stroke-width="2"/>
        <text x="350" y="42" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="16" font-weight="bold">பதி</text>
        <text x="350" y="60" text-anchor="middle" fill="#cbd5e1" font-family="'Outfit', sans-serif" font-size="11">SIVA (God)</text>
        
        <!-- Pasu -->
        <circle cx="160" cy="205" r="30" fill="rgba(42,157,143,0.15)" stroke="#2a9d8f" stroke-width="2"/>
        <text x="160" y="202" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="16" font-weight="bold">பசு</text>
        <text x="160" y="220" text-anchor="middle" fill="#cbd5e1" font-family="'Outfit', sans-serif" font-size="11">SOUL (Jiva)</text>
        
        <!-- Pasam -->
        <circle cx="540" cy="205" r="30" fill="rgba(230,57,70,0.15)" stroke="#e63946" stroke-width="2"/>
        <text x="540" y="202" text-anchor="middle" fill="#f87171" font-family="'Mukta Malar', sans-serif" font-size="16" font-weight="bold">பாசம்</text>
        <text x="540" y="220" text-anchor="middle" fill="#cbd5e1" font-family="'Outfit', sans-serif" font-size="11">BONDS (3 Malas)</text>
        
        <!-- Grace -->
        <circle cx="350" cy="150" r="26" fill="rgba(56,189,248,0.15)" stroke="#38bdf8" stroke-width="1.5"/>
        <text x="350" y="148" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">திருவருள்</text>
        <text x="350" y="164" text-anchor="middle" fill="#e2e8f0" font-family="'Outfit', sans-serif" font-size="10">Grace</text>
        
        <text x="160" y="248" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="12">எண்ணற்ற ஆன்மாக்கள்</text>
        <text x="540" y="248" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="12">ஆணவம், கன்மம், மாயை</text>
        <text x="350" y="18" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="12">முழுமுதற்கடவுள் • நித்தியப் பொருள்</text>
      </svg>
      <div class="diagram-footer">
        <p><strong>தத்துவ விளக்கம்:</strong> பசுவாகிய ஆன்மா பாசக் கயிற்றால் பிணிக்கப்பட்டுள்ளது. பதியாகிய சிவபெருமான் தனது திருவருள் ஒளியால் பாசக் கட்டுகளை அவிழ்த்து ஆன்மாவைத் தன்னோடு இணைத்து முக்தியளிக்கிறார்.</p>
      </div>
    </div>
    """

def generate_svg_naalvar_paths():
    """Diagram showing Naalvar (4 Saints) and the 4 Spiritual Paths."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>சைவ நால்வர் & நான்கு முக்தி மார்க்கங்கள்</h4>
      </div>
      <svg viewBox="0 0 700 240" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="240" rx="12" fill="rgba(11,15,22,0.9)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <g transform="translate(30, 30)">
          <rect width="145" height="150" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.12)"/>
          <text x="72" y="32" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="15" font-weight="bold">அப்பர் சுவாமிகள்</text>
          <text x="72" y="55" text-anchor="middle" fill="#e2e8f0" font-family="'Mukta Malar', sans-serif" font-size="13">சரியை நெறி</text>
          <text x="72" y="75" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="12">தாச மார்க்கம்</text>
          <text x="72" y="100" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">தொண்டு செய்தல்</text>
          <text x="72" y="118" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">(உழவாரப் பணி)</text>
          <rect x="25" y="128" width="95" height="18" rx="4" fill="rgba(255,255,255,0.06)"/>
          <text x="72" y="141" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">சாலோக முக்தி</text>
        </g>

        <g transform="translate(195, 30)">
          <rect width="145" height="150" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.12)"/>
          <text x="72" y="32" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="15" font-weight="bold">சம்பந்த சுவாமிகள்</text>
          <text x="72" y="55" text-anchor="middle" fill="#e2e8f0" font-family="'Mukta Malar', sans-serif" font-size="13">கிரியை நெறி</text>
          <text x="72" y="75" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="12">சற்புத்திர மார்க்கம்</text>
          <text x="72" y="100" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">மகன் போன்ற பக்தி</text>
          <text x="72" y="118" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">(வழிபாட்டு நெறி)</text>
          <rect x="25" y="128" width="95" height="18" rx="4" fill="rgba(255,255,255,0.06)"/>
          <text x="72" y="141" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">சாமீப முக்தி</text>
        </g>

        <g transform="translate(360, 30)">
          <rect width="145" height="150" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.12)"/>
          <text x="72" y="32" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="15" font-weight="bold">சுந்தர சுவாமிகள்</text>
          <text x="72" y="55" text-anchor="middle" fill="#e2e8f0" font-family="'Mukta Malar', sans-serif" font-size="13">யோக நெறி</text>
          <text x="72" y="75" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="12">சக மார்க்கம்</text>
          <text x="72" y="100" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">தோழமைப் பக்தி</text>
          <text x="72" y="118" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">(அகத் தியானம்)</text>
          <rect x="25" y="128" width="95" height="18" rx="4" fill="rgba(255,255,255,0.06)"/>
          <text x="72" y="141" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">சாரூப முக்தி</text>
        </g>

        <g transform="translate(525, 30)">
          <rect width="145" height="150" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.12)"/>
          <text x="72" y="32" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="15" font-weight="bold">மாணிக்கவாசகர்</text>
          <text x="72" y="55" text-anchor="middle" fill="#e2e8f0" font-family="'Mukta Malar', sans-serif" font-size="13">ஞான நெறி</text>
          <text x="72" y="75" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="12">சன்மார்க்கம்</text>
          <text x="72" y="100" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">பேரன்பு &amp; ஞானம்</text>
          <text x="72" y="118" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">(திருவாசக உருக்கம்)</text>
          <rect x="25" y="128" width="95" height="18" rx="4" fill="rgba(255,255,255,0.06)"/>
          <text x="72" y="141" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">சாயுச்சிய முக்தி</text>
        </g>

        <text x="350" y="215" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="12">தொண்டு, வழிபாடு, யோகம், ஞானம் ஆகிய நான்கும் படிப்படியாக ஆன்மாவை முக்தியில் சேர்க்கும் படிக்கட்டுகளாகும்.</text>
      </svg>
      <div class="diagram-footer">
        <p><strong>படிமுறை நெறி:</strong> சாலோகம் (இறை உலகம் அடைதல்), சாமீபம் (இறைவனருகே இருத்தல்), சாரூபம் (இறைவடிவம் பெறுதல்), சாயுச்சியம் (இறைவனோடு இரண்டறக் கலத்தல்) என்ற நான்கு நிலைகளை நால்வர் வழிகாட்டுகின்றனர்.</p>
      </div>
    </div>
    """

def generate_svg_nataraja():
    """Diagram showing Nataraja Ananda Tandava Iconography & Cosmic Functions."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>நடராஜ பெருமானின் ஆனந்த தாண்டவம் & ஐந்தொழில் தத்துவம்</h4>
      </div>
      <svg viewBox="0 0 700 270" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="270" rx="12" fill="rgba(11,15,22,0.9)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        <circle cx="350" cy="130" r="100" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2" stroke-dasharray="6,4"/>
        
        <circle cx="350" cy="80" r="14" fill="#f8fafc"/>
        <line x1="350" y1="94" x2="350" y2="155" stroke="#cbd5e1" stroke-width="4"/>
        
        <line x1="350" y1="105" x2="280" y2="75" stroke="#cbd5e1" stroke-width="3"/>
        <circle cx="275" cy="73" r="8" fill="#38bdf8"/>
        <line x1="350" y1="105" x2="420" y2="75" stroke="#cbd5e1" stroke-width="3"/>
        <circle cx="425" cy="73" r="8" fill="#e63946"/>
        <line x1="350" y1="120" x2="310" y2="120" stroke="#cbd5e1" stroke-width="3"/>
        <line x1="350" y1="120" x2="385" y2="145" stroke="#cbd5e1" stroke-width="3"/>
        
        <line x1="350" y1="155" x2="350" y2="195" stroke="#cbd5e1" stroke-width="3.5"/>
        <line x1="350" y1="155" x2="315" y2="175" stroke="#cbd5e1" stroke-width="3.5"/>
        
        <ellipse cx="350" cy="202" rx="25" ry="7" fill="rgba(255,255,255,0.1)" stroke="#94a3b8" stroke-width="1"/>

        <!-- Crisp white text for key labels -->
        <text x="80" y="65" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">1. உடுக்கை: <tspan fill="#38bdf8">சிருஷ்டி</tspan> (படைத்தல்)</text>
        <text x="80" y="115" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">2. அபய கரம்: <tspan fill="#2dd4bf">திதி</tspan> (காத்தல்)</text>
        <text x="80" y="210" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">4. முயலகன்: திரோபாவம் (மறைத்தல்)</text>

        <text x="470" y="65" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">3. எரியகழல்: <tspan fill="#f87171">சங்காரம்</tspan> (அழித்தல்)</text>
        <text x="470" y="165" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">5. தூக்கிய திருவடி: <tspan fill="#38bdf8">அனுக்ரகம்</tspan> (முத்தி)</text>

        <text x="350" y="250" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="12">"ஆடிய காலில் அனுக்ரகம் கூட்டி... ஓங்கார வடிவாய் நின்றானே" — உண்மை விளக்கம்</text>
      </svg>
      <div class="diagram-footer">
        <p><strong>விஞ்ஞான &amp; மெஞ்ஞான விளக்கம்:</strong> நடராஜரின் திருநடனம் பிரபஞ்ச அணுக்களின் இடையறாத ஆற்றல் இயக்கத்தை (Cosmic Dance of Energy) விளக்குகிறது என நவீன குவாண்டம் இயற்பியலாளர்கள் போற்றுகின்றனர்.</p>
      </div>
    </div>
    """

def generate_svg_ashtanga_yoga():
    """Diagram showing the 8 limbs of Ashtanga Yoga."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>அட்டாங்க யோகம் — எட்டுப் படிகள் தத்துவ வரைபடம்</h4>
      </div>
      <svg viewBox="0 0 700 230" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="230" rx="12" fill="rgba(11,15,22,0.9)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <g transform="translate(40, 20)">
          <rect x="0" y="140" width="70" height="30" rx="4" fill="rgba(255,255,255,0.04)" stroke="#94a3b8"/>
          <text x="35" y="160" text-anchor="middle" fill="#f8fafc" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">1. இயமம்</text>
          
          <rect x="75" y="120" width="70" height="50" rx="4" fill="rgba(255,255,255,0.06)" stroke="#94a3b8"/>
          <text x="110" y="145" text-anchor="middle" fill="#f8fafc" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">2. நியமம்</text>
          
          <rect x="150" y="100" width="70" height="70" rx="4" fill="rgba(255,255,255,0.08)" stroke="#cbd5e1"/>
          <text x="185" y="130" text-anchor="middle" fill="#f8fafc" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">3. ஆதனம்</text>
          
          <rect x="225" y="80" width="75" height="90" rx="4" fill="rgba(255,255,255,0.1)" stroke="#cbd5e1"/>
          <text x="262" y="115" text-anchor="middle" fill="#f8fafc" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">4. பிராணாயாமம்</text>
          
          <rect x="305" y="60" width="75" height="110" rx="4" fill="rgba(42,157,143,0.15)" stroke="#2a9d8f"/>
          <text x="342" y="100" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">5. பிரத்தியாகாரம்</text>
          
          <rect x="385" y="40" width="75" height="130" rx="4" fill="rgba(42,157,143,0.2)" stroke="#2a9d8f"/>
          <text x="422" y="85" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">6. தாரணை</text>
          
          <rect x="465" y="20" width="75" height="150" rx="4" fill="rgba(42,157,143,0.25)" stroke="#2a9d8f"/>
          <text x="502" y="70" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">7. தியானம்</text>
          
          <rect x="545" y="0" width="75" height="170" rx="4" fill="rgba(56,189,248,0.2)" stroke="#38bdf8"/>
          <text x="582" y="55" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">8. சமாதி</text>
        </g>

        <text x="350" y="208" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="12">வெளி உறுப்புப் பயிற்சிகள் (இயமம்-பிராணாயாமம்) → அக உறுப்புப் பயிற்சிகள் (பிரத்தியாகாரம்-சமாதி)</text>
      </svg>
      <div class="diagram-footer">
        <p><strong>திருமூலர் திருமந்திர நெறி:</strong> நன்னடத்தை, மனக்கட்டுப்பாடு, உடற்பயிற்சி மற்றும் மூச்சுப் பயிற்சியின் வழியாக ஆன்மா சமாதி நிலையை அடைந்து சிவனுடன் ஒன்றிணைவதை அட்டாங்க யோகம் விளக்குகிறது.</p>
      </div>
    </div>
    """

def generate_svg_vedic_dinacharya():
    """Diagram showing the Daily Dharmic Routine (Dinacharya)."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>மாணவர் தினசரி வேத வாழ்வியல் சுழற்சி (தினசரியை - Dinacharya)</h4>
      </div>
      <svg viewBox="0 0 700 240" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="240" rx="12" fill="rgba(11,15,22,0.9)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <g transform="translate(60, 30)">
          <rect x="0" y="0" width="130" height="130" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.15)"/>
          <text x="65" y="30" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">1. பிரம்ம முகூர்த்தம்</text>
          <text x="65" y="55" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">விடியற்காலை எழுதல்</text>
          <text x="65" y="75" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">நீராடல் &amp; திருநீறு</text>
          <text x="65" y="95" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">சூரிய நமஸ்காரம்</text>
        </g>

        <path d="M 200 95 L 225 95" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>

        <g transform="translate(235, 30)">
          <rect x="0" y="0" width="130" height="130" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.15)"/>
          <text x="65" y="30" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">2. குரு &amp; கல்வி</text>
          <text x="65" y="55" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">பெற்றோர் வணக்கம்</text>
          <text x="65" y="75" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">பள்ளிப் பாடம் கற்றல்</text>
          <text x="65" y="95" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">நேர்மை &amp; இன்சொல்</text>
        </g>

        <path d="M 375 95 L 400 95" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>

        <g transform="translate(410, 30)">
          <rect x="0" y="0" width="130" height="130" rx="8" fill="rgba(42,157,143,0.1)" stroke="rgba(42,157,143,0.3)"/>
          <text x="65" y="30" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">3. மாலை சந்தியா</text>
          <text x="65" y="55" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">தீப வழிபாடு</text>
          <text x="65" y="75" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">தேவார திருமுறை பாடுதல்</text>
          <text x="65" y="95" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">தியானம் &amp; அமைதி</text>
        </g>

        <path d="M 550 95 L 575 95" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>

        <g transform="translate(585, 30)">
          <rect x="0" y="0" width="105" height="130" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.15)"/>
          <text x="52" y="30" text-anchor="middle" fill="#f8fafc" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">4. இரவு நிஷ்டை</text>
          <text x="52" y="55" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">சுய பரிசோதனை</text>
          <text x="52" y="75" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">நமசிவாய ஜபம்</text>
          <text x="52" y="95" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">அமைதியான உறக்கம்</text>
        </g>

        <text x="350" y="210" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="13">"காலையும் மாலையும் சிவசிந்தனையோடு வாழும் மாணவன் உலகில் எங்கும் வெல்வான்"</text>
      </svg>
      <div class="diagram-footer">
        <p><strong>வாழ்வியல் நெறிமுறை:</strong> விடியற்காலையில் எழுவது மூளைக்கு புத்துணர்ச்சியையும், மாலையில் திருமுறை ஓதுவது மனதிற்குப் பேரமைதியையும் நல்குகிறது.</p>
      </div>
    </div>
    """

def generate_svg_vedas_tree():
    """Diagram showing the 4 Vedas and Upavedas Tree."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>நான்கு வேதங்கள் & உபவேதங்களின் கட்டமைப்பு மரம்</h4>
      </div>
      <svg viewBox="0 0 700 240" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="240" rx="12" fill="rgba(11,15,22,0.9)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- Root: Sanatana Dharma / Veda -->
        <rect x="275" y="20" width="150" height="35" rx="6" fill="rgba(255,255,255,0.06)" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="350" y="42" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="15" font-weight="bold">அபௌருஷேய வேதம்</text>

        <line x1="310" y1="55" x2="100" y2="90" stroke="rgba(255,255,255,0.25)" stroke-width="1.5"/>
        <line x1="335" y1="55" x2="260" y2="90" stroke="rgba(255,255,255,0.25)" stroke-width="1.5"/>
        <line x1="365" y1="55" x2="440" y2="90" stroke="rgba(255,255,255,0.25)" stroke-width="1.5"/>
        <line x1="390" y1="55" x2="600" y2="90" stroke="rgba(255,255,255,0.25)" stroke-width="1.5"/>

        <!-- 1. Rig Veda -->
        <g transform="translate(30, 90)">
          <rect width="140" height="95" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.12)"/>
          <text x="70" y="26" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="14" font-weight="bold">ரிக் வேதம்</text>
          <text x="70" y="48" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">துதிகள் &amp; மந்திரங்கள்</text>
          <text x="70" y="68" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="11">உபவேதம்: ஆயுர்வேதம்</text>
          <text x="70" y="86" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">(மருத்துவ அறிவியல்)</text>
        </g>

        <!-- 2. Yajur Veda -->
        <g transform="translate(190, 90)">
          <rect width="140" height="95" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.12)"/>
          <text x="70" y="26" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="14" font-weight="bold">யஜுர் வேதம்</text>
          <text x="70" y="48" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">சடங்கு &amp; ஸ்ரீருத்ரம்</text>
          <text x="70" y="68" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="11">உபவேதம்: தனுர்வேதம்</text>
          <text x="70" y="86" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">(தற்காப்பு &amp; ஆட்சி)</text>
        </g>

        <!-- 3. Sama Veda -->
        <g transform="translate(370, 90)">
          <rect width="140" height="95" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.12)"/>
          <text x="70" y="26" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="14" font-weight="bold">சாம வேதம்</text>
          <text x="70" y="48" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">இறை இசை &amp; கானம்</text>
          <text x="70" y="68" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="11">உபவேதம்: காந்தர்வவேதம்</text>
          <text x="70" y="86" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">(இசை &amp; நடனம்)</text>
        </g>

        <!-- 4. Atharva Veda -->
        <g transform="translate(530, 90)">
          <rect width="140" height="95" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.12)"/>
          <text x="70" y="26" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="14" font-weight="bold">அதர்வ வேதம்</text>
          <text x="70" y="48" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">அன்றாட தர்ம வாழ்வியல்</text>
          <text x="70" y="68" text-anchor="middle" fill="#2dd4bf" font-family="'Mukta Malar', sans-serif" font-size="11">உபவேதம்: அர்த்தசாத்திரம்</text>
          <text x="70" y="86" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">(பொருளியல் &amp; சிற்பம்)</text>
        </g>

        <text x="350" y="215" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="12">"வேத நெறி தழைத்தோங்க மிகு சைவத் துறை விளங்க" — சேக்கிழார் சுவாமிகள்</text>
      </svg>
      <div class="diagram-footer">
        <p><strong>தத்துவ விளக்கம்:</strong> வேதங்கள் மனிதனால் இயற்றப்படாத இறைவாக்காகும். அவை ஆன்மீக அறிவையும் (ஞான காண்டம்) அன்றாட வாழ்வியல் நெறிமுறைகளையும் (கர்ம காண்டம்) கற்பிக்கின்றன.</p>
      </div>
    </div>
    """

def generate_svg_karma_wheel():
    """Diagram showing the 3 types of Karma (Sanchita, Prarabdha, Agami)."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>கன்ம வினைக் கோட்பாடு — சஞ்சிதம், பிராரப்தம், ஆகாமியம்</h4>
      </div>
      <svg viewBox="0 0 700 240" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="240" rx="12" fill="rgba(11,15,22,0.9)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <g transform="translate(40, 35)">
          <circle cx="80" cy="70" r="55" fill="rgba(255,255,255,0.04)" stroke="#cbd5e1" stroke-width="1.8"/>
          <text x="80" y="55" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="14" font-weight="bold">1. சஞ்சிதம்</text>
          <text x="80" y="75" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">சேமிக்கப்பட்ட வினை</text>
          <text x="80" y="95" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">(தானியக் களஞ்சியம்)</text>
        </g>

        <path d="M 185 105 L 235 105" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>

        <g transform="translate(245, 35)">
          <circle cx="80" cy="70" r="55" fill="rgba(230,57,70,0.12)" stroke="#e63946" stroke-width="1.8"/>
          <text x="80" y="55" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="14" font-weight="bold">2. பிராரப்தம்</text>
          <text x="80" y="75" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">நுகரப்படும் வினை</text>
          <text x="80" y="95" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">(இப்பிறவி இன்ப துன்பம்)</text>
        </g>

        <path d="M 390 105 L 440 105" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>

        <g transform="translate(450, 35)">
          <circle cx="80" cy="70" r="55" fill="rgba(42,157,143,0.12)" stroke="#2a9d8f" stroke-width="1.8"/>
          <text x="80" y="55" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="14" font-weight="bold">3. ஆகாமியம்</text>
          <text x="80" y="75" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">புதிதாகச் செய்யும் வினை</text>
          <text x="80" y="95" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">(எதிர்கால விதை)</text>
        </g>

        <text x="350" y="210" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="12">நல்ல எண்ணங்களும் சிவபக்தியும் புதிய வினைகள் (ஆகாமியம்) உருவாகாமல் தடுத்து முக்தி தரும்.</text>
      </svg>
      <div class="diagram-footer">
        <p><strong>பாடப் பயன்:</strong> பழைய வினைகளை அமைதியோடு சகித்துக் கொண்டு, நிகழ்காலத்தில் பிறருக்குத் தீங்கிழைக்காமல் நற்செயல்களையே செய்வதன் மூலம் கன்ம சுழற்சியிலிருந்து விடுபடலாம்.</p>
      </div>
    </div>
    """

DIAGRAM_MAP = {
    "thiruneeru": generate_svg_thiruneeru,
    "temple": generate_svg_temple,
    "ganesha": generate_svg_ganesha,
    "panchakshara": generate_svg_panchakshara,
    "pancha_yajna": generate_svg_pancha_yajna,
    "pati_pasu_pasam": generate_svg_pati_pasu_pasam,
    "naalvar": generate_svg_naalvar_paths,
    "nataraja": generate_svg_nataraja,
    "ashtanga_yoga": generate_svg_ashtanga_yoga,
    "dinacharya": generate_svg_vedic_dinacharya,
    "vedas_tree": generate_svg_vedas_tree,
    "karma_wheel": generate_svg_karma_wheel,
}

# Integrate expanded diagram suite
try:
    from visual_diagrams_expanded import EXPANDED_DIAGRAM_MAP
    DIAGRAM_MAP.update(EXPANDED_DIAGRAM_MAP)
except ImportError:
    pass

def get_diagram_for_topic(diagram_key):
    if diagram_key in DIAGRAM_MAP:
        return DIAGRAM_MAP[diagram_key]()
    return generate_svg_vedic_dinacharya()
