import json
import sys

# Let's inspect data/puranas/thiruvilaiyadal.json
with open('data/puranas/thiruvilaiyadal.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

sys.stdout.buffer.write((f"Title: {d.get('title')}\n").encode('utf-8'))
sys.stdout.buffer.write((f"Total chapters: {len(d.get('chapters', []))}\n").encode('utf-8'))
