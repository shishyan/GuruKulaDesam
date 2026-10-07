# -*- coding: utf-8 -*-
"""
Mirror Synchronization Utility for Gurukuladesam
Synchronizes active web files across the three project roots:
  1. Root repository (.)
  2. site/
  3. docs/ (GitHub Pages deploy target)
"""

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "site"
DOCS_DIR = ROOT / "docs"

# All core active HTML pages to mirror
HTML_FILES = [
    "about.html", "classes.html", "google-site.html", "help.html", "higher-studies.html",
    "index.html", "irai-isai-virundhu.html", "kalvi.html", "murugan.html",
    "review_quality.html", "saiva-neri.html", "sakthi.html", "sanmargam.html",
    "school.html", "syllabus.html", "thirukkural.html", "vaishnava.html",
    "vinayagar.html", "virtues.html", "youtube.html",
    "embed_amman.html", "embed_murugan.html", "embed_saiva_neri.html",
    "embed_shiva.html", "embed_thirukkural.html", "embed_vallalar_cultural.html",
    "embed_vallalar_sanmargam.html", "embed_vinayagar.html", "embed_vishnu_krishna.html"
] + [f"tharam-{i}.html" for i in range(1, 13)]

# Root-level PWA and manifest files
ROOT_PWA_FILES = ["manifest.json", "sw.js"]

ASSET_SUBDIRS = [
    "assets/css",
    "assets/js",
    "assets/data",
]

def sync_file(src, dst):
    if not src.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    # Check if content differs
    if not dst.exists() or src.read_bytes() != dst.read_bytes():
        shutil.copy2(src, dst)
        return True
    return False

def sync_all():
    print(f"Starting mirror synchronization from root to site/ and docs/...")
    copied_site = 0
    copied_docs = 0

    # 1. Sync HTML files
    for fn in HTML_FILES:
        src = ROOT / fn
        if not src.exists():
            print(f"[WARNING] Source file not found: {fn}")
            continue

        # Sync to site/
        if sync_file(src, SITE_DIR / fn):
            copied_site += 1

        # Sync to docs/
        if sync_file(src, DOCS_DIR / fn):
            copied_docs += 1

    # 2. Sync PWA files
    for fn in ROOT_PWA_FILES:
        src = ROOT / fn
        if src.exists():
            if sync_file(src, SITE_DIR / fn):
                copied_site += 1
            if sync_file(src, DOCS_DIR / fn):
                copied_docs += 1

    # 3. Sync core asset directories
    for sub in ASSET_SUBDIRS:
        src_dir = ROOT / sub
        if not src_dir.exists():
            continue
        for src_file in src_dir.glob("*.*"):
            rel = src_file.relative_to(ROOT)
            if sync_file(src_file, SITE_DIR / rel):
                copied_site += 1
            if sync_file(src_file, DOCS_DIR / rel):
                copied_docs += 1

    print(f"Synchronization complete:")
    print(f"  site/: {copied_site} files updated")
    print(f"  docs/: {copied_docs} files updated")

if __name__ == "__main__":
    sync_all()
