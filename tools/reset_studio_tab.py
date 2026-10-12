import urllib.request, json, time

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json').read())
studio_tabs = [t for t in tabs if t.get('type') == 'page' and 'studio.youtube.com' in t.get('url', '')]

for t in studio_tabs:
    print(f"Closing tab {t['id']} ({t['url']})...")
    urllib.request.urlopen(f"http://127.0.0.1:9225/json/close/{t['id']}")
    time.sleep(1)

print("Opening fresh tab for PO4U3nRv6o0 translations...")
new_tab = json.loads(urllib.request.urlopen("http://127.0.0.1:9225/json/new?https://studio.youtube.com/video/PO4U3nRv6o0/translations").read())
print("New tab created:", new_tab)
