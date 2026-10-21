/* Multi-View Lineage Explorer: Miller Columns & Pedigree Path Navigator */
(function() {
  'use strict';

  let currentLang = localStorage.getItem('gkd_lang') || 'ta';
  let ancestorsMap = {};
  let rootId = 'parabrahman';
  let activePath = ['parabrahman', 'brahma', 'marichi', 'kashyapa', 'vivasvan', 'vaivasvata_manu', 'ikshvaku', 'vikukshi', 'kakutstha', 'mandhatri', 'harishchandra', 'rohita', 'bahu', 'sagara', 'asamanja', 'anshuman', 'dilipa1', 'bhagiratha', 'dilipa2', 'raghu', 'aja', 'dasharatha', 'sri_rama'];
  let currentFilter = 'all';

  const typeColors = {
    root: '#ec4899',
    creator: '#a855f7',
    prajapati: '#38bdf8',
    rishi: '#06b6d4',
    manu: '#f59e0b',
    solar: '#ea580c',
    lunar: '#3b82f6',
    avatar: '#10b981',
    tamil: '#e11d48',
    king: '#facc15'
  };

  const typeLabels = {
    root: { ta: 'பரம்பொருள்', en: 'Supreme Source' },
    creator: { ta: 'படைப்பு', en: 'Creator' },
    prajapati: { ta: 'பிரஜாபதி', en: 'Prajapati' },
    rishi: { ta: 'ரிஷி / முனிவர்', en: 'Rishi / Seer' },
    manu: { ta: 'மனு', en: 'Manu' },
    solar: { ta: 'சூரிய குலம்', en: 'Solar Clan' },
    lunar: { ta: 'சந்திர குலம்', en: 'Lunar Clan' },
    avatar: { ta: 'அவதாரம்', en: 'Avatara' },
    tamil: { ta: 'தமிழ் மரபு', en: 'Tamil Dynasty' },
    king: { ta: 'மன்னர்', en: 'Monarch' }
  };

  // Preset famous lineage journeys
  const famousJourneys = [
    {
      id: 'journey_rama',
      title_ta: '☀️ ஸ்ரீராமர் அவதார வம்சம் (இக்ஷ்வாகு ➔ தசரதர் ➔ ராமர் ➔ சோழர்)',
      title_en: '☀️ Sri Rama Descent (Ikshvaku ➔ Dasharatha ➔ Rama ➔ Cholas)',
      targetId: 'sri_rama'
    },
    {
      id: 'journey_krishna',
      title_ta: '🌙 ஸ்ரீகிருஷ்ணர் யது வம்சம் (சந்திரன் ➔ புரூரவஸ் ➔ யது ➔ வசுதேவர் ➔ கிருஷ்ணர்)',
      title_en: '🌙 Sri Krishna Descent (Chandra ➔ Pururavas ➔ Yadu ➔ Krishna)',
      targetId: 'sri_krishna'
    },
    {
      id: 'journey_pandavas',
      title_ta: '🏹 பாண்டவர் & பரீக்ஷித்து வம்சம் (புரு ➔ பரதன் ➔ சந்தனு ➔ அர்ஜுனன் ➔ பரீக்ஷித்து)',
      title_en: '🏹 Pandavas & Parikshit Line (Puru ➔ Bharata ➔ Shantanu ➔ Arjuna)',
      targetId: 'parikshit'
    },
    {
      id: 'journey_cholas',
      title_ta: '🐅 சோழர் மரபு (இக்ஷ்வாகு ➔ சிபி ➔ கரிகாலன் ➔ இராஜராஜ சோழன்)',
      title_en: '🐅 Chola Dynasty (Ikshvaku ➔ Sibi ➔ Karikala ➔ Rajaraja Chola)',
      targetId: 'rajaraja1'
    },
    {
      id: 'journey_pandyas',
      title_ta: '🐟 பாண்டியர் மரபு (சந்திரன் ➔ புரூரவஸ் ➔ மீன்கொடி ➔ நெடுஞ்செழியன்)',
      title_en: '🐟 Pandya Dynasty (Chandra ➔ Pururavas ➔ Twin-Fish ➔ Rajasimha)',
      targetId: 'rajasimha2'
    },
    {
      id: 'journey_pallavas',
      title_ta: '🪨 பல்லவர் மரபு (அங்கிரஸர் ➔ துரோணர் ➔ அஸ்வத்தாமன் ➔ மாமல்லன்)',
      title_en: '🪨 Pallava Dynasty (Angiras ➔ Drona ➔ Ashvatthama ➔ Mamalla)',
      targetId: 'narasimhavarman1'
    },
    {
      id: 'journey_buddha',
      title_ta: '☸️ சாக்கிய புத்தர் (இக்ஷ்வாகு ➔ பிருஹத்பலன் ➔ சுத்தோதனன் ➔ புத்தர்)',
      title_en: '☸️ Shakya Buddha Line (Ikshvaku ➔ Brihadbala ➔ Suddhodana ➔ Buddha)',
      targetId: 'gautama_buddha'
    }
  ];

  window.initLineageNavigator = function(flatList) {
    if (!flatList || !flatList.length) return;
    ancestorsMap = {};
    flatList.forEach(item => {
      ancestorsMap[item.id] = item;
    });

    renderJourneyPills();
    renderMillerColumns();
    renderPedigreePath();
    renderDossier(ancestorsMap[activePath[activePath.length - 1]]);
  };

  function renderJourneyPills() {
    const container = document.getElementById('lineageJourneyPills');
    if (!container) return;
    container.innerHTML = '';

    famousJourneys.forEach(j => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'journey-pill-btn';
      btn.textContent = currentLang === 'ta' ? j.title_ta : j.title_en;
      btn.onclick = () => {
        jumpToAncestor(j.targetId);
      };
      container.appendChild(btn);
    });
  }

  // Render Miller Columns (Hierarchical drill-down lists)
  function renderMillerColumns() {
    const container = document.getElementById('millerColumnsContainer');
    if (!container) return;
    container.innerHTML = '';

    // Columns correspond to each node in activePath plus one column for children of the active node
    for (let depth = 0; depth < activePath.length; depth++) {
      const parentId = depth === 0 ? null : activePath[depth - 1];
      const selectedId = activePath[depth];
      const column = createColumn(depth, parentId, selectedId);
      container.appendChild(column);
    }

    // Next child column if active leaf has children
    const leafId = activePath[activePath.length - 1];
    const leaf = ancestorsMap[leafId];
    if (leaf && leaf.children_ids && leaf.children_ids.length > 0) {
      const nextCol = createColumn(activePath.length, leafId, null);
      container.appendChild(nextCol);
    }

    // Scroll container horizontally to show the latest active column
    setTimeout(() => {
      container.scrollTo({ left: container.scrollWidth, behavior: 'smooth' });
    }, 50);
  }

  function createColumn(depth, parentId, selectedId) {
    const colDiv = document.createElement('div');
    colDiv.className = 'miller-column';

    let items = [];
    if (depth === 0) {
      items = [ancestorsMap[rootId]];
    } else {
      const parent = ancestorsMap[parentId];
      if (parent && parent.children_ids) {
        items = parent.children_ids.map(id => ancestorsMap[id]).filter(Boolean);
      }
    }

    // Column header indicating Generation / Stage
    const header = document.createElement('div');
    header.className = 'miller-col-header';
    const depthTitles = [
      { ta: 'நிலை 0: ஆதி மூலம்', en: 'Stage 0: Primordial Root' },
      { ta: 'நிலை 1: படைப்பு', en: 'Stage 1: Creation' },
      { ta: 'நிலை 2: பிரஜாபதிகள் & மனு', en: 'Stage 2: Prajapatis & Manu' },
      { ta: 'நிலை 3: ஆதி பரம்பரை', en: 'Stage 3: Ancestral Roots' },
      { ta: 'நிலை 4: சூர்ய/சந்திர மூலவர்கள்', en: 'Stage 4: Solar/Lunar Founders' },
      { ta: 'நிலை 5: மாமன்னர்கள்', en: 'Stage 5: Sovereign Kings' },
      { ta: 'நிலை 6: தர்ம சக்கரவர்த்திகள்', en: 'Stage 6: Chakravartins' }
    ];
    const dt = depthTitles[depth] || { ta: `தலைமுறை ${depth}`, en: `Generation ${depth}` };
    header.innerHTML = `<span>${currentLang === 'ta' ? dt.ta : dt.en}</span> <span class="badge-count">${items.length}</span>`;
    colDiv.appendChild(header);

    const listDiv = document.createElement('div');
    listDiv.className = 'miller-col-list';

    items.forEach(item => {
      const card = document.createElement('div');
      const isSelected = item.id === selectedId;
      card.className = `miller-card ${isSelected ? 'selected' : ''} type-${item.type}`;
      
      const dotColor = typeColors[item.type] || '#a855f7';
      const hasChildren = item.children_ids && item.children_ids.length > 0;

      card.innerHTML = `
        <div style="display: flex; align-items: center; gap: 8px;">
          <span class="miller-dot" style="background: ${dotColor};"></span>
          <div style="flex: 1; min-width: 0;">
            <div class="miller-name">${currentLang === 'ta' ? item.name_ta : item.name_en}</div>
            <div class="miller-role">${currentLang === 'ta' ? item.role_ta : item.role_en}</div>
          </div>
          ${hasChildren ? '<span class="miller-arrow">›</span>' : ''}
        </div>
      `;

      card.onclick = () => {
        // Truncate activePath up to current depth and append this item
        activePath = activePath.slice(0, depth);
        activePath.push(item.id);
        renderMillerColumns();
        renderPedigreePath();
        renderDossier(item);
      };

      listDiv.appendChild(card);
    });

    colDiv.appendChild(listDiv);
    return colDiv;
  }

  // Render Pedigree Breadcrumb / Ribbon Path
  function renderPedigreePath() {
    const ribbon = document.getElementById('lineagePedigreePath');
    if (!ribbon) return;
    ribbon.innerHTML = '';

    activePath.forEach((id, index) => {
      const item = ancestorsMap[id];
      if (!item) return;

      const pill = document.createElement('div');
      pill.className = `pedigree-step ${index === activePath.length - 1 ? 'current' : ''}`;
      pill.style.borderColor = typeColors[item.type] || '#a855f7';
      pill.innerHTML = `
        <span class="step-num">${index}</span>
        <span class="step-title">${currentLang === 'ta' ? item.name_ta : item.name_en}</span>
      `;
      pill.onclick = () => {
        activePath = activePath.slice(0, index + 1);
        renderMillerColumns();
        renderPedigreePath();
        renderDossier(item);
      };

      ribbon.appendChild(pill);

      if (index < activePath.length - 1) {
        const sep = document.createElement('span');
        sep.className = 'pedigree-sep';
        sep.textContent = '➔';
        ribbon.appendChild(sep);
      }
    });
  }

  // Render Detailed Ancestor Dossier Card
  function renderDossier(item) {
    const container = document.getElementById('lineageDossierCard');
    if (!container || !item) return;

    const dotColor = typeColors[item.type] || '#a855f7';
    const typeMeta = typeLabels[item.type] || { ta: item.type, en: item.type };

    const childrenNames = (item.children_ids || []).map(cid => {
      const child = ancestorsMap[cid];
      if (!child) return '';
      return `<button type="button" class="child-quick-jump-btn" onclick="window.selectAncestorChild('${cid}')">${currentLang === 'ta' ? child.name_ta : child.name_en} ›</button>`;
    }).join('');

    container.innerHTML = `
      <div class="dossier-inner" style="border-top: 4px solid ${dotColor};">
        <div class="dossier-header">
          <div>
            <span class="dossier-badge" style="background: ${dotColor}; color: #ffffff;">
              ${currentLang === 'ta' ? typeMeta.ta : typeMeta.en}
            </span>
            <h3 class="dossier-title">${currentLang === 'ta' ? item.name_ta : item.name_en}</h3>
            <div class="dossier-subtitle">${currentLang === 'ta' ? item.name_en : item.name_ta} • ${currentLang === 'ta' ? item.role_ta : item.role_en}</div>
          </div>
          <div class="dossier-generation-badge">
            ${currentLang === 'ta' ? `வம்சாவளி படி: ${item.depth}` : `Lineage Depth: ${item.depth}`}
          </div>
        </div>

        <div class="dossier-meta-grid">
          <div class="dossier-meta-item">
            <span class="meta-label">${currentLang === 'ta' ? 'காலம் / யுகம்:' : 'Era / Epoch:'}</span>
            <span class="meta-val">${item.epoch || (currentLang === 'ta' ? 'அநாதி' : 'Primordial')}</span>
          </div>
          <div class="dossier-meta-item">
            <span class="meta-label">${currentLang === 'ta' ? 'புராண & வரலாற்று ஆதாரம்:' : 'Scriptural Reference:'}</span>
            <span class="meta-val">${item.purana || '12 Mahapuranas'}</span>
          </div>
        </div>

        <div class="dossier-body">
          <h4 style="color: #f1f5f9; font-size: 0.95rem; margin-bottom: 6px;">${currentLang === 'ta' ? 'வரலாற்றுச் சுருக்கம் & பெருமைகள்:' : 'Historic Deeds & Significance:'}</h4>
          <p class="dossier-desc">${currentLang === 'ta' ? item.desc_ta : item.desc_en}</p>
        </div>

        ${childrenNames ? `
        <div class="dossier-children">
          <h4 style="color: #cbd5e1; font-size: 0.88rem; margin-bottom: 8px;">${currentLang === 'ta' ? 'நேரடி வழித்தோன்றல்கள் / பிள்ளைகள் (Click to Navigate):' : 'Direct Descendants (Click to Navigate):'}</h4>
          <div style="display: flex; flex-wrap: wrap; gap: 8px;">
            ${childrenNames}
          </div>
        </div>
        ` : ''}
      </div>
    `;
  }

  window.selectAncestorChild = function(cid) {
    jumpToAncestor(cid);
  };

  function jumpToAncestor(targetId) {
    const target = ancestorsMap[targetId];
    if (!target) return;

    // Find path from root to target
    function findPath(currId, visited = []) {
      if (currId === targetId) return visited.concat(currId);
      const curr = ancestorsMap[currId];
      if (!curr || !curr.children_ids) return null;
      for (let cid of curr.children_ids) {
        const res = findPath(cid, visited.concat(currId));
        if (res) return res;
      }
      return null;
    }

    const path = findPath(rootId);
    if (path) {
      activePath = path;
      renderMillerColumns();
      renderPedigreePath();
      renderDossier(target);
    }
  }

  // Quick Instant Search Auto-complete
  window.searchLineageNavigator = function(query) {
    const resultsContainer = document.getElementById('lineageSearchResults');
    if (!resultsContainer) return;

    if (!query || query.trim().length < 2) {
      resultsContainer.style.display = 'none';
      return;
    }

    const q = query.trim().toLowerCase();
    const matches = Object.values(ancestorsMap).filter(item => {
      return (item.name_ta && item.name_ta.toLowerCase().includes(q)) ||
             (item.name_en && item.name_en.toLowerCase().includes(q)) ||
             (item.role_ta && item.role_ta.toLowerCase().includes(q)) ||
             (item.desc_ta && item.desc_ta.toLowerCase().includes(q));
    }).slice(0, 10);

    if (matches.length === 0) {
      resultsContainer.innerHTML = `<div style="padding: 10px; color: #94a3b8; font-size: 0.85rem;">பொருத்தமான முன்னோர் காணப்படவில்லை.</div>`;
      resultsContainer.style.display = 'block';
      return;
    }

    resultsContainer.innerHTML = '';
    matches.forEach(m => {
      const row = document.createElement('div');
      row.className = 'search-result-row';
      row.innerHTML = `
        <span class="miller-dot" style="background: ${typeColors[m.type] || '#a855f7'};"></span>
        <div style="flex: 1;">
          <div style="font-weight: 700; color: #f8fafc; font-size: 0.92rem;">${currentLang === 'ta' ? m.name_ta : m.name_en}</div>
          <div style="font-size: 0.78rem; color: #94a3b8;">${currentLang === 'ta' ? m.role_ta : m.role_en} • ${currentLang === 'ta' ? m.name_en : m.name_ta}</div>
        </div>
        <span style="color: #c084fc; font-size: 0.82rem; font-weight: 600;">திறக்க ›</span>
      `;
      row.onclick = () => {
        jumpToAncestor(m.id);
        resultsContainer.style.display = 'none';
        document.getElementById('lineageSearchInput').value = '';
      };
      resultsContainer.appendChild(row);
    });
    resultsContainer.style.display = 'block';
  };

  // Close search on click outside
  document.addEventListener('click', (e) => {
    const results = document.getElementById('lineageSearchResults');
    const searchBox = document.getElementById('lineageSearchInput');
    if (results && searchBox && !results.contains(e.target) && e.target !== searchBox) {
      results.style.display = 'none';
    }
  });

  window.setLineageNavigatorLanguage = function(lang) {
    currentLang = lang;
    renderJourneyPills();
    renderMillerColumns();
    renderPedigreePath();
    renderDossier(ancestorsMap[activePath[activePath.length - 1]]);
  };

})();
