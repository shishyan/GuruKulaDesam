import sys, json
sys.stdout.reconfigure(encoding='utf-8')

already_completed = set([
    'Mata6vtnrjQ', 'KFtS403RfbY', 'mQpQEuXiEZ4', '31xVgvxoiUA',
    'AW4cljBWy2w', 'QH-xL37NmGM', 'hm7_qUlTUiU', 't0MRlpqBeJQ',
    'pC5eSiEaar0', 'FVkGdLV7O34', '9iB-E9CpWUo', 'mG9IzlD9vmI',
    'TUwlsvN7v1w', 'klSi7r6YhCU', 'PO4U3nRv6o0', '255aVCj3t0w',
    'KjQZFlnCluU', 'HPP3IG7DWRc', 'ETELjf0OTi4'
])

with open('production/target_priority_queue.json', 'r', encoding='utf-8') as f:
    queue = json.load(f)

pending_kural = [t for t in queue['kural'] if t[0] not in already_completed]
pending_devotional = [t for t in queue['devotional'] if t[0] not in already_completed]

print(f"Pending Kural Athikarams: {len(pending_kural)}")
print(f"Pending Devotional Hymns: {len(pending_devotional)}")

print("\n--- First 10 Pending Kural Athikarams ---")
for vid, title in pending_kural[:10]:
    print(f" - {vid}: {title}")

print("\n--- First 10 Pending Devotional Tracks ---")
for vid, title in pending_devotional[:10]:
    print(f" - {vid}: {title}")

with open('production/pending_work_batches.json', 'w', encoding='utf-8') as f:
    json.dump({
        'pending_kural': pending_kural,
        'pending_devotional': pending_devotional
    }, f, indent=2, ensure_ascii=False)
