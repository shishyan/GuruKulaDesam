import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

req = urllib.request.Request("http://127.0.0.1:9225/json/new", method='PUT')
try:
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode())
except Exception as e:
    print("Error:", e)
