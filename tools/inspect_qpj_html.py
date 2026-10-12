import urllib.request
import sys
import re

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

url = "https://www.youtube.com/watch?v=qPjurMK6xpI"
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    raw = resp.read()

# Check raw bytes or decoded
text = raw.decode('utf-8', errors='ignore')
# Find unicode escaped Tamil
escaped = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), text)

print("In unescaped text:")
print("Has 'முதாகராத்த':", "முதாகராத்த" in escaped)
print("Has 'நிதாந்த காந்த':", "நிதாந்த காந்த" in escaped)
print("Has 'பஞ்சரத்னம்':", "பஞ்சரத்னம்" in escaped)
