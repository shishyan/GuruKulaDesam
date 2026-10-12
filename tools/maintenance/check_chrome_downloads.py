import sqlite3
import shutil
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

src = r'C:\Users\Shishyan\AppData\Local\Google\Chrome\User Data\Default\History'
dst = r'C:\Users\Shishyan\AppData\Local\Temp\chrome_history_downloads.db'

try:
    shutil.copy2(src, dst)
    conn = sqlite3.connect(dst)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT target_path, tab_url, datetime(start_time/1000000-11644473600, 'unixepoch', 'localtime') as dl_date
        FROM downloads 
        ORDER BY start_time DESC 
        LIMIT 50
    """)
    rows = cursor.fetchall()
    print(f'Total recent downloads in Chrome: {len(rows)}')
    for path, url, dt in rows:
        print(f"{dt} | {os.path.basename(path)} -> {url}")
    conn.close()
    if os.path.exists(dst):
        os.remove(dst)
except Exception as e:
    print('Error:', e)
