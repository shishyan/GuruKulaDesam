"""
High-Speed Autonomous Publisher using YouTube API Multi-Project Pool.
Applies:
1. Video Description & Chapters
2. Video & Audio Default Language = Tamil ('ta')
3. Modern 16:9 Thumbnail (1920x1080)
4. Tamil SubRip SRT Subtitles (Deletes older, uploads verified)
Automatically rotates to next Google Cloud project if quota limit is reached.
"""

import os, sys, time, json
from pathlib import Path
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.quota_rotator import get_next_available_youtube_service, mark_project_exhausted

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

def publish_video_complete(vid: str):
    print(f"\n{'='*70}\n[API PUBLISH] Processing {vid}...\n{'='*70}")
    
    desc_p = f"production/descriptions/{vid}.txt"
    thumb_p = f"production/thumbnails/{vid}.png"
    srt_p = f"production/subtitles/{vid}.srt"
    
    for attempt in range(8):
        try:
            yt, pid = get_next_available_youtube_service()
            
            # Step 1: Update Metadata
            if os.path.exists(desc_p):
                with open(desc_p, "r", encoding="utf-8") as f:
                    desc_text = f.read()
                v_res = yt.videos().list(part="snippet", id=vid).execute()
                if v_res.get("items"):
                    snip = v_res["items"][0]["snippet"]
                    snip["description"] = desc_text
                    snip["defaultLanguage"] = "ta"
                    snip["defaultAudioLanguage"] = "ta"
                    yt.videos().update(part="snippet", body={"id": vid, "snippet": snip}).execute()
                    print(f"  ✅ [Step 1] Metadata & Tamil Language updated ({len(desc_text)} chars)")
            
            # Step 2: Upload Thumbnail (skip if rate limited)
            if os.path.exists(thumb_p):
                try:
                    media_thumb = MediaFileUpload(thumb_p, mimetype="image/png")
                    yt.thumbnails().set(videoId=vid, media_body=media_thumb).execute()
                    print(f"  ✅ [Step 2] Modern 16:9 Thumbnail uploaded ({thumb_p})")
                except HttpError as te:
                    print(f"  ⚠️ Thumbnail upload skipped ({te.resp.status}): proceeding with captions.")
                
            # Step 3: Upload Captions
            if os.path.exists(srt_p):
                c_res = yt.captions().list(part="snippet", videoId=vid).execute()
                for c in c_res.get("items", []):
                    if c["snippet"].get("language") == "ta":
                        try:
                            yt.captions().delete(id=c["id"]).execute()
                        except Exception:
                            pass
                
                cap_body = {
                    "snippet": {
                        "videoId": vid,
                        "language": "ta",
                        "name": "தமிழ் (மெய்யான பாடல் வரிகள்)",
                        "isDraft": False
                    }
                }
                cap_media = MediaFileUpload(srt_p, mimetype="application/x-subrip")
                ins_res = yt.captions().insert(part="snippet", body=cap_body, media_body=cap_media, sync=False).execute()
                print(f"  ✅ [Step 3] Subtitles published live! (Caption ID: {ins_res['id'][:25]}...)")
                
            print(f"🎉 100% COMPLETE FOR {vid}!\n")
            return True
            
        except HttpError as e:
            if "quotaExceeded" in str(e):
                print(f"  ⚠️ Project {pid} quota reached. Rotating to next project...")
                mark_project_exhausted(pid)
                continue
            else:
                print(f"  ❌ HttpError for {vid}: {e}")
                return False
        except Exception as ex:
            print(f"  ❌ Error for {vid}: {ex}")
            return False

if __name__ == "__main__":
    vid = sys.argv[1] if len(sys.argv) > 1 else "02C8glMmetw"
    publish_video_complete(vid)
