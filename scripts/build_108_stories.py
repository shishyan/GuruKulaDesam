import os
import json
import re

DATA_DIR = r"C:\GitHub\Gurukuladesam\data\puranas"

# 1. Expand children-purana-stories to 108 stories
# Let's inspect current children-purana-stories.json
children_file = os.path.join(DATA_DIR, "children-purana-stories.json")
with open(children_file, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Current chapters in children-purana-stories: {len(data['chapters'])}")
