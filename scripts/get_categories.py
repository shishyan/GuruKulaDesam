import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('scripts/build_moola_nool_library.py', 'r', encoding='utf-8') as f:
    text = f.read()

categories_match = re.search(r'"categories":\s*\[(.*?)\]', text, re.DOTALL)
if categories_match:
    print('Categories:\n', categories_match.group(0))
