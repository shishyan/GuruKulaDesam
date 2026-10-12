"""
Batch Modern 16:9 Thumbnail Deployer across Guru Kula Desam Catalog.
Deploys pre-rendered 1920x1080 thumbnails from production/thumbnails/{vid}.png
using the multi-project YouTube API quota pool (80,000 units/day).
Tracks progress in production/thumbnails_deploy_progress.json.
"""

import os, sys, time, json
from pathlib import Path
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.quota_rotator import get_next_available_youtube_service, mark_project_exhausted

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

PROGRESS_FILE = Path("production/thumbnails_deploy_progress.json")

def load_progress():
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            pass
    return set()

def save_progress(done_set):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(done_set), f, indent=2)

def deploy_all_thumbnails(max_videos=100):
    done = load_progress()
    with open("live_youtube_metadata.json", "r", encoding="utf-8") as f:
        meta = json.load(f)
        
    candidates = [
        (vid, f"production/thumbnails/{vid}.png", item.get("title", ""))
        for vid, item in meta.items()
        if vid not in done and os.path.exists(f"production/thumbnails/{vid}.png")
    ]
    
    print(f"\n=======================================================")
    print(f"GURU KULA DESAM — MODERN THUMBNAIL BATCH DEPLOYMENT")
    print(f"Total in Catalog: {len(meta)}")
    print(f"Already deployed in this run: {len(done)}")
    print(f"Pending deployment candidates: {len(candidates)}")
    print(f"Targeting up to: {max_videos} in this batch")
    print(f"=======================================================\n")
    
    batch = candidates[:max_videos]
    success_count = 0
    t0 = time.time()
    
    for idx, (vid, thumb_path, title) in enumerate(batch, 1):
        for attempt in range(8):
            try:
                yt, pid = get_next_available_youtube_service()
                media = MediaFileUpload(thumb_path, mimetype="image/png")
                yt.thumbnails().set(videoId=vid, media_body=media).execute()
                done.add(vid)
                success_count += 1
                save_progress(done)
                print(f"  [{idx}/{len(batch)}] ✅ Uploaded {vid} ({title[:40]}) [Project: {pid}]")
                break
            except HttpError as e:
                if "quotaExceeded" in str(e):
                    print(f"  ⚠️ Project {pid} quota reached. Rotating to next project...")
                    mark_project_exhausted(pid)
                    continue
                else:
                    print(f"  ❌ HttpError for {vid}: {e}")
                    done.add(vid) # Skip on non-recoverable error
                    save_progress(done)
                    break
            except Exception as ex:
                print(f"  ❌ Error for {vid}: {ex}")
                break
                
        time.sleep(0.5)
        
    elapsed = time.time() - t0
    print(f"\n🎉 Batch finished! Deployed: {success_count}/{len(batch)} thumbnails in {elapsed:.1f}s.")

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    deploy_all_thumbnails(count)
