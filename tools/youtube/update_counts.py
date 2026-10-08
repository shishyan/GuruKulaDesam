import glob, re

files = glob.glob('docs/*.html')
updated = 0
for f in files:
    content = open(f, encoding='utf-8').read()
    new_content = content.replace('இறை இசை விருந்து (580)', 'இறை இசை விருந்து (600+)')
    if f.endswith('youtube.html'):
        new_content = new_content.replace('580 இசைப் படைப்புகள்', '600+ இசைப் படைப்புகள்')
        new_content = new_content.replace('580 இசைத் திரைப்படங்கள்', '600+ இசைத் திரைப்படங்கள்')
        new_content = new_content.replace('580 காணொளிகளில் சங்கமிக்கும்', '600+ காணொளிகளில் சங்கமிக்கும்')
        new_content = new_content.replace('580 Sacred Musical Productions', '600+ Sacred Musical Productions & Films')
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as out:
            out.write(new_content)
        updated += 1

print(f"Updated counts in {updated} HTML files in docs/")

