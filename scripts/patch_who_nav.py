import os

files = ['about.html', 'index.html', 'docs/about.html', 'docs/index.html', 'site/about.html', 'site/index.html']

nav_snippet = '''      <!-- 10. யார் நாம்? (Who We Are? — தொன்மை சனாதன வம்சாவளி & பரம்பரை) -->
      <div class="strip-group" data-group="who_we_are">
        <a href="who-we-are.html" class="strip-item" data-tooltip="யார் நாம்? (Who We Are)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></span>
          <span class="strip-item-label">யார் நாம்? (Who We Are)</span>
        </a>
      </div>
'''

footer_snippet = '''          <li><a href="who-we-are.html">👑 யார் நாம்? (தொன்மை வம்சாவளி &amp; மரபு)</a></li>\n'''

base_dir = r'C:\GitHub\Gurukuladesam'
for rel in files:
    fn = os.path.join(base_dir, rel)
    if not os.path.exists(fn):
        print(f"Skipping missing {fn}")
        continue
    with open(fn, 'r', encoding='utf-8', errors='surrogateescape') as f:
        content = f.read()

    changed = False
    if 'who-we-are.html' not in content:
        pos_admin = content.find('data-group="admin"')
        if pos_admin != -1:
            pos_close_div = content.find('</div>\n      </div>', pos_admin)
            if pos_close_div != -1:
                insert_pos = pos_close_div + len('</div>\n      </div>\n\n')
                content = content[:insert_pos] + nav_snippet + '\n' + content[insert_pos:]
                changed = True
            else:
                pos_close_nav = content.find('</nav>', pos_admin)
                if pos_close_nav != -1:
                    content = content[:pos_close_nav] + nav_snippet + '    ' + content[pos_close_nav:]
                    changed = True
        
        for pattern in ['<li><a href="admissions.html">', '<li><a href="school.html">']:
            if pattern in content:
                content = content.replace(pattern, footer_snippet + '          ' + pattern, 1)
                changed = True
                break

    if changed:
        with open(fn, 'w', encoding='utf-8', errors='surrogateescape') as f:
            f.write(content)
        print(f"Successfully updated {fn}")
    else:
        print(f"Already updated or no change in {fn}")
