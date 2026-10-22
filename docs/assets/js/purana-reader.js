/**
 * assets/js/purana-reader.js
 * Dedicated Mega-Canon Digital Reader Engine for 18 Mahapuranas & 2 Itihasas
 * Features:
 * - Dynamic loading of all 20 Purana & Itihasa JSON files
 * - Fast sidebar navigation & live search
 * - Large font ergonomic reading mode (22px / 1.25rem+)
 * - 3 Curated verified illustrations per chapter with Lightbox zoom
 * - Structured Concept Questions & 3 Ds Life Application Cards
 * - Full URL synchronization (?purana=mahabharatam&chapter=1)
 */

(function() {
  'use strict';

  let currentPuranaId = 'mahabharatam';
  let currentChapterNum = 1;
  let puranasCatalog = [];
  let currentPuranaData = null;

  async function initPuranaReader() {
    const urlParams = new URLSearchParams(window.location.search);
    const pParam = urlParams.get('purana');
    const cParam = parseInt(urlParams.get('chapter'), 10);

    if (pParam) currentPuranaId = pParam;
    if (cParam && !isNaN(cParam) && cParam > 0) currentChapterNum = cParam;

    try {
      const resp = await fetch('data/puranas/puranas_index.json');
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const indexData = await resp.json();
      puranasCatalog = indexData.catalog || [];
      renderPuranaSidebar(puranasCatalog);
      await loadPuranaData(currentPuranaId, currentChapterNum);
    } catch (e) {
      console.error('Failed to initialize Purana Reader:', e);
      renderErrorState();
    }
  }

  function renderPuranaSidebar(catalog) {
    const listEl = document.getElementById('puranaBookList');
    if (!listEl) return;

    listEl.innerHTML = catalog.map(item => {
      const isActive = item.id === currentPuranaId;
      return `
        <button type="button" class="purana-shelf-item ${isActive ? 'active' : ''}" onclick="window.switchPurana('${item.id}')" data-id="${item.id}" style="display:flex; align-items:flex-start; gap:12px; padding:12px 14px; width:100%; border-radius:12px; margin-bottom:8px; border:1px solid ${isActive ? item.color : 'rgba(255,255,255,0.08)'}; background:${isActive ? 'linear-gradient(135deg, rgba(212,175,55,0.18), rgba(15,23,42,0.9))' : 'rgba(15,23,42,0.6)'}; text-align:left; cursor:pointer; transition:all 0.2s ease;">
          <span style="font-size:1.4rem; line-height:1;">${item.icon || '📜'}</span>
          <div style="flex:1; overflow:hidden;">
            <div style="font-size:0.95rem; font-weight:800; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${item.title}</div>
            <div style="font-size:0.76rem; color:#94a3b8; margin-top:2px;">${item.category} • ${item.total_chapters} அத்தியாயங்கள்</div>
          </div>
        </button>
      `;
    }).join('');
  }

  async function loadPuranaData(puranaId, targetChapter = 1) {
    currentPuranaId = puranaId;
    currentChapterNum = targetChapter;
    updateUrl();

    // Update active highlight in sidebar
    document.querySelectorAll('.purana-shelf-item').forEach(el => {
      if (el.getAttribute('data-id') === puranaId) {
        el.classList.add('active');
        el.style.border = '1px solid var(--gold)';
      } else {
        el.classList.remove('active');
        el.style.border = '1px solid rgba(255,255,255,0.08)';
      }
    });

    const readingArea = document.getElementById('puranaReadingArea');
    if (readingArea) {
      readingArea.innerHTML = `<div style="text-align:center; padding:60px 20px; color:var(--gold);"><span class="spinner"></span> <strong>${puranaId}</strong> மூலப் பெருநூல் பக்கங்கள் ஏற்றப்படுகின்றன...</div>`;
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
            <h3 style="color:#ef4444;">நூல் தரவு ஏற்றுவதில் பிழை</h3>
            <p style="color:#e2e8f0;">${puranaId}.json கோப்பினை வாசிக்க முடியவில்லை. பக்கத்தை மறுஏற்றம் செய்யவும்.</p>
          </div>
        `;
      }
    }
  }

  function renderPuranaHeader(doc) {
    const titleEl = document.getElementById('puranaDisplayTitle');
    const authorEl = document.getElementById('puranaDisplayAuthor');
    const badgeEl = document.getElementById('puranaDisplayBadge');
    const summaryEl = document.getElementById('puranaDisplaySummary');

    if (titleEl) titleEl.innerText = doc.title;
    if (authorEl) authorEl.innerText = `அருளியவர்: ${doc.author} • வகைப்பாடு: ${doc.category}`;
    if (badgeEl) badgeEl.innerText = `${doc.sections_name}: மொத்தம் ${doc.total_chapters} பகுதிகள்`;
    if (summaryEl) summaryEl.innerHTML = doc.summary;
  }

  function renderChapterTabs(doc) {
    const tabsCont = document.getElementById('puranaChapterTabs');
    if (!tabsCont || !doc.chapters) return;

    tabsCont.innerHTML = `
      <div style="display:flex; gap:8px; overflow-x:auto; padding:6px 0 12px; scrollbar-width:thin;">
        ${doc.chapters.map(ch => {
          const isActive = ch.chapterNumber === currentChapterNum;
          return `
            <button type="button" class="purana-tab-btn ${isActive ? 'active' : ''}" onclick="window.switchPuranaChapter(${ch.chapterNumber})" style="white-space:nowrap; padding:8px 16px; border-radius:12px; font-weight:700; font-size:0.88rem; cursor:pointer; background:${isActive ? 'linear-gradient(135deg, var(--gold), #b45309)' : 'rgba(255,255,255,0.06)'}; color:${isActive ? '#02131e' : '#cbd5e1'}; border:1px solid ${isActive ? 'var(--gold-bright)' : 'rgba(255,255,255,0.12)'};">
              <span>அத்தியாயம் ${ch.chapterNumber}</span>: ${ch.title.split('(')[0].trim()}
            </button>
          `;
        }).join('')}
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

    const images = chap.images || [];
    const imgHero = images[0] || null;
    const imgNarrative = images[1] || null;
    const imgDharma = images[2] || null;

    const questionsHtml = (chap.questions || []).map(q => {
      const isProject = /செயல் திட்டம்|குடும்பச் செயல்/i.test(q);
      const icon = isProject ? '✨' : '❓';
      const badge = isProject ? 'குடும்பச் செயல் திட்டம் • Activity' : 'சிந்தனை வினா • Concept Question';
      const borderCol = isProject ? 'rgba(234, 179, 8, 0.45)' : 'rgba(192, 132, 252, 0.4)';
      const bgCol = isProject ? 'linear-gradient(135deg, rgba(234, 179, 8, 0.16), rgba(234, 179, 8, 0.04))' : 'linear-gradient(135deg, rgba(192, 132, 252, 0.14), rgba(192, 132, 252, 0.04))';
      const tagCol = isProject ? '#facc15' : '#e9d5ff';

      return `
        <div style="background:${bgCol}; border:1px solid ${borderCol}; border-radius:16px; padding:18px 22px; margin-bottom:14px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-size:0.92rem; font-weight:800; background:rgba(0,0,0,0.5); color:${tagCol}; border:1px solid ${borderCol}; padding:4px 12px; border-radius:8px; display:inline-flex; align-items:center; gap:6px;">
              ${icon} ${badge}
            </span>
            <span style="font-size:0.8rem; color:#94a3b8;">சுயமதிப்பீடு &amp; விவாதம்</span>
          </div>
          <div style="font-size:1.18rem; color:#ffffff; line-height:1.85; font-weight:500;">${q}</div>
        </div>
      `;
    }).join('');

    const life3D = chap.lifeApplication3Ds || {};

    readingArea.innerHTML = `
      <article class="purana-reading-chapter" style="animation: fadeIn 0.3s ease;">
        
        <!-- Chapter Banner -->
        <div style="background:linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(8,14,26,0.95) 100%); border:1px solid rgba(212,175,55,0.3); border-radius:20px; padding:28px; margin-bottom:30px; box-shadow:0 12px 35px rgba(0,0,0,0.5);">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:12px;">
            <span style="background:rgba(212,175,55,0.15); color:var(--gold-bright); border:1px solid rgba(212,175,55,0.4); padding:4px 14px; border-radius:20px; font-weight:800; font-size:0.84rem;">
              அத்தியாயம் ${chap.chapterNumber} / ${total}
            </span>
            <span style="font-size:0.88rem; color:#94a3b8;">${currentPuranaData.sections_name} • மூல வேத சாஸ்திரம்</span>
          </div>
          <h2 style="color:#ffffff; font-size:2.1rem; font-weight:900; line-height:1.3; margin:0 0 10px 0; letter-spacing:-0.01em;">
            ${chap.title}
          </h2>
          <p style="color:#38bdf8; font-size:1.12rem; line-height:1.8; margin:0;">
            ${chap.synopsis}
          </p>
        </div>

        <!-- 1. Hero Canto Visual & Text Split -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(340px, 1fr)); gap:28px; align-items:center; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.12); border-radius:20px; padding:24px; margin-bottom:32px;">
          ${imgHero ? `
            <div style="border-radius:16px; overflow:hidden; box-shadow:0 14px 35px rgba(0,0,0,0.6); position:relative;">
              <img src="${imgHero.url}" alt="${imgHero.title}" style="width:100%; height:320px; object-fit:cover; display:block;">
              <div style="position:absolute; bottom:0; inset-inline:0; background:linear-gradient(180deg, transparent, rgba(0,0,0,0.95)); padding:12px 16px;">
                <span style="color:#fde047; font-weight:800; font-size:0.85rem;">${imgHero.title}</span>
                <div style="color:#e2e8f0; font-size:0.82rem; margin-top:3px;">${imgHero.caption}</div>
              </div>
            </div>
          ` : ''}
          <div style="font-size:1.22rem; line-height:2.0; color:#f8fafc;">
            <div style="display:inline-block; background:rgba(56,189,248,0.15); color:#7dd3fc; border:1px solid rgba(56,189,248,0.35); padding:3px 10px; border-radius:8px; font-size:0.8rem; font-weight:800; margin-bottom:12px;">
              பிரிவு 1 • மெய்ஞ்ஞான விரிவுரை
            </div>
            <div style="color:#ffffff; font-weight:500;">
              ${chap.exposition}
            </div>
          </div>
        </div>

        <!-- 2. Second Visual & Narrative Canto -->
        ${imgNarrative ? `
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(340px, 1fr)); gap:28px; align-items:center; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.12); border-radius:20px; padding:24px; margin-bottom:32px;">
            <div style="order:2; font-size:1.22rem; line-height:2.0; color:#f8fafc;">
              <div style="display:inline-block; background:rgba(251,146,60,0.15); color:#fdba74; border:1px solid rgba(251,146,60,0.35); padding:3px 10px; border-radius:8px; font-size:0.8rem; font-weight:800; margin-bottom:12px;">
                பிரிவு 2 • தர்ம நெறி &amp; வரலாற்றுச் சரிதம்
              </div>
              <p style="margin:0 0 16px 0;">
                இவ்வத்தியாயத்தின் நிகழ்வுகள் ஊடாக தர்மம் எவ்வாறு இறுதி வெற்றியைப் பெறுகிறது என்பதை வேதப் பெருநூல் விளக்குகிறது. மனிதனின் புலனடக்கம், தன்னலமற்ற தியாகம், மற்றும் வாக்கு மாறா வாய்மை ஆகிய மூன்று பண்புகளே பிரபஞ்சத்தின் அசைக்க முடியாத தூண்களாக நிலைபெற்றுள்ளன.
              </p>
              <p style="margin:0; color:#cbd5e1;">
                இதிகாசங்கள் மற்றும் புராணங்களின் ஒவ்வொரு வரியும் மாணவருக்கு உடனடி மன அமைதியையும், வாழ்வியல் சோதனைகளை எதிர்கொள்ளும் தீரத்தையும் புகட்டுகின்றன.
              </p>
            </div>
            <div style="order:1; border-radius:16px; overflow:hidden; box-shadow:0 14px 35px rgba(0,0,0,0.6); position:relative;">
              <img src="${imgNarrative.url}" alt="${imgNarrative.title}" style="width:100%; height:320px; object-fit:cover; display:block;">
              <div style="position:absolute; bottom:0; inset-inline:0; background:linear-gradient(180deg, transparent, rgba(0,0,0,0.95)); padding:12px 16px;">
                <span style="color:#fdba74; font-weight:800; font-size:0.85rem;">${imgNarrative.title}</span>
                <div style="color:#e2e8f0; font-size:0.82rem; margin-top:3px;">${imgNarrative.caption}</div>
              </div>
            </div>
          </div>
        ` : ''}

        <!-- 3. Practical 3 Ds Life Application Cards -->
        <div style="margin-bottom:36px;">
          <h3 style="color:#6ee7b7; font-size:1.45rem; font-weight:800; margin-bottom:16px; display:flex; align-items:center; gap:8px;">
            <span>🌿</span> 3 Ds வாழ்வியல் நெறிமுறை (Duty, Discipline, Dignity)
          </h3>
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:18px;">
            <div style="background:linear-gradient(135deg, rgba(56,189,248,0.14), rgba(56,189,248,0.03)); border:1px solid rgba(56,189,248,0.38); border-radius:16px; padding:20px;">
              <span style="background:rgba(0,0,0,0.4); color:#7dd3fc; border:1px solid rgba(56,189,248,0.4); font-size:0.88rem; font-weight:800; padding:4px 12px; border-radius:8px;">🛡️ கடமை (Duty)</span>
              <div style="font-size:1.16rem; line-height:1.85; color:#ffffff; margin-top:12px; font-weight:500;">
                ${life3D.duty || 'தமக்குரிய அறப்பணிகளையும் குடும்பப் பொறுப்புகளையும் இன்முகத்தோடு ஏற்றுச் செய்தல்.'}
              </div>
            </div>
            <div style="background:linear-gradient(135deg, rgba(250,204,21,0.14), rgba(250,204,21,0.03)); border:1px solid rgba(250,204,21,0.38); border-radius:16px; padding:20px;">
              <span style="background:rgba(0,0,0,0.4); color:#fde047; border:1px solid rgba(250,204,21,0.4); font-size:0.88rem; font-weight:800; padding:4px 12px; border-radius:8px;">⚖️ கட்டுப்பாடு (Discipline)</span>
              <div style="font-size:1.16rem; line-height:1.85; color:#ffffff; margin-top:12px; font-weight:500;">
                ${life3D.discipline || 'புலனடக்கம், மன உறுதி மற்றும் சத்திய நெறி தவறாத அன்றாட நடத்தை.'}
              </div>
            </div>
            <div style="background:linear-gradient(135deg, rgba(52,211,153,0.14), rgba(52,211,153,0.03)); border:1px solid rgba(52,211,153,0.38); border-radius:16px; padding:20px;">
              <span style="background:rgba(0,0,0,0.4); color:#6ee7b7; border:1px solid rgba(52,211,153,0.4); font-size:0.88rem; font-weight:800; padding:4px 12px; border-radius:8px;">👑 கண்ணியம் (Dignity)</span>
              <div style="font-size:1.16rem; line-height:1.85; color:#ffffff; margin-top:12px; font-weight:500;">
                ${life3D.dignity || 'சோதனைகளிலும் பிறர் நிந்தனைகளிலும் தளராமல் சுயமரியாதையுடன் திகழ்தல்.'}
              </div>
            </div>
          </div>
        </div>

        <!-- 4. Deep Concept Questions Bank -->
        <div style="margin-bottom:36px;">
          <h3 style="color:#e9d5ff; font-size:1.45rem; font-weight:800; margin-bottom:16px; display:flex; align-items:center; gap:8px;">
            <span>❓</span> அத்தியாயச் சிந்தனை வினாக்கள் &amp; செயல் திட்டம்
          </h3>
          ${questionsHtml}
        </div>

        <!-- Chapter Navigation Buttons -->
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; padding-top:20px; border-top:1px solid rgba(255,255,255,0.12);">
          ${prevNum ? `
            <button type="button" class="sheet-btn" onclick="window.switchPuranaChapter(${prevNum})" style="cursor:pointer; font-weight:700; padding:10px 18px;">
              &larr; முந்தைய பகுதி (${prevNum})
            </button>
          ` : '<div></div>'}
          <span style="color:#94a3b8; font-size:0.9rem;">அத்தியாயம் ${currentChapterNum} / ${total}</span>
          ${nextNum ? `
            <button type="button" class="sheet-btn sheet-btn-view" onclick="window.switchPuranaChapter(${nextNum})" style="cursor:pointer; font-weight:700; padding:10px 22px;">
              அடுத்த பகுதி (${nextNum}) &rarr;
            </button>
          ` : `
            <button type="button" class="sheet-btn sheet-btn-view" onclick="window.scrollTo({top:0, behavior:'smooth'})" style="cursor:pointer; font-weight:700; padding:10px 22px;">
              நூலின் முகப்புக்குச் செல்க &uarr;
            </button>
          `}
        </div>

      </article>
    `;

    // Highlight active chapter tab
    document.querySelectorAll('.purana-tab-btn').forEach(btn => {
      if (btn.innerText.includes(`அத்தியாயம் ${currentChapterNum}:`)) {
        btn.classList.add('active');
        btn.style.background = 'linear-gradient(135deg, var(--gold), #b45309)';
        btn.style.color = '#02131e';
      } else {
        btn.classList.remove('active');
        btn.style.background = 'rgba(255,255,255,0.06)';
        btn.style.color = '#cbd5e1';
      }
    });

    readingArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function updateUrl() {
    const newUrl = `${window.location.pathname}?purana=${currentPuranaId}&chapter=${currentChapterNum}`;
    window.history.replaceState({}, '', newUrl);
  }

  function filterPuranas(query) {
    const q = query.trim().toLowerCase();
    const filtered = puranasCatalog.filter(p => {
      return p.title.toLowerCase().includes(q) || p.summary.toLowerCase().includes(q) || p.category.toLowerCase().includes(q);
    });
    renderPuranaSidebar(filtered);
  }

  // Global window functions
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
