"""
Batch Modern 16:9 Thumbnail Deployer strictly for Owned Guru Kula Desam Tracks (294 total).
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

def deploy_owned_thumbnails(max_videos=50):
    done = load_progress()
    with open("production/owned_guru_kula_videos.json", "r", encoding="utf-8") as f:
        owned_list = json.load(f)["owned"]
        
    candidates = [
        (vid, f"production/thumbnails/{vid}.png", title)
        for vid, title in owned_list
        if vid not in done and os.path.exists(f"production/thumbnails/{vid}.png")
    ]
    
    print(f"\n=======================================================")
    print(f"GURU KULA DESAM — OWNED VIDEO THUMBNAIL DEPLOYMENT")
    print(f"Total Owned Videos: {len(owned_list)}")
    print(f"Already deployed: {len(done & set([v[0] for v in owned_list]))}")
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
                    if "uploadRateLimitExceeded" in str(e):
                        print("  🛑 Thumbnail upload rate limit reached by YouTube. Pausing deployment batch.")
                        return success_count
                    break
            except Exception as ex:
                print(f"  ❌ Error for {vid}: {ex}")
                break
                
        time.sleep(0.5)
        
    elapsed = time.time() - t0
    print(f"\n🎉 Batch finished! Deployed: {success_count}/{len(batch)} thumbnails in {elapsed:.1f}s.")

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    deploy_owned_thumbnails(count)
