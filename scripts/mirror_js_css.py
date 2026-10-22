import os
import shutil

ROOT = r"C:\GitHub\Gurukuladesam"
shutil.copyfile(os.path.join(ROOT, "assets", "js", "purana-reader.js"), os.path.join(ROOT, "docs", "assets", "js", "purana-reader.js"))
shutil.copyfile(os.path.join(ROOT, "assets", "js", "purana-reader.js"), os.path.join(ROOT, "site", "assets", "js", "purana-reader.js"))
shutil.copyfile(os.path.join(ROOT, "assets", "css", "story-reader-layout.css"), os.path.join(ROOT, "docs", "assets", "css", "story-reader-layout.css"))
shutil.copyfile(os.path.join(ROOT, "assets", "css", "story-reader-layout.css"), os.path.join(ROOT, "site", "assets", "css", "story-reader-layout.css"))
print("Mirrored updated js and css to docs/ and site/!")
