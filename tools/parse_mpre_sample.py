import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('production/sample_mpre_browse.json', encoding='utf-8') as f:
    d = json.load(f)

def find_items(obj, path=''):
    if isinstance(obj, dict):
        if 'videoId' in obj:
            vid = obj['videoId']
            parent_keys = list(obj.keys())
            title = obj.get('title')
            print(f"Path: {path} | videoId: {vid} | parent: {parent_keys[:5]}")
            if title:
                print(f"   title: {title}")
        for k, v in obj.items():
            find_items(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            find_items(item, f"{path}[{i}]")

find_items(d)
