import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('scripts/build_moola_nool_library.py', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'MOOLA_DATA\["scriptures"\]\["([^"]+)"\]\s*=', text)
print(f'Total scriptures in generator: {len(matches)}')
for m in matches:
    print('  *', m)
