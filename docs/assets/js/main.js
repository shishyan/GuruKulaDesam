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

function toggleModalFullscreen() {
  const modalBox = document.getElementById('playerModalBox') || document.querySelector('.player-modal-box');
  const btn = document.querySelector('.modal-fullscreen-btn');
  
  if (!document.fullscreenElement && !document.webkitFullscreenElement) {
    const target = modalBox || document.documentElement;
    if (target.requestFullscreen) {
      target.requestFullscreen().catch(() => {
        if (modalBox) modalBox.classList.toggle('modal-theater-mode');
      });
    } else if (target.webkitRequestFullscreen) {
      target.webkitRequestFullscreen();
    } else {
      if (modalBox) modalBox.classList.toggle('modal-theater-mode');
    }
    if (btn) btn.innerHTML = '⛶ இயல்பு (Exit)';
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen().catch(() => {});
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    }
    if (modalBox) modalBox.classList.remove('modal-theater-mode');
    if (btn) btn.innerHTML = '⛶ முழுத்திரை';
  }
}

document.addEventListener('fullscreenchange', function() {
  const btn = document.querySelector('.modal-fullscreen-btn');
  const modalBox = document.getElementById('playerModalBox') || document.querySelector('.player-modal-box');
  if (!document.fullscreenElement) {
    if (modalBox) modalBox.classList.remove('modal-theater-mode');
    if (btn) btn.innerHTML = '⛶ முழுத்திரை';
  } else {
    if (btn) btn.innerHTML = '⛶ இயல்பு (Exit)';
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
          <button type="button" class="modal-fullscreen-btn" onclick="toggleModalFullscreen()" title="முழுத்திரை (Fullscreen)">⛶ முழுத்திரை</button>
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
// MODAL & SIDEBAR CONTROLS
// --------------------------------------------------------------------------
function toggleLeftStrip() {
  const strip = document.getElementById('leftStripBar');
  const backdrop = document.getElementById('stripBackdrop');
  if (!strip) return;

  if (window.innerWidth <= 991) {
    const isMobileOpen = strip.classList.toggle('mobile-open');
    if (backdrop) backdrop.classList.toggle('active', isMobileOpen);
  } else {
    const isExpanded = strip.classList.toggle('expanded');
    document.body.classList.toggle('strip-expanded', isExpanded);
    const toggleIcon = strip.querySelector('.strip-toggle-icon');
    if (toggleIcon) toggleIcon.innerText = isExpanded ? '⇥' : '⇤';
    localStorage.setItem('GURUKULA_STRIP_EXPANDED', isExpanded ? 'true' : 'false');
  }
}

function closeMobileStrip() {
  const strip = document.getElementById('leftStripBar');
  const backdrop = document.getElementById('stripBackdrop');
  if (strip) strip.classList.remove('mobile-open');
  if (backdrop) backdrop.classList.remove('active');
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

function mountAppShell() {
  if (document.getElementById('leftStripBar')) return;

  const currentPath = (window.location.pathname.split('/').pop() || 'index.html').toLowerCase();
  const ctx = resolvePageContext();

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
