#!/usr/bin/env python3
"""
tools/sync/sync_trifolder.py
Synchronizes website files across the three mirrors:
1. Root directory (./)
2. docs/
3. site/

Usage:
  python tools/sync/sync_trifolder.py [--source docs|root|site]
Default source is docs/.
"""

import os
import sys
import shutil
import argparse
import hashlib

def file_hash(filepath):
    """Compute sha256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def sync_folders(repo_root, source_name='docs'):
    source_map = {
        'docs': os.path.join(repo_root, 'docs'),
        'root': repo_root,
        'site': os.path.join(repo_root, 'site')
    }
    
    src_dir = source_map.get(source_name)
    if not src_dir or not os.path.exists(src_dir):
        print(f"Error: Invalid source '{source_name}' or directory does not exist: {src_dir}")
        sys.exit(1)
        
    targets = [k for k in source_map.keys() if k != source_name]
    print(f"=== Gurukula Desam Tri-Folder Synchronizer ===")
    print(f"Source: {source_name} ({src_dir})")
    print(f"Targets: {', '.join(targets)}\n")
    
    # Files to sync:
    # 1. HTML files in source
    # 2. assets/ (css, js, images, audio, etc.)
    # 3. manifest.json, sw.js, CNAME if present
    
    # Collect source files
    items_to_copy = []
    
    # Root level web files in source
    for entry in os.listdir(src_dir):
        src_path = os.path.join(src_dir, entry)
        if os.path.isfile(src_path):
            if (entry.endswith('.html') and not entry.startswith('scraped_')) or entry in ['manifest.json', 'sw.js', 'CNAME']:
                items_to_copy.append(('file', entry))
        elif entry == 'assets':
            items_to_copy.append(('dir', 'assets'))
        elif entry == 'data':
            # Only sync data/books to keep mirrors clean and lightweight
            src_books = os.path.join(src_path, 'books')
            if os.path.exists(src_books):
                items_to_copy.append(('dir', os.path.join('data', 'books')))
            
    total_synced = 0
    total_bytes = 0
    
    for target_name in targets:
        target_dir = source_map[target_name]
        os.makedirs(target_dir, exist_ok=True)
        print(f"--> Syncing to target: {target_name} ({target_dir})")
        
        for kind, rel_path in items_to_copy:
            src_item = os.path.join(src_dir, rel_path)
            dest_item = os.path.join(target_dir, rel_path)
            
            if kind == 'file':
                src_hash = file_hash(src_item)
                dest_exists = os.path.exists(dest_item)
                if not dest_exists or file_hash(dest_item) != src_hash:
                    shutil.copy2(src_item, dest_item)
                    total_synced += 1
                    total_bytes += os.path.getsize(src_item)
                    print(f"    [Updated File] {rel_path}")
            elif kind == 'dir':
                # Walk the assets directory
                for root, _, files in os.walk(src_item):
                    rel_dir = os.path.relpath(root, src_dir)
                    target_sub_dir = os.path.join(target_dir, rel_dir)
                    os.makedirs(target_sub_dir, exist_ok=True)
                    
                    for f in files:
                        s_f = os.path.join(root, f)
                        d_f = os.path.join(target_sub_dir, f)
                        s_rel = os.path.relpath(s_f, src_dir)
                        if not os.path.exists(d_f) or file_hash(d_f) != file_hash(s_f):
                            shutil.copy2(s_f, d_f)
                            total_synced += 1
                            total_bytes += os.path.getsize(s_f)
                            # Print only non-image asset updates or summary
                            if not f.endswith(('.jpg', '.png', '.webp', '.svg')):
                                print(f"    [Updated Asset] {s_rel}")
                                
    print(f"\n[OK] Synchronization Complete! Total files updated: {total_synced} ({total_bytes / (1024*1024):.2f} MB)")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tri-folder site synchronizer")
    parser.add_argument('--source', choices=['docs', 'root', 'site'], default='docs', help="Source folder to sync from")
    args = parser.parse_args()
    
    # Calculate repo root (parent of tools/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    
    sync_folders(repo_root, source_name=args.source)
