import re, html

text = open('C:/Users/Shishyan/.gemini/antigravity/brain/80e87c4b-c142-450e-bc23-6a6b12ae1e34/.system_generated/steps/2440/content.md', encoding='utf-8').read()

sections = re.findall(r'Section \d+:[^<"\n]+', text)
for s in sorted(set(sections)):
    print(s)

questions = re.findall(r'(?:<legend[^>]*>|<label[^>]*>)(.*?)(?:</legend>|</label>)', text, re.DOTALL)
clean_q = []
for q in questions:
    c = html.unescape(re.sub(r'<[^>]+>', '', q)).strip()
    if len(c) > 5 and not c.startswith('function') and 'Google' not in c and c not in clean_q:
        clean_q.append(c)

print("\n--- Questions / Fields ---")
for q in clean_q:
    print("-", q)

