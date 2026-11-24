#!/usr/bin/env python3
"""
Generate 1,008 categorized South Indian Cooking Recipes in clean Tamil editorial format
(zero emojis, zero decorative Unicode) organized by category for easy searching.
Uses Gemini API in batches of 36 recipes per category call (28 batches = 1,008 recipes).
"""
import json
import os
import re
import time
import urllib.request
from pathlib import Path

OUT_ROOT = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/south-indian-recipes-1008")
INDEX_JSON = OUT_ROOT / "RECIPES_1008_INDEX.json"
INDEX_MD = OUT_ROOT / "RECIPES_1008_INDEX.md"

CATEGORIES = [
    ("01_டிபன்_மற்றும்_காலை_உணவு", "Tiffin & Breakfast (Idli, Dosa, Pongal, Upma, Adai, Paniyaram, Appam, Idiyappam, Puttu)", 168),
    ("02_சாத_வகைகள்", "Variety Rice (Puliyodarai, Lemon Rice, Coconut Rice, Curd Rice, Bisibelebath, Tomato Rice, Pongal)", 120),
    ("03_சாம்பார்_குழம்பு_ரசம்", "Sambar, Kuzhambu & Rasam (Tiffin Sambar, Arachuvitta Sambar, Vatha Kuzhambu, Mor Kuzhambu, Pepper Rasam)", 168),
    ("04_பொரியல்_கூட்டு_வறுவல்", "Poriyal, Kootu & Curry (Poricha Kootu, Avial, Beans Poriyal, Vazhakkai Roast, Keerai Masiyal)", 168),
    ("05_சட்னி_துவையல்_ஊறுகாய்", "Chutney, Thogayal & Pickle (Coconut Chutney, Kara Chutney, Paruppu Thogayal, Mango Pickle, Vadagam)", 144),
    ("06_பலகாரம்_மற்றும்_இனிப்புகள்", "Traditional Snacks & Sweets (Murukku, Athirasam, Mysore Pak, Payasam, Kozhukattai, Sundal, Vadai)", 144),
    ("07_பண்டிகை_மற்றும்_பத்திய_உணவு", "Festival, Temple Prasadam & Pathiya Samayal (Sakkarai Pongal, Panchamirtham, Sukku Malli Coffee, Kashayam)", 96),
]


def sanitize_name(name: str) -> str:
    return re.sub(r"[^\w\u0B80-\u0BFF-]+", "_", name.strip()).strip("_")


def call_gemini_batch(api_key: str, cat_ta: str, cat_en: str, count: int, existing_titles: list[str]) -> list[dict]:
    avoid = ", ".join(existing_titles[-40:]) if existing_titles else "None"
    prompt = (
        f"Generate {count} unique, authentic South Indian vegetarian recipes in the category '{cat_en}' ({cat_ta}). "
        f"Do NOT repeat any of these titles: {avoid}. "
        "Return ONLY a valid JSON array of objects, each with keys: "
        "'title_ta' (Tamil recipe name), 'title_en' (English name), "
        "'ingredients_ta' (array of 5-8 concise Tamil ingredient strings), "
        "'steps_ta' (array of 3-5 concise Tamil preparation steps), "
        "'tip_ta' (1 concise Tamil cooking tip). "
        "STRICT: Zero emojis, zero decorative symbols, clean literary Tamil."
    )
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.7},
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)


def main() -> None:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is required")

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    index_entries: list[dict] = json.loads(INDEX_JSON.read_text(encoding="utf-8")) if INDEX_JSON.exists() else []
    existing_titles = [e["title_en"] for e in index_entries]
    recipe_num = len(index_entries) + 1

    for cat_ta, cat_en, target_count in CATEGORIES:
        cat_dir = OUT_ROOT / cat_ta
        cat_dir.mkdir(parents=True, exist_ok=True)
        already_in_cat = sum(1 for e in index_entries if e["category_ta"] == cat_ta)

        while already_in_cat < target_count:
            batch_n = min(24, target_count - already_in_cat)
            print(f"[{cat_ta}] Generating {batch_n} recipes ({already_in_cat}/{target_count})...", flush=True)
            items = call_gemini_batch(api_key, cat_ta, cat_en, batch_n, existing_titles)
            for item in items:
                if already_in_cat >= target_count:
                    break
                title_ta = item["title_ta"].strip()
                title_en = item["title_en"].strip()
                fname = f"recipe_{recipe_num:04d}_{sanitize_name(title_ta)[:50]}.txt"
                out_path = cat_dir / fname

                ing_lines = "\n".join(f"- {i.strip()}" for i in item["ingredients_ta"])
                step_lines = "\n".join(f"{idx}. {s.strip()}" for idx, s in enumerate(item["steps_ta"], 1))
                content = (
                    f"தென்னிந்திய சமையல் | {cat_ta.split('_', 1)[1].replace('_', ' ')} | {title_ta} ({title_en})\n\n"
                    f"தேவையான பொருட்கள்:\n{ing_lines}\n\n"
                    f"செய்முறை:\n{step_lines}\n\n"
                    f"சமையல் குறிப்பு:\n{item['tip_ta'].strip()}\n"
                )
                out_path.write_text(content, encoding="utf-8")

                index_entries.append({
                    "num": recipe_num,
                    "category_ta": cat_ta,
                    "title_ta": title_ta,
                    "title_en": title_en,
                    "rel_path": str(out_path.relative_to(OUT_ROOT)),
                })
                existing_titles.append(title_en)
                recipe_num += 1
                already_in_cat += 1

            INDEX_JSON.write_text(json.dumps(index_entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            time.sleep(2)

    md_lines = [
        "# 1008 தென்னிந்திய சமையல் குறிப்புகள் — வகைப்படுத்தப்பட்ட அட்டவணை",
        "",
        "| எண் | வகை | உணவுப் பெயர் | English Name | கோப்பு |",
        "|---:|---|---|---|---|",
    ]
    for e in index_entries:
        md_lines.append(f"| {e['num']} | {e['category_ta']} | {e['title_ta']} | {e['title_en']} | `{e['rel_path']}` |")
    INDEX_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"Generated {len(index_entries)} South Indian recipes in {OUT_ROOT}")


if __name__ == "__main__":
    main()
