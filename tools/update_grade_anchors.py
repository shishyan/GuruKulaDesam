import re
import glob

files = glob.glob('tharam-*.html') + ['books.html']
print(f"Files found: {len(files)}")

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update version strings
    content = re.sub(r'assets/css/books-reader\.css(?:\?v=[^"\']*)?', 'assets/css/books-reader.css?v=2.2', content)
    content = re.sub(r'assets/js/books-reader\.js(?:\?v=[^"\']*)?', 'assets/js/books-reader.js?v=2.2', content)
    content = re.sub(r'assets/js/moola-nool-data\.js(?:\?v=[^"\']*)?', 'assets/js/moola-nool-data.js?v=2.2', content)
    
    # 2. Ensure id="books" is present before booksShelfTabs
    if 'id="books"' not in content:
        content = content.replace(
            '<!-- THE 7 SACRED BOOKS SHELF (SINGLE TOP-LEVEL CONTAINER FOR THE GRADE) -->',
            '<!-- THE 7 SACRED BOOKS SHELF (SINGLE TOP-LEVEL CONTAINER FOR THE GRADE) -->\n      <div id="books" style="scroll-margin-top: 80px;"></div>'
        )
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated version tags and #books anchors across all files successfully.")
