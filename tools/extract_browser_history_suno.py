import sqlite3, os, json

def inspect_browser_history(db_path, browser_name):
    if not os.path.exists(db_path):
        print(f"Path does not exist: {db_path}")
        return []
    
    temp_file = f"temp_{browser_name.lower()}.db"
    try:
        with open(db_path, "rb") as f_in, open(temp_file, "wb") as f_out:
            f_out.write(f_in.read())
            
        conn = sqlite3.connect(temp_file)
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM urls")
        total = cur.fetchone()[0]
        print(f"[{browser_name}] Total History URLs: {total}")
        
        cur.execute("SELECT url, title, visit_count, last_visit_time FROM urls WHERE url LIKE '%suno.com%'")
        rows = cur.fetchall()
        print(f"[{browser_name}] Suno URLs Found: {len(rows)}")
        
        results = []
        for url, title, vc, lvt in rows:
            results.append({
                "browser": browser_name,
                "url": url,
                "title": title,
                "visit_count": vc,
                "last_visit_time": lvt
            })
        conn.close()
        return results
    except Exception as e:
        print(f"Error reading {browser_name}: {e}")
        return []
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == "__main__":
    edge_path = os.path.expanduser("~") + r"\AppData\Local\Microsoft\Edge\User Data\Default\History"
    chrome_path = os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data\Default\History"
    
    edge_results = inspect_browser_history(edge_path, "Edge")
    chrome_results = inspect_browser_history(chrome_path, "Chrome")
    
    all_combined = edge_results + chrome_results
    songs = [r for r in all_combined if "/song/" in r["url"]]
    print(f"\nTotal Suno records across both: {len(all_combined)}")
    print(f"Total /song/ records: {len(songs)}")
    
    # Save all unique song URLs
    unique_songs = {}
    for s in songs:
        url = s["url"]
        cid = url.split("/song/")[-1].split("?")[0].strip()
        if cid and cid not in unique_songs:
            unique_songs[cid] = s
            
    print(f"Unique Song IDs in History: {len(unique_songs)}")
    with open("production/metadata/all_browser_history_suno.json", "w", encoding="utf-8") as f:
        json.dump(list(unique_songs.values()), f, ensure_ascii=False, indent=2)
