"""Layout-only fixes for grade pages (hub bar + 7 books grid) appended to style.css.

Design rule: NO backgrounds or borders (see global scrub rules). This block only
adjusts grid/spacing/focus/readability. Idempotent; replaces any previous UX FIX block.
"""
p = 'assets/css/style.css'
MARK = '/* ===== UX FIX'
txt = open(p, encoding='utf-8', newline='').read()
i = txt.find(MARK)
if i != -1:
    txt = txt[:i].rstrip() + '\n'

r = lambda x: x * 20
B = r('.grade-7books-box')
bx = 'html body .course-main-column ' + B
card = bx + ' > div:last-of-type > div'
cols = ['#38bdf8', '#34d399', '#facc15', '#c084fc', '#fb923c', '#34d399', '#fde68a']
out = [
    MARK + ': layout only, borderless/backgroundless per design ===== */',
    f'{bx} {{padding:8px 0 !important; overflow:visible;}}',
    f'{bx} > div:last-of-type {{display:grid !important; grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr)) !important; gap:16px 24px !important;}}',
    f'{card} {{padding:6px 0 !important; line-height:1.65; word-break:normal; overflow-wrap:anywhere;}}',
]
for n, c in enumerate(cols, 1):
    out.append(f'{card}:nth-child({n}) > strong a {{color:{c} !important;}}')
out += [
    '.grade-7books-box a:focus-visible, .grade-hub-btn:focus-visible {outline:2px solid #fde68a; outline-offset:2px;}',
    '.grade-7books-box a[href*="book="] {text-underline-offset:3px;}',
    '.grade-7books-box a[href*="book="]:hover {color:#fff !important;}',
    '.grade-hub-btn .hub-label {overflow-wrap:anywhere;}',
]
open(p, 'w', encoding='utf-8', newline='').write(txt + '\n' + '\n'.join(out) + '\n')
print('ok')
