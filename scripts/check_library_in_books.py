import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('books.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('data-group="books-library"')
print(text[idx:idx+1800])
