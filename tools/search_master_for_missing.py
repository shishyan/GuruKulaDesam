import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

master = json.load(open('master_all_598_songs_catalog.json', encoding='utf-8'))
print(f"Total songs in master catalog: {len(master)}")

search_terms = [
    'அவிநாசி', 'Avinasi',
    'புலம்பல்', 'Pulambal',
    'தென்னாடுடைய', 'Thennadudaiya',
    'ரேணுகா', 'Renuka',
    'கருமாரி', 'Karumari',
    'வேதசார', 'வேதஸார', 'Vedasar',
    'திருவையாறு', 'Thiruvaiyaru',
    'ரகுபதி', 'Raghupati',
    'நாராயண', 'Narayana',
    'தசாவதாரம்', 'Dasavatharam',
    'சிவ சுப்ரமணியர்',
    'மாதர்ப் பிறைக்'
]

for term in search_terms:
    matches = []
    for s in master:
        title = s.get('title', '')
        lyrics = s.get('lyrics', '')
        author = s.get('author', '')
        if term.lower() in title.lower() or term in lyrics:
            matches.append((s.get('id'), title, s.get('deity'), len(lyrics)))
    print(f"\n--- Search: '{term}' ({len(matches)} matches) ---")
    for m in matches[:5]:
        print(f"  [{m[0]}] {m[1]} | Deity: {m[2]} | lyr_len: {m[3]}")
