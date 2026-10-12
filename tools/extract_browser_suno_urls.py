import os, sys, json, sqlite3, shutil

def search_history(db_path, out_name):
    if not os.path.exists(db_path):
        print(f"Not found: {db_path}")
        return
    temp_db = f"scratch/{out_name}.db"
    try:
        shutil.copy2(db_path, temp_db)
        conn = sqlite3.connect(temp_db)
        cur = conn.cursor()
        cur.execute("SELECT url, title, visit_count, last_visit_time FROM urls WHERE url LIKE '%suno.com%' ORDER BY last_visit_time DESC LIMIT 100")
        rows = cur.fetchall()
        print(f"=== {out_name} Suno URLs ({len(rows)}) ===")
        for r in rows[:20]:
            print(f"  {r[0]} | {r[1]}")
        with open(f"scratch/{out_name}_suno_urls.json", "w", encoding="utf-8") as f:
            json.dump([{"url": r[0], "title": r[1]} for r in rows], f, ensure_ascii=False, indent=2)
        conn.close()
    except Exception as e:
        print(f"Error reading {db_path}: {e}")

os.makedirs("scratch", exist_ok=True)
search_history("C:/Users/Shishyan/AppData/Local/Microsoft/Edge/User Data/Default/History", "edge_history")
search_history("C:/Users/Shishyan/AppData/Local/Google/Chrome/User Data/Default/History", "chrome_history")
search_history("C:/Users/Shishyan/AppData/Local/Google/Chrome/User Data/Profile 1/History", "chrome_p1_history")
search_history("C:/Users/Shishyan/AppData/Local/Microsoft/Edge/User Data/Profile 1/History", "edge_p1_history")
