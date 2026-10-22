/**
 * assets/js/purana-reader.js
 * Multi-Page Storybook Reader Engine
 * - Zero Clutter: Stories only. No verses, no quiz/questions, no boilerplate badges.
 * - Multi-Page Reading Mode: Each chapter is split into page 1 of N, page 2 of N, etc.
 * - Clean Page Turning: Previous Page, Next Page, Chapter Jump.
 * - Big legible fonts and distraction-free reading experience.
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
        { id: 'children-purana-stories', title: 'குழந்தைகளுக்கான புராணக் கதைகள்', category: 'சிறார் கதைப் பேழை', chaptersCount: 10 },
        { id: 'mahabharatam', title: 'மகாபாரதக் கதைகள் (Mahabharatam)', category: 'இதிகாசம்', chaptersCount: 18 },
        { id: 'ramayanam', title: 'ஸ்ரீ ராம சரிதம் (Kamba Ramayanam)', category: 'இதிகாசம்', chaptersCount: 6 },
        { id: 'kandha-puranam', title: 'கந்த புராணக் கதைகள் (Kandha Puranam)', category: 'சைவ மகாபுராணம்', chaptersCount: 4 },
        { id: 'bhagavata-puranam', title: 'ஸ்ரீமத் பாகவதக் கதைகள் (Bhagavatam)', category: 'வைணவ மகாபுராணம்', chaptersCount: 12 },
        { id: 'periyapuranam', title: 'பெரியபுராண நாயன்மார் கதைகள்', category: 'சைவ காப்பியம்', chaptersCount: 5 },
        { id: 'thiruvilaiyadal', title: 'திருவிளையாடற் கதைகள் (64 Leelas)', category: 'சைவ புராணம்', chaptersCount: 5 },
        { id: 'shiva-puranam', title: 'சிவ புராணக் கதைகள் (Shiva Puranam)', category: 'சைவ மகாபுராணம்', chaptersCount: 11 },
        { id: 'vishnu-puranam', title: 'விஷ்ணு புராணக் கதைகள் (Vishnu Puranam)', category: 'வைணவ மகாபுராணம்', chaptersCount: 6 },
        { id: 'matsya-puranam', title: 'மத்ஸ்ய புராணக் கதைகள் (Matsya Puranam)', category: 'மகாபுராணம்', chaptersCount: 5 },
        { id: 'garuda-puranam', title: 'கருட புராணக் கதைகள் (Garuda Puranam)', category: 'மகாபுராணம்', chaptersCount: 3 },
        { id: 'padma-puranam', title: 'பத்ம புராணக் கதைகள் (Padma Puranam)', category: 'மகாபுராணம்', chaptersCount: 5 }
      ];
    }

    sidebarList.innerHTML = catalog.map(p => {
      const isActive = p.id === currentPuranaId;
      const count = p.chaptersCount || p.total_chapters || p.chapters || (p.chapters ? p.chapters.length : 1);
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
    if (total > 10) {
      tabsCont.innerHTML = `
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; background:rgba(15,23,42,0.8); border:1px solid rgba(212,175,55,0.3); border-radius:14px; padding:12px 18px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-weight:700; color:var(--gold-soft); font-size:0.95rem;">கதைத் தேர்வு:</span>
            <select id="chapterSelectDropdown" onchange="window.switchPuranaChapter(parseInt(this.value, 10))" style="background:#02131e; color:#ffffff; border:1px solid var(--gold); border-radius:8px; padding:8px 12px; font-size:0.95rem; font-weight:700; max-width:400px; outline:none; cursor:pointer;">
              ${doc.chapters.map(ch => `
                <option value="${ch.chapterNumber}" ${ch.chapterNumber === currentChapterNum ? 'selected' : ''}>
                  கதை ${ch.chapterNumber}: ${ch.title.split('(')[0].trim()}
                </option>
              `).join('')}
            </select>
          </div>
          <div style="display:flex; gap:8px;">
            <button type="button" class="sheet-btn" onclick="window.switchPuranaChapter(Math.max(1, currentChapterNum - 1))" style="padding:6px 14px; font-size:0.85rem;">&larr; முந்தைய கதை</button>
            <span style="color:#ffffff; font-weight:800; padding:6px 10px; font-size:0.95rem;">${currentChapterNum} / ${total}</span>
            <button type="button" class="sheet-btn sheet-btn-view" onclick="window.switchPuranaChapter(Math.min(${total}, currentChapterNum + 1))" style="padding:6px 14px; font-size:0.85rem;">அடுத்த கதை &rarr;</button>
          </div>
        </div>
      `;
    } else {
      tabsCont.innerHTML = `
        <div style="display:flex; gap:8px; overflow-x:auto; padding:6px 0 12px; scrollbar-width:thin;">
          ${doc.chapters.map(ch => {
            const isActive = ch.chapterNumber === currentChapterNum;
            return `
              <button type="button" class="purana-tab-btn ${isActive ? 'active' : ''}" onclick="window.switchPuranaChapter(${ch.chapterNumber})" style="white-space:nowrap; padding:8px 16px; border-radius:12px; font-weight:700; font-size:0.88rem; cursor:pointer; background:${isActive ? 'linear-gradient(135deg, var(--gold), #b45309)' : 'rgba(255,255,255,0.06)'}; color:${isActive ? '#02131e' : '#cbd5e1'}; border:1px solid ${isActive ? 'var(--gold-bright)' : 'rgba(255,255,255,0.12)'};">
                <span>கதை ${ch.chapterNumber}</span>: ${ch.title.split('(')[0].trim().replace(/^[0-9]+\.\s*/, '')}
              </button>
            `;
          }).join('')}
        </div>
      `;
    }
  }

  function getChapterPages(chap) {
    if (chap.pages && Array.isArray(chap.pages) && chap.pages.length > 0) {
      return chap.pages;
    }
    // Fallback: extract paragraphs from exposition and group into pages
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

    // Validate currentPageNum
    if (currentPageNum < 1) currentPageNum = 1;
    if (currentPageNum > totalPages) currentPageNum = totalPages;

    const pageContent = pages[currentPageNum - 1];

    const hasPrevPage = currentPageNum > 1;
    const hasNextPage = currentPageNum < totalPages;
    const hasPrevChapter = currentChapterNum > 1;
    const hasNextChapter = currentChapterNum < totalChapters;

    // Build Page Dots / Indicator
    const pageDotsHtml = pages.map((_, idx) => {
      const pIdx = idx + 1;
      const isCur = pIdx === currentPageNum;
      return `
        <button type="button" 
                onclick="window.goToStoryPage(${pIdx})"
                title="பக்கம் ${pIdx}"
                style="width:${isCur ? '28px' : '10px'}; height:10px; border-radius:5px; border:none; cursor:pointer; background:${isCur ? 'var(--gold-bright)' : 'rgba(255,255,255,0.25)'}; transition:all 0.2s ease;">
        </button>
      `;
    }).join('');

    readingArea.innerHTML = `
      <article class="purana-reading-chapter" style="animation: fadeIn 0.25s ease;">
        
        <!-- Story Book Header Bar -->
        <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(212,175,55,0.25); border-radius:18px; padding:20px 24px; margin-bottom:20px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="background:rgba(212,175,55,0.18); color:var(--gold-bright); border:1px solid rgba(212,175,55,0.4); padding:3px 14px; border-radius:14px; font-weight:800; font-size:0.85rem;">
              கதை ${chap.chapterNumber} / ${totalChapters}
            </span>
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="color:var(--gold-bright); font-size:0.95rem; font-weight:800; background:rgba(0,0,0,0.4); padding:4px 12px; border-radius:8px; border:1px solid rgba(212,175,55,0.3);">
                📖 பக்கம் ${currentPageNum} / ${totalPages}
              </span>
            </div>
          </div>
          <h2 style="color:#ffffff; font-size:2rem; font-weight:900; line-height:1.3; margin:0;">
            ${chap.title}
          </h2>
        </div>

        <!-- Clean Story Book Page Canvas -->
        <div class="story-page-canvas" style="background:rgba(10, 16, 28, 0.96); border:1px solid rgba(212,175,55,0.2); border-radius:20px; padding:38px 44px; margin-bottom:26px; box-shadow:0 16px 45px rgba(0,0,0,0.6); position:relative; min-height:360px;">
          
          <!-- Top Page Corner Ribbon -->
          <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:12px; margin-bottom:28px;">
            <span style="font-size:0.88rem; color:#94a3b8; font-style:italic;">${chap.title.split('(')[0].trim()}</span>
            <span style="font-size:0.86rem; color:#ffd700; font-weight:700;">பக்கம் ${currentPageNum}</span>
          </div>

          ${chap.images && chap.images.length > 0 ? `
            <div class="story-illustration" style="margin-bottom:28px; text-align:center;">
              <div style="position:relative; display:inline-block; max-width:100%; border-radius:16px; overflow:hidden; border:1px solid rgba(212,175,55,0.3); box-shadow:0 12px 30px rgba(0,0,0,0.5);">
                <img src="${(currentPageNum === 1 || chap.images.length === 1) ? chap.images[0].url : chap.images[1].url}" 
                     alt="${(currentPageNum === 1 || chap.images.length === 1) ? (chap.images[0].title || 'கதைத் தோற்றம்') : (chap.images[1].title || 'கதைத் தோற்றம்')}" 
                     style="max-width:100%; max-height:420px; object-fit:cover; display:block; margin:0 auto; filter:brightness(0.96);"
                     onerror="this.parentElement.style.display='none';">
                <div style="background:rgba(15,23,42,0.92); padding:10px 18px; color:var(--gold-soft); font-size:0.95rem; font-weight:600; border-top:1px solid rgba(212,175,55,0.2);">
                  🎨 ${(currentPageNum === 1 || chap.images.length === 1) ? (chap.images[0].caption || chap.images[0].title || '') : (chap.images[1].caption || chap.images[1].title || '')}
                </div>
              </div>
            </div>
          ` : ''}

          <!-- Pure Story Body -->
          <div class="story-body-text" style="font-size:1.3rem; line-height:2.2; color:#f8fafc; font-family:'Mukta Malar', Georgia, serif; letter-spacing:0.015em;">
            ${pageContent}
          </div>

          <!-- Bottom Story Pagination Dots -->
          <div style="display:flex; justify-content:center; align-items:center; gap:8px; margin-top:36px; padding-top:20px; border-top:1px solid rgba(255,255,255,0.08);">
            ${pageDotsHtml}
          </div>

        </div>

        <!-- Page Turning Controller -->
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; padding:12px 0;">
          
          <div>
            ${hasPrevPage ? `
              <button type="button" class="sheet-btn" onclick="window.goToStoryPage(${currentPageNum - 1})" style="cursor:pointer; font-weight:700; padding:12px 24px; font-size:1rem;">
                &larr; முந்தைய பக்கம் (${currentPageNum - 1})
              </button>
            ` : (hasPrevChapter ? `
              <button type="button" class="sheet-btn" onclick="window.switchPuranaChapter(${currentChapterNum - 1})" style="cursor:pointer; font-weight:700; padding:12px 20px; font-size:0.92rem; opacity:0.85;">
                &larr; முந்தைய கதை (${currentChapterNum - 1})
              </button>
            ` : '<div></div>')}
          </div>

          <div style="text-align:center;">
            <span style="color:#ffffff; font-weight:800; font-size:1.05rem;">
              பக்கம் ${currentPageNum} / ${totalPages}
            </span>
          </div>

          <div>
            ${hasNextPage ? `
              <button type="button" class="sheet-btn sheet-btn-view" onclick="window.goToStoryPage(${currentPageNum + 1})" style="cursor:pointer; font-weight:700; padding:12px 28px; font-size:1rem; box-shadow:0 0 15px rgba(212,175,55,0.3);">
                அடுத்த பக்கம் (${currentPageNum + 1}) &rarr;
              </button>
            ` : (hasNextChapter ? `
              <button type="button" class="sheet-btn sheet-btn-view" onclick="window.switchPuranaChapter(${currentChapterNum + 1})" style="cursor:pointer; font-weight:700; padding:12px 24px; font-size:0.95rem;">
                அடுத்த கதை (${currentChapterNum + 1}) &rarr;
              </button>
            ` : `
              <button type="button" class="sheet-btn sheet-btn-view" onclick="window.scrollTo({top:0, behavior:'smooth'})" style="cursor:pointer; font-weight:700; padding:12px 24px;">
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
