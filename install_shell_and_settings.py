import os
import re

print("=== Starting Left Strip Bar, Context Top Bar & User Profile/Preferences Integration ===")

# --- 1. CSS UPGRADE ---
css_paths = ['assets/css/style.css', 'docs/assets/css/style.css', 'site/assets/css/style.css']

SHELL_CSS = """
/* -------------------------------------------------------------------------- */
/* THEMES & USER PREFERENCES STYLES                                            */
/* -------------------------------------------------------------------------- */
:root {
  --user-font-scale: 1;
}

body {
  font-size: calc(1rem * var(--user-font-scale, 1));
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* Midnight Navy Theme */
body.theme-midnight {
  --bg-dark: #080d1a;
  --bg-surface: #0e172e;
  --bg-card: rgba(16, 26, 48, 0.85);
  --border-gold: rgba(212, 175, 55, 0.3);
  --border-gold-hover: rgba(255, 215, 0, 0.65);
  background-color: #080d1a !important;
  background-image: linear-gradient(180deg, rgba(8, 13, 26, 0.82) 0%, rgba(8, 13, 26, 0.92) 100%), url('../images/western-ghats-bg.jpg') !important;
}

/* AMOLED Pure Black Theme */
body.theme-amoled {
  --bg-dark: #000000;
  --bg-surface: #0a0a0a;
  --bg-card: rgba(14, 14, 14, 0.95);
  --border-subtle: rgba(255, 255, 255, 0.12);
  --border-gold: rgba(212, 175, 55, 0.35);
  --border-gold-hover: rgba(255, 215, 0, 0.7);
  background-color: #000000 !important;
  background-image: none !important;
}

/* Tamil Font Selection */
body.font-noto {
  font-family: 'Noto Sans Tamil', 'Outfit', sans-serif !important;
}
body.font-mukta {
  font-family: 'Mukta Malar', 'Outfit', serif !important;
}

/* -------------------------------------------------------------------------- */
/* LEFT STRIP BAR (SIDEBAR DOCK)                                              */
/* -------------------------------------------------------------------------- */
.left-strip-bar {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  width: 68px;
  background: rgba(10, 13, 20, 0.96);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border-right: 1px solid var(--border-gold);
  z-index: 850;
  display: flex;
  flex-direction: column;
  transition: width 0.25s cubic-bezier(0.4, 0, 0.2, 1), transform 0.25s ease;
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.6);
  user-select: none;
}

.left-strip-bar.expanded {
  width: 230px;
}

.strip-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 14px;
  border-bottom: 1px solid var(--border-subtle);
  flex-shrink: 0;
}

.strip-brand-link {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  overflow: hidden;
}

.strip-emblem {
  font-size: 1.6rem;
  color: var(--gold-bright);
  filter: drop-shadow(0 0 8px rgba(212, 175, 55, 0.6));
  line-height: 1;
  flex-shrink: 0;
}

.strip-brand-text {
  font-size: 0.92rem;
  font-weight: 700;
  color: var(--gold-soft);
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.2s ease;
  pointer-events: none;
}

.left-strip-bar.expanded .strip-brand-text {
  opacity: 1;
  pointer-events: auto;
}

.strip-toggle-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-subtle);
  color: var(--gold-soft);
  width: 28px;
  height: 28px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  transition: all 0.2s;
  flex-shrink: 0;
}

.strip-toggle-btn:hover {
  background: rgba(212, 175, 55, 0.2);
  border-color: var(--gold);
  color: #fff;
}

.strip-nav-list {
  flex-grow: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 10px 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.strip-nav-list::-webkit-scrollbar {
  width: 4px;
}
.strip-nav-list::-webkit-scrollbar-thumb {
  background: rgba(212, 175, 55, 0.3);
  border-radius: 2px;
}

.strip-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 12px;
  border-radius: 10px;
  color: var(--text-muted);
  text-decoration: none;
  font-size: 0.88rem;
  font-weight: 600;
  transition: all 0.2s ease;
  white-space: nowrap;
  position: relative;
}

.strip-item:hover {
  background: rgba(212, 175, 55, 0.12);
  color: var(--gold-soft);
}

.strip-item.active {
  background: linear-gradient(90deg, rgba(212, 175, 55, 0.22), rgba(212, 175, 55, 0.06));
  color: var(--gold-bright);
  border-left: 3px solid var(--gold);
}

.strip-item-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
}

.strip-item-label {
  opacity: 0;
  transition: opacity 0.2s ease;
  pointer-events: none;
}

.left-strip-bar.expanded .strip-item-label {
  opacity: 1;
  pointer-events: auto;
}

/* Floating Tooltip when collapsed */
.left-strip-bar:not(.expanded) .strip-item::after {
  content: attr(data-tooltip);
  position: absolute;
  left: 74px;
  top: 50%;
  transform: translateY(-50%);
  background: #141824;
  color: var(--gold-soft);
  border: 1px solid var(--border-gold);
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 0.8rem;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s, transform 0.2s;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.left-strip-bar:not(.expanded) .strip-item:hover::after {
  opacity: 1;
  transform: translateY(-50%) translateX(4px);
}

.strip-footer-dock {
  padding: 10px 8px;
  border-top: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex-shrink: 0;
  background: rgba(8, 10, 16, 0.8);
}

.strip-dock-btn {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 12px;
  border-radius: 10px;
  color: var(--text-muted);
  background: none;
  border: none;
  font-family: inherit;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s;
  width: 100%;
}

.strip-dock-btn:hover {
  background: rgba(212, 175, 55, 0.14);
  color: var(--gold-bright);
}

.strip-dock-avatar {
  font-size: 1.25rem;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.strip-dock-label {
  opacity: 0;
  transition: opacity 0.2s ease;
  white-space: nowrap;
  pointer-events: none;
}

.left-strip-bar.expanded .strip-dock-label {
  opacity: 1;
  pointer-events: auto;
}

/* Page Layout Offsets on Desktop */
@media (min-width: 992px) {
  body {
    padding-left: 68px;
    transition: padding-left 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  }
  body.strip-expanded {
    padding-left: 230px;
  }
}

/* Mobile Off-canvas Drawer */
@media (max-width: 991px) {
  .left-strip-bar {
    transform: translateX(-100%);
    width: 240px;
  }
  .left-strip-bar.mobile-open {
    transform: translateX(0);
  }
  .left-strip-bar.mobile-open .strip-item-label,
  .left-strip-bar.mobile-open .strip-dock-label,
  .left-strip-bar.mobile-open .strip-brand-text {
    opacity: 1;
    pointer-events: auto;
  }
  .strip-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
    z-index: 840;
    display: none;
  }
  .strip-backdrop.active {
    display: block;
  }
}

/* -------------------------------------------------------------------------- */
/* CONTEXT-SENSITIVE TOP BAR                                                  */
/* -------------------------------------------------------------------------- */
.context-sensitive-bar {
  position: sticky;
  top: 57px;
  z-index: 95;
  background: rgba(12, 15, 23, 0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-gold);
  padding: 8px 16px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45);
}

.context-bar-inner {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  flex-wrap: wrap;
}

.context-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.context-strip-trigger {
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.3);
  color: var(--gold-bright);
  padding: 5px 9px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  line-height: 1;
  transition: all 0.2s;
}

.context-strip-trigger:hover {
  background: rgba(212, 175, 55, 0.25);
  color: #fff;
}

.context-breadcrumbs {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.86rem;
  color: var(--text-muted);
}

.crumb-root {
  color: var(--gold-soft);
  font-weight: 600;
}

.crumb-separator {
  color: rgba(212, 175, 55, 0.4);
}

.crumb-current {
  color: var(--gold-bright);
  font-weight: 700;
}

.context-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

/* Quick Search Input */
.context-search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.context-search-icon {
  position: absolute;
  left: 10px;
  font-size: 0.82rem;
  color: var(--gold);
  pointer-events: none;
}

.context-search-input {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid var(--border-gold);
  border-radius: 20px;
  padding: 5px 28px 5px 30px;
  font-size: 0.82rem;
  color: var(--text-main);
  width: 170px;
  transition: width 0.25s ease, border-color 0.2s, box-shadow 0.2s;
  outline: none;
  font-family: inherit;
}

.context-search-input:focus {
  width: 240px;
  border-color: var(--gold);
  box-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
}

.context-search-clear {
  position: absolute;
  right: 8px;
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 0.75rem;
  cursor: pointer;
  padding: 2px 4px;
}

/* Font Size & Tool Buttons */
.context-tool-group {
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 2px 6px;
  gap: 4px;
}

.context-tool-btn {
  background: none;
  border: none;
  color: var(--gold-soft);
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 700;
  padding: 3px 6px;
  border-radius: 4px;
  transition: background 0.15s, color 0.15s;
  font-family: inherit;
}

.context-tool-btn:hover {
  background: rgba(212, 175, 55, 0.2);
  color: #fff;
}

.font-scale-indicator {
  font-size: 0.74rem;
  color: var(--amber);
  min-width: 34px;
  text-align: center;
}

.theme-quick-btn {
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid var(--border-gold);
  border-radius: 8px;
  padding: 5px 8px;
}

/* Profile Pill */
.context-profile-pill {
  display: flex;
  align-items: center;
  gap: 7px;
  background: rgba(212, 175, 55, 0.12);
  border: 1px solid rgba(212, 175, 55, 0.35);
  border-radius: 20px;
  padding: 4px 12px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
}

.context-profile-pill:hover {
  background: rgba(212, 175, 55, 0.25);
  border-color: var(--gold);
}

.pill-avatar {
  font-size: 1rem;
}

.pill-name {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--gold-soft);
  max-width: 100px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.pill-badge {
  font-size: 0.7rem;
  background: rgba(212, 175, 55, 0.25);
  color: var(--gold-bright);
  padding: 2px 6px;
  border-radius: 10px;
  font-weight: 600;
}

/* -------------------------------------------------------------------------- */
/* USER PROFILE & PREFERENCES MODAL                                          */
/* -------------------------------------------------------------------------- */
.user-settings-modal {
  position: fixed;
  inset: 0;
  z-index: 1100;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  display: none;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.user-settings-modal.active {
  display: flex;
}

.user-modal-box {
  background: #0d111a;
  border: 1px solid var(--border-gold);
  border-radius: 18px;
  width: 100%;
  max-width: 620px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9), 0 0 35px rgba(212, 175, 55, 0.25);
  overflow: hidden;
  animation: modalScale 0.25s ease;
}

.user-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px;
  background: #131724;
  border-bottom: 1px solid var(--border-gold);
}

.user-modal-tabs {
  display: flex;
  gap: 8px;
}

.user-tab-btn {
  background: none;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  color: var(--text-muted);
  font-size: 0.88rem;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  transition: all 0.2s;
}

.user-tab-btn.active {
  background: rgba(212, 175, 55, 0.18);
  color: var(--gold-bright);
}

.user-modal-close-btn {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid var(--border-subtle);
  color: var(--text-main);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.user-modal-close-btn:hover {
  background: rgba(255, 77, 77, 0.2);
  border-color: #ff6666;
  color: #ffcccc;
}

.user-modal-body {
  padding: 22px 24px;
  overflow-y: auto;
  flex-grow: 1;
}

.user-tab-content {
  display: none;
}

.user-tab-content.active {
  display: block;
}

/* Profile Hero Card */
.profile-hero-card {
  display: flex;
  align-items: center;
  gap: 18px;
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.12), rgba(224, 159, 62, 0.06));
  border: 1px solid var(--border-gold);
  border-radius: 14px;
  padding: 16px 20px;
  margin-bottom: 22px;
}

.profile-avatar-large {
  font-size: 3rem;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(212, 175, 55, 0.2);
  border: 2px solid var(--gold);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.profile-hero-info h3 {
  color: var(--gold-bright);
  font-size: 1.2rem;
  margin-bottom: 4px;
}

.profile-tier-badge {
  display: inline-block;
  font-size: 0.78rem;
  background: rgba(212, 175, 55, 0.2);
  border: 1px solid var(--border-gold);
  color: var(--gold-soft);
  padding: 2px 10px;
  border-radius: 12px;
  font-weight: 600;
}

.profile-streak-line {
  font-size: 0.82rem;
  color: var(--text-muted);
  margin-top: 6px;
}

.profile-streak-line strong {
  color: var(--amber);
}

/* Form Groups in Settings */
.settings-form-group {
  margin-bottom: 20px;
}

.settings-label {
  display: block;
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--gold-soft);
  margin-bottom: 8px;
}

.settings-input,
.settings-select {
  width: 100%;
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid var(--border-gold);
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 0.92rem;
  color: var(--text-main);
  outline: none;
  font-family: inherit;
  transition: border-color 0.2s;
}

.settings-input:focus,
.settings-select:focus {
  border-color: var(--gold-bright);
}

.avatar-selection-grid {
  display: grid;
  grid-template-columns: repeat(9, 1fr);
  gap: 8px;
}

.avatar-option {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 8px 4px;
  font-size: 1.3rem;
  cursor: pointer;
  transition: all 0.15s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-option:hover,
.avatar-option.selected {
  background: rgba(212, 175, 55, 0.25);
  border-color: var(--gold);
  transform: scale(1.1);
}

.radio-pill-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.radio-pill {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.radio-pill:hover {
  background: rgba(212, 175, 55, 0.1);
  border-color: var(--border-gold);
}

.radio-pill input[type="radio"] {
  accent-color: var(--gold);
}

.font-size-slider-row {
  display: flex;
  align-items: center;
  gap: 14px;
  background: rgba(0, 0, 0, 0.3);
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid var(--border-subtle);
}

.slider-font-label {
  font-weight: 700;
  color: var(--gold);
  min-width: 120px;
  text-align: center;
}

.toggle-option-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.toggle-checkbox {
  accent-color: var(--gold);
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.profile-stats-card {
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  padding: 14px 18px;
  margin-top: 18px;
}

.profile-stats-card h4 {
  font-size: 0.9rem;
  color: var(--gold-soft);
  margin-bottom: 12px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.stat-box {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 10px 8px;
  text-align: center;
}

.stat-number {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--gold-bright);
}

.stat-desc {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-top: 2px;
}

.settings-actions-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid var(--border-subtle);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid var(--border-subtle);
  color: var(--text-main);
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 600;
  font-family: inherit;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.15);
}

.btn-primary {
  background: linear-gradient(135deg, var(--gold), #b8860b);
  color: #07080b;
  border: none;
  padding: 8px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.88rem;
  font-weight: 700;
  font-family: inherit;
  transition: all 0.2s;
}

.btn-primary:hover {
  filter: brightness(1.15);
}
"""

for cp in css_paths:
    if os.path.exists(cp):
        with open(cp, 'r', encoding='utf-8') as fp:
            css_text = fp.read()
        
        # Check if already appended
        if '/* LEFT STRIP BAR (SIDEBAR DOCK) */' not in css_text:
            css_text += "\n" + SHELL_CSS
            with open(cp, 'w', encoding='utf-8') as fp:
                fp.write(css_text)
            print(f"Appended shell and settings CSS to: {cp}")
        else:
            print(f"CSS already present in: {cp}")


# --- 2. JS APP SHELL ENGINE ---
SHELL_JS = r'''
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
  const themeRadios = document.getElementsByName('themeChoice');
  themeRadios.forEach(r => { r.checked = (r.value === userPrefs.theme); });
  const fontRadios = document.getElementsByName('fontChoice');
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

  // Insert right below header if present, else top of main
  const header = document.querySelector('header.site-header');
  if (header && header.nextSibling) {
    header.parentNode.insertBefore(contextBar, header.nextSibling);
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
'''

js_paths = ['assets/js/main.js', 'docs/assets/js/main.js', 'site/assets/js/main.js']
for jp in js_paths:
    if os.path.exists(jp):
        with open(jp, 'r', encoding='utf-8') as fp:
            js_text = fp.read()
        
        # Check if already appended
        if '/* GURUKULA APP SHELL: LEFT STRIP' not in js_text:
            js_text += "\n\n" + SHELL_JS
            with open(jp, 'w', encoding='utf-8') as fp:
                fp.write(js_text)
            print(f"Appended shell and settings JS to: {jp}")
        else:
            print(f"JS already present in: {jp}")

print("=== App Shell Integration Complete ===")
