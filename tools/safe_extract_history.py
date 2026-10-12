import os, sys, json, sqlite3, shutil

sys.stdout.reconfigure(encoding='utf-8')

def extract_history(db_path, out_file):
    if not os.path.exists(db_path):
        return
    temp_db = f"scratch/{os.path.basename(out_file)}.db"
    shutil.copy2(db_path, temp_db)
    conn = sqlite3.connect(temp_db)
    cur = conn.cursor()
    cur.execute("SELECT url, title FROM urls WHERE url LIKE '%suno.com%' ORDER BY last_visit_time DESC LIMIT 200")
    rows = cur.fetchall()
    conn.close()
    
    items = []
    for u, t in rows:
        items.append({"url": u, "title": t})
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(items)} Suno URLs to {out_file}")

os.makedirs("scratch", exist_ok=True)
extract_history("C:/Users/Shishyan/AppData/Local/Microsoft/Edge/User Data/Default/History", "scratch/edge_suno.json")
extract_history("C:/Users/Shishyan/AppData/Local/Google/Chrome/User Data/Default/History", "scratch/chrome_suno.json")
