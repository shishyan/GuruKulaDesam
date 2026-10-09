import re, glob, sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. tharam-1.html to tharam-12.html: remove admissions link in grade-switch-strip
for f in sorted(glob.glob('tharam-*.html')):
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    # Match any <a href="admissions.html...</a>
    c_new = re.sub(r'<a\s+href="admissions\.html\?grade=\d+"[^>]*>.*?</a>\s*', '', c, flags=re.DOTALL)
    if c_new != c:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(c_new)
        print(f"Removed admissions button from {f}")

# 2. higher-studies.html: remove admissions link
hs_path = 'higher-studies.html'
with open(hs_path, 'r', encoding='utf-8') as fp:
    hs = fp.read()
hs_new = re.sub(r'<a\s+href="admissions\.html"[^>]*class="degree-filter-btn"[^>]*>.*?</a>\s*', '', hs, flags=re.DOTALL)
if hs_new != hs:
    with open(hs_path, 'w', encoding='utf-8') as fp:
        fp.write(hs_new)
    print("Removed admissions button from higher-studies.html")

# 3. school.html: remove admissions link from quick jump & context pill
sc_path = 'school.html'
with open(sc_path, 'r', encoding='utf-8') as fp:
    sc = fp.read()
sc_new = re.sub(r'<a\s+href="admissions\.html"[^>]*>🎒\s*புதிய மாணவர் சேர்க்கை &rarr;</a>\s*', '', sc)
sc_new = re.sub(r'<a\s+href="admissions\.html"[^>]*class="context-tab-pill"[^>]*>.*?</a>\s*', '', sc_new, flags=re.DOTALL)
if sc_new != sc:
    with open(sc_path, 'w', encoding='utf-8') as fp:
        fp.write(sc_new)
    print("Removed admissions buttons from school.html")

# 4. classes.html: remove admissions button
cl_path = 'classes.html'
with open(cl_path, 'r', encoding='utf-8') as fp:
    cl = fp.read()
cl_new = re.sub(r'<a\s+href="admissions\.html"[^>]*class="grade-pill-btn"[^>]*>.*?</a>\s*', '', cl, flags=re.DOTALL)
if cl_new != cl:
    with open(cl_path, 'w', encoding='utf-8') as fp:
        fp.write(cl_new)
    print("Removed admissions button from classes.html")

print("All admissions buttons stripped successfully.")
