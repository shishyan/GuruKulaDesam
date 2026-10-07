# -*- coding: utf-8 -*-
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

card_updates = {
    2: {
        "badge": "5 விரிவுரை அலகுகள்",
        "desc": "சிவ சின்னங்கள், திருக்கோயில் கோபுர & நந்தி வழிபாடு, தோடுடைய செவியன் & கொன்றை வேந்தன் தர்மம்."
    },
    3: {
        "badge": "5 விரிவுரை அலகுகள்",
        "desc": "சமய குரவர் நால்வர், மாணிக்கவாசகரின் திருவெம்பாவை, பஞ்ச பூத ஸ்தலங்கள், மூதுரை & வேத காலை வந்தனம்."
    },
    4: {
        "badge": "5 விரிவுரை அலகுகள்",
        "desc": "பன்னிரு திருமுறைகள் முழுத் தொகுப்பு, அப்பரின் மாசில் வீணையும், சைவ விரதங்கள் & சாத்வீக உணவு நெறி."
    },
    5: {
        "badge": "5 விரிவுரை அலகுகள்",
        "desc": "63 நாயன்மார்கள் பக்தி, சுந்தரரின் திருத்தொண்டர் தொகை, திருக்குறள் அறத்துப்பால் & ஸ்ரீ ருத்ர நமக சாரம்."
    },
    6: {
        "badge": "5 விரிவுரை அலகுகள்",
        "desc": "நான்கு வேதங்களின் கட்டமைப்பு, தைத்திரீய சாந்தி மந்திரம், பதி-பசு-பாசம் & பஞ்ச மகா யக்ஞங்கள்."
    },
    7: {
        "badge": "5 விரிவுரை அலகுகள்",
        "desc": "உபநிடத மகா வாக்கியங்கள் (தத்துவமஸி), சதுர்வித புருஷார்த்தங்கள், பெரியபுராண தியாகம் & கர்ம வினைக் கோட்பாடு."
    },
    8: {
        "badge": "5 விரிவுரை அலகுகள்",
        "desc": "பகவத் கீதை கர்ம யோகம், 14 மெய்கண்ட சாத்திரங்கள், பன்னிரு திருமுறைப் பண்ணிசை, ஆசிரம தர்மம் & வள்ளலார் நெறி."
    },
    9: {
        "badge": "5 விரிவுரை அலகுகள்",
        "desc": "28 சைவ ஆகமங்கள், உடலே ஆலயம் (திருமந்திர உடலியல் தத்துவம்), பாரத ஷட்தர்சனங்கள், யம-நியம யோகம் & செங்கோன்மை."
    },
    10: {
        "badge": "O/L பாடநெறி • 5 அலகுகள்",
        "desc": "O/L பொதுத் தேர்வு முழுமைத் தத்துவம்: பதி-பசு-பாச விரிவுரை, நால்வகை நெறிகள், காஞ்சி மகா பெரியவா அருளுரைகள் & விரத மஹோத்ஸவங்கள்."
    },
    11: {
        "badge": "A/L உயர்தரம் • 5 அலகுகள்",
        "desc": "A/L தத்துவார்த்த ஒப்பாய்வு: அத்வைதம் vs சுத்தாத்வைதம், கடோபநிடதம் (மரணம் வென்ற நசிகேதன்), சிவஞானபோத 12 சூத்திரங்கள் & பஞ்ச கோச உளவியல்."
    },
    12: {
        "badge": "A/L பட்டம் • 5 அலகுகள்",
        "desc": "A/L முழுமை நிலை: ஜீவன் முக்தி, தாயுமானவர் & திருமந்திர சமரசம், நவீன குவாண்டம் இயற்பியலும் நடராஜ தத்துவமும், உலகளாவிய சனாதன தர்மம்."
    }
}

for folder in ['site', 'docs', '.']:
    prefix = f"{folder}/" if folder != '.' else ""
    kalvi_path = f"{prefix}kalvi.html"
    if not os.path.exists(kalvi_path):
        continue
    
    with open(kalvi_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for g, info in card_updates.items():
        # Update badge
        # Find the card block for tharam-g.html
        pattern = rf'(<a href="tharam-{g}\.html" class="grade-card">.*?<span class="grade-card-badge">)(.*?)(</span>.*?<p class="grade-card-desc"[^>]*>)(.*?)(</p>)'
        
        def replacer(m):
            return f"{m.group(1)}{info['badge']}{m.group(3)}{info['desc']}{m.group(5)}"
        
        content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    with open(kalvi_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Updated {kalvi_path}")

print("Curriculum Hub (kalvi.html) successfully updated!")
