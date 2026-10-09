"""DRY RUN: build new YouTube descriptions from catalog.json. Writes local files only.

Usage: python tools/youtube_dryrun.py vinayagar [more vaults...]
Output: production/youtube_dryrun/<vault>/<videoId>.txt + _index.json
Rules honoured: keep existing blurb, append lyrics + meaning, no '<' or '>' (YouTube rejects),
5000-BYTE limit (Tamil = 3 bytes/char) -> flag/truncate with a pointer.
"""
import json, pathlib, sys, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / 'production' / 'youtube_backup'
OUT = ROOT / 'production' / 'youtube_dryrun'
LIMIT = 4900  # bytes, safety margin under 5000
SITE = 'https://gurukuladesam.com'

vids = {v['id']: v for v in json.load(open(B / 'videos.json', encoding='utf-8'))}
cat = json.load(open(ROOT / 'assets/data/catalog.json', encoding='utf-8'))
rep = {r['id']: r for r in json.load(open(B / 'audit_report.json', encoding='utf-8'))['rows']}

def clean(s):
    return re.sub(r'[<>]', '', (s or '').replace('\r', '')).strip()

def build(v, item):
    old = clean(v['snippet'].get('description', ''))
    if len(old) < 40 or old.strip() == 'Guru Kula Desam | குரு குல தேசம்':
        old = ''
    lyrics, meaning = clean(item.get('lyrics')), clean(item.get('meaning'))
    head = old + ('\n\n' if old else '')
    tail = f'\n\n— குரு குல தேசம் | Guru Kula Desam\n{SITE}'
    body = f'{head}பாடல் வரிகள் (Lyrics)\n{lyrics}\n\nபொருள் (Meaning)\n{meaning}{tail}'
    note = ''
    if len(body.encode('utf-8')) > LIMIT:
        # drop meaning first, then trim lyrics, keeping a pointer to the site
        body = f'{head}பாடல் வரிகள் (Lyrics)\n{lyrics}\n\nவிரிவான பொருள் விளக்கம்: {SITE}{tail}'
        note = 'meaning dropped (size)'
        while len(body.encode('utf-8')) > LIMIT:
            lyrics = lyrics[: int(len(lyrics) * 0.9)].rsplit('\n', 1)[0]
            body = f'{head}பாடல் வரிகள் (Lyrics) — முழு வரிகள்: {SITE}\n{lyrics}\n…{tail}'
            note = 'lyrics truncated (size)'
    return body, note

index = []
OVR = json.load(open(ROOT / 'production' / 'youtube_lyrics_overrides.json', encoding='utf-8'))
TKV = json.load(open(B / 'thirukkural_verified.json', encoding='utf-8')) if (B / 'thirukkural_verified.json').exists() else {}
import collections
SHARED = {vn: collections.Counter((i.get('lyrics') or '').strip() for i in items) for vn, items in cat.items()}
for vault in sys.argv[1:]:
    d = OUT / vault
    d.mkdir(parents=True, exist_ok=True)
    for item in cat[vault]:
        v = vids.get(item['id'])
        if not v:
            continue
        r = rep[item['id']]
        if r['lyrics']:
            index.append({'id': item['id'], 'vault': vault, 'action': 'skip (already has lyrics)'})
            continue
        if not (item.get('lyrics') or '').strip():
            index.append({'id': item['id'], 'vault': vault, 'action': 'skip (catalog has no lyrics)'})
            continue
        if item['id'] not in OVR:
            if vault == 'thirukkural':
                if TKV.get(item['id'], {}).get('status') != 'ok':
                    index.append({'id': item['id'], 'vault': vault, 'title': v['snippet']['title'],
                                  'action': 'BLOCKED (kural text not verified vs dataset)'})
                    continue
            else:
                key = item['lyrics'].strip()
                if SHARED[vault][key] >= 3:
                    index.append({'id': item['id'], 'vault': vault, 'title': v['snippet']['title'],
                                  'action': f'BLOCKED (same lyrics on {SHARED[vault][key]} entries - placeholder?)'})
                    continue
                if len(key) < 150:
                    index.append({'id': item['id'], 'vault': vault, 'title': v['snippet']['title'],
                                  'action': 'BLOCKED (catalog lyrics very short - likely partial)'})
                    continue
        status = ''
        if item['id'] in OVR:
            w = OVR['_works'][OVR[item['id']]['ref']]
            item = dict(item, lyrics=w['lyrics'], meaning=w['meaning'])
            status = 'override:' + w['status']
        body, note = build(v, item)
        note = (note + ' ' + status).strip()
        (d / f"{item['id']}.txt").write_text(body, encoding='utf-8')
        index.append({'id': item['id'], 'vault': vault, 'title': v['snippet']['title'], 'action': 'update',
                      'bytes': len(body.encode('utf-8')), 'note': note, 'public': not r['private']})
(OUT / '_index.json').write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding='utf-8')
for i in index:
    print(i['id'], i['action'], i.get('bytes', ''), i.get('note', ''), (i.get('title') or '')[:45])

