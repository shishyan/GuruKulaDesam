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
  if (nav) nav.classList.toggle('open');
}

// Close player on ESC key
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closePlayer();
});
