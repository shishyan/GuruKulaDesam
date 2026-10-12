import sys

with open('assets/js/main.js', 'r', encoding='utf-8') as f:
    text = f.read()

i = 0
n = len(text)
line = 1
stack = []

while i < n:
    c = text[i]
    if c == '\n':
        line += 1
        i += 1
        continue
    if c == '/' and i + 1 < n and text[i+1] == '/':
        while i < n and text[i] != '\n':
            i += 1
        continue
    if c == '/' and i + 1 < n and text[i+1] == '*':
        i += 2
        while i + 1 < n and not (text[i] == '*' and text[i+1] == '/'):
            if text[i] == '\n': line += 1
            i += 1
        i += 2
        continue
    if c == "'" or c == '"':
        q = c
        i += 1
        while i < n and text[i] != q:
            if text[i] == '\\':
                i += 2
                continue
            if text[i] == '\n': line += 1
            i += 1
        i += 1
        continue
    if c == '`':
        i += 1
        while i < n and text[i] != '`':
            if text[i] == '\\':
                i += 2
                continue
            if text[i] == '$' and i + 1 < n and text[i+1] == '{':
                stack.append(('tpl', line))
                i += 2
                break
            if text[i] == '\n': line += 1
            i += 1
        else:
            if i < n and text[i] == '`':
                i += 1
        continue
    if c == '{':
        stack.append(('{', line))
    elif c == '}':
        if stack:
            top = stack.pop()
            if top[0] == 'tpl':
                # back in template string
                i += 1
                while i < n and text[i] != '`':
                    if text[i] == '\\':
                        i += 2
                        continue
                    if text[i] == '$' and i + 1 < n and text[i+1] == '{':
                        stack.append(('tpl', line))
                        i += 2
                        break
                    if text[i] == '\n': line += 1
                    i += 1
                else:
                    if i < n and text[i] == '`':
                        i += 1
                continue
        else:
            print(f"Extra }} at line {line}")
    i += 1

print(f"Unclosed: {len(stack)}")
for item in stack:
    print(f"  {item[0]} at line {item[1]}")

