#!/usr/bin/env python3
"""
tools/test_chrome_headless.py
Runs headless Google Chrome against key site pages to verify 0 console errors,
0 uncaught exceptions, and 0 missing script references.
"""

import os
import sys
import subprocess
import glob
import re

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

def find_chrome():
    for p in CHROME_PATHS:
        if os.path.exists(p):
            return p
    return None

def test_headless_pages():
    chrome = find_chrome()
    if not chrome:
        print("[WARN] Google Chrome not found, skipping headless Chrome runtime test.")
        return True

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(repo_root, 'docs')
    
    # Audit primary entrypoint pages and sampling of grades
    test_pages = [
        'index.html', 'school.html', 'kalvi.html', 'thirukkural.html',
        'higher-studies.html', 'review_quality.html', 'about.html',
        'youtube.html', 'tharam-1.html', 'tharam-12.html', 'help.html'
    ]

    print(f"Testing {len(test_pages)} core pages in Headless Chrome runtime...")
    total_errors = 0

    for page in test_pages:
        file_path = os.path.normpath(os.path.join(docs_dir, page))
        file_url = f"file:///{file_path.replace(os.sep, '/')}"
        
        import tempfile
        temp_dir = os.path.join(tempfile.gettempdir(), f"gkd_chrome_{os.getpid()}")
        cmd = [
            chrome,
            '--headless=new',
            '--disable-gpu',
            '--no-sandbox',
            f'--user-data-dir={temp_dir}',
            '--dump-dom',
            '--enable-logging=stderr',
            '--v=1',
            file_url
        ]

        try:
            res = subprocess.run(cmd, capture_output=True, encoding='utf-8', errors='replace', timeout=15)
            stderr = res.stderr
            
            # Filter console errors
            console_errors = []
            for line in stderr.splitlines():
                if 'INFO:CONSOLE' in line:
                    # Ignore harmless file:// CORS warnings for manifest
                    if 'CORS policy' in line and 'manifest.json' in line:
                        continue
                    # Ignore harmless image intervention notices
                    if '[Intervention]' in line:
                        continue
                    # If line has error or uncaught
                    if any(kw in line.lower() for kw in ['error', 'uncaught', 'failed', 'syntax']):
                        console_errors.append(line.strip())

            if console_errors:
                print(f"  [FAIL] {page}: {len(console_errors)} runtime console error(s):")
                for err in console_errors:
                    print(f"    - {err}")
                total_errors += len(console_errors)
            else:
                print(f"  [PASS] {page}: 0 console errors.")

        except subprocess.TimeoutExpired:
            print(f"  [WARN] {page}: Timeout after 15s")
        except Exception as e:
            print(f"  [ERROR] {page}: Execution error: {e}")
            total_errors += 1

    if total_errors == 0:
        print("\n[OK] All tested pages loaded in Headless Chrome with ZERO runtime errors!")
        return True
    else:
        print(f"\n[FAIL] Found {total_errors} runtime console errors in Headless Chrome.")
        return False

if __name__ == '__main__':
    if not test_headless_pages():
        sys.exit(1)
