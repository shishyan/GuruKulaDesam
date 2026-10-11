import sys, os, json, pathlib, time, re
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = pathlib.Path(__file__).resolve().parent.parent
CRED_FILE = ROOT / 'data' / 'credentials' / 'token.json'
PROGRESS_FILE = ROOT / 'production' / 'channel_sync_progress.json'
SUB_DIR = ROOT / 'production' / 'subtitles'

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

creds = Credentials.from_authorized_user_file(str(CRED_FILE))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

# Load catalog, overrides, and channel videos
cat = json.load(open(ROOT / 'assets/data/catalog.json', encoding='utf-8'))
ovr = json.load(open(ROOT / 'production/youtube_lyrics_overrides.json', encoding='utf-8'))
works = ovr.get('_works', {})
vids_file = ROOT / 'production/youtube_backup/videos.json'
channel_vids = json.load(open(vids_file, encoding='utf-8')) if vids_file.exists() else []

# Load or init progress
if PROGRESS_FILE.exists():
    try:
        progress = json.load(open(PROGRESS_FILE, encoding='utf-8'))
    except Exception:
        progress = {}
else:
    progress = {}

def save_progress():
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

# Build catalog lookup by ID and Title
cat_by_id = {}
cat_by_clean_title = {}
for vault, songs in cat.items():
    if not isinstance(songs, list): continue
    for s in songs:
        sid = s.get('id')
        if sid:
            cat_by_id[sid] = (vault, s)
        t = re.sub(r'\[.*?\]', '', s.get('title', '')).strip()
        if t:
            cat_by_clean_title[t] = (vault, s)

print(f"Total videos in channel backup: {len(channel_vids)}", flush=True)

success_count = 0
quota_exceeded = False

for v in channel_vids:
    vid = v['id']
    cur_prog = progress.get(vid, {})
    if cur_prog.get('done'):
        continue

    title = v['snippet']['title']
    old_desc = v['snippet'].get('description', '')

    # 1. Resolve Lyrics & Meaning
    lyrics = None
    meaning = None
    attribution = None

    if vid in ovr:
        ref = ovr[vid].get('ref')
        if ref and ref in works:
            lyrics = works[ref].get('lyrics')
            meaning = works[ref].get('meaning')
            attribution = works[ref].get('title')

    if not lyrics and vid in cat_by_id:
        s = cat_by_id[vid][1]
        l = (s.get('lyrics') or '').strip()
        if len(l) > 15:
            lyrics = l
            meaning = s.get('meaning')

    if not lyrics:
        # Title matching fallback
        clean_t = re.sub(r'\[.*?\]', '', title).strip()
        for ct, (cvault, cs) in cat_by_clean_title.items():
            if ct in clean_t or clean_t in ct:
                l = (cs.get('lyrics') or '').strip()
                if len(l) > 15:
                    lyrics = l
                    meaning = cs.get('meaning')
                    break

    # 2. Check Subtitle File
    srt_file = SUB_DIR / f"{vid}.srt"
    if not srt_file.exists():
        if vid in ovr and ovr[vid].get('ref'):
            alt = SUB_DIR / f"{ovr[vid]['ref']}.srt"
            if alt.exists():
                srt_file = alt

    # If no subtitles exist but we have lyrics, generate one on the fly
    if not srt_file.exists() and lyrics:
        srt_file = SUB_DIR / f"{vid}.srt"
        from generate_all_catalog_subtitles import generate_srt
        content = generate_srt(lyrics)
        if content:
            srt_file.write_text(content, encoding='utf-8')

    # If still no lyrics, mark skip and continue
    if not lyrics:
        progress[vid] = {'done': True, 'skipped': True, 'reason': 'No lyrics found in catalog/overrides'}
        save_progress()
        continue

    print(f"\n--- Processing {vid}: {title[:40]}... ---", flush=True)

    # 3. Update Video Description & Tags (including yt:cc=on)
    try:
        r = yt.videos().list(part='snippet', id=vid).execute()
        if not r.get('items'):
            print(f"Video {vid} not found on YouTube. Skipping.", flush=True)
            progress[vid] = {'done': True, 'error': 'not_found'}
            save_progress()
            continue

        item = r['items'][0]
        snip = item['snippet']
        tags = snip.get('tags', [])
        tag_needed = 'yt:cc=on' not in tags
        if tag_needed:
            tags.append('yt:cc=on')

        # Check if description already has full lyrics
        has_lyrics_in_desc = ('பாடல் வரிகள்' in snip['description'] and len(snip['description']) > 400)

        if not has_lyrics_in_desc or tag_needed:
            head = snip['description'].split('பாடல் வரிகள்')[0].strip()
            attr_block = f"\n═════════════════════════════════════════\n{attribution}\n═════════════════════════════════════════\n" if attribution else ""
            meaning_block = f"\n\nபொருள் விளக்கம் (Spiritual Meaning):\n{meaning.strip()}\n" if meaning else ""

            new_desc = f"""{head}
{attr_block}
பாடல் வரிகள் (Tamil Lyrics):
{lyrics.strip()}
{meaning_block}
— குரு குல தேசம் | Guru Kula Desam
https://gurukuladesam.com"""

            body = {
                'id': vid,
                'snippet': {
                    'title': snip['title'],
                    'categoryId': snip.get('categoryId', '10'),
                    'description': new_desc[:4900],
                    'tags': tags,
                    'defaultLanguage': 'ta',
                    'defaultAudioLanguage': 'ta'
                }
            }
            yt.videos().update(part='snippet', body=body).execute()
            print(f" -> SUCCESS: Description & yt:cc=on updated for {vid}", flush=True)
        else:
            print(f" -> Info: Description and tags already up to date.", flush=True)

        # 4. Upload Captions Track if available
        if srt_file.exists():
            existing_cap_id = None
            try:
                cap_list = yt.captions().list(part='snippet', videoId=vid).execute()
                for c in cap_list.get('items', []):
                    snip = c.get('snippet', {})
                    if snip.get('language') == 'ta' and snip.get('trackKind') != 'asr':
                        existing_cap_id = c['id']
                        break
            except Exception:
                existing_cap_id = None

            media = MediaFileUpload(str(srt_file), mimetype='application/x-subrip', resumable=True)
            if existing_cap_id:
                # Update existing track with newly generated/corrected srt
                cap_body = {
                    'id': existing_cap_id,
                    'snippet': {
                        'isDraft': False
                    }
                }
                c_res = yt.captions().update(part='snippet', body=cap_body, media_body=media).execute()
                print(f" -> SUCCESS: Updated Tamil caption track with verified subtitles (ID: {c_res.get('id')})", flush=True)
            else:
                # Insert fresh caption track
                cap_body = {
                    'snippet': {
                        'videoId': vid,
                        'language': 'ta',
                        'name': 'தமிழ் பாடல் வரிகள் (Tamil Lyrics)',
                        'isDraft': False
                    }
                }
                c_res = yt.captions().insert(part='snippet', body=cap_body, media_body=media).execute()
                print(f" -> SUCCESS: Uploaded fresh Tamil caption track (ID: {c_res.get('id')})", flush=True)

        progress[vid] = {'done': True, 'timestamp': time.time()}
        save_progress()
        success_count += 1
        time.sleep(0.5)

    except Exception as e:
        err_str = str(e)
        print(f" -> ERROR on {vid}: {err_str}", flush=True)
        if 'quotaexceeded' in err_str.lower():
            quota_exceeded = True
            print("Quota limit reached on current project. Halting loop cleanly.", flush=True)
            break
        progress[vid] = {'done': False, 'error': err_str}
        save_progress()

print(f"\nBatch sync completed: {success_count} videos processed successfully.", flush=True)
if quota_exceeded:
    print("Execution paused due to quota limit. Progress saved.")

