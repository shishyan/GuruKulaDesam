import sqlite3
import shutil
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

src = r'C:\Users\Shishyan\AppData\Local\Microsoft\Edge\User Data\Default\History'
dst = r'C:\Users\Shishyan\AppData\Local\Temp\edge_history_docs_only.db'

try:
    shutil.copy2(src, dst)
    conn = sqlite3.connect(dst)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT url, title, datetime(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') as visit_date
        FROM urls 
        WHERE url LIKE '%docs.google.com/document%'
        ORDER BY last_visit_time DESC
    """)
    rows = cursor.fetchall()
    print(f'Total docs.google.com/document found: {len(rows)}')
    for url, title, dt in rows:
        print(f"{dt} | {title} -> {url}")
    conn.close()
    if os.path.exists(dst):
        os.remove(dst)
except Exception as e:
    print('Error:', e)
