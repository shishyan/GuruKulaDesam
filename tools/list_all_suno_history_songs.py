import sys, json

sys.stdout.reconfigure(encoding='utf-8')
edge = json.load(open('scratch/edge_suno.json', encoding='utf-8'))
chrome = json.load(open('scratch/chrome_suno.json', encoding='utf-8'))
all_urls = edge + chrome

seen = set()
for item in all_urls:
    t = item.get('title', '')
    u = item.get('url', '').split('?')[0]
    if '/song/' in u and u not in seen:
        seen.add(u)
        print(f"{t} ---> {u}")
