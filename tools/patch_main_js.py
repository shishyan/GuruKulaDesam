#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch main.js to update resolvePageContext and highlightActiveSidebarGroup
"""

import re

MAIN_JS_PATH = r"c:\GitHub\Gurukuladesam\assets\js\main.js"

with open(MAIN_JS_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Replace resolvePageContext
new_resolve_page_context = '''function resolvePageContext() {
  const path = window.location.pathname.toLowerCase();
  const filename = path.split('/').pop() || 'index.html';

  const contextMap = {
    'index.html': { root: 'ஆசிரம முகப்பு', stage: 'வித்யாபீடம்', rootLink: 'index.html', title: 'ஆன்மீகப் பெருவெளி', desc: '580 பக்தி இசை வெளியீடுகள்' },
    'kalvi.html': { root: 'பாடத்திட்டம்', stage: 'வாழ்வியல் சாதனா', rootLink: 'kalvi.html', title: 'வாழ்வியல் மையம்', desc: '12 வாழ்வியல் நிலைகள் வழிகாட்டி' },
    'school.html': { root: 'பாடத்திட்டம்', stage: 'வித்யா குடீரம்', rootLink: 'school.html', title: 'குருகுல இணையப் பள்ளி போர்டல்', desc: '21-ஆம் நூற்றாண்டு நவீன மாணவர் கற்றல் தளம்' },
    'syllabus.html': { root: 'பாடத்திட்டம்', stage: 'பாடத்திட்டம்', rootLink: 'syllabus.html', title: 'பதஞ்சலி 7-படிநிலை வரைபடம்', desc: 'WBS முறைசார் பாடநெறி & பதஞ்சலி 7-படிநிலை மதிப்பீடு' },
    'books.html': { root: 'பாடநூல்கள்', stage: '7 ஆசிரம நூல்கள்', rootLink: 'books.html', title: '7 ஆசிரமப் பாடநூல்கள் மின்னூல் அரங்கம்', desc: 'தரம் 1 முதல் 12 வரை 7 நூல்கள் முழு வாசிப்பு' },
    'classes.html': { root: 'பாடத்திட்டம்', stage: 'வகுப்புகள்', rootLink: 'classes.html', title: 'பாடநெறி நேரடி வகுப்புகள் & அட்டவணை', desc: 'குருகுல முறை நேரடிப் பயிற்சி & வழிகாட்டல்' },
    'virtues.html': { root: 'பாடத்திட்டம்', stage: 'நற்பண்புகள்', rootLink: 'virtues.html', title: 'அகர வரிசை நற்பண்பு நெறிமுறை', desc: '30+ நற்பண்புகள் • 4 வாழ்வியல் பருவங்கள்' },
    'grihastha.html': { root: 'வாழ்வியல் சாதனா', stage: 'இல்லற நெறி', rootLink: 'grihastha.html', title: 'இல்லற தர்ம சாசனம்', desc: 'பஞ்ச மகா யக்ஞ டிராக்கர் & குடும்ப சாசனம்' },
    'siddha.html': { root: 'வாழ்வியல் சாதனா', stage: 'சித்தர் வாழ்வியல்', rootLink: 'siddha.html', title: 'பதினெண் சித்தர் வாழ்வியல் & மூலிகைகள்', desc: 'முப்பிணி சமநிலை & மூலிகை மருத்துவம்' },

    // Stage 1: பாலப் பருவம் (Grades 1 - 4 • அற அடித்தளம் & புராணங்கள்)
    'tharam-1.html': { root: 'பாலப் பருவம் (1-4)', stage: 'தரம் 1', rootLink: 'school.html', title: 'தரம் 1 — 7 ஆசிரமப் பாடநூல்கள்', desc: 'பாலப் பருவ அன்பு & இல்லறத் தொடக்கப் பழக்கங்கள்' },
    'tharam-2.html': { root: 'பாலப் பருவம் (1-4)', stage: 'தரம் 2', rootLink: 'school.html', title: 'தரம் 2 — 7 ஆசிரமப் பாடநூல்கள்', desc: 'சிவ சின்னங்கள், பக்தி & இல்லற தர்மம்' },
    'tharam-3.html': { root: 'பாலப் பருவம் (1-4)', stage: 'தரம் 3', rootLink: 'school.html', title: 'தரம் 3 — 7 ஆசிரமப் பாடநூல்கள்', desc: 'நல்வழி, ஒழுக்கம் & ஆசாரக் கல்வி' },
    'tharam-4.html': { root: 'பாலப் பருவம் (1-4)', stage: 'தரம் 4', rootLink: 'school.html', title: 'தரம் 4 — 7 ஆசிரமப் பாடநூல்கள்', desc: 'கொன்றை வேந்தன் & இல்லற நன்னெறி' },
    'vinayagar.html': { root: 'பாலப் பருவம் (1-4)', stage: 'ஆரம்பக் கல்வித் தெய்வம்', rootLink: 'vinayagar.html', title: 'விநாயகர் அகவல் & மூல கணபதி', desc: 'தரம் 1–3 நற்துணை & நற்சொல் பாடம்' },
    'murugan.html': { root: 'பாலப் பருவம் (1-4)', stage: 'ஒழுக்க நெறி', rootLink: 'murugan.html', title: 'தமிழ் தெய்வம் முருகன் & கந்த சஷ்டி', desc: 'தரம் 3–7 நற்துணை & நற்செயல் பாடம்' },

    // Stage 2: இளம் பருவம் (Grades 5 - 8 • திருமுறைகள், பண்பாடு & சமூகம்)
    'tharam-5.html': { root: 'இளம் பருவம் (5-8)', stage: 'தரம் 5', rootLink: 'school.html', title: 'தரம் 5 — 7 ஆசிரமப் பாடநூல்கள்', desc: 'திருமுறைகள் & சுற்றந்தழால் தர்மம்' },
    'tharam-6.html': { root: 'இளம் பருவம் (5-8)', stage: 'தரம் 6', rootLink: 'school.html', title: 'தரம் 6 — 7 ஆசிரமப் பாடநூல்கள்', desc: 'சைவ சித்தாந்த ஆரம்ப நெறி & கடமை உணர்வு' },
    'tharam-7.html': { root: 'இளம் பருவம் (5-8)', stage: 'தரம் 7', rootLink: 'school.html', title: 'தரம் 7 — 7 ஆசிரமப் பாடநூல்கள்', desc: 'திருமுறைகள் & நாயன்மார் தியாக வரலாறு' },
    'tharam-8.html': { root: 'இளம் பருவம் (5-8)', stage: 'தரம் 8', rootLink: 'school.html', title: 'தரம் 8 — 7 ஆசிரமப் பாடநூல்கள்', desc: 'பொறையுடைமை, ஆசிரம தர்மம் & ஆலய தத்துவம்' },
    'panpaadu.html': { root: 'இளம் பருவம் (5-8)', stage: 'பண்பாட்டு நெறி', rootLink: 'panpaadu.html', title: 'தமிழர் பண்பாடு & 12 மாத விழாக்கள்', desc: 'தரம் 6–8 நற்சொல் & நற்செயல் பாடம்' },
    'vaishnava.html': { root: 'இளம் பருவம் (5-8)', stage: 'பக்தி இலக்கியம்', rootLink: 'vaishnava.html', title: 'அரங்கன் & கிருஷ்ணர் வைணவம்', desc: 'தரம் 2–5 & 7 நற்துணை பாடம்' },
    'sakthi.html': { root: 'இளம் பருவம் (5-8)', stage: 'சக்தி உபாசனை', rootLink: 'sakthi.html', title: 'அம்பிகை சக்தி நெறி & அபிராமி அந்தாதி', desc: 'தரம் 4–8 நற்துணை பாடம்' },

    // Stage 3: உயர்நிலைப் பருவம் (Grades 9 - 10 • அறநெறி, வள்ளலார் & சைவ சித்தாந்தம்)
    'tharam-9.html': { root: 'உயர்நிலைப் பருவம் (9-10)', stage: 'தரம் 9', rootLink: 'school.html', title: 'தரம் 9 — 7 ஆசிரமப் பாடநூல்கள்', desc: 'சான்றாண்மை, புலனடக்கம் & குடும்ப மாண்பு' },
    'tharam-10.html': { root: 'உயர்நிலைப் பருவம் (9-10)', stage: 'தரம் 10', rootLink: 'school.html', title: 'தரம் 10 — 7 ஆசிரமப் பாடநூல்கள்', desc: 'O/L வாழ்வியல் நன்னெறி & பதி-பசு-பாச ஆய்வு' },
    'thirukkural.html': { root: 'உயர்நிலைப் பருவம் (9-10)', stage: 'முதன்மை அறநூல்', rootLink: 'thirukkural.html', title: 'திருக்குறள் (1330 அருங்குறள்கள்)', desc: 'தரம் 1–12 நல்லறம் & நன்னெறி பாடம்' },
    'saiva-neri.html': { root: 'உயர்நிலைப் பருவம் (9-10)', stage: 'சைவ சித்தாந்தம்', rootLink: 'saiva-neri.html', title: 'பன்னிரு திருமுறைகள் & 172 பதிகங்கள்', desc: 'தரம் 5–12 நற்துணை & நற்சிந்தனை பாடம்' },
    'sanmargam.html': { root: 'உயர்நிலைப் பருவம் (9-10)', stage: 'சன்மார்க்க நெறி', rootLink: 'sanmargam.html', title: 'வள்ளலார் சுத்த சன்மார்க்கம் & திருவருட்பா', desc: 'தரம் 9–10 & 12 நற்சிந்தனை பாடம்' },

    // Stage 4: மேல்நிலை & உயர்கல்வி (Grades 11 - 12 & வேத-நவீன உயர்கல்வி)
    'tharam-11.html': { root: 'மேல்நிலை & உயர்கல்வி', stage: 'தரம் 11', rootLink: 'higher-studies.html', title: 'தரம் 11 — 7 ஆசிரமப் பாடநூல்கள்', desc: 'A/L உயர்தர தத்துவ ஒப்பாய்வு & சிவஞானபோதம்' },
    'tharam-12.html': { root: 'மேல்நிலை & உயர்கல்வி', stage: 'தரம் 12', rootLink: 'higher-studies.html', title: 'தரம் 12 — 7 ஆசிரமப் பாடநூல்கள்', desc: 'உன்னத இல்லற தர்மம் வழி ஆத்ம நிர்வாணம் / முக்தி' },
    'higher-studies.html': { root: 'மேல்நிலை & உயர்கல்வி', stage: 'வித்யாபீடம்', rootLink: 'higher-studies.html', title: 'வேதாந்த வித்யாபீடம் — வேத-நவீன உயர்கல்வி', desc: 'பிரஸ்தானத்ரயம், மெய்கண்ட சாத்திரங்கள் & அத்வைத ஆய்வு' },
    'about.html': { root: 'மேல்நிலை & உயர்கல்வி', stage: 'வேதாந்த ஆய்வு', rootLink: 'about.html', title: 'காஞ்சி மகா பெரியவா அருளுரைகள் & தெய்வத்தின் குரல்', desc: 'தரம் 11–12 & உயர்கல்வி வேதாந்த நன்னெறி' },

    // பாட ஆதாரக் களஞ்சியம் (Curriculum Media & Source Archives)
    'irai-isai-virundhu.html': { root: 'பாட ஆதாரங்கள்', stage: 'இசை அரங்கம்', rootLink: 'irai-isai-virundhu.html', title: 'இறை இசை விருந்து (600+)', desc: 'தரம் 1–6 நற்சொல் பண்ணிசைப் பாடம்' },
    'youtube.html': { root: 'பாட ஆதாரங்கள்', stage: 'காணொளிகள்', rootLink: 'youtube.html', title: 'YouTube காணொளி ஆய்வகம்', desc: '12 வகுப்புகளுக்கான 600+ கல்வி வீடியோக்கள்' },
    'sannidhis.html': { root: 'பாட ஆதாரங்கள்', stage: 'சந்நிதிகள்', rootLink: 'sannidhis.html', title: '8 ஆசிரம சந்நிதிகள் காட்சியகம்', desc: 'திருக்கோயில் வழிபாட்டின் தத்துவம்' },
    'moola-nool.html': { root: 'பாட ஆதாரங்கள்', stage: 'சுவடிகள்', rootLink: 'moola-nool.html', title: 'மூல நூல் களஞ்சியம் (சாத்திரங்கள்)', desc: 'ஓலைச்சுவடி மூல நூல்கள்' },
    'google-site.html': { root: 'இணைப்பு', stage: 'கூகிள் தளம்', rootLink: 'google-site.html', title: 'அதிகாரப்பூர்வ கூகிள் தளம்', desc: 'Google Sites நேரடி பார்வை' },
    'review_quality.html': { root: 'பாட ஆதாரங்கள்', stage: 'திரைத் தரம்', rootLink: 'review_quality.html', title: 'திரைத் தர ஆய்வு அரங்கம்', desc: 'திருக்குறள் மாஸ்டர் சினிமா ஆய்வு' },
    'help.html': { root: 'உதவி மையம்', stage: 'வழிகாட்டி', rootLink: 'help.html', title: 'உதவி & வழிகாட்டல் மையம் (Help & Support)', desc: 'மாணவர், ஆசான் & பயனர் வழிகாட்டிகள்' }
  };

  return contextMap[filename] || { root: 'குரு குல தேசம்', stage: 'பாட அரங்கம்', rootLink: 'school.html', title: 'ஆன்மீகக் களஞ்சியம்', desc: '' };
}'''

resolve_pattern = re.compile(r'function resolvePageContext\(\)\s*\{.*?return contextMap\[filename\]\s*\|\|\s*\{[^}]+\};\s*\}', re.DOTALL)
if resolve_pattern.search(content):
    content = resolve_pattern.sub(new_resolve_page_context, content, count=1)
    print("Patched resolvePageContext in main.js")
else:
    print("Could not match resolvePageContext pattern")

# Replace highlightActiveSidebarGroup
new_highlight = '''function highlightActiveSidebarGroup() {
  const path = window.location.pathname.toLowerCase();
  const filename = path.split('/').pop() || 'index.html';

  document.querySelectorAll('#leftStripBar .strip-group').forEach(group => {
    // 1. Direct link match
    const matchingLink = group.querySelector(`a[href="${filename}"]`);
    if (matchingLink) {
      group.classList.add('active', 'open');
      matchingLink.classList.add('active');
    }

    // 2. Stages group matching
    const groupKey = group.getAttribute('data-group');
    if (groupKey === 'stages') {
      const stagePages = [
        'tharam-1.html', 'tharam-2.html', 'tharam-3.html', 'tharam-4.html',
        'tharam-5.html', 'tharam-6.html', 'tharam-7.html', 'tharam-8.html',
        'tharam-9.html', 'tharam-10.html', 'tharam-11.html', 'tharam-12.html',
        'vinayagar.html', 'murugan.html', 'panpaadu.html', 'vaishnava.html',
        'sakthi.html', 'thirukkural.html', 'saiva-neri.html', 'sanmargam.html',
        'higher-studies.html', 'about.html'
      ];
      if (stagePages.includes(filename) || filename.startsWith('tharam-')) {
        group.classList.add('active', 'open');
        const stagePill = group.querySelector(`a[href="${filename}"]`);
        if (stagePill) stagePill.classList.add('active');
      }
    }
  });
}'''

highlight_pattern = re.compile(r'function highlightActiveSidebarGroup\(\)\s*\{.*?document\.querySelectorAll\(\'#leftStripBar \.strip-group\'\)\.forEach\(group => \{.*?\}\);\s*\}', re.DOTALL)
if highlight_pattern.search(content):
    content = highlight_pattern.sub(new_highlight, content, count=1)
    print("Patched highlightActiveSidebarGroup in main.js")
else:
    print("Could not match highlightActiveSidebarGroup pattern")

with open(MAIN_JS_PATH, "w", encoding="utf-8") as f:
    f.write(content)
print("Saved assets/js/main.js successfully.")
