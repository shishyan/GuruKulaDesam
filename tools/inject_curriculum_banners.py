#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inject Curriculum Affiliation Banners into Scripture, Deity, Media and Ashram Portals.
Seamlessly integrates all standalone portals into the School Curriculum and 7 Sacred Books.
"""

import os
import re

ROOT_DIR = r"c:\GitHub\Gurukuladesam"

PORTALS = {
    "thirukkural.html": {
        "grade_range": "தரம் 1–12 (முழுப் பள்ளி)",
        "book_name": "நூல் 2: நல்லறம் & நூல் 1: நன்னெறி",
        "title": "திருக்குறள் — குருகுலப் பள்ளியின் முதன்மை அறநூல் அடித்தளம்",
        "subtext": "தொடக்கப் பள்ளி முதல் மேல்நிலை வரை மாணவர்களின் அன்றாட இல்லறவியல் மற்றும் குடிமை தர்மப் பயிற்சிகள் திருக்குறளை மையமாகக் கொண்டு கட்டமைக்கப்பட்டுள்ளன.",
        "deep_link": "books.html?grade=6&book=nallaram"
    },
    "vinayagar.html": {
        "grade_range": "தரம் 1–3 & தரம் 8",
        "book_name": "நூல் 4: நற்துணை & நூல் 6: நற்சொல்",
        "title": "விநாயகர் வழிபாடு — தொடக்கக் கல்வி மங்களம் & நாத யோகப் பாடம்",
        "subtext": "ஔவையாரின் வாக்குண்டாம், ஆத்திசூடி முதல் விநாயகர் அகவலின் குண்டலினி யோக ரகசியங்கள் வரை தரம் 1–3 மற்றும் தரம் 8 பாடங்களில் பயிற்றுவிக்கப்படுகிறது.",
        "deep_link": "books.html?grade=1&book=narthunai"
    },
    "murugan.html": {
        "grade_range": "தரம் 3–7 & தரம் 10",
        "book_name": "நூல் 4: நற்துணை & நூல் 7: நற்செயல்",
        "title": "முருக நெறி — விவேகம், துணிவு மற்றும் கந்தர் அநுபூதி ஆன்மீகப் பாடம்",
        "subtext": "கந்த சஷ்டி கவசத்தின் உடல்-மன பாதுகாப்புச் சாதனாவும், அருணகிரிநாதரின் திருப்புகழ் மற்றும் அநுபூதி ஞானமும் நடுநிலை மற்றும் உயர்நிலைப் பாடநூல்களில் இடம்பெற்றுள்ளன.",
        "deep_link": "books.html?grade=3&book=narthunai"
    },
    "saiva-neri.html": {
        "grade_range": "தரம் 5–8 & தரம் 11–12",
        "book_name": "நூல் 4: நற்துணை & நூல் 5: நற்சிந்தனை",
        "title": "சைவ நெறி — பன்னிரு திருமுறைகள் & மெய்கண்ட சைவ சித்தாந்தப் பாடம்",
        "subtext": "நாயன்மார்களின் தேவாரப் பண்ணிசை பக்தி தரம் 5–8 நற்துணையிலும், சிவஞானபோத மெய்யியல் தரம் 11–12 நற்சிந்தனையிலும் உயர்நிலைப் பாடமாக அமைகின்றன.",
        "deep_link": "books.html?grade=5&book=narthunai"
    },
    "sakthi.html": {
        "grade_range": "தரம் 4–8",
        "book_name": "நூல் 4: நற்துணை & நூல் 1: நன்னெறி",
        "title": "சக்தி நெறி — அகிலாண்டேஸ்வரி அருள், அபிராமி அந்தாதி & தாய்மை விழுமியம்",
        "subtext": "பெற்றோர் மரியாதை, காரைக்கால் அம்மையாரின் பக்தி மற்றும் தேவி சூக்தப் போற்றிகள் தரம் 4 முதல் 8 வரை நற்துணை மற்றும் நன்னெறி நூல்களில் ஒருங்கிணைக்கப்பட்டுள்ளன.",
        "deep_link": "books.html?grade=4&book=narthunai"
    },
    "vaishnava.html": {
        "grade_range": "தரம் 2–5 & தரம் 7, 11",
        "book_name": "நூல் 4: நற்துணை & நூல் 2: நல்லறம்",
        "title": "வைணவ நெறி — பால கிருஷ்ண லீலை, திருப்பாவை & பகவத் கீதா சரணாகதி",
        "subtext": "தொடக்கப் பள்ளி மாணவர்களுக்கு பால கிருஷ்ணரின் கதைகளும், தரம் 7 மற்றும் 11 மாணவர்களுக்கு நாலாயிர திவ்வியப் பிரபந்தம் மற்றும் கீதையின் சரணாகதி தர்மமும் பயிற்றுவிக்கப்படுகிறது.",
        "deep_link": "books.html?grade=2&book=narthunai"
    },
    "sanmargam.html": {
        "grade_range": "தரம் 9–10 & தரம் 12",
        "book_name": "நூல் 5: நற்சிந்தனை & நூல் 2: நல்லறம்",
        "title": "வள்ளலார் சுத்த சன்மார்க்கம் — ஜீவகாருண்ய ஒழுக்கம் & திருவருட்பா உயர் பாடம்",
        "subtext": "சாதி சமய பேதமற்ற ஆன்மநேய ஒருமைப்பாடு மற்றும் அருட்பெருஞ்ஜோதி தரிசனம் உயர்நிலைப் பள்ளி தரம் 9–10 மற்றும் 12 நற்சிந்தனை நூலில் அதிமுக்கியப் பாடமாக அமைந்துள்ளது.",
        "deep_link": "books.html?grade=10&book=narchinthanai"
    },
    "about.html": {
        "grade_range": "தரம் 11–12 & உயர்கல்வி",
        "book_name": "நூல் 5: நற்சிந்தனை & வேத-நவீன வேதாந்தம்",
        "title": "காஞ்சி மகா பெரியவா அருளுரைகள் — தெய்வத்தின் குரல் & வேதாந்த நன்னெறி",
        "subtext": "மேல்நிலைப் பள்ளி தரம் 11–12 மாணவர்களுக்கும் உயர்கல்வி ஆராய்ச்சி மாணவர்களுக்கும் அத்வைத சாரம், வேத ரக்ஷணம் மற்றும் சமய நல்லிணக்கத்தை வழங்கும் உயர்நிலைப் பாடநெறி.",
        "deep_link": "books.html?grade=11&book=narchinthanai"
    },
    "irai-isai-virundhu.html": {
        "grade_range": "தரம் 1–6",
        "book_name": "நூல் 6: நற்சொல் & நூல் 4: நற்துணை",
        "title": "இறை இசை விருந்து — தொடக்க & நடுநிலைப் பள்ளி 5 அமிர்த பண்ணிசைப் பாடங்கள்",
        "subtext": "விநாயகர் துதி, குரு வணக்கம், கந்தர் அநுபூதி, தேசபக்தி கானம் மற்றும் சிவபுராணம் ஆகிய ஐந்து அமிர்த கானங்கள் நற்சொல் நூலின் அதிகாரப்பூர்வ இசைப் பாடத்திட்டமாகும்.",
        "deep_link": "books.html?grade=1&book=narchol"
    },
    "youtube.html": {
        "grade_range": "தரம் 1–12 (முழுப் பள்ளி)",
        "book_name": "7 ஆசிரம நூல்களின் வீடியோ ஆடியோ களஞ்சியம்",
        "title": "YouTube அதிகாரப்பூர்வ ஒளிக்களஞ்சியம் — 12 வகுப்புகளுக்கான 600+ கல்விச் சான்றாதாரங்கள்",
        "subtext": "133 திருக்குறள் சினிமா திரைப்படங்கள், திருமுறைப் பதிகங்கள், மற்றும் பக்தி இசை வெளியீடுகள் அனைத்தும் பள்ளிப் பாடநூல்களின் அத்தியாயக் காணொளிகளாக இணைக்கப்பட்டுள்ளன.",
        "deep_link": "books.html?grade=1&book=nanneri"
    },
    "panpaadu.html": {
        "grade_range": "தரம் 6–8",
        "book_name": "நூல் 6: நற்சொல் & நூல் 7: நற்செயல்",
        "title": "தமிழர் பண்பாடும் 12 மாத விழாக்களும் — நடுநிலைப் பள்ளி சமுதாய அறிவியல் சாதனா",
        "subtext": "விருந்தோம்பல், உழவுத் திருநாள், ஐந்திணை நிலவியல், மற்றும் 12 மாத விழாக்களின் தத்துவங்கள் தரம் 6–8 நற்சொல் மற்றும் நற்செயல் நூல்களில் சமூகக் கடமையாகப் புகட்டப்படுகின்றன.",
        "deep_link": "books.html?grade=6&book=narchol"
    },
    "sannidhis.html": {
        "grade_range": "தரம் 1–12 (முழுப் பள்ளி)",
        "book_name": "நூல் 4: நற்துணை & நூல் 7: நற்செயல்",
        "title": "ஆசிரம மகா சந்நிதிகள் — திருக்கோயில் வழிபாட்டு ஒழுக்கம் & அறிவியல்",
        "subtext": "பஞ்ச மகா யாகங்கள், ஆலய பிரதிஷ்டா விஞ்ஞானம் மற்றும் சந்நிதி வழிபாட்டு ஆசாரங்கள் நற்துணை நூலில் விரிவாகப் பயிற்றுவிக்கப்படுகின்றன.",
        "deep_link": "books.html?grade=4&book=narthunai"
    }
}

def build_banner_html(info):
    return f'''
      <!-- CURRICULUM AFFILIATION BANNER COMPONENT -->
      <div class="curriculum-affiliation-banner" style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.92)); border: 1.5px solid rgba(212, 175, 55, 0.45); border-radius: 16px; padding: 16px 22px; margin: 18px 0 24px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 0 20px rgba(212, 175, 55, 0.05); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
        <div style="display: flex; align-items: center; gap: 14px; flex: 1; min-width: 280px;">
          <div style="background: rgba(212, 175, 55, 0.15); border: 1px solid rgba(212, 175, 55, 0.4); color: var(--gold-bright, #facc15); width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:24px;height:24px;"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 2 3 3 6 3s6-1 6-3v-5"/></svg>
          </div>
          <div>
            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 4px;">
              <span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.35); font-size: 0.72rem; font-weight: 800; padding: 2px 8px; border-radius: 6px; text-transform: uppercase;">குருகுலப் பள்ளிப் பாடத்திட்ட இணைப்பு</span>
              <span style="background: rgba(212, 175, 55, 0.2); color: var(--gold-bright, #facc15); font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 6px;">தரம்: {info['grade_range']}</span>
              <span style="background: rgba(16, 185, 129, 0.15); color: #34d399; font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 6px;">நூல்: {info['book_name']}</span>
            </div>
            <div style="color: #ffffff; font-size: 0.98rem; font-weight: 700;">
              {info['title']}
            </div>
            <p style="color: #94a3b8; font-size: 0.84rem; margin: 3px 0 0 0; line-height: 1.5;">
              {info['subtext']}
            </p>
          </div>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
          <a href="{info['deep_link']}" class="sheet-btn sheet-btn-view" style="font-weight: 700; font-size: 0.84rem; padding: 8px 16px; border-radius: 10px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap;">
            <span>பள்ளிப் பாடநூலில் வாசிக்க</span>
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:14px;height:14px;"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </a>
        </div>
      </div>
'''

def inject_banner_into_file(filename, info):
    file_path = os.path.join(ROOT_DIR, filename)
    if not os.path.exists(file_path):
        print(f"File not found: {filename}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # If banner already present, replace it
    banner_pattern = re.compile(r'<!-- CURRICULUM AFFILIATION BANNER COMPONENT -->.*?</div>\s*</div>', re.DOTALL)
    if banner_pattern.search(content):
        content = banner_pattern.sub(build_banner_html(info).strip(), content, count=1)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated existing banner in: {filename}")
        return True

    # Otherwise inject right after class="hero-banner"...</div>
    hero_pattern = re.compile(r'(<div\s+class="hero-banner"[^>]*>.*?</div>)', re.DOTALL)
    if hero_pattern.search(content):
        banner_html = build_banner_html(info)
        content = hero_pattern.sub(r'\1\n' + banner_html, content, count=1)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Injected banner after hero-banner: {filename}")
        return True

    # Or inject after <main class="main-content">
    main_pattern = re.compile(r'(<main\s+class="main-content"[^>]*>)', re.DOTALL)
    if main_pattern.search(content):
        banner_html = build_banner_html(info)
        content = main_pattern.sub(r'\1\n' + banner_html, content, count=1)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Injected banner after main-content: {filename}")
        return True

    print(f"Could not find insertion point for: {filename}")
    return False

def main():
    print("=== Injecting Curriculum Affiliation Banners into Portals ===")
    for filename, info in PORTALS.items():
        inject_banner_into_file(filename, info)
    print("All portals successfully affiliated with the School Curriculum!")

if __name__ == "__main__":
    main()
