import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

txt = open('assets/js/thirukkural-tree-data.js', encoding='utf-8').read()

athikarams = {}
# Match athikaram entries
for block in re.split(r'\{\s*"num":', txt)[1:]:
    m_num = re.search(r'^\s*(\d+)', block)
    m_name = re.search(r'"name":\s*"([^"]+)"', block)
    m_translit = re.search(r'"translit":\s*"([^"]+)"', block)
    m_trans = re.search(r'"translation":\s*"([^"]+)"', block)
    if m_num and m_name:
        num = int(m_num.group(1))
        athikarams[num] = {
            'number': num,
            'name': m_name.group(1),
            'translit': m_translit.group(1) if m_translit else '',
            'translation': m_trans.group(1) if m_trans else ''
        }

print(f"Total Athikarams extracted: {len(athikarams)}")
with open('production/master_133_athikarams.json', 'w', encoding='utf-8') as f:
    json.dump(athikarams, f, indent=2, ensure_ascii=False)

for c in [1, 2, 5, 6, 8, 16, 25, 26, 27, 28, 29, 30, 133]:
    if c in athikarams:
        a = athikarams[c]
        print(f"Chap {c:03d}: {a['name']} ({a['translit']}) - {a['translation']}")
