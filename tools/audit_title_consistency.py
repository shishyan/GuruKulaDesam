import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/data/catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

print("=== CHECKING POTENTIAL TITLE MISALIGNMENTS IN CATALOG ===")
# Check if title has mismatched work (e.g., says Vinayagar but under Shiva, or mentions different saint)
anomalies = []
for vault, songs in cat.items():
    if not isinstance(songs, list): continue
    for s in songs:
        t = s.get('title', '')
        sid = s.get('id', '')
        
        # Check vault vs title consistency
        if vault == 'thirukkural' and 'திருக்குறள்' not in t and 'அதிகாரம்' not in t:
            anomalies.append((vault, sid, t, 'Thirukkural song missing Kural/Adhigaram'))
        if vault == 'vinayagar' and not any(k in t for k in ['விநாயக', 'கணேச', 'கண நாதா']):
            anomalies.append((vault, sid, t, 'Vinayagar vault song missing Vinayagar terms'))

print(f"Vault vs Title anomalies: {len(anomalies)}")
for a in anomalies:
    print(a)
