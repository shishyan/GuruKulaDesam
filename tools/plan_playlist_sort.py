import sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

items = json.load(open('production/thirukkural_playlist_items_mapped.json', encoding='utf-8'))

# Filter out deleted/unmapped videos
valid_items = [it for it in items if it.get('resolved_chapter') is not None]
deleted_items = [it for it in items if it.get('resolved_chapter') is None]

print(f"Total items in playlist: {len(items)}")
print(f"Valid Thirukkural items: {len(valid_items)}")
print(f"Deleted/Unmapped items: {len(deleted_items)}")

# Sort valid items by:
# 1. Chapter number (1 to 133)
# 2. Title (to keep parts in order, e.g. பகுதி 1 before பகுதி 2)
def sort_key(it):
    chap = it['resolved_chapter']
    t = it['title']
    # If title has 'பகுதி 2' or 'Part 2', give higher sub-rank than 'பகுதி 1'
    part = 1
    if 'பகுதி 2' in t or 'Part 2' in t or 'II' in t:
        part = 2
    elif 'பகுதி 3' in t or 'Part 3' in t or 'III' in t:
        part = 3
    return (chap, part, t)

sorted_items = sorted(valid_items, key=sort_key)

print("\n--- Desired Order Sample (First 20 items) ---")
for idx, it in enumerate(sorted_items[:20]):
    print(f"Target Pos {idx:03d} | Chap {it['resolved_chapter']:03d} | Current Pos {it['position']:03d} | {it['title'][:40]}")

print("\n--- Desired Order Sample (Last 20 items) ---")
for idx, it in enumerate(sorted_items[-20:], len(sorted_items)-20):
    print(f"Target Pos {idx:03d} | Chap {it['resolved_chapter']:03d} | Current Pos {it['position']:03d} | {it['title'][:40]}")

# Save sorted plan
plan = []
for idx, it in enumerate(sorted_items):
    plan.append({
        'target_position': idx,
        'itemId': it['itemId'],
        'videoId': it['videoId'],
        'chapter': it['resolved_chapter'],
        'title': it['title'],
        'current_position': it['position']
    })

with open('production/thirukkural_sort_plan.json', 'w', encoding='utf-8') as f:
    json.dump(plan, f, indent=2, ensure_ascii=False)

print(f"\nSaved sorting plan with {len(plan)} items to production/thirukkural_sort_plan.json")
