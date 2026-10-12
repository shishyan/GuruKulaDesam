import re, json, sys

sys.stdout.reconfigure(encoding='utf-8')

for fname in ['scratch/suno_gurukuladesam.html', 'scratch/suno_shishyan.html']:
    html = open(fname, encoding='utf-8').read()
    print(f"=== File: {fname} ===")
    
    # Suno Next.js state embeds objects with 'title' and 'prompt'
    # Let's search for JSON snippets containing "title"
    # Find all occurrences of "title":"..."
    matches = re.findall(r'\"title\":\"([^\"]+)\"[^\{\}\[\]]*?\"prompt\":\"([^\"]*)\"', html)
    print("Direct title+prompt matches:", len(matches))
    for t, p in matches:
        p_clean = p.encode().decode('unicode-escape', errors='ignore')
        print(f"  Song: {t} | prompt len: {len(p_clean)}")
        if len(p_clean) > 0:
            print("    Sample:", p_clean[:120].replace('\n', ' '))
