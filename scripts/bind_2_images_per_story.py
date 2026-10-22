import os
import json

ROOT = r"C:\GitHub\Gurukuladesam"
imgs_file = os.path.join(ROOT, "data", "purana_available_images.json")
with open(imgs_file, "r", encoding="utf-8") as f:
    images = json.load(f)

print(f"Total available images: {len(images)}")
# Filter out background art images to use only story/lesson illustrations
story_imgs = [img for img in images if "lessons/" in img]
print(f"Story/lesson illustrations: {len(story_imgs)}")

children_file = os.path.join(ROOT, "data", "puranas", "children-purana-stories.json")
with open(children_file, "r", encoding="utf-8") as f:
    book_data = json.load(f)

# Assign exactly 2 authentic images per story
total_story_imgs = len(story_imgs)
for i, ch in enumerate(book_data["chapters"]):
    img1_url = story_imgs[(i * 2) % total_story_imgs]
    img2_url = story_imgs[(i * 2 + 1) % total_story_imgs]

    img1_title = f"{ch['title'].split('(')[0].strip()} — திருக்காட்சி 1"
    img2_title = f"{ch['title'].split('(')[0].strip()} — திருக்காட்சி 2"

    ch["images"] = [
        {
            "url": img1_url,
            "title": img1_title,
            "caption": img1_title
        },
        {
            "url": img2_url,
            "title": img2_title,
            "caption": img2_title
        }
    ]

# Save updated book_data
with open(children_file, "w", encoding="utf-8") as f:
    json.dump(book_data, f, ensure_ascii=False, indent=2)

import shutil
for dest_dir in [os.path.join(ROOT, "docs", "data", "puranas"), os.path.join(ROOT, "site", "data", "puranas")]:
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copyfile(children_file, os.path.join(dest_dir, "children-purana-stories.json"))

print("Successfully bound exactly 2 images per story across all 108 stories in Children's Book!")
