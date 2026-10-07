for p in ['assets/js/main.js', 'docs/assets/js/main.js', 'site/assets/js/main.js']:
    with open(p, 'r', encoding='utf-8') as f:
        txt = f.read()
    txt = txt.replace("document.getElementsByName('themeChoice')", "document.querySelectorAll('input[name=\"themeChoice\"]')")
    txt = txt.replace("document.getElementsByName('fontChoice')", "document.querySelectorAll('input[name=\"fontChoice\"]')")
    with open(p, 'w', encoding='utf-8') as f:
        f.write(txt)
print("Updated radio queries successfully.")
