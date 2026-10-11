import json, sys, pathlib, datetime, time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = pathlib.Path('.')
token_path = ROOT / 'data/credentials/token_backup_guru-kula-desam.json'
creds = Credentials.from_authorized_user_file(str(token_path))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

dups = json.load(open(ROOT / 'production/verified_exact_duplicates.json', encoding='utf-8'))

# Deduplicate redundant_ids and exclude self-matches
unique_redundants = {}
for d in dups:
    rid = d['redundant_id']
    kid = d['keep_id']
    if rid == kid:
        continue # NEVER privatize the keeper itself!
    if rid not in unique_redundants:
        unique_redundants[rid] = d

print(f"Total verified redundant duplicate videos to privatize: {len(unique_redundants)}", flush=True)

log_entries = []
for idx, (rid, d) in enumerate(unique_redundants.items(), 1):
    print(f"[{idx}/{len(unique_redundants)}] Privatizing [{rid}] ({d['redundant_views']}v) '{d['redundant_title'][:40]}' (Duplicate of [{d['keep_id']}])", flush=True)
    try:
        body = {
            'id': rid,
            'status': {
                'privacyStatus': 'private'
            }
        }
        res = yt.videos().update(part='status', body=body).execute()
        new_status = res.get('status', {}).get('privacyStatus')
        print(f"  -> SUCCESS: Status is now '{new_status}'", flush=True)
        log_entries.append({
            'redundant_id': rid,
            'redundant_title': d['redundant_title'],
            'redundant_views': d['redundant_views'],
            'keep_id': d['keep_id'],
            'keep_title': d['keep_title'],
            'keep_views': d['keep_views'],
            'topic': d['topic'],
            'duration': d['duration'],
            'status': new_status,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        time.sleep(0.2)
    except Exception as e:
        print(f"  -> ERROR: {e}", flush=True)

out_log = ROOT / 'production' / 'privatized_verified_duplicates_log.json'
with open(out_log, 'w', encoding='utf-8') as f:
    json.dump(log_entries, f, indent=2, ensure_ascii=False)
print(f"\nCompleted! Privatized {len(log_entries)} duplicate videos. Log saved to {out_log}", flush=True)
