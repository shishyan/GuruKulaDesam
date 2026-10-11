import sys, json, pathlib
sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent
mapped = json.load(open(ROOT / 'production' / 'thirukkural_playlist_items_mapped.json', encoding='utf-8'))
plan = json.load(open(ROOT / 'production' / 'thirukkural_sort_plan.json', encoding='utf-8'))
progress = json.load(open(ROOT / 'production' / 'playlist_sort_progress.json', encoding='utf-8'))

print("="*75)
print("THIRUKKURAL PLAYLIST SORTING STATUS (PLW7qBZp_Q8Ro)")
print("="*75)

sorted_items = []
pending_items = []

for item in plan:
    item_id = item['itemId']
    if progress.get(item_id, {}).get('sorted'):
        sorted_items.append(item)
    else:
        pending_items.append(item)

print(f"Total videos in playlist catalog: {len(mapped)}")
print(f"Total valid videos planned for Chapters 1-133: {len(plan)}")
print(f"Dead / Deleted videos in playlist: {len(mapped) - len(plan)} (will be cleaned/pushed to end)")
print(f"Successfully sorted & locked in place: {len(sorted_items)} items (Positions 0 through {len(sorted_items)-1})")
print(f"Remaining items to sort: {len(pending_items)} items (Positions {len(sorted_items)} through {len(plan)-1})")
print("-"*75)
print("CURRENTLY VERIFIED & LOCKED POSITIONS:")
print(f"{'Pos':<4} | {'Chap':<5} | {'Title'}")
print("-"*75)
for item in sorted_items:
    print(f"{item['target_position']:<4} | {item['chapter']:<5} | {item['title'][:55]}")

print("-"*75)
print("NEXT 5 ITEMS TO BE SORTED ON RESUME:")
print(f"{'Target Pos':<10} | {'Chap':<5} | {'Title'}")
print("-"*75)
for item in pending_items[:5]:
    print(f"{item['target_position']:<10} | {item['chapter']:<5} | {item['title'][:55]}")
print("="*75)
