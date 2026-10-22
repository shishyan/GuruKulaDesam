(function() {
  'use strict';

  let puranasCatalog = [];
  let currentPuranaId = 'children-purana-stories';
  let currentChapterNum = 1;
  let currentPuranaData = null;

  async function initPuranaReader() {
    const urlParams = new URLSearchParams(window.location.search);
    const pParam = urlParams.get('id') || urlParams.get('purana');
    const cParam = urlParams.get('chapter');

    if (pParam) currentPuranaId = pParam;
    if (cParam) currentChapterNum = parseInt(cParam, 10) || 1;

    try {
      const resp = await fetch('data/puranas-index.json');
      if (resp.ok) {
        puranasCatalog = await resp.json();
      }
    } catch (e) {
      console.warn('Could not load puranas-index.json');
    }

    renderPuranaSidebar(puranasCatalog);
    loadPuranaData(currentPuranaId, currentChapterNum);
  }

  function renderPuranaSidebar(catalog) {
    const sidebarList = document.getElementById('puranaBookList');
    if (!sidebarList) return;

    if (!catalog || catalog.length === 0) return;

    sidebarList.innerHTML = catalog.map(p => {
      const isActive = p.id === currentPuranaId;
      const count = p.total_chapters || 1;
      return `
        <div class="purana-shelf-item ${isActive ? 'active' : ''}" 
             onclick="window.switchPurana('${p.id}')"
             style="cursor:pointer; padding:12px 14px; border-radius:12px; margin-bottom:8px; background:${isActive ? 'linear-gradient(135deg, rgba(212,175,55,0.25), rgba(212,175,55,0.08))' : 'rgba(255,255,255,0.03)'}; border:1px solid ${isActive ? 'var(--gold-bright)' : 'rgba(255,255,255,0.08)'}; transition:all 0.2s ease;">
          <div style="font-weight:700; font-size:0.95rem; color:${isActive ? 'var(--gold-bright)' : '#ffffff'}; margin-bottom:4px;">
            ${p.icon || '📖'} ${p.title.split('(')[0].trim()}
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.78rem; color:#94a3b8;">
            <span>${p.category || 'கதைப் புத்தகம்'}</span>
            <span style="background:rgba(255,255,255,0.08); padding:2px 8px; border-radius:6px; color:#cbd5e1;">${count} கதைகள்</span>
          </div>
        </div>
      `;
    }).join('');
  }

  async function loadPuranaData(puranaId, chapterNum = 1) {
    currentPuranaId = puranaId;
    currentChapterNum = chapterNum;
    updateUrl();

    renderPuranaSidebar(puranasCatalog);

    const readingArea = document.getElementById('puranaReadingArea');
    if (readingArea) {
      readingArea.innerHTML = `<div style="text-align:center; padding:60px 20px; color:var(--gold);"><span class="spinner"></span> கதைப் பகுதி வாசிக்க ஏற்றப்படுகிறது...</div>`;
    }

    try {
      const resp = await fetch(`data/puranas/${puranaId}.json`);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      currentPuranaData = await resp.json();
      renderPuranaHeader(currentPuranaData);
      renderChapterTabs(currentPuranaData);
      renderCurrentChapterContent();
    } catch (e) {
      console.error(`Error loading data/puranas/${puranaId}.json:`, e);
      if (readingArea) {
        readingArea.innerHTML = `
          <div style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.4); border-radius:16px; padding:30px; text-align:center;">
            <h3 style="color:#ef4444;">கதை ஏறுவதில் பிழை</h3>
            <p style="color:#e2e8f0;">${puranaId}.json கோப்பினை வாசிக்க முடியவில்லை. பக்கத்தை மறுஏற்றம் செய்யவும்.</p>
          </div>
        `;
      }
    }
  }

  function renderPuranaHeader(doc) {
    const titleEl = document.getElementById('puranaDisplayTitle');
    const authorEl = document.getElementById('puranaDisplayAuthor');

    if (titleEl) titleEl.innerText = doc.title;
    if (authorEl) authorEl.innerText = `அருளியவர்: ${doc.author || 'சனாதன முனிவர் மரபு'}`;
  }

  function renderChapterTabs(doc) {
    const tabsCont = document.getElementById('puranaChapterTabs');
    if (!tabsCont || !doc.chapters) return;

    const total = doc.chapters.length;
    tabsCont.innerHTML = `
      <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; background:rgba(15,23,42,0.85); border:1px solid rgba(212,175,55,0.3); border-radius:14px; padding:10px 16px;">
        <div style="display:flex; align-items:center; gap:10px;">
          <span style="font-weight:700; color:var(--gold-soft); font-size:0.92rem;">கதைத் தேர்வு:</span>
          <select id="chapterSelectDropdown" onchange="window.switchPuranaChapter(parseInt(this.value, 10))" style="background:#02131e; color:#ffffff; border:1px solid var(--gold); border-radius:8px; padding:8px 12px; font-size:0.95rem; font-weight:700; max-width:440px; outline:none; cursor:pointer;">
            ${doc.chapters.map(ch => `
              <option value="${ch.chapterNumber}" ${ch.chapterNumber === currentChapterNum ? 'selected' : ''}>
                கதை ${ch.chapterNumber}: ${ch.title.split('(')[0].trim()}
              </option>
            `).join('')}
          </select>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <button type="button" class="sheet-btn" onclick="window.switchPuranaChapter(Math.max(1, currentChapterNum - 1))" style="padding:6px 14px; font-size:0.85rem; cursor:pointer;">&larr; முந்தைய கதை</button>
          <span style="color:#ffffff; font-weight:800; padding:4px 8px; font-size:0.9rem;">${currentChapterNum} / ${total}</span>
          <button type="button" class="sheet-btn sheet-btn-view" onclick="window.switchPuranaChapter(Math.min(${total}, currentChapterNum + 1))" style="padding:6px 14px; font-size:0.85rem; cursor:pointer;">அடுத்த கதை &rarr;</button>
        </div>
      </div>
    `;
  }

  function renderCurrentChapterContent() {
    const readingArea = document.getElementById('puranaReadingArea');
    if (!readingArea || !currentPuranaData) return;

    const chap = currentPuranaData.chapters.find(c => c.chapterNumber === currentChapterNum) || currentPuranaData.chapters[0];
    if (!chap) return;

    const total = currentPuranaData.chapters.length;
    const prevNum = (currentChapterNum > 1) ? currentChapterNum - 1 : null;
    const nextNum = (currentChapterNum < total) ? currentChapterNum + 1 : null;

    readingArea.innerHTML = `
      <article class="purana-reading-chapter" style="animation: fadeIn 0.3s ease;">
        
        <!-- Story Title Heading -->
        <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(212,175,55,0.25); border-radius:18px; padding:24px 28px; margin-bottom:20px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="background:rgba(212,175,55,0.15); color:var(--gold-bright); border:1px solid rgba(212,175,55,0.4); padding:3px 12px; border-radius:14px; font-weight:800; font-size:0.82rem;">
              கதை ${chap.chapterNumber} / ${total}
            </span>
            <span style="font-size:0.85rem; color:#94a3b8;">${currentPuranaData.title.split('(')[0].trim()}</span>
          </div>
          <h2 style="color:#ffffff; font-size:2rem; font-weight:900; line-height:1.3; margin:0 0 8px 0;">
            ${chap.title}
          </h2>
          ${chap.synopsis ? `<p style="color:#7dd3fc; font-size:1.05rem; line-height:1.7; margin:0; font-weight:500;">${chap.synopsis}</p>` : ''}
        </div>

        <!-- Full Clean Story Body (Only the story, no verses) -->
        <div style="background:rgba(10, 16, 28, 0.95); border:1px solid rgba(255,255,255,0.1); border-radius:18px; padding:32px 36px; margin-bottom:28px; box-shadow:0 12px 35px rgba(0,0,0,0.5);">
          <div class="purana-verbatim-text" style="font-size:1.26rem; line-height:2.1; color:#f8fafc; font-family:'Mukta Malar', Georgia, serif; letter-spacing:0.01em;">
            ${chap.exposition}
          </div>
        </div>

        <!-- Bottom Clean Navigation -->
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; padding:18px 0; border-top:1px solid rgba(255,255,255,0.12);">
          ${prevNum ? `
            <button type="button" class="sheet-btn" onclick="window.switchPuranaChapter(${prevNum})" style="cursor:pointer; font-weight:700; padding:12px 24px; font-size:0.95rem;">
              &larr; முந்தைய கதை (${prevNum})
            </button>
          ` : '<div></div>'}
          <span style="color:#94a3b8; font-size:0.95rem; font-weight:700;">கதை ${currentChapterNum} / ${total}</span>
          ${nextNum ? `
            <button type="button" class="sheet-btn sheet-btn-view" onclick="window.switchPuranaChapter(${nextNum})" style="cursor:pointer; font-weight:700; padding:12px 26px; font-size:0.95rem;">
              அடுத்த கதை (${nextNum}) &rarr;
            </button>
          ` : `
            <button type="button" class="sheet-btn sheet-btn-view" onclick="window.scrollTo({top:0, behavior:'smooth'})" style="cursor:pointer; font-weight:700; padding:12px 24px;">
              நூலின் உச்சிக்குச் செல்க &uarr;
            </button>
          `}
        </div>

      </article>
    `;

    const dropdown = document.getElementById('chapterSelectDropdown');
    if (dropdown) dropdown.value = currentChapterNum;

    readingArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function updateUrl() {
    const newUrl = `${window.location.pathname}?id=${currentPuranaId}&chapter=${currentChapterNum}`;
    window.history.replaceState({}, '', newUrl);
  }

  function filterPuranas(query) {
    const q = query.trim().toLowerCase();
    const filtered = puranasCatalog.filter(p => {
      return p.title.toLowerCase().includes(q) || (p.category && p.category.toLowerCase().includes(q));
    });
    renderPuranaSidebar(filtered);
  }

  window.switchPurana = function(puranaId) {
    loadPuranaData(puranaId, 1);
  };

  window.switchPuranaChapter = function(chapNum) {
    currentChapterNum = chapNum;
    updateUrl();
    renderCurrentChapterContent();
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
