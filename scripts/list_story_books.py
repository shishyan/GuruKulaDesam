import json
import sys

with open('data/puranas/puranas_index.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)['catalog']

verse_files = {'kandha-puranam', 'thiruvilaiyadal', 'periyapuranam', 'ramayanam', 'thirumandhiram'}
story_cat = [p for p in cat if p['id'] not in verse_files]
sys.stdout.buffer.write((f"Story catalog books count: {len(story_cat)}\n").encode('utf-8'))
for p in story_cat:
    sys.stdout.buffer.write((f"- {p['id']}: {p['title']}\n").encode('utf-8'))
