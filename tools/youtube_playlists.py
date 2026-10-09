"""Set playlist descriptions (playlists.update). Backup is production/youtube_backup/playlists.json.

  python tools/youtube_playlists.py            # preview
  python tools/youtube_playlists.py --confirm  # apply + verify
  python tools/youtube_playlists.py --rollback --confirm
Keeps each playlist's existing title; only the description changes. Logs to youtube_backup/playlist_log.jsonl.
"""
import json, pathlib, sys, time
ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / 'production' / 'youtube_backup'
LOG = B / 'playlist_log.jsonl'
SITE = 'https://gurukuladesam.com'
FOOT = f'\n\n— குரு குல தேசம் | Guru Kula Desam\n{SITE}'

DESC = {
 'திருக்குறள் | Thirukkural — Master Collection':
   'திருக்குறள் அதிகாரம் வாரியாக இசையோடு — ஒவ்வொரு காணொளியிலும் அதிகாரத்தின் பத்துக் குறள்களும் வரிகளோடு.\nThirukkural set to music, chapter by chapter, with the verses in each description.',
 'Lord Krishnar Songs':
   'கிருஷ்ண பகவானைப் போற்றும் பாடல்கள், பஜனைகள்.\nDevotional songs and bhajans for Lord Krishna.',
 'Lord Vishnu Songs':
   'திருமாலைப் போற்றும் பாடல்கள் — திருப்பாவை உள்ளிட்டவை.\nDevotional songs for Lord Vishnu, including Thiruppavai.',
 'Lord Vinayagar Songs':
   'விநாயகப் பெருமானைப் போற்றும் பாடல்கள் — மகா கணேச பஞ்சரத்னம், ஔவையார் விநாயகர் துதி உள்ளிட்டவை.\nSongs for Lord Vinayagar, including Maha Ganesha Pancharatnam and Avvaiyar\'s invocation.',
 'Lord Murugar Songs':
   'முருகப் பெருமானைப் போற்றும் பாடல்கள் — திருப்புகழ், கந்தர் அலங்காரம், கந்த சஷ்டி கவசம் உள்ளிட்டவை.\nSongs for Lord Murugan, including Thiruppugazh, Kandar Alankaram and Kandha Sashti Kavasam.',
 'Other Songs':
   'குரு குல தேசத்தின் பிற பக்திப் பாடல்களும் பண்பாட்டுப் பாடல்களும்.\nOther devotional and cultural songs from Guru Kula Desam.',
 'Goddess Amman Songs':
   'அம்மனைப் போற்றும் பாடல்கள் — அபிராமி அந்தாதி, சரஸ்வதி போற்றி உள்ளிட்டவை.\nSongs for the Divine Mother, including Abirami Anthadhi and Saraswathi Pottri.',
 'Lord Shiva Songs':
   'சிவபெருமானைப் போற்றும் பாடல்கள் — தேவாரம், திருவாசகம், திருவெம்பாவை, திருவருட்பா உள்ளிட்ட பாடல்கள்.\nSongs for Lord Shiva, including Thevaram, Thiruvasagam, Thiruvempavai and Thiruvarutpa.',
 'Discography':
   'குரு குல தேசத்தின் அனைத்துப் பாடல்களும் ஒரே இடத்தில்.\nThe complete Guru Kula Desam song collection.',
}

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
creds = Credentials.from_authorized_user_file(str(ROOT / 'data/credentials/token.json'))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)
pls = {p['id']: p for p in json.load(open(B / 'playlists.json', encoding='utf-8'))['playlists']}
confirm = '--confirm' in sys.argv

def live(pid):
    return yt.playlists().list(part='snippet', id=pid).execute()['items'][0]['snippet']

def put(pid, desc):
    sn = live(pid)
    body = {'id': pid, 'snippet': {'title': sn['title'], 'description': desc}}
    if 'defaultLanguage' in sn:
        body['snippet']['defaultLanguage'] = sn['defaultLanguage']
    yt.playlists().update(part='snippet', body=body).execute()

def log(r):
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

if '--rollback' in sys.argv:
    for pid, p in pls.items():
        old = p['snippet'].get('description', '')
        print('ROLLBACK', p['snippet']['title'][:40], '->', len(old), 'chars')
        if confirm:
            put(pid, old)
    sys.exit(0)

for pid, p in pls.items():
    t = p['snippet']['title']
    if t not in DESC:
        print('NO TEXT for', t); continue
    new = DESC[t] + FOOT
    cur = live(pid)
    print(f"{t[:45]:45} | {len(cur.get('description',''))} -> {len(new)} chars")
    if not confirm:
        continue
    put(pid, new)
    good = False
    for _ in range(6):
        time.sleep(2)
        s = live(pid)
        good = s['description'].strip() == new.strip() and s['title'] == cur['title']
        if good:
            break
    log({'id': pid, 'title': t, 'ok': good, 'old': cur.get('description', ''), 'new': new, 't': time.time()})
    print('   ', 'VERIFIED live' if good else 'MISMATCH!', flush=True)

