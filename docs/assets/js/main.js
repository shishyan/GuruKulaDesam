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

  iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1&enablejsapi=1&rel=0&playsinline=1`;
  if (titleEl) titleEl.innerText = title;

  // Render or update direct YouTube link notice (guarantees playback if embed is restricted)
  let directNotice = document.getElementById('modalDirectYtNotice');
  if (!directNotice) {
    directNotice = document.createElement('div');
    directNotice.id = 'modalDirectYtNotice';
    directNotice.className = 'modal-direct-yt-notice';
    const iframeWrap = document.getElementById('modalIframeWrapper') || (modal && modal.querySelector('.modal-iframe-wrapper'));
    if (iframeWrap && iframeWrap.parentNode) {
      iframeWrap.parentNode.insertBefore(directNotice, iframeWrap.nextSibling);
    }
  }
  if (directNotice) {
    directNotice.innerHTML = `
      <div class="direct-notice-inner">
        <span>💡 காணொளி அல்லது ஆடியோ இங்கு இயங்கவில்லை எனில் (If video playback is restricted):</span>
        <a href="https://www.youtube.com/watch?v=${videoId}" target="_blank" rel="noopener noreferrer" class="direct-yt-btn">
          ▶ YouTube-ல் நேரடியாகத் திறக்க (Watch on YouTube) ↗
        </a>
      </div>
    `;
  }

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

function toggleModalFullscreen() {
  const modalBox = document.getElementById('playerModalBox') || document.querySelector('.player-modal-box');
  const btn = document.querySelector('.modal-fullscreen-btn');
  
  // 1. If currently in CSS Big / Theater mode, exit it
  if (modalBox && modalBox.classList.contains('modal-theater-mode')) {
    modalBox.classList.remove('modal-theater-mode');
    if ((document.fullscreenElement || document.webkitFullscreenElement) && document.exitFullscreen) {
      document.exitFullscreen().catch(() => {});
    }
    if (btn) btn.innerHTML = '⛶ பெரிய திரை (Big Mode)';
    return;
  }

  // 2. If currently in native hardware fullscreen, exit it
  if (document.fullscreenElement || document.webkitFullscreenElement) {
    if (document.exitFullscreen) {
      document.exitFullscreen().catch(() => {});
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    }
    if (modalBox) modalBox.classList.remove('modal-theater-mode');
    if (btn) btn.innerHTML = '⛶ பெரிய திரை (Big Mode)';
    return;
  }

  // 3. Otherwise enter Big Mode: attempt hardware fullscreen, fallback gracefully to CSS theater mode
  const target = modalBox || document.documentElement;
  const req = target.requestFullscreen || target.webkitRequestFullscreen || target.mozRequestFullScreen || target.msRequestFullscreen;

  if (req) {
    try {
      const p = req.call(target);
      if (p && p.then) {
        p.then(() => {
          if (btn) btn.innerHTML = '⛶ இயல்பு (Exit Big Mode)';
        }).catch(() => {
          // Hardware fullscreen not allowed by browser/permissions-policy: activate CSS Big Mode!
          if (modalBox) modalBox.classList.add('modal-theater-mode');
          if (btn) btn.innerHTML = '⛶ இயல்பு (Exit Big Mode)';
        });
      } else {
        if (btn) btn.innerHTML = '⛶ இயல்பு (Exit Big Mode)';
      }
    } catch (e) {
      if (modalBox) modalBox.classList.add('modal-theater-mode');
      if (btn) btn.innerHTML = '⛶ இயல்பு (Exit Big Mode)';
    }
  } else {
    if (modalBox) modalBox.classList.add('modal-theater-mode');
    if (btn) btn.innerHTML = '⛶ இயல்பு (Exit Big Mode)';
  }
}

document.addEventListener('fullscreenchange', function() {
  const btn = document.querySelector('.modal-fullscreen-btn');
  const modalBox = document.getElementById('playerModalBox') || document.querySelector('.player-modal-box');
  if (!document.fullscreenElement) {
    if (modalBox && !modalBox.classList.contains('modal-theater-mode')) {
      if (btn) btn.innerHTML = '⛶ பெரிய திரை (Big Mode)';
    }
  } else {
    if (btn) btn.innerHTML = '⛶ இயல்பு (Exit Big Mode)';
  }
});

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
          <button type="button" class="modal-fullscreen-btn" onclick="toggleModalFullscreen()" title="பெரிய திரை (Toggle Big Mode / Fullscreen)">⛶ பெரிய திரை (Big Mode)</button>
          <button type="button" class="modal-scroll-btn" onclick="scrollToModalDetails()" title="வரிகளுக்குச் செல்க">
            📜 வரிகள் &amp; பொருள் ↓
          </button>
          <button type="button" class="modal-close-btn" onclick="closePlayer()" title="மூடுக">✕ மூடுக (Close)</button>
        </div>
      </div>
      <div class="modal-iframe-wrapper" id="modalIframeWrapper">
        <iframe id="modalIframe" src="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share; fullscreen" referrerpolicy="strict-origin-when-cross-origin"></iframe>
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
  if (document.fullscreenElement) { document.exitFullscreen().catch(() => {}); }
  const modal = document.getElementById('playerModal');
  const iframe = document.getElementById('modalIframe');

  if (modal && iframe) {
    iframe.src = '';
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

function toggleMobileNav() {
  toggleLeftStrip();
}

function closeMobileNav() {
  closeMobileStrip();
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



/* ========================================================================== */
/* GURUKULA APP SHELL: LEFT STRIP, CONTEXT BAR, USER PROFILE & PREFERENCES     */
/* ========================================================================== */

const DEFAULT_USER_PREFS = {
  name: 'அன்பான சாதகர்',
  tier: 'tier1',
  avatar: '👤',
  theme: 'cosmic',
  fontStyle: 'mukta',
  fontScale: 1.0,
  navLayout: 'sidebar', // 'sidebar' (default), 'topbar' (classic), 'hybrid' (both)
  autoplay: false,
  continuous: false,
  dailyVirtue: true,
  streakDays: 1,
  lastVisit: new Date().toISOString().split('T')[0],
  completedLessons: 0,
  bookmarks: []
};

let userPrefs = { ...DEFAULT_USER_PREFS };

function loadUserPreferences() {
  try {
    const saved = localStorage.getItem('GURUKULA_USER_PREFS');
    if (saved) {
      userPrefs = { ...DEFAULT_USER_PREFS, ...JSON.parse(saved) };
      if (userPrefs.theme === 'gold' || !userPrefs.theme) userPrefs.theme = 'cosmic';
    }
  } catch (e) {
    console.warn('Failed to load user preferences:', e);
  }

  // Track visit streak
  const today = new Date().toISOString().split('T')[0];
  if (userPrefs.lastVisit !== today) {
    const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
    if (userPrefs.lastVisit === yesterday) {
      userPrefs.streakDays = (userPrefs.streakDays || 1) + 1;
    } else {
      userPrefs.streakDays = 1;
    }
    userPrefs.lastVisit = today;
    saveUserPreferences();
  }

  applyUserPreferences();
}

function saveUserPreferences() {
  try {
    localStorage.setItem('GURUKULA_USER_PREFS', JSON.stringify(userPrefs));
  } catch (e) {
    console.warn('Failed to save preferences:', e);
  }
}

function applyUserPreferences() {
  // Theme
  document.body.classList.remove('theme-cosmic', 'theme-midnight', 'theme-amoled');
  if (userPrefs.theme === 'midnight') document.body.classList.add('theme-midnight');
  else if (userPrefs.theme === 'amoled') document.body.classList.add('theme-amoled');
  else document.body.classList.add('theme-cosmic');

  // Font Style
  document.body.classList.remove('font-noto', 'font-mukta');
  if (userPrefs.fontStyle === 'noto') document.body.classList.add('font-noto');
  else document.body.classList.add('font-mukta');

  // Font Scale
  const scale = userPrefs.fontScale || 1.0;
  document.documentElement.style.setProperty('--user-font-scale', scale);
  const indicator = document.getElementById('fontScaleIndicator');
  if (indicator) indicator.innerText = Math.round(scale * 100) + '%';
  const sliderLabel = document.getElementById('sliderFontLabel');
  if (sliderLabel) sliderLabel.innerText = Math.round(scale * 100) + '% ' + (scale === 1.0 ? '(இயல்பு)' : '');

  // Navigation Shell Layout Mode
  const layout = userPrefs.navLayout || 'sidebar';
  const strip = document.getElementById('leftStripBar');
  const oldNav = document.getElementById('mainNav');
  const contextTabsNav = document.getElementById('contextTabsNav');

  document.body.classList.remove('layout-sidebar', 'layout-topbar', 'layout-hybrid');
  document.body.classList.add('layout-' + layout);

  if (layout === 'topbar') {
    // Classic top navbar mode
    if (strip) strip.style.display = 'none';
    if (oldNav) oldNav.style.display = 'flex';
    if (contextTabsNav) contextTabsNav.style.display = 'none';
    document.body.style.paddingLeft = '0';
  } else if (layout === 'hybrid') {
    // Dual Hybrid Shell
    if (strip) strip.style.display = 'flex';
    if (oldNav) oldNav.style.display = 'flex';
    if (contextTabsNav) contextTabsNav.style.display = 'flex';
    if (window.innerWidth >= 992) {
      const isExp = strip && strip.classList.contains('expanded');
      document.body.style.paddingLeft = isExp ? '230px' : '68px';
    }
  } else {
    // 'sidebar' (DEFAULT): Left sidebar dock + clean context-sensitive top tabs
    if (strip) strip.style.display = 'flex';
    if (oldNav) oldNav.style.display = 'none';
    if (contextTabsNav) contextTabsNav.style.display = 'flex';
    if (window.innerWidth >= 992) {
      const isExp = strip && strip.classList.contains('expanded');
      document.body.style.paddingLeft = isExp ? '230px' : '68px';
    }
  }

  // Update layout radio in Settings modal
  const layoutRadios = document.querySelectorAll('input[name="layoutChoice"]');
  layoutRadios.forEach(r => { r.checked = (r.value === layout); });

  // Profile Badges & Avatars in UI
  const pillAvatar = document.getElementById('pillAvatarIcon');
  const pillName = document.getElementById('pillUserName');
  const pillTier = document.getElementById('pillUserTier');
  const stripAvatar = document.getElementById('stripAvatarIcon');
  const stripName = document.getElementById('stripUserName');

  const tierMap = {
    'tier1': 'தரம் 1-4',
    'tier2': 'தரம் 5-8',
    'tier3': 'தரம் 9-12'
  };

  if (pillAvatar) pillAvatar.innerText = userPrefs.avatar || '👤';
  if (pillName) pillName.innerText = userPrefs.name || 'சாதகர்';
  if (pillTier) pillTier.innerText = tierMap[userPrefs.tier] || 'சாதகர்';
  if (stripAvatar) stripAvatar.innerText = userPrefs.avatar || '👤';
  if (stripName) stripName.innerText = userPrefs.name || 'சுயவிவரம்';

  // Update modal fields if open
  const largeAvatar = document.getElementById('profileLargeAvatar');
  const dispHead = document.getElementById('profileDisplayNameHead');
  const tierBadge = document.getElementById('profileTierBadge');
  const streakText = document.getElementById('profileStreakDays');
  const lessonsText = document.getElementById('profileLessonsCount');
  const nameInput = document.getElementById('prefUserNameInput');
  const tierSelect = document.getElementById('prefUserTierSelect');

  if (largeAvatar) largeAvatar.innerText = userPrefs.avatar || '👤';
  if (dispHead) dispHead.innerText = userPrefs.name || 'அன்பான சாதகர்';
  if (tierBadge) {
    const fullTierMap = {
      'tier1': '🌟 தொடக்க சாதகர் (Grade 1-4)',
      'tier2': '🪔 இடைநிலை சாதகர் (Grade 5-8)',
      'tier3': '🔱 உயர்நிலை சிவநேசர் (Grade 9-12)'
    };
    tierBadge.innerText = fullTierMap[userPrefs.tier] || fullTierMap['tier1'];
  }
  if (streakText) streakText.innerText = (userPrefs.streakDays || 1) + ' நாள்';
  if (lessonsText) lessonsText.innerText = (userPrefs.completedLessons || 0).toString();
  if (nameInput && nameInput.value !== userPrefs.name) nameInput.value = userPrefs.name;
  if (tierSelect) tierSelect.value = userPrefs.tier || 'tier1';

  // Radio choices in Settings modal
  const themeRadios = document.querySelectorAll('input[name="themeChoice"]');
  themeRadios.forEach(r => { r.checked = (r.value === userPrefs.theme); });
  const fontRadios = document.querySelectorAll('input[name="fontChoice"]');
  fontRadios.forEach(r => { r.checked = (r.value === userPrefs.fontStyle); });

  const apCb = document.getElementById('prefAutoplay');
  if (apCb) apCb.checked = Boolean(userPrefs.autoplay);
  const contCb = document.getElementById('prefContinuous');
  if (contCb) contCb.checked = Boolean(userPrefs.continuous);
  const dvCb = document.getElementById('prefDailyVirtue');
  if (dvCb) dvCb.checked = Boolean(userPrefs.dailyVirtue);

  // Update stats box
  const sDays = document.getElementById('statDaysVisited');
  const sLessons = document.getElementById('statLessonsCompleted');
  const sBooks = document.getElementById('statBookmarksCount');
  if (sDays) sDays.innerText = userPrefs.streakDays || 1;
  if (sLessons) sLessons.innerText = userPrefs.completedLessons || 0;
  if (sBooks) sBooks.innerText = (userPrefs.bookmarks && userPrefs.bookmarks.length) || 0;
}

function adjustFontSize(delta) {
  let scale = (userPrefs.fontScale || 1.0) + delta;
  scale = Math.max(0.82, Math.min(1.28, Math.round(scale * 100) / 100));
  userPrefs.fontScale = scale;
  saveUserPreferences();
  applyUserPreferences();
}

function changeNavLayout(layout) {
  userPrefs.navLayout = layout;
  saveUserPreferences();
  applyUserPreferences();
}

function changeTheme(themeName) {
  userPrefs.theme = themeName;
  saveUserPreferences();
  applyUserPreferences();
}

function cycleTheme() {
  const themes = ['cosmic', 'midnight', 'amoled'];
  const curIdx = themes.indexOf(userPrefs.theme || 'cosmic');
  const nextTheme = themes[(curIdx + 1) % themes.length];
  changeTheme(nextTheme);
}

function changeFontStyle(fontName) {
  userPrefs.fontStyle = fontName;
  saveUserPreferences();
  applyUserPreferences();
}

function selectAvatar(icon) {
  userPrefs.avatar = icon;
  document.querySelectorAll('.avatar-option').forEach(btn => {
    btn.classList.toggle('selected', btn.innerText.trim() === icon);
  });
  saveUserPreferences();
  applyUserPreferences();
}

function saveUserProfileFields() {
  const nameInput = document.getElementById('prefUserNameInput');
  const tierSelect = document.getElementById('prefUserTierSelect');
  if (nameInput) userPrefs.name = nameInput.value.trim() || 'அன்பான சாதகர்';
  if (tierSelect) userPrefs.tier = tierSelect.value;
  saveUserPreferences();
  applyUserPreferences();
}

function savePreferences() {
  const apCb = document.getElementById('prefAutoplay');
  if (apCb) userPrefs.autoplay = apCb.checked;
  const contCb = document.getElementById('prefContinuous');
  if (contCb) userPrefs.continuous = contCb.checked;
  const dvCb = document.getElementById('prefDailyVirtue');
  if (dvCb) userPrefs.dailyVirtue = dvCb.checked;
  saveUserPreferences();
}

function resetUserSettings() {
  if (confirm('அனைத்து அமைப்புகளையும் இயல்பு நிலைக்கு மீட்டமைக்க வேண்டுமா?')) {
    userPrefs = { ...DEFAULT_USER_PREFS };
    saveUserPreferences();
    applyUserPreferences();
  }
}

// --------------------------------------------------------------------------
// PRIMARY 6-GROUP MENU DRAWER & SIDEBAR CONTROLS
// --------------------------------------------------------------------------
function togglePrimaryMenu() {
  const strip = document.getElementById('leftStripBar');
  const backdrop = document.getElementById('stripBackdrop');
  if (!strip) return;
  const isOpen = strip.classList.toggle('open');
  document.body.classList.toggle('primary-menu-open', isOpen);
  if (backdrop) backdrop.classList.toggle('active', isOpen);
}

function openPrimaryMenu() {
  const strip = document.getElementById('leftStripBar');
  const backdrop = document.getElementById('stripBackdrop');
  if (!strip) return;
  strip.classList.add('open');
  document.body.classList.add('primary-menu-open');
  if (backdrop) backdrop.classList.add('active');
}

function closePrimaryMenu() {
  const strip = document.getElementById('leftStripBar');
  const backdrop = document.getElementById('stripBackdrop');
  if (strip) {
    strip.classList.remove('open');
    strip.classList.remove('mobile-open');
  }
  document.body.classList.remove('primary-menu-open');
  if (backdrop) backdrop.classList.remove('active');
}

function toggleLeftStrip() {
  togglePrimaryMenu();
}

function closeMobileStrip() {
  closePrimaryMenu();
}

function openUserSettingsModal(tab) {
  let modal = document.getElementById('userSettingsModal');
  if (!modal) {
    mountAppShell();
    modal = document.getElementById('userSettingsModal');
  }
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    switchUserTab(tab || 'profile');
  }
}

function closeUserSettingsModal() {
  const modal = document.getElementById('userSettingsModal');
  if (modal) {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

function switchUserTab(tabId) {
  const tabProfileBtn = document.getElementById('userTabProfileBtn');
  const tabPrefsBtn = document.getElementById('userTabPrefsBtn');
  const contentProfile = document.getElementById('tabContentProfile');
  const contentPrefs = document.getElementById('tabContentPreferences');

  if (tabId === 'preferences') {
    if (tabProfileBtn) tabProfileBtn.classList.remove('active');
    if (tabPrefsBtn) tabPrefsBtn.classList.add('active');
    if (contentProfile) contentProfile.classList.remove('active');
    if (contentPrefs) contentPrefs.classList.add('active');
  } else {
    if (tabProfileBtn) tabProfileBtn.classList.add('active');
    if (tabPrefsBtn) tabPrefsBtn.classList.remove('active');
    if (contentProfile) contentProfile.classList.add('active');
    if (contentPrefs) contentPrefs.classList.remove('active');
  }
}

// --------------------------------------------------------------------------
// CONTEXT-SENSITIVE SEARCH DISPATCHER
// --------------------------------------------------------------------------
function handleContextSearch(val) {
  const clearBtn = document.getElementById('contextSearchClear');
  if (clearBtn) clearBtn.style.display = val ? 'inline-block' : 'none';

  // 1. If catalog search function exists on this page
  if (typeof onSearchInput === 'function') {
    onSearchInput(val);
  }

  // 2. Also filter in-page text or cards
  const query = val.toLowerCase().trim();
  const searchTargets = document.querySelectorAll('.video-card, .virtue-card, .lesson-unit-panel, .canonical-card, .quiz-card');
  if (searchTargets.length > 0 && typeof onSearchInput !== 'function') {
    searchTargets.forEach(el => {
      const text = el.innerText.toLowerCase();
      el.style.display = (!query || text.includes(query)) ? '' : 'none';
    });
  }
}

function clearContextSearch() {
  const input = document.getElementById('contextQuickSearch');
  if (input) {
    input.value = '';
    handleContextSearch('');
    input.focus();
  }
}

// Keyboard shortcuts: '/' or 'Ctrl+K' to open universal search, 'Esc' to close modals
document.addEventListener('keydown', e => {
  if ((e.key === '/' || ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k')) && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
    e.preventDefault();
    openUniversalSearch();
  }
  if (e.key === 'Escape') {
    closeUniversalSearch();
    closeUserSettingsModal();
    closeMobileStrip();
  }
});

// --------------------------------------------------------------------------
// 1. AMBIENT MEDITATIVE TANPURA DRONE (Web Audio API)
// --------------------------------------------------------------------------
let droneAudioCtx = null;
let droneOscillators = [];
let droneGainNode = null;
let isDronePlaying = false;

function toggleAmbientDrone() {
  if (isDronePlaying) {
    stopAmbientDrone();
  } else {
    startAmbientDrone();
  }
}

function startAmbientDrone() {
  try {
    const AudioCtxClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtxClass) return;
    if (!droneAudioCtx) {
      droneAudioCtx = new AudioCtxClass();
    }
    if (droneAudioCtx.state === 'suspended') {
      droneAudioCtx.resume();
    }

    droneGainNode = droneAudioCtx.createGain();
    droneGainNode.gain.setValueAtTime(0.001, droneAudioCtx.currentTime);
    droneGainNode.gain.exponentialRampToValueAtTime(0.12, droneAudioCtx.currentTime + 2.5);
    droneGainNode.connect(droneAudioCtx.destination);

    // C# Tanpura Harmonic Frequencies:
    // Kharaj Sa (C#3 - 138.59 Hz), Pa (G#3 - 207.65 Hz), Sa (C#4 - 277.18 Hz), Sa (C#4 - 277.65 Hz)
    const freqs = [138.59, 207.65, 277.18, 277.65];
    droneOscillators = freqs.map((freq, i) => {
      const osc = droneAudioCtx.createOscillator();
      const oscGain = droneAudioCtx.createGain();
      osc.type = (i === 0) ? 'triangle' : 'sine';
      osc.frequency.setValueAtTime(freq, droneAudioCtx.currentTime);

      const lfo = droneAudioCtx.createOscillator();
      lfo.frequency.setValueAtTime(0.12 + (i * 0.04), droneAudioCtx.currentTime);
      const lfoGain = droneAudioCtx.createGain();
      lfoGain.gain.setValueAtTime(0.4, droneAudioCtx.currentTime);
      lfo.connect(lfoGain);
      lfoGain.connect(osc.frequency);
      lfo.start();

      oscGain.gain.setValueAtTime(i === 0 ? 0.35 : 0.22, droneAudioCtx.currentTime);
      osc.connect(oscGain);
      oscGain.connect(droneGainNode);
      osc.start();
      return { osc, lfo };
    });

    isDronePlaying = true;
    updateDroneUI(true);
  } catch (err) {
    console.error('Ambient drone initialization error:', err);
  }
}

function stopAmbientDrone() {
  if (droneGainNode && droneAudioCtx) {
    try {
      droneGainNode.gain.exponentialRampToValueAtTime(0.0001, droneAudioCtx.currentTime + 1.2);
    } catch(e){}
    setTimeout(() => {
      droneOscillators.forEach(o => {
        try { o.osc.stop(); o.lfo.stop(); } catch(e){}
      });
      droneOscillators = [];
      isDronePlaying = false;
      updateDroneUI(false);
    }, 1200);
  } else {
    isDronePlaying = false;
    updateDroneUI(false);
  }
}

function updateDroneUI(playing) {
  const btns = document.querySelectorAll('.ambient-drone-btn');
  btns.forEach(btn => {
    if (playing) {
      btn.classList.add('playing');
      btn.title = 'நாத தியான ஒலி இயங்குகிறது (நிறுத்த கிளிக் செய்க)';
    } else {
      btn.classList.remove('playing');
      btn.title = 'நாத தியான ஒலி (Ambient Tanpura Drone)';
    }
  });
}

// --------------------------------------------------------------------------
// 2. UNIVERSAL SITE-WIDE SEARCH MODAL ENGINE
// --------------------------------------------------------------------------
const UNIVERSAL_SEARCH_ITEMS = [
  // Flagship Living Dharma Tools
  { title: "பஞ்ச மகா யக்ஞ டிராக்கர் (Daily Pancha Maha Yagna Habit Tracker)", desc: "தினசரி 5 வேள்விகள், சினமின்மை, இல்லற நல்லிணக்கம் & தொடர் சாதனா டிராக்கர்", url: "kalvi.html#grihasthaTracker", category: "இல்லற சாதனா", badge: "தினசரி சாதனா" },
  { title: "மாண்புறு குடும்ப அறநெறி சாசனம் (Printable Noble Family Living Charter)", desc: "இல்லத்தின் பெயர், உறுப்பினர்கள் & ஐம்பெரும் குடும்பச் சூளுரைகளுடன் சட்டமிடக்கூடிய சாசனம்", url: "kalvi.html#familyCharter", category: "இல்லற சாதனா", badge: "அச்சிடுக / PDF" },
  { title: "பதஞ்சலி 7 படிநிலைகள் (Patanjali 7-Level Self-Realization Curriculum)", desc: "சுபேச்சை முதல் துரியகா வரை 7 யோக மெய்ஞ்ஞான படிநிலைகள் & சுயமதிப்பீட்டுத் தேர்வு", url: "syllabus.html#patanjaliSyllabus", category: "பாடத்திட்டம்", badge: "7 படிநிலைகள்" },
  { title: "திருக்குறள் இல்லறவியல் 20 அதிகாரங்கள் அரங்கம் (Illaraviyal Cinema Lounge)", desc: "இல்வாழ்க்கை, துணைநலம், அன்புடைமை, பொறையுடைமை முதல் புகழ் வரை 20 தூண்கள்", url: "thirukkural.html#illaraviyalLounge", category: "திருக்குறள்", badge: "20 அதிகாரங்கள்" },
  { title: "இணையப் பள்ளி போர்டல் (Vedic-Modern Online School LMS)", desc: "21-ஆம் நூற்றாண்டு அறிவியல்-வேத சங்கமம், மாணவர் போர்டல் & படிப்பு அரங்கம்", url: "school.html", category: "பள்ளி", badge: "Online School" },
  
  // Degrees
  { title: "B.A. Grihastha Dharma (DEG-BA-GRI)", desc: "இல்லற தர்ம இளங்கலை — அறம், இல்லற மேலாண்மை & சான்றாண்மை விழுமியங்கள்", url: "higher-studies.html", category: "உயர்கல்வி", badge: "B.A. பட்டம்" },
  { title: "M.A. Applied Domestic Vedanta (DEG-MA-GRI)", desc: "பயன்முறை இல்லற வேதாந்த முதுகலை — சங்கர அத்வைதம், ராமானுஜ விசிஷ்டாத்வைதம் & இல்லற சமரசம்", url: "higher-studies.html", category: "உயர்கல்வி", badge: "M.A. பட்டம்" },
  { title: "Ph.D. in Family Self-Sacrifice as Fastest Vehicle for Nirvana (DOC-PHD-GRI)", desc: "இல்லறத் தியாக அன்பே அதிவேக முக்தி தரும் பெருவழி — முனைவர் பட்ட ஆய்வுநெறி", url: "higher-studies.html", category: "உயர்கல்வி", badge: "Ph.D. ஆய்வு" },
  { title: "Fellowship in Applied Domestic Dharma (FEL-GRI-01)", desc: "சான்றோன் இல்லற ஆய்வு கூட்டுறவு — தலைமுறை தலைமுறையாக தர்மத்தை நிலைநிறுத்தும் சாசனம்", url: "higher-studies.html", category: "உயர்கல்வி", badge: "Fellowship" },

  // Grades 1-12
  { title: "தரம் 1 — பாலப் பருவ வாழ்வியல் நெறி (Grade 1)", desc: "பாலப் பருவ அன்பு, பெற்றோர் பணிவிடை & நற்பண்புத் தொடக்கம்", url: "tharam-1.html", category: "பள்ளிக் கல்வி", badge: "Grade 1" },
  { title: "தரம் 2 — சிவ சின்னங்கள் & ஆலய வழிபாடு (Grade 2)", desc: "திருநீறு, ருத்ராட்சம், பஞ்சாட்சரம் & ஒழுக்கம்", url: "tharam-2.html", category: "பள்ளிக் கல்வி", badge: "Grade 2" },
  { title: "தரம் 3 — பஞ்சபூதம் & விழிப்புணர்வு (Grade 3)", desc: "நல்வழி, இயற்கை ஆராதனை & ஆசாரக் கல்வி", url: "tharam-3.html", category: "பள்ளிக் கல்வி", badge: "Grade 3" },
  { title: "தரம் 4 — பன்னிரு திருமுறை & சாத்வீக உணவு (Grade 4)", desc: "கொன்றை வேந்தன், திருமுறை பக்தி & அஹிம்சை", url: "tharam-4.html", category: "பள்ளிக் கல்வி", badge: "Grade 4" },
  { title: "தரம் 5 — 63 நாயன்மார்கள் & அறத்துப்பால் (Grade 5)", desc: "திருத்தொண்டர் தொகை, சுற்றந்தழால் & தேவாரம்", url: "tharam-5.html", category: "பள்ளிக் கல்வி", badge: "Grade 5" },
  { title: "தரம் 6 — நான்கு வேதங்கள் & சைவ சித்தாந்தம் (Grade 6)", desc: "தைத்திரீய சாந்தி மந்திரம், பதி-பசு-பாசம் & பஞ்ச மகா யக்ஞம்", url: "tharam-6.html", category: "பள்ளிக் கல்வி", badge: "Grade 6" },
  { title: "தரம் 7 — உபநிடத மகா வாக்கியங்கள் & கர்ம விதி (Grade 7)", desc: "பிரக்ஞானம் பிரம்ம, தத்வமஸி & புனர்ஜென்ம கர்ம நியதி", url: "tharam-7.html", category: "பள்ளிக் கல்வி", badge: "Grade 7" },
  { title: "தரம் 8 — பகவத் கீதை கர்ம யோகம் & வள்ளலார் (Grade 8)", desc: "கடமையைச் செய் பலனை எதிர்பாராதே & ஜீவகாருண்யம்", url: "tharam-8.html", category: "பள்ளிக் கல்வி", badge: "Grade 8" },
  { title: "தரம் 9 — ஆகமங்கள், ஆலய தத்துவம் & யோகம் (Grade 9)", desc: "உடலே ஆலயம், குண்டலினி சக்கரங்கள் & தியான அறிவியல்", url: "tharam-9.html", category: "பள்ளிக் கல்வி", badge: "Grade 9" },
  { title: "தரம் 10 — பதி பசு பாசம் & O/L வாழ்வியல் தேர்ச்சி (Grade 10)", desc: "சைவ சித்தாந்த முப்பொருள் உண்மை & முக்தி தத்துவம்", url: "tharam-10.html", category: "பள்ளிக் கல்வி", badge: "Grade 10" },
  { title: "தரம் 11 — கடோபநிடதம் & A/L தத்துவார்த்த ஒப்பாய்வு (Grade 11)", desc: "மரணத்தை வென்ற நசிகேதன் & பஞ்ச கோச உளவியல்", url: "tharam-11.html", category: "பள்ளிக் கல்வி", badge: "Grade 11" },
  { title: "தரம் 12 — ஜீவன் முக்தி, நடராஜர் & குவாண்டம் சங்கமம் (Grade 12)", desc: "உன்னத இல்லற வாழ்வு வழி அதிவேக முக்திப் பேறு", url: "tharam-12.html", category: "பள்ளிக் கல்வி", badge: "Grade 12" },

  // Canonical Paths
  { title: "சிவ நெறி — பன்னிரு திருமுறைகள் (Saiva Neri)", desc: "172 சிவத் திருப்பதிகங்கள், தேவாரப் பண்கள் & ஸ்ரீ ருத்ரம்", url: "saiva-neri.html", category: "ஆன்மீக நெறி", badge: "172 பாடல்கள்" },
  { title: "திருக்குறள் — உலகப் பொதுமறை அறநெறி (Thirukkural)", desc: "1330 அருங்குறள்கள், சினிமாத் திரைப்படங்கள் & இசை வெளியீடுகள்", url: "thirukkural.html", category: "ஆன்மீக நெறி", badge: "185 வெளியீடுகள்" },
  { title: "சுத்த சன்மார்க்கம் — வள்ளலார் பெருமான் (Sanmargam)", desc: "திருவருட்பா, ஜோதி வழிபாடு & பசிப்பிணி போக்கும் அன்னதானம்", url: "sanmargam.html", category: "ஆன்மீக நெறி", badge: "94 பாடல்கள்" },
  { title: "முருக நெறி — கௌமாரம் (Murugan)", desc: "கந்த சஷ்டி கவசம், திருப்புகழ் & அறுபடை வீடு திருவருள்", url: "murugan.html", category: "ஆன்மீக நெறி", badge: "முருகன்" },
  { title: "சக்தி நெறி — சாக்தம் (Sakthi)", desc: "அபிராமி அந்தாதி, லலிதா திரிசதி & தேவி போற்றிகள்", url: "sakthi.html", category: "ஆன்மீக நெறி", badge: "அம்பாள்" },
  { title: "விநாயகர் & வைணவ நெறி (Vinayagar & Vaishnavam)", desc: "விநாயகர் அகவல், திவ்யப் பிரபந்தம் & விஷ்ணு-கிருஷ்ண கானங்கள்", url: "vinayagar.html", category: "ஆன்மீக நெறி", badge: "விநாயகர்/வைணவம்" },
  { title: "காஞ்சி மகா பெரியவா அருளுரைகள் (Deivathin Kural)", desc: "வேத தர்மம், சனாதன சம்ஸ்கிருதி & மகா பெரியவா திவ்ய உபதேசங்கள்", url: "about.html", category: "குருவருள்", badge: "தெய்வத்தின் குரல்" }
];

function ensureUniversalSearchModal() {
  let modal = document.getElementById('universalSearchModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'universalSearchModal';
    modal.className = 'universal-search-modal';
    modal.onclick = function(e) { if (e.target === this) closeUniversalSearch(); };
    modal.innerHTML = `
      <div class="universal-search-box">
        <div class="universal-search-header">
          <span style="font-size:1.15rem; color:#38bdf8;">🔍</span>
          <input type="text" id="universalSearchInput" class="universal-search-input" placeholder="குருகுல தேசத்தில் தேடுக... (எ.கா: தரம் 1, இல்லறம், குறள், PhD, யக்ஞம்)" autocomplete="off" oninput="handleUniversalSearchQuery(this.value)">
          <button type="button" class="universal-search-close" onclick="closeUniversalSearch()">Esc</button>
        </div>
        <div class="universal-search-results" id="universalSearchResults"></div>
      </div>
    `;
    document.body.appendChild(modal);
  }
  return modal;
}

function openUniversalSearch() {
  const modal = ensureUniversalSearchModal();
  modal.classList.add('open');
  const input = document.getElementById('universalSearchInput');
  if (input) {
    input.value = '';
    input.focus();
  }
  handleUniversalSearchQuery('');
}

function closeUniversalSearch() {
  const modal = document.getElementById('universalSearchModal');
  if (modal) modal.classList.remove('open');
}

function handleUniversalSearchQuery(q) {
  const container = document.getElementById('universalSearchResults');
  if (!container) return;

  const query = q.toLowerCase().trim();
  let results = [];

  if (!query) {
    results = UNIVERSAL_SEARCH_ITEMS.slice(0, 8);
  } else {
    results = UNIVERSAL_SEARCH_ITEMS.filter(item => {
      const haystack = (item.title + ' ' + item.desc + ' ' + item.category + ' ' + (item.badge || '')).toLowerCase();
      return haystack.includes(query);
    });

    if (window.GURUKULA_CATALOG && query.length >= 2) {
      let catalogMatches = [];
      Object.keys(window.GURUKULA_CATALOG).forEach(cat => {
        const list = window.GURUKULA_CATALOG[cat];
        if (Array.isArray(list)) {
          list.forEach(item => {
            const h = (item.title + ' ' + (item.lyrics || '') + ' ' + (item.meaning || '')).toLowerCase();
            if (h.includes(query)) {
              catalogMatches.push({
                title: item.title,
                desc: (item.meaning || item.lyrics || '').slice(0, 90) + '...',
                url: (cat === 'thirukkural') ? 'thirukkural.html' : (cat === 'shiva' ? 'saiva-neri.html' : 'index.html'),
                category: cat === 'thirukkural' ? 'திருக்குறள்' : (cat === 'shiva' ? 'சிவ நெறி' : 'பக்தி இசை'),
                badge: item.type === 'film' ? '🎬 படம்' : '🎵 பாடல்'
              });
            }
          });
        }
      });
      results = results.concat(catalogMatches.slice(0, 10));
    }
  }

  if (results.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:30px 10px; color:#94a3b8;">
        <div style="font-size:2rem; margin-bottom:8px;">🌿</div>
        <div>"${q}" என்பதற்குரிய முடிவுகள் கிடைக்கவில்லை.</div>
        <div style="font-size:0.82rem; margin-top:4px; color:#64748b;">வேத தர்மம், குறள், தரம் 1-12, அல்லது இல்லறம் எனத் தேடிப் பாருங்கள்.</div>
      </div>
    `;
    return;
  }

  let html = '';
  if (!query) {
    html += '<div class="search-group-title">🌟 பரிந்துரைக்கப்படும் முதன்மை வாழ்வியல் &amp; தர்மப் பாதைகள்:</div>';
  } else {
    html += `<div class="search-group-title">🔍 கண்டறியப்பட்ட தேடல் முடிவுகள் (${results.length}):</div>`;
  }

  results.forEach(r => {
    html += `
      <a href="${r.url}" class="search-result-item" onclick="closeUniversalSearch()">
        <div class="search-item-info">
          <span class="search-item-title">${r.title}</span>
          <span class="search-item-desc">${r.desc}</span>
        </div>
        <span class="search-item-badge">${r.badge || r.category}</span>
      </a>
    `;
  });

  container.innerHTML = html;
}

// --------------------------------------------------------------------------
// APP SHELL DOM MOUNTING & CONTEXT RESOLUTION
// --------------------------------------------------------------------------
function resolvePageContext() {
  const path = window.location.pathname.toLowerCase();
  const filename = path.split('/').pop() || 'index.html';

  const contextMap = {
    'index.html': { root: 'முகப்பு', title: 'ஆன்மீகப் பெருவெளி', desc: '580 பக்தி இசை வெளியீடுகள்' },
    'kalvi.html': { root: 'வாழ்வியல்', title: 'வாழ்வியல் நெறி & இல்லற தர்மம்', desc: 'தரம் 1 முதல் 12 வரையிலான உன்னத இல்லற தர்மம் & சான்றாண்மை' },
    'virtues.html': { root: 'வாழ்வியல்', title: 'அகர வரிசை நற்பண்பு நெறிமுறை', desc: '30+ நற்பண்புகள் • 4 வாழ்வியல் பருவங்கள்' },
    'tharam-1.html': { root: 'வாழ்வியல்', title: 'தரம் 1 (Grade 1)', desc: 'பாலப் பருவ அன்பு & இல்லறத் தொடக்கப் பழக்கங்கள்' },
    'tharam-2.html': { root: 'வாழ்வியல்', title: 'தரம் 2 (Grade 2)', desc: 'சிவ சின்னங்கள், பக்தி & இல்லற தர்மம்' },
    'tharam-3.html': { root: 'வாழ்வியல்', title: 'தரம் 3 (Grade 3)', desc: 'நல்வழி, ஒழுக்கம் & ஆசாரக் கல்வி' },
    'tharam-4.html': { root: 'வாழ்வியல்', title: 'தரம் 4 (Grade 4)', desc: 'கொன்றை வேந்தன் & இல்லற நன்னெறி' },
    'tharam-5.html': { root: 'வாழ்வியல்', title: 'தரம் 5 (Grade 5)', desc: 'திருமுறைகள் & சுற்றந்தழால் தர்மம்' },
    'tharam-6.html': { root: 'வாழ்வியல்', title: 'தரம் 6 (Grade 6)', desc: 'சைவ சித்தாந்த ஆரம்ப நெறி & கடமை உணர்வு' },
    'tharam-7.html': { root: 'வாழ்வியல்', title: 'தரம் 7 (Grade 7)', desc: 'திருமுறைகள் & நாயன்மார் தியாக வரலாறு' },
    'tharam-8.html': { root: 'வாழ்வியல்', title: 'தரம் 8 (Grade 8)', desc: 'பொறையுடைமை, ஆசிரம தர்மம் & ஆலய தத்துவம்' },
    'tharam-9.html': { root: 'வாழ்வியல்', title: 'தரம் 9 (Grade 9)', desc: 'சான்றாண்மை, புலனடக்கம் & குடும்ப மாண்பு' },
    'tharam-10.html': { root: 'வாழ்வியல்', title: 'தரம் 10 (Grade 10)', desc: 'O/L வாழ்வியல் நன்னெறி & இல்லற மாண்பு' },
    'tharam-11.html': { root: 'வாழ்வியல்', title: 'தரம் 11 (Grade 11)', desc: 'A/L உயர்தர தத்துவ ஆய்வு & சால்பு' },
    'tharam-12.html': { root: 'வாழ்வியல்', title: 'தரம் 12 (Grade 12)', desc: 'உன்னத இல்லற தர்மம் வழி ஆத்ம நிர்வாணம் / முக்தி' },
    'saiva-neri.html': { root: 'சைவ நெறி', title: 'பன்னிரு திருமுறைகள்', desc: '172 சிவத் திருப்பதிகங்கள் & ருத்ரம்' },
    'murugan.html': { root: 'வழிபாட்டு நெறி', title: 'முருகன் (Kaumaram)', desc: 'கந்த சஷ்டி, திருப்புகழ் & கானங்கள்' },
    'sakthi.html': { root: 'வழிபாட்டு நெறி', title: 'சக்தி (Shaktham)', desc: 'அபிராமி அந்தாதி & லலிதா போற்றிகள்' },
    'vinayagar.html': { root: 'வழிபாட்டு நெறி', title: 'விநாயகர் (Ganapathyam)', desc: 'விநாயகர் அகவல் & மூல கணபதி' },
    'vaishnava.html': { root: 'வழிபாட்டு நெறி', title: 'வைணவம் (Vaishnavam)', desc: 'விஷ்ணு, கிருஷ்ணர் & திவ்வியப் பிரபந்தம்' },
    'thirukkural.html': { root: 'தமிழ்மறை', title: 'திருக்குறள் (Thirukkural)', desc: '1330 அருங்குறள்கள் & இசைப்பாடல்கள்' },
    'sanmargam.html': { root: 'சன்மார்க்கம்', title: 'வள்ளலார் சுத்த சன்மார்க்கம்', desc: 'திருவருட்பா & ஆன்மநேய ஒருமைப்பாடு' },
    'irai-isai-virundhu.html': { root: 'இசை', title: 'இறை இசை விருந்து', desc: 'ஆன்மீக பக்தி ஆல்பங்கள்' },
    'syllabus.html': { root: 'வாழ்வியல்', title: 'முழுமையான பாடத்திட்டம்', desc: 'வேத & சைவ வாழ்வியல் நெறி அமைப்பு' },
    'classes.html': { root: 'வகுப்புகள்', title: 'பாடநெறி அட்டவணை', desc: 'குருகுல கல்வி வகுப்புகள்' },
    'about.html': { root: 'காஞ்சி மகா பெரியவா', title: 'தெய்வத்தின் குரல் & தரிசனம்', desc: 'அருளுரைகள் & வழிகாட்டல்' }
  };

  return contextMap[filename] || { root: 'குரு குல தேசம்', title: 'ஆன்மீகக் களஞ்சியம்', desc: '' };
}


/* ========================================================================== */
/* GURUKULA CONTEXT-SENSITIVE TOP MENU TABS & APP SHELL                       */
/* ========================================================================== */

function getContextTabsForPage() {
  const path = window.location.pathname.toLowerCase();
  const filename = path.split('/').pop() || 'index.html';

  // 1. Grade / Tharam Pages (tharam-1.html to tharam-12.html)
  const gradeMatch = filename.match(/^tharam-(\d+)\.html$/);
  if (gradeMatch) {
    const gradeNum = parseInt(gradeMatch[1], 10);
    const prevGrade = gradeNum > 1 ? `tharam-${gradeNum - 1}.html` : null;
    const nextGrade = gradeNum < 12 ? `tharam-${gradeNum + 1}.html` : null;

    return [
      { id: 'tab-units', icon: '📖', label: 'பாட அலகுகள்', action: "scrollToSection('courseUnits', 'lessonUnitPanel1')" },
      { id: 'tab-virtues', icon: '🔤', label: 'நற்பண்பு நெறி', action: "scrollToSection('gradeVirtueBox')" },
      { id: 'tab-diagram', icon: '🎨', label: 'காட்சி விளக்கம்', action: "scrollToSection('visualDiagramCard')" },
      { id: 'tab-quiz', icon: '❓', label: 'சுய வினாடி-வினா', action: "scrollToSection('quizSection')" },
      { id: 'tab-sadhana', icon: '🪔', label: 'தினசரி சாதனை', action: "scrollToSection('sadhanaBox')" },
      ...(prevGrade ? [{ id: 'tab-prev', icon: '⏪', label: `தரம் ${gradeNum - 1}`, href: prevGrade }] : []),
      ...(nextGrade ? [{ id: 'tab-next', icon: '⏩', label: `தரம் ${gradeNum + 1}`, href: nextGrade }] : []),
      { id: 'tab-all-grades', icon: '🌿', label: '12 வாழ்வியல் நிலைகள்', href: 'kalvi.html' }
    ];
  }

  // 2. Curriculum Hub (kalvi.html)
  if (filename === 'kalvi.html') {
    return [
      { id: 'tab-overview', icon: '🌿', label: 'வாழ்வியல் நெறி அறிமுகம்', action: "scrollToSection('kalviOverview')", active: true },
      { id: 'tab-dharma', icon: '🏡', label: 'உன்னத இல்லற தர்மம்', action: "scrollToSection('dharmaPrinciples')" },
      { id: 'tab-tracker', icon: '✅', label: 'பஞ்ச மகா யக்ஞ டிராக்கர்', action: "scrollToSection('grihasthaTracker')" },
      { id: 'tab-charter', icon: '📜', label: 'குடும்ப சாசனம்', action: "scrollToSection('familyCharter')" },
      { id: 'tab-stages', icon: '🔤', label: '4 வாழ்வியல் பருவங்கள்', action: "scrollToSection('virtue-mapping')" },
      { id: 'tab-grades', icon: '📚', label: '12 வாழ்வியல் நிலைகள்', action: "scrollToSection('gradesPortalSection')" },
      { id: 'tab-school', icon: '🏫', label: 'இணையப் பள்ளி', href: 'school.html' },
      { id: 'tab-higher', icon: '🔬', label: 'உயர்கல்வி', href: 'higher-studies.html' },
      { id: 'tab-syllabus', icon: '📜', label: 'முழு பாடத்திட்டம்', href: 'syllabus.html' }
    ];
  }

  // 2b. Gurukula Academy Portal (school.html)
  if (filename === 'school.html') {
    return [
      { id: 'tab-portal', icon: '📊', label: 'மாணவர் போர்டல்', action: "scrollToSection('portalDashboard')", active: true },
      { id: 'tab-fusion', icon: '🔬', label: 'அறிவியல்-வேத சங்கமம்', action: "scrollToSection('stemFusionSection')" },
      { id: 'tab-hall', icon: '⏱️', label: 'தியான & படிப்பு அரங்கம்', action: "scrollToSection('focusStudyHall')" },
      { id: 'tab-cert', icon: '📜', label: 'பட்டயச் சான்றிதழ்', action: "scrollToSection('certificateSection')" },
      { id: 'tab-cards', icon: '🗂️', label: 'நினைவாற்றல் அட்டைகள்', action: "scrollToSection('flashcardsSection')" },
      { id: 'tab-roadmap', icon: '🧭', label: '12 தரப் பாடநெறி', action: "scrollToSection('roadmapSection')" },
      { id: 'tab-tracker', icon: '✅', label: 'தினசரி தர்ம டிராக்கர்', href: 'kalvi.html#grihasthaTracker' },
      { id: 'tab-charter', icon: '📜', label: 'குடும்ப சாசனம்', href: 'kalvi.html#familyCharter' }
    ];
  }

  // 3. Virtues Matrix (virtues.html)
  if (filename === 'virtues.html') {
    return [
      { id: 'tab-all', icon: '🌟', label: 'அனைத்து நற்பண்புகள் (30+)', action: "filterVirtues('all')", active: true },
      { id: 'tab-t1', icon: '🟢', label: 'பருவம் 1: அறிதல் (தரம் 1-4)', action: "filterVirtues('tier-1')" },
      { id: 'tab-t2', icon: '🟡', label: 'பருவம் 2: செய்தல் (தரம் 5-8)', action: "filterVirtues('tier-2')" },
      { id: 'tab-t3', icon: '🔴', label: 'பருவம் 3: காத்தல் (தரம் 9-12)', action: "filterVirtues('tier-3')" },
      { id: 'tab-kalvi', icon: '🌿', label: 'வாழ்வியல் மையம்', href: 'kalvi.html' }
    ];
  }

  // 4. Master Home (index.html - Guru Kula Ashram Sanctuary)
  if (filename === 'index.html' || filename === '') {
    return [
      { id: 'tab-home', icon: '🏛️', label: 'ஆசிரம முகப்பு', href: 'index.html', active: true },
      { id: 'tab-kalvi', icon: '🌿', label: 'தர்ம குடீரம் (12 நிலைகள்)', href: 'kalvi.html' },
      { id: 'tab-school', icon: '🏫', label: 'வித்யா குடீரம்', href: 'school.html' },
      { id: 'tab-pedagogy', icon: '📜', label: 'போதனை மரபு', action: "scrollToSection('ashramPedagogy')" },
      { id: 'tab-dinacharya', icon: '🪔', label: 'தினசரி காலச்சக்கரம்', action: "scrollToSection('ashramDinacharya')" },
      { id: 'tab-yagna', icon: '🔥', label: 'பஞ்ச மகா யக்ஞம்', action: "scrollToSection('ashramPanchaYagna')" },
      { id: 'tab-featured', icon: '🎬', label: 'கான அரங்கம்', action: "scrollToSection('featuredScreeningRoom')" },
      { id: 'tab-catalog', icon: '📺', label: '580 சுவடிக் களஞ்சியம்', href: 'youtube.html' },
      { id: 'tab-contact', icon: '📍', label: 'ஆசிரம முகவரி', action: "scrollToSection('siteFooter')" }
    ];
  }

  // 5. Saiva Neri (saiva-neri.html)
  if (filename === 'saiva-neri.html') {
    return [
      { id: 'tab-all-shiva', icon: '🔱', label: 'அனைத்து சிவப்பதிகங்கள்', action: "setTypeFilter('all')", active: true },
      { id: 'tab-thevaram', icon: '🌿', label: 'தேவாரம்', action: "filterByText('தேவாரம்')" },
      { id: 'tab-thiruvasagam', icon: '💎', label: 'திருவாசகம்', action: "filterByText('திருவாசகம்')" },
      { id: 'tab-thirumandhiram', icon: '🧘', label: 'திருமந்திரம்', action: "filterByText('திருமந்திரம்')" },
      { id: 'tab-rudram', icon: '🔥', label: 'ஸ்ரீ ருத்ரம்', action: "filterByText('ருத்ரம்')" }
    ];
  }

  // 6. Traditions / Deities
  if (['murugan.html', 'sakthi.html', 'vinayagar.html', 'vaishnava.html'].includes(filename)) {
    return [
      { id: 'tab-murugan', icon: '🔱', label: 'முருகன் (Kaumaram)', href: 'murugan.html', active: filename === 'murugan.html' },
      { id: 'tab-sakthi', icon: '🌸', label: 'சக்தி (Shaktham)', href: 'sakthi.html', active: filename === 'sakthi.html' },
      { id: 'tab-vinayagar', icon: '🐘', label: 'விநாயகர் (Ganapathyam)', href: 'vinayagar.html', active: filename === 'vinayagar.html' },
      { id: 'tab-vaishnava', icon: '🪷', label: 'வைணவம் (Vaishnavam)', href: 'vaishnava.html', active: filename === 'vaishnava.html' }
    ];
  }

  // 7. Thirukkural (thirukkural.html)
  if (filename === 'thirukkural.html') {
    return [
      { id: 'tab-all-tk', icon: '📖', label: 'அனைத்து குறள்கள்', action: "setTypeFilter('all')", active: true },
      { id: 'tab-aram', icon: '🌿', label: 'அறத்துப்பால்', action: "filterByText('அறத்துப்பால்')" },
      { id: 'tab-porul', icon: '👑', label: 'பொருட்பால்', action: "filterByText('பொருட்பால்')" },
      { id: 'tab-inbam', icon: '🌺', label: 'காமத்துப்பால்', action: "filterByText('காமத்துப்பால்')" },
      { id: 'tab-films-tk', icon: '🎬', label: 'குறள் திரைப்படங்கள்', action: "setTypeFilter('film')" }
    ];
  }

  // 8. Sanmargam (sanmargam.html)
  if (filename === 'sanmargam.html') {
    return [
      { id: 'tab-all-san', icon: '🪔', label: 'திருவருட்பா படைப்புகள்', action: "setTypeFilter('all')", active: true },
      { id: 'tab-jeeva', icon: '☀️', label: 'ஜீவகாருண்யம்', action: "filterByText('ஜீவகாருண்யம்')" },
      { id: 'tab-jyoti', icon: '🕯️', label: 'ஜோதி வழிபாடு', action: "filterByText('ஜோதி')" },
      { id: 'tab-audio-san', icon: '🎵', label: 'சன்மார்க்க இசை', action: "setTypeFilter('audio')" }
    ];
  }

  // 9. About / Periyava (about.html)
  if (filename === 'about.html') {
    return [
      { id: 'tab-periyava-darshan', icon: '🌟', label: 'மகா பெரியவா தரிசனம்', action: "scrollToSection('darshanSection')", active: true },
      { id: 'tab-deivathin-kural', icon: '📖', label: 'தெய்வத்தின் குரல்', action: "scrollToSection('teachingsSection')" },
      { id: 'tab-vedic-preservation', icon: '🕉️', label: 'வேத சம்ரக்ஷணம்', action: "scrollToSection('vedicSection')" },
      { id: 'tab-hq-address', icon: '📍', label: 'மைய முகவரி', action: "scrollToSection('siteFooter')" }
    ];
  }

  // 10. Syllabus / Classes
  if (filename === 'syllabus.html' || filename === 'classes.html') {
    return [
      { id: 'tab-full-syl', icon: '📚', label: 'முழு பாடத்திட்டம்', href: 'syllabus.html', active: filename === 'syllabus.html' },
      { id: 'tab-classes', icon: '🏛️', label: 'வகுப்புகள் அட்டவணை', href: 'classes.html', active: filename === 'classes.html' },
      { id: 'tab-virtues-map', icon: '🔤', label: 'நற்பண்பு நெறிமுறை', href: 'virtues.html' },
      { id: 'tab-grade-portal', icon: '🌿', label: '12 வாழ்வியல் நிலைகள்', href: 'kalvi.html' }
    ];
  }

  // Default fallback
  return [
    { id: 'tab-home', icon: '🏠', label: 'முகப்பு', href: 'index.html' },
    { id: 'tab-kalvi', icon: '🌿', label: 'வாழ்வியல் நெறி', href: 'kalvi.html' },
    { id: 'tab-virtues', icon: '🔤', label: 'நற்பண்புகள்', href: 'virtues.html' },
    { id: 'tab-saiva', icon: '🕉️', label: 'சைவ நெறி', href: 'saiva-neri.html' }
  ];
}

function scrollToSection(id, optionalTabId) {
  if (optionalTabId && typeof switchCourseTab === 'function') {
    switchCourseTab(optionalTabId);
  }
  let el = document.getElementById(id) || document.querySelector('.' + id);
  if (!el) {
    const fallbacks = {
      'courseUnits': ['#course-content-start', '#unit-panel-1', '.sheets-grid', '#sheets-section', '.course-layout', '#curriculumGrid'],
      'gradeVirtueBox': ['#syllabus-highlights', '.scripture-study-section', '#side-group-virtue', '.virtue-card', '#virtue-mapping', '.virtue-section'],
      'visualDiagramCard': ['.lesson-hero-visual-card', '.visual-card', '.infographic-card', '.lesson-video-microclip-card', '.poster-container'],
      'quizSection': ['.interactive-quiz', '.quiz-card', '.quiz-container', '.quiz-panel', '#quizSection'],
      'sadhanaBox': ['.sadhana-box', '#grihasthaTracker', '#familyCharter']
    };
    if (fallbacks[id]) {
      for (let i = 0; i < fallbacks[id].length; i++) {
        el = document.querySelector(fallbacks[id][i]);
        if (el) break;
      }
    }
  }
  if (el) {
    const yOffset = -75;
    const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset;
    window.scrollTo({ top: Math.max(0, y), behavior: 'smooth' });
  }
}

function filterByText(keyword) {
  const searchInput = document.getElementById('contextQuickSearch') || document.getElementById('searchInput');
  if (searchInput) {
    searchInput.value = keyword;
    handleContextSearch(keyword);
  }
}

function renderContextTabsIntoHeader() {
  const headerContainer = document.querySelector('.header-container');
  if (!headerContainer) return;

  // 1. Remove or hide the old duplicate main-nav
  const oldNav = document.getElementById('mainNav');
  if (oldNav) {
    oldNav.style.display = 'none';
  }

  // 2. Remove any previous context-tabs-nav or right tools
  const existingTabs = document.getElementById('contextTabsNav');
  if (existingTabs && existingTabs.parentNode) existingTabs.parentNode.removeChild(existingTabs);
  const existingTools = document.querySelector('.header-right-tools');
  if (existingTools && existingTools.parentNode) existingTools.parentNode.removeChild(existingTools);

  // 3. Build Context-Sensitive Menu Tabs with Primary Hamburger Trigger
  const tabs = getContextTabsForPage();
  const tabsNav = document.createElement('nav');
  tabsNav.id = 'contextTabsNav';
  tabsNav.className = 'context-tabs-nav';
  tabsNav.setAttribute('aria-label', 'Context Specific Tabs');

  const hamburgerBtnHtml = `
    <button type="button" class="primary-hamburger-btn" onclick="togglePrimaryMenu()" title="முதன்மை பட்டி (6 பிரிவுகள்)" aria-label="முதன்மை பட்டி">
      <span class="hb-icon">☰</span>
      <span class="hb-emblem">ॐ</span>
      <span class="hb-label">முதன்மை பட்டி</span>
    </button>
  `;

  tabsNav.innerHTML = hamburgerBtnHtml + tabs.map((t, idx) => {
    if (t.href) {
      return `
        <a href="${t.href}" class="context-tab-pill ${t.active ? 'active' : ''}" id="${t.id}">
          <span class="context-tab-pill-icon">${t.icon}</span>
          <span>${t.label}</span>
        </a>
      `;
    } else {
      return `
        <button type="button" class="context-tab-pill ${t.active || idx === 0 ? 'active' : ''}" id="${t.id}" onclick="handleTabClick(this, '${t.action}')">
          <span class="context-tab-pill-icon">${t.icon}</span>
          <span>${t.label}</span>
        </button>
      `;
    }
  }).join('');

  // 4. Build Right Tools Dock
  const rightTools = document.createElement('div');
  rightTools.className = 'header-right-tools';
  rightTools.innerHTML = `
    <div class="context-search-wrapper">
      <span class="context-search-icon">🔍</span>
      <input type="text" id="contextQuickSearch" class="context-search-input" placeholder="தேடுக... [/]" oninput="handleContextSearch(this.value)" autocomplete="off">
      <button type="button" class="context-search-clear" id="contextSearchClear" onclick="clearContextSearch()" style="display: none;">✕</button>
    </div>

    <div class="context-tool-group">
      <button type="button" class="context-tool-btn font-dec-btn" onclick="adjustFontSize(-0.06)" title="எழுத்தளவைக் குறைக்க (A-)">A⁻</button>
      <span class="font-scale-indicator" id="fontScaleIndicator" title="தற்போதைய எழுத்தளவு">100%</span>
      <button type="button" class="context-tool-btn font-inc-btn" onclick="adjustFontSize(0.06)" title="எழுத்தளவை அதிகரிக்க (A+)">A⁺</button>
    </div>

    <button type="button" class="context-tool-btn ambient-drone-btn" id="ambientDroneBtn" onclick="toggleAmbientDrone()" title="நாத தியான ஒலி (Ambient Tanpura Drone)"><span class="drone-icon" id="ambientDroneIcon">🪔</span></button>
        <button type="button" class="context-tool-btn theme-quick-btn" onclick="cycleTheme()" title="வண்ணக் கருப்பொருள் மாற்று">
      <span class="theme-icon" id="themeQuickIcon">🌓</span>
    </button>

    <button type="button" class="context-profile-pill" onclick="openUserSettingsModal('profile')" title="பயனர் சுயவிவரம் &amp; அமைப்புகள்">
      <span class="pill-avatar" id="pillAvatarIcon">👤</span>
      <span class="pill-name" id="pillUserName">சாதகர்</span>
    </button>
  `;

  headerContainer.appendChild(tabsNav);
  headerContainer.appendChild(rightTools);
}

function handleTabClick(btn, actionStr) {
  // Update active pill state
  const parent = btn.closest('.context-tabs-nav');
  if (parent) {
    parent.querySelectorAll('.context-tab-pill').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }
  // Execute action
  try {
    const fn = new Function(actionStr);
    fn();
  } catch (e) {
    console.error('Error executing tab action:', e);
  }
}


function mountAppShell() {
  if (document.getElementById('leftStripBar')) return;

  const currentPath = (window.location.pathname.split('/').pop() || 'index.html').toLowerCase();
  const ctx = resolvePageContext();

  renderContextTabsIntoHeader();

  // 1. Mobile Backdrop
  const backdrop = document.createElement('div');
  backdrop.id = 'stripBackdrop';
  backdrop.className = 'strip-backdrop';
  backdrop.onclick = closeMobileStrip;
  document.body.appendChild(backdrop);

  // 2. Left Strip Bar
  const strip = document.createElement('aside');
  strip.id = 'leftStripBar';
  strip.className = 'left-strip-bar';
  strip.setAttribute('aria-label', 'Quick Portals');

  const navItems = [
    { href: 'index.html', icon: '🏠', label: 'முகப்பு' },
    { href: 'kalvi.html', icon: '🌿', label: 'வாழ்வியல் நெறி' },
    { href: 'virtues.html', icon: '🔤', label: 'நற்பண்புகள்' },
    { href: 'saiva-neri.html', icon: '🕉️', label: 'சைவ நெறி' },
    { href: 'irai-isai-virundhu.html', icon: '🎵', label: 'இறை இசை' },
    { href: 'thirukkural.html', icon: '📖', label: 'திருக்குறள்' },
    { href: 'sanmargam.html', icon: '🪔', label: 'சன்மார்க்கம்' },
    { href: 'murugan.html', icon: '🔱', label: 'முருகன்' },
    { href: 'sakthi.html', icon: '🌸', label: 'சக்தி நெறி' },
    { href: 'vinayagar.html', icon: '🐘', label: 'விநாயகர்' },
    { href: 'vaishnava.html', icon: '🪷', label: 'வைணவம்' },
    { href: 'syllabus.html', icon: '📚', label: 'பாடத்திட்டம்' },
    { href: 'about.html', icon: '🏛️', label: 'பெரியவா' }
  ];

  strip.innerHTML = `
    <div class="strip-header">
      <a href="index.html" class="strip-brand-link" title="குரு குல தேசம்">
        <span class="strip-emblem">ॐ</span>
        <span class="strip-brand-text">குரு குல தேசம்</span>
      </a>
      <button type="button" class="strip-toggle-btn" id="stripToggleBtn" onclick="toggleLeftStrip()" title="விரிவுபடுத்து / சுருக்கு">
        <span class="strip-toggle-icon">⇤</span>
      </button>
    </div>

    <nav class="strip-nav-list" id="stripNavList">
      ${navItems.map(item => `
        <a href="${item.href}" class="strip-item ${currentPath === item.href ? 'active' : ''}" data-tooltip="${item.label}">
          <span class="strip-item-icon">${item.icon}</span>
          <span class="strip-item-label">${item.label}</span>
        </a>
      `).join('')}
    </nav>

    <div class="strip-footer-dock">
      <button type="button" class="strip-dock-btn" onclick="openUserSettingsModal('preferences')" title="அமைப்புகள்">
        <span class="strip-item-icon">⚙️</span>
        <span class="strip-dock-label">அமைப்புகள்</span>
      </button>
      <button type="button" class="strip-dock-btn profile-dock-btn" onclick="openUserSettingsModal('profile')" title="சுயவிவரம்">
        <span class="strip-dock-avatar" id="stripAvatarIcon">👤</span>
        <span class="strip-dock-label" id="stripUserName">சுயவிவரம்</span>
      </button>
    </div>
  `;

  document.body.prepend(strip);

  // Restore strip expanded state on desktop
  if (window.innerWidth >= 992 && localStorage.getItem('GURUKULA_STRIP_EXPANDED') === 'true') {
    strip.classList.add('expanded');
    document.body.classList.add('strip-expanded');
    const toggleIcon = strip.querySelector('.strip-toggle-icon');
    if (toggleIcon) toggleIcon.innerText = '⇥';
  }

  // 3. Context Sensitive Top Bar
  const contextBar = document.createElement('div');
  contextBar.id = 'contextSensitiveBar';
  contextBar.className = 'context-sensitive-bar';
  contextBar.innerHTML = `
    <div class="context-bar-inner">
      <div class="context-left">
        <button type="button" class="context-strip-trigger" onclick="toggleLeftStrip()" title="பக்கப்பட்டி திறக்க/மூட">
          ☰
        </button>
        <div class="context-breadcrumbs" id="contextBreadcrumbs">
          <span class="crumb-root">${ctx.root}</span>
          <span class="crumb-separator">/</span>
          <span class="crumb-current" id="contextCurrentTitle">${ctx.title}</span>
        </div>
      </div>

      <div class="context-right">
        <div class="context-search-wrapper">
          <span class="context-search-icon">🔍</span>
          <input type="text" id="contextQuickSearch" class="context-search-input" placeholder="தேடுக... [/]" oninput="handleContextSearch(this.value)" autocomplete="off">
          <button type="button" class="context-search-clear" id="contextSearchClear" onclick="clearContextSearch()" style="display: none;">✕</button>
        </div>

        <div class="context-tool-group">
          <button type="button" class="context-tool-btn font-dec-btn" onclick="adjustFontSize(-0.06)" title="எழுத்தளவைக் குறைக்க (A-)">A⁻</button>
          <span class="font-scale-indicator" id="fontScaleIndicator" title="தற்போதைய எழுத்தளவு">100%</span>
          <button type="button" class="context-tool-btn font-inc-btn" onclick="adjustFontSize(0.06)" title="எழுத்தளவை அதிகரிக்க (A+)">A⁺</button>
        </div>

        <button type="button" class="context-tool-btn ambient-drone-btn" id="ambientDroneBtn" onclick="toggleAmbientDrone()" title="நாத தியான ஒலி (Ambient Tanpura Drone)"><span class="drone-icon" id="ambientDroneIcon">🪔</span></button>
        <button type="button" class="context-tool-btn theme-quick-btn" onclick="cycleTheme()" title="வண்ணக் கருப்பொருள் மாற்று">
          <span class="theme-icon" id="themeQuickIcon">🌓</span>
        </button>

        <button type="button" class="context-profile-pill" onclick="openUserSettingsModal('profile')" title="பயனர் சுயவிவரம் &amp; அமைப்புகள்">
          <span class="pill-avatar" id="pillAvatarIcon">👤</span>
          <span class="pill-name" id="pillUserName">சாதகர்</span>
          <span class="pill-badge" id="pillUserTier">தரம் 1-4</span>
        </button>
      </div>
    </div>
  `;

  // Attach inside header for unified sticky behavior
  const header = document.querySelector('header.site-header');
  if (header) {
    header.appendChild(contextBar);
  } else {
    document.body.prepend(contextBar);
  }

  // 4. User Profile & Settings Modal
  const modal = document.createElement('div');
  modal.id = 'userSettingsModal';
  modal.className = 'user-settings-modal';
  modal.onclick = function(e) { if (e.target === this) closeUserSettingsModal(); };
  modal.innerHTML = `
    <div class="user-modal-box">
      <div class="user-modal-header">
        <div class="user-modal-tabs">
          <button type="button" class="user-tab-btn active" id="userTabProfileBtn" onclick="switchUserTab('profile')">
            <span>👤 சுயவிவரம்</span>
          </button>
          <button type="button" class="user-tab-btn" id="userTabPrefsBtn" onclick="switchUserTab('preferences')">
            <span>⚙️ விருப்பங்கள் &amp; அமைப்புகள்</span>
          </button>
        </div>
        <button type="button" class="user-modal-close-btn" onclick="closeUserSettingsModal()" title="மூடுக">✕</button>
      </div>

      <div class="user-modal-body">
        <!-- PROFILE TAB -->
        <div class="user-tab-content active" id="tabContentProfile">
          <div class="profile-hero-card">
            <div class="profile-avatar-large" id="profileLargeAvatar">👤</div>
            <div class="profile-hero-info">
              <h3 id="profileDisplayNameHead">அன்பான சாதகர்</h3>
              <span class="profile-tier-badge" id="profileTierBadge">🌟 தொடக்க சாதகர் (Grade 1-4)</span>
              <p class="profile-streak-line">🔥 தொடர் கற்றல்: <strong id="profileStreakDays">1 நாள்</strong> • படித்த அலகுகள்: <strong id="profileLessonsCount">0</strong></p>
            </div>
          </div>

          <div class="settings-form-group">
            <label class="settings-label">உங்கள் பெயர் அல்லது ஆன்மீகப் பெயர்:</label>
            <input type="text" id="prefUserNameInput" class="settings-input" placeholder="உங்கள் பெயர்" maxlength="30" oninput="saveUserProfileFields()">
          </div>

          <div class="settings-form-group">
            <label class="settings-label">ஆன்மீக நிலை / தரம் (Spiritual Learning Level):</label>
            <select id="prefUserTierSelect" class="settings-select" onchange="saveUserProfileFields()">
              <option value="tier1">🌟 தொடக்க சாதகர் — தரம் 1 முதல் 4 (அறம் அறிதல்)</option>
              <option value="tier2">🪔 இடைநிலை சாதகர் — தரம் 5 முதல் 8 (அறம் பின்பற்றுதல்)</option>
              <option value="tier3">🔱 உயர்நிலை சிவநேசர் — தரம் 9 முதல் 12 (அறம் காத்தல்)</option>
            </select>
          </div>

          <div class="settings-form-group">
            <label class="settings-label">சுயவிவரச் சின்னம் (Choose Avatar Icon):</label>
            <div class="avatar-selection-grid" id="avatarSelectionGrid">
              <button type="button" class="avatar-option" onclick="selectAvatar('👤')">👤</button>
              <button type="button" class="avatar-option" onclick="selectAvatar('🕉️')">🕉️</button>
              <button type="button" class="avatar-option" onclick="selectAvatar('🪔')">🪔</button>
              <button type="button" class="avatar-option" onclick="selectAvatar('🔱')">🔱</button>
              <button type="button" class="avatar-option" onclick="selectAvatar('🌸')">🌸</button>
              <button type="button" class="avatar-option" onclick="selectAvatar('🌺')">🌺</button>
              <button type="button" class="avatar-option" onclick="selectAvatar('📖')">📖</button>
              <button type="button" class="avatar-option" onclick="selectAvatar('🧘')">🧘</button>
              <button type="button" class="avatar-option" onclick="selectAvatar('👑')">👑</button>
            </div>
          </div>

          <div class="profile-stats-card">
            <h4>📊 உங்கள் ஆன்மீகப் பயணக் குறிப்பு (Personal Dashboard)</h4>
            <div class="stats-grid">
              <div class="stat-box">
                <div class="stat-number" id="statDaysVisited">1</div>
                <div class="stat-desc">வருகை நாட்கள்</div>
              </div>
              <div class="stat-box">
                <div class="stat-number" id="statLessonsCompleted">0</div>
                <div class="stat-desc">முடித்த பாடங்கள்</div>
              </div>
              <div class="stat-box">
                <div class="stat-number" id="statBookmarksCount">0</div>
                <div class="stat-desc">சேமித்தவை</div>
              </div>
            </div>
          </div>
        </div>

        <!-- PREFERENCES TAB -->
        <div class="user-tab-content" id="tabContentPreferences">
          <div class="settings-form-group">
            <label class="settings-label">🎨 வண்ணக் கருப்பொருள் (Theme Appearance):</label>
            <div class="radio-pill-group">
              <label class="radio-pill">
                <input type="radio" name="themeChoice" value="cosmic" onchange="changeTheme('cosmic')">
                <span>🌌 தர்மப் பேரொளி (Teal-Violet-Blue-Green - Default)</span>
              </label>
              <label class="radio-pill">
                <input type="radio" name="themeChoice" value="midnight" onchange="changeTheme('midnight')">
                <span>🌊 ஆழ்கடல் நீலம் (Midnight Ocean)</span>
              </label>
              <label class="radio-pill">
                <input type="radio" name="themeChoice" value="amoled" onchange="changeTheme('amoled')">
                <span>🖤 அடர் கருப்பு (OLED Pure Black)</span>
              </label>
            </div>
          </div>

          <div class="settings-form-group">
            <label class="settings-label">🔤 தமிழ் எழுத்துரு பாணி (Tamil Font Style):</label>
            <div class="radio-pill-group">
              <label class="radio-pill">
                <input type="radio" name="fontChoice" value="mukta" onchange="changeFontStyle('mukta')">
                <span>📜 முக்த மலர் (மரபுச் செம்மொழி - Mukta Malar)</span>
              </label>
              <label class="radio-pill">
                <input type="radio" name="fontChoice" value="noto" onchange="changeFontStyle('noto')">
                <span>🔤 நோட்டோ சான்ஸ் (நவீனத் தெளிவு - Noto Sans Tamil)</span>
              </label>
            </div>
          </div>

          <div class="settings-form-group">
            <label class="settings-label">🔍 தளத்தின் பொது எழுத்தளவு (Base Font Scaling):</label>
            <div class="font-size-slider-row">
              <button type="button" class="btn-secondary" onclick="adjustFontSize(-0.06)">A⁻ சிறிதாக்கு</button>
              <span id="sliderFontLabel" class="slider-font-label">100% (இயல்பு)</span>
              <button type="button" class="btn-secondary" onclick="adjustFontSize(0.06)">A⁺ பெரிதாக்கு</button>
            </div>
          </div>

          <div class="settings-form-group">
            <label class="settings-label">🎬 காணொளி &amp; ஒலி விருப்பங்கள் (Media Playback):</label>
            <div class="toggle-option-row">
              <span>தானியங்கி இயக்கம் (Autoplay Video on Open)</span>
              <input type="checkbox" id="prefAutoplay" class="toggle-checkbox" onchange="savePreferences()">
            </div>
            <div class="toggle-option-row">
              <span>தொடர் பின்னணி இசை பயன்முறை (Continuous Loop)</span>
              <input type="checkbox" id="prefContinuous" class="toggle-checkbox" onchange="savePreferences()">
            </div>
          </div>

          <div class="settings-form-group">
            <label class="settings-label">🔔 நற்பண்பு வழிகாட்டல் (Virtue Prompt):</label>
            <div class="toggle-option-row">
              <span>தினம் ஒரு ஆத்திசூடி / குறள் நற்பண்பு நினைவூட்டல்</span>
              <input type="checkbox" id="prefDailyVirtue" class="toggle-checkbox" onchange="savePreferences()">
            </div>
          </div>

          <div class="settings-actions-row">
            <button type="button" class="btn-secondary" onclick="resetUserSettings()">
              🔄 மீட்டமை (Reset)
            </button>
            <button type="button" class="btn-primary" onclick="closeUserSettingsModal()">
              ✓ சேமித்து மூடுக (Save &amp; Close)
            </button>
          </div>
        </div>
      </div>
    </div>
  `;

  document.body.appendChild(modal);

  // Initialize preferences
  loadUserPreferences();
  restorePatanjaliAssessment();
  restorePalmLeafMode();
}

// Auto mount when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', mountAppShell);
} else {
  mountAppShell();
}

// Accordion support and Drawer auto-close on selection
document.addEventListener('click', (e) => {
  // 1. If clicked on a group header that has sub-items, TOGGLE THE ACCORDION!
  const subToggle = e.target.closest('.strip-item.strip-has-sub');
  if (subToggle) {
    e.preventDefault();
    e.stopPropagation();
    const group = subToggle.closest('.strip-group');
    if (group) {
      const wasOpen = group.classList.contains('open');
      // Close other open groups for clean single-accordion behavior
      document.querySelectorAll('.strip-group').forEach(g => {
        if (g !== group) {
          g.classList.remove('open');
          const ind = g.querySelector('.strip-sub-indicator');
          if (ind) ind.innerText = '▾';
        }
      });
      group.classList.toggle('open', !wasOpen);
      const indicator = subToggle.querySelector('.strip-sub-indicator');
      if (indicator) {
        indicator.innerText = !wasOpen ? '▴' : '▾';
      }
    }
    return;
  }

  // 2. If clicked on an actual destination leaf link inside the drawer, close drawer
  const leafLink = e.target.closest('#leftStripBar .strip-sub-item, #leftStripBar .strip-item:not(.strip-has-sub)');
  if (leafLink) {
    closePrimaryMenu();
    return;
  }

  // 3. If clicked on backdrop, close drawer
  if (e.target.id === 'stripBackdrop') {
    closePrimaryMenu();
    return;
  }
});

// Graceful fallback for Google Sites scan images blocked cross-site (CORP: same-site)
document.addEventListener('error', function (e) {
  var img = e.target;
  if (!img || img.tagName !== 'IMG' || !/sitesv-images-rt/.test(img.src || '')) return;
  img.style.display = 'none';
  var thumb = img.closest('.sheet-thumb');
  if (thumb && !thumb.querySelector('.sheet-fallback')) {
    var d = document.createElement('div');
    d.className = 'sheet-fallback';
    d.style.cssText = 'display:flex;align-items:center;justify-content:center;min-height:140px;color:#94a3b8;font-size:0.85rem;text-align:center;padding:12px;';
    d.textContent = '📄 பக்கம் — Google Site இல் காண்க ↗';
    thumb.appendChild(d);
    var ov = thumb.querySelector('.sheet-zoom-overlay'); if (ov) ov.style.display = 'none';
    thumb.removeAttribute('onclick');
  }
}, true);

/* ========================================================================== */
/* FEATURE 1: PATANJALI 7-STAGE SELF-REALIZATION ASSESSMENT & RATING ENGINE   */
/* ========================================================================== */

function calculatePatanjaliScore() {
  const qNames = ['pq1', 'pq2', 'pq3', 'pq4', 'pq5', 'pq6', 'pq7'];
  let totalScore = 0;
  const answers = {};

  for (let i = 0; i < qNames.length; i++) {
    const radios = document.getElementsByName(qNames[i]);
    let val = 1;
    for (let r of radios) {
      if (r.checked) {
        val = parseInt(r.value, 10);
        break;
      }
    }
    answers[qNames[i]] = val;
    totalScore += val;
  }

  try {
    localStorage.setItem('gurukula_patanjali_answers', JSON.stringify(answers));
    localStorage.setItem('gurukula_patanjali_score', totalScore);
  } catch (e) {}

  renderPatanjaliResult(totalScore);
}

function renderPatanjaliResult(score) {
  const resultBox = document.getElementById('patScoreResultBox');
  const levelNameEl = document.getElementById('patResultLevelName');
  const starsEl = document.getElementById('patResultStars');
  const descEl = document.getElementById('patResultDesc');
  const actionEl = document.getElementById('patResultAction');

  if (!resultBox) return;

  let levelName = '';
  let stars = '';
  let desc = '';
  let badgeColor = '#38bdf8';
  let ratingNum = '1.0';
  let legacyAdvice = '';

  if (score <= 9) {
    ratingNum = '1.5';
    levelName = 'நிலை 1: சுபேச்சை (Subheccha) — நல்விருப்ப தொடக்க நிலை';
    stars = '⭐️☆☆☆☆';
    badgeColor = '#38bdf8';
    desc = 'நீங்கள் தர்ம நெறியின் முதற்படியில் அடியெடுத்து வைத்துள்ளீர்கள். ஆன்மீக அமைதியை நாட வேண்டும் என்ற உன்னத விருப்பம் (சுபேச்சை) மலர்ந்துள்ளது. தரம் 1 - 4 தொடக்கப் பாடங்களை வாசித்து, கோபம் தணித்தல், தாய்-தந்தை வழிபாடு மற்றும் தினசரி எளிய தியானத்தில் ஈடுபடுங்கள்.';
    legacyAdvice = 'இல்லற அடித்தளம்: குடும்பத்தில் தினசரி 10 நிமிடம் அமைதி காத்தல், ஒரு குறள் வாசித்தல்.';
  } else if (score <= 12) {
    ratingNum = '2.8';
    levelName = 'நிலை 2: விசாரணை (Vicharana) — மெய்விசாரணை சாதகர் நிலை';
    stars = '⭐️⭐️☆☆☆';
    badgeColor = '#2dd4bf';
    desc = 'சாத்திர விவேகமும் மெய்ப்பொருள் ஆய்வும் உங்களில் மலர்ந்துள்ளது. நித்திய-அநித்திய பகுத்தறிவுடன் வாழ்வியல் முடிவுகளை எடுக்கிறீர்கள். தரம் 5 - 8 பாடங்கள், திருமுறைத் தேவாரங்கள் மற்றும் பகவத் கீதை சிந்தனைகள் உங்கள் விவேகத்தை மேலும் கூர்மையாக்கும்.';
    legacyAdvice = 'இல்லற தர்மம்: குழந்தைகளுக்கு நல்லொழுக்கக் கதைகள் கற்பித்தல், எளிய ஜீவகாருண்ய தானம்.';
  } else if (score <= 15) {
    ratingNum = '4.2';
    levelName = 'நிலை 3: தனுமானசி (Tanumanasa) — நுண்ணிய மன அடக்கம் & இல்லற ஒழுக்கம்';
    stars = '⭐️⭐️⭐️☆☆';
    badgeColor = '#c084fc';
    desc = 'புலனடக்கமும், கோப மேலாண்மையும் கைகூடியுள்ளது. மனம் சிதறாமல் தர்மத்தில் ஒருமுகப்பட்டுள்ளது. இல்லறத்தில் பஞ்ச மகா யக்ஞங்களைத் தவறாது கடைப்பிடித்து, சினமின்மை என்ற மாபெரும் தவத்தை உங்கள் இல்லத்தில் நிலைநிறுத்துங்கள்.';
    legacyAdvice = 'இல்லற தர்மம்: தினசரி பஞ்ச மகா யக்ஞ டிராக்கரை 30 நாட்கள் தொடர்ச்சியாக பூர்த்தி செய்தல்.';
  } else if (score <= 17) {
    ratingNum = '5.4';
    levelName = 'நிலை 4: சத்வாபத்தி (Sattvapatti) — தூய சத்துவ நிலை & பிரம்ம பாவனை';
    stars = '⭐️⭐️⭐️⭐️☆';
    badgeColor = '#facc15';
    desc = 'அகத்தூய்மையும், விருப்பு-வெறுப்பற்ற சமநிலையும் ஆழமாக நிலவுகிறது. உலக சவால்கள் உங்கள் நிம்மதியைக் குலைப்பதில்லை. பதி, பசு, பாச மெய்யறிவை உணர்ந்து, உங்கள் குடும்பத்தை ஆன்மீகத் திருத்தலமாக வழிநடத்தும் சான்றோனாக மிளிர்கிறீர்கள்.';
    legacyAdvice = 'இல்லற தலைமை: குடும்ப அறநெறி சாசனம் (Family Charter) உருவாக்கி தலைமுறை நெறியாக்குதல்.';
  } else if (score <= 19) {
    ratingNum = '6.3';
    levelName = 'நிலை 5: அசம்சக்தி (Asamsakti) — பற்றற்ற நிஷ்காம கர்ம யோகம்';
    stars = '⭐️⭐️⭐️⭐️⭐️';
    badgeColor = '#fb923c';
    desc = 'தாமரை இலைத் தண்ணீர் போல குடும்பப் பொறுப்புகளை முழுமையான அன்போடும் கடமையுணர்ச்சியோடும் நிறைவேற்றுகிறீர்கள்; அதே சமயம் எவ்வித சுயநலப் பற்றுமின்றி ஈசன் செயல் என சரணடைகிறீர்கள். மரண பயமற்ற ஜீவன் முக்திப் பாதைக்கு மிக அருகில் உள்ளீர்கள்.';
    legacyAdvice = 'உன்னத மரபு (Legacy): சமுதாய அறப்பணிகள், வித்யா தானம், இளைஞர்களுக்கு தர்ம வழிகாட்டல்.';
  } else {
    ratingNum = '7.0';
    levelName = 'நிலை 6 & 7: பதார்த்த பாவனை & துரியகா (Turiya) — ஜீவன் முக்தி & உன்னத சால்பு';
    stars = '👑 ⭐️⭐️⭐️⭐️⭐️ 👑';
    badgeColor = '#e11d48';
    desc = '‘வையத்துள் வாழ்வாங்கு வாழ்பவன் வான்உறையும் தெய்வத்துள் வைக்கப் படும்’ (குறள் 50). குடும்பத்தை அறவழியில் உயர்த்தி, தலைமுறைகள் போற்றும் அழியாத தர்ம மரபை (Enduring Legacy) நிறுவிய நிறைவு நிலை. பிறவிப் பெருங்கடலை நீந்தி அதிவேக முக்தியை அடைந்துவிட்டீர்கள்!';
    legacyAdvice = 'மரபுச் சின்னம்: முழு சமுதாயத்திற்கும் தெய்விக சான்றாண்மையின் நேரடி கலங்கரை விளக்கம்.';
  }

  if (levelNameEl) levelNameEl.innerHTML = `<span style="color:${badgeColor}; font-size:1.1rem; display:block; margin-bottom:4px;">ஆன்ம முதிர்ச்சி எண்: ${ratingNum} / 7.0 (மதிப்பெண்: ${score}/21)</span>${levelName}`;
  if (starsEl) starsEl.innerHTML = stars;
  if (descEl) {
    descEl.innerHTML = `
      <div style="margin-bottom:12px;">${desc}</div>
      <div style="background:rgba(255,255,255,0.06); border-left:3px solid ${badgeColor}; padding:10px 14px; border-radius:6px; font-size:0.88rem; color:#f1f5f9; text-align:left;">
        <strong>🌿 இல்லற &amp; மரபு வழிகாட்டல் (Legacy Action):</strong> ${legacyAdvice}
      </div>
    `;
  }

  if (actionEl) {
    actionEl.innerHTML = `
      <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap; margin-top:14px;">
        <button type="button" onclick="window.print()" class="sheet-btn" style="background:linear-gradient(135deg,#059669,#0d9488); color:#ffffff; font-weight:700; padding:8px 18px; border-radius:10px; cursor:pointer;">
          🖨️ மதிப்பீட்டுச் சான்றிதழை அச்சிடுக
        </button>
        <a href="kalvi.html#grihasthaTracker" class="sheet-btn" style="background:linear-gradient(135deg,#d4af37,#996515); color:#000000; font-weight:700; padding:8px 18px; border-radius:10px; text-decoration:none;">
          ✅ பஞ்ச மகா யக்ஞ சாதனா தொடங்குக ↗
        </a>
      </div>
    `;
  }

  resultBox.style.display = 'block';
  resultBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function restorePatanjaliAssessment() {
  try {
    const raw = localStorage.getItem('gurukula_patanjali_answers');
    if (!raw) return;
    const answers = JSON.parse(raw);
    for (let k in answers) {
      const radios = document.getElementsByName(k);
      for (let r of radios) {
        if (parseInt(r.value, 10) === answers[k]) {
          r.checked = true;
        }
      }
    }
    const score = parseInt(localStorage.getItem('gurukula_patanjali_score'), 10);
    if (score && document.getElementById('patScoreResultBox')) {
      renderPatanjaliResult(score);
    }
  } catch (e) {}
}

/* ========================================================================== */
/* FEATURE 2: ASHRAM SOUNDSCAPE & DINACHARYA BELL (WEB AUDIO SYNTHESIS)       */
/* ========================================================================== */

let _audioCtx = null;
let _omOsc1 = null;
let _omOsc2 = null;
let _omGain = null;
let _isOmPlaying = false;

function getAudioContext() {
  if (!_audioCtx) {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (AudioContext) {
      _audioCtx = new AudioContext();
    }
  }
  if (_audioCtx && _audioCtx.state === 'suspended') {
    _audioCtx.resume();
  }
  return _audioCtx;
}

/**
 * Synthesizes an authentic bronze temple bell with inharmonic resonant partials.
 * @param {number} baseFreq Base frequency in Hz (Default: 432 Hz sacred A / 528 Hz)
 */
function playAshramTempleBell(baseFreq = 432) {
  const ctx = getAudioContext();
  if (!ctx) return;

  const now = ctx.currentTime;
  const masterGain = ctx.createGain();
  masterGain.connect(ctx.destination);

  // Inharmonic bell partial multipliers (approx. resonant ratios of traditional temple bells)
  const partials = [
    { ratio: 1.0, gain: 0.6, decay: 3.5 },
    { ratio: 2.02, gain: 0.4, decay: 2.8 },
    { ratio: 3.01, gain: 0.25, decay: 2.0 },
    { ratio: 4.24, gain: 0.18, decay: 1.5 },
    { ratio: 5.43, gain: 0.12, decay: 1.1 },
    { ratio: 6.81, gain: 0.08, decay: 0.8 }
  ];

  masterGain.gain.setValueAtTime(0.8, now);

  partials.forEach(p => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(baseFreq * p.ratio, now);

    // Strike attack and exponential decay
    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(p.gain, now + 0.008);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + p.decay);

    osc.connect(gain);
    gain.connect(masterGain);

    osc.start(now);
    osc.stop(now + p.decay + 0.1);
  });
}

/**
 * Plays a distinct melodic chime for each of the 4 Ashram Yamas.
 * @param {number} yamaIndex 0: Usha (528Hz), 1: Vidya (432Hz), 2: Seva (384Hz), 3: Sandhya (288Hz)
 */
function playYamaChime(yamaIndex) {
  const freqs = [528, 432, 384, 288];
  const freq = freqs[yamaIndex] || 432;
  playAshramTempleBell(freq);

  // Show a gentle visual toast if possible
  const yamaNames = ['உஷா காலம் (பிரம்ம முகூர்த்தம்)', 'வித்யா யாமம் (சுவடிப் பாடம்)', 'சேவா யாமம் (கோ சேவை)', 'சந்தியா யாமம் (தீபாராதனை)'];
  console.log('🪔 ஆசிரம யாம நாதம் ஒலித்தது:', yamaNames[yamaIndex] || 'ஆசிரம மணி');
}

/**
 * Toggles ambient continuous Pranava Om (136.1 Hz) + Tambura harmonic drone.
 */
function toggleAshramOmDrone() {
  const ctx = getAudioContext();
  if (!ctx) return false;

  const btn = document.getElementById('ashramSoundToggleBtn');

  if (_isOmPlaying) {
    if (_omGain) {
      _omGain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 1.0);
      setTimeout(() => {
        if (_omOsc1) { _omOsc1.stop(); _omOsc1.disconnect(); }
        if (_omOsc2) { _omOsc2.stop(); _omOsc2.disconnect(); }
        _isOmPlaying = false;
        if (btn) {
          btn.classList.remove('active');
          btn.innerHTML = '🪔 <span>ஓம் நாதம் கேட்க</span>';
        }
      }, 1000);
    }
    return false;
  } else {
    const now = ctx.currentTime;
    _omGain = ctx.createGain();
    _omGain.gain.setValueAtTime(0.0001, now);
    _omGain.gain.linearRampToValueAtTime(0.25, now + 1.5);
    _omGain.connect(ctx.destination);

    // Fundamental Om tone (136.1 Hz - Earth frequency / Cosmic Aum)
    _omOsc1 = ctx.createOscillator();
    _omOsc1.type = 'sine';
    _omOsc1.frequency.setValueAtTime(136.1, now);

    // Fifth harmonic (204.15 Hz Pa / Panchama tanpura string)
    _omOsc2 = ctx.createOscillator();
    _omOsc2.type = 'sine';
    _omOsc2.frequency.setValueAtTime(204.15, now);

    _omOsc1.connect(_omGain);
    _omOsc2.connect(_omGain);

    _omOsc1.start(now);
    _omOsc2.start(now);
    _isOmPlaying = true;

    if (btn) {
      btn.classList.add('active');
      btn.innerHTML = '🔕 <span>ஓம் நாதம் நிறுத்துக</span>';
    }
    return true;
  }
}

/* ========================================================================== */
/* FEATURE 4: PALM-LEAF MANUSCRIPT (ஓலைச்சுவடி வடிவம்) CONTROLLER             */
/* ========================================================================== */

function togglePalmLeafMode() {
  document.body.classList.toggle('palm-leaf-mode-active');
  const isEnabled = document.body.classList.contains('palm-leaf-mode-active');
  try {
    localStorage.setItem('gurukula_palm_leaf_mode', isEnabled ? 'true' : 'false');
  } catch (e) {}

  const btn = document.getElementById('palmLeafToggleBtn');
  if (btn) {
    btn.classList.toggle('active', isEnabled);
    btn.innerHTML = isEnabled ? '📜 <span>இயல்பு வடிவம் (Modern)</span>' : '📜 <span>ஓலைச்சுவடி வடிவம் (Palm-Leaf)</span>';
  }
}

function restorePalmLeafMode() {
  try {
    const isEnabled = localStorage.getItem('gurukula_palm_leaf_mode') === 'true';
    if (isEnabled) {
      document.body.classList.add('palm-leaf-mode-active');
      const btn = document.getElementById('palmLeafToggleBtn');
      if (btn) {
        btn.classList.add('active');
        btn.innerHTML = '📜 <span>இயல்பு வடிவம் (Modern)</span>';
      }
    }
  } catch (e) {}
}

/* ========================================================================== */
/* FEATURE 5: PWA & OFFLINE SERVICE WORKER REGISTRATION                       */
/* ========================================================================== */

if ('serviceWorker' in navigator && (window.location.protocol === 'https:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js').then((reg) => {
      console.log('🏛️ ஆசிரம ஆஃப்லைன் சேவை இயங்குகிறது (PWA Service Worker registered):', reg.scope);
    }).catch((err) => {
      console.warn('PWA Service Worker registration skipped or failed:', err);
    });
  });
}

/* ========================================================================== */
/* FEATURE 6: GURU SPEECH SYNTHESIS ENGINE (குரு உரை கேட்போம்)                 */
/* ========================================================================== */

let _currentSpeechUtterance = null;

function speakLessonText(text, btnElement) {
  if (!('speechSynthesis' in window)) {
    alert('உங்கள் உலாவியில் குரல் வாசிப்பு வசதி (Speech Synthesis) ஆதரிக்கப்படவில்லை.');
    return;
  }

  if (window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel();
    if (btnElement && btnElement.classList.contains('speaking')) {
      btnElement.classList.remove('speaking');
      btnElement.innerHTML = '🔊 குரு உரை கேட்க';
      return;
    }
  }

  const cleanText = text.replace(/<[^>]*>/g, '').trim();
  if (!cleanText) return;

  const utterance = new SpeechSynthesisUtterance(cleanText);
  utterance.rate = 0.88; // Calm, meditative pace
  utterance.pitch = 1.0;

  // Search for available Tamil voice
  const voices = window.speechSynthesis.getVoices();
  const tamilVoice = voices.find(v => v.lang.startsWith('ta')) || voices.find(v => v.lang.includes('IN'));
  if (tamilVoice) {
    utterance.voice = tamilVoice;
  }

  if (btnElement) {
    btnElement.classList.add('speaking');
    btnElement.innerHTML = '⏹️ நிறுத்துக';
  }

  utterance.onend = function() {
    if (btnElement) {
      btnElement.classList.remove('speaking');
      btnElement.innerHTML = '🔊 குரு உரை கேட்க';
    }
  };

  utterance.onerror = function() {
    if (btnElement) {
      btnElement.classList.remove('speaking');
      btnElement.innerHTML = '🔊 குரு உரை கேட்க';
    }
  };

  _currentSpeechUtterance = utterance;
  window.speechSynthesis.speak(utterance);
}


