import pathlib
from playwright.sync_api import sync_playwright

url = pathlib.Path('tharam-1.html').resolve().as_uri()
with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge')
    for w in (1280, 390):
        pg = b.new_page(viewport={'width': w, 'height': 900})
        pg.set_default_timeout(5000)
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(url + '#books', wait_until='domcontentloaded')
        pg.wait_for_timeout(800)
        print('== width', w, 'hscroll:', pg.evaluate('document.documentElement.scrollWidth>innerWidth'), flush=True)
        for m in ['books', 'sheets', 'highlights', 'panpaadu', 'virtues', 'books']:
            pg.click(f'#hubBtn_{m}')
            pg.wait_for_timeout(250)
            act = pg.evaluate("document.querySelector('.grade-hub-btn.active').id")
            vis = pg.evaluate("[...document.querySelectorAll('.course-main-column > *')].filter(e=>e.offsetHeight>0).length")
            print(m, 'active=', act, 'visible=', vis, flush=True)
        st = pg.evaluate("""()=>{const c=document.querySelector('.grade-7books-box');const cs=getComputedStyle(c);
          const cards=[...c.querySelectorAll(':scope > div:last-of-type > div')];
          const rs=cards.map(d=>d.getBoundingClientRect());
          return {bg:cs.backgroundImage+'|'+cs.backgroundColor,border:cs.borderTopWidth,
          cardBg:getComputedStyle(cards[0]).backgroundColor,cardBorder:getComputedStyle(cards[0]).borderLeftWidth,
          n:cards.length,overflow:rs.some(r=>r.right>innerWidth+1),cols:new Set(rs.map(r=>Math.round(r.left))).size}}""")
        print('books box', st, flush=True)
        hrefs = pg.eval_on_selector_all('.grade-7books-box a', 'els=>els.map(a=>a.getAttribute("href"))')
        for h in hrefs:
            f = pathlib.Path(h.split('?')[0].split('#')[0])
            print(' ', h, 'exists' if f.exists() else 'MISSING', flush=True)
        print('errors', errs, flush=True)
        pg.close()
    b.close()
