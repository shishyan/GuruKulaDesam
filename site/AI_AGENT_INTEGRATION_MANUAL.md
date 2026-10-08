# Guru Kula Desam (@guru-kula-desam) — AI Agent Integration Manual & System Architecture
### The Definitive Technical Playbook for Autonomous AI Agents & Lead Engineers
*Document Version: 2.0 | Last Updated: October 2026 | Platform: Guru Kula Desam*

---

## 📖 Table of Contents
1. [Mission, Vision & Platform Philosophy](#1-mission-vision--platform-philosophy)
2. [Core Architectural Invariants](#2-core-architectural-invariants)
   - [The Tri-Folder Mirror Invariant (CRITICAL)](#the-tri-folder-mirror-invariant-critical)
   - [Zero-Build Vanilla Web Architecture](#zero-build-vanilla-web-architecture)
   - [Modern SVG Vector Icon System](#modern-svg-vector-icon-system)
   - [Catalog Parity & Cryptographic Invariants](#catalog-parity--cryptographic-invariants)
3. [YouTube Data API v3 Automation & Live Studio Integration](#3-youtube-data-api-v3-automation--live-studio-integration)
   - [Authentication & OAuth 2.0 Credential Lifecycle](#authentication--oauth-20-credential-lifecycle)
   - [YouTube Daily Quota Mechanics & Economic Budgeting](#youtube-daily-quota-mechanics--economic-budgeting)
   - [Channel Direct Uploads vs. DistroKid Topic Audios](#channel-direct-uploads-vs-distrokid-topic-audios)
   - [Recency-Prioritized Queue Architecture](#recency-prioritized-queue-architecture)
4. [Canonical Scripture Naming Convention Specification](#4-canonical-scripture-naming-convention-specification)
   - [The Canonical Title Formula](#the-canonical-title-formula)
   - [Strict Length Constraint (< 95 Chars)](#strict-length-constraint--95-chars)
   - [Scripture-First Ordering Principle](#scripture-first-ordering-principle)
   - [Disambiguation Engine & Recursive Prefix Stripping](#disambiguation-engine--recursive-prefix-stripping)
   - [Complete Sacred Corpus Classification Registry](#complete-sacred-corpus-classification-registry)
5. [Data Catalog Architecture & Synchronization](#5-data-catalog-architecture--synchronization)
   - [Master Data Files (`master_all_598_songs_catalog.*`)](#master-data-files)
   - [Web Frontend Catalogs (`catalog.json` & `catalog.js`)](#web-frontend-catalogs)
   - [The Tri-Folder Parity Pipeline](#the-tri-folder-parity-pipeline)
6. [Visual & Media Asset Production Guidelines](#6-visual--media-asset-production-guidelines)
   - [Sacred Visual Aesthetic Standards](#sacred-visual-aesthetic-standards)
   - [Asset Directory Taxonomy](#asset-directory-taxonomy)
7. [Step-by-Step AI Agent Operational Runbooks](#7-step-by-step-ai-agent-operational-runbooks)
   - [Runbook A: Executing Daily YouTube Title Updates](#runbook-a-executing-daily-youtube-title-updates)
   - [Runbook B: Regenerating & Validating Scripture Catalogs](#runbook-b-regenerating--validating-scripture-catalogs)
   - [Runbook C: Ingesting New Songs or Video Chapters](#runbook-c-ingesting-new-songs-or-video-chapters)
   - [Runbook D: Synchronizing the Tri-Folder Tree](#runbook-d-synchronizing-the-tri-folder-tree)
   - [Runbook E: Git Branch Parity & Safe Pushing](#runbook-e-git-branch-parity--safe-pushing)
8. [Developer Pitfalls & Troubleshooting Matrix](#8-developer-pitfalls--troubleshooting-matrix)

---

## 1. Mission, Vision & Platform Philosophy

**Guru Kula Desam (@guru-kula-desam)** is an authentic, non-commercial digital gurukulam dedicated to preserving and propagating classical Tamil spirituality, Vedic nobility, and virtuous character education.

### Architectural Core Values:
1. **Purity of Presentation**: Contemplative, sacred, and serene. No pop-ups, no tracking advertisements, no distracting sensory overload.
2. **Reverence for Scripture**: Tamil scriptures (Thirukkural, Thevaram, Thiruvasagam, Thiruvarutpa, Thiruppugazh, etc.) are sacred literature. Every hymn must be identified accurately by its origin work and author.
3. **Bilingual Accessibility**: Every title and catalog entry provides both native Tamil script and international English transliteration so that youth and seekers worldwide can learn.
4. **Deterministic Engineering**: All tooling, synchronization scripts, and integrity checkers are deterministic, idempotent, and self-auditing.

---

## 2. Core Architectural Invariants

### The Tri-Folder Mirror Invariant (CRITICAL)
The live production website is hosted on **GitHub Pages**, which serves directly from the `docs/` folder. However, for local development, test servers, and staging, two identical mirrors exist at the repository root (`./`) and `site/`.

```
Gurukuladesam/
├── [Root Web Pages]       # Mirror 1: Local HTTP test server root
├── docs/                  # Mirror 2: GitHub Pages production deployment root
└── site/                  # Mirror 3: Staging & sandbox test environment
```

> [!IMPORTANT]
> **The Golden Tri-Folder Invariant**:
> Every web page (`.html`), script (`assets/js/main.js`), stylesheet (`assets/css/style.css`), and catalog asset (`assets/data/*`) **must maintain 100% SHA-256 byte-for-byte parity across all three locations (`./`, `docs/`, `site/`)**.
> 
> Never commit a change to `docs/` without mirroring it to `./` and `site/`, or vice-versa.

#### Automated Tri-Folder Synchronization:
```bash
# Propagate changes from docs/ to root and site/
python tools/sync/sync_trifolder.py --source docs

# Validate 5-point integrity and zero divergence
python tools/sync/validate_integrity.py
```

### Zero-Build Vanilla Web Architecture
- Built on modern **HTML5, CSS3, and ES6 JavaScript**.
- **No Node.js/npm bundling or webpack compile steps are required**. Opening any HTML file in a local browser or through Python's `http.server` works immediately.
- Offline-first caching is enabled by the Service Worker (`sw.js`) and Web Application Manifest (`manifest.json`).

### Modern SVG Vector Icon System
- **Raw unicode emojis in UI controls, action buttons, cards, and badges are strictly prohibited**.
- All UI icons utilize the `.gkd-icon` SVG vector architecture declared in `assets/css/style.css` and `assets/js/main.js`.
- Always use `getModernIcon(key)` or `<svg class="gkd-icon">...</svg>` in HTML markup.

### Catalog Parity & Cryptographic Invariants
All data catalogs:
- `master_all_598_songs_catalog.json`
- `master_all_598_songs_catalog.csv`
- `assets/data/catalog.json`
- `assets/data/catalog.js`
must have identical SHA-256 hashes across `assets/data/`, `site/assets/data/`, and `docs/assets/data/`. `build_clean_scripture_mapping.py` automatically asserts this cryptographic parity upon each execution.

---

## 3. YouTube Data API v3 Automation & Live Studio Integration

### Authentication & OAuth 2.0 Credential Lifecycle
The platform updates the official channel `@guru-kula-desam` via Google YouTube Data API v3.

- **Client Secrets**: `data/credentials/client_secrets.json` (Google Cloud OAuth 2.0 Desktop Client).
- **Authorized Token**: `data/credentials/token.json` (stores refresh token and active access token).
- **Scope**: `https://www.googleapis.com/auth/youtube.force-ssl` (enables updating video snippets, titles, and playlists).
- **Token Refresh**: Handled automatically in Python by `google.oauth2.credentials.Credentials`. If expired, it auto-refreshes using `google.auth.transport.requests.Request()` and writes the renewed token back to disk.

```python
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file("data/credentials/token.json", SCOPES)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
    with open("data/credentials/token.json", "w") as f:
        f.write(creds.to_json())
youtube = build("youtube", "v3", credentials=creds)
```

> [!CAUTION]
> Both `client_secrets.json` and `token.json` reside inside the gitignored `data/credentials/` directory. **Never remove them from `.gitignore` or push credentials to remote GitHub repositories.**

---

### YouTube Daily Quota Mechanics & Economic Budgeting

Google Cloud enforces a hard daily quota budget on YouTube Data API v3:
- **Daily Quota Ceiling**: **10,000 units per project**.
- **Operation Costs**:
  - `videos().list(part="snippet", id="id1,id2,...")`: **1 quota unit** (batches up to 50 video IDs per request).
  - `videos().update(part="snippet", body=...)`: **50 quota units** per video updated.
  - `playlistItems().list(...)`: **1 quota unit** per 50 items.
- **Maximum Daily Update Capacity**:
  $$\frac{10,000 \text{ units}}{50 \text{ units/update}} \approx 200 \text{ video updates per 24 hours}$$
- **Daily Quota Reset Window**:
  - **UTC**: 07:00 UTC (Midnight Pacific Time / PT).
  - **IST (India)**: **12:30 PM IST** (Winter) / **12:30 PM IST** (Summer).

#### Cost-Optimized Idempotent Execution:
Before sending a `videos().update()` call, the script reads snippets in batches of 50 (1 unit cost) and tests:
```python
if current_title == target_title:
    skip_count += 1
    continue  # Consumes 0 update quota!
```
This ensures already-updated videos cost **zero** update units, preserving 100% of the day's quota for pending videos.

---

### Channel Direct Uploads vs. DistroKid Topic Audios

The 600+ audio-visual library consists of two fundamentally distinct categories:

| Category | Typical Count | Host Channel | API Update Capability | Storage / Sync Method |
| :--- | :--- | :--- | :--- | :--- |
| **Direct Channel Uploads** | **~317 videos** | `@guru-kula-desam` | **Full API Update** (`videos().update`) | Synchronized live to YouTube Studio via OAuth. |
| **DistroKid Auto-Generated Audios** | **~286 tracks** | *YouTube Music Topic Channel* | **Read-Only** (Hosted by YouTube Music) | Maintained in master JSON/CSV & web catalogs (`catalog.json`, `catalog.js`). |

> [!NOTE]
> DistroKid topic tracks are uploaded to YouTube Music's automated CDN under artistic distribution licenses. Attempting to update a DistroKid video ID via the channel's OAuth credentials will return HTTP 404/403 because it belongs to the Topic channel, not `@guru-kula-desam`. Our scripts automatically detect and segregate these tracks.

---

### Recency-Prioritized Queue Architecture
To maximize channel impact, the pending queue `channel_direct_uploads_pending.json` is strictly ordered by **upload recency**:
1. It queries the channel's uploads playlist (`ch_resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]`).
2. It fetches all 317 channel video IDs in reverse-chronological order (newest upload first).
3. The latest Thirukkural master films (Chapters 45, 44, 42, 40, 39, 31, 30, etc.) sit at the very top of the queue, ensuring any visitor to `@guru-kula-desam` sees standardized titles immediately.

---

## 4. Canonical Scripture Naming Convention Specification

### The Canonical Title Formula
Every title must conform to the following bilingual template:
$$\text{[Tamil Scripture/Corpus]}: \text{[Hymn / Chapter Name]} \mid \text{[English Scripture]}: \text{[English Name]} \text{ [Descriptor]}$$

#### Canonical Title Examples:
- `திருக்குறள்: அதிகாரம் 45 - பெரியாரைத் துணைக்கோடல் (Remix) | Periyarai Thunaikodal [Remix]`
- `திருக்குறள்: அதிகாரம் 39 - இறைமாட்சி | Thirukkural: Irai Maatchi [Film]`
- `தேவாரம்: கடவுளைக் கடலுள் எழு (திருக்குறுந்தொகை) | Thevaram: Kadavulai Kadalul Ezhu [Film]`
- `திருவாசகம்: அச்சோப் பதிகம் | Thiruvasagam: Achcho Pathigam [Film]`
- `திருவருட்பா: தோடுடையார் | Thiruvarutpa: Thodudaiyaar [Film]`
- `திருப்புகழ்: கைத்தல நிறைகனி | Thiruppugazh: Kaithala Niraigani [Film]`
- `கந்தர் அலங்காரம்: நாள் என் செய்யும் | Kandhar Alangaram: Naal En Seyyum [Film]`
- `நாம சங்கீர்த்தனம்: நமச்சிவாய சங்கீர்த்தனம் | Namasivaya Sankeerthanam [Film]`
- `தேசிய கீதம்: ஜன கண மன | National Anthem: Jana Gana Mana [Film]`

---

### Strict Length Constraint ($\le 95$ Chars)
- YouTube enforces a hard ceiling of 100 characters per video title.
- **Guru Kula Desam Standard**: **Strictly $\le 95$ characters** (leaving a 5-character buffer to prevent truncation in search and mobile cards).
- Fallback truncation logic in `build_clean_scripture_mapping.py` gracefully shortens the English sub-title if necessary, preserving 100% of the Tamil scripture title and descriptor.

---

### Scripture-First Ordering Principle
The title **must start with where the work belongs**:
- `திருவாசகம்: சிவபுராணம் ...` *(NOT: `சிவபுராணம் | திருவாசகம்`)*
- `தேவாரம்: மாசில் வீணையும் ...` *(NOT: `மாசில் வீணையும் | அப்பர் தேவாரம்`)*
- `திருக்குறள்: அதிகாரம் 1 - கடவுள் வாழ்த்து ...` *(NOT: `கடவுள் வாழ்த்து | திருக்குறள்`)*

---

### Disambiguation Engine & Recursive Prefix Stripping
Legacy video titles frequently contained repetitive prefixes or generic labels such as `சிவ பக்திப் பாடல்: பக்திப் பாடல்: ...` or `பக்திப் பாடல்: திருவருட்பா: ...`.

`build_clean_scripture_mapping.py` implements a **Recursive Prefix Sanitizer**:
```python
def strip_all_prefixes(tam_str, eng_str):
    t = tam_str.strip()
    while True:
        sub = re.sub(prefix_pat, "", t, flags=re.IGNORECASE).strip()
        if sub == t: break
        t = sub
    e = eng_str.strip()
    while True:
        sub = re.sub(eng_prefix_pat, "", e, flags=re.IGNORECASE).strip()
        if sub == e: break
        e = sub
    return t, e
```
This eliminates all double colons and ensures that each title receives exactly one clean scripture prefix.

---

### Complete Sacred Corpus Classification Registry

| Scripture / Origin Corpus | Tamil Origin Prefix | English Origin Prefix | Key Works / Poets |
| :--- | :--- | :--- | :--- |
| **Thirukkural** | `திருக்குறள்` | `Thirukkural` | திருவள்ளுவர் (1330 குறள்கள் / 133 அதிகாரங்கள்) |
| **Thiruvasagam** | `திருவாசகம்` | `Thiruvasagam` | மாணிக்கவாசகப் பெருமான் (சிவபுராணம், அச்சோ, திருவெம்பாவை) |
| **Thevaram** | `தேவாரம்` | `Thevaram` | அப்பர், திருஞானசம்பந்தர், சுந்தரமூர்த்தி நாயனார் |
| **Thiruvarutpa** | `திருவருட்பா` | `Thiruvarutpa` | திருவருட்பிரகாச வள்ளலார் (ஆறாம் திருமுறை, அருட்பெருஞ்சோதி) |
| **Thiruppugazh** | `திருப்புகழ்` | `Thiruppugazh` | அருணகிரிநாதர் (கைத்தல நிறைகனி, நாத விந்துகள்) |
| **Kandhar Alangaram** | `கந்தர் அலங்காரம்` | `Kandhar Alangaram` | அருணகிரிநாதர் (நாள் என் செய்யும்) |
| **Kandhar Anuboothi** | `கந்தர் அநுபூதி` | `Kandhar Anuboothi` | அருணகிரிநாதர் (உருவாய் அருவாய்) |
| **Kandha Sashti** | `கந்த சஷ்டி கவசம்` | `Kandha Sashti Kavasam` | பாலதேவராய சுவாமிகள் |
| **Kandha Puranam** | `கந்த புராணம்` | `Kandha Puranam` | கச்சியப்ப சிவாச்சாரியார் (வான் முகில் வழாது பெய்க) |
| **Thiruppavai** | `திருப்பாவை` | `Thiruppavai` | சூடிக்கொடுத்த சுடர்க்கொடி ஆண்டாள் (மார்கழித் திங்கள்) |
| **Periyazhvar Thirumozhi**| `பெரியாழ்வார் திருமொழி` | `Periyazhvar Thirumozhi`| பெரியாழ்வார் (கண்ணன் தாலாட்டு) |
| **Periyapuranam** | `பெரியபுராணம்` | `Periyapuranam` | சேக்கிழார் பெருமான் (தில்லை வாழ் அந்தணர், உலகெலாம்) |
| **Panniru Thirumurai** | `பன்னிரு திருமுறை` | `Panniru Thirumurai` | சேந்தனார் (திருப்பல்லாண்டு), திருவிசைப்பா |
| **Thirumanthiram** | `திருமந்திரம்` | `Thirumanthiram` | திருமூல நாயனார் (ஒன்றே குலமும் ஒருவனே தேவனும்) |
| **Abhirami Andhadhi** | `அபிராமி அந்தாதி` | `Abhirami Andhadhi` | அபிராமி பட்டர் (தனந்தரும் கல்விதரும்) |
| **Vinayagar Nanmanimalai**| `விநாயகர் நான்மணிமாலை` | `Vinayagar Nanmanimalai` | கபிலதேவர் (பாலும் தெளிதேனும்) |
| **Vinayagar Agaval** | `விநாயகர் அகவல்` | `Vinayagar Agaval` | ஔவையார் |
| **Adi Shankara** | `ஆதிசங்கரர்` | `Adi Shankara` | மகா கணேச பஞ்சரத்னம், வேதஸார சிவ ஸ்தோத்திரம் |
| **Bharathiyar** | `பாரதியார்` | `Bharathiyar` | மகாகவி பாரதியார் (தாயின் மணிக்கொடி பாரீர்) |
| **Pazhamozhi Naanooru** | `பழமொழி நானூறு` | `Pazhamozhi Naanooru` | முன்றுறை அரையனார் (கோயிலாகநல்) |
| **Shiva Namavali** | `சிவ நாமாவளி` | `Shiva Namavali` | ஆதி யோகீஸ்வரர், ஈஸ்வர நாமவளி |
| **Nama Sankeerthanam** | `நாம சங்கீர்த்தனம்` | `Nama Sankeerthanam` | நமச்சிவாய ஸங்கீர்த்தனம், ராம நாம சங்கீர்த்தனம் |
| **Tamil Thai Vazhthu** | `தமிழ்த்தாய் வாழ்த்து` | `Tamil Thai Vazhthu` | மனோன்மணீயம் சுந்தரனார் (நீராரும் கடலுடுத்த) |
| **National Anthem** | `தேசிய கீதம்` | `National Anthem` | ரவீந்திரநாத் தாகூர் (ஜன கண மன) |
| **Philosophical Song** | `தத்துவப் பாடல்` | `Philosophical Song` | சம்சாரம் என்பது வீணை |
| **Ambient / Meditation** | `இசைத் தியானம்` | `Ambient Meditation` | ஆலய நாதம், இன்டர்ஸ்டெல்லார் |

---

## 5. Data Catalog Architecture & Synchronization

```
                                  build_clean_scripture_mapping.py
                                                 │
            ┌────────────────────────────────────┴────────────────────────────────────┐
            ▼                                                                         ▼
master_all_598_songs_catalog.json / .csv                               channel_direct_uploads_pending.json
            │                                                                         │
            ├───────────────┬───────────────┐                                         │
            ▼               ▼               ▼                                         ▼
      assets/data/    site/assets/data/ docs/assets/data/               update_youtube_channel_titles.py --live
            │               │               │                                         │
    (100% SHA-256)   (100% SHA-256)   (100% SHA-256)                                  ▼
                                                                           Live YouTube Studio API
```

### Master Data Files
- `master_all_598_songs_catalog.json` (604 items): The single source of truth containing Video ID, Canonical Title, Scripture Source, Tamil Title, English Title, Descriptor, Genre, Track Type, Author, Source Scripture, and YouTube URLs.
- `master_all_598_songs_catalog.csv`: High-performance flat spreadsheet export for archival analysis.

### Web Frontend Catalogs
- `assets/data/catalog.json`: Object-keyed catalog categorized into 8 genres (`thirukkural`, `shiva`, `murugan`, `vaishnava`, `amman`, `vinayagar`, `vallalar`, `cultural`).
- `assets/data/catalog.js`: Injects `window.GKD_SITE_CATALOG` globally for offline-ready vanilla frontend pages.

---

## 6. Visual & Media Asset Production Guidelines

### Sacred Visual Aesthetic Standards
Guru Kula Desam's visual imagery is grounded in ancient Dravidian temple architecture, classical Tanjore iconography, and reverent Vedic traditions.

- **Mandatory Elements**:
  - Warm stone temple pillars, carved granite gopurams.
  - Traditional brass oil lamps (*kuthuvilakku*), deepams, and gentle agarbaththi smoke.
  - Sacred ashes (*vibhuti*), kumkumam, rudraksha malas, and saffron/ochre cotton vastras.
  - Serene contemplative expressions, respectful gestures (*anjali mudra*), olai palm-leaf manuscripts.
- **Strictly Forbidden Elements**:
  - Hyper-stylized neon fantasy lighting, distorted anatomy, or comic aesthetics.
  - Distracting watermarks or third-party studio logos.
  - Any secular or commercial imagery.

### Asset Directory Taxonomy
Visual art for Thirukkural chapters is organized under:
`production/visuals/thirukkural/<chapter_number>-<slug>/`
- Format: `<seq_number>-n<kural_number>_<description_slug>.jpg` (e.g., `01-n01_listening_to_the_elder_sage.jpg`).

---

## 7. Step-by-Step AI Agent Operational Runbooks

### Runbook A: Executing Daily YouTube Title Updates
When the daily quota resets (12:30 PM IST / 07:00 UTC):
```bash
# Step 1: Ensure UTF-8 execution and run dry-run simulation
python update_youtube_channel_titles.py --dry-run

# Step 2: Execute live updates (runs until daily 10,000 quota limit)
python -u update_youtube_channel_titles.py --live

# Step 3: Inspect live title verification on top channel videos
python -X utf8 -c "from update_youtube_channel_titles import get_authenticated_service; yt=get_authenticated_service(); res=yt.videos().list(part='snippet', id='aZ830iKkqBs,zzJZkyX1GL4').execute(); [print(i['snippet']['title']) for i in res['items']]"
```

### Runbook B: Regenerating & Validating Scripture Catalogs
```bash
# Step 1: Execute scripture resolution and parity replication
python build_clean_scripture_mapping.py

# Step 2: Verify zero double colons or invalid formats
python -X utf8 -c "import json; m=json.load(open('master_all_598_songs_catalog.json', encoding='utf-8')); assert all(len(x['canonical_title']) <= 95 for x in m); print('All titles <= 95 chars validated!')"
```

### Runbook C: Ingesting New Songs or Video Chapters
1. Add new items to `master_all_598_songs_catalog.json`.
2. Map specific hymn keywords in `SPECIFIC_EXACT` inside `build_clean_scripture_mapping.py`.
3. Re-run `python build_clean_scripture_mapping.py`.
4. Run `python tools/sync/sync_trifolder.py --source docs`.
5. Run `python tools/sync/validate_integrity.py`.

### Runbook D: Synchronizing the Tri-Folder Tree
Whenever modifying any HTML, JS, CSS, or data files:
```bash
# 1. Sync all three mirrors
python tools/sync/sync_trifolder.py --source docs

# 2. Run the 5-point automated integrity suite
python tools/sync/validate_integrity.py
```

### Runbook E: Git Branch Parity & Safe Pushing
Always push to both `origin/main` and `origin/master`:
```bash
git add assets/ site/ assets/ docs/ assets/ master_all_598_songs_catalog.* channel_direct_uploads_pending.json
git commit -m "feat(youtube): update live titles and sync master catalogs"
git push origin main
git push origin main:master
```

---

## 8. Developer Pitfalls & Troubleshooting Matrix

| Issue / Symptom | Root Cause | Permanent Resolution |
| :--- | :--- | :--- |
| `UnicodeEncodeError: 'charmap' codec can't encode characters` in PowerShell | Windows PowerShell defaults to `cp1252` encoding when streaming Tamil UTF-8. | Always launch Python with `-X utf8` or add `sys.stdout.reconfigure(encoding="utf-8")` at script entry. |
| Background tasks hang or produce buffered output | Python buffers stdout when run without an interactive TTY. | Use `python -u ...` and add `sys.stdout.reconfigure(line_buffering=True)`. |
| YouTube API returns `quotaExceeded` (HTTP 403) | Daily 10,000 quota units exhausted for the 24h cycle. | Wait until 12:30 PM IST / 07:00 UTC for automatic reset. The queue saves progress; re-running picks up without penalty. |
| Inconsistencies between local and GitHub Pages site | Changes made only in `./` or `site/` without syncing `docs/`. | Always run `python tools/sync/sync_trifolder.py --source docs` and check with `validate_integrity.py`. |
| Git rejects push or warns of untracked credentials | Attempting to stage `data/credentials/` or `data/dumps/`. | Keep credentials and raw dumps in `.gitignore`. Only stage core scripts and catalog manifests. |
| Duplicate title prefixes (e.g. `பக்திப் பாடல்: பக்திப் பாடல்:`) | Title passed through multiple non-stripping regex passes. | Use `strip_all_prefixes()` in `build_clean_scripture_mapping.py` to iteratively strip all tags. |

---

*Authored by Antigravity AI Engineering for Guru Kula Desam. Dedicated to Truth, Virtue, and Eternal Knowledge.*
