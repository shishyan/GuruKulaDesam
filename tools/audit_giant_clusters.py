import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/data/catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

# Let's inspect the songs sharing Sivapuranam (156 songs)
siva_cluster = []
hare_cluster = []
arutperum_cluster = []
thiruppavai_cluster = []
abirami_cluster = []

for vault, songs in cat.items():
    if not isinstance(songs, list): continue
    for s in songs:
        sid = s.get('id', '')
        title = s.get('title', '')
        lyr = (s.get('lyrics') or '').strip()
        if 'நமச்சிவாய வாழ்க' in lyr:
            siva_cluster.append((vault, sid, title))
        elif 'ஹரே கிருஷ்ண' in lyr:
            hare_cluster.append((vault, sid, title))
        elif 'அருட்பெருஞ் சோதி' in lyr:
            arutperum_cluster.append((vault, sid, title))
        elif 'மார்கழித் திங்கள்' in lyr:
            thiruppavai_cluster.append((vault, sid, title))
        elif 'தனந்தரும் கல்வி தரும்' in lyr:
            abirami_cluster.append((vault, sid, title))

print(f"=== SIVAPURANAM CLUSTER ({len(siva_cluster)} songs) ===")
# Show first 20 titles
for vault, sid, title in siva_cluster[:25]:
    print(f"[{vault}] {sid}: {title}")

print(f"\n=== HARE KRISHNA CLUSTER ({len(hare_cluster)} songs) ===")
for vault, sid, title in hare_cluster[:15]:
    print(f"[{vault}] {sid}: {title}")

print(f"\n=== ARUTPERUM JOTHI CLUSTER ({len(arutperum_cluster)} songs) ===")
for vault, sid, title in arutperum_cluster[:15]:
    print(f"[{vault}] {sid}: {title}")

print(f"\n=== THIRUPPAVAI 1 CLUSTER ({len(thiruppavai_cluster)} songs) ===")
for vault, sid, title in thiruppavai_cluster[:15]:
    print(f"[{vault}] {sid}: {title}")

print(f"\n=== ABIRAMI 69 CLUSTER ({len(abirami_cluster)} songs) ===")
for vault, sid, title in abirami_cluster[:15]:
    print(f"[{vault}] {sid}: {title}")
