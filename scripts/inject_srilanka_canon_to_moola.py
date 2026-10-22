import json

with open('data/catalogs/authentic_srilanka_canon.json', 'r', encoding='utf-8') as f:
    canon_items = json.load(f)

# Load existing moola-nool-data.js
with open('assets/js/moola-nool-data.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

# We want to inject the 10 Sri Lankan canonical works into moola-nool-data.js
# First check if puranas-epics category exists in moola-nool-data.js
category_json = '''    {
      "id": "puranas-epics",
      "name": "ஈழத்து மூலப் பதிப்புகள் — புராணங்கள் & இதிகாசங்கள் (Authentic Jaffna Recensions)",
      "count": 10
    },'''

if '"id": "puranas-epics"' not in js_text:
    js_text = js_text.replace(
        '  "categories": [\n',
        '  "categories": [\n' + category_json + '\n'
    )

# Format each canon item into a scripture entry compatible with moola-nool-data.js
scriptures_to_add = {}
for item in canon_items:
    sc_id = item["id"]
    
    sections = []
    for sec in item.get("sampleSections", []):
        verses = []
        for v in sec.get("verses", []):
            verses.append({
                "num": v.get("num", ""),
                "rootSanskrit": "",
                "rootTamilTranslit": v.get("tamil", ""),
                "padavurai": v.get("padavurai", []),
                "bhavartha": v.get("meaning", v.get("bhavartha", "")),
                "notes": f"【குழந்தைகளுக்கான அறக்கதை】: {v.get('storyForKids', '')}\n\n【ஈழத்து மூல ஆவணக் குறிப்பு】: {item.get('scholarlySignificance', '')} (நூலக எண்: {item.get('noolahamId', '')})",
                "archivePdfUrl": item.get("pdfUrl", "")
            })
        sections.append({
            "id": sec.get("id", ""),
            "title": sec.get("title", ""),
            "verses": verses
        })
    
    scriptures_to_add[sc_id] = {
        "id": sc_id,
        "title": item.get("title", ""),
        "sanskritTitle": item.get("englishTitle", ""),
        "author": f"{item.get('author', '')} | பதிப்பாசிரியர்: {item.get('editor', '')}",
        "commentaryTradition": f"{item.get('publisher', '')} ({item.get('era', '')})",
        "category": "puranas-epics",
        "academicLevel": item.get("gradeLevel", "General"),
        "summary": f"{item.get('childrenFriendlySummary', '')}\n\n[அசல் ஏட்டுச்சுவடி / மூல ஆவணம்: {item.get('publisher', '')}, {item.get('pages', '')} பக்கங்கள்]",
        "noolahamId": item.get("noolahamId", ""),
        "archivePdfUrl": item.get("pdfUrl", ""),
        "rawPdfUrl": item.get("rawPdfUrl", ""),
        "sections": sections
    }

# Inject scriptures into js_text
# Find '"scriptures": {'
marker = '"scriptures": {\n'
idx = js_text.find(marker)
if idx != -1:
    entries_str = ""
    for k, sc in scriptures_to_add.items():
        if f'"{k}":' not in js_text:
            formatted = json.dumps(sc, ensure_ascii=False, indent=4)
            # Indent each line by 4 spaces
            indented = "\n".join("    " + line for line in formatted.splitlines())
            entries_str += f'    "{k}": {indented[4:]},\n'
    
    js_text = js_text[:idx + len(marker)] + entries_str + js_text[idx + len(marker):]

with open('assets/js/moola-nool-data.js', 'w', encoding='utf-8') as f:
    f.write(js_text)

print(f"Successfully integrated {len(scriptures_to_add)} authentic Sri Lankan scriptures into assets/js/moola-nool-data.js!")
