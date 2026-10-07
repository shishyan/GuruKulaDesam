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
  theme: 'gold',
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
  document.body.classList.remove('theme-midnight', 'theme-amoled');
  if (userPrefs.theme === 'midnight') document.body.classList.add('theme-midnight');
  if (userPrefs.theme === 'amoled') document.body.classList.add('theme-amoled');

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
  const themes = ['gold', 'midnight', 'amoled'];
  const curIdx = themes.indexOf(userPrefs.theme || 'gold');
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

// Keyboard shortcuts: '/' to search, 'Esc' to close
document.addEventListener('keydown', e => {
  if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
    const input = document.getElementById('contextQuickSearch');
    if (input) {
      e.preventDefault();
      input.focus();
      input.select();
    }
  }
  if (e.key === 'Escape') {
    closeUserSettingsModal();
    closeMobileStrip();
  }
});

// --------------------------------------------------------------------------
// APP SHELL DOM MOUNTING & CONTEXT RESOLUTION
// --------------------------------------------------------------------------
function resolvePageContext() {
  const path = window.location.pathname.toLowerCase();
  const filename = path.split('/').pop() || 'index.html';

  const contextMap = {
    'index.html': { root: 'முகப்பு', title: 'ஆன்மீகப் பெருவெளி', desc: '580 பக்தி இசை வெளியீடுகள்' },
    'kalvi.html': { root: 'கல்வி', title: 'சைவ நெறி பாடநெறி', desc: 'தரம் 1 முதல் 12 வரையிலான முழுமைப் பாடத்திட்டம்' },
    'virtues.html': { root: 'கல்வி', title: 'அகர வரிசை நற்பண்பு நெறிமுறை', desc: '30+ நற்பண்புகள் • 3 நிலைகள்' },
    'tharam-1.html': { root: 'கல்வி', title: 'தரம் 1 (Grade 1)', desc: 'அடிப்படை சைவ நெறி & நற்பண்புகள்' },
    'tharam-2.html': { root: 'கல்வி', title: 'தரம் 2 (Grade 2)', desc: 'இறைவணக்கம் & இல்லற தர்மம்' },
    'tharam-3.html': { root: 'கல்வி', title: 'தரம் 3 (Grade 3)', desc: 'நல்வழி & ஆசாரக் கல்வி' },
    'tharam-4.html': { root: 'கல்வி', title: 'தரம் 4 (Grade 4)', desc: 'கொன்றை வேந்தன் & ஒழுக்கம்' },
    'tharam-5.html': { root: 'கல்வி', title: 'தரம் 5 (Grade 5)', desc: 'பன்னிரு திருமுறை அறிமுகம்' },
    'tharam-6.html': { root: 'கல்வி', title: 'தரம் 6 (Grade 6)', desc: 'சைவ சித்தாந்த ஆரம்ப நெறி' },
    'tharam-7.html': { root: 'கல்வி', title: 'தரம் 7 (Grade 7)', desc: 'திருமுறைகள் & நாயன்மார் வரலாறு' },
    'tharam-8.html': { root: 'கல்வி', title: 'தரம் 8 (Grade 8)', desc: 'அட்ட வீரட்டம் & ஆலய தத்துவம்' },
    'tharam-9.html': { root: 'கல்வி', title: 'தரம் 9 (Grade 9)', desc: 'சைவ சித்தாந்த சாத்திரங்கள்' },
    'tharam-10.html': { root: 'கல்வி', title: 'தரம் 10 (Grade 10)', desc: 'O/L சைவ நன்னெறி முழுமைப் பாடநெறி' },
    'tharam-11.html': { root: 'கல்வி', title: 'தரம் 11 (Grade 11)', desc: 'A/L உயர்தர சைவ சித்தாந்தம்' },
    'tharam-12.html': { root: 'கல்வி', title: 'தரம் 12 (Grade 12)', desc: 'A/L தத்துவ ஆய்வு & சிவபோக நிலை' },
    'saiva-neri.html': { root: 'சைவ நெறி', title: 'பன்னிரு திருமுறைகள்', desc: '172 சிவத் திருப்பதிகங்கள் & ருத்ரம்' },
    'murugan.html': { root: 'வழிபாட்டு நெறி', title: 'முருகன் (Kaumaram)', desc: 'கந்த சஷ்டி, திருப்புகழ் & கானங்கள்' },
    'sakthi.html': { root: 'வழிபாட்டு நெறி', title: 'சக்தி (Shaktham)', desc: 'அபிராமி அந்தாதி & லலிதா போற்றிகள்' },
    'vinayagar.html': { root: 'வழிபாட்டு நெறி', title: 'விநாயகர் (Ganapathyam)', desc: 'விநாயகர் அகவல் & மூல கணபதி' },
    'vaishnava.html': { root: 'வழிபாட்டு நெறி', title: 'வைணவம் (Vaishnavam)', desc: 'விஷ்ணு, கிருஷ்ணர் & திவ்வியப் பிரபந்தம்' },
    'thirukkural.html': { root: 'தமிழ்மறை', title: 'திருக்குறள் (Thirukkural)', desc: '1330 அருங்குறள்கள் & இசைப்பாடல்கள்' },
    'sanmargam.html': { root: 'சன்மார்க்கம்', title: 'வள்ளலார் சுத்த சன்மார்க்கம்', desc: 'திருவருட்பா & ஆன்மநேய ஒருமைப்பாடு' },
    'irai-isai-virundhu.html': { root: 'இசை', title: 'இறை இசை விருந்து', desc: 'ஆன்மீக பக்தி ஆல்பங்கள்' },
    'syllabus.html': { root: 'கல்வி', title: 'முழுமையான பாடத்திட்டம்', desc: 'வேத & சைவ நெறி கல்வி அமைப்பு' },
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
      { id: 'tab-all-grades', icon: '🎓', label: 'அனைத்து தரங்கள்', href: 'kalvi.html' }
    ];
  }

  // 2. Curriculum Hub (kalvi.html)
  if (filename === 'kalvi.html') {
    return [
      { id: 'tab-overview', icon: '🏛️', label: 'பாடநெறி அறிமுகம்', action: "scrollToSection('kalviOverview')", active: true },
      { id: 'tab-virtues', icon: '🔤', label: 'அகர வரிசை நற்பண்புகள்', href: 'virtues.html' },
      { id: 'tab-tier1', icon: '🌟', label: 'தரம் 1-4 (தொடக்க நிலை)', action: "scrollToSection('tier1Section')" },
      { id: 'tab-tier2', icon: '🪔', label: 'தரம் 5-8 (இடைநிலை)', action: "scrollToSection('tier2Section')" },
      { id: 'tab-tier3', icon: '🔱', label: 'தரம் 9-12 (உயர்நிலை)', action: "scrollToSection('tier3Section')" },
      { id: 'tab-syllabus', icon: '📚', label: 'முழு பாடத்திட்டம்', href: 'syllabus.html' }
    ];
  }

  // 3. Virtues Matrix (virtues.html)
  if (filename === 'virtues.html') {
    return [
      { id: 'tab-all', icon: '🌟', label: 'அனைத்து நற்பண்புகள் (30+)', action: "filterVirtues('all')", active: true },
      { id: 'tab-t1', icon: '🟢', label: 'Tier 1: அறிதல் (தரம் 1-4)', action: "filterVirtues('tier-1')" },
      { id: 'tab-t2', icon: '🟡', label: 'Tier 2: செய்தல் (தரம் 5-8)', action: "filterVirtues('tier-2')" },
      { id: 'tab-t3', icon: '🔴', label: 'Tier 3: காத்தல் (தரம் 9-12)', action: "filterVirtues('tier-3')" },
      { id: 'tab-kalvi', icon: '🎓', label: 'கல்வித் தளம்', href: 'kalvi.html' }
    ];
  }

  // 4. Master Home (index.html)
  if (filename === 'index.html' || filename === '') {
    return [
      { id: 'tab-all-media', icon: '🌟', label: 'அனைத்து வெளியீடுகள் (580)', action: "setTypeFilter('all')", active: true },
      { id: 'tab-films', icon: '🎬', label: 'முழுத் திரைப்படங்கள்', action: "setTypeFilter('film')" },
      { id: 'tab-audio', icon: '🎵', label: 'இசை வெளியீடுகள்', action: "setTypeFilter('audio')" },
      { id: 'tab-phil', icon: '🔱', label: 'தத்துவ சாரம்', action: "scrollToSection('philosophySection')" },
      { id: 'tab-contact', icon: '📍', label: 'மைய முகவரி', action: "scrollToSection('siteFooter')" }
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
      { id: 'tab-grade-portal', icon: '🎓', label: '12 தரங்கள்', href: 'kalvi.html' }
    ];
  }

  // Default fallback
  return [
    { id: 'tab-home', icon: '🏠', label: 'முகப்பு', href: 'index.html' },
    { id: 'tab-kalvi', icon: '🎓', label: 'கல்வி', href: 'kalvi.html' },
    { id: 'tab-virtues', icon: '🔤', label: 'நற்பண்புகள்', href: 'virtues.html' },
    { id: 'tab-saiva', icon: '🕉️', label: 'சைவ நெறி', href: 'saiva-neri.html' }
  ];
}

function scrollToSection(id, optionalTabId) {
  if (optionalTabId && typeof switchCourseTab === 'function') {
    switchCourseTab(optionalTabId);
  }
  const el = document.getElementById(id) || document.querySelector('.' + id);
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
    { href: 'kalvi.html', icon: '🎓', label: 'கல்வி நெறி' },
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
                <input type="radio" name="themeChoice" value="gold" onchange="changeTheme('gold')">
                <span>✨ தங்கக் கருமை (Cosmic Gold - Default)</span>
              </label>
              <label class="radio-pill">
                <input type="radio" name="themeChoice" value="midnight" onchange="changeTheme('midnight')">
                <span>🌌 நள்ளிரவு நீலம் (Midnight Navy)</span>
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
