import os
import re

ROOT = r'c:\GitHub\Gurukuladesam'

# 1. Update books.html
books_path = os.path.join(ROOT, 'books.html')
with open(books_path, 'r', encoding='utf-8') as f:
    bcontent = f.read()

bcontent = bcontent.replace(
    'நன்னெறி, நல்லறம், நல்வழி, நற்துணை, நற்சிந்தனை, நற்சொல், நற்செயல் - தரம் 1 முதல் 12 வரை.',
    'நன்னெறி, நல்லறம், நற்பண்பு, நற்துணை, நற்சிந்தனை, நற்சொல், நற்செயல் — தரம் 1 முதல் 12 வரை.'
)
bcontent = bcontent.replace(
    'நன்னெறி, நல்லறம், நல்வழி, நற்துணை, நற்சிந்தனை, நற்சொல், நற்செயல் ஆகிய 7 நூல்களும்',
    'நன்னெறி, நல்லறம், நற்பண்பு, நற்துணை, நற்சிந்தனை, நற்சொல், நற்செயல் ஆகிய ஆசிரம நூல்களும்'
)

with open(books_path, 'w', encoding='utf-8') as f:
    f.write(bcontent)
print("Updated books.html")

# 2. Update syllabus.html
syl_path = os.path.join(ROOT, 'syllabus.html')
with open(syl_path, 'r', encoding='utf-8') as f:
    scontent = f.read()

scontent = scontent.replace('நன்னெறி, நல்லறம், நல்வழி, நற்துணை', 'நன்னெறி, நல்லறம், நற்பண்பு, நற்துணை')
scontent = scontent.replace('நன்னெறி • நல்லறம் • நல்வழி • நற்துணை', 'நன்னெறி • நல்லறம் • நற்பண்பு • நற்துணை')
scontent = scontent.replace('"நன்னெறி நல்லறம் நல்வழி நற்துணை', '"நன்னெறி நல்லறம் நற்பண்பு நற்துணை')
scontent = scontent.replace('<!-- Book 3: நல்வழி -->', '<!-- Book 3: நற்பண்பு -->')
scontent = scontent.replace('நல்வழி (The Noble Path)', 'நற்பண்பு (The Noble Virtues & Character)')
scontent = scontent.replace('ஒழுக்கம், வாய்மை, நடுவுநிலைமை பயிற்றுவிக்கும் நல்வழிச் செய்யுள்.', 'ஒழுக்கம், வாய்மை, நற்பண்பு பயிற்றுவிக்கும் அறச் செய்யுள்.')

with open(syl_path, 'w', encoding='utf-8') as f:
    f.write(scontent)
print("Updated syllabus.html")
