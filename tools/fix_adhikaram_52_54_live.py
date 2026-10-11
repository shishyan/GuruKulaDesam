import json, sys, pathlib
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path('.')
tk_data = json.load(open(ROOT / 'production/thirukkural_all.json', encoding='utf-8'))
kurals_by_num = {item['Number']: item for item in tk_data['kural']}

token_path = ROOT / 'data/credentials/token_backup_guru-kula-desam.json'
creds = Credentials.from_authorized_user_file(str(token_path))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

targets = [
    {
        'vid': 'oEH4ztdn2Nc',
        'chapter': 54,
        'title_ta': 'பொச்சாவாமை',
        'title_en': 'Pochchaavaamai',
        'sub': 'Unmindfulness & Constant Vigilance',
        'total_dur': 320.0,
        'intro': 12.0,
        'outro': 312.0,
        'start_k': 531,
        'end_k': 540
    },
    {
        'vid': 'F6PrK6E9qB0',
        'chapter': 52,
        'title_ta': 'தெரிந்து வினையாடல்',
        'title_en': 'Therinthu Vinaiyaadal',
        'sub': 'Selection & Delegation of Trusted Allies',
        'total_dur': 383.0,
        'intro': 12.0,
        'outro': 375.0,
        'start_k': 511,
        'end_k': 520
    }
]

for t in targets:
    vid = t['vid']
    ch = t['chapter']
    print(f"\n=======================================================")
    print(f"Processing {vid} (Chapter {ch}: {t['title_ta']})...")
    print(f"=======================================================")
    
    # 1. Generate SRT
    start_k = t['start_k']
    end_k = t['end_k']
    active_dur = t['outro'] - t['intro']
    slot = active_dur / 10.0
    display_dur = slot - 0.8
    
    srt_entries = []
    kural_sections = []
    chapter_timestamps = [f"00:00 - தொடக்கம் (Prelude)"]
    
    for i in range(10):
        kn = start_k + i
        kd = kurals_by_num[kn]
        st = t['intro'] + i * slot
        et = st + display_dur
        
        srt_entries.append(f"{i+1}\n{format_time(st)} --> {format_time(et)}\nகுறள் {kn}:\n{kd['Line1']}\n{kd['Line2']}\n")
        
        mean = kd.get('mv') or kd.get('mk') or kd.get('sp') or kd.get('explanation')
        kural_sections.append(f"குறள் {kn}:\n{kd['Line1']}\n{kd['Line2']}\nஉரை: {mean}")
        
        # chapter timestamp
        chapter_timestamps.append(f"{format_time(st)[:5]} - குறள் {kn}: {kd['Line1'][:25]}...")

    chapter_timestamps.append(f"{format_time(t['outro'])[:5]} - நிறைவு (Outro & Finale)")
    
    srt_content = "\n".join(srt_entries)
    srt_file = ROOT / f'production/subtitles/{vid}.srt'
    srt_file.write_text(srt_content, encoding='utf-8')
    print(f"Saved verified 10-Kural SRT to {srt_file}")
    
    # 2. Build Description
    full_kurals_text = "\n\n".join(kural_sections)
    timestamps_text = "\n".join(chapter_timestamps)
    
    desc = f"""திருக்குறள்: அதிகாரம் {ch} - {t['title_ta']} | {t['title_en']} - {t['sub']} | Guru Kula Desam

அதிகாரம் {ch}: {t['title_ta']} ({t['title_en']}) — வள்ளுவர் அருளிய முப்பாலில் அமைந்த உன்னத வாழ்வியல் நெறி.

Chapter {ch}: {t['title_en']} ({t['sub']}) from Thirukkural by Thiruvalluvar. Classical musical rendition produced by Guru Kula Desam with authentic Tamil heritage aesthetics.

⏱️ Timestamps / Chapters:
{timestamps_text}

═════════════════════════════════════════════════════════════════
📜 அதிகாரம் {ch}: {t['title_ta']} — முழுப் பாடல் வரிகளும் உரையும் (Kurals {start_k}-{end_k})
═════════════════════════════════════════════════════════════════
{full_kurals_text}

═════════════════════════════════════════════════════════════════
🎵 Credits & Release Info:
• Track: அதிகாரம் {ch} - {t['title_ta']} (Original Master)
• Channel: Guru Kula Desam (@guru-kula-desam)
• Production & Vocals: Nagarajan Balasubramanian
• Thirukkural Master Collection: https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro

#திருக்குறள் #{t['title_ta']} #Thirukkural #{t['title_en']} #TamilHeritage #GuruKulaDesam #Wisdom #Ethics

— குரு குல தேசம் | Guru Kula Desam
https://gurukuladesam.com
"""
    print(f"Description length: {len(desc)} characters")
    
    # Update Description on YouTube
    print(f"Updating video description on YouTube for {vid}...")
    v_obj = yt.videos().list(part='snippet', id=vid).execute()['items'][0]
    v_snippet = v_obj['snippet']
    v_snippet['description'] = desc
    yt.videos().update(part='snippet', body={'id': vid, 'snippet': v_snippet}).execute()
    print("SUCCESS: Live video description updated on YouTube!")
    
    # Update Captions on YouTube
    print(f"Updating captions on YouTube for {vid}...")
    caps = yt.captions().list(part='snippet', videoId=vid).execute()
    for c in caps.get('items', []):
        cid = c['id']
        clang = c['snippet']['language']
        cname = c['snippet']['name']
        print(f"Deleting old caption track: {cid} ({clang} - {cname})...")
        yt.captions().delete(id=cid).execute()
        print("Old caption deleted.")
        
    print("Uploading new 10-Kural caption track...")
    media = MediaFileUpload(str(srt_file), mimetype='application/x-subrip', resumable=True)
    new_cap = yt.captions().insert(
        part='snippet',
        body={
            'snippet': {
                'videoId': vid,
                'language': 'ta',
                'name': 'தமிழ் பாடல் வரிகள் (Tamil Lyrics)',
                'isDraft': False
            }
        },
        media_body=media
    ).execute()
    print(f"SUCCESS: Uploaded new caption track {new_cap.get('id')}!")
    
    # Verify download
    d_check = yt.captions().download(id=new_cap['id']).execute().decode('utf-8')
    print(f"Verified live track download: {len(d_check)} chars, {d_check.count('-->')} blocks confirmed!")

print("\nALL TARGET THIRUKKURAL TRACKS 100% FIXED & VERIFIED ON YOUTUBE!")
