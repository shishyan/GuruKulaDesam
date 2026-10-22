import os

puranas_dir = r"C:\GitHub\Gurukuladesam\data\puranas"
for f in os.listdir(puranas_dir):
    if f.endswith('.json'):
        fp = os.path.join(puranas_dir, f)
        size = os.path.getsize(fp)
        print(f"{f:35} {size/1024:.1f} KB")
