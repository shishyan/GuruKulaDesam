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
  5. **Active Kernel Heartbeat (`colab exec --timeout 0`) & Session Isolation**: Always snapshot `colab sessions` before `colab new -s <name>` and **never** touch or stop pre-existing sessions. For long GPU diffusion/video runs (`> 15 min`, such as `Wan2.1-FLF2V`), never leave the Jupyter kernel `idle` behind a bare `nohup` — Colab's idle-kernel reaper reclaims idle kernels after ~20–25 min (`404/401`). Instead, wrap the worker inside a streaming `colab exec -s <name> --timeout 0` loop printing log deltas or a `[heartbeat Xs]` line every 10s until completion so the kernel stays `busy`.
  6. **Direct Delivery to Google Drive**: Download master MP4 with `colab download -s <session-id> /content/output.mp4 <local-drive-path>`.
  7. **Release Instance**: Release immediately upon download: `colab stop -s <session-id>`.

### 1.5 Official YouTube Channel Network
- **`@guru-kula-desam`** (`UCPqB1A_WzpLJec6q69BOO3Q`): Main long-form Thirukkural & South Indian devotional channel (+ daily 5:30 AM IST literary Tamil editorial Community Posts).
- **`@GuruKulaDesam`**: Primary Shorts channel (நற்செய்கை — Virtuous Shorts, 1 Short/day schedule).
- **`@GuruKulaDesam2`** (`UCGUmNzaV_OUFbsNdHJQtaNQ`): Secondary Shorts channel (நற்பண்பு — Devotional Temples & Sacred Chants, 1 Short/day schedule).
- **`@TamilDailyLife` / `@TamilMusicalStories`** (`UCDdEZ6CPCr6tIzWdDY9mzxg`): Daily Purana & Family Wisdom Storytelling channel — 365-day Diwali-to-Diwali calendar (`2026-11-08`..`2027-11-07`), solo `ShishyanPro` (`6fJYxeFW7wEpPJADYKSZ`) @ `80%` speed (`0.80x`) + studio sitar/guitar `Intro`/`Interlude`/`Background`/`Outro` stems, 24-shot photorealistic canonical cast + in-scene Mode-B 3D kinetic Tamil story waves (`TamilDailyLifeDynamic`), and daily 6:00 AM IST 3-category Community Posts.
- **`@karmicgenie`** (`UCmixCKV4uTv3wIp634IRLXg`): Full-length cinematic wisdom episodes & philosophical theatrical films.
- **`@influenzian`** (`UCcJFqC7z0f-ARNcJadKiKpQ`): Long-form Useful Operating Manuals (**1. Mind/Cognitive Models -> 2. Practical AI Workflows -> 3. Behavioral Money & Career Capital**) built with Dark-Slate Blueprint Remotion + OpenReel Video (`v1.2.0`), plus Sports/Gaming Shorts.

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
| **`google-flow`** | AI Visual Asset Generation | `gflow-headless` CLI (`>= 0.103.1`), `--out-file <path>.jpg`, sequential profile lock, backward-`i2i` time-lapse keyframe anchoring (`t2i -> i2i`), character consistency seeds |
| **`agent-desktop`** | Desktop & OS Operation | Accessibility tree navigation, `@ref` snapshot queries, semantic clicks/types, headless GUI execution |
| **`spotify-episode-build`** | Spotify Video Podcasts | Rec.709 colorspace, 1s GOP keyframe cadence, strict audio-video stream duration parity, GCS multipart uploads |
| **`sports-clips-video`** | Sports & Gaming Shorts | 4-5s peak-action clip harvesting, horizontal mirror (hflip), Suno instrumental soundtrack replacement |
| **`meditative-video-guide`** | Global Meditation & Deep Sleep | 432Hz/528Hz ambient mix, binaural audio layer, slow-mo nature & zero-credit `Wan2.1-FLF2V` + `RIFE` `4x` botanical time-lapse visuals, quota-resilient publisher |
| **`flower-bloom-timelapse`** (`tools/flower_bloom_timelapse/`) | Zero-Credit Botanical & Plant-Growth Time-Lapses (`@influenzian` / `@GuruKulaDesam`) | `$0` video-credit backward-`i2i` (`nano-pro` keyframes) + `Comfy-Org/Wan_2.1_ComfyUI_repackaged` (`WanFirstLastFrameToVideo` `fp8_e4m3fn_fast` on Colab L4) + `Practical-RIFE` (`RIFEv4.25` `4x` `--img` mode) + `h264_nvenc` `1080p` `bt709` + Zero-CTA publisher |
| **`story-telling-guide` (`@TamilDailyLife`)** | Daily Tamil Purana & Wisdom Storytelling (`UCDdEZ6CPCr6tIzWdDY9mzxg`) | 365-day Diwali-to-Diwali scripts (Date/Weekday/Tamil Month/Tithi/Nakshatra only, zero clock/bad-time windows), Solo `ShishyanPro` @ `80%` speed + `Intro`/`Interlude`/`Background`/`Outro` studio WAVs, 24-shot photorealistic canonical cast + in-scene 3D Kinetic Tamil waves (`TamilDailyLifeDynamic` on Colab L4), raw CDP `DOM.setFileInputFiles` YouTube Studio publisher |
| **`Utility_Explainer_Studio` (`@influenzian`)** | Long-Form Colorful Paper-Billions Storytelling (`Mind -> AI -> Money` & Future Timelines) | Vibrant Uncluttered Paper-Billions 2D Cartoon Engine (`PaperBillionsBeatStage.tsx`, `Influenzian-PaperStory-16x9`) + OpenReel Video (`v1.2.0` `.openreel.json`), Free `kokoro-onnx` TTS + CUDA `faster-whisper` written-token sync, Colab `--gpu t4 --high-mem` (or `l4`), Zero HUD Clutter & Zero CTA |

---

## 4. `@influenzian` Colorful Paper-Billions Storytelling Standard (`/home/shishyan/GitHub/Influenzian/Utility_Explainer_Studio/`)

1. **STRICT ZERO-CTA INVARIANT (NEVER Violate)**:
   - **NEVER ask viewers to subscribe, like, comment, share, follow, or hit the notification bell** anywhere in spoken narration, on-screen text, titles, or YouTube descriptions. Let pure storytelling & utility earn organic return viewers; automated code assertions (`assert_zero_cta`) enforce this across all manifests and publishers.
2. **Vibrant, Uncluttered Paper-Billions Visual Engine (`PaperBillionsBeatStage.tsx` / `Influenzian-PaperStory-16x9`)**:
   - **NEVER render dark grey/black slide decks or permanent top/bottom HUD banners/footnotes.**
   - **100% Full-Bleed Vibrant Color**: Warm, saturated 2D paper-cut cartoon illustrations (golden ambers, teal skies, coral highlights, lush emerald greens) with tactile push-ins, whip-pans, and soft ambient floating particles.
   - **Zero Clutter — Transient Stamps Only When Spoken**: Year stamps (`YEAR 2026`, `YEAR 2032`, `YEAR 2050`) and punch callouts (`$0 ELECTRICITY`) appear **only for ~2 seconds at the exact beat moment** and immediately exit, keeping 100% of the canvas clean and focused on the visual story alongside a crisp single-line karaoke caption pill.
3. **3 Daily Categories -> 3 Distinct Audiences (`influenzian-daily-3category.yml`) + 20-Tries 1M Viral Challenge**:
   - **Category 1 (`MIND` · 12:00 PM IST / `06:30 UTC`)**: *Audience A — Knowledge Workers, Builders & Strategic Thinkers* (`am_michael` voice).
   - **Category 2 (`AI_WORKFLOW` · 07:00 PM IST / `13:30 UTC`)**: *Audience B — Engineers, Builders & Technical AI Operators* (`am_adam` voice).
   - **Category 3 (`MONEY` · 01:00 AM IST / `19:30 UTC`)**: *Audience C — Working Professionals, Families & Long-Term Investors* (`am_fenrir` voice).
4. **Zero-Cost Cloud Stack, Dual Output & GitHub Actions Autonomy**:
   - Voice + Sync + Render on **Colab GPU** (`colab new --gpu t4 --high-mem` 8-core when `tdlw1..3` hold L4 slots, or `l4`): `kokoro-onnx` (`v1.0`, `$0/video`) + pre-decoded `16kHz float32` `faster-whisper` + `remotion render Influenzian-PaperStory-16x9 --gl=angle --concurrency=8`.
   - Every build exports both the `1080p` master `.mp4` AND an **OpenReel Video `v1.2.0` `.openreel.json` multi-track project**, plus a vibrant 16:9 cartoon poster, staged to `gdrive:Influenzian/DailyQueue/<CATEGORY>/` and `gdrive:Influenzian/Viral_20_Tries/`, and published daily by `.github/workflows/influenzian-daily-3category.yml` (`tools/influenzian_daily_3category_publisher.py`).

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

---

## 5. Zero-Credit Botanical Blooming & Full Plant-Growth Time-Lapse Standard (`tools/flower_bloom_timelapse/`)

Canonical zero-`gflow-video`-credit workflow proven on both a 4-stage Sacred Pink Lotus bloom (`4oio027kKpo`) and a 5-stage Dwarf Golden Sunflower seed-to-bloom growth film (`kzhVTKOo4f8`):

1. **`$0` Video-Credit Backward-`i2i` Keyframe Locking (`gflow-headless image` `nano-pro`)**:
   - Generate the **final** full-grown / full-bloom frame first via `gflow-headless image t2i --profile nagaraj957 --aspect 16:9 --model nano-pro --out-file stage_0N.jpg` (`gflow-cli` writes `.jpg` natively for `nano-pro`; never pass `-o` which sets text format `id|json|table`; run strictly one sequential process per profile lock; ban `"16:9"`, `"24K"`, and `"completely blank"` from prompts).
   - Frame the entire compact plant from the dark moist soil mound + flanking optical anchors (e.g., two small mossy stones on left/right edges) up to top woodland headroom, and inspect `stage_0N.jpg` via `read_file` before stepping backward.
   - Step **backward** sequentially via `gflow-headless image i2i --ref <next_stage>.jpg` down to the newborn sprout or tightly closed bud (`stage_05 -> 04 -> 03 -> 02 -> 01`), keeping the soil mound, stones, stem emergence coordinate, and lighting locked, and pass a mandatory `read_file` Visual QA Gate across all keyframes before provisioning Colab.
2. **Cloud GPU Diffusion (`Comfy-Org/Wan_2.1_ComfyUI_repackaged` FP8-Fast — `22.96 GB` total)**:
   - Provision a dedicated Colab L4 session (`colab new -s plant2 --gpu l4`) after snapshotting `colab sessions` (leaving other active sessions untouched) and run the worker inside a live streaming `colab exec --timeout 0` heartbeat loop (`10s` log/heartbeat updates so Colab never idle-reclaims the kernel).
   - Download the 4 split files via `aria2c -x 16 -s 16`: `wan2.1_flf2v_720p_14B_fp8_e4m3fn.safetensors` (`15.27 GB`), `umt5_xxl_fp8_e4m3fn_scaled.safetensors` (`6.27 GB`), `clip_vision_h.safetensors` (`1.18 GB`), and `wan_2.1_vae.safetensors` (`0.24 GB`).
   - Run core ComfyUI node `WanFirstLastFrameToVideo` (`832x480`, `length=49` × 4 segments for 5-stage plant growth or `length=65` × 3 segments for 4-stage bloom → `193` stitched frames, `steps=16`, `cfg=5.0`, `sampler_name="uni_pc"`, `scheduler="simple"`, `ModelSamplingSD3 shift=8.0`) using `UNETLoader weight_dtype="fp8_e4m3fn_fast"` on NVIDIA L4 (`CC >= 8.9`, ~455s/segment, with automatic `"fp8_e4m3fn"` fallback).
3. **`4x` Neural Optical-Flow & `1080p` Mastering (`Practical-RIFE` `RIFEv4.25` + `h264_nvenc` Rec.709)**:
   - Deduplicate segment boundary frames (`193` continuous PNGs) and run `Practical-RIFE` (`r3gm/RIFE` `RIFEv4.25_0919.zip`) in `--img` PNG mode (guard `import skvideo.io` in `try/except` for `numpy 2.x` compatibility) with `--exp=2` (`193 -> 769` lossless frames = `25.63s` @ `30fps`; automatic FFmpeg `minterpolate` fallback).
   - Upscale via Lanczos + `cas=0.3` to `1920x1080` `h264_nvenc` High Profile (`bt709`), mux trimmed `48kHz` stereo ambient studio WAV (`audio_dur <= video_dur - 0.05s`, 1.5s fade-in / 2.5s fade-out), verify `ffprobe` + multi-panel QA sheet via `read_file`, immediately `colab stop -s <name>`, sync deliverables to `gdrive:GuruKulaDesam/Samples/`, and publish via `publish_timelapse_youtube.py` (`assert_zero_cta`, channel-ID check, isolated thumbnail `try/except` so a `403` never re-uploads a duplicate video).
4. **Companion Zero-Credit Modes**:
   - **Method 2 (Real 4K CC0 Macro + `RIFE` Slow-Mo)**: Harvest studio intervalometer macro blooms from Pexels, Pixabay, and Wikimedia Commons (`Category:Time-lapse videos of flowers`), retime `4x` via `RIFEv4.25`, apply a uniform Rec.709 color LUT, and mix `48kHz` ambient audio (`meditative-video-guide/SKILL.md`).
   - **Method 3 (Headless Blender 4.x `Geometry Nodes`)**: Procedural `137.508°` Fibonacci phyllotaxis flower driven by `growth ∈ [0, 1]` with subsurface-scattered backlit petals and an orbiting macro camera rendered headlessly (`blender -b -P bloom.py -a`) on Colab L4 Cycles/OptiX.
