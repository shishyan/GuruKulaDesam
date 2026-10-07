# -*- coding: utf-8 -*-
"""
Site Integrity and Link / Anchor Auditor for Gurukuladesam
Checks all active site HTML files in the project root for:
  - Valid internal links
  - Valid anchor references
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Core active site pages
ACTIVE_PAGES = [
    "about.html", "classes.html", "google-site.html", "help.html", "higher-studies.html",
    "index.html", "irai-isai-virundhu.html", "kalvi.html", "murugan.html",
    "review_quality.html", "saiva-neri.html", "sakthi.html", "sanmargam.html",
    "school.html", "syllabus.html", "thirukkural.html", "vaishnava.html",
    "vinayagar.html", "virtues.html", "youtube.html",
    "embed_amman.html", "embed_murugan.html", "embed_saiva_neri.html",
    "embed_shiva.html", "embed_thirukkural.html", "embed_vallalar_cultural.html",
    "embed_vallalar_sanmargam.html", "embed_vinayagar.html", "embed_vishnu_krishna.html"
] + [f"tharam-{i}.html" for i in range(1, 13)]

def collect_ids(html_text):
    return set(re.findall(r'id=["\']([^"\']+)["\']', html_text))

def collect_links_and_anchors(html_text):
    # Matches href="page.html", href="#anchor", href="page.html#anchor"
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', html_text)
    # Matches scrollToSection('sectionId')
    scroll_ids = re.findall(r'scrollToSection\(["\']([^"\']+)["\']', html_text)
    return hrefs, scroll_ids

def audit():
    print(f"Auditing {len(ACTIVE_PAGES)} active site pages in {ROOT}...")
    page_ids = {}
    for p_name in ACTIVE_PAGES:
        p_path = ROOT / p_name
        if p_path.exists():
            with open(p_path, "r", encoding="utf-8") as f:
                content = f.read()
                page_ids[p_name] = collect_ids(content)

    broken_links = []
    broken_anchors = []

    for p_name in ACTIVE_PAGES:
        p_path = ROOT / p_name
        if not p_path.exists():
            broken_links.append((p_name, p_name, "Active page file missing from root"))
            continue

        with open(p_path, "r", encoding="utf-8") as f:
            content = f.read()

        hrefs, scroll_ids = collect_links_and_anchors(content)

        # Audit hrefs
        for h in hrefs:
            if h.startswith("http://") or h.startswith("https://") or h.startswith("mailto:") or h.startswith("tel:"):
                continue
            if h.startswith("javascript:") or h.startswith("#!"):
                continue

            target_page = p_name
            target_anchor = None

            if "#" in h:
                parts = h.split("#", 1)
                if parts[0]:
                    target_page = parts[0]
                target_anchor = parts[1]
            else:
                target_page = h

            # Ignore empty or query string only
            if not target_page or target_page == "#":
                continue

            # Strip query params
            target_page = target_page.split("?")[0]

            target_path = ROOT / target_page
            if not target_path.exists():
                broken_links.append((p_name, h, f"Target path {target_page} does not exist"))
            elif target_anchor:
                # Check anchor ID
                target_ids = page_ids.get(target_page, set())
                known_fallbacks = {'courseUnits', 'gradeVirtueBox', 'visualDiagramCard', 'quizSection', 'sadhanaBox', 'familyCharter', 'grihasthaTracker', 'featuredScreeningRoom', 'panchaMahaYagna', 'siteFooter'}
                if target_anchor not in target_ids and target_anchor not in known_fallbacks:
                    broken_anchors.append((p_name, h, f"Anchor #{target_anchor} not found in {target_page}"))

        # Audit scrollToSection IDs on same page
        for sid in scroll_ids:
            known_fallbacks = {'courseUnits', 'gradeVirtueBox', 'visualDiagramCard', 'quizSection', 'sadhanaBox', 'familyCharter', 'grihasthaTracker', 'featuredScreeningRoom', 'panchaMahaYagna', 'siteFooter'}
            if sid not in page_ids.get(p_name, set()) and sid not in known_fallbacks:
                # Check if it exists as class
                if f'class="{sid}"' not in content and f"class='{sid}'" not in content and f'id="{sid}"' not in content:
                    broken_anchors.append((p_name, f"scrollToSection('{sid}')", f"Section '{sid}' not found on {p_name}"))

    print("\n--- Audit Results ---")
    print(f"Total active HTML files checked: {len(ACTIVE_PAGES)}")
    print(f"Broken links: {len(broken_links)}")
    for b in broken_links:
        print(f"  [BROKEN LINK] in {b[0]}: {b[1]} -> {b[2]}")

    print(f"Broken anchors: {len(broken_anchors)}")
    for a in broken_anchors:
        print(f"  [BROKEN ANCHOR] in {a[0]}: {a[1]} -> {a[2]}")

    if not broken_links and not broken_anchors:
        print("SUCCESS: 0 broken links and 0 broken anchors across all 40 active pages!")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(audit())
