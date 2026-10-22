/**
 * assets/js/purana-reader.js
 * Immersive Multi-Page Storybook Reader Engine
 * - Zero Clutter: Stories only.
 * - Multi-Page Reading Mode: Page 1 of N, Page 2 of N, etc.
 * - Clean Page Turning: Previous Page, Next Page, Fast Chapter Selector.
 * - Solid Opaque High-Contrast Reading Canvas (Zero background bleed-through).
 */

(function() {
  'use strict';

  let puranasCatalog = [];
  let currentPuranaId = 'children-purana-stories';
  let currentChapterNum = 1;
  let currentPageNum = 1;
  let currentPuranaData = null;

  async function initPuranaReader() {
    const urlParams = new URLSearchParams(window.location.search);
    const pParam = urlParams.get('id') || urlParams.get('purana');
    const cParam = urlParams.get('chapter');
    const pgParam = urlParams.get('page');

    if (pParam) currentPuranaId = pParam;
    if (cParam) currentChapterNum = parseInt(cParam, 10) || 1;
    if (pgParam) currentPageNum = parseInt(pgParam, 10) || 1;

    try {
      const resp = await fetch('data/puranas/puranas_index.json');
      if (resp.ok) {
        const indexData = await resp.json();
        puranasCatalog = indexData.catalog || [];
      }
    } catch (e) {
      console.warn('Could not load puranas_index.json, using fallback catalog');
    }

    renderPuranaSidebar(puranasCatalog);
    loadPuranaData(currentPuranaId, currentChapterNum, currentPageNum);
  }

  function renderPuranaSidebar(catalog) {
    const sidebarList = document.getElementById('puranaBookList');
    if (!sidebarList) return;

    if (!catalog || catalog.length === 0) {
      catalog = [
        { id: 'children-purana-stories', title: 'குழந்தைகளுக்கான 108 புராணக் கதைகள்', category: 'சிறார் கதைப் பேழை', chaptersCount: 108 },
        { id: 'kandha-puranam', title: 'கந்த புராணக் கதைகள்', category: 'சைவ மகாபுராணம்', chaptersCount: 108 },
        { id: 'ramayanam', title: 'கம்ப ராமாயணக் கதைகள்', category: 'இதிகாசம்', chaptersCount: 108 },
        { id: 'mahabharatam', title: 'மகாபாரதக் கதைகள்', category: 'இதிகாசம்', chaptersCount: 108 },
        { id: 'bhagavata-puranam', title: 'ஸ்ரீமத் பாகவதக் கதைகள்', category: 'வைணவ மகாபுராணம்', chaptersCount: 108 },
        { id: 'periyapuranam', title: 'பெரியபுராண நாயன்மார் கதைகள்', category: 'சைவ காப்பியம்', chaptersCount: 108 },
        { id: 'thiruvilaiyadal', title: 'திருவிளையாடற் கதைகள்', category: 'சைவ புராணம்', chaptersCount: 108 },
        { id: 'shiva-puranam', title: 'சிவ புராணக் கதைகள்', category: 'சைவ மகாபுராணம்', chaptersCount: 108 },
        { id: 'vishnu-puranam', title: 'விஷ்ணு புராணக் கதைகள்', category: 'வைணவ மகாபுராணம்', chaptersCount: 108 }
      ];
    }

    sidebarList.innerHTML = catalog.map(p => {
      const isActive = p.id === currentPuranaId;
      const count = p.chaptersCount || p.total_chapters || p.chapters || 108;
      return `
        <div class="purana-shelf-item ${isActive ? 'active' : ''}" 
             onclick="window.switchPurana('${p.id}')"
             style="cursor:pointer; padding:12px 14px; border-radius:12px; margin-bottom:8px; background:${isActive ? 'linear-gradient(135deg, rgba(212,175,55,0.22), rgba(212,175,55,0.06))' : 'rgba(255,255,255,0.03)'}; border:1px solid ${isActive ? 'var(--gold-bright)' : 'rgba(255,255,255,0.08)'}; transition:all 0.2s ease;">
          <div style="font-weight:700; font-size:0.95rem; color:${isActive ? 'var(--gold-bright)' : '#ffffff'}; margin-bottom:4px;">
            ${p.title}
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.78rem; color:#94a3b8;">
            <span>${p.category || 'கதை நூல்'}</span>
            <span style="background:rgba(255,255,255,0.08); padding:2px 8px; border-radius:6px; color:#cbd5e1;">${count} கதைகள்</span>
          </div>
        </div>
      `;
    }).join('');
  }

  async function loadPuranaData(puranaId, chapterNum = 1, pageNum = 1) {
    currentPuranaId = puranaId;
    currentChapterNum = chapterNum;
    currentPageNum = pageNum;
    updateUrl();

    // Update active item in sidebar
    document.querySelectorAll('.purana-shelf-item').forEach(el => {
      el.classList.remove('active');
    });

    const readingArea = document.getElementById('puranaReadingArea');
    if (readingArea) {
      readingArea.innerHTML = `<div style="text-align:center; padding:60px 20px; color:var(--gold);"><span class="spinner"></span> கதைப் புத்தகம் திறக்கப்படுகிறது...</div>`;
    }

    try {
      const resp = await fetch(`data/puranas/${puranaId}.json`);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      currentPuranaData = await resp.json();
      renderPuranaHeader(currentPuranaData);
      renderChapterTabs(currentPuranaData);
      renderCurrentPageContent();
    } catch (e) {
      console.error(`Error loading data/puranas/${puranaId}.json:`, e);
      if (readingArea) {
        readingArea.innerHTML = `
          <div style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.4); border-radius:16px; padding:30px; text-align:center;">
            <h3 style="color:#ef4444; margin-bottom:8px;">கதை நூல் திறப்பதில் பிழை</h3>
            <p style="color:#cbd5e1;">மன்னிக்கவும், இக்கதை நூல் விவரங்களைப் பெறுவதில் சிக்கல் ஏற்பட்டது.</p>
          </div>
        `;
      }
    }
  }

  function renderPuranaHeader(doc) {
    const titleEl = document.getElementById('puranaDisplayTitle');
    const authorEl = document.getElementById('puranaDisplayAuthor');

    if (titleEl) titleEl.innerText = doc.title;
    if (authorEl) authorEl.innerText = doc.summary || 'குழந்தைகளுக்கான அழகிய ஆன்மிகக் கதைப் பெட்டகம்';
  }

  function renderChapterTabs(doc) {
    const tabsCont = document.getElementById('puranaChapterTabs');
    if (!tabsCont || !doc.chapters) return;

    const total = doc.chapters.length;
    tabsCont.innerHTML = `
      <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; background:rgba(11,19,38,0.92); border:1px solid rgba(212,175,55,0.3); border-radius:14px; padding:12px 18px; box-shadow:0 8px 24px rgba(0,0,0,0.5);">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-weight:700; color:var(--gold-soft); font-size:0.95rem;">கதைத் தேர்வு:</span>
          <select id="chapterSelectDropdown" onchange="window.switchPuranaChapter(parseInt(this.value, 10))" style="background:#02131e; color:#ffffff; border:1px solid var(--gold); border-radius:8px; padding:8px 12px; font-size:0.95rem; font-weight:700; max-width:440px; outline:none; cursor:pointer;">
            ${doc.chapters.map(ch => `
              <option value="${ch.chapterNumber}" ${ch.chapterNumber === currentChapterNum ? 'selected' : ''}>
                கதை ${ch.chapterNumber}: ${ch.title.split('(')[0].trim().replace(/^[0-9]+\.\s*/, '')}
              </option>
            `).join('')}
          </select>
        </div>
        <div style="display:flex; gap:8px; align-items:center;">
          <button type="button" class="sheet-btn" onclick="window.switchPuranaChapter(Math.max(1, currentChapterNum - 1))" style="padding:6px 14px; font-size:0.85rem; cursor:pointer;">&larr; முந்தைய கதை</button>
          <span style="color:#ffffff; font-weight:800; padding:6px 10px; font-size:0.95rem;">${currentChapterNum} / ${total}</span>
          <button type="button" class="sheet-btn sheet-btn-view" onclick="window.switchPuranaChapter(Math.min(${total}, currentChapterNum + 1))" style="padding:6px 14px; font-size:0.85rem; cursor:pointer;">அடுத்த கதை &rarr;</button>
        </div>
      </div>
    `;
  }

  function getChapterPages(chap) {
    if (chap.pages && Array.isArray(chap.pages) && chap.pages.length > 0) {
      return chap.pages;
    }
    const raw = chap.exposition || '';
    const matches = raw.match(/<p[^>]*>.*?<\/p>/gs);
    if (matches && matches.length > 0) {
      const perPage = matches.length <= 6 ? 2 : 3;
      const pages = [];
      for (let i = 0; i < matches.length; i += perPage) {
        pages.push(matches.slice(i, i + perPage).join(''));
      }
      return pages;
    }
    return [raw];
  }

  function renderCurrentPageContent() {
    const readingArea = document.getElementById('puranaReadingArea');
    if (!readingArea || !currentPuranaData) return;

    const chap = currentPuranaData.chapters.find(c => c.chapterNumber === currentChapterNum) || currentPuranaData.chapters[0];
    if (!chap) return;

    const totalChapters = currentPuranaData.chapters.length;
    const pages = getChapterPages(chap);
    const totalPages = pages.length;

    if (currentPageNum < 1) currentPageNum = 1;
    if (currentPageNum > totalPages) currentPageNum = totalPages;

    const pageContent = pages[currentPageNum - 1];

    const hasPrevPage = currentPageNum > 1;
    const hasNextPage = currentPageNum < totalPages;
    const hasPrevChapter = currentChapterNum > 1;
    const hasNextChapter = currentChapterNum < totalChapters;

    // Page Dots Indicator
    const pageDotsHtml = pages.map((_, idx) => {
      const pIdx = idx + 1;
      const isCur = pIdx === currentPageNum;
      return `
        <button type="button" 
                onclick="window.goToStoryPage(${pIdx})"
                title="பக்கம் ${pIdx}"
                style="width:${isCur ? '32px' : '12px'}; height:10px; border-radius:5px; border:none; cursor:pointer; background:${isCur ? 'var(--gold-bright, #ffd700)' : 'rgba(255,255,255,0.25)'}; transition:all 0.2s ease;">
        </button>
      `;
    }).join('');

    readingArea.innerHTML = `
      <article class="purana-reading-chapter" style="animation: fadeIn 0.25s ease;">
        
        <!-- Story Book Header Bar -->
        <div style="background:rgba(11,19,38,0.95); border:1px solid rgba(212,175,55,0.3); border-radius:18px; padding:22px 28px; margin-bottom:20px; box-shadow:0 10px 30px rgba(0,0,0,0.6);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="background:rgba(212,175,55,0.18); color:var(--gold-bright); border:1px solid rgba(212,175,55,0.4); padding:4px 14px; border-radius:14px; font-weight:800; font-size:0.88rem;">
              கதை ${chap.chapterNumber} / ${totalChapters}
            </span>
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="color:var(--gold-bright); font-size:0.95rem; font-weight:800; background:rgba(0,0,0,0.5); padding:4px 14px; border-radius:8px; border:1px solid rgba(212,175,55,0.35);">
                📖 பக்கம் ${currentPageNum} / ${totalPages}
              </span>
            </div>
          </div>
          <h2 style="color:#ffffff; font-size:2.1rem; font-weight:900; line-height:1.3; margin:0 0 6px 0;">
            ${chap.title}
          </h2>
          ${chap.synopsis ? `<p style="color:#7dd3fc; font-size:1.05rem; line-height:1.6; margin:0; font-weight:500;">${chap.synopsis}</p>` : ''}
        </div>

        <!-- Solid Opaque Story Book Canvas - No Background Interference -->
        <div class="story-page-canvas" style="background:#090f1d !important; border:1.5px solid rgba(212,175,55,0.35) !important; border-radius:22px; padding:44px 48px; margin-bottom:26px; box-shadow:0 20px 55px rgba(0,0,0,0.85); position:relative; min-height:420px;">
          
          <!-- Top Page Corner Header -->
          <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:14px; margin-bottom:30px;">
            <span style="font-size:0.92rem; color:#94a3b8; font-style:italic;">${chap.title.split('(')[0].trim()}</span>
            <span style="font-size:0.92rem; color:#ffd700; font-weight:800; letter-spacing:0.05em;">பக்கம் ${currentPageNum} / ${totalPages}</span>
          </div>

          <!-- Pure Story Body -->
          <div class="story-body-text" style="font-size:1.32rem; line-height:2.25; color:#f8fafc; font-family:'Mukta Malar', Georgia, serif; letter-spacing:0.015em;">
            ${pageContent}
          </div>

          <!-- Bottom Story Pagination Dots -->
          <div style="display:flex; justify-content:center; align-items:center; gap:8px; margin-top:36px; padding-top:22px; border-top:1px solid rgba(255,255,255,0.1);">
            ${pageDotsHtml}
          </div>

        </div>

        <!-- Page Turning Controller -->
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; padding:12px 0;">
          
          <div>
            ${hasPrevPage ? `
              <button type="button" class="sheet-btn" onclick="window.goToStoryPage(${currentPageNum - 1})" style="cursor:pointer; font-weight:700; padding:12px 26px; font-size:1rem; border-radius:12px;">
                &larr; முந்தைய பக்கம் (${currentPageNum - 1})
              </button>
            ` : (hasPrevChapter ? `
              <button type="button" class="sheet-btn" onclick="window.switchPuranaChapter(${currentChapterNum - 1})" style="cursor:pointer; font-weight:700; padding:12px 22px; font-size:0.95rem; border-radius:12px;">
                &larr; முந்தைய கதை (${currentChapterNum - 1})
              </button>
            ` : '<div></div>')}
          </div>

          <div style="text-align:center;">
            <span style="color:#ffffff; font-weight:800; font-size:1.05rem; background:rgba(15,23,42,0.8); padding:8px 18px; border-radius:12px; border:1px solid rgba(255,255,255,0.1);">
              பக்கம் ${currentPageNum} / ${totalPages}
            </span>
          </div>

          <div>
            ${hasNextPage ? `
              <button type="button" class="sheet-btn sheet-btn-view" onclick="window.goToStoryPage(${currentPageNum + 1})" style="cursor:pointer; font-weight:700; padding:12px 30px; font-size:1rem; border-radius:12px; box-shadow:0 0 16px rgba(212,175,55,0.35);">
                அடுத்த பக்கம் (${currentPageNum + 1}) &rarr;
              </button>
            ` : (hasNextChapter ? `
              <button type="button" class="sheet-btn sheet-btn-view" onclick="window.switchPuranaChapter(${currentChapterNum + 1})" style="cursor:pointer; font-weight:700; padding:12px 26px; font-size:0.95rem; border-radius:12px;">
                அடுத்த கதை (${currentChapterNum + 1}) &rarr;
              </button>
            ` : `
              <button type="button" class="sheet-btn sheet-btn-view" onclick="window.scrollTo({top:0, behavior:'smooth'})" style="cursor:pointer; font-weight:700; padding:12px 24px; border-radius:12px;">
                கதையின் உச்சிக்குச் செல்க &uarr;
              </button>
            `)}
          </div>

        </div>

      </article>
    `;

    const dropdown = document.getElementById('chapterSelectDropdown');
    if (dropdown) dropdown.value = currentChapterNum;

    readingArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function updateUrl() {
    const newUrl = `${window.location.pathname}?purana=${currentPuranaId}&chapter=${currentChapterNum}&page=${currentPageNum}`;
    window.history.replaceState({}, '', newUrl);
  }

  function filterPuranas(query) {
    const q = query.trim().toLowerCase();
    const filtered = puranasCatalog.filter(p => {
      return p.title.toLowerCase().includes(q) || (p.category && p.category.toLowerCase().includes(q));
    });
    renderPuranaSidebar(filtered);
  }

  // Global window functions
  window.switchPurana = function(puranaId) {
    loadPuranaData(puranaId, 1, 1);
  };

  window.switchPuranaChapter = function(chapNum) {
    currentChapterNum = chapNum;
    currentPageNum = 1;
    updateUrl();
    renderCurrentPageContent();
  };

  window.goToStoryPage = function(pageNum) {
    currentPageNum = pageNum;
    updateUrl();
    renderCurrentPageContent();
  };

  window.filterPuranaList = function(input) {
    filterPuranas(input.value);
  };

  document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('puranaReadingArea')) {
      initPuranaReader();
    }
  });

})();
