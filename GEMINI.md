# Global Gemini & Guru Kula Desam Unified Master Runbook (GEMINI.md)
> **Canonical Single Source of Truth**: Consolidated reference for all Antigravity and Gemini agents across all Guru Kula Desam, Karmic Genie, and Influenzian productions.
> **DO NOT DUPLICATE**: Instead of creating fragmented skill files or duplicate guides across directories, keep all production standards, core rules, channel IDs, rendering standards, and pipeline blueprints updated directly in this document.

---

## 1. Global Core Rules & Invariants

### 1.1 Clickable Links Only (Google Drive)
- When sharing any file, script, or video for user review, upload it to Google Drive via `rclone copy` and provide the clickable `https://drive.google.com/...` URL from `rclone link` (never rely on `file://` links alone, as they are not clickable in the chat UI).

### 1.2 Zero-Distraction Headless Execution
- **Mandatory Headless Google Flow (`gflow-headless`)**: Always use `gflow-headless` (never `gflow`) for all Google Flow image and video generation (`gflow-headless image t2i`, `gflow-headless video t2v`, etc.) so no visible browser window ever pops up or steals focus.
- **Background Desktop Automation**: All desktop/GUI automation must use `agent-desktop` cleanly in the background without stealing window focus.

### 1.3 Default Computer Use: `agent-desktop`
- Whenever desktop application operation, UI navigation, GUI automation, clicking, typing into system apps, or window management is requested, use **`agent-desktop`** as the default computer-use tool.
- Prioritize native accessibility tree interaction (`snapshot`, `find`, `get`, `is`, semantic `click`, `type`, `press`) using stable `@ref` IDs over blind visual pixel coordinate guessing.
- Run `agent-desktop skills get desktop` or `agent-desktop skills get platform` when operating desktop applications.

### 1.4 Mandatory Cloud GPU Rendering & Whisper Policy — Colab CLI (`colab`)
- **Zero Local Master Video Renders & Zero Local Whisper**: Never run full video rendering jobs (`remotion render`, long FFmpeg master compositions, etc.) or Whisper/forced-alignment transcription locally on the workstation. Local workstation resources are strictly reserved for code alignment, script checks, and sub-second test stills (`remotion still ... --gl=angle`).
- **Colab CLI for All Video Renders & Whisper**: Dispatch all video rendering and all Whisper / forced-alignment tasks to cloud GPU instances via Colab CLI (`colab` / `/home/shishyan/GuruKulaDesam_Local/.venv/bin/colab`).
- **Standard Cloud GPU Workflow & Prerequisites**:
  1. **Provision session**: `colab new --gpu l4` (or `a100`/`t4`).
  2. **TAMIL FONTS ARE MANDATORY (Hard Requirement)**:
     A Colab VM has no Tamil font by default. Without system fonts, every Tamil letter renders as an empty tofu box. Defense-in-depth requires:
     - Project-bundled `public/fonts/NotoSansTamil-*.ttf` loaded via `src/TamilFontLoader.tsx` (`loadTamilFonts()`).
     - System fonts installed in their **own** dedicated apt call and verified via `fc-list`:
       ```bash
       apt-get update -qq
       DEBIAN_FRONTEND=noninteractive apt-get install -y -qq fonts-noto-core fonts-taml fonts-indic fonts-deva fonts-noto-cjk fonts-noto-hinted
       fc-cache -f -v
       fc-list :lang=ta family | grep -i tamil || { echo "FATAL: no Tamil font"; exit 1; }
       ```
     - Chromium libraries installed in a separate call: `libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpangocairo-1.0-0 libxshmfence1 libasound2t64`.
     - Render a proof still on Colab (`remotion still ...`) and inspect the frame via `read_file` to verify Tamil glyphs before starting full render.
  3. **Lean Code Transfer**: Create a targeted `.tar.gz` omitting `node_modules`, `.git`, `out`, and large raw video stems; upload via `colab upload -s <session-id> <archive.tar.gz> /content/<archive.tar.gz>`, extract, and run `npm ci --prefer-offline`.
  4. **Background Execution & 10x-12x Hardware Concurrency**: Launch Remotion detached with `nohup` using 10x-12x parallel concurrency on Colab L4 (`nohup ./node_modules/.bin/remotion render <CompId> /content/output.mp4 --gl=angle --concurrency=12 > /content/render.log 2>&1 &`).
  5. **Direct Delivery to Google Drive**: Download master MP4 with `colab download -s <session-id> /content/output.mp4 <local-drive-path>`.
  6. **Release Instance**: Release immediately upon download: `colab stop -s <session-id>`.

### 1.5 Official YouTube Channel Network
- **`@guru-kula-desam`** (`UCPqB1A_WzpLJec6q69BOO3Q`): Main long-form Thirukkural & South Indian devotional channel.
- **`@GuruKulaDesam`**: Primary Shorts channel (நற்செய்கை — Virtuous Shorts, 1 Short/day schedule).
- **`@GuruKulaDesam2`** (`UCGUmNzaV_OUFbsNdHJQtaNQ`): Secondary Shorts channel (நற்பண்பு — Devotional Temples & Sacred Chants, 1 Short/day schedule).
- **`@karmicgenie`** (`UCmixCKV4uTv3wIp634IRLXg`): Full-length cinematic wisdom episodes & philosophical theatrical films.
- **`@influenzian`**: Sports & gaming high-adrenaline Shorts.

### 1.6 Devotional Lyrical Video Standard (Modern Google Flow & Mode B Invariants)
- **Mandatory Use of Asset Folder Lyrics**: Always check the song's asset folder for `*_lyrics.md` or `*.txt` **first** before running Whisper. Use Whisper only for vocal block timestamps, and always map/align the **exact written Tamil lyrics** from the asset file (never raw Whisper transcription text).
- **Mandatory Modern Imagery via Google Flow (`gflow-headless`)**: Never use vintage, faded, or aged illustrations/scans. Background visual assets must be generated using `gflow-headless image t2i --aspect 16:9 --model nano-pro` targeting 16:9 widescreen photorealistic South Indian sacred realism (24K gold kavacham sanctum darshan, glowing brass oil lamps, mountain temple sunrises, divine peacock).
- **Exact Top Notch Pill Title Matching**: The top white notch pill must strictly display the current song title (e.g. `திருப்புகழ்: <பாடல் பெயர்>`), with 50% glass transparency (`rgba(255, 255, 255, 0.50)` + `backdropFilter: blur(10px)`). Never leave titles from previous songs or templates.
- **Continuous Mode B 3D Letter Undulating Waves**: All Tamil lyrics must animate using Mode B grapheme-level continuous acoustic synchronization with 24K multi-layer gold extrusion, sine-wave undulations, dynamic vocal crest leaps (+75px Z-pop), and natural cubic gravity drop exits.
- **4-Edge RTA Golden Spectrum Bars**: 40%-transparent golden thin spectrum bars along all four edges (<= 18% bottom, <= 9% top, <= 5.4% left/right) driven by 30fps RTA telemetry binaries. Always verify the `.bin` spectrum file is passed/loaded with zero 404 errors in Remotion logs.
- **Brand Watermark**: The channel avatar (`GuruKulaDesam.png`) must always be anchored in the bottom-right corner.

### 1.7 Remote Agent Skills Synchronization
- Remote agents running outside the local workstation can instantly sync the full suite of production skills and templates via:
  ```bash
  # Option A: Clone/pull from GitHub repository
  git clone https://github.com/shishyan/AI-Prompt-Skills.git ~/.gemini/skills/

  # Option B: Direct curl/gdrive download from Google Drive Master Bundle (ID: 1-xp4eLnH-z6cz4XXxI3Bsr6euy0dkBBF)
  gdrive readonly download 1-xp4eLnH-z6cz4XXxI3Bsr6euy0dkBBF --out /tmp/agent_skills_master.tar.gz && mkdir -p ~/.gemini/skills && tar -xzf /tmp/agent_skills_master.tar.gz -C ~/.gemini/skills/
  ```

---

## 2. Master Table of Consolidated Skills & Runbooks

| Skill / Runbook Name | Primary Target | Key Pipeline & Technologies |
| :--- | :--- | :--- |
| **`lyrical-video-guide`** | Devotional Lyrical Master Films | 3-stage CTC alignment, 3D Kinetic Waves, 4-edge RTA gold spectrum, native video background looping, Colab L4 GPU |
| **`gurukuladesam-video-build`** | Thirukkural Chapter Master Videos | Visual layering v6.0/v6.1, WhisperX + Wav2Vec2 forced alignment, 5-project YouTube API quota rotation pool |
| **`gurukuladesam-shorts-publisher`** | Dedicated Vertical Shorts | 15/75/10 vertical layout, 0s vocal lead (no instrumental delay), 1 Short/day per channel, multi-token upload |
| **`karmic-genie-show`** | The Karmic Genie Show & Shorts | 7D virtual studio, 75% story / 25% studio composite, @Me ivory bandhgala persona, 2-line news crawl, theme interludes |
| **`karmic-genie-episode-guide`** | Theatrical Karmic Genie Films | 14-page screenplay format, Bala-Rishi & Bala-Matha personas, Google Flow ULTRA cinematography, L4 render delivery |
| **`youtube-movie-poster-thumbnail`** | 16:9 v2 `nano-pro` Movie-Poster Thumbnails | 50/50 zoomed-in deity hero + monumental 3D solid-gold Tamil cinema lettering, prompt-hygiene & sandhi rules, mandatory `read_file` visual QA, multi-token + rolling-24h drip uploader |
| **`google-flow`** | AI Visual Asset Generation | `gflow-headless` CLI (`>= 0.103.1`), `--out-file`, text-to-image (t2i), text-to-video (t2v), character consistency seeds |
| **`agent-desktop`** | Desktop & OS Operation | Accessibility tree navigation, `@ref` snapshot queries, semantic clicks/types, headless GUI execution |
| **`spotify-episode-build`** | Spotify Video Podcasts | Rec.709 colorspace, 1s GOP keyframe cadence, strict audio-video stream duration parity, GCS multipart uploads |
| **`sports-clips-video`** | Sports & Gaming Shorts | 4-5s peak-action clip harvesting, horizontal mirror (hflip), Suno instrumental soundtrack replacement |
| **`meditative-video-guide`** | Global Meditation & Deep Sleep | 432Hz/528Hz ambient mix, binaural audio layer, seamless hour-long visual loop, quota-resilient publisher |

---

## 3. Canonical v2 Movie-Poster YouTube Thumbnail Standard (`youtube-movie-poster-thumbnail`)

Treat every long-form devotional, wisdom, or storytelling video as an **epic theatrical motion picture** (`~/.gemini/config/skills/youtube-movie-poster-thumbnail/SKILL.md`):

1. **50/50 Full-Bleed Theatrical Architecture**:
   - **Half A (Right 50%)**: **Zoomed-in chest-up/waist-up active Deity or Sage hero** (`45%–55%` of frame) in a narrative posture matched to the song/chapter meaning, lit with warm golden rim-lighting.
   - **Half B (Left 50%)**: **Two-tier monumental Tamil cinema typography**—dark midnight-indigo top pill badge (`1–2` Tamil words, zero quotation marks) + gigantic 3D-extruded solid polished gold Tamil lettering (`1–3` crisp Tamil words) on a royal crimson-maroon velvet banner.
   - **UI Safe Zone**: Seamless full-bleed background with **no text or numbers in the lower-right corner** for YouTube's duration badge.
2. **Mandatory CLI, Model & Prompt-Hygiene Rules (`95–100%` First-Pass Tamil Accuracy)**:
   - Always run `gflow-headless image t2i ... --aspect 16:9 --model nano-pro --out-file <path>.jpg` (`gflow-cli >= 0.103.1`; never `nano2`; never `-o` which selects format; single sequential process per profile lock).
   - **Banned Prompt Tokens**: Never write literal `"24K"` or `"16:9"` inside prompt text (prevents badge text leaks); never write `"completely blank"` (prevents white/black corner cutouts); always specify `pure poster artwork with zero UI buttons or play icons` (prevents fake red YouTube play icons).
   - **Tamil Sandhi & Single-Word Guards**: Split long sandhi-joined compound words into 2 space-separated words (`நெஞ்சு அறிவு`, `சிற்றினம் சேராமை`, `மெய் உணர்தல்`, `அருட்பெருஞ் சோதி`); prefer pure Tamil (`திருமகள்`) over complex Grantha (`லக்ஷ்மி`); for 1-word titles (`கேள்வி`, `தூது`, `ஊழ்`), specify `single-line Tamil cinema lettering <WORD> (written once cleanly)`.
3. **Mandatory Visual QA Gate Before Upload**:
   - Never blindly upload generated Tamil posters. Inspect every poster (or 2-column `1280px` high-res QA contact sheet) via `read_file` for exact Tamil spelling, zero UI/quote artifacts, and `< 2 MB` file size; regenerate any catch immediately.
4. **Multi-Project Quota Rotation & Rolling-24h Channel Rate-Limit Workflow**:
   - Upload via `/home/shishyan/GuruKulaDesam_Local/thumbnails/upload_target_thumbnails.py` (rotates across OAuth tokens on `quotaExceeded` `50 units/set`), and back up `.jpg` + QA sheets to `gdrive:GuruKulaDesam/Assets/Thumbnails/` via `rclone copy`.
   - For bulk backfills exceeding YouTube's per-channel **~100 custom thumbnails / rolling 24h cap (`uploadRateLimitExceeded`, HTTP 429)**, stage verified IDs sorted by views descending into `verified_v2_upload_queue.json` and let `auto_drip_verified_thumbnails.py` (or `.github/workflows/sync-verified-thumbnails.yml`) drain ~100/day automatically.
