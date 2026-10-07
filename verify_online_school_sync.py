# -*- coding: utf-8 -*-
import os
import hashlib

def get_hash(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

files_to_check = [
    'school.html',
    'kalvi.html',
    'index.html',
    'assets/css/style.css',
] + [f'tharam-{g}.html' for g in range(1, 13)]

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

with open('school.html', 'r', encoding='utf-8') as fp:
    school_content = fp.read()
print("\n--- Content Key Feature Verification ---")
print("Web Audio Temple Bell in school.html:", "playTempleBell()" in school_content)
print("4-7-8 Pranayama in school.html:", "runBreathCycle()" in school_content)
print("Pomodoro Focus Timer in school.html:", "timerDisplay" in school_content)
print("Official Certificate Generator in school.html:", "certificate-preview-card" in school_content)
print("Flashcards in school.html:", "flipFlashcard()" in school_content)

with open('tharam-2.html', 'r', encoding='utf-8') as fp:
    t2_content = fp.read()
print("WBS 2.1.11 (Fusion) in tharam-2.html:", "WBS 2.1.11" in t2_content)
print("LMS Progress Tracking in tharam-2.html:", "grade-lms-tracker-banner" in t2_content)

with open('tharam-12.html', 'r', encoding='utf-8') as fp:
    t12_content = fp.read()
print("WBS 12.5.11 (Fusion) in tharam-12.html:", "WBS 12.5.11" in t12_content)
print("CERN Nataraja Dance in tharam-12.html:", "CERN" in t12_content)

with open('tharam-1.html', 'r', encoding='utf-8') as fp:
    t1_content = fp.read()
print("WBS 1.5 in tharam-1.html:", "WBS 1.5" in t1_content)
print("LMS Tracking in tharam-1.html:", "grade-lms-tracker-banner" in t1_content)

if all_ok:
    print("\nALL FILES FULLY SYNCHRONIZED AND VERIFIED!")
else:
    print("\nSOME FILES HAVE ISSUES.")
