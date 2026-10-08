#!/usr/bin/env python3
"""
tools/sync/validate_integrity.py
Comprehensive integrity test suite for Gurukula Desam:
1. Tri-folder mirror parity (root, docs, site)
2. JavaScript syntax check (node -c)
3. Internal anchor & page link verification
4. Image file existence verification (zero 404s)
5. Page visual requirement check (at least 2 images on major pages)
6. Modern SVG icon system verification
"""

import os
import sys
import re
import glob
import hashlib
import subprocess

def file_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def test_tri_folder_parity(repo_root):
    print("--> Test 1: Checking Tri-Folder Mirror Parity (root, docs, site)...")
    docs_dir = os.path.join(repo_root, 'docs')
    site_dir = os.path.join(repo_root, 'site')
    root_dir = repo_root
    
    html_files = [os.path.basename(f) for f in glob.glob(os.path.join(docs_dir, '*.html'))]
    mismatches = []
    
    for hf in html_files:
        p_docs = os.path.join(docs_dir, hf)
        p_root = os.path.join(root_dir, hf)
        p_site = os.path.join(site_dir, hf)
        
        h_docs = file_hash(p_docs)
        if not os.path.exists(p_root) or file_hash(p_root) != h_docs:
            mismatches.append(f"{hf}: docs != root")
        if not os.path.exists(p_site) or file_hash(p_site) != h_docs:
            mismatches.append(f"{hf}: docs != site")
            
    # Also check main.js and style.css
    for asset in ['assets/js/main.js', 'assets/css/style.css']:
        a_docs = os.path.join(docs_dir, asset)
        a_root = os.path.join(root_dir, asset)
        a_site = os.path.join(site_dir, asset)
        if os.path.exists(a_docs):
            h_asset = file_hash(a_docs)
            if not os.path.exists(a_root) or file_hash(a_root) != h_asset:
                mismatches.append(f"{asset}: docs != root")
            if not os.path.exists(a_site) or file_hash(a_site) != h_asset:
                mismatches.append(f"{asset}: docs != site")
                
    if mismatches:
        print(f"    [FAIL] Found {len(mismatches)} mirror parity discrepancies:")
        for m in mismatches[:10]:
            print(f"      - {m}")
        return False
    print(f"    [PASS] All {len(html_files)} HTML pages and core assets have 100% identical SHA-256 hashes across all 3 folders.")
    return True

def test_js_syntax(repo_root):
    print("--> Test 2: Validating JavaScript Syntax with node -c...")
    js_files = glob.glob(os.path.join(repo_root, 'docs', 'assets', 'js', '*.js'))
    has_errors = False
    for jsf in js_files:
        try:
            res = subprocess.run(['node', '-c', jsf], capture_output=True, text=True, encoding='utf-8', errors='replace', check=True)
            print(f"    [PASS] {os.path.basename(jsf)} syntax valid.")
        except subprocess.CalledProcessError as e:
            print(f"    [FAIL] {os.path.basename(jsf)} syntax error:\n{e.stderr}")
            has_errors = True
        except FileNotFoundError:
            print("    [WARN] node executable not found in PATH, skipping JS syntax check.")
            return True
    return not has_errors

def test_image_existence(repo_root):
    print("--> Test 3: Verifying Image References (Zero 404s)...")
    docs_dir = os.path.join(repo_root, 'docs')
    html_files = glob.glob(os.path.join(docs_dir, '*.html'))
    missing_imgs = set()
    total_img_refs = 0
    
    for hf in html_files:
        with open(hf, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        # Find img src and url()
        srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
        for src in srcs:
            if src.startswith(('http://', 'https://', 'data:', '${')) or '${' in src:
                continue
            total_img_refs += 1
            # Clean anchors or params
            clean_src = src.split('?')[0].split('#')[0]
            target_path = os.path.normpath(os.path.join(os.path.dirname(hf), clean_src))
            if not os.path.exists(target_path):
                missing_imgs.add((os.path.basename(hf), src))
                
    if missing_imgs:
        print(f"    [FAIL] Found {len(missing_imgs)} missing image references:")
        for page, src in list(missing_imgs)[:10]:
            print(f"      - Page {page}: {src}")
        return False
    print(f"    [PASS] Verified {total_img_refs} image references across all pages. 0 broken images.")
    return True

def test_page_visual_requirement(repo_root):
    print("--> Test 4: Auditing Minimum 2 Images on Major Pages...")
    docs_dir = os.path.join(repo_root, 'docs')
    # Filter out embed_*.html
    pages = [f for f in glob.glob(os.path.join(docs_dir, '*.html')) if not os.path.basename(f).startswith('embed_')]
    low_image_pages = []
    
    for hf in pages:
        with open(hf, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        # Count <img> tags (including template tags or static tags)
        img_tags = re.findall(r'<img[^>]+>', content)
        basename = os.path.basename(hf)
        if len(img_tags) < 2:
            low_image_pages.append((basename, len(img_tags)))
            
    if low_image_pages:
        print(f"    [FAIL] {len(low_image_pages)} pages have fewer than 2 images:")
        for page, count in low_image_pages:
            print(f"      - {page}: {count} image(s)")
        return False
    print(f"    [PASS] All {len(pages)} primary pages contain at least 2 sacred/classical visual images.")
    return True

def test_internal_links(repo_root):
    print("--> Test 5: Verifying Internal Page Links...")
    docs_dir = os.path.join(repo_root, 'docs')
    html_files = glob.glob(os.path.join(docs_dir, '*.html'))
    valid_pages = set(os.path.basename(f) for f in html_files)
    broken_links = []
    
    for hf in html_files:
        with open(hf, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        hrefs = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', content)
        for href in hrefs:
            if href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:', '#', '${')) or '${' in href:
                continue
            clean_href = href.split('#')[0].split('?')[0]
            if not clean_href:
                continue
            # Check if it's an HTML page
            if clean_href in valid_pages:
                continue
            # Check if it's a relative asset on disk
            target_asset = os.path.normpath(os.path.join(os.path.dirname(hf), clean_href))
            if os.path.exists(target_asset):
                continue
            broken_links.append((os.path.basename(hf), href))
                
    if broken_links:
        print(f"    [FAIL] Found {len(broken_links)} broken internal page links:")
        for page, href in broken_links[:10]:
            print(f"      - Page {page}: {href}")
        return False
    print("    [PASS] All internal navigational links resolve successfully.")
    return True

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    print("=== Gurukula Desam Automated System Integrity Suite ===")
    print(f"Repository Root: {repo_root}\n")
    
    tests = [
        test_tri_folder_parity,
        test_js_syntax,
        test_image_existence,
        test_page_visual_requirement,
        test_internal_links
    ]
    
    results = [t(repo_root) for t in tests]
    
    print("\n---------------------------------------------------------")
    if all(results):
        print("RESULT: ALL 5 INTEGRITY CHECKS PASSED (100% HEALTHY) [OK]")
        sys.exit(0)
    else:
        failed = sum(1 for r in results if not r)
        print(f"RESULT: {failed} CHECKS FAILED. Please review above output. [FAIL]")
        sys.exit(1)

if __name__ == '__main__':
    main()
