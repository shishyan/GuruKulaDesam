import glob, re, sys

sys.stdout.reconfigure(encoding='utf-8')

PURE_CURRICULUM_FOOTER = """  <footer class="site-footer" id="siteFooter">
    <div class="footer-container">
      <div class="footer-col">
        <h4>குரு குல ஆசிரமம் (Guru Kula Ashram)</h4>
        <p>அனைத்து மெய்ஞ்ஞானக் கருத்துக்கள், திருமுறைகள், திருக்குறள், இறை இசை மற்றும் வாழ்வியல் தர்மங்கள் அனைத்தும் பள்ளிப் பாடத்திட்டம் (தரம் 1-12) மற்றும் உயர்கல்வி வித்யாபீடத்தின் (B.A., M.A., Ph.D.) 7 ஆசிரமப் பாடநூல்களுக்குள் ஒருங்கிணைக்கப்பட்டுள்ளன.</p>
        <p style="margin-top: 10px; color: var(--gold); font-weight: 600;">தரம் &rarr; 7 நூல்கள் &rarr; 49 அத்தியாயங்கள் &rarr; உட்பிரிவுகள் &rarr; விரிவான பாடங்கள்</p>
        <div style="margin-top: 14px; font-size: 0.84rem; color: #94a3b8; line-height: 1.6; border-left: 2px solid var(--gold); padding-left: 12px;">
          <strong>மைய வளாகம்:</strong> 32, SSS Jaya Enclave, Kovaipudur, Coimbatore, 641042, Tamil Nadu, India.
        </div>
      </div>
      <div class="footer-col">
        <h4>பள்ளிப் பருவங்கள் &amp; உயர்கல்வி</h4>
        <ul class="footer-links">
          <li><a href="admissions.html">🎒 மாணவர் சேர்க்கை (Online Admissions)</a></li>
          <li><a href="tharam-1.html">1. பாலப் பருவம் (தரம் 1–4) • அற அடித்தளம்</a></li>
          <li><a href="tharam-5.html">2. இளம் பருவம் (தரம் 5–8) • பண்பாடு &amp; நெறி</a></li>
          <li><a href="tharam-9.html">3. உயர்நிலைப் பருவம் (தரம் 9–10) • சித்தாந்தம் &amp; தர்மம்</a></li>
          <li><a href="tharam-11.html">4. மேல்நிலைப் பருவம் (தரம் 11–12) • கீதை &amp; பள்ளி இறுதி</a></li>
          <li><a href="higher-studies.html">5. உயர்கல்வி வித்யாபீடம் (B.A. இளங்கலை • M.A. முதுகலை • Ph.D. ஆய்வு)</a></li>
          <li><a href="school.html">வித்யா குடீரம் — இணையப் பள்ளி அரங்கம்</a></li>
          <li><a href="syllabus.html">பாடத்திட்ட வரைபடம் (Curriculum Matrix)</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>7 ஆசிரமப் பாடநூல்கள் (The 7 Books)</h4>
        <ul class="footer-links">
          <li><a href="books.html?book=nanneri">1. நன்னெறி (Nanneri — ஒழுக்கம் &amp; பணிவு)</a></li>
          <li><a href="books.html?book=nallaram">2. நல்லறம் (Nallaram — ஈகை &amp; ஜீவகாருண்யம்)</a></li>
          <li><a href="books.html?book=nalvazhi">3. நல்வழி (Nalvazhi — வாய்மை &amp; நேர்மை)</a></li>
          <li><a href="books.html?book=narthunai">4. நற்துணை (Narthunai — இறைத் துதி &amp; சரணாகதி)</a></li>
          <li><a href="books.html?book=narchinthanai">5. நற்சிந்தனை (Narchinthanai — விஞ்ஞானம் &amp; தத்துவம்)</a></li>
          <li><a href="books.html?book=narchol">6. நற்சொல் (Narchol — இன்சொல் &amp; கவிதை)</a></li>
          <li><a href="books.html?book=narcheyal">7. நற்செயல் (Narcheyal — இல்லற தர்மம் &amp; 3 Ds)</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      &copy; 2026 குரு குல ஆசிரமம் (Guru Kula Ashram) | வேத-நவீன பள்ளிப் பாடத்திட்டம் &amp; 7 ஆசிரமப் பாடநூல்கள் | அனைத்து உரிமைகளும் இறைப்பணிக்கே சமர்ப்பணம்.
    </div>
  </footer>"""

def apply_footers():
    files = sorted(glob.glob("*.html"))
    updated = 0
    for f in files:
        if f.startswith("scraped_"):
            continue
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
        
        # Match any <footer ... </footer>
        if re.search(r"<footer.*?</footer>", content, re.DOTALL):
            new_content = re.sub(r"<footer.*?</footer>", PURE_CURRICULUM_FOOTER, content, flags=re.DOTALL)
            if new_content != content:
                with open(f, "w", encoding="utf-8") as fp:
                    fp.write(new_content)
                updated += 1
                print(f"Updated footer in {f}")
    print(f"Total HTML files updated with Pure Curriculum Footer: {updated}")

if __name__ == "__main__":
    apply_footers()
