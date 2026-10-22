import os
import shutil

ROOT = r"C:\GitHub\Gurukuladesam"
src_html = os.path.join(ROOT, "puranas.html")

# Also mirror all updated html files to docs/ and site/
for fname in os.listdir(ROOT):
    if fname.endswith('.html'):
        src = os.path.join(ROOT, fname)
        for dest_folder in [os.path.join(ROOT, "docs"), os.path.join(ROOT, "site")]:
            dest = os.path.join(dest_folder, fname)
            shutil.copyfile(src, dest)

print("Successfully mirrored all HTML files to docs/ and site/!")
