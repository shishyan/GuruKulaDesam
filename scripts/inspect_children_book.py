import json
import sys

with open("data/puranas/children-purana-stories.json", "r", encoding="utf-8") as f:
    d = json.load(f)

sys.stdout.buffer.write((f"Title: {d['title']}\n").encode('utf-8'))
sys.stdout.buffer.write((f"Total stories: {len(d['chapters'])}\n").encode('utf-8'))
for i, ch in enumerate(d['chapters']):
    sys.stdout.buffer.write((f"Story {i+1}: {ch['title']} ({len(ch['exposition'])} chars)\n").encode('utf-8'))
