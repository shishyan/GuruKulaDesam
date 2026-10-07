# -*- coding: utf-8 -*-
"""Retry downloading scan pages that failed (403) in export_scan_images.py, with fresh tokens."""
import urllib.request, re, sys, json, html as H, os, time, shutil, subprocess

sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120 Safari/537.36'}
BASE = "https://sites.google.com/view/wwwgurukuladesamcom/home/%E0%AE%9A%E0%AE%B5-%E0%AE%A8%E0%AE%B1/%E0%AE%A4%E0%AE%B0%E0%AE%AE-{g}"
PAT = r'https://sites\.google\.com/sitesv-images-rt/[A-Za-z0-9_\-]+'
uniq = lambda t: list(dict.fromkeys(re.findall(PAT, H.unescape(t))))


def ext(b):
    return 'png' if b[:4] == b'\x89PNG' else ('webp' if b[:4] == b'RIFF' else 'jpg')


for g in (1, 2):
    url = BASE.format(g=g)
    orig = json.loads(subprocess.check_output(['git', 'show', f'HEAD:grade{g}_images.json']).decode('utf-8'))
    old = uniq(open(f'scraped_Saiva_Neri_-_Grade_{g}.html', encoding='utf-8').read())
    pos = [old.index(x.split('=')[0]) for x in orig]
    outdir = f'assets/images/saiva-neri/grade{g}'
    have = lambda n: any(os.path.exists(f'{outdir}/p{n:02d}.{e}') for e in ('jpg', 'png', 'webp'))
    for attempt in range(8):
        missing = [n for n in range(1, len(orig) + 1) if not have(n)]
        print(f'Grade {g} attempt {attempt}: missing {len(missing)}')
        if not missing:
            break
        fresh = uniq(urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read().decode('utf-8', 'ignore'))
        for n in missing:
            src = fresh[pos[n - 1]]
            for v in (src + '=w1280', src):
                try:
                    d = urllib.request.urlopen(urllib.request.Request(v, headers={**UA, 'Referer': url}), timeout=60).read()
                    open(f'{outdir}/p{n:02d}.{ext(d)}', 'wb').write(d)
                    break
                except Exception:
                    pass
            time.sleep(1.5)
    # final local list + html rewrite
    local = []
    for n, o in enumerate(orig, 1):
        f = next((f'assets/images/saiva-neri/grade{g}/p{n:02d}.{e}' for e in ('jpg', 'png', 'webp') if os.path.exists(f'{outdir}/p{n:02d}.{e}')), None)
        local.append(f or o)
    for root in ('.', 'docs', 'site'):
        p = os.path.join(root, f'tharam-{g}.html')
        if not os.path.exists(p):
            continue
        s = open(p, encoding='utf-8').read()
        for o, l in zip(orig, local):
            if l != o:
                s = s.replace(o, l)
        open(p, 'w', encoding='utf-8', newline='').write(s)
    json.dump(local, open(f'grade{g}_images.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    for root in ('docs', 'site'):
        shutil.copytree(outdir, os.path.join(root, outdir), dirs_exist_ok=True)
    print(f'Grade {g}: still remote = {sum(x.startswith("http") for x in local)}')
