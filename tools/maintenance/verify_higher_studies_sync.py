# -*- coding: utf-8 -*-
import os
import hashlib

def get_hash(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

files_to_check = [
    'higher-studies.html',
    'school.html',
    'kalvi.html',
    'tharam-12.html',
]

all_ok = True
for f in files_to_check:
    p_root = f
    p_site = os.path.join('site', f)
    p_docs = os.path.join('docs', f)

    if not (os.path.exists(p_root) and os.path.exists(p_site) and os.path.exists(p_docs)):
        print(f"MISSING: {f}")
        all_ok = False
        continue

    h_root = get_hash(p_root)
    h_site = get_hash(p_site)
    h_docs = get_hash(p_docs)

    if h_root == h_site == h_docs:
        print(f"MATCH [OK]: {f}")
    else:
        print(f"MISMATCH [FAIL]: {f} (root={h_root[:6]}, site={h_site[:6]}, docs={h_docs[:6]})")
        all_ok = False

with open('higher-studies.html', 'r', encoding='utf-8') as fp:
    hs_content = fp.read()
print("\n--- Higher Studies Content Verification ---")
print("Prasthanatraya Fellowship:", "பிரஸ்தானத்ரய ஆய்வுப் பட்டயம்" in hs_content)
print("Prakarana Granthas Track:", "தத்வ போதம்" in hs_content and "விவேகசூடாமணி" in hs_content)
print("Shaiva Siddhanta Track:", "சிவஞானபோதம்" in hs_content and "சிவஞான சித்தியார்" in hs_content)
print("Shad-Darshana & Epistemology Track:", "நியாய-வைசேஷிக பிரமாண சாஸ்திரம்" in hs_content)
print("Applied Vedanta Track:", "சுவாமி விவேகானந்தரின் பிரயோக வேதாந்தம்" in hs_content)
print("Glossary Engine:", "showGlossaryTerm" in hs_content)
print("Fellowship Certificate Generator:", "fellowshipFrame" in hs_content)

if all_ok:
    print("\nALL HIGHER STUDIES FILES FULLY SYNCHRONIZED AND VERIFIED!")
else:
    print("\nSOME FILES HAVE ISSUES.")
