# -*- coding: utf-8 -*-
import os

BANNER_HTML = """    <!-- Online School Academy Flagship Banner -->
    <div style="background: linear-gradient(135deg, rgba(14, 25, 45, 0.95), rgba(15, 23, 42, 0.95)); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 16px; padding: 20px 24px; margin: 20px 0 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
      <div style="max-width: 760px;">
        <div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(56,189,248,0.12); color: #38bdf8; border: 1px solid rgba(56,189,248,0.3); padding: 3px 12px; border-radius: 14px; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">
          <span>🏫 The Vedic-Modern Global Academy</span>
        </div>
        <h3 style="color: #ffffff; font-size: 1.25rem; font-weight: 800; margin-bottom: 4px;">
          குருகுல இணையப் பள்ளி — 21-ஆம் நூற்றாண்டு மாணவர் போர்டல்
        </h3>
        <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.6; margin: 0;">
          வேத மெய்யறிவு, குவாண்டம் அறிவியல், AI நெறிமுறைகள் சங்கமிக்கும் 12 தரப் பாடநெறி, போமோடோரோ படிப்பு அரங்கம் மற்றும் உடனடிப் பட்டயச் சான்றிதழ்.
        </p>
      </div>
      <a href="school.html" class="sheet-btn sheet-btn-view" style="padding: 10px 20px; font-size: 0.9rem; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(56,189,248,0.3);">
        <span>இணையப் பள்ளி காண்க ↗</span>
      </a>
    </div>
"""

def patch_index(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    if 'The Vedic-Modern Global Academy' in text:
        print(f"Already in {path}")
        return

    target = '    <!-- Sacred Authority & Source Foundations -->'
    if target in text:
        text = text.replace(target, BANNER_HTML + '\n' + target)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Patched {path}")
    else:
        print(f"Target not found in {path}")

for p in ['index.html', 'site/index.html', 'docs/index.html']:
    patch_index(p)
