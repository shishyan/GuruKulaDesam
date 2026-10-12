import json, sys, pathlib, re
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path('.')
token_path = ROOT / 'data/credentials/token_backup_guru-kula-desam.json'
creds = Credentials.from_authorized_user_file(str(token_path))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

vids = json.load(open(ROOT / 'production/youtube_backup/videos.json', encoding='utf-8'))
vid_ids = [v['id'] for v in vids]

live_vids = []
for i in range(0, len(vid_ids), 50):
    chunk = vid_ids[i:i+50]
    res = yt.videos().list(part='status,snippet,contentDetails,statistics', id=','.join(chunk)).execute()
    live_vids.extend(res.get('items', []))

public_vids = [v for v in live_vids if v.get('status', {}).get('privacyStatus') == 'public']

def extract_core_topic(title):
    # Normalize title to extract core topic
    t = title.lower()
    # Check for thirukkural chapter
    m_adh = re.search(r'அதிகாரம்\s*(\d+)', t)
    if m_adh:
        return f"thirukkural_adhikaram_{m_adh.group(1)}"
    
    # Specific known works
    known = [
        ('தமிழ்த்தாய் வாழ்த்து', 'thamizhthai_vaazhthu'),
        ('ரகுபதி ராகவ', 'raghupati_raghava'),
        ('இராம கிருஷ்ண துதி', 'rama_krishna_thuthi'),
        ('திருப்புலம்பல்', 'thiruppulambal'),
        ('வேதஸார', 'vedasaara_shiva'),
        ('வேதசார்', 'vedasaara_shiva'),
        ('சிவ சுப்ரமணியர் திருவிருத்தம்', 'siva_subramaniyar_thiruvirutham'),
        ('வான்முகில் வழாது பெய்க', 'kaanmugil_vazhadhu'),
        ('வான் முகில் வழாது பெய்க', 'kaanmugil_vazhadhu'),
        ('கந்தபுராணம் வாழ்த்து', 'kaanmugil_vazhadhu'),
        ('தென்னாடுடைய சிவனே', 'thennadudaiya_sivane'),
        ('திருப்பாவை - 1', 'thiruppavai_1'),
        ('திருப்பாவை 1', 'thiruppavai_1'),
        ('திருப்பாவை 2', 'thiruppavai_2'),
        ('பாலும் தெளிதேனும்', 'paalum_thelithenum'),
        ('தனந்தரும் கல்வி', 'dhanam_tharum_kalvi'),
        ('சமயபுரத்தாயே', 'samayapurathaye'),
        ('ஓம் நமோ நாராயணாய', 'om_namo_narayanaya'),
        ('துஞ்சலும் துஞ்சல்', 'tunjalum_tunjal'),
        ('திருநீற்றுப் பதிகம்', 'thiruneetru_pathigam'),
        ('மாசில் வீணையும்', 'maasil_veenaiyum'),
    ]
    for pattern, key in known:
        if pattern in t:
            return key
    return None

# Group by (duration, core_topic)
groups = {}
for v in public_vids:
    dur = v['contentDetails']['duration']
    topic = extract_core_topic(v['snippet']['title'])
    if topic:
        groups.setdefault((dur, topic), []).append(v)

exact_dups = []
for (dur, topic), v_list in groups.items():
    if len(v_list) >= 2:
        # Sort by view count descending
        v_list.sort(key=lambda x: int(x.get('statistics', {}).get('viewCount', 0)), reverse=True)
        keeper = v_list[0]
        for red in v_list[1:]:
            exact_dups.append({
                'topic': topic,
                'duration': dur,
                'keep_id': keeper['id'],
                'keep_title': keeper['snippet']['title'],
                'keep_views': int(keeper.get('statistics', {}).get('viewCount', 0)),
                'redundant_id': red['id'],
                'redundant_title': red['snippet']['title'],
                'redundant_views': int(red.get('statistics', {}).get('viewCount', 0))
            })

print(f"Found {len(exact_dups)} verified exact duplicate videos:")
for d in exact_dups:
    print(f"[{d['topic']} | {d['duration']}]")
    print(f"   KEEP: [{d['keep_id']}] ({d['keep_views']} views) - {d['keep_title'][:50]}")
    print(f"   PRIVATIZE: [{d['redundant_id']}] ({d['redundant_views']} views) - {d['redundant_title'][:50]}")
    print()

out_path = ROOT / 'production' / 'verified_exact_duplicates.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(exact_dups, f, indent=2, ensure_ascii=False)
print(f"Saved to {out_path}")
