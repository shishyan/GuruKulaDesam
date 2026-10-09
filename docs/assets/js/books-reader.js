/**
 * Gurukula Desam - 7 Sacred Ashram Books Digital Reader Engine
 * Supports Grades 1-12, all 7 Books, 7+ Chapters per book, URL deep-linking, Audio TTS
 */

let currentGrade = 1;
let currentBook = 'nanneri';
let currentChapter = 1;
let loadedBookData = {};

const BOOKS_METADATA = [
  { id: 'nanneri', name: 'நன்னெறி', en: 'Good Ethics & Conduct', icon: 'M12 2v3M7 5h10l-1.5 4H8.5L7 5z', color: '#38bdf8' },
  { id: 'nallaram', name: 'நல்லறம்', en: 'Virtue & Householder Dharma', icon: 'M11 20A7 7 0 0 1 4 13a8.9 8.9 0 0 1 8.2-8.9 7 7 0 0 1 7.8 7.8A8.9 8.9 0 0 1 11 20z', color: '#10b981' },
  { id: 'nalvazhi', name: 'நல்வழி', en: 'Path of Wisdom & Labor', icon: 'M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z', color: '#facc15' },
  { id: 'narthunai', name: 'நற்துணை', en: 'Rituals, Yagnas & Temple', icon: 'M12 2a9.5 9.5 0 0 0-9.5 9.5c0 7 9.5 12.5 9.5 12.5s9.5-5.5 9.5-12.5A9.5 9.5 0 0 0 12 2z', color: '#c084fc' },
  { id: 'narchinthanai', name: 'நற்சிந்தனை', en: 'Buddha Teachings & Mind', icon: 'M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z', color: '#fb923c' },
  { id: 'narchol', name: 'நற்சொல்', en: 'Thiru Manthiram & Mantras', icon: 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z', color: '#34d399' },
  { id: 'narcheyal', name: 'நற்செயல்', en: '3 Ds: Duty, Discipline, Dignity', icon: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z', color: '#ffd700' }
];

async function initBookReader() {
  // Parse URL query params
  const urlParams = new URLSearchParams(window.location.search);
  const gradeParam = parseInt(urlParams.get('grade'));
  const bookParam = urlParams.get('book');
  const chapterParam = parseInt(urlParams.get('chapter'));

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
        <button type="button" class="lesson-speech-btn" onclick="readAloudChapter()" title="குரல்வழிக் கேட்க">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>
          <span>அத்தியாயம் கேட்க</span>
        </button>
      </div>

      <!-- 7 Chapter Visuals Carousel Gallery -->
      ${carouselHtml}

      <!-- Sacred Verse Block -->
      <div class="verse-callout-clean" style="background: rgba(0,0,0,0.35); border-left: 4px solid var(--gold); padding: 16px 20px; border-radius: 0 12px 12px 0; margin-bottom: 22px;">
        <div style="font-size:0.8rem; font-weight:700; color:var(--gold); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;">மூலப் பாடல் / சூத்திரம் (Sacred Verse):</div>
        <div class="verse-text-sacred" style="font-size:1.18rem; font-weight:700; color:#ffffff; line-height:1.6; font-family:'Mukta Malar', serif;">${chap.verse}</div>
        <div class="verse-meaning-clean" style="color:#cbd5e1; font-size:0.92rem; margin-top:10px; line-height:1.6;">
          <strong style="color:var(--gold-soft);">பொருள் விளக்கம்:</strong> ${chap.verseMeaning}
        </div>
        <div class="moola-reader-actions-row" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-top:14px; padding-top:10px; border-top:1px dashed rgba(212,175,55,0.25);">
          <button type="button" class="moola-read-btn" onclick="openChapterMoolaModal('${currentBook}', ${chap.chapterNumber}, ${currentGrade})">
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:13px; height:13px;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg> 📖 மூல நூல் &amp; பதவுரை காண்க
          </button>
          <a href="moola-nool.html" class="moola-canon-link" target="_blank" title="முழு மூல நூலகத்தில் திறக்க">
            மூல நூல் நூலகம் &rarr;
          </a>
        </div>
        ${images[1] ? `
          <div class="inline-art-card" onclick="openArtLightboxByIndex(1)" title="பெரிதாகக் காண கிளிக் செய்க">
            <div class="art-zoom-hint">
              <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg> பெரிதாக்கு
            </div>
            <img src="${images[1].url}" alt="${images[1].caption}" loading="lazy">
            <div class="inline-art-caption">
              <span>${images[1].caption}</span>
              <span class="inline-art-badge">காட்சி 2 • செய்யுள் களம்</span>
            </div>
          </div>
        ` : ''}
      </div>

      <!-- Philosophical Exposition -->
      <div class="reading-section-block">
        <h4 style="color:#38bdf8; font-size:1.05rem; font-weight:700; margin:0 0 10px 0; display:flex; align-items:center; gap:8px;">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
          விரிவுரை &amp; தத்துவ உரை (Philosophical Exposition)
        </h4>
        <div style="color:#e2e8f0; font-size:0.96rem; line-height:1.8; margin-bottom:12px;">
          ${chap.exposition}
        </div>
        ${images[2] ? `
          <div class="inline-art-card" onclick="openArtLightboxByIndex(2)" title="பெரிதாகக் காண கிளிக் செய்க">
            <div class="art-zoom-hint">
              <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg> பெரிதாக்கு
            </div>
            <img src="${images[2].url}" alt="${images[2].caption}" loading="lazy">
            <div class="inline-art-caption">
              <span>${images[2].caption}</span>
              <span class="inline-art-badge">காட்சி 3 • தத்துவ உரை</span>
            </div>
          </div>
        ` : ''}
      </div>

      <!-- Puranic / Itihasic Narrative Story -->
      <div class="reading-section-block story-block" style="background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:18px 20px; margin-bottom:20px;">
        <h4 style="color:var(--gold-bright); font-size:1.05rem; font-weight:700; margin:0 0 8px 0; display:flex; align-items:center; gap:8px;">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8"/></svg>
          மெய்ஞ்ஞானக் கதை / அற உருவகம் (Narrative Illustration)
        </h4>
        ${images[3] ? `
          <div class="inline-art-card" onclick="openArtLightboxByIndex(3)" title="பெரிதாகக் காண கிளிக் செய்க">
            <div class="art-zoom-hint">
              <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg> பெரிதாக்கு
            </div>
            <img src="${images[3].url}" alt="${images[3].caption}" loading="lazy">
            <div class="inline-art-caption">
              <span>${images[3].caption}</span>
              <span class="inline-art-badge">காட்சி 4 • கதைக் களம்</span>
            </div>
          </div>
        ` : ''}
        <div style="color:#cbd5e1; font-size:0.93rem; line-height:1.8; margin:12px 0;">
          ${chap.story}
        </div>
        ${images[4] ? `
          <div class="inline-art-card" onclick="openArtLightboxByIndex(4)" title="பெரிதாகக் காண கிளிக் செய்க">
            <div class="art-zoom-hint">
              <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg> பெரிதாக்கு
            </div>
            <img src="${images[4].url}" alt="${images[4].caption}" loading="lazy">
            <div class="inline-art-caption">
              <span>${images[4].caption}</span>
              <span class="inline-art-badge">காட்சி 5 • அறத்தின் வெற்றி</span>
            </div>
          </div>
        ` : ''}
      </div>

      <!-- Life Application & Householder Dharma -->
      <div class="reading-section-block" style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.3); border-radius:12px; padding:18px 20px; margin-bottom:20px;">
        <h4 style="color:#34d399; font-size:1.05rem; font-weight:700; margin:0 0 8px 0; display:flex; align-items:center; gap:8px;">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 4 13a8.9 8.9 0 0 1 8.2-8.9 7 7 0 0 1 7.8 7.8A8.9 8.9 0 0 1 11 20z"/><path d="M12.5 4.5c.5 4.5-1 7.5-5 9.5"/></svg>
          இல்லற &amp; அன்றாட வாழ்வியல் நடைமுறை (Practical Application: 3 Ds)
        </h4>
        <div style="color:#e2e8f0; font-size:0.92rem; line-height:1.7;">
          ${chap.lifeApplication}
        </div>
        ${images[5] ? `
          <div class="inline-art-card" onclick="openArtLightboxByIndex(5)" title="பெரிதாகக் காண கிளிக் செய்க">
            <div class="art-zoom-hint">
              <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg> பெரிதாக்கு
            </div>
            <img src="${images[5].url}" alt="${images[5].caption}" loading="lazy">
            <div class="inline-art-caption">
              <span>${images[5].caption}</span>
              <span class="inline-art-badge">காட்சி 6 • வாழ்வியல் சாதனா</span>
            </div>
          </div>
        ` : ''}
      </div>

      <!-- Sadhana Exercise & Contemplative Question -->
      <div class="reading-section-block" style="background:rgba(234,179,8,0.08); border:1px solid rgba(234,179,8,0.3); border-radius:12px; padding:18px 20px; margin-bottom:26px;">
        <h4 style="color:#facc15; font-size:1.05rem; font-weight:700; margin:0 0 8px 0; display:flex; align-items:center; gap:8px;">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
          சாதனா பயிற்சி &amp; சிந்தனை வினாக்கள் (Sadhana Exercise)
        </h4>
        <div style="color:#e2e8f0; font-size:0.92rem; line-height:1.7;">
          ${chap.exercise}
        </div>
        ${images[6] ? `
          <div class="inline-art-card" onclick="openArtLightboxByIndex(6)" title="பெரிதாகக் காண கிளிக் செய்க">
            <div class="art-zoom-hint">
              <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg> பெரிதாக்கு
            </div>
            <img src="${images[6].url}" alt="${images[6].caption}" loading="lazy">
            <div class="inline-art-caption">
              <span>${images[6].caption}</span>
              <span class="inline-art-badge">காட்சி 7 • தியான &amp; சிந்தனைக் காட்சி</span>
            </div>
          </div>
        ` : ''}
      </div>

      <!-- Navigation Footer (Prev / Next Chapter) -->
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; border-top:1px solid rgba(255,255,255,0.08); padding-top:16px;">
        ${prevNum ? `<button type="button" class="sheet-btn" onclick="switchChapter(${prevNum})"><svg class="gkd-icon gkd-arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg> முந்தைய அத்தியாயம் (${prevNum})</button>` : '<div></div>'}
        <span style="color:#94a3b8; font-size:0.85rem;">அத்தியாயம் ${chap.chapterNumber} / ${totalChapters}</span>
        ${nextNum ? `<button type="button" class="sheet-btn sheet-btn-view" onclick="switchChapter(${nextNum})">அடுத்த அத்தியாயம் (${nextNum}) <svg class="gkd-icon gkd-arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></button>` : `<a href="tharam-${currentGrade}.html" class="sheet-btn sheet-btn-view">வகுப்புப் பாடங்களுக்குத் திரும்புக <svg class="gkd-icon gkd-external-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg></a>`}
      </div>
    </article>
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
  const container = document.getElementById('activeChapterReadingArea');
  if (!container) return;
  const text = container.innerText;
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'ta-IN';
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  } else {
    alert('உங்கள் உலாவியில் குரல்வழி வாசிப்பு வசதி இல்லை.');
  }
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
