import os
import json
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

queries = ["DCJ2qoMSIBA", "தியாக வண்ணப் பதிகம்", "அன்பு மாலை"]

for q in queries:
    print(f"\n--- Searching for: {q} ---")
    for fpath in glob.glob("**/*.json", recursive=True):
        if "node_modules" in fpath or ".git" in fpath:
            continue
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if q in content:
                    print(f"Found in {fpath}")
        except:
            pass
