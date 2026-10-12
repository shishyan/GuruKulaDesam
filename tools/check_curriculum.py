"""Read-only curriculum invariant checker for the master design.

Master design: every grade contains ONLY the 7 sacred books, and ALL content
(Thirukkural, deities, Vallalar, Periyava, YouTube...) lives inside book chapters.
This script edits nothing; it reports violations and unmapped content.

Usage: python tools/check_curriculum.py [--json out.json]
Exit code 1 if any hard violation is found.
"""
import json, re, sys, glob, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOKS = ['nanneri', 'nallaram', 'nalvazhi', 'narthunai', 'narchinthanai', 'narchol', 'narcheyal']
GRADES = list(range(1, 13))
STAGES = {'பாலப் பருவம்': (1, 3), 'இளம் பருவம்': (4, 6), 'உயர்நிலைப் பருவம்': (7, 10), 'மேல்நிலை & உயர்கல்வி': (11, 13)}
CH_FIELDS = ['title', 'verse', 'verseMeaning', 'exposition', 'story', 'lifeApplication', 'exercise']

errors, warns, info = [], [], []
E = lambda m: errors.append(m)
W = lambda m: warns.append(m)

# ---------- 1. books data: 7 books per grade, chapters complete ----------
all_text = {}
chapters_total = 0
for g in GRADES + [13]:
    p = ROOT / 'data' / 'books' / f'grade_{g}.json'
    if not p.exists():
        (E if g == 13 else E)(f'grade_{g}.json missing' + (' (collegiate/higher-studies grade has no book data)' if g == 13 else ''))
        continue
    raw = p.read_text(encoding='utf-8')
    all_text[g] = raw
    d = json.loads(raw)
    bk = d.get('books', {})
    blist = list(bk.values()) if isinstance(bk, dict) else bk
    ids = [b.get('id') for b in blist]
    if ids != BOOKS:
        E(f'grade {g}: books are {ids}, expected exactly {BOOKS}')
    for b in blist:
        chs = b.get('chapters', [])
        chapters_total += len(chs)
        if not chs:
            E(f'grade {g}/{b.get("id")}: no chapters')
        for c in chs:
            miss = [f for f in CH_FIELDS if not str(c.get(f, '')).strip()]
            if miss:
                W(f'grade {g}/{b.get("id")} ch{c.get("chapterNumber")}: empty {miss}')
    extra = [k for k in d if k not in ('grade', 'gradeTitle', 'phase', 'literatureBase', 'psychologicalGoal', 'books')]
    if extra:
        E(f'grade {g}: non-book top-level keys {extra}')
info.append(f'books data: {len([g for g in all_text])} grade files, {chapters_total} chapters')

# ---------- 2. content vault inventory + mapping into chapters ----------
cat = json.loads((ROOT / 'assets/data/catalog.json').read_text(encoding='utf-8'))
corpus = '\n'.join(all_text.values())
mapped_ids = set()
for gj in all_text.values():
    mapped_ids |= set(re.findall(r'[A-Za-z0-9_-]{11}', gj))
inv = {}
for vault, items in cat.items():
    ids = [i['id'] for i in items]
    m = [i for i in ids if i in mapped_ids]
    inv[vault] = (len(ids), len(m))
    if len(m) < len(ids):
        E(f'vault "{vault}": {len(ids) - len(m)} of {len(ids)} items not placed in any grade/book/chapter')
dupe = [k for k, v in collections.Counter(i['id'] for v in cat.values() for i in v).items() if v > 1]
if dupe:
    W(f'{len(dupe)} item ids appear in more than one vault')
info.append('vaults (items, placed): ' + ', '.join(f'{k}={a}/{b}' for k, (a, b) in inv.items()))

# ---------- 3. grade pages: nothing outside the 7 books ----------
allowed_hub = {'books'}
for g in GRADES:
    f = ROOT / f'tharam-{g}.html'
    if not f.exists():
        E(f'tharam-{g}.html missing'); continue
    t = f.read_text(encoding='utf-8')
    modes = re.findall(r"switchGradeStudyMode\('(\w+)'\)", t)
    outside = sorted(set(modes) - allowed_hub)
    if outside:
        E(f'tharam-{g}.html: non-book study modes still present: {outside}')
    if 'tharam-13' not in str(list(ROOT.glob('*.html'))) and g == 12:
        pass

# ---------- 4. orphan / legacy standalone pages still in primary nav ----------
LEGACY = ['thirukkural', 'youtube', 'virtues', 'vaishnava', 'saiva-neri', 'sakthi', 'murugan', 'vinayagar',
          'sanmargam', 'moola-nool', 'siddha', 'panpaadu', 'irai-isai-virundhu', 'grihastha', 'higher-studies', 'syllabus']
nav_src = (ROOT / 'index.html').read_text(encoding='utf-8')
nav_links = set(re.findall(r'href="([a-z\-]+)\.html', nav_src))
leg = sorted(nav_links & set(LEGACY))
if leg:
    E(f'index.html still links legacy standalone pages (should be chapters inside grades): {leg}')
mj = (ROOT / 'assets/js/main.js').read_text(encoding='utf-8', errors='ignore')
mnav = sorted({m for m in re.findall(r"""['"]([a-z\-]+)\.html""", mj)} & set(LEGACY))
if mnav:
    E(f'main.js nav still references legacy pages: {mnav}')
stage_hits = [s for s in STAGES if s in mj or s in nav_src]
if len(stage_hits) < 4:
    E(f'nav exposes {len(stage_hits)}/4 classical stages: {stage_hits}')

# ---------- report ----------
print('=== INFO ===');   [print(' ', i) for i in info]
print(f'=== ERRORS ({len(errors)}) ===');   [print(' ', e) for e in errors]
print(f'=== WARNINGS ({len(warns)}) ===');  [print(' ', w) for w in warns[:40]]
if len(warns) > 40: print(f'  ... {len(warns) - 40} more')
if '--json' in sys.argv:
    out = sys.argv[sys.argv.index('--json') + 1]
    pathlib.Path(out).write_text(json.dumps({'info': info, 'errors': errors, 'warnings': warns}, ensure_ascii=False, indent=1), encoding='utf-8')
sys.exit(1 if errors else 0)
