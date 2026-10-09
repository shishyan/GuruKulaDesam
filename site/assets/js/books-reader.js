/**
 * Gurukula Desam - 7 Sacred Ashram Books Digital Reader Engine
 * Supports Grades 1-12, all 7 Books, 7+ Chapters per book, URL deep-linking, Audio TTS
 */

let currentGrade = 1;
let currentBook = 'nanneri';
let currentChapter = 1;
let loadedBookData = {};

const BOOKS_METADATA = [
  { id: 'nanneri', name: 'நன்னெறி', en: 'ஒழுக்கமும் பணிவும்', icon: 'M12 2v3M7 5h10l-1.5 4H8.5L7 5z', color: '#38bdf8' },
  { id: 'nallaram', name: 'நல்லறம்', en: 'ஈகையும் இல்லற தர்மமும்', icon: 'M11 20A7 7 0 0 1 4 13a8.9 8.9 0 0 1 8.2-8.9 7 7 0 0 1 7.8 7.8A8.9 8.9 0 0 1 11 20z', color: '#10b981' },
  { id: 'nalvazhi', name: 'நல்வழி', en: 'வாய்மையும் நேர்மை வழியும்', icon: 'M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z', color: '#facc15' },
  { id: 'narthunai', name: 'நற்துணை', en: 'இறைத்துதியும் சரணாகதியும்', icon: 'M12 2a9.5 9.5 0 0 0-9.5 9.5c0 7 9.5 12.5 9.5 12.5s9.5-5.5 9.5-12.5A9.5 9.5 0 0 0 12 2z', color: '#c084fc' },
  { id: 'narchinthanai', name: 'நற்சிந்தனை', en: 'மெய்யறிவும் தத்துவமும்', icon: 'M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z', color: '#fb923c' },
  { id: 'narchol', name: 'நற்சொல்', en: 'இன்சொல்லும் நாவடக்கமும்', icon: 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z', color: '#34d399' },
  { id: 'narcheyal', name: 'நற்செயல்', en: 'கடமையும் இல்லற வாழ்வியலும்', icon: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z', color: '#ffd700' }
];

async function initBookReader() {
  // Parse URL query params
  const urlParams = new URLSearchParams(window.location.search);
  const gradeParam = parseInt(urlParams.get('grade'));
  const bookParam = urlParams.get('book');
  const chapterParam = parseInt(urlParams.get('chapter'));

  if (typeof window.DEFAULT_GRADE === 'number' && window.DEFAULT_GRADE >= 1 && window.DEFAULT_GRADE <= 12) {
    currentGrade = window.DEFAULT_GRADE;
  }
  if (gradeParam >= 1 && gradeParam <= 12) currentGrade = gradeParam;
  if (bookParam && BOOKS_METADATA.some(b => b.id === bookParam)) currentBook = bookParam;
  if (chapterParam >= 1 && chapterParam <= 7) currentChapter = chapterParam;

  renderGradePills();
  renderBookShelfTabs();
  await loadGradeBookData(currentGrade);
}

function renderGradePills() {
  const container = document.getElementById('gradeSelectorPills');
  if (!container) return;
  // If on a specific grade page, isolate completely and do NOT render other grade pills
  if (typeof window.DEFAULT_GRADE === 'number') {
    container.style.display = 'none';
    const parentHeading = container.previousElementSibling;
    if (parentHeading && parentHeading.innerText.includes('வகுப்பைத் தேர்வு செய்க')) {
      parentHeading.style.display = 'none';
    }
    return;
  }
  let html = '';
  for (let g = 1; g <= 12; g++) {
    const activeClass = (g === currentGrade) ? 'active' : '';
    html += `<button type="button" class="book-grade-btn ${activeClass}" onclick="switchGrade(${g})">தரம் ${g}</button>`;
  }
  container.innerHTML = html;
}

function renderBookShelfTabs() {
  const container = document.getElementById('booksShelfTabs');
  if (!container) return;
  let html = '';
  BOOKS_METADATA.forEach((book, idx) => {
    const activeClass = (book.id === currentBook) ? 'active' : '';
    html += `
      <button type="button" class="shelf-book-btn ${activeClass}" onclick="switchBook('${book.id}')" style="--book-accent:${book.color};">
        <span class="shelf-book-num">நூல் ${idx + 1}</span>
        <span class="shelf-book-title">${book.name}</span>
        <span class="shelf-book-en">${book.en}</span>
      </button>
    `;
  });
  container.innerHTML = html;
}

async function loadGradeBookData(grade) {
  const readerArea = document.getElementById('activeChapterReadingArea');
  if (readerArea) {
    readerArea.innerHTML = `<div style="text-align:center; padding:40px; color:var(--gold);"><span class="spinner"></span> பாடநூல் தரவுகள் ஏற்றப்படுகின்றன...</div>`;
  }

  try {
    const resp = await fetch(`data/books/grade_${grade}.json`);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    loadedBookData = await resp.json();
    renderCurrentBook();
  } catch (err) {
    console.warn(`Could not load data/books/grade_${grade}.json:`, err);
    renderFallbackBook();
  }
}

function switchGrade(grade) {
  currentGrade = grade;
  currentChapter = 1;
  renderGradePills();
  updateUrlParams();
  loadGradeBookData(grade);
}

function switchBook(bookId) {
  currentBook = bookId;
  currentChapter = 1;
  renderBookShelfTabs();
  updateUrlParams();
  renderCurrentBook();
}

function switchChapter(chapNum) {
  currentChapter = chapNum;
  updateUrlParams();
  renderCurrentChapterContent();
}

function updateUrlParams() {
  const newUrl = `${window.location.pathname}?grade=${currentGrade}&book=${currentBook}&chapter=${currentChapter}`;
  window.history.replaceState({}, '', newUrl);
}

function renderCurrentBook() {
  const book = loadedBookData?.books?.[currentBook];
  if (!book) {
    renderFallbackBook();
    return;
  }

  // Update Book Title Header
  const titleEl = document.getElementById('readerBookTitle');
  const subEl = document.getElementById('readerBookSubtitle');
  const badgeEl = document.getElementById('readerBookBadge');
  const litEl = document.getElementById('readerLiteratureBase');

  if (titleEl) titleEl.innerText = book.title;
  if (subEl) subEl.innerText = book.tagline || book.englishTitle;
  if (badgeEl) badgeEl.innerText = `தரம் ${currentGrade} • ${loadedBookData.phase || ''}`;
  if (litEl) litEl.innerText = `இலக்கிய அடித்தளம்: ${loadedBookData.literatureBase || ''} • மூலம்: ${book.source || ''}`;

  // Render Chapter Tabs (1 to 7)
  const tabsContainer = document.getElementById('readerChapterTabs');
  if (tabsContainer && book.chapters) {
    let tabsHtml = '';
    book.chapters.forEach((chap, idx) => {
      const num = chap.chapterNumber || (idx + 1);
      const activeClass = (num === currentChapter) ? 'active' : '';
      tabsHtml += `
        <button type="button" class="reader-chap-btn ${activeClass}" onclick="switchChapter(${num})">
          <span class="chap-badge">அத் ${num}</span>
          <span class="chap-btn-title">${chap.title}</span>
        </button>
      `;
    });
    tabsContainer.innerHTML = tabsHtml;
  }

  renderCurrentChapterContent();
}

function renderCurrentChapterContent() {
  const book = loadedBookData?.books?.[currentBook];
  if (!book || !book.chapters) return;

  const chap = book.chapters.find(c => c.chapterNumber === currentChapter) || book.chapters[0];
  const container = document.getElementById('activeChapterReadingArea');
  if (!container || !chap) return;

  // Highlight active tab
  document.querySelectorAll('.reader-chap-btn').forEach(btn => {
    const text = btn.innerText;
    if (text.includes(`அத் ${chap.chapterNumber}`)) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });

  const totalChapters = book.chapters.length;
  const prevNum = (currentChapter > 1) ? currentChapter - 1 : null;
  const nextNum = (currentChapter < totalChapters) ? currentChapter + 1 : null;

  const images = chap.images || [];
  window.currentChapterImages = images;
  window.currentActiveImageIdx = 0;

  // Build Carousel HTML
  let carouselHtml = '';
  if (images.length > 0) {
    const img0 = images[0];
    let thumbsHtml = '';
    images.forEach((img, idx) => {
      thumbsHtml += `
        <button type="button" class="carousel-thumb-btn ${idx === 0 ? 'active' : ''}" id="chapThumb_${idx}" onclick="switchChapterImage(${idx})" title="${img.typeTitle}: ${img.caption}">
          <span class="thumb-num-badge">${idx + 1}</span>
          <img src="${img.url}" alt="${img.caption}" loading="lazy">
        </button>
      `;
    });

    carouselHtml = `
      <div class="chapter-visuals-panel">
        <div class="carousel-top-bar">
          <div class="carousel-heading">
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
            7 அத்தியாயக் காட்சிகள் (Chapter Visual Gallery)
          </div>
          <span class="carousel-counter-pill" id="carouselCounterBadge">காட்சி 1 / ${images.length} • ${img0.typeTitle}</span>
        </div>

        <div class="carousel-stage" id="carouselStage">
          <button type="button" class="carousel-nav-btn carousel-prev-btn" onclick="event.stopPropagation(); prevChapterImage()" aria-label="முந்தைய காட்சி">
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          </button>
          <img id="carouselMainImg" src="${img0.url}" alt="${img0.caption}" onclick="openArtLightboxByIndex(window.currentActiveImageIdx || 0)" title="பெரிதாகக் காண கிளிக் செய்க">
          <button type="button" class="carousel-nav-btn carousel-next-btn" onclick="event.stopPropagation(); nextChapterImage()" aria-label="அடுத்த காட்சி">
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </button>
          <div class="carousel-overlay-caption" id="carouselCaptionBox" onclick="openArtLightboxByIndex(window.currentActiveImageIdx || 0)">
            <span class="carousel-caption-tag" id="carouselCaptionTag">${img0.typeTitle}</span>
            <div class="carousel-caption-text" id="carouselCaptionText">${img0.caption}</div>
          </div>
        </div>

        <div class="carousel-thumbs-row">
          ${thumbsHtml}
        </div>
      </div>
    `;
  }

  container.innerHTML = `
    <article class="reading-chapter-card">
      <div class="chap-read-header">
        <div>
          <span class="chap-num-tag">அத்தியாயம் ${chap.chapterNumber} / ${totalChapters}</span>
          <h2 class="chap-read-title">${chap.title}</h2>
        </div>
        <button type="button" class="lesson-speech-btn" id="lessonSpeechBtn" onclick="readAloudChapter()" title="குரல்வழிக் கேட்க">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>
          <span>அத்தியாயம் கேட்க</span>
        </button>
      </div>

      <!-- 7 Sub-Chapters Interactive Jump Bar (பாட உட்பிரிவுகள்) -->
      <nav class="subchapter-nav-strip" aria-label="அத்தியாய உட்பிரிவுகள்">
        ${images.length > 0 ? `<a href="#subchap-visuals" class="subchap-pill-btn"><span class="subchap-icon">🎨</span><span>1. காட்சிகள்</span></a>` : ''}
        <a href="#subchap-verse" class="subchap-pill-btn"><span class="subchap-icon">📜</span><span>2. மூலப் பாடல்</span></a>
        <a href="#subchap-exposition" class="subchap-pill-btn"><span class="subchap-icon">📖</span><span>3. விரிவுரை</span></a>
        <a href="#subchap-story" class="subchap-pill-btn"><span class="subchap-icon">🪔</span><span>4. மெய்ஞ்ஞானக் கதை</span></a>
        <a href="#subchap-life" class="subchap-pill-btn"><span class="subchap-icon">🌿</span><span>5. இல்லற நடைமுறை</span></a>
        <a href="#subchap-exercise" class="subchap-pill-btn"><span class="subchap-icon">☀️</span><span>6. சாதனா பயிற்சி</span></a>
        <a href="#subchap-media" class="subchap-pill-btn"><span class="subchap-icon">🎵</span><span>7. பாட இசை &amp; படம்</span></a>
        <a href="#subchap-mastery" class="subchap-pill-btn"><span class="subchap-icon">🏆</span><span>8. நிறைவு &amp; தேர்வு</span></a>
      </nav>

      <!-- 1. Chapter Visuals Carousel Gallery -->
      <div id="subchap-visuals" style="scroll-margin-top: 90px;">
        ${carouselHtml}
      </div>

      <!-- 2. Sacred Verse Block (Zero-Wrapper & Deep Shadow) -->
      <div id="subchap-verse" class="verse-callout-clean" style="scroll-margin-top: 90px; padding: 10px 0 16px 0; margin-bottom: 22px;">
        <div style="font-size:0.8rem; font-weight:700; color:var(--gold); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px; text-shadow:0 1px 3px rgba(0,0,0,0.95);">மூலப் பாடல் / சூத்திரம் (Sacred Verse):</div>
        <div class="verse-text-sacred" style="font-size:1.22rem; font-weight:700; color:#ffffff; line-height:1.6; font-family:'Mukta Malar', serif; text-shadow:0 2px 8px rgba(0,0,0,0.98);">${chap.verse}</div>
        <div class="verse-meaning-clean" style="color:#cbd5e1; font-size:0.95rem; margin-top:10px; line-height:1.6; text-shadow:0 1px 3px rgba(0,0,0,0.95);">
          <strong style="color:var(--gold-soft);">பொருள் விளக்கம்:</strong> ${chap.verseMeaning}
        </div>
        <div class="moola-reader-actions-row" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-top:14px; padding-top:10px;">
          <button type="button" class="sheet-btn" onclick="openChapterMoolaModal('${currentBook}', ${chap.chapterNumber}, ${currentGrade})" style="font-size:0.82rem; padding:6px 12px; cursor:pointer;">
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:13px; height:13px;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg> 📖 மூல நூல் &amp; பதவுரை காண்க
          </button>
          <a href="moola-nool.html" class="moola-canon-link" target="_blank" title="முழு மூல நூலகத்தில் திறக்க" style="color:#38bdf8; text-decoration:none; font-size:0.82rem;">
            மூல நூல் நூலகம் &rarr;
          </a>
        </div>
      </div>

      <!-- 3. Philosophical Exposition (Zero-Wrapper) -->
      <div id="subchap-exposition" class="reading-section-block" style="scroll-margin-top: 90px;">
        <h4 style="color:#38bdf8; font-size:1.1rem; font-weight:700; margin:0 0 10px 0; display:flex; align-items:center; gap:8px; text-shadow:0 1px 4px rgba(0,0,0,0.98);">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
          விரிவுரை &amp; தத்துவ உரை (Philosophical Exposition)
        </h4>
        <div style="color:#e2e8f0; font-size:0.96rem; line-height:1.8; margin-bottom:12px; text-shadow:0 1px 3px rgba(0,0,0,0.95);">
          ${chap.exposition}
        </div>
      </div>

      <!-- 4. Puranic / Itihasic Narrative Story (Zero-Wrapper) -->
      <div id="subchap-story" class="reading-section-block story-block" style="scroll-margin-top: 90px; padding:10px 0; margin-bottom:20px;">
        <h4 style="color:var(--gold-bright); font-size:1.1rem; font-weight:700; margin:0 0 8px 0; display:flex; align-items:center; gap:8px; text-shadow:0 1px 4px rgba(0,0,0,0.98);">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8"/></svg>
          மெய்ஞ்ஞானக் கதை / அற உருவகம் (Narrative Illustration)
        </h4>
        <div style="color:#cbd5e1; font-size:0.95rem; line-height:1.8; margin:12px 0; text-shadow:0 1px 3px rgba(0,0,0,0.95);">
          ${chap.story}
        </div>
      </div>

      <!-- 5. Life Application & Householder Dharma (Zero-Wrapper) -->
      <div id="subchap-life" class="reading-section-block" style="scroll-margin-top: 90px; padding:10px 0; margin-bottom:20px;">
        <h4 style="color:#34d399; font-size:1.1rem; font-weight:700; margin:0 0 8px 0; display:flex; align-items:center; gap:8px; text-shadow:0 1px 4px rgba(0,0,0,0.98);">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 4 13a8.9 8.9 0 0 1 8.2-8.9 7 7 0 0 1 7.8 7.8A8.9 8.9 0 0 1 11 20z"/><path d="M12.5 4.5c.5 4.5-1 7.5-5 9.5"/></svg>
          இல்லற &amp; அன்றாட வாழ்வியல் நடைமுறை (Practical Application: 3 Ds)
        </h4>
        <div style="color:#e2e8f0; font-size:0.94rem; line-height:1.7; text-shadow:0 1px 3px rgba(0,0,0,0.95);">
          ${chap.lifeApplication}
        </div>
      </div>

      <!-- 6. Sadhana Exercise & Contemplative Question (Zero-Wrapper) -->
      <div id="subchap-exercise" class="reading-section-block" style="scroll-margin-top: 90px; padding:10px 0; margin-bottom:24px;">
        <h4 style="color:#facc15; font-size:1.1rem; font-weight:700; margin:0 0 8px 0; display:flex; align-items:center; gap:8px; text-shadow:0 1px 4px rgba(0,0,0,0.98);">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
          சாதனா பயிற்சி &amp; சிந்தனை வினாக்கள் (Sadhana Exercise)
        </h4>
        <div style="color:#e2e8f0; font-size:0.94rem; line-height:1.7; text-shadow:0 1px 3px rgba(0,0,0,0.95);">
          ${chap.exercise}
        </div>
      </div>

      <!-- 7. Curricular Integrated Media Player (பாட இசை & காணொளிக் களம்) -->
      <div id="subchap-media" style="scroll-margin-top: 90px;">
        ${renderCurriculumMediaSection(currentGrade, currentBook, chap.chapterNumber)}
      </div>

      <!-- 8. Student Chapter Mastery, LMS Completion & Self-Check Deck -->
      <div id="subchap-mastery" style="scroll-margin-top: 90px;">
        ${renderStudentChapterDeck(currentGrade, currentBook, chap)}
      </div>

      <!-- Navigation Footer (Prev / Next Chapter) -->
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-top:20px; padding-top:16px;">
        ${prevNum ? `<button type="button" class="sheet-btn" onclick="switchChapter(${prevNum})" style="cursor:pointer;"><svg class="gkd-icon gkd-arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg> முந்தைய அத்தியாயம் (${prevNum})</button>` : '<div></div>'}
        <span style="color:#94a3b8; font-size:0.85rem; text-shadow:0 1px 3px rgba(0,0,0,0.95);">அத்தியாயம் ${chap.chapterNumber} / ${totalChapters}</span>
        ${nextNum ? `<button type="button" class="sheet-btn sheet-btn-view" onclick="switchChapter(${nextNum})" style="cursor:pointer;">அடுத்த அத்தியாயம் (${nextNum}) <svg class="gkd-icon gkd-arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></button>` : `<a href="tharam-${currentGrade}.html" class="sheet-btn sheet-btn-view">வகுப்புப் பாடங்களுக்குத் திரும்புக <svg class="gkd-icon gkd-external-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg></a>`}
      </div>
    </article>
  `;
}

// Curricular Media Integrator (பாட இசை & காணொளிக் களம்)
function getCurriculumMediaForChapter(grade, bookKey, chapterNum) {
  const cat = window.GURUKULA_CATALOG;
  if (!cat) return null;

  if (bookKey === 'nallaram' || bookKey === 'nalvazhi') {
    if (cat.thirukkural && cat.thirukkural.length > 0) {
      const idx = (grade * 7 + chapterNum * 3) % cat.thirukkural.length;
      return cat.thirukkural[idx];
    }
  }

  if (bookKey === 'narthunai') {
    if (grade <= 3) {
      if (chapterNum === 1 && cat.vinayagar && cat.vinayagar.length > 0) return cat.vinayagar[0];
      if (chapterNum === 2 && cat.murugan && cat.murugan.length > 0) return cat.murugan[0];
      if (chapterNum === 3 && cat.shiva && cat.shiva.length > 0) return cat.shiva[0];
      if (chapterNum === 4 && cat.amman && cat.amman.length > 0) return cat.amman[0];
      if (chapterNum === 5 && cat.vishnu_krishna && cat.vishnu_krishna.length > 0) return cat.vishnu_krishna[0];
      if (chapterNum === 6 && cat.murugan && cat.murugan.length > 1) return cat.murugan[1];
      if (chapterNum === 7 && cat.shiva && cat.shiva.length > 1) return cat.shiva[1];
    } else if (grade <= 8) {
      if (chapterNum % 4 === 1 && cat.shiva) return cat.shiva[(grade * 5 + chapterNum) % cat.shiva.length];
      if (chapterNum % 4 === 2 && cat.murugan) return cat.murugan[(grade * 3 + chapterNum) % cat.murugan.length];
      if (chapterNum % 4 === 3 && cat.amman) return cat.amman[(grade * 2 + chapterNum) % cat.amman.length];
      if (chapterNum % 4 === 0 && cat.vishnu_krishna) return cat.vishnu_krishna[(grade * 2 + chapterNum) % cat.vishnu_krishna.length];
    } else {
      if (cat.shiva) return cat.shiva[(grade * 7 + chapterNum) % cat.shiva.length];
    }
  }

  if (bookKey === 'narchinthanai') {
    if (cat.vallalar_cultural && cat.vallalar_cultural.length > 0) {
      const idx = (grade * 4 + chapterNum) % cat.vallalar_cultural.length;
      return cat.vallalar_cultural[idx];
    }
  }

  if (bookKey === 'narchol') {
    if (cat.shiva && cat.shiva.length > 0) {
      const idx = (chapterNum * 5) % cat.shiva.length;
      return cat.shiva[idx];
    }
  }

  if (cat.vallalar_cultural && cat.vallalar_cultural.length > 0) {
    const idx = (grade * 6 + chapterNum) % cat.vallalar_cultural.length;
    return cat.vallalar_cultural[idx];
  } else if (cat.thirukkural && cat.thirukkural.length > 0) {
    const idx = (grade * 3 + chapterNum) % cat.thirukkural.length;
    return cat.thirukkural[idx];
  }

  return null;
}

function renderCurriculumMediaSection(grade, bookKey, chapterNum) {
  const mediaItem = getCurriculumMediaForChapter(grade, bookKey, chapterNum);
  if (!mediaItem) return '';

  const cleanTitle = (mediaItem.title || '').replace(/'/g, "\\'");
  const hasLyrics = Boolean(mediaItem.lyrics);
  const hasMeaning = Boolean(mediaItem.meaning);

  return `
    <div class="reading-section-block chapter-media-card">
      <div class="chapter-media-header">
        <div class="chapter-media-title">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8"/></svg>
          <span>பாட இசை &amp; காணொளிக் களம் (Lesson Sacred Song &amp; Film)</span>
        </div>
        <span class="chap-badge" style="font-size:0.75rem;">பாட ஆதாரக் களஞ்சியம்</span>
      </div>
      <div style="color:#ffffff; font-weight:700; font-size:1.05rem; margin-bottom:6px; text-shadow:0 1px 4px rgba(0,0,0,0.98);">
        ${mediaItem.title}
      </div>
      <div style="color:#94a3b8; font-size:0.85rem; margin-bottom:12px; text-shadow:0 1px 3px rgba(0,0,0,0.95);">
        ஆசிரியர்: ${mediaItem.author || 'குருகுல மரபு'} • மூலம்: ${mediaItem.source || 'ஆசிரம வெளியீடு'}
      </div>
      <div class="chapter-media-player-wrap">
        <iframe src="https://www.youtube-nocookie.com/embed/${mediaItem.id}?rel=0" title="${mediaItem.title}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      </div>
      <div class="chapter-media-info">
        ${(hasLyrics || hasMeaning) ? `
          <button type="button" class="sheet-btn" onclick="toggleChapterLyrics('${mediaItem.id}')" style="font-size:0.82rem; padding:6px 14px; cursor:pointer;">
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3H4a2 2 0 0 0-2 2v13a3 3 0 0 0 3 3h13a3 3 0 0 0 3-3V5a2 2 0 0 0-2-2h-7"/><path d="M19 18a3 3 0 0 0 0-6H6a2 2 0 0 0 0 4h12"/><line x1="8" y1="7" x2="14" y2="7"/></svg>
            <span>வரிகள் &amp; பொருள் காண்க</span>
          </button>
        ` : ''}
        ${(typeof window.openPlayer === 'function') ? `
          <button type="button" class="sheet-btn sheet-btn-view" onclick="openPlayer('${mediaItem.id}', '${cleanTitle}')" style="font-size:0.82rem; padding:6px 14px; cursor:pointer;">
            <span>சினிமா தியேட்டர் முழுத்திரை &rarr;</span>
          </button>
        ` : ''}
      </div>
      <div class="chapter-media-lyrics-drawer" id="chapLyrics_${mediaItem.id}" style="display:none;">
        ${hasLyrics ? `<div style="margin-bottom:12px;"><strong style="color:var(--gold-soft); display:block; margin-bottom:4px;">பாடல் வரிகள்:</strong><div style="line-height:1.7;">${mediaItem.lyrics}</div></div>` : ''}
        ${hasMeaning ? `<div><strong style="color:#38bdf8; display:block; margin-bottom:4px;">உரை விளக்கம்:</strong><div style="line-height:1.7;">${mediaItem.meaning}</div></div>` : ''}
      </div>
    </div>
  `;
}

window.toggleChapterLyrics = function(id) {
  const el = document.getElementById('chapLyrics_' + id);
  if (!el) return;
  el.style.display = (el.style.display === 'none' || !el.style.display) ? 'block' : 'none';
};

// ==========================================================================
// STUDENT CHAPTER MASTERY, LMS COMPLETION & INTERACTIVE SELF-CHECK ENGINE
// ==========================================================================

function isBookChapterCompleted(grade, bookKey, chapterNum) {
  try {
    return localStorage.getItem(`gkd_completed_${grade}_${bookKey}_${chapterNum}`) === 'true' ||
           localStorage.getItem(`gkd_completed_${grade}_${chapterNum}`) === 'true';
  } catch (e) {
    return false;
  }
}

window.toggleBookChapterCompletion = function(grade, bookKey, chapterNum) {
  try {
    const key = `gkd_completed_${grade}_${bookKey}_${chapterNum}`;
    const legacyKey = `gkd_completed_${grade}_${chapterNum}`;
    const isDone = isBookChapterCompleted(grade, bookKey, chapterNum);
    const newState = !isDone;

    if (newState) {
      localStorage.setItem(key, 'true');
      localStorage.setItem(legacyKey, 'true');
      if (typeof window.playTempleBell === 'function') {
        window.playTempleBell();
      }
      if (typeof window.showToast === 'function') {
        window.showToast(`தரம் ${grade} • அத்தியாயம் ${chapterNum} வாசித்து உணரப்பட்டது.`);
      }
    } else {
      localStorage.removeItem(key);
      localStorage.removeItem(legacyKey);
      if (typeof window.showToast === 'function') {
        window.showToast('பாடப் பதிவு மீட்டமைக்கப்பட்டது.');
      }
    }

    const btn = document.getElementById('chapterLmsBtn');
    if (btn) {
      if (newState) {
        btn.classList.add('completed');
        btn.innerHTML = `<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> <span>பாடம் வாசித்து உணரப்பட்டது (Contemplated)</span>`;
      } else {
        btn.classList.remove('completed');
        btn.innerHTML = `<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg> <span>நான் இப்பாடத்தை முழுமையாக வாசித்து உணர்ந்தேன்</span>`;
      }
    }
  } catch (err) {
    console.error('Error toggling chapter completion:', err);
  }
};

function getChapterQuizData(grade, bookKey, chap) {
  const title = chap.title || 'இப்பாடம்';
  const verseMeaning = chap.verseMeaning || '';

  let question = `இப்பாடத்தின் (${title}) முக்கிய தத்துவக் கருத்து அல்லது வாழ்வியல் ஒழுக்கம் யாது?`;
  let optCorrect = `${verseMeaning.slice(0, 70)}... வழிநடக்கும் மெய்யொழுக்கம்.`;
  if (optCorrect.length < 25) optCorrect = 'பெரியோரை மதித்து, கடமையை செவ்வனே ஆற்றி நற்பெயர் பெறுதல்.';
  let optWrong1 = 'சக மனிதர்களைப் பொருட்படுத்தாமல் சுயநலத்துடன் செயல்படுதல்.';
  let optWrong2 = 'தவறுகளை மறைத்து வாய்மையற்ற வழிகளில் செல்வது.';

  if (bookKey === 'nanneri') {
    question = `நன்னெறி அத்தியாயம் '${title}' நமக்கு உணர்த்தும் முதன்மை அறம் எது?`;
    optCorrect = 'பணிவு, பெரியோர் மரியாதை மற்றும் தூய உள்ளத்தோடு அறம் செய்தல்.';
    optWrong1 = 'பிறர் குறைகளைத் தேடிப் பேசுதல் மற்றும் ஆணவம் கொள்ளுதல்.';
    optWrong2 = 'தன் நலனை மட்டுமே பெரிதாக எண்ணி வாழ்வது.';
  } else if (bookKey === 'nallaram') {
    question = `நல்லறம் அத்தியாயம் '${title}' வலியுறுத்தும் இல்லற நெறிமுறை என்ன?`;
    optCorrect = 'ஜீவகாருண்யம், விருந்தோம்பல் மற்றும் ஏழைகளுக்குப் பகிர்ந்தளித்தல்.';
    optWrong1 = 'ஈகைக் குணம் இன்றிப் பொருளை மட்டுமே சேர்த்து வைத்தல்.';
    optWrong2 = 'குடும்பப் பொறுப்புகளைத் துறந்து சோம்பலில் இருத்தல்.';
  } else if (bookKey === 'nalvazhi') {
    question = `நல்வழி அத்தியாயம் '${title}' காட்டும் நேரிய பாதை யாது?`;
    optCorrect = 'வாய்மை, கடின உழைப்பு மற்றும் சோதனைகளிலும் தர்மத்தைக் கைவிடாமை.';
    optWrong1 = 'பொய் கூறி குறுக்கு வழியில் தற்காலிக வெற்றி தேடுதல்.';
    optWrong2 = 'விதியை மட்டுமே நம்பி முயற்சியைக் கைவிடுதல்.';
  } else if (bookKey === 'narthunai') {
    question = `நற்துணை அத்தியாயம் '${title}' வழங்கும் ஆன்மீகத் துணிவு எது?`;
    optCorrect = 'இறைத் திருவருளைச் சரணடைந்து பயமின்றி தர்மத்தை நிலைநாட்டுதல்.';
    optWrong1 = 'கடவுள் நம்பிக்கையின்றி மன அழுத்தத்திற்கு ஆளாதல்.';
    optWrong2 = 'சடங்குகளை மட்டுமே செய்து உள்ளத்தில் தூய்மையற்றிருத்தல்.';
  } else if (bookKey === 'narchinthanai') {
    question = `நற்சிந்தனை அத்தியாயம் '${title}' எழுப்பும் மெய்யறிவுத் தூண்டல் என்ன?`;
    optCorrect = 'மனதை ஒருமுகப்படுத்தி, பிரபஞ்ச உண்மைகளையும் அறிவியல் சங்கமத்தையும் ஆய்ந்தறிதல்.';
    optWrong1 = 'ஆராயாமல் குருட்டுத்தனமாக எல்லாவற்றையும் நம்புதல்.';
    optWrong2 = 'எதிர்மறை எண்ணங்களை மனதில் வளர்த்து அமைதியிழத்தல்.';
  } else if (bookKey === 'narchol') {
    question = `நற்சொல் அத்தியாயம் '${title}' கற்பிக்கும் வாக்கின் வலிமை யாது?`;
    optCorrect = 'இனிய சொல் பேசுதல், புண்படுத்தாமை மற்றும் மந்திர ஒலி அதிர்வுகளின் மேன்மை.';
    optWrong1 = 'கடுஞ்சொற்கள் பேசி மற்றவர் மனதை நோகடித்தல்.';
    optWrong2 = 'பயனற்ற வீண் பேச்சுகளில் காலத்தை வீணடித்தல்.';
  } else if (bookKey === 'narcheyal') {
    question = `நற்செயல் அத்தியாயம் '${title}' போதிக்கும் 3 Ds செயல்முறை என்ன?`;
    optCorrect = 'கடமை (Duty), கட்டுப்பாடு (Discipline), கண்ணியம் (Dignity) உடன் சேவை செய்தல்.';
    optWrong1 = 'விதிமுறைகளை மீறி தன்னிச்சையாகச் செயல்படுவது.';
    optWrong2 = 'செயலில் முனைப்பின்றி ஒத்திப்போடும் மனப்பான்மை.';
  }

  return {
    q: question,
    options: [
      { text: optCorrect, correct: true, exp: 'சரியான விடை! இப்பாடத்தின் மெய்யறிவுச் சாரம் இதுவே.' },
      { text: optWrong1, correct: false, exp: 'தவறான விடை! மீண்டும் ஒருமுறை மூலப்பாடலை வாசித்து சிந்தியுங்கள்.' },
      { text: optWrong2, correct: false, exp: 'தவறான விடை! இப்பாடம் போதிக்கும் தர்ம நெறியை மீண்டும் அறியவும்.' }
    ]
  };
}

window.checkChapterQuizAnswer = function(btn, isCorrect, exp) {
  const parent = btn.closest('.chapter-quiz-wrap');
  if (!parent) return;
  const fb = parent.querySelector('.chapter-quiz-feedback');
  const allBtns = parent.querySelectorAll('.chapter-quiz-opt');

  allBtns.forEach(b => {
    b.disabled = true;
    b.style.pointerEvents = 'none';
  });

  if (isCorrect) {
    btn.classList.add('opt-correct');
    if (fb) {
      fb.style.display = 'block';
      fb.style.background = 'rgba(16, 185, 129, 0.2)';
      fb.style.color = '#6ee7b7';
      fb.style.border = '1px solid #10b981';
      fb.innerHTML = `✨ <strong>அற்புதம்!</strong> ${exp}`;
    }
    if (typeof window.playTempleBell === 'function') {
      window.playTempleBell();
    }
  } else {
    btn.classList.add('opt-wrong');
    if (fb) {
      fb.style.display = 'block';
      fb.style.background = 'rgba(239, 68, 68, 0.2)';
      fb.style.color = '#fca5a5';
      fb.style.border = '1px solid #ef4444';
      fb.innerHTML = `⚠️ ${exp}`;
    }
    setTimeout(() => {
      allBtns.forEach(b => {
        b.disabled = false;
        b.style.pointerEvents = 'auto';
        b.classList.remove('opt-wrong');
      });
    }, 2000);
  }
};

window.saveStudentChapterNote = function(grade, bookKey, chapterNum, text) {
  try {
    const key = `gkd_note_${grade}_${bookKey}_${chapterNum}`;
    localStorage.setItem(key, text);
    const ind = document.getElementById('chapterNoteSavedBadge');
    if (ind) {
      ind.style.display = 'inline-block';
      setTimeout(() => { ind.style.display = 'none'; }, 2000);
    }
  } catch (e) {
    console.warn('Note save error:', e);
  }
};

window.printLessonHandout = function() {
  window.print();
};

function renderStudentChapterDeck(grade, bookKey, chap) {
  const isDone = isBookChapterCompleted(grade, bookKey, chap.chapterNumber);
  const quiz = getChapterQuizData(grade, bookKey, chap);
  const noteKey = `gkd_note_${grade}_${bookKey}_${chap.chapterNumber}`;
  const savedNote = localStorage.getItem(noteKey) || '';

  const optsHtml = quiz.options.map((opt, idx) => `
    <button type="button" class="chapter-quiz-opt" onclick="checkChapterQuizAnswer(this, ${opt.correct}, '${opt.exp.replace(/'/g, "\\'")}')">
      <span style="font-weight:700; color:var(--gold);">${String.fromCharCode(65 + idx)}.</span>
      <span>${opt.text}</span>
    </button>
  `).join('');

  return `
    <div class="student-chapter-deck" id="studentMasteryDeck">
      <div class="student-deck-header">
        <div class="student-deck-title">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          <span>அத்தியாய நிறைவு &amp; தர்ம சிந்தனை (Chapter Contemplation &amp; Reflection)</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <button type="button" class="sheet-btn" onclick="printLessonHandout()" title="இப்பாடத்தை அச்சிடுக" style="font-size:0.82rem; padding:6px 14px;">
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
            <span>பாட அச்சுத்தாள் (Print Handout)</span>
          </button>
        </div>
      </div>

      <!-- Mark as Read / Completed Button -->
      <div style="margin: 14px 0 18px; display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
        <button type="button" id="chapterLmsBtn" class="chapter-lms-btn ${isDone ? 'completed' : ''}" onclick="toggleBookChapterCompletion(${grade}, '${bookKey}', ${chap.chapterNumber})">
          ${isDone ? `
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            <span>பாடம் வாசித்து உணரப்பட்டது (Contemplated)</span>
          ` : `
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>
            <span>நான் இப்பாடத்தை முழுமையாக வாசித்து உணர்ந்தேன்</span>
          `}
        </button>
        <span style="font-size:0.84rem; color:#94a3b8; text-shadow:0 1px 3px #000;">
          அத்தியாயத்தை முழுமையாக வாசித்து உள்ளத்தில் நிறுத்திய பின் இக்குறிப்பை உறுதிசெய்க.
        </span>
      </div>

      <!-- Contemplative Self-Check -->
      <div class="chapter-quiz-wrap">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <span style="font-size:0.82rem; font-weight:700; color:#38bdf8; text-transform:uppercase; letter-spacing:0.5px;">அறச்சிந்தனைத் தெளிவு (Contemplative Self-Inquiry):</span>
        </div>
        <div class="chapter-quiz-q">${quiz.q}</div>
        <div class="chapter-quiz-opts">
          ${optsHtml}
        </div>
        <div class="chapter-quiz-feedback"></div>
      </div>

      <!-- Student Sadhana Reflection Notes -->
      <div class="chapter-note-box">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
          <label style="font-size:0.85rem; font-weight:700; color:#cbd5e1; text-shadow:0 1px 3px #000;">
            📝 மாணவரின் தர்ம சங்கற்பக் குறிப்பு (Student's Sacred Reflection &amp; Daily Resolve):
          </label>
          <span id="chapterNoteSavedBadge" style="display:none; font-size:0.78rem; color:#34d399; font-weight:700;">✓ சேமிக்கப்பட்டது</span>
        </div>
        <textarea class="chapter-note-textarea" placeholder="இப்பாடத்தின் மூலம் நான் மேற்கொண்ட உறுதிமொழி அல்லது குறிப்பு..." oninput="saveStudentChapterNote(${grade}, '${bookKey}', ${chap.chapterNumber}, this.value)">${savedNote}</textarea>
      </div>
    </div>
  `;
}

// Carousel Interactive Controls
window.switchChapterImage = function(idx) {
  const images = window.currentChapterImages || [];
  if (!images || idx < 0 || idx >= images.length) return;
  window.currentActiveImageIdx = idx;

  const img = images[idx];
  const mainImg = document.getElementById('carouselMainImg');
  const badge = document.getElementById('carouselCounterBadge');
  const tag = document.getElementById('carouselCaptionTag');
  const text = document.getElementById('carouselCaptionText');

  if (mainImg) {
    mainImg.style.opacity = '0.4';
    setTimeout(() => {
      mainImg.src = img.url;
      mainImg.alt = img.caption;
      mainImg.style.opacity = '1';
    }, 150);
  }
  if (badge) badge.innerText = `காட்சி ${idx + 1} / ${images.length} • ${img.typeTitle}`;
  if (tag) tag.innerText = img.typeTitle;
  if (text) text.innerText = img.caption;

  // Update active thumbnail
  document.querySelectorAll('.carousel-thumb-btn').forEach((btn, bIdx) => {
    if (bIdx === idx) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });
};

window.nextChapterImage = function() {
  const images = window.currentChapterImages || [];
  if (!images || images.length === 0) return;
  let nextIdx = (window.currentActiveImageIdx || 0) + 1;
  if (nextIdx >= images.length) nextIdx = 0;
  window.switchChapterImage(nextIdx);
};

window.prevChapterImage = function() {
  const images = window.currentChapterImages || [];
  if (!images || images.length === 0) return;
  let prevIdx = (window.currentActiveImageIdx || 0) - 1;
  if (prevIdx < 0) prevIdx = images.length - 1;
  window.switchChapterImage(prevIdx);
};

function renderFallbackBook() {
  const container = document.getElementById('activeChapterReadingArea');
  if (!container) return;
  const meta = BOOKS_METADATA.find(b => b.id === currentBook) || BOOKS_METADATA[0];

  container.innerHTML = `
    <article class="reading-chapter-card" style="text-align:center; padding:40px 20px;">
      <h3 style="color:var(--gold-bright);">${meta.name} — தரம் ${currentGrade}</h3>
      <p style="color:#cbd5e1; max-width:600px; margin:10px auto;">
        இந்த வகுப்பிற்கான மின்னூல் அத்தியாயங்கள் ஒருங்கிணைக்கப்பட்டு வருகின்றன. மூலப் பாடங்களை உடனே வாசிக்க கீழ்க்கண்ட இணைப்பை அழுத்தவும்.
      </p>
      <a href="tharam-${currentGrade}.html" class="sheet-btn sheet-btn-view">தரம் ${currentGrade} முழுப் பாடங்களைக் காண்க</a>
    </article>
  `;
}

function readAloudChapter() {
  const btn = document.getElementById('lessonSpeechBtn');
  if (!('speechSynthesis' in window)) {
    alert('உங்கள் உலாவியில் குரல்வழி வாசிப்பு வசதி இல்லை.');
    return;
  }

  if (window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel();
    if (btn) {
      btn.classList.remove('speaking');
      btn.innerHTML = `
        <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>
        <span>அத்தியாயம் கேட்க</span>
      `;
    }
    return;
  }

  window.speechSynthesis.cancel();
  const container = document.getElementById('activeChapterReadingArea');
  if (!container) return;

  // Clean text extraction without button labels or navigation text
  const textBlocks = Array.from(container.querySelectorAll('.chap-read-title, .verse-text-sacred, .verse-meaning-clean, .reading-section-block'))
    .map(el => el.innerText.trim())
    .filter(t => t.length > 0);

  const textToRead = textBlocks.join('\n\n');
  const utterance = new SpeechSynthesisUtterance(textToRead);
  utterance.lang = 'ta-IN';
  utterance.rate = 0.95;

  utterance.onend = () => {
    if (btn) {
      btn.classList.remove('speaking');
      btn.innerHTML = `
        <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>
        <span>அத்தியாயம் கேட்க</span>
      `;
    }
  };

  utterance.onerror = () => {
    if (btn) {
      btn.classList.remove('speaking');
      btn.innerHTML = `
        <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>
        <span>அத்தியாயம் கேட்க</span>
      `;
    }
  };

  if (btn) {
    btn.classList.add('speaking');
    btn.innerHTML = `
      <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
      <span>வாசிப்பை நிறுத்துக</span>
    `;
  }

  window.speechSynthesis.speak(utterance);
}

// High-Resolution Artwork Lightbox Modal Controls
window.currentLightboxIdx = 0;

window.openArtLightboxByIndex = function(idx) {
  const images = window.currentChapterImages || [];
  if (!images || images.length === 0) return;
  if (idx < 0) idx = 0;
  if (idx >= images.length) idx = images.length - 1;
  window.currentLightboxIdx = idx;

  const modal = document.getElementById('artLightboxModal');
  const imgEl = document.getElementById('artLightboxImg');
  const counterEl = document.getElementById('artLightboxCounter');
  const typeEl = document.getElementById('artLightboxType');
  const captionEl = document.getElementById('artLightboxCaption');
  const promptEl = document.getElementById('artLightboxPrompt');
  const dlBtn = document.getElementById('artLightboxDownloadBtn');

  if (!modal || !imgEl) return;

  const cur = images[idx];
  imgEl.src = cur.url;
  imgEl.alt = cur.caption;
  imgEl.classList.remove('zoomed');

  if (counterEl) counterEl.innerText = `காட்சி ${idx + 1} / ${images.length}`;
  if (typeEl) typeEl.innerText = cur.typeTitle || 'மரபு ஓவியக் காட்சி';
  if (captionEl) captionEl.innerText = cur.caption;
  if (promptEl) promptEl.innerText = cur.prompt || 'பாரம்பரிய இந்திய மரபு ஓவியக் கலை பாணி';
  if (dlBtn) {
    dlBtn.href = cur.url;
    dlBtn.setAttribute('download', cur.url.split('/').pop());
  }

  modal.classList.add('active');
  document.body.style.overflow = 'hidden';
};

window.closeArtLightbox = function() {
  const modal = document.getElementById('artLightboxModal');
  if (modal) modal.classList.remove('active');
  const imgEl = document.getElementById('artLightboxImg');
  if (imgEl) imgEl.classList.remove('zoomed');
  document.body.style.overflow = '';
};

window.nextArtLightboxImage = function() {
  const images = window.currentChapterImages || [];
  if (!images || images.length === 0) return;
  let next = window.currentLightboxIdx + 1;
  if (next >= images.length) next = 0;
  window.openArtLightboxByIndex(next);
};

window.prevArtLightboxImage = function() {
  const images = window.currentChapterImages || [];
  if (!images || images.length === 0) return;
  let prev = window.currentLightboxIdx - 1;
  if (prev < 0) prev = images.length - 1;
  window.openArtLightboxByIndex(prev);
};

window.toggleArtZoom = function() {
  const imgEl = document.getElementById('artLightboxImg');
  if (imgEl) imgEl.classList.toggle('zoomed');
};

// Keyboard navigation for Lightbox
document.addEventListener('keydown', (e) => {
  const modal = document.getElementById('artLightboxModal');
  if (!modal || !modal.classList.contains('active')) return;

  if (e.key === 'Escape') {
    window.closeArtLightbox();
  } else if (e.key === 'ArrowRight') {
    window.nextArtLightboxImage();
  } else if (e.key === 'ArrowLeft') {
    window.prevArtLightboxImage();
  }
});

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('activeChapterReadingArea')) {
    initBookReader();
  }
});
