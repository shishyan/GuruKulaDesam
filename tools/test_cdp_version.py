import urllib.request
import json

try:
    with urllib.request.urlopen("http://127.0.0.1:9225/json/version", timeout=3) as resp:
        print(resp.read().decode())
except Exception as e:
    print("Error:", e)
