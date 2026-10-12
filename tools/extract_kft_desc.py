with open('tools/update_kft_description.py', 'r', encoding='utf-8') as f:
    code = f.read()
start = code.find('new_description = """') + len('new_description = """')
end = code.find('"""', start)
desc = code[start:end]
with open('production/descriptions/KFtS403RfbY.txt', 'w', encoding='utf-8') as out:
    out.write(desc)
print('Saved KFtS403RfbY.txt, len:', len(desc))
