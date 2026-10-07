# Guru Kula Desam — Architecture & Engineering Manual
### For Software Engineers, AI Agents & Maintainers

This document provides the foundational architecture, invariants, and operational guidelines for Guru Kula Desam. Any developer or autonomous AI agent working on this repository **must** read and adhere to these principles.

---

## 🏛️ Core Architectural Invariants

### 1. The Tri-Folder Rule (CRITICAL)
The site is deployed via GitHub Pages from the `docs/` folder, but identical mirrors exist at the repository root (`./`) and `site/`.
- **Invariant**: Any edit made to an HTML file, `assets/js/main.js`, or `assets/css/style.css` **must exist identically across all three folders**:
  1. Root directory (`./filename.html`)
  2. GitHub Pages directory (`docs/filename.html`)
  3. Staging directory (`site/filename.html`)
- **Automated Sync**: Always run `python tools/sync/sync_trifolder.py --source docs` after making changes to synchronize the tree.
- **Automated Validation**: Always verify zero divergence by running `python tools/sync/validate_integrity.py`.

### 2. Zero-Build Vanilla Web Stack
- The platform uses pure **HTML5, CSS3, and ES6 JavaScript**.
- **No external npm/webpack build step is required**. Opening any HTML file in a local browser or static HTTP server works instantly.
- Scripts must run in modern Evergreen browsers and mobile devices with zero cumulative layout shift (CLS).
- Service worker (`sw.js`) and Web Manifest (`manifest.json`) provide offline caching and PWA functionality.

### 3. Modern Vector SVG Icon System
- **Raw unicode emojis in UI controls, headers, buttons, cards, and badges are strictly prohibited**.
- All icons must use the `.gkd-icon` vector SVG system defined in `assets/css/style.css` and `assets/js/main.js`:
  ```html
  <!-- Standard Inline SVG -->
  <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    ...
  </svg>
  ```
- **Standard Sizing Classes**:
  - `.gkd-icon`: Base responsive icon (`1.15em`, `vertical-align: -0.16em`, inherits `currentColor`).
  - `.strip-item-icon .gkd-icon`: Sidebar top-level item (`1.25rem`).
  - `.strip-sub-icon .gkd-icon`: Sidebar sub-item (`1.05rem`).
  - `.gkd-sub-arrow`: Sub-menu and dropdown chevron arrows (`0.75em`).
- **Dynamic Helper in JS**: In `assets/js/main.js`, always use `getModernIcon(key)` or `GKD_ICONS[key]`.

### 4. Video & Audio Authenticity Standard
- The channel is dedicated to authentic, serene, contemplative Tamil spirituality and Vedic nobility.
- **Rule**: Only use **authentic, original YouTube releases from the Guru Kula Desam channel** (featuring traditional temple scenes, oil lamps, sacred music, and the circular emblem).
- **Prohibited**:
  - Raw local MP4 references (`assets/videos/*.mp4`) in production coursebooks.
  - Multi-shot experimental/rejected video files.
- **Standard YouTube Embed Markup**:
  ```html
  <div class="video-embed-wrapper" style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px;">
    <iframe src="https://www.youtube.com/embed/VIDEO_ID" 
            title="Video Title" 
            loading="lazy" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
            allowfullscreen 
            style="position:absolute; top:0; left:0; width:100%; height:100%; border:none;">
    </iframe>
  </div>
  ```

---

## 🗺️ Page Topology & Routing Map

| File | Scope & Title | Key Features |
| :--- | :--- | :--- |
| `index.html` | Guru Kula Desam Home Gateway | 6 Main Portals, Ashram Daily Clock, Daily Sadhana Tracker |
| `tharam-1.html` | Grade 1 — Early Moral Foundation | Aathichoodi, Ahimsa, Respect for Life, 5 Mahayajnas |
| `tharam-2.html` | Grade 2 — Compassion & Nature | 5 Classical Landscapes (Ainthinai), Animal Welfare, Aruludaimai |
| `tharam-3.html` | Grade 3 — Four Nayanmar Saints | Appar, Sambandar, Sundarar, Manikkavasagar, Devaram |
| `tharam-4.html` | Grade 4 — Forbearance & Truth | Poraiyudaimai, Sathsang, Character Building |
| `tharam-5.html` | Grade 5 — Industry & Energy | Ookkamudaimai, Pancha Bhutas, Temple Sanctum Science |
| `tharam-6.html` | Grade 6 — Relentless Effort | Aazhvinaiyudaimai, Chola Architecture, Thiruvasagam |
| `tharam-7.html` | Grade 7 — Inner Mastery & Tapas | Thirumandiram, Yoga, Meditation, Food Ethics |
| `tharam-8.html` | Grade 8 — Four Ashramas of Life | Brahmacharya, Grihastha (Foundation), Vanaprastha, Sannyasa |
| `tharam-9.html` | Grade 9 — Saiva Agamas & Dialectics | 28 Saiva Agamas, Shaddarshanas (6 Indian Philosophies) |
| `tharam-10.html`| Grade 10 — Discretion & Leadership | Therinthu Thelithal, Deliberation in Action, Citizen Ethics |
| `tharam-11.html`| Grade 11 — Truth Realization | Meyyunarthal, Governance (*Sengonmai*), Ministership |
| `tharam-12.html`| Grade 12 — Sovereignty & Mukti | Iraimaatchi, Sivagnana Bodham, Non-killing (*Kollaamai*) |
| `thirukkural.html` | Thirukkural Hub & Cinema Lounge | 1330 Couplets, 20-Chapter Illaraviyal Full Film Player |
| `saiva-neri.html` | Saiva Neri Hub | Panniru Thirumurai, 63 Nayanmars, Agamic Worship |
| `sanmargam.html` | Suddha Sanmargam Hub | Vallalar, Thiru Arutpa, Jyothi Worship, Jivakarunyam |
| `kalvi.html` | Kalvi Vidya Hub | 12 Life Stages, Grade Matrix, WBS Curriculum Map |
| `school.html` | Ashram School & Daily Routine | Brahma Muhurtham, Pomodoro Study Timer, 5 Mahayajnas |
| `higher-studies.html`| Higher Studies & Research | B.A., M.A., Ph.D. syllabus across Indian universities |
| `virtues.html` | Character & Virtue Registry | Alphabetical virtues, daily sadhana reflection cards |
| `classes.html` | Classes & Timetable Portal | Schedule, live satsang timings, teacher resources |
| `about.html` | About the Mission | Founders, lineage, sacred vision, cultural heritage |
| `help.html` | Help & Student Support | FAQ, user guide, technical support, theme preferences |
| `youtube.html` | YouTube Video Archive | 580+ categorized spiritual films, bhajans, discourses |
| `review_quality.html` | QA Screening Room | Production screening lounge for video pipeline verification |
| `google-site.html` | Google Sites Migration Portal | Sync point with legacy Google Sites classroom |
| `irai-isai-virundhu.html` | Sacred Music Lounge | 5 Amrita compositions, pann research, audio player |
| `murugan.html` | Kaumaram Tradition | Thiruppugazh, Kandar Anubhuti, Skanda Sashti |
| `sakthi.html` | Shakta Tradition | Abhirami Anthadhi, Lalitha Sahasranama |
| `vaishnava.html` | Vaishnava Tradition | Nalayira Divya Prabandham, Thiruppavai, Gita |
| `vinayagar.html` | Ganesha Worship | Vinayagar Agaval, Mudakaratha Modakam |

---

## ⚙️ Component Architecture (`assets/js/main.js`)

1. **Context-Sensitive Top Bar (`renderContextTabsIntoHeader`)**:
   - Detects the current page and injects context-specific quick navigation pills.
   - Includes a primary hamburger button, search bar (hotkey: `/`), font scaler (`A-` / `A+`), tanpura drone player, theme toggle, and student profile pill.
2. **Left Strip Sidebar (`toggleLeftStrip`)**:
   - Slide-out drawer with 6 primary spiritual categories and nested expandable trees.
   - Accessible via keyboard, click outside to close, or toggle icon.
3. **Student Profile & Settings Modal (`userSettingsModal`)**:
   - Stored in `localStorage` under `gkd_user_profile` and `gkd_user_preferences`.
   - Allows students to select their spiritual learning tier (Grades 1-4, 5-8, 9-12), theme appearance, and font preference.
4. **Tanpura Drone Generator (`toggleAmbientDrone`)**:
   - Synthesizes a calming 432Hz ambient Indian tanpura drone directly in Web Audio API.

---

## 🛠️ Tooling & Directory Guide

```
tools/
├── sync/
│   ├── sync_trifolder.py       # Mirror docs/ to ./ and site/
│   └── validate_integrity.py   # Run 5-point automated health audit
├── curriculum/                 # Generators for syllabus, courses, and diagrams
├── youtube/                    # Metadata tools, title standardizers, and upload tools
├── colab/                      # High-resolution GPU rendering notebooks
└── maintenance/                # Shell updaters, sidebars, and QA scripts
```

### Standard Operating Procedure for Updates

When making any change:
```bash
# 1. Edit the target files in docs/ (or root)
# 2. Run Tri-Folder Sync to propagate changes identically
python tools/sync/sync_trifolder.py --source docs

# 3. Run Automated Integrity Audit
python tools/sync/validate_integrity.py

# 4. Verify clean git status
git status
```
