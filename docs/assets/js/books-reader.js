/**
 * Gurukula Desam - 7 Sacred Ashram Books Digital Reader Engine
 * Supports Grades 1-12, all 7 Books, 7+ Chapters per book, URL deep-linking, Audio TTS
 */

let currentGrade = 1;
let currentBook = 'nanneri';
let currentChapter = 1;
let loadedBookData = {};

const BOOK_NARCHEYAL = {
  id: 'narcheyal',
  name: 'நற்செயல்',
  en: 'விளையாடிப் பயிலல் & 3 Ds',
  icon: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z',
  color: '#ffd700',
  desc: 'விளையாட்டும் பகிர்தலும், உள்ளதைக் கொண்டு மகிழ்தல், கடமை-கட்டுப்பாடு-கண்ணியம் (3 Ds)'
};

const BOOK_NARPANBU = {
  id: 'nalvazhi',
  name: 'நற்பண்பு',
  en: 'வாய்மையும் நற்பண்பும்',
  icon: 'M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z',
  color: '#facc15',
  desc: 'பெரியோர் பணிவு, வாய்மை, நாவடக்கம், இன்சொல் & நற்பண்பு நெறி'
};

const BOOK_NANNERI = {
  id: 'nanneri',
  name: 'நன்னெறி',
  en: 'ஒழுக்கமும் பணிவும்',
  icon: 'M12 2v3M7 5h10l-1.5 4H8.5L7 5z',
  color: '#38bdf8',
  desc: 'பணிவு, பெரியோர் மரியாதை மற்றும் தூய நடத்தை'
};

const BOOK_NALLARAM = {
  id: 'nallaram',
  name: 'நல்லறம்',
  en: 'ஈகையும் இல்லற தர்மமும்',
  icon: 'M11 20A7 7 0 0 1 4 13a8.9 8.9 0 0 1 8.2-8.9 7 7 0 0 1 7.8 7.8A8.9 8.9 0 0 1 11 20z',
  color: '#10b981',
  desc: 'ஈகை, விருந்தோம்பல், ஜீவகாருண்யம் மற்றும் சமுதாயத் தொண்டு'
};

const BOOK_NARTHUNAI = {
  id: 'narthunai',
  name: 'நற்துணை',
  en: 'இறைத்துதியும் சரணாகதியும்',
  icon: 'M12 2a9.5 9.5 0 0 0-9.5 9.5c0 7 9.5 12.5 9.5 12.5s9.5-5.5 9.5-12.5A9.5 9.5 0 0 0 12 2z',
  color: '#c084fc',
  desc: 'இறைத் திருவருள், திருமுறைகள், பக்தி மற்றும் சரணாகதி'
};

const BOOK_NARCHOL = {
  id: 'narchol',
  name: 'நற்சொல்',
  en: 'இன்சொல்லும் நாவடக்கமும்',
  icon: 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z',
  color: '#34d399',
  desc: 'இன்சொல் பேசுதல், நாவடக்கம் மற்றும் மந்திர ஒலி அதிர்வுகள்'
};

const BOOK_NARCHINTHANAI = {
  id: 'narchinthanai',
  name: 'நற்சிந்தனை',
  en: 'மெய்யறிவும் தத்துவமும்',
  icon: 'M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z',
  color: '#fb923c',
  desc: 'விஞ்ஞான-மெய்ஞ்ஞான சங்கமம், பிரபஞ்ச விதிகள் மற்றும் தத்துவ ஆய்வு'
};

function getBooksMetadataForGrade(grade) {
  if (grade <= 2) {
    // Grades 1 & 2: Only 1 book - நற்செயல்
    return [BOOK_NARCHEYAL];
  } else if (grade <= 4) {
    // Grades 3 & 4: 2 books - add நற்பண்பு (நற்செயல், நற்பண்பு)
    return [BOOK_NARCHEYAL, BOOK_NARPANBU];
  } else if (grade <= 8) {
    // Middle school (Grades 5 to 8): 5 books (remove நற்சிந்தனை, நற்சொல்)
    return [BOOK_NANNERI, BOOK_NALLARAM, BOOK_NARPANBU, BOOK_NARTHUNAI, BOOK_NARCHEYAL];
  } else if (grade <= 12) {
    // High school (Grades 9 to 12): 6 books (remove நற்சிந்தனை)
    return [BOOK_NANNERI, BOOK_NALLARAM, BOOK_NARPANBU, BOOK_NARTHUNAI, BOOK_NARCHOL, BOOK_NARCHEYAL];
  } else {
    // Higher Studies / Collegiate (B.A., M.A., Ph.D.): All 7 books (including நற்சிந்தனை)
    return [BOOK_NANNERI, BOOK_NALLARAM, BOOK_NARPANBU, BOOK_NARTHUNAI, BOOK_NARCHINTHANAI, BOOK_NARCHOL, BOOK_NARCHEYAL];
  }
}

const BOOKS_METADATA = [BOOK_NANNERI, BOOK_NALLARAM, BOOK_NARPANBU, BOOK_NARTHUNAI, BOOK_NARCHINTHANAI, BOOK_NARCHOL, BOOK_NARCHEYAL];

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

  const activeMeta = getBooksMetadataForGrade(currentGrade);
  currentBook = activeMeta[0].id;
  if (bookParam && activeMeta.some(b => b.id === bookParam)) currentBook = bookParam;
  if (chapterParam >= 1 && chapterParam <= 7) currentChapter = chapterParam;

  renderGradePills();
  renderBookShelfTabs();
  await loadGradeBookData(currentGrade);
  initClassroomApp(currentGrade);
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
  const activeMeta = getBooksMetadataForGrade(currentGrade);
  activeMeta.forEach((book, idx) => {
    const activeClass = (book.id === currentBook) ? 'active' : '';
    let done = 0;
    for (let c = 1; c <= 7; c++) {
      if (isBookChapterCompleted(currentGrade, book.id, c)) done++;
    }
    const badgeText = done === 7 ? '✓ 7/7 நிறைவு' : `${done}/7 பாடம்`;
    const isFull = done === 7 ? 'color:#10b981;' : 'color:#94a3b8;';
    html += `
      <button type="button" class="shelf-book-btn ${activeClass}" onclick="switchBook('${book.id}')" style="--book-accent:${book.color};">
        <span class="shelf-book-num">நூல் ${idx + 1}</span>
        <span class="shelf-book-title">${book.name}</span>
        <span class="shelf-book-en">${book.en}</span>
        <span class="shelf-book-prog-badge" style="font-size:0.75rem; font-weight:700; margin-top:6px; ${isFull}">${badgeText}</span>
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

async function switchGrade(grade) {
  currentGrade = grade;
  currentChapter = 1;
  renderGradePills();
  updateUrlParams();
  await loadGradeBookData(grade);
  initClassroomApp(grade);
  updateClassroomStats();
}

function switchBook(bookId) {
  currentBook = bookId;
  currentChapter = 1;
  renderBookShelfTabs();
  updateUrlParams();
  renderCurrentBook();
  updateClassroomStats();
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
    return localStorage.getItem(`gkd_completed_${grade}_${bookKey}_${chapterNum}`) === 'true';
  } catch (e) {
    return false;
  }
}

window.toggleBookChapterCompletion = function(grade, bookKey, chapterNum) {
  try {
    const key = `gkd_completed_${grade}_${bookKey}_${chapterNum}`;
    const isDone = isBookChapterCompleted(grade, bookKey, chapterNum);
    const newState = !isDone;

    if (newState) {
      localStorage.setItem(key, 'true');
      if (typeof window.playTempleBell === 'function') {
        window.playTempleBell();
      }
      if (typeof window.showToast === 'function') {
        window.showToast(`தரம் ${grade} • அத்தியாயம் ${chapterNum} வாசித்து உணரப்பட்டது.`);
      }
    } else {
      localStorage.removeItem(key);
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

    if (typeof updateClassroomStats === 'function') {
      updateClassroomStats();
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
    question = `நற்பண்பு அத்தியாயம் '${title}' நமக்கு உணர்த்தும் நற்பண்பு யாது?`;
    optCorrect = 'வாய்மை, நற்பண்பு, கடின உழைப்பு மற்றும் சோதனைகளிலும் தர்மத்தைக் கைவிடாமை.';
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
    try {
      localStorage.setItem(`gkd_quiz_${currentGrade}_${currentBook}_${currentChapter}`, 'true');
    } catch (e) {}
    if (fb) {
      fb.style.display = 'block';
      fb.style.background = 'rgba(16, 185, 129, 0.2)';
      fb.style.color = '#6ee7b7';
      fb.style.border = '1px solid #10b981';
      fb.innerHTML = `✨ <strong>அற்புதம்!</strong> ${exp} (+100 தர்ம XP)`;
    }
    if (typeof window.playTempleBell === 'function') {
      window.playTempleBell();
    }
    if (typeof updateClassroomStats === 'function') {
      updateClassroomStats();
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
    if (text && text.trim().length > 0) {
      localStorage.setItem(key, text);
    } else {
      localStorage.removeItem(key);
    }
    const ind = document.getElementById('chapterNoteSavedBadge');
    if (ind) {
      ind.style.display = 'inline-block';
      setTimeout(() => { ind.style.display = 'none'; }, 2000);
    }
    if (typeof updateClassroomStats === 'function') {
      updateClassroomStats();
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
  const activeMeta = getBooksMetadataForGrade(currentGrade);
  const meta = activeMeta.find(b => b.id === currentBook) || activeMeta[0];

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

// ==========================================================================
// 3-MONTH / 12-WEEK TRIMESTER CLASSROOM ENGINE & PROGRESS TRACKING
// ==========================================================================

const GRADE_1_2_SCHEDULE = [
  {
    month: 1,
    title: 'மாதம் 1: விளையாடிப் பயிலல் & 3 Ds கடமை (Play, Share & 3 Ds Action)',
    desc: 'நற்செயல் • அத் 1-3 • விளையாட்டு வழிக் கற்றல், பகிர்தல், உள்ளதைக் கொண்டு மகிழ்தல், கடமை-கட்டுப்பாடு-கண்ணியம்',
    checkpoint: '🎯 மாதம் 1 பால சாதனா ஆய்வு (Month 1 Checkpoint)',
    weeks: [
      {
        weekNum: 1,
        title: 'வாரம் 1: விளையாட்டும் மழலை மகிழ்ச்சியும்',
        theme: 'நற்செயல் அத் 1 • விளையாடுதல், பகிர்தல் & உள்ளதைக் கொண்டு மகிழ்தல்',
        lessons: [{ book: 'narcheyal', chap: 1 }]
      },
      {
        weekNum: 2,
        title: 'வாரம் 2: உணவு வீணாக்காத மழலைக் கடமை',
        theme: 'நற்செயல் அத் 2 • உணவை வீணாக்காமல் உண்ணும் நற்பழக்கம்',
        lessons: [{ book: 'narcheyal', chap: 2 }]
      },
      {
        weekNum: 3,
        title: 'வாரம் 3: விடியற்காலை எழும் கட்டுப்பாடு',
        theme: 'நற்செயல் அத் 3 • சூரிய உதயத்தில் எழுதல் & காலை வணக்கம்',
        lessons: [{ book: 'narcheyal', chap: 3 }]
      },
      {
        weekNum: 4,
        title: 'வாரம் 4: மாதம் 1 நற்செயல் ஆய்வு & 3 Ds பயிற்சி',
        theme: 'நற்செயல் அத் 3 • காலை விழிப்பு & விளையாடிப் பகிர்தல் செயல்முறைப் பயிற்சி',
        milestone: 'மாதம் 1 நற்செயல் தேர்ச்சி ஆய்வு',
        lessons: [{ book: 'narcheyal', chap: 3 }]
      }
    ]
  },
  {
    month: 2,
    title: 'மாதம் 2: பள்ளி ஒழுக்கமும் தூய்மையும் (School Reverence & Cleanliness)',
    desc: 'நற்செயல் • அத் 4-5 • பள்ளிக்கு ஒழுங்காகச் செல்லுதல், காலணிகளை அடுக்குதல் & தூய்மை',
    checkpoint: '🎯 மாதம் 2 பால நற்செயல் ஆய்வு (Month 2 Checkpoint)',
    weeks: [
      {
        weekNum: 5,
        title: 'வாரம் 5: பள்ளிக்கு ஒழுங்காகச் செல்லுதல்',
        theme: 'நற்செயல் அத் 4 • ஆசிரியர் பணிவு, நேரந் தவறாமை & சுறுசுறுப்பு',
        lessons: [{ book: 'narcheyal', chap: 4 }]
      },
      {
        weekNum: 6,
        title: 'வாரம் 6: சுறுசுறுப்பும் சோம்பலின்மையும்',
        theme: 'நற்செயல் அத் 4 • சோம்பல் தவிர்த்து மகிழ்வோடு கற்றல்',
        lessons: [{ book: 'narcheyal', chap: 4 }]
      },
      {
        weekNum: 7,
        title: 'வாரம் 7: காலணிகளை அடுக்குதல் & தூய்மை',
        theme: 'நற்செயல் அத் 5 • உடைமைகள் பாதுகாப்பு & சுற்றுப்புறத் தூய்மை',
        lessons: [{ book: 'narcheyal', chap: 5 }]
      },
      {
        weekNum: 8,
        title: 'வாரம் 8: மாதம் 2 பால சாதனா ஆய்வு',
        theme: 'நற்செயல் அத் 5 • தூய்மை ஒழுக்கமும் சுயக் கட்டுப்பாடும்',
        milestone: 'மாதம் 2 நற்செயல் தேர்ச்சி ஆய்வு',
        lessons: [{ book: 'narcheyal', chap: 5 }]
      }
    ]
  },
  {
    month: 3,
    title: 'மாதம் 3: தோழர் கண்ணியமும் புன்னகையும் (Friendship Dignity & Smile)',
    desc: 'நற்செயல் • அத் 6-7 • தோழர்களிடம் கண்ணியமாக விளையாடுதல், புன்னகை & நிறைவு',
    checkpoint: '🎓 மழலைப் பருவ நிறைவு & பட்டயம் (Infant Graduation)',
    weeks: [
      {
        weekNum: 9,
        title: 'வாரம் 9: தோழர்களிடம் கண்ணியமாக விளையாடுதல்',
        theme: 'நற்செயல் அத் 6 • விட்டுக்கொடுத்தல், பகிர்தல் & கண்ணியமான விளையாட்டு',
        lessons: [{ book: 'narcheyal', chap: 6 }]
      },
      {
        weekNum: 10,
        title: 'வாரம் 10: சண்டை போடாமல் சமாதானம்',
        theme: 'நற்செயல் அத் 6 • கோபமின்மை & தோழர் அன்பு',
        lessons: [{ book: 'narcheyal', chap: 6 }]
      },
      {
        weekNum: 11,
        title: 'வாரம் 11: புன்னகைக் கண்ணியமும் அமைதியும்',
        theme: 'நற்செயல் அத் 7 • அழுது அடம்பிடிக்காத புன்னகைக் கண்ணியம் & அமைதி',
        lessons: [{ book: 'narcheyal', chap: 7 }]
      },
      {
        weekNum: 12,
        title: 'வாரம் 12: மழலைப் பருவ நிறைவுப் பட்டய ஆய்வு',
        theme: 'நற்செயல் அத் 7 • நற்செயல் 7 அத்தியாயங்கள் முழு நிறைவு & 3 Ds வாழ்வியல் பயிற்சி',
        milestone: '🎓 மழலைப் பருவ நிறைவுப் பட்டயம் (Infant Term Diploma - 7 அத்தியாயங்கள்)',
        lessons: [{ book: 'narcheyal', chap: 7 }]
      }
    ]
  }
];

const GRADE_3_4_SCHEDULE = [
  {
    month: 1,
    title: 'மாதம் 1: நற்செயல் அடித்தளமும் 3 Ds கடமையும் (Action Foundation & 3 Ds)',
    desc: 'நற்செயல் • அத் 1-5 • விளையாட்டு வழிக் கற்றல், பகிர்தல், விடியற்காலை விழிப்பு & தூய்மை',
    checkpoint: '🎯 மாதம் 1 பால சாதனா ஆய்வு (Month 1 Checkpoint)',
    weeks: [
      {
        weekNum: 1,
        title: 'வாரம் 1: விளையாடிப் பகிர்தலும் உணவு உண்பதும்',
        theme: 'நற்செயல் அத் 1-2 • விளையாடுதல் & உணவை வீணாக்காமல் உண்ணும் கடமை',
        lessons: [
          { book: 'narcheyal', chap: 1 },
          { book: 'narcheyal', chap: 2 }
        ]
      },
      {
        weekNum: 2,
        title: 'வாரம் 2: சூரிய உதயமும் விடியலில் எழும் கடமையும்',
        theme: 'நற்செயல் அத் 3 • விடியற்காலை எழும் கட்டுப்பாடு & காலை வணக்கம்',
        lessons: [
          { book: 'narcheyal', chap: 3 }
        ]
      },
      {
        weekNum: 3,
        title: 'வாரம் 3: பள்ளிக்கு ஒழுங்காகச் செல்லுதல்',
        theme: 'நற்செயல் அத் 4 • சுறுசுறுப்பு & ஆசிரியர் பணிவு',
        lessons: [
          { book: 'narcheyal', chap: 4 }
        ]
      },
      {
        weekNum: 4,
        title: 'வாரம் 4: தூய்மையும் உடைமைப் பாதுகாப்பும்',
        theme: 'நற்செயல் அத் 5 • காலணிகளை அடுக்குதல் & உடைமைத் தூய்மை',
        milestone: 'மாதம் 1 நற்செயல் தேர்ச்சி ஆய்வு',
        lessons: [
          { book: 'narcheyal', chap: 5 }
        ]
      }
    ]
  },
  {
    month: 2,
    title: 'மாதம் 2: நற்செயல் நிறைவும் நற்பண்பு தொடக்கமும் (Action Completion & Noble Virtue)',
    desc: 'நற்செயல் அத் 6-7 & நற்பண்பு அத் 1-2 • கண்ணியமான விளையாட்டு, சுறுசுறுப்பு & உண்மை நெறி',
    checkpoint: '🎯 மாதம் 2 நற்பண்பு ஆய்வு (Month 2 Checkpoint)',
    weeks: [
      {
        weekNum: 5,
        title: 'வாரம் 5: தோழர்களிடம் கண்ணியமாக விளையாடுதல்',
        theme: 'நற்செயல் அத் 6 • பகிர்வு, விட்டுக் கொடுத்தல் & நேசமான தோழமை',
        lessons: [
          { book: 'narcheyal', chap: 6 }
        ]
      },
      {
        weekNum: 6,
        title: 'வாரம் 6: புன்னகைக் கண்ணியமும் நற்செயல் நிறைவும்',
        theme: 'நற்செயல் அத் 7 • அழுது அடம்பிடிக்காத புன்னகை & நற்செயல் முழுமை',
        lessons: [
          { book: 'narcheyal', chap: 7 }
        ]
      },
      {
        weekNum: 7,
        title: 'வாரம் 7: நற்பண்பும் நேர்மையும்',
        theme: 'நற்பண்பு அத் 1 • பெரியோர் வணக்கம், பணிவு & நற்பண்பு தொடக்கம்',
        lessons: [
          { book: 'nalvazhi', chap: 1 }
        ]
      },
      {
        weekNum: 8,
        title: 'வாரம் 8: சுறுசுறுப்பும் சோம்பல் தவிர்த்தலும்',
        theme: 'நற்பண்பு அத் 2 • சுறுசுறுப்பான வாழ்க்கை & ஊக்கம்',
        milestone: 'மாதம் 2 நற்பண்பு தொடக்க ஆய்வு',
        lessons: [
          { book: 'nalvazhi', chap: 2 }
        ]
      }
    ]
  },
  {
    month: 3,
    title: 'மாதம் 3: நற்பண்பு மேன்மையும் தர்ம நிறைவும் (Noble Character & Dharma Graduation)',
    desc: 'நற்பண்பு அத் 3-7 • அறிவு, நல்ல தோழமை, அடக்கம், முயற்சி & நற்பெயர் காத்தல்',
    checkpoint: '🎓 தொடக்கப் பள்ளிப் பருவ நிறைவு & பட்டயம் (Primary Graduation)',
    weeks: [
      {
        weekNum: 9,
        title: 'வாரம் 9: அறிவின் மேன்மை',
        theme: 'நற்பண்பு அத் 3 • கல்வி ஆர்வமும் நல்லறிவுத் தேடலும்',
        lessons: [
          { book: 'nalvazhi', chap: 3 }
        ]
      },
      {
        weekNum: 10,
        title: 'வாரம் 10: நல்ல நண்பர்கள் சேர்க்கை',
        theme: 'நற்பண்பு அத் 4 • நற்குணத் தோழமையும் நற்பழக்கமும்',
        lessons: [
          { book: 'nalvazhi', chap: 4 }
        ]
      },
      {
        weekNum: 11,
        title: 'வாரம் 11: பணிவும் முயற்சியும்',
        theme: 'நற்பண்பு அத் 5-6 • அடக்கம் உடைமை & விடாமுயற்சியே செல்வம்',
        lessons: [
          { book: 'nalvazhi', chap: 5 },
          { book: 'nalvazhi', chap: 6 }
        ]
      },
      {
        weekNum: 12,
        title: 'வாரம் 12: நற்பெயர் காத்தல் & தொடக்கப் பள்ளி நிறைவு',
        theme: 'நற்பண்பு அத் 7 • நற்பெயரைக் காத்து வாழ்தல் & 2 நூல்கள் முழு நிறைவு',
        milestone: '🎓 தொடக்கப் பள்ளிப் பருவ நிறைவுப் பட்டயம் (Primary Term Diploma - 14 அத்தியாயங்கள்)',
        lessons: [
          { book: 'nalvazhi', chap: 7 }
        ]
      }
    ]
  }
];

const MIDDLE_SCHOOL_SCHEDULE = [
  {
    month: 1,
    title: 'மாதம் 1: நன்னெறி & நல்லறம் (Conduct & Righteous Deeds)',
    desc: 'நன்னெறி & நல்லறம் • 14 அத்தியாயங்கள் • பெரியோர் வழிபாடு, நற்பழக்கம், ஈகை & உயிரிரக்கம்',
    checkpoint: '🎯 மாதம் 1 அறநெறி ஆய்வு (Month 1 Checkpoint)',
    weeks: [
      {
        weekNum: 1,
        title: 'வாரம் 1: ஒழுக்கமும் பணிவும்',
        theme: 'நன்னெறி அத் 1-4 • தாய் தந்தை வழிபாடு, ஆசிரியர் பணிவு, இறை பக்தி & நற்குணம்',
        lessons: [
          { book: 'nanneri', chap: 1 },
          { book: 'nanneri', chap: 2 },
          { book: 'nanneri', chap: 3 },
          { book: 'nanneri', chap: 4 }
        ]
      },
      {
        weekNum: 2,
        title: 'வாரம் 2: இன்சொல்லும் ஈகையும்',
        theme: 'நன்னெறி அத் 5-7 & நல்லறம் அத் 1 • இன்சொல், அடக்கம், பகிர்தல் & ஈகைக் குணம்',
        lessons: [
          { book: 'nanneri', chap: 5 },
          { book: 'nanneri', chap: 6 },
          { book: 'nanneri', chap: 7 },
          { book: 'nallaram', chap: 1 }
        ]
      },
      {
        weekNum: 3,
        title: 'வாரம் 3: ஜீவகாருண்யமும் விருந்தோம்பலும்',
        theme: 'நல்லறம் அத் 2-4 • பசி தீர்த்தல், உயிரிரக்கம் & விருந்தினர் பேணல்',
        lessons: [
          { book: 'nallaram', chap: 2 },
          { book: 'nallaram', chap: 3 },
          { book: 'nallaram', chap: 4 }
        ]
      },
      {
        weekNum: 4,
        title: 'வாரம் 4: அறநெறியும் இயற்கை நேயமும்',
        theme: 'நல்லறம் அத் 5-7 • அறத்தின் சிறப்பு, தூய்மை & இயற்கை பாதுகாப்பு',
        milestone: 'மாதம் 1 நன்னெறி & நல்லறத் தேர்ச்சி ஆய்வு (14 அத்தியாயங்கள்)',
        lessons: [
          { book: 'nallaram', chap: 5 },
          { book: 'nallaram', chap: 6 },
          { book: 'nallaram', chap: 7 }
        ]
      }
    ]
  },
  {
    month: 2,
    title: 'மாதம் 2: நற்பண்பு & நற்துணை (Virtue, Truth & Divine Refuge)',
    desc: 'நற்பண்பு & நற்துணை • 14 அத்தியாயங்கள் • வாய்மை, உழைப்பு, தெய்வத் துதி & சரணாகதி',
    checkpoint: '🎯 மாதம் 2 நற்பண்பு & பக்தி ஆய்வு (Month 2 Checkpoint)',
    weeks: [
      {
        weekNum: 5,
        title: 'வாரம் 5: வாய்மையும் நேர்மை வழியும்',
        theme: 'நற்பண்பு அத் 1-4 • சத்திய நெறி, பொய் பேசாமை & உழைப்பின் மேன்மை',
        lessons: [
          { book: 'nalvazhi', chap: 1 },
          { book: 'nalvazhi', chap: 2 },
          { book: 'nalvazhi', chap: 3 },
          { book: 'nalvazhi', chap: 4 }
        ]
      },
      {
        weekNum: 6,
        title: 'வாரம் 6: முயற்சி உணர்வும் இறை சரணாகதியும்',
        theme: 'நற்பண்பு அத் 5-7 & நற்துணை அத் 1 • அடக்கம், முயற்சி, நற்பெயர் காத்தல் & விநாயகர் துணை',
        lessons: [
          { book: 'nalvazhi', chap: 5 },
          { book: 'nalvazhi', chap: 6 },
          { book: 'nalvazhi', chap: 7 },
          { book: 'narthunai', chap: 1 }
        ]
      },
      {
        weekNum: 7,
        title: 'வாரம் 7: திருமுறை இசையும் தெய்வ வழிபாடும்',
        theme: 'நற்துணை அத் 2-4 • முருகன் வேல் துணை, சிவபெருமான் அருள் & அம்பிகை கருணை',
        lessons: [
          { book: 'narthunai', chap: 2 },
          { book: 'narthunai', chap: 3 },
          { book: 'narthunai', chap: 4 }
        ]
      },
      {
        weekNum: 8,
        title: 'வாரம் 8: அஞ்சாமையும் தெய்வ சரணாகதியும்',
        theme: 'நற்துணை அத் 5-7 • திருமால் அருள், ஆஞ்சநேயர் வீரம் & அபயம்',
        milestone: 'மாதம் 2 நற்பண்பு & நற்துணை ஆய்வு (28 அத்தியாயங்கள்)',
        lessons: [
          { book: 'narthunai', chap: 5 },
          { book: 'narthunai', chap: 6 },
          { book: 'narthunai', chap: 7 }
        ]
      }
    ]
  },
  {
    month: 3,
    title: 'மாதம் 3: நற்செயல் & 3 Ds வாழ்வியல் நெறி (Practical Dharma & Graduation)',
    desc: 'நற்செயல் • 7 அத்தியாயங்கள் • கடமை (Duty), கட்டுப்பாடு (Discipline), கண்ணியம் (Dignity) & தர்ம வாழ்க்கை',
    checkpoint: '🎓 நடுநிலைப் பள்ளிப் பருவ நிறைவு & பட்டயம் (Middle School Graduation)',
    weeks: [
      {
        weekNum: 9,
        title: 'வாரம் 9: விளையாடிப் பகிர்தலும் உணவு நெறியும்',
        theme: 'நற்செயல் அத் 1-2 • விளையாடுதல், பகிர்தல் & உணவு வீணாக்காத கடமை',
        lessons: [
          { book: 'narcheyal', chap: 1 },
          { book: 'narcheyal', chap: 2 }
        ]
      },
      {
        weekNum: 10,
        title: 'வாரம் 10: அதிகாலை எழுச்சியும் பள்ளி ஒழுக்கமும்',
        theme: 'நற்செயல் அத் 3-4 • விடியற்காலை விழிப்பு, சூரிய நமஸ்காரம் & பள்ளி சுறுசுறுப்பு',
        lessons: [
          { book: 'narcheyal', chap: 3 },
          { book: 'narcheyal', chap: 4 }
        ]
      },
      {
        weekNum: 11,
        title: 'வாரம் 11: தூய்மையும் தோழர் கண்ணியமும்',
        theme: 'நற்செயல் அத் 5-6 • தூய்மைப் பழக்கம் & தோழர்களிடம் கண்ணியமாகப் பழகுதல்',
        lessons: [
          { book: 'narcheyal', chap: 5 },
          { book: 'narcheyal', chap: 6 }
        ]
      },
      {
        weekNum: 12,
        title: 'வாரம் 12: புன்னகைக் கண்ணியமும் நடுநிலைப் பள்ளிப் பட்டயமும்',
        theme: 'நற்செயல் அத் 7 • புன்னகைக் கண்ணியம் & 5 நூல்கள் முழுப் பருவ நிறைவு',
        milestone: '🎓 நடுநிலைப் பள்ளிப் பருவ நிறைவுப் பட்டயம் (Middle School Diploma - 35 அத்தியாயங்கள்)',
        lessons: [
          { book: 'narcheyal', chap: 7 }
        ]
      }
    ]
  }
];

const HIGH_SCHOOL_SCHEDULE = [
  {
    month: 1,
    title: 'மாதம் 1: நன்னெறி & நல்லறம் (Right Conduct & Righteous Deeds)',
    desc: 'நன்னெறி & நல்லறம் • 14 அத்தியாயங்கள் • நற்பழக்கம், பெரியோர் பணிவு, ஈகை & ஜீவகாருண்யம்',
    checkpoint: '🎯 மாதம் 1 உயர் அறநெறி ஆய்வு (Month 1 Checkpoint)',
    weeks: [
      {
        weekNum: 1,
        title: 'வாரம் 1: ஒழுக்கமும் வணக்கமும்',
        theme: 'நன்னெறி அத் 1-4 • தாய் தந்தை வழிபாடு, ஆசிரியர் பணிவு, இறை பக்தி & நற்குணம்',
        lessons: [
          { book: 'nanneri', chap: 1 },
          { book: 'nanneri', chap: 2 },
          { book: 'nanneri', chap: 3 },
          { book: 'nanneri', chap: 4 }
        ]
      },
      {
        weekNum: 2,
        title: 'வாரம் 2: நற்பழக்கங்களும் இன்சொல்லும்',
        theme: 'நன்னெறி அத் 5-7 & நல்லறம் அத் 1 • இன்சொல், அடக்கம், பகிர்வு & அறம் போற்றுதல்',
        lessons: [
          { book: 'nanneri', chap: 5 },
          { book: 'nanneri', chap: 6 },
          { book: 'nanneri', chap: 7 },
          { book: 'nallaram', chap: 1 }
        ]
      },
      {
        weekNum: 3,
        title: 'வாரம் 3: ஜீவகாருண்யமும் விருந்தோம்பலும்',
        theme: 'நல்லறம் அத் 2-4 • பசி தீர்த்தல், உயிரிரக்கம் & விருந்தினர் பேணல்',
        lessons: [
          { book: 'nallaram', chap: 2 },
          { book: 'nallaram', chap: 3 },
          { book: 'nallaram', chap: 4 }
        ]
      },
      {
        weekNum: 4,
        title: 'வாரம் 4: அறநெறியும் இயற்கை நேயமும்',
        theme: 'நல்லறம் அத் 5-7 • அறத்தின் சிறப்பு, தூய்மை & இயற்கை சூழல் பாதுகாப்பு',
        milestone: 'மாதம் 1 தேர்ச்சி ஆய்வு (14 அத்தியாயங்கள்)',
        lessons: [
          { book: 'nallaram', chap: 5 },
          { book: 'nallaram', chap: 6 },
          { book: 'nallaram', chap: 7 }
        ]
      }
    ]
  },
  {
    month: 2,
    title: 'மாதம் 2: நற்பண்பு & நற்துணை (Virtue, Truth & Divine Refuge)',
    desc: 'நற்பண்பு & நற்துணை • 14 அத்தியாயங்கள் • வாய்மை, உழைப்பு, திருமுறை பக்தி & சரணாகதி',
    checkpoint: '🎯 மாதம் 2 வாய்மை & சரணாகதி ஆய்வு (Month 2 Checkpoint)',
    weeks: [
      {
        weekNum: 5,
        title: 'வாரம் 5: வாய்மையும் நேர்மை வழியும்',
        theme: 'நற்பண்பு அத் 1-4 • சத்திய நெறி, பொய் பேசாமை & உழைப்பின் மேன்மை',
        lessons: [
          { book: 'nalvazhi', chap: 1 },
          { book: 'nalvazhi', chap: 2 },
          { book: 'nalvazhi', chap: 3 },
          { book: 'nalvazhi', chap: 4 }
        ]
      },
      {
        weekNum: 6,
        title: 'வாரம் 6: கடமை உணர்வும் சரணாகதியும்',
        theme: 'நற்பண்பு அத் 5-7 & நற்துணை அத் 1 • சோதனை வெல்லும் அறம், நற்பெயர் காத்தல் & விநாயகர் துணை',
        lessons: [
          { book: 'nalvazhi', chap: 5 },
          { book: 'nalvazhi', chap: 6 },
          { book: 'nalvazhi', chap: 7 },
          { book: 'narthunai', chap: 1 }
        ]
      },
      {
        weekNum: 7,
        title: 'வாரம் 7: திருமுறை இசையும் தெய்வ வழிபாடும்',
        theme: 'நற்துணை அத் 2-4 • முருகன் துணை, சிவபெருமான் திருவருள் & அம்பிகை பக்தி',
        lessons: [
          { book: 'narthunai', chap: 2 },
          { book: 'narthunai', chap: 3 },
          { book: 'narthunai', chap: 4 }
        ]
      },
      {
        weekNum: 8,
        title: 'வாரம் 8: அஞ்சாமையும் தெய்வ சரணாகதியும்',
        theme: 'நற்துணை அத் 5-7 • காக்கும் பெருமாள், ஆஞ்சநேயர் பக்தி & அபயம்',
        milestone: 'மாதம் 2 தேர்ச்சி ஆய்வு (28 அத்தியாயங்கள்)',
        lessons: [
          { book: 'narthunai', chap: 5 },
          { book: 'narthunai', chap: 6 },
          { book: 'narthunai', chap: 7 }
        ]
      }
    ]
  },
  {
    month: 3,
    title: 'மாதம் 3: நற்சொல் & நற்செயல் (Sweet Speech & Practical Dharma)',
    desc: 'நற்சொல் & நற்செயல் • 14 அத்தியாயங்கள் • நாவடக்கம், இன்சொல், 3 Ds & பஞ்ச மகா யாகங்கள்',
    checkpoint: '🎓 உயர்நிலைப் பள்ளிப் பருவ நிறைவு & பட்டயம் (High School Graduation)',
    weeks: [
      {
        weekNum: 9,
        title: 'வாரம் 9: நாவடக்கமும் இனிய மொழியும்',
        theme: 'நற்சொல் அத் 1-4 • இன்சொல் பேசுதல், புறங்கூறாமை & வாக்கின் தூய்மை',
        lessons: [
          { book: 'narchol', chap: 1 },
          { book: 'narchol', chap: 2 },
          { book: 'narchol', chap: 3 },
          { book: 'narchol', chap: 4 }
        ]
      },
      {
        weekNum: 10,
        title: 'வாரம் 10: பயனுள்ள சொல்லும் தினசரி தர்மமும்',
        theme: 'நற்சொல் அத் 5-7 & நற்செயல் அத் 1 • பயன்படப் பேசுதல், கோபமின்மை & விளையாடிப் பகிர்தல்',
        lessons: [
          { book: 'narchol', chap: 5 },
          { book: 'narchol', chap: 6 },
          { book: 'narchol', chap: 7 },
          { book: 'narcheyal', chap: 1 }
        ]
      },
      {
        weekNum: 11,
        title: 'வாரம் 11: உணவு நெறியும் விடியற்காலை எழும் கட்டுப்பாடும்',
        theme: 'நற்செயல் அத் 2-4 • உணவு வீணாக்காத கடமை, விடியற்காலை விழிப்பு & பள்ளி ஒழுக்கம்',
        lessons: [
          { book: 'narcheyal', chap: 2 },
          { book: 'narcheyal', chap: 3 },
          { book: 'narcheyal', chap: 4 }
        ]
      },
      {
        weekNum: 12,
        title: 'வாரம் 12: 3 Ds செயல்முறை, பஞ்ச யாகங்கள் & பட்டமளிப்பு',
        theme: 'நற்செயல் அத் 5-7 • தூய்மை, தோழர் கண்ணியம், புன்னகை & 6 நூல்கள் முழு நிறைவு',
        milestone: '🎓 உயர்நிலைப் பள்ளிப் பருவ நிறைவுப் பட்டயம் (High School Diploma - 42 அத்தியாயங்கள்)',
        lessons: [
          { book: 'narcheyal', chap: 5 },
          { book: 'narcheyal', chap: 6 },
          { book: 'narcheyal', chap: 7 }
        ]
      }
    ]
  }
];

const COLLEGIATE_SCHEDULE = [
  {
    month: 1,
    title: 'மாதம் 1: அற அடித்தளமும் தர்ம ஒழுக்கமும் (Moral Foundation & Right Conduct)',
    desc: 'நன்னெறி & நல்லறம் • 14 அத்தியாயங்கள் • நற்பழக்கம், ஈகை & பெரியோர் பணிவு',
    checkpoint: '🎯 மாதம் 1 இடைப் பருவ ஆய்வு (Month 1 Milestone Checkpoint)',
    weeks: [
      {
        weekNum: 1,
        title: 'வாரம் 1: ஒழுக்கமும் வணக்கமும்',
        theme: 'நன்னெறி அத் 1-4 • தாய் தந்தை வழிபாடு, ஆசிரியர் பணிவு, இறை பக்தி',
        lessons: [
          { book: 'nanneri', chap: 1 },
          { book: 'nanneri', chap: 2 },
          { book: 'nanneri', chap: 3 },
          { book: 'nanneri', chap: 4 }
        ]
      },
      {
        weekNum: 2,
        title: 'வாரம் 2: நற்பழக்கங்களும் இன்சொல்லும்',
        theme: 'நன்னெறி அத் 5-7 & நல்லறம் அத் 1 • இன்சொல், அடக்கம் & பகிர்வு',
        lessons: [
          { book: 'nanneri', chap: 5 },
          { book: 'nanneri', chap: 6 },
          { book: 'nanneri', chap: 7 },
          { book: 'nallaram', chap: 1 }
        ]
      },
      {
        weekNum: 3,
        title: 'வாரம் 3: ஜீவகாருண்யமும் விருந்தோம்பலும்',
        theme: 'நல்லறம் அத் 2-4 • பசி தீர்த்தல், உயிரிரக்கம் & விருந்தினர் பேணல்',
        lessons: [
          { book: 'nallaram', chap: 2 },
          { book: 'nallaram', chap: 3 },
          { book: 'nallaram', chap: 4 }
        ]
      },
      {
        weekNum: 4,
        title: 'வாரம் 4: அறநெறியும் இயற்கை நேயமும்',
        theme: 'நல்லறம் அத் 5-7 • அறத்தின் சிறப்பு, தூய்மை, சுற்றுப்புறப் பாதுகாப்பு',
        milestone: 'மாதம் 1 தேர்ச்சி ஆய்வு (14 அத்தியாயங்கள்)',
        lessons: [
          { book: 'nallaram', chap: 5 },
          { book: 'nallaram', chap: 6 },
          { book: 'nallaram', chap: 7 }
        ]
      }
    ]
  },
  {
    month: 2,
    title: 'மாதம் 2: பக்தி, இசை & மெய்யறிவு விழிப்பு (Devotion, Sacred Hymns & Wisdom)',
    desc: 'நற்பண்பு, நற்துணை & நற்சிந்தனை • 16 அத்தியாயங்கள் • வாய்மை, தேவாரம் & பிரபஞ்ச வியப்பு',
    checkpoint: '🎯 மாதம் 2 இடைப் பருவ ஆய்வு (Month 2 Milestone Checkpoint)',
    weeks: [
      {
        weekNum: 5,
        title: 'வாரம் 5: வாய்மையும் நேர்மை வழியும்',
        theme: 'நற்பண்பு அத் 1-4 • சத்திய நெறி, பொய் பேசாமை, உழைப்பின் மேன்மை',
        lessons: [
          { book: 'nalvazhi', chap: 1 },
          { book: 'nalvazhi', chap: 2 },
          { book: 'nalvazhi', chap: 3 },
          { book: 'nalvazhi', chap: 4 }
        ]
      },
      {
        weekNum: 6,
        title: 'வாரம் 6: கடமை உணர்வும் சரணாகதியும்',
        theme: 'நற்பண்பு அத் 5-7 & நற்துணை அத் 1 • சோதனை வெல்லும் அறம், இறை சரணாகதி',
        lessons: [
          { book: 'nalvazhi', chap: 5 },
          { book: 'nalvazhi', chap: 6 },
          { book: 'nalvazhi', chap: 7 },
          { book: 'narthunai', chap: 1 }
        ]
      },
      {
        weekNum: 7,
        title: 'வாரம் 7: திருமுறை இசையும் தெய்வ வழிபாடும்',
        theme: 'நற்துணை அத் 2-5 • விநாயகர், முருகன், சிவபெருமான், சக்தி வழிபாட்டுப் பாடல்கள்',
        lessons: [
          { book: 'narthunai', chap: 2 },
          { book: 'narthunai', chap: 3 },
          { book: 'narthunai', chap: 4 },
          { book: 'narthunai', chap: 5 }
        ]
      },
      {
        weekNum: 8,
        title: 'வாரம் 8: அஞ்சாமையும் தத்துவ ஆய்வும்',
        theme: 'நற்துணை அத் 6-7 & நற்சிந்தனை அத் 1-2 • அபயம், மன அமைதி & மெய்யறிவு வினாக்கள்',
        milestone: 'மாதம் 2 தேர்ச்சி ஆய்வு (30 அத்தியாயங்கள்)',
        lessons: [
          { book: 'narthunai', chap: 6 },
          { book: 'narthunai', chap: 7 },
          { book: 'narchinthanai', chap: 1 },
          { book: 'narchinthanai', chap: 2 }
        ]
      }
    ]
  },
  {
    month: 3,
    title: 'மாதம் 3: வேதாந்த-அறிவியல், சமுதாயத் தொண்டு & இறுதிப் பட்டயம் (Higher Studies & Graduation)',
    desc: 'நற்சிந்தனை, நற்சொல் & நற்செயல் • 19 அத்தியாயங்கள் • விஞ்ஞான-மெய்ஞ்ஞானம், 3 Ds & பஞ்ச யாகங்கள்',
    checkpoint: '🎓 இறுதிப் பருவத் தேர்ச்சி & பட்டயம் (Term Graduation)',
    weeks: [
      {
        weekNum: 9,
        title: 'வாரம் 9: விஞ்ஞானமும் பிரபஞ்ச தத்துவமும்',
        theme: 'நற்சிந்தனை அத் 3-6 • இயற்கை விதிகள், அண்டவெளி ஆச்சர்யம், அறிவியல் சங்கமம்',
        lessons: [
          { book: 'narchinthanai', chap: 3 },
          { book: 'narchinthanai', chap: 4 },
          { book: 'narchinthanai', chap: 5 },
          { book: 'narchinthanai', chap: 6 }
        ]
      },
      {
        weekNum: 10,
        title: 'வாரம் 10: நாவடக்கமும் இனிய மொழியும்',
        theme: 'நற்சிந்தனை அத் 7 & நற்சொல் அத் 1-3 • இன்சொல் பேசுதல், புறங்கூறாமை, வாக்கின் தூய்மை',
        lessons: [
          { book: 'narchinthanai', chap: 7 },
          { book: 'narchol', chap: 1 },
          { book: 'narchol', chap: 2 },
          { book: 'narchol', chap: 3 }
        ]
      },
      {
        weekNum: 11,
        title: 'வாரம் 11: பயனுள்ள சொல்லும் தினசரி தர்மமும்',
        theme: 'நற்சொல் அத் 4-7 & நற்செயல் அத் 1-2 • பயன்படப் பேசுதல், இல்லறக் கடமைகள் தொடக்கம்',
        lessons: [
          { book: 'narchol', chap: 4 },
          { book: 'narchol', chap: 5 },
          { book: 'narchol', chap: 6 },
          { book: 'narchol', chap: 7 },
          { book: 'narcheyal', chap: 1 },
          { book: 'narcheyal', chap: 2 }
        ]
      },
      {
        weekNum: 12,
        title: 'வாரம் 12: 3 Ds செயல்முறை, பஞ்ச யாகங்கள் & பட்டமளிப்பு',
        theme: 'நற்செயல் அத் 3-7 • கடமை (Duty), கட்டுப்பாடு (Discipline), கண்ணியம் (Dignity), பஞ்ச மகா யாகங்கள் & முழுப் பருவ நிறைவு',
        milestone: '🎓 பருவ நிறைவுப் பட்டயச் சான்றிதழ் (Grade Term Diploma - 49 அத்தியாயங்கள்)',
        lessons: [
          { book: 'narcheyal', chap: 3 },
          { book: 'narcheyal', chap: 4 },
          { book: 'narcheyal', chap: 5 },
          { book: 'narcheyal', chap: 6 },
          { book: 'narcheyal', chap: 7 }
        ]
      }
    ]
  }
];

const PRIMARY_TRIMESTER_SCHEDULE = GRADE_1_2_SCHEDULE;
const SECONDARY_TRIMESTER_SCHEDULE = COLLEGIATE_SCHEDULE;
const TRIMESTER_SCHEDULE = COLLEGIATE_SCHEDULE;

function getScheduleForGrade(grade) {
  if (grade <= 2) return GRADE_1_2_SCHEDULE;
  if (grade <= 4) return GRADE_3_4_SCHEDULE;
  if (grade <= 8) return MIDDLE_SCHOOL_SCHEDULE;
  if (grade <= 12) return HIGH_SCHOOL_SCHEDULE;
  return COLLEGIATE_SCHEDULE;
}

function getOriginalSheetsForGrade(grade) {
  if (grade === 1) {
    const sheets = [];
    for (let i = 1; i <= 60; i++) {
      const pad = String(i).padStart(2, '0');
      sheets.push({
        num: i,
        file: `assets/images/saiva-neri/grade1/p${pad}.jpg`,
        title: `பக்கம் ${i} (Page ${i})`
      });
    }
    return sheets;
  } else if (grade === 2) {
    const sheets = [];
    for (let i = 1; i <= 64; i++) {
      const pad = String(i).padStart(2, '0');
      let ext = 'jpg';
      if (i === 1 || i === 64) ext = 'png';
      sheets.push({
        num: i,
        file: `assets/images/saiva-neri/grade2/p${pad}.${ext}`,
        title: `பக்கம் ${i} (Page ${i})`
      });
    }
    return sheets;
  }
  return [];
}

function isBookChapterQuizPassed(grade, bookKey, chapterNum) {
  try {
    return localStorage.getItem(`gkd_quiz_${grade}_${bookKey}_${chapterNum}`) === 'true';
  } catch (e) {
    return false;
  }
}

function getGradeProgressMetrics(grade) {
  const activeBooks = getBooksMetadataForGrade(grade);
  let completedCount = 0;
  let quizCount = 0;
  let notesCount = 0;
  let bookMetrics = {};

  activeBooks.forEach(book => {
    let bookDone = 0;
    for (let c = 1; c <= 7; c++) {
      if (isBookChapterCompleted(grade, book.id, c)) {
        completedCount++;
        bookDone++;
      }
      if (isBookChapterQuizPassed(grade, book.id, c)) {
        quizCount++;
      }
      if (localStorage.getItem(`gkd_note_${grade}_${book.id}_${c}`)) {
        notesCount++;
      }
    }
    bookMetrics[book.id] = bookDone;
  });

  const totalChapters = activeBooks.length * 7;
  const percentage = totalChapters > 0 ? Math.round((completedCount / totalChapters) * 100) : 0;
  const totalXp = (completedCount * 50) + (quizCount * 100) + (notesCount * 25);

  let levelTitle = 'பால சாதகன் (Young Seeker)';
  if (grade <= 2) {
    if (totalXp >= 900) levelTitle = 'மழலை நற்செயல் வித்தகர் (Infant Action Master)';
    else if (totalXp >= 500) levelTitle = 'பால நற்செயல் சாதகன் (Young Action Seeker)';
    else if (totalXp >= 200) levelTitle = 'விளையாட்டு சாதகன் (Play & Learn Seeker)';
    else levelTitle = 'மழலை சாதகன் (Little Seeker)';
  } else if (grade <= 4) {
    if (totalXp >= 1800) levelTitle = 'பால தர்ம வித்வான் (Primary Dharma Master)';
    else if (totalXp >= 1000) levelTitle = 'பால நற்பண்பாளர் (Primary Virtue Scholar)';
    else if (totalXp >= 400) levelTitle = 'தர்ம பாலன் (Dharmic Student)';
    else levelTitle = 'பால சாதகன் (Young Seeker)';
  } else if (grade <= 8) {
    if (totalXp >= 4500) levelTitle = 'இளம் குருகுல வித்வான் (Junior Ashram Master)';
    else if (totalXp >= 2500) levelTitle = 'இளம் நற்பண்பாளர் (Middle School Scholar)';
    else if (totalXp >= 1000) levelTitle = 'தர்ம வித்யார்த்தி (Dharmic Student)';
    else levelTitle = 'வித்யா சாதகன் (Vedic Seeker)';
  } else if (grade <= 12) {
    if (totalXp >= 5500) levelTitle = 'உயர்நிலைக் குருகுல வித்வான் (Senior Gurukula Master)';
    else if (totalXp >= 3000) levelTitle = 'உயர்நிலை நற்பண்பாளர் (Senior Dharmic Scholar)';
    else if (totalXp >= 1200) levelTitle = 'தர்ம வித்யார்த்தி (Dharmic Student)';
    else levelTitle = 'வித்யா சாதகன் (Vedic Seeker)';
  } else {
    if (totalXp >= 6000) levelTitle = 'ஆசிரம வித்வான் (Ashram Master)';
    else if (totalXp >= 3500) levelTitle = 'குருகுல நற்பண்பாளர் (Gurukula Scholar)';
    else if (totalXp >= 1500) levelTitle = 'தர்ம வித்யார்த்தி (Dharmic Student)';
    else levelTitle = 'வித்யா சாதகன் (Vedic Seeker)';
  }

  let unlockedBadges = 0;
  activeBooks.forEach(b => {
    if (bookMetrics[b.id] === 7) unlockedBadges++;
  });

  return {
    completedCount,
    totalChapters,
    percentage,
    quizCount,
    notesCount,
    totalXp,
    levelTitle,
    bookMetrics,
    unlockedBadges,
    totalBadges: activeBooks.length
  };
}

let activeClassroomTab = 'classwork';

function initClassroomApp(grade) {
  const shelf = document.getElementById('booksShelfTabs');
  const workspace = document.getElementById('bookReaderWorkspace');
  if (!shelf && !workspace) return;

  let mount = document.getElementById('gurukulaClassroomApp');
  if (!mount) {
    mount = document.createElement('section');
    mount.id = 'gurukulaClassroomApp';
    mount.className = 'classroom-shell';

    // Wrap classwork elements in panel
    let classworkPanel = document.getElementById('classroomTabClasswork');
    if (!classworkPanel) {
      classworkPanel = document.createElement('div');
      classworkPanel.id = 'classroomTabClasswork';
      classworkPanel.className = 'classroom-panel active';

      const booksAnchor = document.getElementById('books');
      const targetParent = (booksAnchor ? booksAnchor.parentNode : shelf.parentNode);

      // Move shelf heading and elements
      if (booksAnchor) {
        targetParent.insertBefore(classworkPanel, booksAnchor);
        classworkPanel.appendChild(booksAnchor);
      } else {
        targetParent.insertBefore(classworkPanel, shelf);
      }

      // Collect shelf siblings up to workspace
      const prevHeading = shelf.previousElementSibling;
      if (prevHeading && prevHeading !== booksAnchor && prevHeading.querySelector && (prevHeading.querySelector('h3') || prevHeading.innerText.includes('ஆசிரம'))) {
        classworkPanel.appendChild(prevHeading);
      }
      classworkPanel.appendChild(shelf);
      if (workspace) classworkPanel.appendChild(workspace);

      // Insert mount right before classwork panel
      targetParent.insertBefore(mount, classworkPanel);
    }
  }

  const studentName = localStorage.getItem('gkd_student_name') || 'மாணவர்';
  const metrics = getGradeProgressMetrics(grade);
  const classCode = `GKD-G${grade < 10 ? '0' + grade : grade}`;
  const hasOriginalSheets = (grade === 1 || grade === 2);

  let mainTitle = '';
  let termDesc = '';
  let classworkTabTitle = '';

  if (grade <= 2) {
    mainTitle = `தரம் ${grade} — மழலைப் பருவம் 3 மாதப் பயில்வு (Infant 12-Week Academy)`;
    termDesc = `மழலைப் பருவம் • 1 ஆசிரமப் பாடநூல் (நற்செயல்) • 7 அத்தியாயங்கள் • விளையாடிப் பயிலல், பகிர்தல் &amp; 3 Ds நெறிமுறை`;
    classworkTabTitle = `பாடப் பணிகள் (Classwork • 1 நூல்)`;
  } else if (grade <= 4) {
    mainTitle = `தரம் ${grade} — தொடக்கப் பள்ளி 3 மாதப் பருவம் (Primary 12-Week Academy)`;
    termDesc = `பாலப் பருவம் • 2 முதன்மை ஆசிரமப் பாடநூல்கள் (நற்செயல், நற்பண்பு) • 14 அத்தியாயங்கள் • விளையாடிப் பயிலல் &amp; நற்பண்பு`;
    classworkTabTitle = `பாடப் பணிகள் (Classwork • 2 நூல்கள்)`;
  } else if (grade <= 8) {
    mainTitle = `தரம் ${grade} — நடுநிலைப் பள்ளி 3 மாதப் பருவம் (Middle School 12-Week Academy)`;
    termDesc = `இளம் பருவம் • 5 ஆசிரமப் பாடநூல்கள் (நன்னெறி, நல்லறம், நற்பண்பு, நற்துணை, நற்செயல்) • 35 அத்தியாயங்கள் • தினசரி சாதனா &amp; 3 Ds`;
    classworkTabTitle = `பாடப் பணிகள் (Classwork • 5 நூல்கள்)`;
  } else if (grade <= 12) {
    mainTitle = `தரம் ${grade} — உயர்நிலைப் பள்ளி 3 மாதப் பருவம் (High School 12-Week Academy)`;
    termDesc = `உயர்நிலைப் பருவம் • 6 ஆசிரமப் பாடநூல்கள் (நன்னெறி, நல்லறம், நற்பண்பு, நற்துணை, நற்சொல், நற்செயல்) • 42 அத்தியாயங்கள் • தர்ம நெறி &amp; வாழ்வியல் சாதனா`;
    classworkTabTitle = `பாடப் பணிகள் (Classwork • 6 நூல்கள்)`;
  } else {
    mainTitle = `உயர்கல்வி வித்யாபீடம் — 3 மாத காலப் பருவம் (Higher Studies 12-Week Academy)`;
    termDesc = `உயர்கல்விப் பருவம் • 7 ஆசிரமப் பாடநூல்கள் • 49 அத்தியாயங்கள் • வேத-நவீன அறிவியல் சங்கமம் &amp; 3 Ds நெறிமுறை`;
    classworkTabTitle = `பாடப் பணிகள் (Classwork • 7 நூல்கள்)`;
  }

  mount.innerHTML = `
    <!-- 1. Classroom Header Card -->
    <div class="classroom-header-card">
      <div class="classroom-header-top">
        <div class="classroom-title-box">
          <div class="classroom-sub-pill">
            <span>🌿</span>
            <span>வித்யா குடீரம் இணைய வகுப்பறை • Gurukula Digital Classroom</span>
          </div>
          <h2 class="classroom-main-title">${mainTitle}</h2>
          <p class="classroom-term-desc">${termDesc}</p>
        </div>
        <div class="classroom-badges-strip">
          <div class="classroom-chip classroom-chip-gold" title="வகுப்புக் குறியீடு">
            <span>🏷️ ${classCode}</span>
          </div>
          <button type="button" class="classroom-chip classroom-chip-btn" onclick="editStudentName()" title="மாணவர் பெயரை மாற்றுக">
            <span>👤</span>
            <span id="classroomStudentNameText">${studentName}</span>
            <span style="font-size:0.75rem; color:var(--gold); margin-left:4px;">✏️</span>
          </button>
        </div>
      </div>

      <div class="classroom-progress-row">
        <div>
          <div class="classroom-progress-label">
            <span id="classroomProgressLabel">${metrics.completedCount} / ${metrics.totalChapters} அத்தியாயங்கள் நிறைவு (${metrics.percentage}%)</span>
            <span style="color:var(--gold-soft); font-size:0.8rem;">${metrics.levelTitle}</span>
          </div>
          <div class="classroom-progress-track">
            <div class="classroom-progress-fill" id="classroomProgressFill" style="width: ${metrics.percentage}%;"></div>
          </div>
        </div>
        <div class="classroom-xp-badge-lg" id="classroomHeaderXpBadge" title="உங்கள் தர்ம சாதனா புள்ளிகள்">
          <span>✨</span>
          <span>${metrics.totalXp.toLocaleString()} தர்ம XP</span>
        </div>
      </div>
    </div>

    <!-- 2. Classroom Mode Navigation Tabs -->
    <nav class="classroom-nav-tabs" aria-label="வகுப்பறை பிரிவுகள்">
      <button type="button" class="classroom-tab-btn ${activeClassroomTab === 'classwork' ? 'active' : ''}" id="btnTabClasswork" onclick="switchClassroomTab('classwork')">
        <span>📑</span>
        <span>${classworkTabTitle}</span>
      </button>
      ${hasOriginalSheets ? `
      <button type="button" class="classroom-tab-btn ${activeClassroomTab === 'authorSheets' ? 'active' : ''}" id="btnTabAuthorSheets" onclick="switchClassroomTab('authorSheets')">
        <span>📖</span>
        <span>ஆசிரியர் மூலப் பாடநூல் (Author's Original Sheets)</span>
        <span class="classroom-tab-badge">${grade === 1 ? '60 ஏடுகள்' : '64 ஏடுகள்'}</span>
      </button>
      ` : ''}
      <button type="button" class="classroom-tab-btn ${activeClassroomTab === 'schedule' ? 'active' : ''}" id="btnTabSchedule" onclick="switchClassroomTab('schedule')">
        <span>📅</span>
        <span>3 மாத கால அட்டவணை (12-Week Roadmap)</span>
        <span class="classroom-tab-badge">12 வாரங்கள்</span>
      </button>
      <button type="button" class="classroom-tab-btn ${activeClassroomTab === 'mastery' ? 'active' : ''}" id="btnTabMastery" onclick="switchClassroomTab('mastery')">
        <span>📊</span>
        <span>மாணவர் முன்னேற்றப் பலகை (Mastery Tracker)</span>
        <span class="classroom-tab-badge">${metrics.unlockedBadges}/${metrics.totalBadges} பதக்கங்கள்</span>
      </button>
      <button type="button" class="classroom-tab-btn ${activeClassroomTab === 'diploma' ? 'active' : ''}" id="btnTabDiploma" onclick="switchClassroomTab('diploma')">
        <span>🎓</span>
        <span>பருவப் பட்டயச் சான்றிதழ் (Grade Term Diploma)</span>
      </button>
    </nav>

    <!-- 3. Panels for Modes -->
    ${hasOriginalSheets ? `
    <div id="classroomTabAuthorSheets" class="classroom-panel ${activeClassroomTab === 'authorSheets' ? 'active' : ''}">
      ${renderAuthorSheetsPanelHtml(grade)}
    </div>
    ` : ''}

    <div id="classroomTabSchedule" class="classroom-panel ${activeClassroomTab === 'schedule' ? 'active' : ''}">
      ${renderSchedulePanelHtml(grade)}
    </div>

    <div id="classroomTabMastery" class="classroom-panel ${activeClassroomTab === 'mastery' ? 'active' : ''}">
      ${renderMasteryPanelHtml(grade)}
    </div>

    <div id="classroomTabDiploma" class="classroom-panel ${activeClassroomTab === 'diploma' ? 'active' : ''}">
      ${renderDiplomaPanelHtml(grade)}
    </div>
  `;

  // Apply tab state
  applyClassroomTabVisibility(activeClassroomTab);
}

function switchClassroomTab(tabKey) {
  activeClassroomTab = tabKey;

  document.querySelectorAll('.classroom-tab-btn').forEach(btn => btn.classList.remove('active'));
  if (tabKey === 'classwork') {
    const btn = document.getElementById('btnTabClasswork');
    if (btn) btn.classList.add('active');
  } else if (tabKey === 'authorSheets') {
    const btn = document.getElementById('btnTabAuthorSheets');
    if (btn) btn.classList.add('active');
    const p = document.getElementById('classroomTabAuthorSheets');
    if (p) p.innerHTML = renderAuthorSheetsPanelHtml(currentGrade);
  } else if (tabKey === 'schedule') {
    const btn = document.getElementById('btnTabSchedule');
    if (btn) btn.classList.add('active');
    const p = document.getElementById('classroomTabSchedule');
    if (p) p.innerHTML = renderSchedulePanelHtml(currentGrade);
  } else if (tabKey === 'mastery') {
    const btn = document.getElementById('btnTabMastery');
    if (btn) btn.classList.add('active');
    const p = document.getElementById('classroomTabMastery');
    if (p) p.innerHTML = renderMasteryPanelHtml(currentGrade);
  } else if (tabKey === 'diploma') {
    const btn = document.getElementById('btnTabDiploma');
    if (btn) btn.classList.add('active');
    const p = document.getElementById('classroomTabDiploma');
    if (p) p.innerHTML = renderDiplomaPanelHtml(currentGrade);
  }

  applyClassroomTabVisibility(tabKey);
}

function applyClassroomTabVisibility(tabKey) {
  const pClasswork = document.getElementById('classroomTabClasswork');
  const pAuthorSheets = document.getElementById('classroomTabAuthorSheets');
  const pSchedule = document.getElementById('classroomTabSchedule');
  const pMastery = document.getElementById('classroomTabMastery');
  const pDiploma = document.getElementById('classroomTabDiploma');

  if (pClasswork) pClasswork.style.display = (tabKey === 'classwork') ? 'block' : 'none';
  if (pAuthorSheets) pAuthorSheets.style.display = (tabKey === 'authorSheets') ? 'block' : 'none';
  if (pSchedule) pSchedule.style.display = (tabKey === 'schedule') ? 'block' : 'none';
  if (pMastery) pMastery.style.display = (tabKey === 'mastery') ? 'block' : 'none';
  if (pDiploma) pDiploma.style.display = (tabKey === 'diploma') ? 'block' : 'none';
}

function updateClassroomStats() {
  const metrics = getGradeProgressMetrics(currentGrade);

  // Update header progress bar & stats
  const fill = document.getElementById('classroomProgressFill');
  if (fill) fill.style.width = `${metrics.percentage}%`;

  const label = document.getElementById('classroomProgressLabel');
  if (label) label.innerText = `${metrics.completedCount} / ${metrics.totalChapters} அத்தியாயங்கள் நிறைவு (${metrics.percentage}%)`;

  const xpBadge = document.getElementById('classroomHeaderXpBadge');
  if (xpBadge) xpBadge.innerHTML = `<span>✨</span> <span>${metrics.totalXp.toLocaleString()} தர்ம XP</span>`;

  // Update shelf tabs badges
  renderBookShelfTabs();

  // If schedule, mastery, diploma, or author sheets panel is active, refresh
  if (activeClassroomTab === 'schedule') {
    const p = document.getElementById('classroomTabSchedule');
    if (p) p.innerHTML = renderSchedulePanelHtml(currentGrade);
  } else if (activeClassroomTab === 'mastery') {
    const p = document.getElementById('classroomTabMastery');
    if (p) p.innerHTML = renderMasteryPanelHtml(currentGrade);
  } else if (activeClassroomTab === 'diploma') {
    const p = document.getElementById('classroomTabDiploma');
    if (p) p.innerHTML = renderDiplomaPanelHtml(currentGrade);
  } else if (activeClassroomTab === 'authorSheets') {
    const p = document.getElementById('classroomTabAuthorSheets');
    if (p) p.innerHTML = renderAuthorSheetsPanelHtml(currentGrade);
  }
}

// Author's Original Textbook Sheets Gallery & Modal
function renderAuthorSheetsPanelHtml(grade) {
  const sheets = getOriginalSheetsForGrade(grade);
  if (sheets.length === 0) {
    return `<div style="text-align:center; padding:30px; color:#94a3b8;">இவ்வகுப்பிற்கு மூலப் பாடநூல் ஏடுகள் கிடைக்கவில்லை.</div>`;
  }

  let html = `
    <div class="author-sheets-container">
      <div style="background:linear-gradient(135deg, rgba(212, 175, 55, 0.12), rgba(15, 23, 42, 0.9)); border:1px solid rgba(212, 175, 55, 0.35); border-radius:12px; padding:18px 22px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:14px;">
        <div style="max-width:750px;">
          <div style="color:var(--gold-bright); font-size:1.15rem; font-weight:800; margin-bottom:6px; display:flex; align-items:center; gap:8px;">
            <span>📖</span>
            <span>ஆசிரியர் மூலப் பாடநூல் ஏடுகள் (Author's Original Google Sites Textbook Sheets)</span>
            <span class="classroom-tab-badge" style="background:var(--gold); color:#000; font-weight:800;">மொத்தம் ${sheets.length} பக்கங்கள்</span>
          </div>
          <p style="color:#cbd5e1; font-size:0.9rem; line-height:1.6; margin:0;">
            குரு குல ஆசிரமத்தின் ஆசிரியர் கைப்பட அமைத்த தொடக்கப் பள்ளி மூலப் பாடநூலின் அசல் சித்திரப் பக்கங்கள். மழலையர் விளையாடிப் பயிலவும், தமிழ் எழுத்துக்கள் மற்றும் எளிய சைவ நெறி வழிபாட்டுப் பாடல்களை வண்ணப் படங்களுடன் வாசிக்கவும் உருவான மூல ஏடுகள்.
          </p>
        </div>
        <div style="display:flex; align-items:center; gap:10px;">
          <button type="button" class="sheet-btn sheet-btn-view" onclick="openAuthorSheetModal(${grade}, 1)" style="font-size:0.88rem; padding:8px 18px;">
            <span>🔍 பக்கம் 1 முதல் வாசிக்கத் தொடங்குக</span>
          </button>
        </div>
      </div>

      <!-- Quick Page Search / Filter -->
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
        <div style="color:#94a3b8; font-size:0.86rem;">
          ஏதேனும் ஒரு பக்கத்தைச் சொடுக்கி முழுத் திரையில் பெரிதாக்கிக் காணலாம்:
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <label for="authorSheetJump" style="color:#cbd5e1; font-size:0.82rem; font-weight:600;">பக்கத்திற்குச் செல்க:</label>
          <select id="authorSheetJump" class="context-search-input" style="width:auto; padding:4px 10px; font-size:0.84rem;" onchange="openAuthorSheetModal(${grade}, parseInt(this.value))">
            ${sheets.map(s => `<option value="${s.num}">பக்கம் ${s.num}</option>`).join('')}
          </select>
        </div>
      </div>

      <!-- 60 / 64 Sheets Grid -->
      <div class="sheets-grid" style="margin-top:10px;">
  `;

  sheets.forEach(s => {
    html += `
      <div class="sheet-card">
        <div class="sheet-header">
          <span>${s.title}</span>
          <span style="font-size:0.75rem; color:var(--gold);">தரம் ${grade}</span>
        </div>
        <div class="sheet-thumb" onclick="openAuthorSheetModal(${grade}, ${s.num})" title="${s.title} பெரிதாக்குக">
          <img src="${s.file}" alt="${s.title}" loading="lazy">
          <div class="sheet-zoom-overlay">
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
          </div>
        </div>
        <div class="sheet-actions">
          <button type="button" class="sheet-btn sheet-btn-view" onclick="openAuthorSheetModal(${grade}, ${s.num})">
            <span>பெரிதாக்குக</span>
          </button>
          <a href="${s.file}" target="_blank" rel="noopener noreferrer" class="sheet-btn sheet-btn-direct" title="நேரடி இணைப்பு">
            <span>மூலம் ↗</span>
          </a>
        </div>
      </div>
    `;
  });

  html += `
      </div>
    </div>
  `;
  return html;
}

window.currentAuthorSheetGrade = 1;
window.currentAuthorSheetNum = 1;

window.openAuthorSheetModal = function(grade, sheetNum) {
  const sheets = getOriginalSheetsForGrade(grade);
  if (!sheets || sheets.length === 0) return;
  if (sheetNum < 1) sheetNum = 1;
  if (sheetNum > sheets.length) sheetNum = sheets.length;

  window.currentAuthorSheetGrade = grade;
  window.currentAuthorSheetNum = sheetNum;

  let modal = document.getElementById('authorSheetLightboxModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'authorSheetLightboxModal';
    modal.className = 'art-lightbox-modal';
    modal.innerHTML = `
      <div class="art-lightbox-backdrop" onclick="closeAuthorSheetModal()"></div>
      <div class="art-lightbox-content" style="max-width: 900px; max-height: 92vh; display:flex; flex-direction:column;">
        <div class="art-lightbox-header">
          <div class="art-lightbox-title-wrap">
            <span class="chap-badge" id="authorSheetGradeBadge">தரம் 1 மூல ஏடு</span>
            <strong id="authorSheetPageTitle" style="color:var(--gold-bright); font-size:1.05rem;">பக்கம் 1</strong>
          </div>
          <div class="art-lightbox-actions">
            <span id="authorSheetCounter" style="color:#94a3b8; font-size:0.85rem; margin-right:8px;">1 / 60</span>
            <a id="authorSheetDlBtn" href="#" download class="art-lightbox-btn" title="ஏட்டைப் பதிவிறக்குக">
              <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            </a>
            <button type="button" class="art-lightbox-btn" onclick="toggleAuthorSheetZoom()" title="பெரிதாக்குக / சுருக்குக">
              <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            </button>
            <button type="button" class="art-lightbox-btn art-lightbox-close" onclick="closeAuthorSheetModal()" title="மூடுக">
              <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>
        </div>

        <div class="art-lightbox-viewport" style="flex:1; overflow:auto; text-align:center; padding:10px;">
          <img id="authorSheetImg" src="" alt="" style="max-height:74vh; width:auto; border-radius:8px; box-shadow:0 8px 30px rgba(0,0,0,0.8); cursor:zoom-in;" onclick="toggleAuthorSheetZoom()">
        </div>

        <div class="art-lightbox-footer" style="padding:10px 16px; display:flex; justify-content:space-between; align-items:center; background:rgba(0,0,0,0.6);">
          <button type="button" class="sheet-btn" onclick="prevAuthorSheet()" style="cursor:pointer;" title="முந்தைய பக்கம்">
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg> <span>முந்தைய பக்கம்</span>
          </button>
          <span style="color:#cbd5e1; font-size:0.85rem;" id="authorSheetFooterNote">ஆசிரியர் மூலப் பாடநூல் அசல் ஏடு</span>
          <button type="button" class="sheet-btn sheet-btn-view" onclick="nextAuthorSheet()" style="cursor:pointer;" title="அடுத்த பக்கம்">
            <span>அடுத்த பக்கம்</span> <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
          </button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
  }

  const cur = sheets[sheetNum - 1];
  const imgEl = document.getElementById('authorSheetImg');
  const titleEl = document.getElementById('authorSheetPageTitle');
  const badgeEl = document.getElementById('authorSheetGradeBadge');
  const counterEl = document.getElementById('authorSheetCounter');
  const dlBtn = document.getElementById('authorSheetDlBtn');

  if (imgEl) {
    imgEl.src = cur.file;
    imgEl.alt = cur.title;
    imgEl.classList.remove('zoomed');
    imgEl.style.maxHeight = '74vh';
  }
  if (titleEl) titleEl.innerText = cur.title;
  if (badgeEl) badgeEl.innerText = `தரம் ${grade} மூல ஏடு`;
  if (counterEl) counterEl.innerText = `${sheetNum} / ${sheets.length}`;
  if (dlBtn) {
    dlBtn.href = cur.file;
    dlBtn.setAttribute('download', cur.file.split('/').pop());
  }

  modal.classList.add('active');
  document.body.style.overflow = 'hidden';
};

window.closeAuthorSheetModal = function() {
  const modal = document.getElementById('authorSheetLightboxModal');
  if (modal) modal.classList.remove('active');
  document.body.style.overflow = '';
};

window.nextAuthorSheet = function() {
  const sheets = getOriginalSheetsForGrade(window.currentAuthorSheetGrade || 1);
  if (!sheets || sheets.length === 0) return;
  let next = (window.currentAuthorSheetNum || 1) + 1;
  if (next > sheets.length) next = 1;
  window.openAuthorSheetModal(window.currentAuthorSheetGrade, next);
};

window.prevAuthorSheet = function() {
  const sheets = getOriginalSheetsForGrade(window.currentAuthorSheetGrade || 1);
  if (!sheets || sheets.length === 0) return;
  let prev = (window.currentAuthorSheetNum || 1) - 1;
  if (prev < 1) prev = sheets.length;
  window.openAuthorSheetModal(window.currentAuthorSheetGrade, prev);
};

window.toggleAuthorSheetZoom = function() {
  const imgEl = document.getElementById('authorSheetImg');
  if (imgEl) {
    imgEl.classList.toggle('zoomed');
    imgEl.style.cursor = imgEl.classList.contains('zoomed') ? 'zoom-out' : 'zoom-in';
    imgEl.style.maxHeight = imgEl.classList.contains('zoomed') ? 'none' : '74vh';
  }
};

document.addEventListener('keydown', (e) => {
  const modal = document.getElementById('authorSheetLightboxModal');
  if (!modal || !modal.classList.contains('active')) return;

  if (e.key === 'Escape') {
    window.closeAuthorSheetModal();
  } else if (e.key === 'ArrowRight') {
    window.nextAuthorSheet();
  } else if (e.key === 'ArrowLeft') {
    window.prevAuthorSheet();
  }
});

function renderSchedulePanelHtml(grade) {
  const schedule = getScheduleForGrade(grade);
  const activeMeta = getBooksMetadataForGrade(grade);

  let html = `
    <div class="trimester-roadmap-container">
      <div style="background:rgba(56, 189, 248, 0.1); border:1px solid rgba(56, 189, 248, 0.25); border-radius:10px; padding:12px 16px; color:#cbd5e1; font-size:0.88rem; line-height:1.6;">
        💡 <strong>3 மாத காலப் பருவ நெறிமுறை (Trimester Methodology):</strong> ஒரு பருவத்திற்கு 12 வாரங்கள். ஒவ்வொரு வாரமும் நியமிக்கப்பட்ட அத்தியாயங்களை வாசித்து, மூலப் பாடலை மனனம் செய்து, மெய்ஞ்ஞானக் கதையையும் இல்லற தர்மப் பயிற்சியையும் பூர்த்தி செய்க. வாரந்தோறும் சரிபார்க்கும் பெட்டியை [✓] சொடுக்கவும்.
      </div>
  `;

  schedule.forEach(m => {
    let monthDone = 0;
    let monthTotal = 0;

    m.weeks.forEach(w => {
      w.lessons.forEach(l => {
        monthTotal++;
        if (isBookChapterCompleted(grade, l.book, l.chap)) monthDone++;
      });
    });

    const isMonthComplete = (monthDone === monthTotal);

    html += `
      <div class="trimester-month-card">
        <div class="trimester-month-header">
          <div>
            <h3 class="trimester-month-title">
              <span>📅</span>
              <span>${m.title}</span>
            </h3>
            <p style="color:#94a3b8; font-size:0.85rem; margin:4px 0 0 0;">${m.desc}</p>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            <span class="trimester-checkpoint-badge">${m.checkpoint}</span>
            <span style="font-size:0.85rem; font-weight:700; color:${isMonthComplete ? '#34d399' : 'var(--gold)'};">${monthDone} / ${monthTotal} நிறைவு</span>
          </div>
        </div>

        <div class="trimester-weeks-grid">
    `;

    m.weeks.forEach(w => {
      let weekDone = 0;
      const weekTotal = w.lessons.length;
      w.lessons.forEach(l => {
        if (isBookChapterCompleted(grade, l.book, l.chap)) weekDone++;
      });
      const isWeekComplete = (weekDone === weekTotal);

      html += `
        <div class="trimester-week-card">
          <div class="trimester-week-header">
            <span class="trimester-week-title">${w.title}</span>
            <span class="trimester-week-status ${isWeekComplete ? 'completed' : ''}">${isWeekComplete ? '✓ நிறைவு' : `${weekDone}/${weekTotal}`}</span>
          </div>
          <div style="font-size:0.78rem; color:#94a3b8; line-height:1.4;">${w.theme}</div>

          <div class="week-lessons-list">
      `;

      w.lessons.forEach(l => {
        const isDone = isBookChapterCompleted(grade, l.book, l.chap);
        const bMeta = activeMeta.find(b => b.id === l.book) || { name: l.book, color: '#38bdf8' };
        
        let chapTitle = `அத்தியாயம் ${l.chap}`;
        if (loadedBookData?.books?.[l.book]?.chapters) {
          const chapObj = loadedBookData.books[l.book].chapters.find(c => c.chapterNumber === l.chap);
          if (chapObj && chapObj.title) chapTitle = chapObj.title;
        }

        html += `
          <div class="week-lesson-row ${isDone ? 'is-done' : ''}">
            <div class="week-lesson-left">
              <button type="button" class="week-lesson-check ${isDone ? 'checked' : ''}" onclick="toggleWeekChapterCompletion(${grade}, '${l.book}', ${l.chap})" title="${isDone ? 'நிறைவு செய்ததை மீட்டமைக்க' : 'நிறைவு செய்ததாகக் குறிக்க'}">
                ${isDone ? '✓' : ''}
              </button>
              <div class="week-lesson-text" title="${bMeta.name} அத் ${l.chap}: ${chapTitle}">
                <strong style="color:${bMeta.color};">${bMeta.name} ${l.chap}:</strong> ${chapTitle}
              </div>
            </div>
            <button type="button" class="week-lesson-open-btn" onclick="openClassroomChapter('${l.book}', ${l.chap})">
              <span>படிக்க</span>
              <span>&rarr;</span>
            </button>
          </div>
        `;
      });

      html += `
          </div>
        </div>
      `;
    });

    html += `
        </div>
      </div>
    `;
  });

  html += `</div>`;
  return html;
}

function renderMasteryPanelHtml(grade) {
  const metrics = getGradeProgressMetrics(grade);
  const activeBooks = getBooksMetadataForGrade(grade);

  let masteryTitle = '7 ஆசிரம நூல்களின் தேர்ச்சி நிலை (7 Sacred Books Mastery)';
  if (grade <= 2) masteryTitle = '1 ஆசிரம நூலின் தேர்ச்சி நிலை (Infant 1 Book Mastery • நற்செயல்)';
  else if (grade <= 4) masteryTitle = '2 முதன்மை ஆசிரம நூல்களின் தேர்ச்சி நிலை (Primary 2 Books Mastery • நற்செயல், நற்பண்பு)';
  else if (grade <= 8) masteryTitle = '5 ஆசிரம நூல்களின் தேர்ச்சி நிலை (Middle School 5 Books Mastery)';
  else if (grade <= 12) masteryTitle = '6 ஆசிரம நூல்களின் தேர்ச்சி நிலை (High School 6 Books Mastery)';

  let html = `
    <div>
      <!-- Mastery Metrics Strip -->
      <div class="mastery-overview-strip">
        <div class="mastery-metric-card">
          <div class="mastery-metric-num">${metrics.totalChapters}</div>
          <div class="mastery-metric-label">பருவப் பாடங்கள் (Total Chapters)</div>
        </div>
        <div class="mastery-metric-card">
          <div class="mastery-metric-num" style="color:#10b981;">${metrics.completedCount}</div>
          <div class="mastery-metric-label">வாசித்து உணர்ந்தவை (${metrics.percentage}%)</div>
        </div>
        <div class="mastery-metric-card">
          <div class="mastery-metric-num" style="color:#38bdf8;">${metrics.totalXp.toLocaleString()}</div>
          <div class="mastery-metric-label">தர்ம சாதனா புள்ளிகள் (Vedic XP)</div>
        </div>
        <div class="mastery-metric-card">
          <div class="mastery-metric-num" style="color:var(--gold-bright);">${metrics.unlockedBadges} / ${metrics.totalBadges}</div>
          <div class="mastery-metric-label">நிறைவுப் பதக்கங்கள் (Ashram Badges)</div>
        </div>
      </div>

      <!-- Books Mastery Cards Grid -->
      <div style="margin: 20px 0 12px; display:flex; justify-content:space-between; align-items:center;">
        <h3 style="color:#ffffff; font-size:1.15rem; font-weight:800; margin:0;">
          ${masteryTitle}
        </h3>
        <span style="font-size:0.8rem; color:#94a3b8;">ஒவ்வொரு நூலிலும் 7 அத்தியாயங்கள்</span>
      </div>

      <div class="mastery-books-grid">
  `;

  const bookBadges = {
    'narcheyal': '☀️ நற்செயல் கர்மவீரர் (Action Champion & 3 Ds)',
    'nalvazhi': '⭐ நற்பண்பு நேர்மையாளர் (Virtue & Truth Bearer)',
    'nanneri': '🏅 நன்னெறி சுடர் (Conduct Pillar)',
    'nallaram': '🛡️ நல்லறச் செம்மல் (Dharma Champion)',
    'narthunai': '🪔 நற்துணை யோகி (Divine Refuge)',
    'narchol': '🌸 நற்சொல் வள்ளல் (Sweet Word Master)',
    'narchinthanai': '⚛️ நற்சிந்தனை ஞானி (Wisdom Seeker)'
  };

  activeBooks.forEach((book, idx) => {
    const done = metrics.bookMetrics[book.id] || 0;
    const isMastered = (done === 7);
    const pct = Math.round((done / 7) * 100);

    let dotsHtml = '';
    for (let c = 1; c <= 7; c++) {
      const cDone = isBookChapterCompleted(grade, book.id, c);
      dotsHtml += `<span class="mastery-dot ${cDone ? 'done' : ''}" title="அத்தியாயம் ${c}: ${cDone ? 'நிறைவு பெற்றது' : 'படிக்க வேண்டியுள்ளது'}"></span>`;
    }

    const badgeName = bookBadges[book.id] || `${book.name} தேர்ச்சிப் பதக்கம்`;

    html += `
      <div class="mastery-book-card ${isMastered ? 'fully-completed' : ''}" style="--book-accent:${book.color};">
        <div class="mastery-book-header">
          <div>
            <div style="font-size:0.75rem; color:var(--gold); font-weight:700;">நூல் ${idx + 1}</div>
            <div class="mastery-book-title">${book.name}</div>
            <div style="font-size:0.78rem; color:#94a3b8;">${book.en}</div>
          </div>
          <button type="button" class="sheet-btn" onclick="switchClassroomTab('classwork'); switchBook('${book.id}');" style="font-size:0.75rem; padding:4px 10px;">
            படிக்க &rarr;
          </button>
        </div>

        <div>
          <div style="display:flex; justify-content:space-between; font-size:0.8rem; color:#cbd5e1; margin-bottom:4px; font-weight:600;">
            <span>முன்னேற்றம்: ${done} / 7</span>
            <span>${pct}%</span>
          </div>
          <div class="classroom-progress-track">
            <div class="classroom-progress-fill" style="width: ${pct}%; background:${book.color};"></div>
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:0.75rem; color:#94a3b8;">அத்தியாயங்கள்:</span>
          <div class="mastery-dots-row">${dotsHtml}</div>
        </div>

        <div class="mastery-badge-box ${isMastered ? 'unlocked' : ''}">
          <span>${isMastered ? '🏆' : '🔒'}</span>
          <span>${isMastered ? badgeName : `${badgeName} (இன்னும் ${7 - done} பாடம்)`}</span>
        </div>
      </div>
    `;
  });

  html += `
      </div>

      <!-- Student Saved Sacred Reflections (சங்கற்பக் குறிப்புகள்) -->
      <div style="margin-top:28px; background:rgba(15, 23, 42, 0.7); border:1px solid rgba(255, 255, 255, 0.1); border-radius:12px; padding:20px;">
        <h3 style="color:var(--gold-bright); font-size:1.1rem; font-weight:800; margin:0 0 12px 0;">
          📝 மாணவரின் தர்ம சங்கற்பக் குறிப்புகள் (Sacred Reflections Log)
        </h3>
        <p style="color:#94a3b8; font-size:0.85rem; margin-bottom:14px;">
          நீங்கள் அத்தியாயங்களின் முடிவில் எழுதிச் சேமித்த தினசரி தர்ம உறுதிமொழிகள் இங்கு தொகுக்கப்பட்டுள்ளன.
        </p>
        <div style="display:flex; flex-direction:column; gap:10px;">
  `;

  let notesCountFound = 0;
  activeBooks.forEach(b => {
    for (let c = 1; c <= 7; c++) {
      const note = localStorage.getItem(`gkd_note_${grade}_${b.id}_${c}`);
      if (note && note.trim().length > 0) {
        notesCountFound++;
        html += `
          <div style="background:rgba(0,0,0,0.35); border-left:3px solid ${b.color}; border-radius:6px; padding:10px 14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
              <strong style="color:${b.color}; font-size:0.85rem;">${b.name} • அத்தியாயம் ${c}</strong>
              <button type="button" class="week-lesson-open-btn" onclick="openClassroomChapter('${b.id}', ${c})">பாடத்திற்குச் செல்க</button>
            </div>
            <div style="color:#e2e8f0; font-size:0.9rem; line-height:1.6; font-style:italic;">"${note}"</div>
          </div>
        `;
      }
    }
  });

  if (notesCountFound === 0) {
    html += `
      <div style="text-align:center; padding:24px; color:#94a3b8; font-size:0.9rem;">
        இன்னும் குறிப்புகள் ஏதும் சேமிக்கப்படவில்லை. பாடங்களை வாசிக்கும் போது உங்கள் மன உணர்வுகளையும் தர்ம உறுதிமொழிகளையும் கீழே உள்ள குறிப்புப் பெட்டியில் எழுதிச் சேமிக்கவும்.
      </div>
    `;
  }

  html += `
        </div>
      </div>
    </div>
  `;

  return html;
}

function renderDiplomaPanelHtml(grade) {
  const metrics = getGradeProgressMetrics(grade);
  const studentName = localStorage.getItem('gkd_student_name') || 'மாணவர்';
  const todayStr = new Date().toLocaleDateString('ta-IN', { year: 'numeric', month: 'long', day: 'numeric' });

  let diplomaTitle = 'பருவ நிறைவுப் பட்டயச் சான்றிதழ்';
  let diplomaIntro = 'Diploma of Dharmic & Curricular Completion';
  let diplomaBody = '';

  if (grade <= 2) {
    diplomaTitle = 'மழலைப் பருவ நிறைவுப் பட்டயச் சான்றிதழ்';
    diplomaIntro = 'Infant Diploma of Dharmic Completion';
    diplomaBody = `
      இம்மாணவர் குரு குல தேசத்தின் <strong>தரம் ${grade}</strong> மழலைப் பருவப் பாடத்திட்டத்தில் உள்ள <strong>நற்செயல்</strong> ஆசிரமப் பாடநூல் (7 அத்தியாயங்கள் — விளையாடிப் பயிலல், பகிர்தல், உள்ளதைக் கொண்டு மகிழ்தல், காலையில் விழித்தல், தூய்மை, புன்னகைக் கண்ணியம் மற்றும் மூல ஏடுகள் பயிற்சி) அடங்கிய 3 மாத காலப் பருவப் பயில்வை முறைப்படி பயின்று, தர்ம நெறிகளையும் <strong>3 Ds (Duty, Discipline, Dignity)</strong> வாழ்வியல் நெறிமுறைகளையும் செவ்வனே உணர்ந்து <strong>${metrics.totalXp.toLocaleString()} தர்ம XP</strong> புள்ளிகளுடன் நிறைவு செய்துள்ளார் என ஆசிரம பீடத்தால் சான்றளிக்கப்படுகிறது.
    `;
  } else if (grade <= 4) {
    diplomaTitle = 'தொடக்கப் பள்ளிப் பருவ நிறைவுப் பட்டயச் சான்றிதழ்';
    diplomaIntro = 'Primary Diploma of Dharmic Completion';
    diplomaBody = `
      இம்மாணவர் குரு குல தேசத்தின் <strong>தரம் ${grade}</strong> வித்யா குடீரம் தொடக்கப் பள்ளிப் பாடத்திட்டத்தில் உள்ள <strong>2 முதன்மை ஆசிரமப் பாடநூல்கள்</strong> (நற்செயல், நற்பண்பு ஆகிய 14 அத்தியாயங்கள் — விளையாடிப் பயிலல், பகிர்தல், நற்பண்புகள், உண்மை பேசுதல், பெரியோர் பணிவு மற்றும் தினசரி சாதனா பயிற்சிகள்) அடங்கிய 3 மாத காலப் பருவப் பாடத்திட்டத்தை முறைப்படி பயின்று, தர்ம நெறிகளையும் <strong>3 Ds (Duty, Discipline, Dignity)</strong> வாழ்வியல் நெறிமுறைகளையும் செவ்வனே உணர்ந்து <strong>${metrics.totalXp.toLocaleString()} தர்ம XP</strong> புள்ளிகளுடன் நிறைவு செய்துள்ளார் என ஆசிரம பீடத்தால் சான்றளிக்கப்படுகிறது.
    `;
  } else if (grade <= 8) {
    diplomaTitle = 'நடுநிலைப் பள்ளிப் பருவ நிறைவுப் பட்டயச் சான்றிதழ்';
    diplomaIntro = 'Middle School Diploma of Dharmic Completion';
    diplomaBody = `
      இம்மாணவர் குரு குல தேசத்தின் <strong>தரம் ${grade}</strong> வித்யா குடீரம் நடுநிலைப் பள்ளிப் பாடத்திட்டத்தில் உள்ள <strong>5 ஆசிரமப் பாடநூல்கள்</strong> (நன்னெறி, நல்லறம், நற்பண்பு, நற்துணை, நற்செயல் ஆகிய 35 அத்தியாயங்கள் — தாய்-தந்தை வழிபாடு, ஜீவகாருண்யம், உண்மை நெறி, இறை பக்தி, 3 Ds வாழ்வியல் சாதனா) அடங்கிய 3 மாத காலப் பருவப் பாடத்திட்டத்தை முறைப்படி பயின்று, தர்ம நெறிகளையும் <strong>3 Ds (Duty, Discipline, Dignity)</strong> வாழ்வியல் நெறிமுறைகளையும் செவ்வனே உணர்ந்து <strong>${metrics.totalXp.toLocaleString()} தர்ம XP</strong> புள்ளிகளுடன் நிறைவு செய்துள்ளார் என ஆசிரம பீடத்தால் சான்றளிக்கப்படுகிறது.
    `;
  } else if (grade <= 12) {
    diplomaTitle = 'உயர்நிலைப் பள்ளிப் பருவ நிறைவுப் பட்டயச் சான்றிதழ்';
    diplomaIntro = 'High School Diploma of Dharmic Completion';
    diplomaBody = `
      இம்மாணவர் குரு குல தேசத்தின் <strong>தரம் ${grade}</strong> வித்யா குடீரம் உயர்நிலைப் பள்ளிப் பாடத்திட்டத்தில் உள்ள <strong>6 ஆசிரமப் பாடநூல்கள்</strong> (நன்னெறி, நல்லறம், நற்பண்பு, நற்துணை, நற்சொல், நற்செயல் ஆகிய 42 அத்தியாயங்கள் — அறநெறி, நல்லறம், வாய்மை, இறை சரணாகதி, நாவடக்கம், இனிய உரை, 3 Ds வாழ்வியல் சாதனா) அடங்கிய 3 மாத காலப் பருவப் பாடத்திட்டத்தை முறைப்படி பயின்று, தர்ம நெறிகளையும் <strong>3 Ds (Duty, Discipline, Dignity)</strong> வாழ்வியல் நெறிமுறைகளையும் செவ்வனே உணர்ந்து <strong>${metrics.totalXp.toLocaleString()} தர்ம XP</strong> புள்ளிகளுடன் நிறைவு செய்துள்ளார் என ஆசிரம பீடத்தால் சான்றளிக்கப்படுகிறது.
    `;
  } else {
    diplomaTitle = 'உயர்கல்விப் பருவ நிறைவுப் பட்டயச் சான்றிதழ்';
    diplomaIntro = 'Higher Studies Vedic Diploma of Dharmic Completion';
    diplomaBody = `
      இம்மாணவர் குரு குல தேசத்தின் <strong>உயர்கல்வி வித்யாபீடப்</strong> பாடத்திட்டத்தில் உள்ள <strong>7 ஆசிரமப் பாடநூல்கள்</strong> (நன்னெறி, நல்லறம், நற்பண்பு, நற்துணை, நற்சிந்தனை, நற்சொல், நற்செயல் ஆகிய 49 அத்தியாயங்கள் — வேத-நவீன அறிவியல் சங்கமம், குவாண்டம் இயற்பியல், வேதாந்தம், உபநிடதங்கள், தினசரி பஞ்ச மகா யாகங்கள் & 3 Ds) அடங்கிய 3 மாத காலப் பருவப் பாடத்திட்டத்தை முறைப்படி பயின்று, தர்ம நெறிகளையும் <strong>3 Ds (Duty, Discipline, Dignity)</strong> வாழ்வியல் நெறிமுறைகளையும் செவ்வனே உணர்ந்து <strong>${metrics.totalXp.toLocaleString()} தர்ம XP</strong> புள்ளிகளுடன் நிறைவு செய்துள்ளார் என ஆசிரம பீடத்தால் சான்றளிக்கப்படுகிறது.
    `;
  }

  return `
    <div class="diploma-outer-wrap">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:8px;">
        <span style="color:#94a3b8; font-size:0.85rem;">தரம் ${grade} — 3 மாத காலப் பருவ நிறைவுச் சான்றிதழ்</span>
        <div style="display:flex; gap:8px;">
          <button type="button" class="sheet-btn" onclick="editStudentName()" style="font-size:0.82rem; padding:6px 14px;">
            ✍️ மாணவர் பெயர் மாற்றுக
          </button>
          <button type="button" class="sheet-btn sheet-btn-view" onclick="printGradeDiploma()" style="font-size:0.82rem; padding:6px 16px;">
            🖨️ சான்றிதழ் அச்சிடுக / PDF சேமிக்க
          </button>
        </div>
      </div>

      <!-- Traditional Vedic Certificate -->
      <article class="diploma-certificate-shell" id="gradeDiplomaShell">
        <div class="diploma-top-emblem">ॐ</div>
        <div class="diploma-inst-name">குரு குல ஆசிரமம் • வித்யா குடீரம் பள்ளி</div>
        <div class="diploma-inst-sub">Guru Kula Desam — Modern Gurukulam Online Vedic Academy</div>

        <h1 class="diploma-cert-title">${diplomaTitle}</h1>
        <div class="diploma-citation-intro">${diplomaIntro}</div>

        <div>இப்பட்டயம் பெருமதிப்பிற்குரிய மாணவர்</div>
        <div class="diploma-student-name-box" id="diplomaStudentNameText">${studentName}</div>
        <div>அவர்களுக்கு நல்லாசியுடன் வழங்கப்படுகிறது.</div>

        <div class="diploma-citation-body">
          ${diplomaBody}
        </div>

        <div class="diploma-seal-row">
          <div class="diploma-sign-col">
            <div style="font-family:'Mukta Malar', serif; font-size:1.1rem; color:var(--gold); font-weight:700;">ஆசிரம ஆச்சார்யர்</div>
            <div class="diploma-sign-line"></div>
            <div class="diploma-sign-label">குருகுல தலைமை ஆச்சார்யர் கையொப்பம்</div>
          </div>

          <div class="diploma-seal-stamp">
            <span>ॐ</span>
            <span>வித்யா பீடம்</span>
            <span>தர்ம முத்திரை</span>
          </div>

          <div class="diploma-sign-col">
            <div style="font-size:0.95rem; color:#cbd5e1; font-weight:700;">${todayStr}</div>
            <div class="diploma-sign-line"></div>
            <div class="diploma-sign-label">வழங்கப்பட்ட நாள் &amp; பதிவு எண்: GKD-${grade}-${Date.now().toString().slice(-6)}</div>
          </div>
        </div>
      </article>

      <div style="text-align:center; margin-top:12px;">
        <button type="button" class="sheet-btn sheet-btn-view" onclick="printGradeDiploma()" style="font-size:0.95rem; padding:10px 24px;">
          🖨️ உங்கள் பட்டயச் சான்றிதழை அச்சிடுக அல்லது PDF ஆகப் பதிவிறக்குக
        </button>
      </div>
    </div>
  `;
}

window.toggleWeekChapterCompletion = function(grade, bookKey, chapterNum) {
  toggleBookChapterCompletion(grade, bookKey, chapterNum);
};

window.openClassroomChapter = function(bookKey, chapterNum) {
  switchClassroomTab('classwork');
  switchBook(bookKey);
  switchChapter(chapterNum);
  const area = document.getElementById('bookReaderWorkspace');
  if (area) {
    area.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
};

window.editStudentName = function() {
  const current = localStorage.getItem('gkd_student_name') || 'மாணவர்';
  const newName = prompt('உங்கள் பெயரை உள்ளிடவும் (Enter Student Name):', current);
  if (newName && newName.trim().length > 0) {
    const clean = newName.trim();
    localStorage.setItem('gkd_student_name', clean);
    const stripNameEl = document.getElementById('stripUserName');
    if (stripNameEl) stripNameEl.innerText = clean;
    const classStudentEl = document.getElementById('classroomStudentNameText');
    if (classStudentEl) classStudentEl.innerText = clean;
    const diplomaNameEl = document.getElementById('diplomaStudentNameText');
    if (diplomaNameEl) diplomaNameEl.innerText = clean;
    if (typeof window.showToast === 'function') {
      window.showToast(`மாணவர் பெயர் "${clean}" என புதுப்பிக்கப்பட்டது.`);
    }
  }
};

window.printGradeDiploma = function() {
  document.body.classList.add('printing-diploma');
  window.print();
  setTimeout(() => {
    document.body.classList.remove('printing-diploma');
  }, 1000);
};

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('activeChapterReadingArea')) {
    initBookReader();
  }
});

