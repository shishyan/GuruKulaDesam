# -*- coding: utf-8 -*-
"""
Expanded Visual Diagrams & Infographics for Guru Kula Desam Curriculum
Provides 15 bespoke, high-resolution SVG pedagogical illustrations for all remaining
curriculum learning topics across Grades 2 to 12.

Palette:
  - Celestial Sky Blue (#38bdf8)
  - Sacred Emerald Green (#34d399)
  - Clean Crisp White (#ffffff)
  - Cool Slate (#cbd5e1, #94a3b8)
  - Translucent dark backgrounds (rgba(11,15,22,0.92))
  - Subtle gold / warm accents (avoiding yellow/orange overload)
"""

# ===========================================================================
# 1. Lord Murugan's Jnana Vel & Surasamharam Philosophy
# ===========================================================================
def generate_svg_murugan_vel():
    """Diagram showing Murugan's Jnana Vel structure and Surasamharam philosophy."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>முருகனின் ஞானவேல் தத்துவம் &amp; சூரசம்ஹார அகப்பொருள்</h4>
      </div>
      <svg viewBox="0 0 700 240" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="velBladeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#ffffff"/>
            <stop offset="50%" stop-color="#38bdf8"/>
            <stop offset="100%" stop-color="#0284c7"/>
          </linearGradient>
          <linearGradient id="velShaftGrad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#38bdf8"/>
            <stop offset="50%" stop-color="#cbd5e1"/>
            <stop offset="100%" stop-color="#38bdf8"/>
          </linearGradient>
          <filter id="velGlow" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="5" result="blur"/>
            <feComposite in="SourceGraphic" in2="blur" operator="over"/>
          </filter>
        </defs>
        <rect width="700" height="240" rx="12" fill="rgba(11,15,22,0.92)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- Left: Jnana Vel Graphic -->
        <g transform="translate(60, 20)">
          <!-- Aura behind Vel -->
          <ellipse cx="90" cy="85" rx="60" ry="75" fill="rgba(56,189,248,0.06)" filter="url(#velGlow)"/>
          
          <!-- Vel Shaft -->
          <line x1="90" y1="95" x2="90" y2="195" stroke="url(#velShaftGrad)" stroke-width="5" stroke-linecap="round"/>
          <circle cx="90" cy="195" r="5" fill="#38bdf8"/>
          
          <!-- Vel Blade (Leaf shape) -->
          <path d="M 90 25 C 65 50 60 95 80 110 L 90 118 L 100 110 C 120 95 115 50 90 25 Z" 
                fill="url(#velBladeGrad)" stroke="#ffffff" stroke-width="2" filter="drop-shadow(0 0 8px rgba(56,189,248,0.8))"/>
          
          <!-- Central spine of Vel -->
          <line x1="90" y1="28" x2="90" y2="115" stroke="#ffffff" stroke-width="2"/>
          <circle cx="90" cy="45" r="3" fill="#ffffff"/>
          
          <!-- Tip Pointer -->
          <line x1="90" y1="25" x2="165" y2="25" stroke="rgba(255,255,255,0.3)" stroke-dasharray="2,2"/>
          <text x="175" y="29" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">கூர்மை: <tspan fill="#ffffff">நுண்ணறிவு (Discernment)</tspan></text>
          
          <!-- Blade Pointer -->
          <line x1="110" y1="75" x2="165" y2="70" stroke="rgba(255,255,255,0.3)" stroke-dasharray="2,2"/>
          <text x="175" y="74" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">அகலம்: <tspan fill="#ffffff">விசாலாறிவு (Broad Intellect)</tspan></text>
          
          <!-- Shaft Pointer -->
          <line x1="95" y1="150" x2="165" y2="120" stroke="rgba(255,255,255,0.3)" stroke-dasharray="2,2"/>
          <text x="175" y="124" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">நீளம்: <tspan fill="#ffffff">ஆழ்ந்தறிவு (Profound Depth)</tspan></text>
        </g>

        <!-- Right: Surasamharam & Transformations -->
        <g transform="translate(370, 25)">
          <rect x="0" y="5" width="295" height="185" rx="10" fill="rgba(255,255,255,0.03)" stroke="rgba(56,189,248,0.25)" stroke-width="1"/>
          
          <text x="147" y="30" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="14" font-weight="bold">சூரசம்ஹாரத்தின் மெய்ஞ்ஞானத் தத்துவம்</text>
          
          <!-- Peacock transformed -->
          <g transform="translate(18, 45)">
            <circle cx="28" cy="28" r="24" fill="rgba(52,211,153,0.12)" stroke="#34d399" stroke-width="1.5"/>
            <text x="28" y="34" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="18">🦚</text>
            <text x="65" y="24" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">மயில் வாகனம்</text>
            <text x="65" y="42" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">அகங்காரம் அடங்கி சரணடைதல் (Ego Subdued)</text>
          </g>
          
          <!-- Rooster transformed -->
          <g transform="translate(18, 105)">
            <circle cx="28" cy="28" r="24" fill="rgba(56,189,248,0.12)" stroke="#38bdf8" stroke-width="1.5"/>
            <text x="28" y="34" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="18">🚩</text>
            <text x="65" y="24" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">சேவல் கொடி</text>
            <text x="65" y="42" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="11">ஓம் எனும் பிரணவ நாதப் பிரகடனம் (Pranava Nada)</text>
          </g>

          <path d="M 20 168 L 275 168" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
          <text x="147" y="180" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">அசுரனை அழிக்காமல் ஆட்கொண்டு அருள் புரிந்த கருணை நெறி</text>
        </g>
      </svg>
      <div class="diagram-footer">
        <p><strong>தத்துவக் குறிப்பு:</strong> வேல் என்பது பராசக்தியால் முருகப்பெருமானுக்கு அளிக்கப்பட்ட ஞானசக்தி. கூர்மையான, அகன்ற, ஆழ்ந்த அறிவே அஞ்ஞானத்தை வென்று ஆன்மாவை மலரச் செய்யும் கருவியாகும்.</p>
      </div>
    </div>
    """

# ===========================================================================
# 2. Divine Mother Parasakthi, Sri Chakra & Kundalini Shakthi
# ===========================================================================
def generate_svg_sakthi_srichakra():
    """Diagram showing Sri Chakra 9 interlocking triangles, Bindu, and Kundalini flow."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>ஸ்ரீ சக்கர ராஜம் &amp; குண்டலினி யோக சக்தி விளக்கம்</h4>
      </div>
      <svg viewBox="0 0 700 250" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <filter id="binduGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="4" result="blur"/>
            <feComposite in="SourceGraphic" in2="blur" operator="over"/>
          </filter>
        </defs>
        <rect width="700" height="250" rx="12" fill="rgba(11,15,22,0.92)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- Left: Sri Chakra Sacred Geometry -->
        <g transform="translate(130, 125)">
          <!-- Outer Bhupura square gates -->
          <rect x="-95" y="-95" width="190" height="190" fill="none" stroke="rgba(56,189,248,0.4)" stroke-width="1.5"/>
          <rect x="-85" y="-85" width="170" height="170" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>
          
          <!-- Concentric Petal Rings -->
          <circle cx="0" cy="0" r="72" fill="none" stroke="#34d399" stroke-width="1" stroke-dasharray="4,2"/>
          <circle cx="0" cy="0" r="60" fill="rgba(56,189,248,0.04)" stroke="#38bdf8" stroke-width="1"/>
          
          <!-- 4 Shiva Triangles (Pointing UP) in Blue -->
          <polygon points="0,-52 -45,26 45,26" fill="none" stroke="#38bdf8" stroke-width="1.8"/>
          <polygon points="0,-42 -40,36 40,36" fill="none" stroke="#38bdf8" stroke-width="1.5"/>
          <polygon points="0,-32 -32,20 32,20" fill="none" stroke="#38bdf8" stroke-width="1.2"/>
          <polygon points="0,-22 -24,14 24,14" fill="none" stroke="#38bdf8" stroke-width="1"/>
          
          <!-- 5 Shakthi Triangles (Pointing DOWN) in Emerald -->
          <polygon points="0,52 -46,-26 46,-26" fill="none" stroke="#34d399" stroke-width="1.8"/>
          <polygon points="0,44 -38,-20 38,-20" fill="none" stroke="#34d399" stroke-width="1.5"/>
          <polygon points="0,35 -30,-14 30,-14" fill="none" stroke="#34d399" stroke-width="1.2"/>
          <polygon points="0,25 -22,-8 22,-8" fill="none" stroke="#34d399" stroke-width="1"/>
          <polygon points="0,15 -14,-4 14,-4" fill="none" stroke="#34d399" stroke-width="1"/>
          
          <!-- Central Maha Bindu -->
          <circle cx="0" cy="0" r="4.5" fill="#ffffff" filter="url(#binduGlow)"/>
          
          <text x="0" y="112" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">ஸ்ரீ சக்கரம் (9 யோனி முக்கோணங்கள் = 43 சக்கரக் கோணங்கள்)</text>
        </g>

        <!-- Center arrow bridge -->
        <g transform="translate(265, 120)">
          <line x1="0" y1="0" x2="45" y2="0" stroke="rgba(255,255,255,0.4)" stroke-width="2" stroke-dasharray="3,3"/>
          <polygon points="45,-4 52,0 45,4" fill="#34d399"/>
        </g>

        <!-- Right: Kundalini Shakthi Column & Correspondence -->
        <g transform="translate(340, 25)">
          <rect x="0" y="0" width="325" height="200" rx="10" fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
          
          <text x="162" y="24" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="13.5" font-weight="bold">பிரபஞ்ச ஸ்ரீ சக்கரமும் மனித உடலும்</text>
          
          <g transform="translate(20, 42)">
            <circle cx="15" cy="18" r="10" fill="rgba(56,189,248,0.15)" stroke="#38bdf8" stroke-width="1.5"/>
            <text x="15" y="22" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="bold">1</text>
            <text x="35" y="15" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">மகாபிந்து (Maha Bindu)</text>
            <text x="35" y="30" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10.5">சிவ-சக்தி சமரசம் / சஹஸ்ரார பேரொளி</text>
          </g>

          <g transform="translate(20, 82)">
            <circle cx="15" cy="18" r="10" fill="rgba(52,211,153,0.15)" stroke="#34d399" stroke-width="1.5"/>
            <text x="15" y="22" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="bold">2</text>
            <text x="35" y="15" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">நவாவரணம் (9 திருச்சுற்றுகள்)</text>
            <text x="35" y="30" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10.5">பூபுர வாயில்கள் முதல் உள்மையம் வரை 9 ஆன்ம நிலைகள்</text>
          </g>

          <g transform="translate(20, 122)">
            <circle cx="15" cy="18" r="10" fill="rgba(255,255,255,0.1)" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="15" y="22" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="bold">3</text>
            <text x="35" y="15" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">குண்டலினி பிரவேசம் (Kundalini)</text>
            <text x="35" y="30" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10.5">மூலாதாரத்தில் உறங்கும் சக்தி சுழுமுனை வழி மேல்நோக்கி எழுதல்</text>
          </g>

          <rect x="15" y="162" width="295" height="26" rx="5" fill="rgba(56,189,248,0.08)"/>
          <text x="162" y="179" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">"அண்டத்தில் உள்ளதே பிண்டம்; பிண்டத்தில் உள்ளதே அண்டம்"</text>
        </g>
      </svg>
      <div class="diagram-footer">
        <p><strong>விளக்கம்:</strong> ஸ்ரீ சக்கரம் அகிலத்தின் தோற்றம், நிலைபேறு, ஒடுக்கத்தின் வரைபடம். 4 மேல்நோக்கிய சிவ முக்கோணங்களும் 5 கீழ்நோக்கிய சக்தி முக்கோணங்களும் இணைந்து உயிர்களின் ஆன்ம எழுச்சியை விளக்குகின்றன.</p>
      </div>
    </div>
    """

# ===========================================================================
# 3. Vallalar's Arutperunjothi & 7 Curtains of Maya
# ===========================================================================
def generate_svg_vallalar_jyothi():
    """Diagram showing Arutperunjothi Agaval and the 7 Curtains of Maya dissolving."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>அருட்பெருஞ்ஜோதி &amp; மாயையின் ஏழு திரைகள் நீங்கும் தத்துவம்</h4>
      </div>
      <svg viewBox="0 0 700 245" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <radialGradient id="jyothiCore" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#ffffff"/>
            <stop offset="35%" stop-color="#fef08a"/>
            <stop offset="70%" stop-color="#38bdf8"/>
            <stop offset="100%" stop-color="rgba(11,15,22,0)"/>
          </radialGradient>
        </defs>
        <rect width="700" height="245" rx="12" fill="rgba(11,15,22,0.92)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- Left: 7 Curtains (Layered Screens) -->
        <g transform="translate(30, 25)">
          <text x="150" y="16" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">வடலூர் சத்திய ஞான சபை — 7 மாயா திரைகள்</text>
          
          <!-- Screen 1: Black -->
          <rect x="0" y="30" width="300" height="20" rx="4" fill="rgba(30,41,59,0.85)" stroke="#475569" stroke-width="1"/>
          <text x="12" y="44" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">1. கருப்புத் திரை</text>
          <text x="288" y="44" text-anchor="end" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10.5">மாயா சக்தி (அறியாமை மறைப்பு)</text>

          <!-- Screen 2: Blue -->
          <rect x="0" y="54" width="300" height="20" rx="4" fill="rgba(30,58,138,0.8)" stroke="#3b82f6" stroke-width="1"/>
          <text x="12" y="68" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">2. நீலத் திரை</text>
          <text x="288" y="68" text-anchor="end" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10.5">கிரியா சக்தி (செயல் மயக்கம்)</text>

          <!-- Screen 3: Green -->
          <rect x="0" y="78" width="300" height="20" rx="4" fill="rgba(6,95,70,0.8)" stroke="#34d399" stroke-width="1"/>
          <text x="12" y="92" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">3. பச்சைத் திரை</text>
          <text x="288" y="92" text-anchor="end" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10.5">பராசக்தி (பிரபஞ்ச விகற்பம்)</text>

          <!-- Screen 4: Red -->
          <rect x="0" y="102" width="300" height="20" rx="4" fill="rgba(153,27,27,0.8)" stroke="#f87171" stroke-width="1"/>
          <text x="12" y="116" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">4. சிவப்புத் திரை</text>
          <text x="288" y="116" text-anchor="end" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10.5">இச்சா சக்தி (ஆசை மயக்கம்)</text>

          <!-- Screen 5: Golden -->
          <rect x="0" y="126" width="300" height="20" rx="4" fill="rgba(180,83,9,0.7)" stroke="#fbbf24" stroke-width="1"/>
          <text x="12" y="140" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">5. பொன் திரை</text>
          <text x="288" y="140" text-anchor="end" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10.5">ஞான சக்தி (அறிவுப் பேத மறைப்பு)</text>

          <!-- Screen 6: White -->
          <rect x="0" y="150" width="300" height="20" rx="4" fill="rgba(248,250,252,0.2)" stroke="#e2e8f0" stroke-width="1"/>
          <text x="12" y="164" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">6. வெண்மைத் திரை</text>
          <text x="288" y="164" text-anchor="end" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10.5">ஆதி சக்தி (நுட்ப மறைப்பு)</text>

          <!-- Screen 7: Mixed -->
          <rect x="0" y="174" width="300" height="20" rx="4" fill="rgba(147,51,234,0.3)" stroke="#c084fc" stroke-width="1"/>
          <text x="12" y="188" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">7. சித்திரத் திரை</text>
          <text x="288" y="188" text-anchor="end" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10.5">சிற்சக்தி (காரண அவஸ்தை)</text>
        </g>

        <!-- Right: Radiant Arutperunjothi Grace Light -->
        <g transform="translate(360, 20)">
          <!-- Dissolving arrows -->
          <path d="M 0 105 L 45 105" stroke="#34d399" stroke-width="2.5" stroke-dasharray="4,3"/>
          <polygon points="45,100 55,105 45,110" fill="#34d399"/>
          
          <rect x="65" y="10" width="250" height="195" rx="10" fill="rgba(56,189,248,0.03)" stroke="rgba(56,189,248,0.3)" stroke-width="1"/>
          
          <!-- Radiating Light -->
          <circle cx="190" cy="85" r="55" fill="url(#jyothiCore)"/>
          <circle cx="190" cy="85" r="14" fill="#ffffff" filter="drop-shadow(0 0 10px #ffffff)"/>
          
          <!-- Beams -->
          <line x1="190" y1="20" x2="190" y2="45" stroke="#ffffff" stroke-width="2"/>
          <line x1="190" y1="125" x2="190" y2="150" stroke="#ffffff" stroke-width="2"/>
          <line x1="130" y1="85" x2="155" y2="85" stroke="#ffffff" stroke-width="2"/>
          <line x1="225" y1="85" x2="250" y2="85" stroke="#ffffff" stroke-width="2"/>
          
          <text x="190" y="165" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">அருட்பெருஞ்ஜோதி</text>
          <text x="190" y="183" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="11.5">தனிப்பெருங்கருணை</text>
          <text x="190" y="198" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">திரைகள் விலகிய அகப் பேரொளி</text>
        </g>
      </svg>
      <div class="diagram-footer">
        <p><strong>வள்ளலார் அருள்நெறி:</strong> மனித ஆன்மாவை உண்மை நிலையிலிருந்து பிரித்து அறியாமையில் ஆழ்த்தும் 7 மாயா திரைகளும் அருளொளியால் விலகும்போது, உள்ளொளியான சிவஜோதி தரிசனமாகி மரணமில்லாப் பெருவாழ்வு வாய்க்கும்.</p>
      </div>
    </div>
    """

# ===========================================================================
# 4. Thirukkural Trivarga (Aram, Porul, Inbam)
# ===========================================================================
def generate_svg_thirukkural_trivarga():
    """Diagram showing the Threefold path of Thirukkural (Dharma, Artha, Kama -> Moksha)."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>திருக்குறள் முப்பால் கட்டமைப்பு (அறம், பொருள், இன்பம்)</h4>
      </div>
      <svg viewBox="0 0 700 240" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="240" rx="12" fill="rgba(11,15,22,0.92)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- Pillar 1: Aram -->
        <g transform="translate(30, 25)">
          <rect x="0" y="0" width="195" height="150" rx="8" fill="rgba(52,211,153,0.06)" stroke="#34d399" stroke-width="1.5"/>
          <rect x="0" y="0" width="195" height="32" rx="8" fill="rgba(52,211,153,0.2)"/>
          <text x="97" y="21" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">1. அறத்துப்பால் (38)</text>
          
          <text x="15" y="55" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">• பாயிரவியல் (4)</text>
          <text x="15" y="72" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">  கடவுள் வாழ்த்து, வான்சிறப்பு</text>
          
          <text x="15" y="95" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">• இல்லறவியல் (20)</text>
          <text x="15" y="112" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">  அன்புடைமை, விருந்தோம்பல்</text>
          
          <text x="15" y="132" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">• துறவறவியல் &amp; ஊழியல் (14)</text>
        </g>

        <!-- Pillar 2: Porul -->
        <g transform="translate(252, 25)">
          <rect x="0" y="0" width="195" height="150" rx="8" fill="rgba(56,189,248,0.06)" stroke="#38bdf8" stroke-width="1.5"/>
          <rect x="0" y="0" width="195" height="32" rx="8" fill="rgba(56,189,248,0.2)"/>
          <text x="97" y="21" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">2. பொருட்பால் (70)</text>
          
          <text x="15" y="55" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">• அரசியல் (25)</text>
          <text x="15" y="72" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">  இறைமாட்சி, கல்வி, செங்கோன்மை</text>
          
          <text x="15" y="95" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">• அங்கவியல் (32)</text>
          <text x="15" y="112" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">  அமைச்சு, நாடு, அரண், நட்பு</text>
          
          <text x="15" y="132" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">• ஒழிபியல் (13) - குடிமை, உழவு</text>
        </g>

        <!-- Pillar 3: Inbam -->
        <g transform="translate(475, 25)">
          <rect x="0" y="0" width="195" height="150" rx="8" fill="rgba(244,114,182,0.06)" stroke="rgba(244,114,182,0.7)" stroke-width="1.5"/>
          <rect x="0" y="0" width="195" height="32" rx="8" fill="rgba(244,114,182,0.2)"/>
          <text x="97" y="21" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">3. இன்பத்துப்பால் (25)</text>
          
          <text x="15" y="55" fill="#f472b6" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">• களவியல் (7)</text>
          <text x="15" y="72" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">  தூய அன்பின் இயல்பான ஈர்ப்பு</text>
          
          <text x="15" y="95" fill="#f472b6" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">• கற்பியல் (18)</text>
          <text x="15" y="112" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">  இணைபிரியாத இல்லறப் பேரின்பம்</text>
          
          <text x="15" y="132" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">  அன்பின் உச்சமே ஆன்ம விடுதலை</text>
        </g>

        <!-- Bottom Banner: 133 Chapters -> Moksha -->
        <g transform="translate(30, 188)">
          <rect x="0" y="0" width="640" height="36" rx="6" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
          <text x="320" y="23" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12">
            மொத்தம் 133 அதிகாரங்கள் (1330 குறள்கள்) <tspan fill="#38bdf8">➔</tspan> இம்மூன்றையும் கடைப்பிடித்தால் மலரும் நான்காம் பேறு: <tspan fill="#34d399" font-weight="bold">வீடுபேறு (மோக்ஷம்)</tspan>
          </text>
        </g>
      </svg>
      <div class="diagram-footer">
        <p><strong>குறள் நெறி:</strong> அறத்தின் வழியே பொருளை ஈட்டி, அப்பொருளால் தூய அன்புடன் இல்லறம் நடத்தும் மனிதன், தனியே துறவு பூணாமலேயே வீடுபேறு எனும் முக்தியை எளிதில் அடைவான் என்பது திருவள்ளுவரின் நெறி.</p>
      </div>
    </div>
    """

# ===========================================================================
# 5. 63 Nayanmars & 4 Samaya Kuravars
# ===========================================================================
def generate_svg_nayanmar_lineage():
    """Diagram showing the 63 Nayanmars lineage and 4 Samaya Kuravars spiritual paths."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>சைவத் திருமுறைப் பரம்பரை — நால்வர் &amp; 63 நாயன்மார்கள்</h4>
      </div>
      <svg viewBox="0 0 700 245" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="245" rx="12" fill="rgba(11,15,22,0.92)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- Top Banner -->
        <rect x="30" y="16" width="640" height="28" rx="6" fill="rgba(56,189,248,0.1)" stroke="rgba(56,189,248,0.3)" stroke-width="1"/>
        <text x="350" y="35" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">
          திருத்தொண்டத் தொகை மரபு: 63 தனி அடியார்கள் + 9 தொகை அடியார்கள்
        </text>

        <!-- 4 Samaya Kuravars Grid -->
        <!-- 1. Sambandar -->
        <g transform="translate(30, 56)">
          <rect x="0" y="0" width="152" height="135" rx="8" fill="rgba(255,255,255,0.03)" stroke="#38bdf8" stroke-width="1.2"/>
          <circle cx="76" cy="30" r="18" fill="rgba(56,189,248,0.15)"/>
          <text x="76" y="36" text-anchor="middle" fill="#38bdf8" font-size="16">👶</text>
          <text x="76" y="66" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">திருஞானசம்பந்தர்</text>
          <text x="76" y="84" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">சற்புத்திர மார்க்கம்</text>
          <text x="76" y="100" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">(மகன் நெறி)</text>
          <text x="76" y="120" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">திருமுறைகள் 1, 2, 3</text>
        </g>

        <!-- 2. Appar -->
        <g transform="translate(192, 56)">
          <rect x="0" y="0" width="152" height="135" rx="8" fill="rgba(255,255,255,0.03)" stroke="#34d399" stroke-width="1.2"/>
          <circle cx="76" cy="30" r="18" fill="rgba(52,211,153,0.15)"/>
          <text x="76" y="36" text-anchor="middle" fill="#34d399" font-size="16">🧹</text>
          <text x="76" y="66" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">திருநாவுக்கரசர்</text>
          <text x="76" y="84" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">தாச மார்க்கம்</text>
          <text x="76" y="100" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">(தொண்டு நெறி)</text>
          <text x="76" y="120" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">திருமுறைகள் 4, 5, 6</text>
        </g>

        <!-- 3. Sundarar -->
        <g transform="translate(354, 56)">
          <rect x="0" y="0" width="152" height="135" rx="8" fill="rgba(255,255,255,0.03)" stroke="#38bdf8" stroke-width="1.2"/>
          <circle cx="76" cy="30" r="18" fill="rgba(56,189,248,0.15)"/>
          <text x="76" y="36" text-anchor="middle" fill="#38bdf8" font-size="16">🤝</text>
          <text x="76" y="66" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">சுந்தரமூர்த்தி</text>
          <text x="76" y="84" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">சக மார்க்கம்</text>
          <text x="76" y="100" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">(தோழமை நெறி)</text>
          <text x="76" y="120" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">7-ஆம் திருமுறை</text>
        </g>

        <!-- 4. Manikkavasagar -->
        <g transform="translate(516, 56)">
          <rect x="0" y="0" width="152" height="135" rx="8" fill="rgba(255,255,255,0.03)" stroke="#34d399" stroke-width="1.2"/>
          <circle cx="76" cy="30" r="18" fill="rgba(52,211,153,0.15)"/>
          <text x="76" y="36" text-anchor="middle" fill="#34d399" font-size="16">📖</text>
          <text x="76" y="66" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">மாணிக்கவாசகர்</text>
          <text x="76" y="84" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">சன்மார்க்கம்</text>
          <text x="76" y="100" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">(ஞான நெறி)</text>
          <text x="76" y="120" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">8-ஆம் திருமுறை (திருவாசகம்)</text>
        </g>

        <!-- Bottom Summary Footnote -->
        <text x="350" y="215" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">
          "என் கடன் பணி செய்து கிடப்பதே" — சாதிகள், வர்க்கங்களைக் கடந்து சிவபக்தியால் இணைந்த திருத்தொண்டர் மரபு.
        </text>
      </svg>
      <div class="diagram-footer">
        <p><strong>பக்தி மரபு:</strong> நால்வர் காட்டிய மகன்மை, தொண்டு, தோழமை, ஞானம் ஆகிய 4 நெறிகளும் இறைவனை எளிய மனிதனும் அடையும் வழிகளாகும். 63 நாயன்மார்கள் சுயநலமற்று இறைப்பணியே உயிரென வாழ்ந்து வழிகாட்டினர்.</p>
      </div>
    </div>
    """

# ===========================================================================
# 6. 28 Saiva Agamas & 14 Meikanda Shastras
# ===========================================================================
def generate_svg_agamas_shastras():
    """Diagram showing the 28 Saiva Agamas and 14 Meikanda Shastras tree of knowledge."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>28 சிவாகமங்களும் 14 மெய்கண்ட சாத்திரங்களும் (ஞான விருட்சம்)</h4>
      </div>
      <svg viewBox="0 0 700 250" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="250" rx="12" fill="rgba(11,15,22,0.92)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- Left: 28 Saiva Agamas (Roots & Temple Architecture) -->
        <g transform="translate(30, 25)">
          <rect x="0" y="0" width="295" height="195" rx="8" fill="rgba(56,189,248,0.04)" stroke="#38bdf8" stroke-width="1.2"/>
          <text x="147" y="24" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">28 சிவாகமங்கள் (சிவாலய நெறி)</text>
          
          <g transform="translate(15, 38)">
            <!-- 4 Padas -->
            <rect x="0" y="0" width="125" height="42" rx="5" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.15)"/>
            <text x="62" y="17" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">1. சரியா பாதம்</text>
            <text x="62" y="32" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">கோயில் வழிபாடு &amp; பணி</text>

            <rect x="140" y="0" width="125" height="42" rx="5" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.15)"/>
            <text x="202" y="17" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">2. கிரியா பாதம்</text>
            <text x="202" y="32" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">சிவபூஜை &amp; பிரதிஷ்டை</text>

            <rect x="0" y="50" width="125" height="42" rx="5" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.15)"/>
            <text x="62" y="67" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">3. யோக பாதம்</text>
            <text x="62" y="82" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">அகத்தியான ஒருமை</text>

            <rect x="140" y="50" width="125" height="42" rx="5" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.15)"/>
            <text x="202" y="67" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">4. ஞான பாதம்</text>
            <text x="202" y="82" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">முப்பொருள் உண்மை</text>
          </g>

          <text x="147" y="155" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">10 சிவபேத ஆகமங்கள் (காமிகம் முதல் சுப்ரபேதம்)</text>
          <text x="147" y="173" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">18 ருத்ரபேத ஆகமங்கள் (விஜயம் முதல் வாதுளம்)</text>
        </g>

        <!-- Center Connector Arrow -->
        <g transform="translate(330, 115)">
          <line x1="0" y1="0" x2="35" y2="0" stroke="#34d399" stroke-width="2" stroke-dasharray="3,2"/>
          <polygon points="35,-4 42,0 35,4" fill="#34d399"/>
        </g>

        <!-- Right: 14 Meikanda Shastras -->
        <g transform="translate(375, 25)">
          <rect x="0" y="0" width="295" height="195" rx="8" fill="rgba(52,211,153,0.04)" stroke="#34d399" stroke-width="1.2"/>
          <text x="147" y="24" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">14 மெய்கண்ட சாத்திரங்கள் (சித்தாந்த ஞானம்)</text>
          
          <!-- Crown jewel: Sivagnana Bodham -->
          <rect x="15" y="38" width="265" height="42" rx="5" fill="rgba(52,211,153,0.15)" stroke="#34d399" stroke-width="1.5"/>
          <text x="147" y="55" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">தலையாய நூல்: சிவஞானபோதம்</text>
          <text x="147" y="70" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">மெய்கண்ட தேவர் அருளிய 12 சூத்திரங்கள்</text>

          <g transform="translate(15, 88)">
            <text x="5" y="18" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="10.5">• சிவஞான சித்தியார் &amp; இருபா இருபஃது</text>
            <text x="5" y="36" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="10.5">• உண்மை விளக்கம் &amp; திருவுந்தியார்</text>
            <text x="5" y="54" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="10.5">• திருவருட்பயன், கொடிக்கவி &amp; நெஞ்சுவிடுதூது</text>
            <text x="5" y="72" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="10.5">• சிவப்பிரகாசம் &amp; சங்கற்ப நிராகரணம்</text>
          </g>

          <text x="147" y="182" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="10.5" font-weight="bold">பதி (சிவம்) - பசு (ஆன்மா) - பாசம் (மலம்) மெய்யறிவு</text>
        </g>
      </svg>
      <div class="diagram-footer">
        <p><strong>சித்தாந்த விளக்கம்:</strong> சிவாகமங்கள் சிவாலய அமைப்பு, பூஜா விதிகள் மற்றும் கிரியைகளை விளக்கும் மூல நூல்களாகும்; 14 மெய்கண்ட சாத்திரங்கள் தமிழ் மொழியில் முப்பொருள் உண்மையை தருக்க ரீதியாக நிறுவும் மெய்யறிவுச் சிகரங்களாகும்.</p>
      </div>
    </div>
    """

# ===========================================================================
# 7. Pancha Bhuta Temples, Senses & Chakras
# ===========================================================================
def generate_svg_pancha_bhuta():
    """Diagram showing the 5 Elements and their correspondence to Temples, Senses & Chakras."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>பஞ்ச பூதத் தலங்கள் &amp; மனித உடல் — ஐம்பூதத் தத்துவம்</h4>
      </div>
      <svg viewBox="0 0 700 255" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="255" rx="12" fill="rgba(11,15,22,0.92)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- 5 Element Columns -->
        <!-- 1. Earth / Kanchipuram -->
        <g transform="translate(25, 25)">
          <rect x="0" y="0" width="120" height="175" rx="8" fill="rgba(52,211,153,0.06)" stroke="#34d399" stroke-width="1.2"/>
          <circle cx="60" cy="28" r="16" fill="rgba(52,211,153,0.2)"/>
          <text x="60" y="34" text-anchor="middle" fill="#34d399" font-size="14">🌱</text>
          <text x="60" y="62" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">நிலம் (Earth)</text>
          <text x="60" y="80" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">காஞ்சிபுரம்</text>
          <text x="60" y="98" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">ஏகாம்பரேஸ்வரர்</text>
          <text x="60" y="116" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">மண் லிங்கம்</text>
          <path d="M 15 128 L 105 128" stroke="rgba(255,255,255,0.1)"/>
          <text x="60" y="145" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="10">மூலாதாரம்</text>
          <text x="60" y="162" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">நுகர்ச்சி (மணம்)</text>
        </g>

        <!-- 2. Water / Thiruvanaikka -->
        <g transform="translate(155, 25)">
          <rect x="0" y="0" width="120" height="175" rx="8" fill="rgba(56,189,248,0.06)" stroke="#38bdf8" stroke-width="1.2"/>
          <circle cx="60" cy="28" r="16" fill="rgba(56,189,248,0.2)"/>
          <text x="60" y="34" text-anchor="middle" fill="#38bdf8" font-size="14">💧</text>
          <text x="60" y="62" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">நீர் (Water)</text>
          <text x="60" y="80" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">திருவானைக்கா</text>
          <text x="60" y="98" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">ஜம்புகேஸ்வரர்</text>
          <text x="60" y="116" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">அப்பு லிங்கம்</text>
          <path d="M 15 128 L 105 128" stroke="rgba(255,255,255,0.1)"/>
          <text x="60" y="145" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="10">சுவாதிஷ்டானம்</text>
          <text x="60" y="162" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">சுவை (நாக்கு)</text>
        </g>

        <!-- 3. Fire / Thiruvannamalai -->
        <g transform="translate(285, 25)">
          <rect x="0" y="0" width="120" height="175" rx="8" fill="rgba(245,158,11,0.06)" stroke="#f59e0b" stroke-width="1.2"/>
          <circle cx="60" cy="28" r="16" fill="rgba(245,158,11,0.2)"/>
          <text x="60" y="34" text-anchor="middle" fill="#f59e0b" font-size="14">🔥</text>
          <text x="60" y="62" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">தீ (Fire)</text>
          <text x="60" y="80" text-anchor="middle" fill="#f59e0b" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">திருவண்ணாமலை</text>
          <text x="60" y="98" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">அருணாசலேஸ்வரர்</text>
          <text x="60" y="116" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">தேயு லிங்கம்</text>
          <path d="M 15 128 L 105 128" stroke="rgba(255,255,255,0.1)"/>
          <text x="60" y="145" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="10">மணிபூரகம்</text>
          <text x="60" y="162" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">பார்வை (கண்)</text>
        </g>

        <!-- 4. Air / Kalahasti -->
        <g transform="translate(415, 25)">
          <rect x="0" y="0" width="120" height="175" rx="8" fill="rgba(147,197,253,0.06)" stroke="#93c5fd" stroke-width="1.2"/>
          <circle cx="60" cy="28" r="16" fill="rgba(147,197,253,0.2)"/>
          <text x="60" y="34" text-anchor="middle" fill="#93c5fd" font-size="14">💨</text>
          <text x="60" y="62" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">காற்று (Air)</text>
          <text x="60" y="80" text-anchor="middle" fill="#93c5fd" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">திருக்காளஹத்தி</text>
          <text x="60" y="98" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">காளத்தீஸ்வரர்</text>
          <text x="60" y="116" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">வாயு லிங்கம்</text>
          <path d="M 15 128 L 105 128" stroke="rgba(255,255,255,0.1)"/>
          <text x="60" y="145" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="10">அனாகதம்</text>
          <text x="60" y="162" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">தொடுதல் (மெய்)</text>
        </g>

        <!-- 5. Space / Chidambaram -->
        <g transform="translate(545, 25)">
          <rect x="0" y="0" width="120" height="175" rx="8" fill="rgba(167,139,250,0.06)" stroke="#a78bfa" stroke-width="1.2"/>
          <circle cx="60" cy="28" r="16" fill="rgba(167,139,250,0.2)"/>
          <text x="60" y="34" text-anchor="middle" fill="#a78bfa" font-size="14">✨</text>
          <text x="60" y="62" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">ஆகாயம் (Space)</text>
          <text x="60" y="80" text-anchor="middle" fill="#a78bfa" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">சிதம்பரம்</text>
          <text x="60" y="98" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">நடராஜ பெருமான்</text>
          <text x="60" y="116" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">ஆகாய ரகசியம்</text>
          <path d="M 15 128 L 105 128" stroke="rgba(255,255,255,0.1)"/>
          <text x="60" y="145" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="10">விசுத்தி</text>
          <text x="60" y="162" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">கேட்டல் (செவி)</text>
        </g>

        <!-- Bottom Connection Text -->
        <text x="350" y="225" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11.5">
          "பூதங்கள் ஐந்தும் சிவமே; பொறிகள் ஐந்தும் சிவமே" — புற இயற்கைக்கும் அக உடலுக்குமான உன்னத ஒருமைப்பாடு.
        </text>
      </svg>
      <div class="diagram-footer">
        <p><strong>பிரபஞ்ச ஒருமைப்பாடு:</strong> பிரபஞ்சத்தை இயக்கும் ஐந்து மூலக் கூறுகளும் நமது உடலின் ஐந்து புலன்களோடும் யோக சக்கரங்களோடும் நேரடித் தொடர்பு கொண்டவை. பஞ்சபூதத் தலங்களை வணங்குவது இயற்கைச் சமநிலையைப் பேணும் நன்றி நவிதலாகும்.</p>
      </div>
    </div>
    """

# ===========================================================================
# 8. Chakra System & Kundalini Awakening
# ===========================================================================
def generate_svg_chakra_system():
    """Diagram showing the 7 Chakras with Tamil yogic terms and stages of spiritual awakening."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>சப்த சக்கரங்கள் &amp; குண்டலினி ஆன்ம விழிப்புணர்வு</h4>
      </div>
      <svg viewBox="0 0 700 250" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="250" rx="12" fill="rgba(11,15,22,0.92)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- Left: Spinal Axis & 7 Lotus Nodes -->
        <g transform="translate(60, 20)">
          <!-- Sushumna Nadi Line -->
          <line x1="45" y1="15" x2="45" y2="195" stroke="rgba(56,189,248,0.4)" stroke-width="4" stroke-linecap="round"/>
          
          <!-- 7. Sahasrara -->
          <circle cx="45" cy="20" r="11" fill="rgba(255,255,255,0.2)" stroke="#ffffff" stroke-width="2"/>
          <text x="70" y="24" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">7. சகஸ்ராரம் <tspan fill="#94a3b8">(உச்சி - 1000 இதழ் - சிவ ஐக்கியம்)</tspan></text>

          <!-- 6. Ajna -->
          <circle cx="45" cy="50" r="10" fill="rgba(167,139,250,0.25)" stroke="#a78bfa" stroke-width="2"/>
          <text x="70" y="54" fill="#a78bfa" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">6. ஆஞ்ஞை <tspan fill="#94a3b8">(புருவ நடு - 2 இதழ் - உள்ளொளி)</tspan></text>

          <!-- 5. Vishuddha -->
          <circle cx="45" cy="80" r="10" fill="rgba(56,189,248,0.25)" stroke="#38bdf8" stroke-width="2"/>
          <text x="70" y="84" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">5. விசுத்தி <tspan fill="#94a3b8">(கண்டம்/தொண்டை - 16 இதழ் - ஆகாயம்)</tspan></text>

          <!-- 4. Anahata -->
          <circle cx="45" cy="110" r="10" fill="rgba(52,211,153,0.25)" stroke="#34d399" stroke-width="2"/>
          <text x="70" y="114" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">4. அனாகதம் <tspan fill="#94a3b8">(இதயம் - 12 இதழ் - காற்று/அன்பு)</tspan></text>

          <!-- 3. Manipura -->
          <circle cx="45" cy="140" r="10" fill="rgba(245,158,11,0.25)" stroke="#f59e0b" stroke-width="2"/>
          <text x="70" y="144" fill="#f59e0b" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">3. மணிபூரகம் <tspan fill="#94a3b8">(நாபி/கொப்பூழ் - 10 இதழ் - தீ)</tspan></text>

          <!-- 2. Svadhisthana -->
          <circle cx="45" cy="170" r="10" fill="rgba(56,189,248,0.2)" stroke="#38bdf8" stroke-width="1.8"/>
          <text x="70" y="174" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">2. சுவாதிஷ்டானம் <tspan fill="#94a3b8">(கொப்பூழடி - 6 இதழ் - நீர்)</tspan></text>

          <!-- 1. Muladhara -->
          <circle cx="45" cy="195" r="11" fill="rgba(239,68,68,0.25)" stroke="#ef4444" stroke-width="2"/>
          <text x="70" y="199" fill="#ef4444" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">1. மூலாதாரம் <tspan fill="#94a3b8">(மலத்துவாரம் - 4 இதழ் - மண்/குண்டலினி)</tspan></text>
        </g>

        <!-- Right: Yogic Ascent Philosophy -->
        <g transform="translate(420, 25)">
          <rect x="0" y="0" width="250" height="195" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
          <text x="125" y="24" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">ஆன்ம விழிப்புணர்வு நிலைகள்</text>
          
          <g transform="translate(15, 38)">
            <!-- Top Tier -->
            <rect x="0" y="0" width="220" height="42" rx="5" fill="rgba(56,189,248,0.08)"/>
            <text x="10" y="17" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">பேரின்ப நிலை (உச்சி)</text>
            <text x="10" y="32" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">சிவ-சக்தி சங்கமம் &amp; துரியாதீதம்</text>

            <!-- Mid Tier -->
            <rect x="0" y="50" width="220" height="42" rx="5" fill="rgba(52,211,153,0.08)"/>
            <text x="10" y="67" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">அன்புப் பாலம் (இதயம்)</text>
            <text x="10" y="82" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">சுயநலமற்ற ஜீவகாருண்ய உணர்வு</text>

            <!-- Base Tier -->
            <rect x="0" y="100" width="220" height="42" rx="5" fill="rgba(245,158,11,0.08)"/>
            <text x="10" y="117" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">உடல் இயக்கம் (கீழ் மையம்)</text>
            <text x="10" y="132" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">பசியும் தூக்கமும் உடற்பாதுகாப்பும்</text>
          </g>

          <text x="125" y="178" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="10.5">
            இடகலை, பிங்கலை ➔ சுழுமுனையில் ஓங்கும் பிராணன்
          </text>
        </g>
      </svg>
      <div class="diagram-footer">
        <p><strong>திருமூலர் திருமந்திர யோகம்:</strong> மனித உடலின் சுழுமுனை நாடியில் அமைந்துள்ள 7 ஆதார மையங்கள் வழியே மூலாதாரத்தில் உறங்கும் குண்டலினி அருள்சக்தி விழித்தெழுந்து உச்சியில் சிவத்தோடு கலப்பதே யோக முக்தியாகும்.</p>
      </div>
    </div>
    """

# ===========================================================================
# 9. Deivathin Kural (Kanchi Maha Periyava)
# ===========================================================================
def generate_svg_deivathin_kural():
    """Diagram showing Kanchi Maha Periyava's Call of God: Vedas, Cow Protection, Simple Living."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>தெய்வத்தின் குரல் — வேத சம்ரக்ஷணம், கோ சம்ரக்ஷணம், எளிய வாழ்வு</h4>
      </div>
      <svg viewBox="0 0 700 240" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="240" rx="12" fill="rgba(11,15,22,0.92)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- Pillar 1: Veda Samrakshanam -->
        <g transform="translate(30, 25)">
          <rect x="0" y="0" width="195" height="155" rx="8" fill="rgba(56,189,248,0.05)" stroke="#38bdf8" stroke-width="1.2"/>
          <circle cx="97" cy="32" r="18" fill="rgba(56,189,248,0.15)"/>
          <text x="97" y="38" text-anchor="middle" fill="#38bdf8" font-size="16">📜</text>
          
          <text x="97" y="68" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12.5" font-weight="bold">வேத சம்ரக்ஷணம்</text>
          <text x="97" y="86" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="11">பிரபஞ்ச ஒலி வடிவம்</text>
          
          <text x="15" y="112" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">• சனாதன தர்மத்தின் ஆணிவேர்</text>
          <text x="15" y="128" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">• மந்திர ஒலிகள் உலகைக் காக்கும்</text>
          <text x="15" y="144" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">• வேத பாடசாலைகளை ஆதரித்தல்</text>
        </g>

        <!-- Pillar 2: Go Samrakshanam -->
        <g transform="translate(252, 25)">
          <rect x="0" y="0" width="195" height="155" rx="8" fill="rgba(52,211,153,0.05)" stroke="#34d399" stroke-width="1.2"/>
          <circle cx="97" cy="32" r="18" fill="rgba(52,211,153,0.15)"/>
          <text x="97" y="38" text-anchor="middle" fill="#34d399" font-size="16">🐄</text>
          
          <text x="97" y="68" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12.5" font-weight="bold">கோ சம்ரக்ஷணம்</text>
          <text x="97" y="86" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="11">காமதேனு வழிபாட்டு நெறி</text>
          
          <text x="15" y="112" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">• முப்பத்து முக்கோடி தேவர் உறைவிடம்</text>
          <text x="15" y="128" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">• பசுவை தாயாகப் போற்றுதல்</text>
          <text x="15" y="144" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">• கோசாலை அமைத்து பராமரித்தல்</text>
        </g>

        <!-- Pillar 3: Simple Living & High Thinking -->
        <g transform="translate(475, 25)">
          <rect x="0" y="0" width="195" height="155" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.2)" stroke-width="1.2"/>
          <circle cx="97" cy="32" r="18" fill="rgba(255,255,255,0.1)"/>
          <text x="97" y="38" text-anchor="middle" fill="#ffffff" font-size="16">🪷</text>
          
          <text x="97" y="68" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12.5" font-weight="bold">எளிய வாழ்வு — நற்சிந்தனை</text>
          <text x="97" y="86" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">அகத்தூய்மையும் தர்மமும்</text>
          
          <text x="15" y="112" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">• ஆடம்பரமற்ற தூய எளிய வாழ்வு</text>
          <text x="15" y="128" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">• பிடி அரிசித் திட்டம் (பிறர் பசி தீர்த்தல்)</text>
          <text x="15" y="144" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">• நித்ய அனுஷ்டானங்களை வழுவாமை</text>
        </g>

        <!-- Bottom Quote -->
        <text x="350" y="215" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="11.5">
          "நாம் வேதத்தைக் காத்தால் வேதம் நம்மை உலக நன்மைக்காகக் காக்கும்" — காஞ்சி காமகோடி மகா பெரியவா
        </text>
      </svg>
      <div class="diagram-footer">
        <p><strong>மகா பெரியவா தர்ம நெறி:</strong> சனாதன பண்பாட்டின் தூண்களான வேத மரபைப் பாதுகாப்பதும், பசுக்களை தாயெனப் போற்றிப் பேணுதலும், ஆடம்பரங்களை விடுத்து எளிய தூய வாழ்வை வாழ்வதுமே மனித குல அமைதிக்கான வழியாகும்.</p>
      </div>
    </div>
    """

# ===========================================================================
# 10. Jivakarunyam & Universal Compassion (Vallalar)
# ===========================================================================
def generate_svg_jivakarunyam():
    """Diagram showing Vallalar's Jivakarunyam, Plant consciousness, and Vadalur Dharmasala."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>ஜீவகாருண்ய ஒழுக்கம் &amp; ஆன்மநேய ஒருமைப்பாடு (வள்ளலார்)</h4>
      </div>
      <svg viewBox="0 0 700 240" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="240" rx="12" fill="rgba(11,15,22,0.92)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- Left: Plant Consciousness -->
        <g transform="translate(30, 25)">
          <rect x="0" y="0" width="195" height="155" rx="8" fill="rgba(52,211,153,0.06)" stroke="#34d399" stroke-width="1.2"/>
          <text x="97" y="26" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="12.5" font-weight="bold">தாவர உணர்வு</text>
          
          <!-- Sprout Graphic -->
          <g transform="translate(97, 70)">
            <circle cx="0" cy="0" r="22" fill="rgba(52,211,153,0.15)"/>
            <path d="M 0 16 L 0 -10 C -12 -12 -14 0 0 5 C 12 -10 14 0 0 5" fill="#34d399"/>
            <circle cx="0" cy="-14" r="2" fill="#ffffff"/>
          </g>
          
          <text x="97" y="115" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">"வாடிய பயிரைக் கண்ட</text>
          <text x="97" y="132" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">போதெல்லாம் வாடினேன்"</text>
          <text x="97" y="148" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">பயிர்க்கும் உயிர் உண்டு</text>
        </g>

        <!-- Center: Ever-burning Fire at Vadalur -->
        <g transform="translate(252, 25)">
          <rect x="0" y="0" width="195" height="155" rx="8" fill="rgba(56,189,248,0.06)" stroke="#38bdf8" stroke-width="1.2"/>
          <text x="97" y="26" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="12.5" font-weight="bold">வடலூர் சத்ய தருமசாலை</text>
          
          <!-- Cauldron with Eternal Flame -->
          <g transform="translate(97, 68)">
            <!-- Cauldron / Pot -->
            <ellipse cx="0" cy="18" rx="28" ry="10" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.5"/>
            <path d="M -26 18 Q 0 35 26 18 Z" fill="#334155" stroke="#cbd5e1" stroke-width="1.5"/>
            
            <!-- Sacred Flame -->
            <path d="M 0 10 Q -15 -8 0 -24 Q 15 -8 0 10 Z" fill="#38bdf8" filter="drop-shadow(0 0 6px #38bdf8)"/>
            <circle cx="0" cy="-6" r="4" fill="#ffffff"/>
          </g>

          <text x="97" y="115" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">அணையாத அடுப்பு</text>
          <text x="97" y="132" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">1867 முதல் இன்றும் தொடரும்</text>
          <text x="97" y="148" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="10">பசிப்பிணி போக்கும் அருளறம்</text>
        </g>

        <!-- Right: Universal Brotherhood -->
        <g transform="translate(475, 25)">
          <rect x="0" y="0" width="195" height="155" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.2)" stroke-width="1.2"/>
          <text x="97" y="26" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12.5" font-weight="bold">ஆன்மநேய ஒருமைப்பாடு</text>
          
          <g transform="translate(97, 65)">
            <circle cx="0" cy="0" r="22" fill="rgba(255,255,255,0.08)"/>
            <text x="0" y="6" text-anchor="middle" fill="#ffffff" font-size="18">🕊️</text>
          </g>

          <text x="97" y="112" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">கொல்லாமை நெறி</text>
          <text x="97" y="128" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">புலால் மறுப்பு &amp; இரக்கம்</text>
          <text x="97" y="146" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">எல்லா உயிரும் கடவுளின் ஆலயம்</text>
        </g>

        <!-- Bottom Quote -->
        <text x="350" y="215" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11.5">
          "பசியினால் இளைத்துப் பிணியினால் வருந்தி பாவம் செய்வோரைக் கண்டபோதெல்லாம் என் உள்ளம் நடுங்கியது" — திருவருட்பா
        </text>
      </svg>
      <div class="diagram-footer">
        <p><strong>ஜீவகாருண்ய தத்துவம்:</strong> தாவரங்கள், விலங்குகள், மனிதர்கள் என அனைத்து உயிர்களிடத்தும் ஒரே சிவ ஆற்றல் துடிக்கிறது. பசியால் வாடும் சக உயிர்களுக்கு உணவளிப்பதே இறைவனை அடையும் தலைசிறந்த அருட்பணியாகும்.</p>
      </div>
    </div>
    """

# ===========================================================================
# 11. Konrai Vendhan (Avvaiyar's Ethical Moral Ladder)
# ===========================================================================
def generate_svg_konrai_vendhan():
    """Diagram showing Avvaiyar's Konrai Vendhan moral ladder for youthful minds."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>கொன்றை வேந்தன் — ஔவையாரின் வாழ்வியல் ஒழுக்க ஏணி</h4>
      </div>
      <svg viewBox="0 0 700 245" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="245" rx="12" fill="rgba(11,15,22,0.92)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- Left: Avvaiyar's 5 Moral Steps Ladder -->
        <g transform="translate(40, 20)">
          <text x="210" y="18" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">கொன்றை வேந்தன் ஒழுக்கப் படிகள்</text>

          <!-- Step 5 (Top): Discipline -->
          <g transform="translate(0, 32)">
            <rect x="0" y="0" width="420" height="28" rx="5" fill="rgba(52,211,153,0.15)" stroke="#34d399" stroke-width="1.2"/>
            <text x="15" y="19" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">படி 5:</text>
            <text x="65" y="19" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">ஒழுக்கம் விழுப்பம் தரலான் உயிரினும் ஓம்பப்படும்</text>
          </g>

          <!-- Step 4: Literacy & Numeracy -->
          <g transform="translate(0, 66)">
            <rect x="0" y="0" width="420" height="28" rx="5" fill="rgba(56,189,248,0.12)" stroke="#38bdf8" stroke-width="1"/>
            <text x="15" y="19" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">படி 4:</text>
            <text x="65" y="19" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11.5">எண்ணும் எழுத்தும் கண்எனத் தகும் (கல்வி அறிவு)</text>
          </g>

          <!-- Step 3: Righteous Family Life -->
          <g transform="translate(0, 100)">
            <rect x="0" y="0" width="420" height="28" rx="5" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>
            <text x="15" y="19" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">படி 3:</text>
            <text x="65" y="19" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11.5">இல்லறம் அல்லது நல்லறம் அன்று (குடும்ப நல்லொழுக்கம்)</text>
          </g>

          <!-- Step 2: Temple Worship -->
          <g transform="translate(0, 134)">
            <rect x="0" y="0" width="420" height="28" rx="5" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>
            <text x="15" y="19" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">படி 2:</text>
            <text x="65" y="19" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11.5">ஆலயம் தொழுவது சாலவும் நன்று (மனத்தூய்மை வழிபாடு)</text>
          </g>

          <!-- Step 1 (Foundation): Parents as First Gods -->
          <g transform="translate(0, 168)">
            <rect x="0" y="0" width="420" height="28" rx="5" fill="rgba(56,189,248,0.2)" stroke="#38bdf8" stroke-width="1.5"/>
            <text x="15" y="19" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">படி 1:</text>
            <text x="65" y="19" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">அன்னையும் பிதாவும் முன்னணி தெய்வம் (அடித்தளம்)</text>
          </g>
        </g>

        <!-- Right: Avvaiyar Persona Card -->
        <g transform="translate(490, 25)">
          <rect x="0" y="0" width="180" height="190" rx="8" fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
          
          <circle cx="90" cy="40" r="24" fill="rgba(52,211,153,0.15)" stroke="#34d399" stroke-width="1.5"/>
          <text x="90" y="46" text-anchor="middle" fill="#ffffff" font-size="20">👵</text>
          
          <text x="90" y="82" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">ஔவை பிராட்டியார்</text>
          <text x="90" y="100" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="11">கொன்றை வேந்தன்</text>
          
          <path d="M 20 114 L 160 114" stroke="rgba(255,255,255,0.1)"/>
          
          <text x="90" y="134" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">சிவனின் கொன்றை மாலையை</text>
          <text x="90" y="150" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">வணங்கித் தொடங்கும்</text>
          <text x="90" y="168" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="10.5" font-weight="bold">குழந்தை நீதிநூல்</text>
        </g>
      </svg>
      <div class="diagram-footer">
        <p><strong>ஔவை நெறி:</strong> பெற்றோரை வணங்குவதே அறவாழ்வின் தொடக்கப் படி. கல்வி, பக்தி மற்றும் ஒழுக்கத்தை அடுத்தடுத்த படிகளாகக் கொண்டு மனிதன் வாழ்வின் உயர் நற்குணங்களை அடைய வேண்டும் என்று ஔவையார் எளிய வரிகளில் கற்பிக்கிறார்.</p>
      </div>
    </div>
    """

# ===========================================================================
# 12. Pranayama Science of Breath (Puraka, Kumbhaka, Rechaka)
# ===========================================================================
def generate_svg_pranayama_breath():
    """Diagram showing the science of breath: Puraka, Kumbhaka, Rechaka, and mental equilibrium."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>பிராணாயாம மூச்சு அறிவியல் — பூரகம், கும்பகம், ரேசகம்</h4>
      </div>
      <svg viewBox="0 0 700 240" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="240" rx="12" fill="rgba(11,15,22,0.92)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- Breath Cycle (1 : 4 : 2 Ratio) -->
        <!-- 1. Puraka (Inhale) -->
        <g transform="translate(30, 25)">
          <rect x="0" y="0" width="195" height="150" rx="8" fill="rgba(56,189,248,0.06)" stroke="#38bdf8" stroke-width="1.5"/>
          <text x="97" y="26" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">1. பூரகம் (Inhale)</text>
          
          <g transform="translate(97, 65)">
            <circle cx="0" cy="0" r="22" fill="rgba(56,189,248,0.15)"/>
            <path d="M 0 12 L 0 -12 M -6 -6 L 0 -12 L 6 -6" stroke="#38bdf8" stroke-width="2.5" fill="none"/>
          </g>

          <text x="97" y="108" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">மூச்சை உள்ளிழுத்தல்</text>
          <text x="97" y="126" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">விகிதம்: 1 பங்கு (4 வினாடி)</text>
          <text x="97" y="142" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">இடகலை (சந்திரன்/குளிர்ச்சி)</text>
        </g>

        <!-- Arrow 1 -> 2 -->
        <path d="M 230 100 L 248 100" stroke="rgba(255,255,255,0.4)" stroke-width="2" stroke-dasharray="2,2"/>

        <!-- 2. Kumbhaka (Retention) -->
        <g transform="translate(252, 25)">
          <rect x="0" y="0" width="195" height="150" rx="8" fill="rgba(52,211,153,0.08)" stroke="#34d399" stroke-width="2"/>
          <text x="97" y="26" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">2. கும்பகம் (Retention)</text>
          
          <g transform="translate(97, 65)">
            <circle cx="0" cy="0" r="22" fill="rgba(52,211,153,0.2)"/>
            <circle cx="0" cy="0" r="8" fill="#34d399"/>
          </g>

          <text x="97" y="108" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">உள்ளே நிறுத்துதல்</text>
          <text x="97" y="126" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="10" font-weight="bold">விகிதம்: 4 பங்கு (16 வினாடி)</text>
          <text x="97" y="142" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="9.5">சுழுமுனையில் பிராணன் குவிதல்</text>
        </g>

        <!-- Arrow 2 -> 3 -->
        <path d="M 452 100 L 470 100" stroke="rgba(255,255,255,0.4)" stroke-width="2" stroke-dasharray="2,2"/>

        <!-- 3. Rechaka (Exhale) -->
        <g transform="translate(475, 25)">
          <rect x="0" y="0" width="195" height="150" rx="8" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
          <text x="97" y="26" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="13" font-weight="bold">3. ரேசகம் (Exhale)</text>
          
          <g transform="translate(97, 65)">
            <circle cx="0" cy="0" r="22" fill="rgba(255,255,255,0.1)"/>
            <path d="M 0 -12 L 0 12 M -6 6 L 0 12 L 6 6" stroke="#ffffff" stroke-width="2.5" fill="none"/>
          </g>

          <text x="97" y="108" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11" font-weight="bold">மூச்சை வெளியேற்றுதல்</text>
          <text x="97" y="126" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10">விகிதம்: 2 பங்கு (8 வினாடி)</text>
          <text x="97" y="142" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="9.5">பிங்கலை (சூரியன்/வெப்பம்)</text>
        </g>

        <!-- Bottom Quote -->
        <g transform="translate(30, 188)">
          <rect x="0" y="0" width="640" height="36" rx="6" fill="rgba(56,189,248,0.06)" stroke="rgba(56,189,248,0.2)" stroke-width="1"/>
          <text x="320" y="23" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">
            "ஏற்றி இறக்கி இருகாலும் பூரிக்கும் காற்றைப் பிடிக்கும் கணக்கறிவார்க்கு கூற்றை உதைக்கும் குறியதுவாமே" — <tspan fill="#34d399">திருமந்திரம்</tspan>
          </text>
        </g>
      </svg>
      <div class="diagram-footer">
        <p><strong>மூச்சுப் பயிற்சிப் பயன்:</strong> 1:4:2 விகிதத்தில் பிராணாயாமம் செய்யும் போது நுரையீரலின் கொள்ளளவு அதிகரிக்கிறது; இரத்தத்தில் பிராணவாயு நிறைந்து, மனக்குழப்பங்கள் நீங்கி ஆழ்ந்த அமைதியும் புத்திக்கூர்மையும் உருவாகிறது.</p>
      </div>
    </div>
    """

# ===========================================================================
# 13. Sandhyavandanam (Solar-Cosmic Attunement)
# ===========================================================================
def generate_svg_sandhyavandanam():
    """Diagram showing Sandhyavandanam solar-cosmic attunement at dawn, noon, and dusk."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>முக்கால சந்தியாவந்தனம் — சூரிய-பிரபஞ்ச ஆன்ம ஒருங்கிணைப்பு</h4>
      </div>
      <svg viewBox="0 0 700 245" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="245" rx="12" fill="rgba(11,15,22,0.92)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- Solar Trajectory Arc -->
        <path d="M 120 135 Q 350 40 580 135" stroke="rgba(255,255,255,0.15)" stroke-width="2" stroke-dasharray="4,4" fill="none"/>

        <!-- 1. Pratah Sandhya (Dawn) -->
        <g transform="translate(30, 45)">
          <rect x="0" y="0" width="195" height="135" rx="8" fill="rgba(56,189,248,0.06)" stroke="#38bdf8" stroke-width="1.2"/>
          
          <circle cx="97" cy="28" r="16" fill="rgba(56,189,248,0.2)"/>
          <text x="97" y="34" text-anchor="middle" fill="#38bdf8" font-size="14">🌅</text>
          
          <text x="97" y="62" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">பிராதஃ சந்தியா (விடியல்)</text>
          <text x="97" y="80" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="11">பிரம்ம ரூபிணி காயத்ரி</text>
          
          <text x="15" y="104" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">• கிழக்கு நோக்கி நின்று அர்க்கியம்</text>
          <text x="15" y="122" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">• புத்துணர்ச்சி &amp; அறிவுப் பிரகாசம்</text>
        </g>

        <!-- 2. Madhyannika Sandhya (Noon) -->
        <g transform="translate(252, 45)">
          <rect x="0" y="0" width="195" height="135" rx="8" fill="rgba(245,158,11,0.06)" stroke="#f59e0b" stroke-width="1.2"/>
          
          <circle cx="97" cy="28" r="16" fill="rgba(245,158,11,0.2)"/>
          <text x="97" y="34" text-anchor="middle" fill="#f59e0b" font-size="14">☀️</text>
          
          <text x="97" y="62" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">மாத்யானிகம் (நண்பகல்)</text>
          <text x="97" y="80" text-anchor="middle" fill="#f59e0b" font-family="'Mukta Malar', sans-serif" font-size="11">ருத்ர ரூபிணி சாவித்ரி</text>
          
          <text x="15" y="104" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">• உச்சி சூரியன் நோக்குதல்</text>
          <text x="15" y="122" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">• உடல் தேஜஸ் &amp; ஆற்றல் பெருக்கம்</text>
        </g>

        <!-- 3. Sayam Sandhya (Dusk) -->
        <g transform="translate(475, 45)">
          <rect x="0" y="0" width="195" height="135" rx="8" fill="rgba(52,211,153,0.06)" stroke="#34d399" stroke-width="1.2"/>
          
          <circle cx="97" cy="28" r="16" fill="rgba(52,211,153,0.2)"/>
          <text x="97" y="34" text-anchor="middle" fill="#34d399" font-size="14">🌆</text>
          
          <text x="97" y="62" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">சாயங்காலம் (அந்திப் பொழுது)</text>
          <text x="97" y="80" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="11">விஷ்ணு ரூபிணி சரஸ்வதி</text>
          
          <text x="15" y="104" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">• மேற்கு நோக்கி அமர்ந்து தியானம்</text>
          <text x="15" y="122" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">• ஆத்ம சாந்தி &amp; சிவ சிந்தனை</text>
        </g>

        <!-- Bottom Mantra Line -->
        <text x="350" y="210" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="12" font-weight="bold">
          காயத்ரி &amp; சிவகாயத்ரி: <tspan fill="#38bdf8">"தந்நோ ருத்ர ப்ரசோதயாத்"</tspan> — சூரியப் பேரொளியை வணங்கும் வேத வழிபாடு
        </text>
      </svg>
      <div class="diagram-footer">
        <p><strong>அனுஷ்டானப் பயன்:</strong> விடியல், நண்பகல், மாலை ஆகிய மூன்று வேளைகளும் சூரிய ஒளியின் ஆற்றல் மாறுபடும் சந்தி காலங்கள். இந்நேரங்களில் காயத்ரி மந்திரத்தை ஜபித்து அர்க்கியம் அளிப்பது பிரபஞ்ச இயற்கையோடு மனிதனை ஒத்திசைத்து வாழ வைக்கிறது.</p>
      </div>
    </div>
    """

# ===========================================================================
# 14. Saiva Siddhanta 36 Tattvas
# ===========================================================================
def generate_svg_saiva_siddhanta_36_tattvas():
    """Diagram showing the 36 Tattvas (Atma, Vidya, Shiva Tattvas) mapping to Pure Consciousness."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>சைவ சித்தாந்த முப்பத்தாறு (36) தத்துவங்களின் அடுக்கு</h4>
      </div>
      <svg viewBox="0 0 700 250" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="250" rx="12" fill="rgba(11,15,22,0.92)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- Ascent Arrow on Left -->
        <g transform="translate(30, 25)">
          <line x1="15" y1="185" x2="15" y2="15" stroke="#34d399" stroke-width="3"/>
          <polygon points="15,8 9,20 21,20" fill="#34d399"/>
          <text x="-100" y="8" transform="rotate(-90)" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">ஆன்மாவின் முக்திப் பயணம்</text>
        </g>

        <!-- 3 Tiers of Tattvas -->
        <!-- Tier 3: Shiva Tattvas (Top - Pure Maya) -->
        <g transform="translate(70, 20)">
          <rect x="0" y="0" width="595" height="52" rx="8" fill="rgba(56,189,248,0.1)" stroke="#38bdf8" stroke-width="1.5"/>
          <text x="15" y="22" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="12.5" font-weight="bold">சுத்த மாயை — 5 சிவதத்துவங்கள் (Pure Consciousness)</text>
          <text x="15" y="40" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11">
            சிவம் (நாதம்) <tspan fill="#38bdf8">|</tspan> சக்தி (விந்து) <tspan fill="#38bdf8">|</tspan> சாதாக்கியம் <tspan fill="#38bdf8">|</tspan> ஈசுவரம் <tspan fill="#38bdf8">|</tspan> சுத்தவித்தை
          </text>
        </g>

        <!-- Tier 2: Vidya Tattvas (Middle - Mixed Maya) -->
        <g transform="translate(70, 80)">
          <rect x="0" y="0" width="595" height="52" rx="8" fill="rgba(52,211,153,0.08)" stroke="#34d399" stroke-width="1.5"/>
          <text x="15" y="22" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="12.5" font-weight="bold">மிச்ர மாயை — 7 வித்யா தத்துவங்கள் (Cognitive &amp; Karmic Tools)</text>
          <text x="15" y="40" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11">
            காலம் <tspan fill="#34d399">|</tspan> நியதி <tspan fill="#34d399">|</tspan> கலை <tspan fill="#34d399">|</tspan> வித்தை <tspan fill="#34d399">|</tspan> அராகம் <tspan fill="#34d399">|</tspan> புருடன் (ஆன்மா) <tspan fill="#34d399">|</tspan> மாயை
          </text>
        </g>

        <!-- Tier 1: Atma Tattvas (Bottom - Impure Maya) -->
        <g transform="translate(70, 140)">
          <rect x="0" y="0" width="595" height="75" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
          <text x="15" y="20" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="12.5" font-weight="bold">அசுத்த மாயை — 24 ஆன்ம தத்துவங்கள் (Gross Universe &amp; Body)</text>
          
          <text x="15" y="40" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="10.5">
            • அந்தக்கரணம் (4): மனம், புத்தி, சித்தம், அகங்காரம்  <tspan fill="#94a3b8">|</tspan>  ஞானேந்திரியம் (5): மெய், வாய், கண், மூக்கு, செவி
          </text>
          <text x="15" y="58" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="10.5">
            • கன்மேந்திரியம் (5): கை, கால், வாய், எருவாய், கருவாய்  <tspan fill="#94a3b8">|</tspan>  தன்மாத்திரை (5) &amp; பூதங்கள் (5): நிலம், நீர், தீ, காற்று, வான்
          </text>
        </g>

        <!-- Bottom Legend -->
        <text x="367" y="235" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="11">
          24 ஆன்ம தத்துவங்கள் + 7 வித்யா தத்துவங்கள் + 5 சிவதத்துவங்கள் = <tspan fill="#38bdf8" font-weight="bold">36 தத்துவங்கள்</tspan>
        </text>
      </svg>
      <div class="diagram-footer">
        <p><strong>சித்தாந்த விளக்கம்:</strong> பருப்பொருளான உலகம் முதல் தூய சிவம் வரை 36 தத்துவங்களாக விரிந்துள்ளது. ஆன்மா அசுத்த தத்துவங்களின் மாயைப் பிடியிலிருந்து விடுபட்டு, சுத்த வித்தையைக் கடந்து சிவானந்தப் பெருவெளியில் கலப்பதே முக்தி.</p>
      </div>
    </div>
    """

# ===========================================================================
# 15. Ancient Tamil Music Scales (Panniru Thirumurai Panns)
# ===========================================================================
def generate_svg_isai_pann():
    """Diagram showing Ancient Tamil music scales (Pann) in Thirumurai and emotional rasas."""
    return """
    <div class="visual-diagram-card">
      <div class="diagram-header">
        <span class="diagram-tag">🎨 காட்சி விளக்கம்</span>
        <h4>பண்டைத் தமிழ் பண்ணிசை மரபு &amp; பன்னிரு திருமுறைகள்</h4>
      </div>
      <svg viewBox="0 0 700 255" class="pedagogy-svg" xmlns="http://www.w3.org/2000/svg">
        <rect width="700" height="255" rx="12" fill="rgba(11,15,22,0.92)" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
        
        <!-- 5 Tamil Landscape Panns -->
        <!-- 1. Kurinji -->
        <g transform="translate(25, 25)">
          <rect x="0" y="0" width="120" height="155" rx="8" fill="rgba(56,189,248,0.06)" stroke="#38bdf8" stroke-width="1.2"/>
          <circle cx="60" cy="25" r="14" fill="rgba(56,189,248,0.2)"/>
          <text x="60" y="30" text-anchor="middle" fill="#38bdf8" font-size="12">⛰️</text>
          
          <text x="60" y="56" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">குறிஞ்சிப் பண்</text>
          <text x="60" y="74" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="10.5">மலை நிலம்</text>
          
          <path d="M 15 84 L 105 84" stroke="rgba(255,255,255,0.1)"/>
          <text x="60" y="102" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="9.5">இராகம்:</text>
          <text x="60" y="118" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="10">ஹரிகாம்போஜி</text>
          <text x="60" y="140" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="9.5">சாந்த பக்தி &amp; வியப்பு</text>
        </g>

        <!-- 2. Mullai -->
        <g transform="translate(155, 25)">
          <rect x="0" y="0" width="120" height="155" rx="8" fill="rgba(52,211,153,0.06)" stroke="#34d399" stroke-width="1.2"/>
          <circle cx="60" cy="25" r="14" fill="rgba(52,211,153,0.2)"/>
          <text x="60" y="30" text-anchor="middle" fill="#34d399" font-size="12">🌲</text>
          
          <text x="60" y="56" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">முல்லைப் பண்</text>
          <text x="60" y="74" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="10.5">காடு நிலம்</text>
          
          <path d="M 15 84 L 105 84" stroke="rgba(255,255,255,0.1)"/>
          <text x="60" y="102" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="9.5">இராகம்:</text>
          <text x="60" y="118" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="10">மோகனம்</text>
          <text x="60" y="140" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="9.5">ஆனந்தம் &amp; தாய்மை</text>
        </g>

        <!-- 3. Marutham -->
        <g transform="translate(285, 25)">
          <rect x="0" y="0" width="120" height="155" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.2)" stroke-width="1.2"/>
          <circle cx="60" cy="25" r="14" fill="rgba(255,255,255,0.1)"/>
          <text x="60" y="30" text-anchor="middle" fill="#ffffff" font-size="12">🌾</text>
          
          <text x="60" y="56" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">மருதப் பண்</text>
          <text x="60" y="74" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="10.5">வயல் நிலம்</text>
          
          <path d="M 15 84 L 105 84" stroke="rgba(255,255,255,0.1)"/>
          <text x="60" y="102" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="9.5">இராகம்:</text>
          <text x="60" y="118" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="10">சங்கராபரணம்</text>
          <text x="60" y="140" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="9.5">கம்பீரம் &amp; விடியல்</text>
        </g>

        <!-- 4. Neithal -->
        <g transform="translate(415, 25)">
          <rect x="0" y="0" width="120" height="155" rx="8" fill="rgba(56,189,248,0.06)" stroke="#38bdf8" stroke-width="1.2"/>
          <circle cx="60" cy="25" r="14" fill="rgba(56,189,248,0.2)"/>
          <text x="60" y="30" text-anchor="middle" fill="#38bdf8" font-size="12">🌊</text>
          
          <text x="60" y="56" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">நெய்தல் பண்</text>
          <text x="60" y="74" text-anchor="middle" fill="#38bdf8" font-family="'Mukta Malar', sans-serif" font-size="10.5">கடல் நிலம்</text>
          
          <path d="M 15 84 L 105 84" stroke="rgba(255,255,255,0.1)"/>
          <text x="60" y="102" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="9.5">இராகம்:</text>
          <text x="60" y="118" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="10">தோடி (விளரி)</text>
          <text x="60" y="140" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="9.5">கருணை &amp; உருக்கம்</text>
        </g>

        <!-- 5. Paalai -->
        <g transform="translate(545, 25)">
          <rect x="0" y="0" width="120" height="155" rx="8" fill="rgba(245,158,11,0.06)" stroke="#f59e0b" stroke-width="1.2"/>
          <circle cx="60" cy="25" r="14" fill="rgba(245,158,11,0.2)"/>
          <text x="60" y="30" text-anchor="middle" fill="#f59e0b" font-size="12">🏜️</text>
          
          <text x="60" y="56" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11.5" font-weight="bold">பாலைப் பண்</text>
          <text x="60" y="74" text-anchor="middle" fill="#f59e0b" font-family="'Mukta Malar', sans-serif" font-size="10.5">பாலை நிலம்</text>
          
          <path d="M 15 84 L 105 84" stroke="rgba(255,255,255,0.1)"/>
          <text x="60" y="102" text-anchor="middle" fill="#cbd5e1" font-family="'Mukta Malar', sans-serif" font-size="9.5">இராகம்:</text>
          <text x="60" y="118" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="10">கரகரப்பிரியா</text>
          <text x="60" y="140" text-anchor="middle" fill="#34d399" font-family="'Mukta Malar', sans-serif" font-size="9.5">வைராக்கிய பக்தி</text>
        </g>

        <!-- Bottom Yazh / Thevaram Odhuvars Ribbon -->
        <g transform="translate(25, 195)">
          <rect x="0" y="0" width="640" height="42" rx="6" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
          <text x="320" y="18" text-anchor="middle" fill="#ffffff" font-family="'Mukta Malar', sans-serif" font-size="11.5">
            சம்பந்தரின் <tspan fill="#38bdf8" font-weight="bold">யாழ்முறிப் பண்</tspan> முதல் திருக்கோயில் ஓதுவார்களின் பன்னிரு திருமுறை இசை மரபு
          </text>
          <text x="320" y="34" text-anchor="middle" fill="#94a3b8" font-family="'Mukta Malar', sans-serif" font-size="10">
            குரல், துத்தம், கைக்கிளை, உழை, இளி, விளரி, தாரம் — தமிழின் ஆதி சப்த சுரங்கள்
          </text>
        </g>
      </svg>
      <div class="diagram-footer">
        <p><strong>இசைத்தமிழ் மரபு:</strong> பண்டைத் தமிழர்கள் ஐவகை நிலங்களின் இயல்புக்கேற்ப பண்களை வகுத்தனர். திருஞானசம்பந்தர், திருநாவுக்கரசர், சுந்தரமூர்த்தி நாயனார் மூவரும் திருப்பதிகங்களைப் பண்ணோடு பாடி இறையருள் பெற்றனர்.</p>
      </div>
    </div>
    """

# ===========================================================================
# Master Registry Map & Helper Dispatchers
# ===========================================================================
EXPANDED_DIAGRAM_MAP = {
    "murugan_vel": generate_svg_murugan_vel,
    "sakthi_srichakra": generate_svg_sakthi_srichakra,
    "vallalar_jyothi": generate_svg_vallalar_jyothi,
    "thirukkural_trivarga": generate_svg_thirukkural_trivarga,
    "nayanmar_lineage": generate_svg_nayanmar_lineage,
    "agamas_shastras": generate_svg_agamas_shastras,
    "pancha_bhuta": generate_svg_pancha_bhuta,
    "chakra_system": generate_svg_chakra_system,
    "deivathin_kural": generate_svg_deivathin_kural,
    "jivakarunyam": generate_svg_jivakarunyam,
    "konrai_vendhan": generate_svg_konrai_vendhan,
    "pranayama_breath": generate_svg_pranayama_breath,
    "sandhyavandanam": generate_svg_sandhyavandanam,
    "saiva_siddhanta_36_tattvas": generate_svg_saiva_siddhanta_36_tattvas,
    "isai_pann": generate_svg_isai_pann,
}

def get_expanded_diagram(diagram_key, fallback=None):
    """Retrieve an expanded SVG diagram by key."""
    if diagram_key in EXPANDED_DIAGRAM_MAP:
        return EXPANDED_DIAGRAM_MAP[diagram_key]()
    if fallback and callable(fallback):
        return fallback()
    return None

def get_combined_diagram_for_topic(diagram_key):
    """Universal diagram resolver across both original and expanded diagram suites."""
    if diagram_key in EXPANDED_DIAGRAM_MAP:
        return EXPANDED_DIAGRAM_MAP[diagram_key]()
    try:
        from visual_diagrams import DIAGRAM_MAP as BASE_DIAGRAM_MAP
        if diagram_key in BASE_DIAGRAM_MAP:
            return BASE_DIAGRAM_MAP[diagram_key]()
        if "dinacharya" in BASE_DIAGRAM_MAP:
            return BASE_DIAGRAM_MAP["dinacharya"]()
    except Exception:
        pass
    return generate_svg_thirukkural_trivarga()
