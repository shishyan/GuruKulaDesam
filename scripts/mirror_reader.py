import shutil
import os

ROOT = r"C:\GitHub\Gurukuladesam"
src = os.path.join(ROOT, "assets", "js", "purana-reader.js")

for dest_dir in [os.path.join(ROOT, "docs", "assets", "js"), os.path.join(ROOT, "site", "assets", "js")]:
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "purana-reader.js")
    shutil.copyfile(src, dest)
    print(f"Copied purana-reader.js to {dest}")
