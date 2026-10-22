import json
import glob
import os

pattern = "data/puranas/*.json"
catalog = []

for filepath in sorted(glob.glob(pattern)):
    fname = os.path.basename(filepath)
    if fname in ("puranas_index.json", "puranas-index.json"):
        continue
    with open(filepath, "r", encoding="utf-8") as f:
        d = json.load(f)
    
    catalog.append({
        "id": d["id"],
        "title": d["title"],
        "category": d.get("category", "புராண இதிகாசம்"),
        "author": d.get("author", "சனாதன முனிவர் மரபு"),
        "summary": d.get("summary", ""),
        "icon": d.get("icon", "📖"),
        "color": d.get("color", "#f59e0b"),
        "sections_name": d.get("sections_name", "அத்தியாயம்"),
        "total_chapters": len(d.get("chapters", []))
    })

index_data = {
    "total_puranas": len(catalog),
    "catalog": catalog
}

with open("data/puranas/puranas_index.json", "w", encoding="utf-8") as f:
    json.dump(index_data, f, ensure_ascii=False, indent=2)

with open("data/puranas-index.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

print(f"Generated clean puranas catalog with {len(catalog)} story books!")
