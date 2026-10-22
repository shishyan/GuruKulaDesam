import urllib.request, urllib.parse, json, sys, ssl
sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Queries targeting authentic Sri Lanka / Jaffna preserved documents on Internet Archive
queries = [
    'jaffna puranam',
    'jaffna mahabharata',
    'jaffna ramayana',
    'arumuga navalar',
    'arumuka navalar',
    'damodaram pillai',
    'ceylon saiva',
    'jaffna saiva',
    'vidyanupalana'
]

for q in queries:
    url = f'https://archive.org/advancedsearch.php?q={urllib.parse.quote(q)}&fl[]=identifier,title,creator,year,mediatype,collection&rows=5&output=json'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        data = json.loads(urllib.request.urlopen(req, context=ctx).read().decode('utf-8'))
        docs = data.get('response', {}).get('docs', [])
        num_found = data.get('response', {}).get('numFound', 0)
        print(f"=== Query: '{q}' -> {num_found} items ===")
        for d in docs:
            print(f"  - ID: {d.get('identifier')} | Title: {d.get('title')} | Year: {d.get('year')}")
    except Exception as e:
        print(f"Query {q} error:", e)
