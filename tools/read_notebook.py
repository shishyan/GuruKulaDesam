import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('c:/GitHub/Guru-Kula-Desam.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}")
for i, cell in enumerate(nb['cells']):
    ctype = cell['cell_type']
    source = ''.join(cell['source'])
    print(f"\n==========================================")
    print(f"CELL {i} ({ctype})")
    print(f"==========================================")
    print(source[:500])
