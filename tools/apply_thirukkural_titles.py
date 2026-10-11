import sys, os, json, pathlib, time, re
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROGRESS_FILE = ROOT / "production" / "thirukkural_titles_progress.json"
TITLES_FILE = ROOT / "production" / "thirukkural_standardized_titles_ready.json"

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
    except Exception as e:
        if 'quotaExceeded' in str(e):
            return False
        return False

def main():
    if not TITLES_FILE.exists():
        print(f"Error: {TITLES_FILE} not found!")
        return

    items = json.load(open(TITLES_FILE, encoding='utf-8'))
    print(f"Loaded {len(items)} standardized Thirukkural titles.")

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
    
    # Find first working token
    for idx, t in enumerate(tokens):
        try:
            client = get_yt_client(t)
            if client and probe_client(client):
                yt = client
                active_idx = idx
                print(f"Using active credential: {t}")
                break
        except Exception as e:
            continue

    if not yt:
        print("ERROR: All API credentials currently have quota exceeded or are invalid.")
        print("Please wait until the daily quota reset at 12:30:00 PM IST.")
        return

    updated_count = 0
    skipped_count = 0

    for idx, row in enumerate(items):
        vid = row['videoId']
        new_title = row['standardized_title']
        chap = row['chapter']

        if progress.get(vid, {}).get('done'):
            skipped_count += 1
            continue

        print(f"[{idx+1}/{len(items)}] Updating Chap {chap} ({vid}): {new_title}")

        # Attempt update with active token, failover if quota exceeded
        success = False
        while not success and active_idx < len(tokens):
            try:
                # 1. Fetch current snippet
                v_res = yt.videos().list(part='snippet', id=vid).execute()
                v_items = v_res.get('items', [])
                if not v_items:
                    print(f"  Warning: Video {vid} not found on YouTube.")
                    progress[vid] = {'done': True, 'error': 'not_found'}
                    success = True
                    break

                snip = v_items[0]['snippet']
                channel_id = snip.get('channelId', '')
                if channel_id != 'UCPqB1A_WzpLJec6q69BOO3Q':
                    print(f"  External video (channel {channel_id}). Skipping update.")
                    progress[vid] = {'done': True, 'action': 'skipped_external_channel', 'channelId': channel_id}
                    success = True
                    skipped_count += 1
                    break

                current_live_title = snip.get('title', '')
                if current_live_title == new_title:
                    print(f"  Already matches live title! Skipping.")
                    progress[vid] = {'done': True, 'action': 'already_matched', 'title': new_title}
                    success = True
                    skipped_count += 1
                    break

                # 2. Update title
                snip['title'] = new_title
                yt.videos().update(
                    part='snippet',
                    body={
                        'id': vid,
                        'snippet': snip
                    }
                ).execute()

                print(f"  --> Updated successfully to: {new_title}")
                progress[vid] = {
                    'done': True,
                    'action': 'updated',
                    'old_title': current_live_title,
                    'new_title': new_title,
                    'updated_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                updated_count += 1
                success = True
                time.sleep(0.5)

            except Exception as e:
                err_str = str(e)
                if 'quotaExceeded' in err_str:
                    print(f"Quota exceeded on {tokens[active_idx]}! Switching to next token...")
                    active_idx += 1
                    if active_idx < len(tokens):
                        yt = get_yt_client(tokens[active_idx])
                        print(f"Switched to {tokens[active_idx]}")
                    else:
                        print("All tokens have exhausted quota for today.")
                        break
                else:
                    print(f"  Error updating {vid}: {e}")
                    progress[vid] = {'done': False, 'error': err_str}
                    break

        # Save progress after every video
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

        if active_idx >= len(tokens):
            print("\nTerminating run early: Quota exhausted on all tokens.")
            break

    print("\n" + "=" * 60)
    print(f"BATCH FINISHED:")
    print(f"  Updated: {updated_count}")
    print(f"  Skipped / Already Canonical: {skipped_count}")
    print(f"  Total Processed: {updated_count + skipped_count} / {len(items)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
