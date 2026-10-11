import sys, os, json, pathlib, time
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROGRESS_FILE = ROOT / "production" / "standardize_tamil_audio_cc_progress.json"
AUDIT_FILE = ROOT / "production" / "live_videos_language_audit.json"

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def get_yt_client(token_path):
    p = ROOT / token_path
    if not p.exists():
        return None
    creds = Credentials.from_authorized_user_file(str(p))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build('youtube', 'v3', credentials=creds, cache_discovery=False)

def probe_client(yt):
    try:
        yt.videos().list(part='id', id='4s48KQnjSyQ').execute()
        return True
    except Exception:
        return False

def main():
    if not AUDIT_FILE.exists():
        print(f"Error: {AUDIT_FILE} not found!")
        return

    data = json.load(open(AUDIT_FILE, encoding='utf-8'))
    targets = [d for d in data if d.get('defaultAudioLanguage') != 'ta' or d.get('defaultLanguage') != 'ta']
    print(f"Loaded {len(targets)} videos needing Tamil language standardization.")

    progress = {}
    if PROGRESS_FILE.exists():
        try:
            progress = json.load(open(PROGRESS_FILE, encoding='utf-8'))
        except Exception:
            progress = {}

    tokens = [
        'data/credentials/token.json',
        'data/credentials/token_backup_guru-kula-desam.json'
    ]

    active_idx = 0
    yt = None
    for idx, t in enumerate(tokens):
        client = get_yt_client(t)
        if client and probe_client(client):
            yt = client
            active_idx = idx
            print(f"Using active credential: {t}")
            break

    if not yt:
        print("ERROR: All API credentials exhausted quota or invalid.")
        return

    success_count = 0
    skipped_count = 0
    deleted_en_cc_count = 0

    for idx, row in enumerate(targets, 1):
        vid = row['id']
        title = row['title']

        if progress.get(vid, {}).get('done'):
            skipped_count += 1
            continue

        print(f"\n[{idx}/{len(targets)}] Standardizing {vid}: {title[:40]}...", flush=True)

        success = False
        while not success and active_idx < len(tokens):
            try:
                # 1. Fetch live snippet
                v_res = yt.videos().list(part='snippet', id=vid).execute()
                items = v_res.get('items', [])
                if not items:
                    print(f"  Warning: Video {vid} not found on YouTube.")
                    progress[vid] = {'done': True, 'error': 'not_found'}
                    success = True
                    break

                snip = items[0]['snippet']
                channel_id = snip.get('channelId', '')
                if channel_id != 'UCPqB1A_WzpLJec6q69BOO3Q':
                    print(f"  External video ({channel_id}). Skipping.")
                    progress[vid] = {'done': True, 'action': 'skipped_external'}
                    success = True
                    break

                curr_dl = snip.get('defaultLanguage')
                curr_dal = snip.get('defaultAudioLanguage')
                tags = snip.get('tags', [])
                tag_added = False
                if 'yt:cc=on' not in tags:
                    tags.append('yt:cc=on')
                    tag_added = True

                # Check if update is needed
                needs_update = (curr_dl != 'ta' or curr_dal != 'ta' or tag_added)
                if needs_update:
                    snip['defaultLanguage'] = 'ta'
                    snip['defaultAudioLanguage'] = 'ta'
                    snip['tags'] = tags

                    yt.videos().update(
                        part='snippet',
                        body={'id': vid, 'snippet': snip}
                    ).execute()
                    print(f"  --> Updated defaultLanguage='ta', defaultAudioLanguage='ta', yt:cc=on", flush=True)

                # 2. Audit & delete any English caption tracks
                try:
                    c_res = yt.captions().list(part='snippet', videoId=vid).execute()
                    c_items = c_res.get('items', [])
                    for c in c_items:
                        c_snip = c.get('snippet', {})
                        c_lang = c_snip.get('language', '')
                        if c_lang == 'en' or c_lang.startswith('en-'):
                            print(f"  Found English caption track ({c['id']})! Deleting...", flush=True)
                            yt.captions().delete(id=c['id']).execute()
                            deleted_en_cc_count += 1
                            print(f"  --> Deleted English caption track.", flush=True)
                except Exception as ce:
                    if 'quotaExceeded' in str(ce):
                        raise ce
                    pass

                progress[vid] = {
                    'done': True,
                    'action': 'standardized_tamil',
                    'prev_dl': curr_dl,
                    'prev_dal': curr_dal,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                success_count += 1
                success = True
                time.sleep(0.5)

            except Exception as e:
                err_str = str(e)
                if 'quotaExceeded' in err_str:
                    print(f"Quota exceeded on {tokens[active_idx]}! Switching to backup token...")
                    active_idx += 1
                    if active_idx < len(tokens):
                        yt = get_yt_client(tokens[active_idx])
                        print(f"Switched to {tokens[active_idx]}")
                    else:
                        print("All tokens have exhausted quota for today.")
                        break
                else:
                    print(f"  Error on {vid}: {e}")
                    progress[vid] = {'done': False, 'error': err_str}
                    break

        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

        if active_idx >= len(tokens):
            print("\nHalting early: Quota limit reached on all tokens.")
            break

    print("\n" + "=" * 60)
    print("STANDARDIZATION BATCH COMPLETE:")
    print(f"  Successfully standardized: {success_count}")
    print(f"  Skipped / Already Canonical: {skipped_count}")
    print(f"  English caption tracks deleted: {deleted_en_cc_count}")
    print(f"  Total Processed: {success_count + skipped_count} / {len(targets)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
