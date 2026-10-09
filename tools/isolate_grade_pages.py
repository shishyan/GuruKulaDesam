import re, glob, sys

sys.stdout.reconfigure(encoding='utf-8')

for f in sorted(glob.glob("tharam-*.html")):
    m = re.search(r'tharam-(\d+)\.html', f)
    if not m:
        continue
    g = m.group(1)
    
    with open(f, "r", encoding="utf-8") as fp:
        c = fp.read()
    
    # 1. Replace the entire region from header/switcher up to THE 7 SACRED BOOKS SHELF
    pat = re.compile(r'(?:<!--\s*GRADE FOCUSED SHELF HEADER\s*-->|<!--\s*QUICK GRADE SWITCHER STRIP\s*-->)[\s\S]*?(?=<!--\s*THE 7 SACRED BOOKS SHELF)', re.DOTALL)
    
    clean_bar = f'''<!-- GRADE FOCUSED SHELF HEADER -->
      <div class="grade-focus-bar" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin: 10px 0 16px; padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.08);">
        <div style="color:var(--gold-soft); font-size:0.9rem; font-weight:700;">
          📖 தரம் {g} — 7 ஆசிரமப் பாடநூல்கள் மட்டுமே (Exclusive Grade {g} Curriculum)
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <a href="school.html" class="sheet-btn" style="font-size:0.8rem; padding:6px 14px; text-decoration:none;">🏛️ வித்யா குடீரம் பள்ளி அரங்கம்</a>
          <a href="books.html?grade={g}" class="sheet-btn sheet-btn-view" style="font-size:0.8rem; padding:6px 14px; text-decoration:none;">முழு மின்னூல் அரங்கம் &rarr;</a>
        </div>
      </div>

      '''
    
    c_new = pat.sub(clean_bar, c)
    
    # 2. Remove Quick 12 Grades Jump Footer Grid if still present
    jump_grid_pat = re.compile(r'<!--\s*Quick 12 Grades Jump Footer Grid\s*-->\s*<div style="margin-top:35px;[\s\S]*?</div>\s*</div>', re.DOTALL)
    c_new = jump_grid_pat.sub('', c_new)
    
    if c_new != c:
        with open(f, "w", encoding="utf-8") as fp:
            fp.write(c_new)
        print(f"Isolated Grade {g} in {f} - removed all cross-grade references.")

print("All grade pages isolated successfully.")
