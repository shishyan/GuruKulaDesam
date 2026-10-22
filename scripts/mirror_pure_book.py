import shutil
import os

ROOT = r"C:\GitHub\Gurukuladesam"
targets = ["docs", "site"]

for t in targets:
    shutil.copyfile(os.path.join(ROOT, "puranas.html"), os.path.join(ROOT, t, "puranas.html"))
    shutil.copyfile(os.path.join(ROOT, "assets", "js", "purana-reader.js"), os.path.join(ROOT, t, "assets", "js", "purana-reader.js"))
    shutil.copyfile(os.path.join(ROOT, "assets", "css", "pure-book-reader.css"), os.path.join(ROOT, t, "assets", "css", "pure-book-reader.css"))

print("Successfully mirrored pure-book-reader files to docs/ and site/!")
