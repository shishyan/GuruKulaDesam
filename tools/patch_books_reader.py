#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch books-reader.js to support window.DEFAULT_GRADE and render Curriculum Media Vault links
"""

READER_JS = r"c:\GitHub\Gurukuladesam\assets\js\books-reader.js"

with open(READER_JS, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update initBookReader to check window.DEFAULT_GRADE
old_init = """async function initBookReader() {
  // Parse URL query params
  const urlParams = new URLSearchParams(window.location.search);
  const gradeParam = parseInt(urlParams.get('grade'));
  const bookParam = urlParams.get('book');
  const chapterParam = parseInt(urlParams.get('chapter'));

  if (gradeParam >= 1 && gradeParam <= 12) currentGrade = gradeParam;"""

new_init = """async function initBookReader() {
  // Parse URL query params
  const urlParams = new URLSearchParams(window.location.search);
  const gradeParam = parseInt(urlParams.get('grade'));
  const bookParam = urlParams.get('book');
  const chapterParam = parseInt(urlParams.get('chapter'));

  if (typeof window.DEFAULT_GRADE === 'number' && window.DEFAULT_GRADE >= 1 && window.DEFAULT_GRADE <= 12) {
    currentGrade = window.DEFAULT_GRADE;
  }
  if (gradeParam >= 1 && gradeParam <= 12) currentGrade = gradeParam;"""

if old_init in code:
    code = code.replace(old_init, new_init, 1)
    print("Patched initBookReader for DEFAULT_GRADE")
else:
    print("Could not find old_init pattern")

# 2. Add curriculum source link generator in renderCurrentChapterContent
old_footer = """      <!-- Navigation Footer (Prev / Next Chapter) -->"""

curriculum_source_code = """      <!-- Curricular Scripture & Media Vault Integration -->
      ${(() => {
        let box = '';
        if (currentBook === 'nallaram') {
          box = `
            <div class="curriculum-source-pill-box" style="background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.35); border-radius:12px; padding:14px 18px; margin:20px 0; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
              <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:1.4rem;">📜</span>
                <div>
                  <strong style="color:#34d399; font-size:0.92rem; display:block;">பாட மூலக் களஞ்சியம்: திருக்குறள் ஆய்வு மையம்</strong>
                  <span style="color:#cbd5e1; font-size:0.82rem;">1330 குறள்கள், இல்லறவியல் மற்றும் திரைப்படக் காட்சிகள்</span>
                </div>
              </div>
              <a href="thirukkural.html" class="sheet-btn" style="font-size:0.82rem; padding:6px 14px; text-decoration:none;">திருக்குறள் காண்க &rarr;</a>
            </div>
          `;
        } else if (currentBook === 'narthunai') {
          let link = 'saiva-neri.html';
          let title = 'சைவ நெறி & 172 திருப்பதிகங்கள்';
          if (currentGrade <= 3) {
            link = 'vinayagar.html'; title = 'விநாயகர் அகவல் & வழிபாடு';
          } else if (currentGrade <= 7) {
            link = 'murugan.html'; title = 'முருகன் திருப்புகழ் & கந்த சஷ்டி';
          }
          box = `
            <div class="curriculum-source-pill-box" style="background:rgba(192,132,252,0.12); border:1px solid rgba(192,132,252,0.35); border-radius:12px; padding:14px 18px; margin:20px 0; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
              <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:1.4rem;">🕉️</span>
                <div>
                  <strong style="color:#c084fc; font-size:0.92rem; display:block;">பாட மூலக் களஞ்சியம்: ${title}</strong>
                  <span style="color:#cbd5e1; font-size:0.82rem;">தேவாரம், பதிகங்கள் மற்றும் ஆலய வழிபாட்டு நெறிமுறைகள்</span>
                </div>
              </div>
              <a href="${link}" class="sheet-btn" style="font-size:0.82rem; padding:6px 14px; text-decoration:none;">வழிபாட்டுக் களம் &rarr;</a>
            </div>
          `;
        } else if (currentBook === 'narchinthanai') {
          let link = (currentGrade >= 11) ? 'about.html' : 'sanmargam.html';
          let title = (currentGrade >= 11) ? 'காஞ்சி மகா பெரியவா அருளுரைகள் (தெய்வத்தின் குரல்)' : 'வள்ளலார் சுத்த சன்மார்க்கம் (திருவருட்பா)';
          box = `
            <div class="curriculum-source-pill-box" style="background:rgba(251,146,60,0.12); border:1px solid rgba(251,146,60,0.35); border-radius:12px; padding:14px 18px; margin:20px 0; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
              <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:1.4rem;">✨</span>
                <div>
                  <strong style="color:#fb923c; font-size:0.92rem; display:block;">பாட மூலக் களஞ்சியம்: ${title}</strong>
                  <span style="color:#cbd5e1; font-size:0.82rem;">மெய்யியல் சிந்தனை மற்றும் ஆன்மநேய ஒருமைப்பாடு</span>
                </div>
              </div>
              <a href="${link}" class="sheet-btn" style="font-size:0.82rem; padding:6px 14px; text-decoration:none;">மெய்யியல் களம் &rarr;</a>
            </div>
          `;
        } else if (currentBook === 'narchol') {
          let link = (currentGrade >= 6) ? 'panpaadu.html' : 'irai-isai-virundhu.html';
          let title = (currentGrade >= 6) ? 'தமிழர் பண்பாடும் 12 மாதத் திருவிழாக்களும்' : 'இறை இசை விருந்து — 5 அமிர்த பண்ணிசைப் பாடல்கள்';
          box = `
            <div class="curriculum-source-pill-box" style="background:rgba(52,211,153,0.12); border:1px solid rgba(52,211,153,0.35); border-radius:12px; padding:14px 18px; margin:20px 0; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
              <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:1.4rem;">🎶</span>
                <div>
                  <strong style="color:#34d399; font-size:0.92rem; display:block;">பாட மூலக் களஞ்சியம்: ${title}</strong>
                  <span style="color:#cbd5e1; font-size:0.82rem;">திருமந்திர நாத யோகம் மற்றும் பண்ணிசைப் பாடல்கள்</span>
                </div>
              </div>
              <a href="${link}" class="sheet-btn" style="font-size:0.82rem; padding:6px 14px; text-decoration:none;">இசைக்களஞ்சியம் &rarr;</a>
            </div>
          `;
        } else if (currentBook === 'narcheyal') {
          box = `
            <div class="curriculum-source-pill-box" style="background:rgba(250,204,21,0.12); border:1px solid rgba(250,204,21,0.35); border-radius:12px; padding:14px 18px; margin:20px 0; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
              <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:1.4rem;">🌿</span>
                <div>
                  <strong style="color:#facc15; font-size:0.92rem; display:block;">பாட மூலக் களஞ்சியம்: இல்லற தர்மம் &amp; சித்தர் வாழ்வியல்</strong>
                  <span style="color:#cbd5e1; font-size:0.82rem;">பஞ்ச மகா யக்ஞ டிராக்கர், குடும்ப சாசனம் &amp; 18 சித்தர் மூலிகைகள்</span>
                </div>
              </div>
              <div style="display:flex; gap:8px;">
                <a href="grihastha.html" class="sheet-btn" style="font-size:0.82rem; padding:6px 12px; text-decoration:none;">இல்லறம்</a>
                <a href="siddha.html" class="sheet-btn" style="font-size:0.82rem; padding:6px 12px; text-decoration:none;">சித்தர் நெறி</a>
              </div>
            </div>
          `;
        }
        return box;
      })()}

      <!-- Navigation Footer (Prev / Next Chapter) -->"""

if old_footer in code:
    code = code.replace(old_footer, curriculum_source_code, 1)
    print("Patched renderCurrentChapterContent with curriculum media links")
else:
    print("Could not find old_footer pattern")

with open(READER_JS, "w", encoding="utf-8") as f:
    f.write(code)
print("Saved books-reader.js successfully.")
