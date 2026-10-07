import shutil
import hashlib
import os

files_to_copy = ['master_all_598_songs_catalog.json', 'master_all_598_songs_catalog.csv']
target_dirs = ['assets/data', 'site/assets/data', 'docs/assets/data']

for d in target_dirs:
    os.makedirs(d, exist_ok=True)
    for f in files_to_copy:
        shutil.copy2(f, os.path.join(d, f))
        print(f"Copied {f} -> {d}/")

def get_hash(filepath):
    with open(filepath, 'rb') as fp:
        return hashlib.sha256(fp.read()).hexdigest()

print("\n--- Integrity Verification ---")
for f in files_to_copy:
    hashes = [get_hash(os.path.join(d, f)) for d in target_dirs]
    assert all(h == hashes[0] for h in hashes), f"Hash mismatch in {f}"
    print(f"{f}: 100% PARITY across all mirrors (SHA256: {hashes[0][:12]}...)")

