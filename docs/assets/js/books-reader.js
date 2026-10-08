/**
 * Gurukula Desam - 7 Sacred Ashram Books Digital Reader Engine
 * Supports Grades 1-12, all 7 Books, 7+ Chapters per book, URL deep-linking, Audio TTS
 */

let currentGrade = 1;
let currentBook = 'nanneri';
let currentChapter = 1;
let loadedBookData = {};

const BOOKS_METADATA = [
  { id: 'nanneri', name: 'நன்னெறி', en: 'Nanneri', icon: 'M12 2v3M7 5h10l-1.5 4H8.5L7 5z', color: '#38bdf8' },
  { id: 'nallaram', name: 'நல்லறம்', en: 'Nallaram', icon: 'M11 20A7 7 0 0 1 4 13a8.9 8.9 0 0 1 8.2-8.9 7 7 0 0 1 7.8 7.8A8.9 8.9 0 0 1 11 20z', color: '#10b981' },
  { id: 'nalvazhi', name: 'நல்வழி', en: 'Nalvazhi', icon: 'M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z', color: '#facc15' },
  { id: 'narthunai', name: 'நற்துணை', en: 'Narthunai', icon: 'M12 2a9.5 9.5 0 0 0-9.5 9.5c0 7 9.5 12.5 9.5 12.5s9.5-5.5 9.5-12.5A9.5 9.5 0 0 0 12 2z', color: '#c084fc' },
  { id: 'narchinthanai', name: 'நற்சிந்தனை', en: 'Narchinthanai', icon: 'M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z', color: '#fb923c' },
  { id: 'narchol', name: 'நற்சொல்', en: 'Narchol', icon: 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z', color: '#34d399' },
  { id: 'narcheyal', name: 'நற்செயல்', en: 'Narcheyal', icon: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z', color: '#ffd700' }
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

      <!-- Sacred Verse Block -->
      <div class="verse-callout-clean" style="background: rgba(0,0,0,0.35); border-left: 4px solid var(--gold); padding: 16px 20px; border-radius: 0 12px 12px 0; margin-bottom: 22px;">
        <div style="font-size:0.8rem; font-weight:700; color:var(--gold); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;">மூலப் பாடல் / சூத்திரம் (Sacred Verse):</div>
        <div class="verse-text-sacred" style="font-size:1.18rem; font-weight:700; color:#ffffff; line-height:1.6; font-family:'Mukta Malar', serif;">${chap.verse}</div>
        <div class="verse-meaning-clean" style="color:#cbd5e1; font-size:0.92rem; margin-top:10px; line-height:1.6;">
          <strong style="color:var(--gold-soft);">பொருள் விளக்கம்:</strong> ${chap.verseMeaning}
        </div>
      </div>

      <!-- Philosophical Exposition -->
      <div class="reading-section-block">
        <h4 style="color:#38bdf8; font-size:1.05rem; font-weight:700; margin:0 0 10px 0; display:flex; align-items:center; gap:8px;">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
          விரிவுரை &amp; தத்துவ உரை (Philosophical Exposition)
        </h4>
        <div style="color:#e2e8f0; font-size:0.96rem; line-height:1.8; margin-bottom:18px;">
          ${chap.exposition}
        </div>
      </div>

      <!-- Puranic / Itihasic Narrative Story -->
      <div class="reading-section-block story-block" style="background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:18px 20px; margin-bottom:20px;">
        <h4 style="color:var(--gold-bright); font-size:1.05rem; font-weight:700; margin:0 0 8px 0; display:flex; align-items:center; gap:8px;">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8"/></svg>
          மெய்ஞ்ஞானக் கதை / அற உருவகம் (Narrative Illustration)
        </h4>
        <div style="color:#cbd5e1; font-size:0.93rem; line-height:1.8;">
          ${chap.story}
        </div>
      </div>

      <!-- Life Application & Householder Dharma -->
      <div class="reading-section-block" style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.3); border-radius:12px; padding:18px 20px; margin-bottom:20px;">
        <h4 style="color:#34d399; font-size:1.05rem; font-weight:700; margin:0 0 8px 0; display:flex; align-items:center; gap:8px;">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 4 13a8.9 8.9 0 0 1 8.2-8.9 7 7 0 0 1 7.8 7.8A8.9 8.9 0 0 1 11 20z"/><path d="M12.5 4.5c.5 4.5-1 7.5-5 9.5"/></svg>
          இல்லற &amp; அன்றாட வாழ்வியல் நடைமுறை (Practical Application)
        </h4>
        <div style="color:#e2e8f0; font-size:0.92rem; line-height:1.7;">
          ${chap.lifeApplication}
        </div>
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

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('activeChapterReadingArea')) {
    initBookReader();
  }
});
