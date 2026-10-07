// Guru Kula Desam - Modern Video Portal Logic
let currentFilter = 'all';
let currentSearch = '';

function initPage(itemsData) {
  window.pageItems = itemsData;
  renderCards();
}

function getFilteredItems() {
  if (!window.pageItems) return [];
  return window.pageItems.filter(it => {
    if (currentFilter !== 'all' && it.type !== currentFilter) return false;
    if (currentSearch) {
      const q = currentSearch.toLowerCase();
      return it.title.toLowerCase().includes(q) || it.id.includes(q);
    }
    return true;
  });
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

  grid.innerHTML = items.map(it => `
    <div class="video-card" onclick="openPlayer('${it.id}', '${it.title.replace(/'/g, "\\'")}')">
      <div class="card-thumbnail">
        <img src="https://i.ytimg.com/vi/${it.id}/mqdefault.jpg" loading="lazy" alt="${it.title}">
        <span class="card-badge ${it.type === 'film' ? 'badge-film' : 'badge-audio'}">${it.type === 'film' ? 'Film' : 'Audio'}</span>
        <div class="card-play-btn">▶</div>
      </div>
      <div class="card-body">
        <div class="card-title">${it.title}</div>
        <div class="card-footer">
          <span class="tag">${it.type === 'film' ? '🎬 முழுப் படம் (Film)' : '🎵 இசை வெளியீடு (Audio)'}</span>
          <span>YouTube ↗</span>
        </div>
      </div>
    </div>
  `).join('');
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
  const modal = document.getElementById('playerModal');
  const iframe = document.getElementById('modalIframe');
  const titleEl = document.getElementById('modalTitle');

  if (modal && iframe) {
    iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1`;
    if (titleEl) titleEl.innerText = title;
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
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

function toggleDropdown(e) {
  if (e) {
    e.preventDefault();
    e.stopPropagation();
  }
  const dropdown = document.querySelector('.nav-dropdown');
  const toggleBtn = document.getElementById('traditionsDropdownBtn');
  if (!dropdown) return;
  const isOpen = dropdown.classList.toggle('open');
  if (toggleBtn) toggleBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
}

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
  const dropdown = document.querySelector('.nav-dropdown');
  if (dropdown && !dropdown.contains(e.target)) {
    dropdown.classList.remove('open');
    const toggleBtn = document.getElementById('traditionsDropdownBtn');
    if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'false');
  }
});

// Close player and menus on ESC key
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    closePlayer();
    closeMobileNav();
    const dropdown = document.querySelector('.nav-dropdown');
    if (dropdown) dropdown.classList.remove('open');
  }
});

// Sheet Modal Handlers
function openSheetModal(imgSrc, pageNum, pageTitle) {
  const modal = document.getElementById('sheetModal');
  const modalImg = document.getElementById('sheetModalImg');
  const modalTitle = document.getElementById('sheetModalTitle');
  if (modal && modalImg) {
    modalImg.src = imgSrc;
    if (modalTitle) modalTitle.innerText = `தரம் 1 — பக்கம் ${pageNum} ${pageTitle ? '• ' + pageTitle : ''}`;
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
