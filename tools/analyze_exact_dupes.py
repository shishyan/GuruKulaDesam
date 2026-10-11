import json, sys

sys.stdout.reconfigure(encoding='utf-8')
data = json.load(open('production/duplicates_audit_report.json', encoding='utf-8'))
exact_groups = data['exact_raw_title_and_duration_duplicates']

print(f"Total exact duplicate groups: {len(exact_groups)}\n")

candidates_to_privatize = []

for i, g in enumerate(exact_groups, 1):
    title = g['title']
    dur = g['duration_sec']
    vids = g['videos']
    
    # Prioritize:
    # 1. public over private
    # 2. higher view count
    # 3. earlier publishedAt
    vids_sorted = sorted(
        vids,
        key=lambda x: (
            1 if x['privacyStatus'] == 'public' else 0,
            x['viewCount'],
            -int(x['publishedAt'].replace('-', '').replace(':', '').replace('T', '').replace('Z', '')[:14])
        ),
        reverse=True
    )
    
    primary = vids_sorted[0]
    dupes = vids_sorted[1:]
    
    print(f"[{i:02d}] '{title[:55]}' ({dur}s):")
    print(f"     [KEEP] -> {primary['id']} (Views: {primary['viewCount']}, Date: {primary['publishedAt']}, {primary['privacyStatus']})")
    for d in dupes:
        print(f"     [HIDE] -> {d['id']} (Views: {d['viewCount']}, Date: {d['publishedAt']}, {d['privacyStatus']})")
        if d['privacyStatus'] != 'private':
            candidates_to_privatize.append({
                'id': d['id'],
                'title': d['title'],
                'keep_id': primary['id'],
                'views': d['viewCount'],
                'primary_views': primary['viewCount']
            })

print("\n" + "=" * 60)
print(f"TOTAL EXACT DUPLICATE VIDEOS CURRENTLY PUBLIC THAT SHOULD BE PRIVATE/UNLISTED: {len(candidates_to_privatize)}")
print("=" * 60)

with open('production/exact_duplicates_to_privatize.json', 'w', encoding='utf-8') as f:
    json.dump(candidates_to_privatize, f, indent=2, ensure_ascii=False)
