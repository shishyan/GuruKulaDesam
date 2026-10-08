# Guru Kula Desam (குரு குல தேசம்)
### Sacred Tamil Heritage, Vedic Wisdom & Character Education Platform

Guru Kula Desam is a comprehensive spiritual, cultural, and moral education platform bridging classical Tamil scriptures (Thirukkural, Thevaram, Thiruvasagam, Thiru Arutpa, Bhagavad Gita, Upanishads) with 21st-century digital learning.

---

## 🌟 Quick Overview

- **12 Comprehensive Grade Books (`tharam-1.html` – `tharam-12.html`)**: Covering early childhood morals to advanced Saiva Siddhanta, Vedantic metaphysics, and householder leadership (*Illara Dharmam*).
- **Core Spiritual Portals**:
  - `thirukkural.html` — All 1330 couplets with the 20-chapter Illaraviyal Cinema Lounge.
  - `saiva-neri.html`, `sakthi.html`, `murugan.html`, `vinayagar.html`, `vaishnava.html` — Sacred hymn repositories.
  - `sanmargam.html` — Vallalar Ramalinga Swamigal's compassionate Suddha Sanmargam.
  - `kalvi.html` & `school.html` — Complete curriculum, 4 ashramas of life, and daily ashram routines.
  - `higher-studies.html` — Undergraduate, postgraduate, and doctoral research syllabus.
  - `virtues.html` — Comprehensive registry of spiritual virtues and moral benchmarks.
  - `youtube.html` — Categorized archive of all official YouTube releases.
- **Authentic Video & Audio Integration**: Hooked directly into the channel's contemplative, meditative original YouTube releases.
- **Modern Professional SVG Iconography**: Zero raw emojis in UI; 100% scalable, accessible vector SVGs.
- **Progressive Web App (PWA)**: Offline-first caching with `sw.js` and `manifest.json`.

---

## 📁 Repository Directory Structure

```
Gurukuladesam/
├── [Root Web Pages]              # Active website HTML files (32 pages + 9 embeds)
│   ├── index.html                # Main gateway portal
│   ├── tharam-1.html .. 12.html  # 12 Gurukulam Coursebooks
│   ├── thirukkural.html          # Thirukkural Cinema Lounge & Scripture Hub
│   ├── saiva-neri.html, ...      # Core spiritual tradition portals
│   ├── manifest.json, sw.js      # Progressive Web App service worker
│   ├── README.md                 # Project overview and quickstart
│   └── ARCHITECTURE.md           # Engineering & AI Agent operational guide
│
├── assets/                       # Static front-end assets
│   ├── css/style.css             # Main stylesheet & modern SVG icon system
│   ├── js/main.js                # Context tabs, hamburger, search, modal engine
│   └── images/                   # Sacred classical paintings & diagrams
│
├── docs/                         # GitHub Pages production mirror (byte-for-byte with root)
├── site/                         # Staging / local test mirror (byte-for-byte with root)
│
├── tools/                        # Categorized Engineering Utilities
│   ├── sync/                     # Tri-folder synchronization & integrity validators
│   │   ├── sync_trifolder.py     # 1-command parity synchronizer
│   │   └── validate_integrity.py # Automated 5-point health check
│   ├── curriculum/               # Curriculum builders, WBS enrichers & diagram engines
│   ├── youtube/                  # YouTube API metadata sync, title tools & cataloging
│   ├── colab/                    # GPU notebooks & sacred artwork ingestion pipelines
│   └── maintenance/              # Site generators, shell patchers & QA auditors
│
├── data/                         # Data Catalogs, Archives & Manifests
│   ├── catalogs/                 # Master site catalog (site_catalog.json)
│   ├── credentials/              # API keys & OAuth credentials (gitignored)
│   ├── dumps/                    # Title updates, analysis CSVs & text manifests
│   └── archive/                  # Legacy scraped HTML pages
│
└── production/                   # High-resolution video generation & motion pipelines
    ├── visuals/                  # Master chapter visuals & paintings
    ├── scripts/                  # Video compilation scripts
    └── review/                   # Screening room & quality control scripts
```

---

## 🚀 Key Commands & Maintenance

### 1. Run Complete Site Health Check
```bash
python tools/sync/validate_integrity.py
```
Validates:
- 100% byte-for-byte parity across `./`, `docs/`, and `site/`.
- JavaScript syntax via `node -c` (zero errors).
- Zero broken internal page links or asset paths.
- Video embed integrity (0 unauthorized local video tags).
- Modern SVG icon compliance.

### 2. Synchronize Tri-Folders (Root, Docs, Site)
```bash
# Sync from docs/ to root and site/
python tools/sync/sync_trifolder.py --source docs

# Or check pending updates without applying
python tools/sync/sync_trifolder.py --dry-run
```

---

## 🤖 Guide for AI Agents

- **Architectural Principles & Front-End Guidelines**: See [ARCHITECTURE.md](ARCHITECTURE.md).
- **YouTube Automation, Quota Management & Scripture Invariants**: See [AI_AGENT_INTEGRATION_MANUAL.md](AI_AGENT_INTEGRATION_MANUAL.md).

