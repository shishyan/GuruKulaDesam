import sys, os, json, pathlib, time
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = pathlib.Path(__file__).resolve().parent.parent
CRED_FILE = ROOT / 'data' / 'credentials' / 'token_backup_guru-kula-desam.json'
LOG_FILE = ROOT / 'production' / 'privatized_duplicates_log.json'

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file(str(CRED_FILE))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

# Targets to make private
targets_to_hide = [
    {"hide_id": "9KBzMRfl2wk", "keep_id": "mG9IzlD9vmI", "title": "திருப்புகழ் 566 இரத்னகிரி II"},
    {"hide_id": "VBKDbEzRDVE", "keep_id": "Bg2caGP5RhA", "title": "அதிகாரம் 67 - வினைத்திட்பம்"},
    {"hide_id": "VmadaEBPB1s", "keep_id": "9iB-E9CpWUo", "title": "வேண்டுமே இத்தனையும் (திருவெம்பாவை)"},
    {"hide_id": "i_8dDkGrCCw", "keep_id": "udRsA-oWxS0", "title": "மகா கணேச பஞ்சரத்னம் (278s)"},
    {"hide_id": "XNKA3jyrIPw", "keep_id": "iXHNzqOrxzw", "title": "மகா கணேச பஞ்சரத்னம் (254s)"},
    {"hide_id": "bDF1Gz0sgpU", "keep_id": "pYuwzoJkhTE", "title": "மகா கணேச பஞ்சரத்னம் (278s II)"},
    {"hide_id": "6Q07zG4t838", "keep_id": "dd3x2HfeE0I", "title": "கைத்தல நிறைகனி (திருப்புகழ்)"},
    {"hide_id": "m3MVnlIKMTs", "keep_id": "TE5TagJU8H4", "title": "பாலும் தெளிதேனும் (203s I)"},
    {"hide_id": "7YJesR7OYZI", "keep_id": "lG2XES4aL5s", "title": "பாலும் தெளிதேனும் (203s II)"},
    {"hide_id": "eEYBleNgRGU", "keep_id": "Gdv9p4cl7TE", "title": "கந்தர் அலங்காரம் 2026"},
    {"hide_id": "0PvXn4gqlFM", "keep_id": "2xCDL6uPfbk", "title": "கந்த சஷ்டி கவசம் (1862s)"},
    {"hide_id": "Hq6XdaHfdfo", "keep_id": "F6PrK6E9qB0", "title": "திருக்குறள்: அதிகாரம் 52 - தெரிந்து வினையாடல்"},
    {"hide_id": "sa5f7NcYuRQ", "keep_id": "FvpGjzaW2TA", "title": "திருக்குறள்: அதிகாரம் 27 - தவம்"},
    {"hide_id": "leIJDxweGiM", "keep_id": "YlNGYTlCedk", "title": "இராம கிருஷ்ண துதி (506s)"}
]

print(f"Beginning privatization of {len(targets_to_hide)} exact duplicate videos...")

results = []

for idx, item in enumerate(targets_to_hide, 1):
    hid = item['hide_id']
    kid = item['keep_id']
    title = item['title']
    
    print(f"[{idx}/{len(targets_to_hide)}] Making private: {hid} (Keeping: {kid}) | {title}...", flush=True)
    try:
        res = yt.videos().update(
            part='status',
            body={
                'id': hid,
                'status': {
                    'privacyStatus': 'private'
                }
            }
        ).execute()
        
        status = res.get('status', {}).get('privacyStatus')
        print(f"  --> Successfully updated privacy to: {status}", flush=True)
        results.append({
            'id': hid,
            'keep_id': kid,
            'title': title,
            'status': status,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        })
        time.sleep(0.5)
    except Exception as e:
        print(f"  Error on {hid}: {e}", flush=True)
        results.append({
            'id': hid,
            'keep_id': kid,
            'title': title,
            'error': str(e),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        })

with open(LOG_FILE, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 60)
print(f"PRIVATIZATION COMPLETED: {sum(1 for r in results if r.get('status') == 'private')} / {len(targets_to_hide)} made private.")
print("=" * 60)
