with open('about.html', 'rb') as f:
    b = f.read()

target = b'      </div>\r\n\r\n    </nav>'
if target not in b:
    target = b'      </div>\n\n    </nav>'

idx = b.find(target)
print('idx:', idx)
if idx != -1:
    addition = """      </div>

      <!-- 10. யார் நாம்? (Who We Are? — தொன்மை சனாதன வம்சாவளி & பரம்பரை) -->
      <div class="strip-group" data-group="who_we_are">
        <a href="who-we-are.html" class="strip-item" data-tooltip="யார் நாம்? (Who We Are)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></span>
          <span class="strip-item-label">யார் நாம்? (Who We Are)</span>
        </a>
      </div>

    </nav>""".replace('\n', '\r\n').encode('utf-8')
    b_new = b[:idx] + addition + b[idx+len(target):]
    
    footer_tgt = '<li><a href="admissions.html">'.encode('utf-8')
    f_idx = b_new.find(footer_tgt)
    if f_idx != -1:
        f_add = '<li><a href="who-we-are.html">👑 யார் நாம்? (தொன்மை வம்சாவளி &amp; மரபு)</a></li>\r\n          '.encode('utf-8')
        b_new = b_new[:f_idx] + f_add + b_new[f_idx:]
    
    with open('about.html', 'wb') as f:
        f.write(b_new)
    print('Updated about.html successfully!')
