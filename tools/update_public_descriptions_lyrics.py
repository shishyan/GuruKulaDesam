# -*- coding: utf-8 -*-
"""
tools/update_public_descriptions_lyrics.py

Autonomous Description Updater:
Appends authentic Suno / Sung Song Lyrics to all 239 public YouTube video descriptions.

Rules:
1. DOES NOT override or delete existing descriptions, commentary, or chapters.
2. Checks if description already has '🎵 முழுமையான பாடல் வரிகள்' - skips if already present.
3. Appends lyrics at the bottom under:
   -------------------------------------------------
   🎵 முழுமையான பாடல் வரிகள் (Full Song Lyrics):
   -------------------------------------------------
4. Strictly respects YouTube 5,000 char limit (truncates safely to 4,950 chars).
5. Rotates across Google Cloud projects in quota pool to prevent exhaustion.
"""

import os, sys, json, time, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.quota_rotator import get_next_available_youtube_service, mark_project_exhausted
from googleapiclient.errors import HttpError

PROGRESS_FILE = ROOT / "production" / "metadata" / "descriptions_lyrics_progress.json"

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
        json.dump(list(done_set), f, ensure_ascii=False, indent=2)

def extract_lyrics(vid: str):
    # 1. From Suno Lyrics file if mapped
    # 2. From Subtitle SRT (sung song-flow)
    srt_p = ROOT / "production" / "subtitles" / f"{vid}.srt"
    if srt_p.exists():
        with open(srt_p, "r", encoding="utf-8") as f:
            content = f.read()
        blocks = content.strip().split("\n\n")
        lines = []
        for b in blocks:
            parts = b.strip().split("\n")
            if len(parts) >= 3:
                txt = "\n".join(parts[2:]).strip()
                if "செவ்வியல் திரையிசை" in txt or "Classical Devotional Song" in txt:
                    continue
                if txt and (not lines or lines[-1] != txt):
                    lines.append(txt)
        if lines:
            return "\n\n".join(lines)
    
    # 3. Fallback from metadata registry
    meta_p = ROOT / "production" / "metadata" / "all_songs_lyrics_and_meanings.json"
    if meta_p.exists():
        with open(meta_p, "r", encoding="utf-8") as f:
            data = json.load(f)
        if vid in data and data[vid].get("tamil_lyrics"):
            return data[vid]["tamil_lyrics"].strip()
            
    return None

def run_update(batch_size=50):
    done = load_progress()
    
    with open(ROOT / "production" / "metadata" / "all_owned_videos_status.json", "r", encoding="utf-8") as f:
        statuses = json.load(f)
        
    public_vids = [(vid, d["title"]) for vid, d in statuses.items() if d.get("status") == "public" and vid not in done]
    
    print("=" * 80)
    print("GURU KULA DESAM — SUNO LYRICS DESCRIPTION APPENDER")
    print(f"Total Public Videos: {len([v for v, d in statuses.items() if d.get('status') == 'public'])}")
    print(f"Already updated: {len(done)}")
    print(f"Remaining to process: {len(public_vids)}")
    print("=" * 80)
    
    if not public_vids:
        print("All public video descriptions already updated!")
        return

    processed_this_run = 0
    yt, pid = get_next_available_youtube_service()

    for vid, title in public_vids:
        if processed_this_run >= batch_size:
            print(f"Batch size {batch_size} reached. Pausing for next invocation.")
            break
            
        print(f"\nProcessing [{processed_this_run+1}/{min(batch_size, len(public_vids))}] {vid} - {title[:40]}...")
        
        lyrics = extract_lyrics(vid)
        if not lyrics:
            print(f"  ⚠️ No lyrics resolved for {vid}. Skipping.")
            done.add(vid)
            save_progress(done)
            continue
            
        # Fetch current live snippet from YouTube
        for attempt in range(5):
            try:
                res = yt.videos().list(part="snippet", id=vid).execute()
                if not res.get("items"):
                    print(f"  ❌ Video {vid} not found on YouTube.")
                    done.add(vid)
                    save_progress(done)
                    break
                    
                snippet = res["items"][0]["snippet"]
                cur_desc = snippet.get("description", "").strip()
                
                # Check if lyrics already appended
                if "முழுமையான பாடல் வரிகள்" in cur_desc or "Full Song Lyrics" in cur_desc:
                    print(f"  ℹ️ Lyrics already appended in YouTube description for {vid}.")
                    done.add(vid)
                    save_progress(done)
                    break
                    
                # Format appended section
                lyrics_section = f"\n\n═════════════════════════════════════════════════════════════════\n🎵 முழுமையான பாடல் வரிகள் (Full Song Lyrics):\n═════════════════════════════════════════════════════════════════\n{lyrics}\n"
                
                # Check character limit (YouTube allows up to 5,000 characters)
                if len(cur_desc) + len(lyrics_section) > 4850:
                    allowed_lyrics_len = 4850 - len(cur_desc) - 150
                    if allowed_lyrics_len > 200:
                        lyrics_section = f"\n\n═════════════════════════════════════════════════════════════════\n🎵 முழுமையான பாடல் வரிகள் (Full Song Lyrics):\n═════════════════════════════════════════════════════════════════\n{lyrics[:allowed_lyrics_len]}\n..."
                    else:
                        print(f"  ⚠️ Existing description too long ({len(cur_desc)} chars). Cannot append without exceeding limit.")
                        done.add(vid)
                        save_progress(done)
                        break
                        
                new_desc = cur_desc + lyrics_section
                snippet["description"] = new_desc
                snippet["defaultLanguage"] = "ta"
                snippet["defaultAudioLanguage"] = "ta"
                
                yt.videos().update(
                    part="snippet",
                    body={"id": vid, "snippet": snippet}
                ).execute()
                
                print(f"  ✅ [SUCCESS] Appended song lyrics to description! ({len(cur_desc)} -> {len(new_desc)} chars)")
                
                # Also save locally
                loc_desc_p = ROOT / "production" / "descriptions" / f"{vid}.txt"
                loc_desc_p.parent.mkdir(parents=True, exist_ok=True)
                loc_desc_p.write_text(new_desc, encoding="utf-8")
                
                done.add(vid)
                save_progress(done)
                processed_this_run += 1
                time.sleep(1.0)
                break
                
            except HttpError as e:
                if e.resp.status in [403, 429]:
                    print(f"  ⚠️ Quota limit or rate limit on project {pid} ({e.resp.status}). Rotating to next project...")
                    mark_project_exhausted(pid)
                    yt, pid = get_next_available_youtube_service()
                    time.sleep(2)
                else:
                    print(f"  ❌ API HttpError for {vid}: {e}")
                    done.add(vid)
                    save_progress(done)
                    break
            except Exception as e:
                print(f"  ❌ Unexpected error for {vid}: {e}")
                break

    print(f"\nCompleted run! Total public videos with updated descriptions now: {len(done)}")

if __name__ == "__main__":
    b_size = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    run_update(batch_size=b_size)
