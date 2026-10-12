import sqlite3
import shutil
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

src = r'C:\Users\Shishyan\AppData\Local\Google\Chrome\User Data\Default\History'
dst = r'C:\Users\Shishyan\AppData\Local\Temp\chrome_history_drive.db'

try:
    shutil.copy2(src, dst)
    conn = sqlite3.connect(dst)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT url, title, datetime(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') as visit_date
        FROM urls 
        WHERE url LIKE '%drive.google.com%'
           OR url LIKE '%docs.google.com%'
           OR url LIKE '%sites.google.com%'
        ORDER BY last_visit_time DESC 
        LIMIT 100
    """)
    rows = cursor.fetchall()
    print(f'Total Drive/Docs/Sites in Chrome: {len(rows)}')
    for url, title, dt in rows:
        print(f"{dt} | {title} -> {url}")
    conn.close()
    if os.path.exists(dst):
        os.remove(dst)
except Exception as e:
    print('Error:', e)
