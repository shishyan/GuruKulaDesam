import urllib.request, re, json, sys

sys.stdout.reconfigure(encoding='utf-8')
url = 'https://suno.com/song/4d6133cc-4ae7-41ca-aef4-818821a2fefd'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
print("HTML len:", len(html))

# Suno embeds clip data in self.__next_f.push lines
for line in html.split('\n'):
    if '4d6133cc' in line or 'prompt' in line:
        # Search for prompt/lyrics
        idx = line.find('"prompt"')
        if idx != -1:
            print("Found prompt in line! Substring:")
            sub = line[idx:idx+500]
            print(sub)
