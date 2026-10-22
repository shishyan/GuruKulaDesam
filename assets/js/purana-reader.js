/**
 * assets/js/purana-reader.js
 * Immersive Digital Library Subsite Story Reader
 * - 2 Beautiful High-Definition Illustrations per Story
 * - Warm Ivory/Parchment Book Spread
 * - Page Turning Pagination (Page 1 of N)
 * - Standalone Subsite Controls
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

    renderPuranaDrawer(puranasCatalog);
    loadPuranaData(currentPuranaId, currentChapterNum, currentPageNum);
  }

  function renderPuranaDrawer(catalog) {
    const drawerList = document.getElementById('puranaBookList');
    if (!drawerList) return;

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

    drawerList.innerHTML = catalog.map(p => {
      const isActive = p.id === currentPuranaId;
      const count = p.chaptersCount || p.total_chapters || p.chapters || 108;
      return `
        <div class="purana-shelf-item ${isActive ? 'active' : ''}" 
             onclick="window.switchPurana('${p.id}')"
             style="cursor:pointer; padding:12px 14px; border-radius:12px; margin-bottom:8px; background:${isActive ? 'linear-gradient(135deg, rgba(212,175,55,0.25), rgba(180,83,9,0.2))' : 'rgba(255,255,255,0.04)'}; border:1px solid ${isActive ? 'var(--gold-bright, #ffd700)' : 'rgba(255,255,255,0.08)'}; transition:all 0.2s ease;">
          <div style="font-weight:700; font-size:0.95rem; color:${isActive ? 'var(--gold-bright, #ffd700)' : '#ffffff'}; margin-bottom:4px;">
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

    // Close offcanvas drawer if open
    const overlay = document.getElementById('booksDrawerOverlay');
    if (overlay) overlay.classList.remove('open');

    // Update active item in drawer
    document.querySelectorAll('.purana-shelf-item').forEach(el => {
      el.classList.remove('active');
    });

    const readingArea = document.getElementById('puranaReadingArea');
    if (readingArea) {
      readingArea.innerHTML = `<div style="text-align:center; padding:90px 20px; color:var(--gold, #ffd700); font-size:1.25rem; font-weight:700;"><span class="spinner"></span> கதை நூல் திறக்கப்படுகிறது...</div>`;
    }

    try {
      const resp = await fetch(`data/puranas/${puranaId}.json`);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      currentPuranaData = await resp.json();

      // Update badge in subsite header
      const badge = document.getElementById('currentBookBadge');
      if (badge) badge.innerText = currentPuranaData.title.split('(')[0].trim();

      renderChapterSelect(currentPuranaData);
      renderCurrentPageContent();
    } catch (e) {
      console.error(`Error loading data/puranas/${puranaId}.json:`, e);
      if (readingArea) {
        readingArea.innerHTML = `
          <div style="background:#fdfbf7; border:1px solid #e7dfd1; border-radius:18px; padding:44px; text-align:center; color:#991b1b; box-shadow:0 12px 35px rgba(0,0,0,0.6);">
            <h3 style="font-size:1.45rem; margin-bottom:8px;">கதை நூல் திறப்பதில் பிழை</h3>
            <p style="color:#786c57; font-size:1.05rem;">மன்னிக்கவும், இக்கதை நூல் விவரங்களைப் பெறுவதில் சிக்கல் ஏற்பட்டது.</p>
          </div>
        `;
      }
    }
  }

  function renderChapterSelect(doc) {
    const dropdown = document.getElementById('chapterSelectDropdown');
    if (!dropdown || !doc.chapters) return;

    dropdown.innerHTML = doc.chapters.map(ch => {
      const cleanTitle = ch.title.split('(')[0].trim().replace(/^[0-9]+\.\s*/, '');
      return `
        <option value="${ch.chapterNumber}" ${ch.chapterNumber === currentChapterNum ? 'selected' : ''}>
          கதை ${ch.chapterNumber}: ${cleanTitle}
        </option>
      `;
    }).join('');
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

    // Pick 2 images for the story:
    // Image 1 displays on Page 1; Image 2 displays on Page 2 or later pages
    const images = chap.images || [];
    let currentImageHtml = '';

    if (images.length >= 1) {
      const imgObj = (currentPageNum === 1 || images.length === 1) ? images[0] : (images[1] || images[0]);
      currentImageHtml = `
        <div class="story-illustration-frame">
          <img src="${imgObj.url}" alt="${imgObj.title || 'கதைத் திருக்காட்சி'}" onerror="this.parentElement.style.display='none';">
          ${imgObj.caption ? `<div class="story-illustration-caption">🎨 ${imgObj.caption}</div>` : ''}
        </div>
      `;
    }

    // Page Dots Indicator
    const pageDotsHtml = pages.map((_, idx) => {
      const pIdx = idx + 1;
      const isCur = pIdx === currentPageNum;
      return `
        <button type="button" 
                class="book-page-dot ${isCur ? 'active' : ''}"
                onclick="window.goToStoryPage(${pIdx})"
                title="பக்கம் ${pIdx}">
        </button>
      `;
    }).join('');

    readingArea.innerHTML = `
      <article class="authentic-book-spread" style="animation: fadeIn 0.25s ease;">
        
        <!-- Header line of the open book spread -->
        <div class="book-inner-header">
          <div class="book-title-sub">
            📖 ${currentPuranaData.title.split('(')[0].trim()} &bull; கதை ${chap.chapterNumber} / ${totalChapters}
          </div>
          <div class="book-page-counter">
            பக்கம் ${currentPageNum} / ${totalPages}
          </div>
        </div>

        <!-- Story Title & Theme -->
        <h1 class="book-chapter-heading">
          ${chap.title}
        </h1>
        ${chap.synopsis ? `<div class="book-chapter-synopsis">${chap.synopsis}</div>` : ''}

        <!-- 1 of the 2 High-Definition Story Illustrations -->
        ${currentImageHtml}

        <!-- Book Text Paragraphs -->
        <div class="book-story-content">
          ${pageContent}
        </div>

        <!-- Bottom Page Indicator Dots -->
        <div class="book-page-dots-track">
          ${pageDotsHtml}
        </div>

      </article>

      <!-- Clean Book Turning Controller -->
      <div class="book-turn-controls">
        <div>
          ${hasPrevPage ? `
            <button type="button" class="book-turn-btn" onclick="window.goToStoryPage(${currentPageNum - 1})">
              &larr; முந்தைய பக்கம் (${currentPageNum - 1})
            </button>
          ` : (hasPrevChapter ? `
            <button type="button" class="book-turn-btn" onclick="window.switchPuranaChapter(${currentChapterNum - 1})">
              &larr; முந்தைய கதை (${currentChapterNum - 1})
            </button>
          ` : '<div></div>')}
        </div>

        <div style="font-weight:700; color:#cbd5e1; font-size:1.05rem;">
          பக்கம் ${currentPageNum} / ${totalPages}
        </div>

        <div>
          ${hasNextPage ? `
            <button type="button" class="book-turn-btn book-turn-btn-next" onclick="window.goToStoryPage(${currentPageNum + 1})">
              அடுத்த பக்கம் (${currentPageNum + 1}) &rarr;
            </button>
          ` : (hasNextChapter ? `
            <button type="button" class="book-turn-btn book-turn-btn-next" onclick="window.switchPuranaChapter(${currentChapterNum + 1})">
              அடுத்த கதை (${currentChapterNum + 1}) &rarr;
            </button>
          ` : `
            <button type="button" class="book-turn-btn book-turn-btn-next" onclick="window.scrollTo({top:0, behavior:'smooth'})">
              நூலின் உச்சிக்குச் செல்க &uarr;
            </button>
          `)}
        </div>
      </div>
    `;

    // Sync dropdown value
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
    renderPuranaDrawer(filtered);
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

  window.prevChapterQuick = function() {
    if (currentChapterNum > 1) {
      window.switchPuranaChapter(currentChapterNum - 1);
    }
  };

  window.nextChapterQuick = function() {
    if (currentPuranaData && currentChapterNum < currentPuranaData.chapters.length) {
      window.switchPuranaChapter(currentChapterNum + 1);
    }
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
