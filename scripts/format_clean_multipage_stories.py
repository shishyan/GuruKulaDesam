"""
format_clean_multipage_stories.py
Removes all clutters (questions, 3D activity cards, tests, unnecessary badges)
and formats each story into a beautiful, multi-page reading book experience!
"""

import json
import re
import os
import shutil

ROOT_DIR = r"C:\GitHub\Gurukuladesam"
DATA_FILE = os.path.join(ROOT_DIR, "data", "puranas", "children-purana-stories.json")

def process_children_stories():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["summary"] = "குழந்தைகளுக்கான ஆன்மிக, அறநெறிப் புராண இதிகாசப் பெருங்கதைகள். எளிய நடை, நேரடிப் பக்க வாசிப்பு முறை."

    for ch in data["chapters"]:
        # Remove clutter keys
        for clutter_key in ["questions", "lifeApplication3Ds", "source", "moral_lesson"]:
            if clutter_key in ch:
                del ch[clutter_key]

        # Extract paragraphs
        raw_paras = re.findall(r"<p[^>]*>(.*?)</p>", ch["exposition"], re.DOTALL)
        if not raw_paras:
            # Fallback if no tags
            raw_paras = [p.strip() for p in ch["exposition"].split("\n\n") if p.strip()]

        # Clean each paragraph
        cleaned_paras = []
        for p in raw_paras:
            # Remove any residual moral lesson heading if in text
            p_clean = re.sub(r'<\/?(?:strong|b|span|div)[^>]*>', '', p).strip()
            if p_clean:
                cleaned_paras.append(p_clean)

        # Distribute into 3 to 4 pages per story for clean multi-page reading
        total_p = len(cleaned_paras)
        if total_p <= 6:
            per_page = 2
        elif total_p <= 9:
            per_page = 2
        else:
            per_page = 3

        pages = []
        for i in range(0, total_p, per_page):
            chunk = cleaned_paras[i : i + per_page]
            page_content = "".join([f"<p style='margin-bottom:24px; text-indent:1.5rem;'>{p}</p>" for p in chunk])
            pages.append(page_content)

        ch["pages"] = pages
        ch["totalPages"] = len(pages)

    # Save to data/
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Mirror to docs/ and site/
    for target_dir in [
        os.path.join(ROOT_DIR, "docs", "data", "puranas"),
        os.path.join(ROOT_DIR, "site", "data", "puranas")
    ]:
        os.makedirs(target_dir, exist_ok=True)
        dest = os.path.join(target_dir, "children-purana-stories.json")
        shutil.copyfile(DATA_FILE, dest)
        print(f"Mirrored clean multi-page stories to: {dest}")

    print("Success! Processed all chapters into multi-page pure stories without any clutter.")

if __name__ == "__main__":
    process_children_stories()
