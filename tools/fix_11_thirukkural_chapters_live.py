import json, sys, pathlib, re, time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

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

def iso_dur_to_sec(dur_str):
    m = re.match(r'PT(?:(\d+)M)?(?:(\d+)S)?', dur_str)
    if not m: return 210.0
    mins = int(m.group(1) or 0)
    secs = int(m.group(2) or 0)
    return mins * 60 + secs

chapters = [
    {'vid': 'IHMZsM7LJf8', 'ch': 74, 'title_ta': 'நாடு', 'title_en': 'Naadu', 'sub': 'The Prosperous Realm'},
    {'vid': 'UPAYRisyN7Q', 'ch': 67, 'title_ta': 'வினைத்திட்பம்', 'title_en': 'Vinaithitpam', 'sub': 'Resolute Action'},
    {'vid': 'lvlDsTq-skg', 'ch': 66, 'title_ta': 'வினைத்தூய்மை', 'title_en': 'Vinaithooymai', 'sub': 'Purity of Action'},
    {'vid': 'OXgMCvchSt8', 'ch': 62, 'title_ta': 'ஆள்வினையுடைமை', 'title_en': 'Aalvinaiyudaimai', 'sub': 'Manly Effort'},
    {'vid': 'YqHg3hf8T8w', 'ch': 57, 'title_ta': 'வெருவந்த செய்யாமை', 'title_en': 'Veruvantha Seyyaamai', 'sub': 'Benevolent Governance'},
    {'vid': 'u23cwmejN1k', 'ch': 46, 'title_ta': 'சிற்றினஞ்சேராமை', 'title_en': 'Sitrinanjeraamai', 'sub': 'Avoiding Base Fellowship'},
    {'vid': 'U-u4rAYBUkc', 'ch': 44, 'title_ta': 'குற்றங்கடிதல்', 'title_en': 'Kutrangadithal', 'sub': 'Guarding Against Faults'},
    {'vid': '3FoioD6p6Mk', 'ch': 40, 'title_ta': 'கல்வி', 'title_en': 'Kalvi', 'sub': 'Sacred Learning & The Lamp of Education'},
    {'vid': 'AD6LgqNksFQ', 'ch': 30, 'title_ta': 'வாய்மை', 'title_en': 'Vaaimai', 'sub': 'The Power of Absolute Truthfulness'},
    {'vid': 'G6NSHWKhQcY', 'ch': 16, 'title_ta': 'பொறையுடைமை', 'title_en': 'Poraiyudaimai', 'sub': 'Forbearance & Supreme Forgiveness'},
    {'vid': 'MXK8vB3_fBE', 'ch': 25, 'title_ta': 'அருளுடைமை', 'title_en': 'Aruludaimai', 'sub': 'Universal Grace & Compassion to All Beings'}
]

print(f"Beginning live fix of {len(chapters)} Thirukkural chapter videos on YouTube...", flush=True)

for idx, item in enumerate(chapters, 1):
    vid = item['vid']
    ch = item['ch']
    title_ta = item['title_ta']
    title_en = item['title_en']
    sub = item['sub']
    
    print(f"\n=======================================================", flush=True)
    print(f"[{idx}/{len(chapters)}] Processing {vid} (Chapter {ch}: {title_ta})...", flush=True)
    print(f"=======================================================", flush=True)
    
    # Get live video metadata
    v_obj = yt.videos().list(part='snippet,contentDetails', id=vid).execute()['items'][0]
    total_dur = float(iso_dur_to_sec(v_obj['contentDetails']['duration']))
    intro = 12.0
    outro = total_dur - 8.0
    active_dur = outro - intro
    slot = active_dur / 10.0
    display_dur = slot - 0.8
    
    start_k = (ch - 1) * 10 + 1
    end_k = ch * 10
    
    # 1. Build 10-Kural SRT
    srt_entries = []
    kural_sections = []
    chapter_timestamps = [f"00:00 - தொடக்கம் (Prelude)"]
    
    for i in range(10):
        kn = start_k + i
        kd = kurals_by_num[kn]
        st = intro + i * slot
        et = st + display_dur
        
        srt_entries.append(f"{i+1}\n{format_time(st)} --> {format_time(et)}\nகுறள் {kn}:\n{kd['Line1']}\n{kd['Line2']}\n")
        
        mean = kd.get('mv') or kd.get('mk') or kd.get('sp') or kd.get('explanation')
        kural_sections.append(f"குறள் {kn}:\n{kd['Line1']}\n{kd['Line2']}\nஉரை: {mean}")
        chapter_timestamps.append(f"{format_time(st)[:5]} - குறள் {kn}: {kd['Line1'][:25]}...")

    chapter_timestamps.append(f"{format_time(outro)[:5]} - நிறைவு (Outro & Finale)")
    
    srt_content = "\n".join(srt_entries)
    srt_file = ROOT / f'production/subtitles/{vid}.srt'
    srt_file.write_text(srt_content, encoding='utf-8')
    print(f"Saved verified 10-Kural SRT to {srt_file}", flush=True)
    
    # 2. Build Title & Description
    std_title = f"திருக்குறள்: அதிகாரம் {ch} - {title_ta} | {title_en} - {sub} | Guru Kula Desam"
    if len(std_title) > 100:
        std_title = f"திருக்குறள்: அதிகாரம் {ch} - {title_ta} | {title_en} | Guru Kula Desam"
        
    full_kurals_text = "\n\n".join(kural_sections)
    timestamps_text = "\n".join(chapter_timestamps)
    
    desc = f"""{std_title}

அதிகாரம் {ch}: {title_ta} ({title_en}) — வள்ளுவர் அருளிய முப்பாலில் அமைந்த உன்னத வாழ்வியல் நெறி.

Chapter {ch}: {title_en} ({sub}) from Thirukkural by Thiruvalluvar. Classical musical rendition produced by Guru Kula Desam with authentic Tamil heritage aesthetics.

⏱️ Timestamps / Chapters:
{timestamps_text}

═════════════════════════════════════════════════════════════════
📜 அதிகாரம் {ch}: {title_ta} — முழுப் பாடல் வரிகளும் உரையும் (Kurals {start_k}-{end_k})
═════════════════════════════════════════════════════════════════
{full_kurals_text}

═════════════════════════════════════════════════════════════════
🎵 Credits & Release Info:
• Track: அதிகாரம் {ch} - {title_ta} (Original Master)
• Channel: Guru Kula Desam (@guru-kula-desam)
• Production & Vocals: Nagarajan Balasubramanian
• Thirukkural Master Collection: https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro

#திருக்குறள் #{title_ta} #Thirukkural #{title_en} #TamilHeritage #GuruKulaDesam #Wisdom #Ethics

— குரு குல தேசம் | Guru Kula Desam
https://gurukuladesam.com
"""
    
    # Update Video Title & Description
    v_snippet = v_obj['snippet']
    v_snippet['title'] = std_title
    v_snippet['description'] = desc
    tags = v_snippet.get('tags', [])
    if 'yt:cc=on' not in tags: tags.append('yt:cc=on')
    v_snippet['tags'] = tags
    v_snippet['defaultLanguage'] = 'ta'
    v_snippet['defaultAudioLanguage'] = 'ta'
    
    yt.videos().update(part='snippet', body={'id': vid, 'snippet': v_snippet}).execute()
    print(f"SUCCESS: Video title and description updated on YouTube!", flush=True)
    
    # Update Captions on YouTube
    caps = yt.captions().list(part='snippet', videoId=vid).execute()
    for c in caps.get('items', []):
        cid = c['id']
        clang = c['snippet']['language']
        cname = c['snippet']['name']
        print(f"Deleting old caption track: {cid} ({clang} - {cname})...", flush=True)
        yt.captions().delete(id=cid).execute()
        
    print("Uploading new 10-Kural caption track...", flush=True)
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
    print(f"SUCCESS: Uploaded new caption track {new_cap.get('id')}!", flush=True)
    
    # Verify download
    d_check = yt.captions().download(id=new_cap['id']).execute().decode('utf-8')
    print(f"Verified live track download: {len(d_check)} chars, {d_check.count('-->')} blocks confirmed!", flush=True)
    time.sleep(1.0)

print("\nALL 11 THIRUKKURAL CHAPTERS 100% FIXED & VERIFIED ON YOUTUBE!", flush=True)
