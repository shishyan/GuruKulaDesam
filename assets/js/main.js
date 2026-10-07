// Guru Kula Desam - Modern Video Portal Logic with Full Lyrics & Meaning Support
let currentFilter = 'all';
let currentSearch = '';

function enrichItem(it) {
  if (!it) return it;
  const lookup = (window.GURUKULA_ITEMS_BY_ID && window.GURUKULA_ITEMS_BY_ID[it.id]) || {};
  return {
    ...lookup,
    ...it,
    author: it.author || lookup.author || '',
    source: it.source || lookup.source || '',
    lyrics: it.lyrics || lookup.lyrics || '',
    meaning: it.meaning || lookup.meaning || '',
    category: it.category || lookup.category || ''
  };
}

function initPage(itemsData) {
  if (Array.isArray(itemsData)) {
    window.pageItems = itemsData.map(enrichItem);
  } else {
    window.pageItems = [];
  }
  renderCards();
}

function getFilteredItems() {
  if (!window.pageItems) return [];
  return window.pageItems.filter(it => {
    if (currentFilter !== 'all' && it.type !== currentFilter) return false;
    if (currentSearch) {
      const q = currentSearch.toLowerCase();
      const titleMatch = (it.title || '').toLowerCase().includes(q);
      const idMatch = (it.id || '').toLowerCase().includes(q);
      const authorMatch = (it.author || '').toLowerCase().includes(q);
      const sourceMatch = (it.source || '').toLowerCase().includes(q);
      const lyricsMatch = (it.lyrics || '').toLowerCase().includes(q);
      const meaningMatch = (it.meaning || '').toLowerCase().includes(q);
      return titleMatch || idMatch || authorMatch || sourceMatch || lyricsMatch || meaningMatch;
    }
    return true;
  });
}

function escapeHtml(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function renderCards() {
  const items = getFilteredItems();
  const grid = document.getElementById('cardsGrid');
  const countBadge = document.getElementById('itemCountBadge');

  if (countBadge) {
    countBadge.innerText = `காட்டப்படும் பாடல்கள்: ${items.length}`;
  }

  if (!grid) return;

  if (items.length === 0) {
    grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 70px 20px; color: var(--text-muted); font-size: 1.15rem;">பொருத்தமான பாடல்கள் காணப்படவில்லை (No matching items found)</div>';
    return;
  }

  grid.innerHTML = items.map(it => {
    const safeTitle = escapeHtml(it.title);
    const safeAuthor = escapeHtml(it.author);
    const safeSource = escapeHtml(it.source);
    const formattedLyrics = it.lyrics ? escapeHtml(it.lyrics).replace(/\\n/g, '<br>') : '';
    const safeMeaning = escapeHtml(it.meaning);
    const hasDetails = Boolean(it.lyrics || it.meaning || it.author);

    return `
    <div class="video-card" id="card-${it.id}">
      <div class="card-thumbnail" onclick="openPlayer('${it.id}', '${safeTitle.replace(/'/g, "\\'")}')">
        <img src="https://i.ytimg.com/vi/${it.id}/mqdefault.jpg" loading="lazy" alt="${safeTitle}">
        <span class="card-badge ${it.type === 'film' ? 'badge-film' : 'badge-audio'}">${it.type === 'film' ? 'Film' : 'Audio'}</span>
        <div class="card-play-btn" title="காணொளியை இயக்குக">▶</div>
      </div>
      <div class="card-body">
        <div class="card-title" onclick="openPlayer('${it.id}', '${safeTitle.replace(/'/g, "\\'")}')" title="${safeTitle}">
          ${safeTitle}
        </div>

        ${(safeAuthor || safeSource) ? `
          <div class="card-meta-line">
            ${safeAuthor ? `<span class="card-meta-tag">✍️ ${safeAuthor}</span>` : ''}
            ${safeSource ? `<span class="card-meta-tag">📖 ${safeSource}</span>` : ''}
          </div>
        ` : ''}

        <div class="card-footer">
          <span class="tag">${it.type === 'film' ? '🎬 முழுப் படம் (Film)' : '🎵 இசை வெளியீடு (Audio)'}</span>
          <a href="https://www.youtube.com/watch?v=${it.id}" target="_blank" rel="noopener noreferrer" class="card-yt-link" onclick="event.stopPropagation()">YouTube ↗</a>
        </div>

        ${hasDetails ? `
          <button type="button" class="card-lyrics-toggle-btn" onclick="toggleCardLyrics(event, '${it.id}')" aria-expanded="false">
            <span>📜 வரிகள் &amp; பொருள் விளக்கம்</span>
            <span class="lyrics-chevron">▾</span>
          </button>

          <div class="card-lyrics-drawer" id="drawer-${it.id}" style="display: none;">
            ${it.lyrics ? `
              <div class="drawer-section">
                <div class="drawer-section-title">📜 பாடல் வரிகள் (Lyrics)</div>
                <div class="drawer-lyrics-text">${formattedLyrics}</div>
              </div>
            ` : ''}

            ${it.meaning ? `
              <div class="drawer-section">
                <div class="drawer-section-title">💡 பொருள் விளக்கம் (Meaning)</div>
                <div class="drawer-meaning-text">${safeMeaning}</div>
              </div>
            ` : ''}

            <button type="button" class="drawer-play-btn" onclick="openPlayer('${it.id}', '${safeTitle.replace(/'/g, "\\'")}')">
              ▶ இந்த காணொளியை இயக்குக (Play Video)
            </button>
          </div>
        ` : ''}
      </div>
    </div>
    `;
  }).join('');
}

function toggleCardLyrics(e, itemId) {
  if (e) {
    e.preventDefault();
    e.stopPropagation();
  }
  const drawer = document.getElementById('drawer-' + itemId);
  const card = document.getElementById('card-' + itemId);
  const btn = card ? card.querySelector('.card-lyrics-toggle-btn') : null;
  if (!drawer) return;

  const isOpen = drawer.style.display !== 'none';
  drawer.style.display = isOpen ? 'none' : 'block';
  if (btn) {
    btn.classList.toggle('open', !isOpen);
    btn.setAttribute('aria-expanded', !isOpen ? 'true' : 'false');
  }
}

function setTypeFilter(type) {
  currentFilter = type;
  document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
  const target = document.getElementById('filter-' + type);
  if (target) target.classList.add('active');
  renderCards();
}

function onSearchInput(val) {
  currentSearch = val;
  renderCards();
}

function openPlayer(videoId, title) {
  let modal = document.getElementById('playerModal');
  let iframe = document.getElementById('modalIframe');
  let titleEl = document.getElementById('modalTitle');

  // If modal doesn't exist on page, create dynamically
  if (!modal) {
    modal = createPlayerModalElement();
    document.body.appendChild(modal);
    iframe = document.getElementById('modalIframe');
    titleEl = document.getElementById('modalTitle');
  }

  if (!iframe) return;

  iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1`;
  if (titleEl) titleEl.innerText = title;

  // Resolve item details
  let item = (window.GURUKULA_ITEMS_BY_ID && window.GURUKULA_ITEMS_BY_ID[videoId]) ||
             (window.pageItems && window.pageItems.find(x => x.id === videoId)) ||
             { id: videoId, title: title };
  item = enrichItem(item);

  // Render modal details section below the video
  let detailsEl = document.getElementById('modalDetails');
  if (!detailsEl) {
    detailsEl = document.createElement('div');
    detailsEl.id = 'modalDetails';
    detailsEl.className = 'modal-details';
    const box = document.getElementById('playerModalBox') || modal.querySelector('.player-modal-box');
    if (box) box.appendChild(detailsEl);
  }

  const safeTitle = escapeHtml(item.title || title);
  const safeAuthor = escapeHtml(item.author || '');
  const safeSource = escapeHtml(item.source || '');
  const formattedLyrics = item.lyrics ? escapeHtml(item.lyrics).replace(/\n/g, '<br>') : 'இப்பாடலின் வரிகள் சேகரிக்கப்பட்டு வருகின்றன.';
  const safeMeaning = escapeHtml(item.meaning || 'இப்பாடலின் தத்துவப் பொருள் விளக்கம் சேகரிக்கப்பட்டு வருகிறது.');
  const rawLyrics = item.lyrics || '';

  detailsEl.innerHTML = `
    <div class="modal-meta-row">
      <div class="modal-meta-tags">
        <span class="modal-meta-tag badge-${item.type === 'film' ? 'film' : 'audio'}">
          ${item.type === 'film' ? '🎬 முழுப் படம் (Cinematic Film)' : '🎵 இசை வெளியீடு (Sacred Audio)'}
        </span>
        ${safeAuthor ? `<span class="modal-meta-tag">✍️ ஆசிரியர்: <strong>${safeAuthor}</strong></span>` : ''}
        ${safeSource ? `<span class="modal-meta-tag">📖 மூலம்: <strong>${safeSource}</strong></span>` : ''}
      </div>

      <div class="modal-action-buttons">
        <a href="https://www.youtube.com/watch?v=${videoId}" target="_blank" rel="noopener noreferrer" class="modal-btn modal-btn-yt">
          ▶ YouTube-ல் காண்க ↗
        </a>
        ${rawLyrics ? `
          <button type="button" class="modal-btn modal-btn-copy" onclick="copyLyricsText(this, ${JSON.stringify(rawLyrics)})">
            📋 வரிகளை நகலெடு
          </button>
        ` : ''}
      </div>
    </div>

    <div class="modal-content-grid">
      <div class="modal-box modal-lyrics-box">
        <div class="modal-box-header">
          <span class="modal-box-icon">📜</span>
          <h4 class="modal-box-title">பாடல் வரிகள் (Sacred Lyrics)</h4>
        </div>
        <div class="modal-box-body lyrics-body">${formattedLyrics}</div>
      </div>

      <div class="modal-box modal-meaning-box">
        <div class="modal-box-header">
          <span class="modal-box-icon">💡</span>
          <h4 class="modal-box-title">பொருள் விளக்கம் &amp; தத்துவம் (Spiritual Meaning)</h4>
        </div>
        <div class="modal-box-body meaning-body">${safeMeaning}</div>
      </div>
    </div>

    <div class="modal-bottom-actions">
      <button type="button" class="modal-btn modal-btn-top" onclick="scrollToModalTop()">
        ▲ காணொளிக்குத் திரும்புக (Back to Video)
      </button>
      <button type="button" class="modal-btn modal-btn-close-bottom" onclick="closePlayer()">
        ✕ மூடுக (Close Player)
      </button>
    </div>
  `;

  modal.classList.add('active');
  document.body.style.overflow = 'hidden';

  // Scroll modal box to top when opening
  const modalBox = document.getElementById('playerModalBox') || modal.querySelector('.player-modal-box');
  if (modalBox) {
    modalBox.scrollTop = 0;
  }
}

function scrollToModalDetails() {
  const details = document.getElementById('modalDetails');
  const box = document.getElementById('playerModalBox') || document.querySelector('.player-modal-box');
  if (details && box) {
    const topPos = details.offsetTop - 55;
    box.scrollTo({ top: Math.max(0, topPos), behavior: 'smooth' });
  }
}

function scrollToModalTop() {
  const box = document.getElementById('playerModalBox') || document.querySelector('.player-modal-box');
  if (box) {
    box.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

function createPlayerModalElement() {
  const modal = document.createElement('div');
  modal.className = 'player-modal';
  modal.id = 'playerModal';
  modal.onclick = function(e) { if (e.target === this) closePlayer(); };
  modal.innerHTML = `
    <div class="player-modal-box" id="playerModalBox">
      <div class="modal-header">
        <div class="modal-title" id="modalTitle">Now Playing</div>
        <div class="modal-header-actions">
          <button type="button" class="modal-scroll-btn" onclick="scrollToModalDetails()" title="வரிகளுக்குச் செல்க">
            📜 வரிகள் &amp; பொருள் ↓
          </button>
          <button type="button" class="modal-close-btn" onclick="closePlayer()" title="மூடுக">✕ மூடுக (Close)</button>
        </div>
      </div>
      <div class="modal-iframe-wrapper" id="modalIframeWrapper">
        <iframe id="modalIframe" src="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      </div>
      <div class="modal-scroll-hint" onclick="scrollToModalDetails()">
        <span>▼ கீழே பாடல் வரிகள் &amp; தத்துவப் பொருள் விளக்கம் (Scroll down for Lyrics &amp; Meaning) ▼</span>
      </div>
      <div class="modal-details" id="modalDetails"></div>
    </div>
  `;
  return modal;
}

// Global escape key listener
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closePlayer();
  }
});

function copyLyricsText(btn, text) {
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => {
    const originalText = btn.innerHTML;
    btn.innerHTML = '✓ நகலெடுக்கப்பட்டது!';
    btn.style.borderColor = 'var(--gold)';
    btn.style.color = 'var(--gold-bright)';
    setTimeout(() => {
      btn.innerHTML = originalText;
      btn.style.borderColor = '';
      btn.style.color = '';
    }, 2200);
  }).catch(err => {
    console.error('Failed to copy lyrics:', err);
  });
}

function closePlayer() {
  const modal = document.getElementById('playerModal');
  const iframe = document.getElementById('modalIframe');

  if (modal && iframe) {
    iframe.src = '';
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

function toggleMobileNav() {
  const nav = document.getElementById('mainNav');
  const toggleBtn = document.getElementById('mobileNavToggle') || document.querySelector('.mobile-toggle');
  const overlay = document.getElementById('navOverlay');
  if (!nav) return;
  
  const isOpen = nav.classList.toggle('open');
  if (overlay) overlay.classList.toggle('open', isOpen);
  if (toggleBtn) {
    toggleBtn.innerHTML = isOpen ? '✕' : '☰';
    toggleBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  }
  document.body.style.overflow = isOpen ? 'hidden' : '';
}

function closeMobileNav() {
  const nav = document.getElementById('mainNav');
  const toggleBtn = document.getElementById('mobileNavToggle') || document.querySelector('.mobile-toggle');
  const overlay = document.getElementById('navOverlay');
  if (nav && nav.classList.contains('open')) {
    nav.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
    if (toggleBtn) {
      toggleBtn.innerHTML = '☰';
      toggleBtn.setAttribute('aria-expanded', 'false');
    }
    document.body.style.overflow = '';
  }
}

// Multi-dropdown support
function toggleDropdown(e, dropdownId) {
  if (e) {
    e.preventDefault();
    e.stopPropagation();
  }
  const targetId = dropdownId || (e && e.currentTarget && e.currentTarget.id ? e.currentTarget.id.replace('Btn', '') : null);
  const dropdown = targetId ? document.getElementById(targetId) : (e ? e.currentTarget.closest('.nav-dropdown') : document.querySelector('.nav-dropdown'));
  if (!dropdown) return;
  const wasOpen = dropdown.classList.contains('open');
  document.querySelectorAll('.nav-dropdown').forEach(d => {
    if (d !== dropdown) d.classList.remove('open');
  });
  dropdown.classList.toggle('open', !wasOpen);
  const toggleBtn = dropdown.querySelector('.dropdown-toggle');
  if (toggleBtn) toggleBtn.setAttribute('aria-expanded', !wasOpen ? 'true' : 'false');
}

document.addEventListener('click', (e) => {
  document.querySelectorAll('.nav-dropdown').forEach(dropdown => {
    if (!dropdown.contains(e.target)) {
      dropdown.classList.remove('open');
      const toggleBtn = dropdown.querySelector('.dropdown-toggle');
      if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'false');
    }
  });
});

// Close player and menus on ESC key
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    closePlayer();
    closeMobileNav();
    document.querySelectorAll('.nav-dropdown').forEach(d => d.classList.remove('open'));
  }
});

// Sheet Modal Handlers
function openSheetModal(imgSrc, pageNum, pageTitle, gradeLabel) {
  const modal = document.getElementById('sheetModal');
  const modalImg = document.getElementById('sheetModalImg');
  const modalTitle = document.getElementById('sheetModalTitle');
  if (modal && modalImg) {
    modalImg.src = imgSrc;
    const label = gradeLabel || 'பாடநூல்';
    if (modalTitle) modalTitle.innerText = `${label} — பக்கம் ${pageNum} ${pageTitle ? '• ' + pageTitle : ''}`;
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeSheetModal() {
  const modal = document.getElementById('sheetModal');
  const modalImg = document.getElementById('sheetModalImg');
  if (modal) {
    modal.classList.remove('active');
    if (modalImg) modalImg.src = '';
    document.body.style.overflow = '';
  }
}
