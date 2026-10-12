import sqlite3
import shutil
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

src = r'C:\Users\Shishyan\AppData\Local\Google\Chrome\User Data\Default\History'
dst = r'C:\Users\Shishyan\AppData\Local\Temp\chrome_history_search.db'

try:
    shutil.copy2(src, dst)
    conn = sqlite3.connect(dst)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT url, title, datetime(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') as visit_date
        FROM urls 
        WHERE lower(title) LIKE '%saiva%' 
           OR lower(title) LIKE '%concept%'
           OR lower(title) LIKE '%gurukula%'
           OR lower(title) LIKE '%sites.google%'
           OR lower(url) LIKE '%sites.google.com%'
           OR title LIKE '%சைவ%'
           OR title LIKE '%குரு குல%'
           OR title LIKE '%கோட்பாடு%'
           OR title LIKE '%தத்துவம்%'
        ORDER BY last_visit_time DESC 
        LIMIT 100
    """)
    rows = cursor.fetchall()
    print(f'Total matching entries in Chrome history: {len(rows)}')
    for url, title, dt in rows:
        print(f"{dt} | {title} -> {url}")
    conn.close()
    if os.path.exists(dst):
        os.remove(dst)
except Exception as e:
    print('Error:', e)
