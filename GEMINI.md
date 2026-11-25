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
  4. **Background Execution, Settle Guard & 10x-12x Concurrency**: Wait `2–3s` after `colab upload` before running `colab exec` (avoids proxy ZMQ socket reset `RuntimeError: Connection was lost.`); launch Remotion/FFmpeg detached via `nohup ... > /content/render.log 2>&1 &` at `--concurrency=10..12`. Always inspect `colab exec` stdout for `Traceback`/`AssertionError` + an explicit completion sentinel (`colab exec` returns exit `0` even on remote Python exceptions), and match specific error strings (`status: 404`, `HTTP 404`, `Failed to fetch`, `Error:`) rather than bare `"404"` (which false-positives on `Rendered 404/10008`).
  5. **Active Kernel Heartbeat (`colab exec --timeout 0`) & Session Isolation**: Always snapshot `colab ls` before `colab new` and **never** touch or stop pre-existing sessions. Never pass `--timeout 0` to `colab exec` on silent/detached commands (causes proxy `ReadTimeout`); reserve `--timeout 0` strictly for streaming loops printing log deltas or a `[heartbeat Xs]` line every `<= 10s` on long single-cell GPU runs (`> 15 min`, such as `Wan2.1-FLF2V`) so Colab never idle-reclaims the kernel (`404/401`). Otherwise detach via `nohup` and wait reactively with `schedule` timers.
  6. **Direct Delivery to Google Drive**: Download master MP4 with `colab download -s <session-id> /content/output.mp4 <local-drive-path>`.
  7. **Release Instance**: Release immediately upon download: `colab stop -s <session-id>`.

### 1.5 Official YouTube Channel Network
- **`@guru-kula-desam`** (`UCPqB1A_WzpLJec6q69BOO3Q`): Main long-form Thirukkural & South Indian devotional channel (+ daily 5:30 AM IST literary Tamil editorial Community Posts).
- **`@GuruKulaDesam`**: Primary Shorts channel (நற்செய்கை — Virtuous Shorts, 1 Short/day schedule).
- **`@GuruKulaDesam2`** (`UCGUmNzaV_OUFbsNdHJQtaNQ`): Secondary Shorts channel (நற்பண்பு — Devotional Temples & Sacred Chants, 1 Short/day schedule).
- **`@TamilDailyLife` / `@TamilMusicalStories`** (`UCDdEZ6CPCr6tIzWdDY9mzxg`): Daily Purana & Family Wisdom Storytelling channel — 365-day Diwali-to-Diwali calendar (`2026-11-08`..`2027-11-07`), solo `ShishyanTM` (`4Ti6ecav4G1JU5JkCUn5`) @ `84%` speed (`0.84x`) + studio sitar/guitar `Intro`/`Interlude`/`Background`/`Outro` stems, 24-shot photorealistic canonical cast + in-scene Mode-B 3D kinetic Tamil story waves (`TamilDailyLifeDynamic`), and daily 6:00 AM IST 3-category Community Posts.
- **`@karmicgenie`** (`UCmixCKV4uTv3wIp634IRLXg`): Full-length cinematic wisdom episodes, philosophical theatrical films, and the **26-Film Singularity Chronicles (`2022–2100`, including Annual Episodes `2027–2050`)** organized across canonical playlist buckets (`PLL9vX_C3dLxc` Singularity Chronicles, `PLTadq3TncTFE` Dharma & Life Wisdom, `PLB4tSmh3p9M8` Wisdom Shorts).
- **`@influenzian`** (`UCcJFqC7z0f-ARNcJadKiKpQ`): Long-form Useful Operating Manuals (**1. Mind/Cognitive Models -> 2. Practical AI Workflows -> 3. Behavioral Money & Career Capital**) built with Dark-Slate Blueprint Remotion + OpenReel Video (`v1.2.0`), plus Sports/Gaming Shorts.

### 1.6 Devotional Lyrical Video Standard (Modern Google Flow & Mode B Invariants)
- **Mandatory Use of Asset Folder Lyrics**: Always check the song's asset folder for `*_lyrics.md` or `*.txt` **first** before running Whisper. Use Whisper only for vocal block timestamps, and always map/align the **exact written Tamil lyrics** from the asset file (never raw Whisper transcription text).
- **Mandatory Modern Imagery via Google Flow (`gflow-headless`)**: Never use vintage, faded, or aged illustrations/scans. Background visual assets must be generated using `gflow-headless image t2i --aspect 16:9 --model nano-pro` targeting 16:9 widescreen photorealistic South Indian sacred realism (24K gold kavacham sanctum darshan, glowing brass oil lamps, mountain temple sunrises, divine peacock).
- **Calm Opening & Hybrid `60%`-Speed Optical-Flow Backdrop Standard (`lyrical-video-guide` Mode 3)**:
  - **First 20–28s Are Sacred**: Never open a long-form devotional song with rapid back-to-back `3s` video cuts. Start with calm, meaning-matched `1.00 -> 1.032` zoom images (e.g. spelling-verified South Indian sacred maps checked via `read_file` when opening hymns invoke Southern Shiva/Tamil lands) so listeners absorb opening lyrics cleanly.
  - **Zero Grid Collages & Zero Repetition**: Programmatically reject `2x2`/`3x3` divider-seam collages and assert `len(set(images)) == len(images)` and `len(set(videos)) == len(videos)` (never repeat any image or video clip).
  - **Interleaved `60%`-Speed Optical-Flow Videos + Quintic S-Curve Dissolves**: Slow `3.0s` (`24fps`) motion clips to `60%` (`0.60x` = `5.00s` / `150` frames @ `30fps`) via `tpad=stop_mode=clone:stop_duration=0.20,setpts=PTS/0.60,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1:scd=none` before Lanczos `1080p` upscale, interleave `1` slowed video bridge after every `3–4` images, and pre-synthesize ONE unified `1080p30` H.264 stream (`-g 30 -keyint_min 30 -sc_threshold 0`) on Colab GPU via `lyrical-video-guide/scripts/build_hybrid_smooth_backdrop.py` with C2 quintic S-curve dissolves (`6u^5 - 15u^4 + 10u^3`: `2.0s` image↔image, `1.7s` image↔video).
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


### 1.8 Mandatory Tamil Voiceover (`eleven_v4` @ `84%`) & 4-Stem Studio Music Invariant
- **Mandatory `eleven_v4` Model**: All Tamil ElevenLabs voiceovers (`ShishyanTM` `4Ti6ecav4G1JU5JkCUn5` or fallback `GuruKulaDesam` `Mu63hpI1uigjGMdYVTDr`) **MUST** use `"model_id": "eleven_v4"` at `speed: 0.84` (`84%`). Never use `eleven_multilingual_v2` or any older model.
- **Mandatory 4-Stem Studio Music & Interlude Cadence (`Intro.wav`, `Interlude.wav`, `Background.wav`, `Outro.wav`)**: Every Tamil storytelling, *தல வரலாறு*, and Suddha Bhakti episode **MUST** include all 4 studio music stems from `/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life/` (`Intro.wav` at start, `Interlude.wav` inserted every ~60–90s at natural section/act pauses so there is never a long unbroken narration, `Background.wav` ducked at `-26 dB` behind speech, and `Outro.wav` at the end) with crisp presence EQ on the vocal track. Never ship dry solo voice or unbroken narration without interludes.

---

## 2. Master Table of Consolidated Skills & Runbooks

| Skill / Runbook Name | Primary Target | Key Pipeline & Technologies |
| :--- | :--- | :--- |
| **`lyrical-video-guide`** | Devotional Lyrical Master Films | 3-stage CTC alignment, 3D Kinetic Waves, 4-edge RTA gold spectrum, native video background looping, Colab L4 GPU |
| **`gurukuladesam-video-build`** | Thirukkural Chapter Master Videos | Visual layering v6.0/v6.1, WhisperX + Wav2Vec2 forced alignment, 5-project YouTube API quota rotation pool |
| **`gurukuladesam-shorts-publisher`** | Dedicated Vertical Shorts | 15/75/10 vertical layout, 0s vocal lead (no instrumental delay), 1 Short/day per channel, multi-token upload |
| **`karmic-genie-show`** | The Karmic Genie Show, Singularity Chronicles & Shorts | 7D virtual studio (`pip75`), `ShishyanEN` + *தல வரலாறு* movie stems, Business/Industrial Singularity Chronicles (`2022–2100` -> `PLL9vX_C3dLxc`), `PLTadq3TncTFE` & `PLB4tSmh3p9M8` playlist buckets, Zero-CTA SEO |
| **`karmic-genie-episode-guide`** | Theatrical Karmic Genie & Annual Singularity Films | 14-page screenplay & annual causal-bottleneck architecture (`2027–2050`), `Bala-Rishi` & `Bala-Matha` personas, Colab L4 render & Google Drive delivery (`gdrive:KarmicGenie/`) |
| **`youtube-movie-poster-thumbnail`** | 16:9 v2 `nano-pro` Movie-Poster Thumbnails | 50/50 zoomed-in deity hero + monumental 3D solid-gold Tamil cinema lettering, prompt-hygiene & sandhi rules, mandatory `read_file` visual QA, multi-token + rolling-24h drip uploader |
| **`google-flow`** | AI Visual Asset Generation | `gflow-headless` CLI (`>= 0.103.1`), `--out-file <path>.jpg`, sequential profile lock, backward-`i2i` time-lapse keyframe anchoring (`t2i -> i2i`), character consistency seeds |
| **`agent-desktop`** | Desktop & OS Operation | Accessibility tree navigation, `@ref` snapshot queries, semantic clicks/types, headless GUI execution |
| **`spotify-episode-build`** | Spotify Video Podcasts | Rec.709 colorspace, 1s GOP keyframe cadence, strict audio-video stream duration parity, GCS multipart uploads |
| **`sports-clips-video`** | Sports & Gaming Shorts | 4-5s peak-action clip harvesting, horizontal mirror (hflip), Suno instrumental soundtrack replacement |
| **`meditative-video-guide`** | Global Meditation & Deep Sleep | 432Hz/528Hz ambient mix, binaural audio layer, slow-mo nature & zero-credit `Wan2.1-FLF2V` + `RIFE` `4x` botanical time-lapse visuals, quota-resilient publisher |
| **`flower-bloom-timelapse`** (`tools/flower_bloom_timelapse/`) | Zero-Credit Botanical & Plant-Growth Time-Lapses (`@influenzian` / `@GuruKulaDesam`) | `$0` video-credit backward-`i2i` (`nano-pro` keyframes) + `Comfy-Org/Wan_2.1_ComfyUI_repackaged` (`WanFirstLastFrameToVideo` `fp8_e4m3fn_fast` on Colab L4) + `Practical-RIFE` (`RIFEv4.25` `4x` `--img` mode) + `h264_nvenc` `1080p` `bt709` + Zero-CTA publisher |
| **`story-telling-guide` (`@TamilDailyLife`)** | Daily Tamil Purana & Wisdom Storytelling (`UCDdEZ6CPCr6tIzWdDY9mzxg`) | 365-day Diwali-to-Diwali scripts (Date/Weekday/Tamil Month/Tithi/Nakshatra only, zero clock/bad-time windows), Solo `ShishyanTM` @ `84%` speed + `Intro`/`Interlude`/`Background`/`Outro` studio WAVs, 24-shot photorealistic canonical cast + in-scene 3D Kinetic Tamil waves (`TamilDailyLifeDynamic` on Colab L4), raw CDP `DOM.setFileInputFiles` YouTube Studio publisher |
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
4. **Multi-Project Quota Rotation, Priority Preemption & Zero-Quota CDN Check**:
   - Upload via `/home/shishyan/GuruKulaDesam_Local/thumbnails/upload_target_thumbnails.py` (rotates across OAuth tokens on `quotaExceeded` `50 units/set`), and back up `.jpg` + QA sheets to `gdrive:GuruKulaDesam/Assets/Thumbnails/` via `rclone copy`.
   - For channels hitting YouTube's per-channel **~100 custom thumbnails / rolling 24h cap (`uploadRateLimitExceeded`, HTTP 429)**, enqueue new releases with `"priority": 1` ahead of `"priority": 100` backfills into `verified_v2_upload_queue.json`. Both `sync_verified_thumbnails.py` (`.github/workflows/sync-verified-thumbnails.yml`) and `auto_drip_verified_thumbnails.py` sort deterministically by `(int(priority), -int(views))` and run a **zero-quota live-CDN pixel pre-check** against `i.ytimg.com` (`64x36` RGB `mean_abs_diff < 16.0`) so thumbnails already live on YouTube are marked complete without burning API quota or a rolling-24h upload slot.

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

---

## 6. `@guru-kula-desam` South Indian Temple History Series (V4 Yoga-Stickman Standard)

Canonical production rules for all South Indian Temple & Heritage episodes (`Ep 07+`) on `@guru-kula-desam` (`UCPqB1A_WzpLJec6q69BOO3Q`):

1. **Real Temple Photographs First (`real_photo_beat_ids` in `build_temple_v4_package.py`)**:
   - Harvest verified high-resolution Wikimedia Commons / Wikipedia photographs of the actual temple first for the opening introduction (`INTRO_00` backed by `B01`, plus `B01..B04`) and key architectural beats (`B17`, `B18`), cropped cleanly to `1920x1080` (`frame_real_photo_to_16x9`).
   - Reserve `gflow-headless` `nano2` stills strictly for historical/puranic dramatization scenes, record CC/artist attributions in `work_stickman_v4/real_photo_credits.json`, and cite them in the YouTube description (`0` video credits spent).
2. **Mandatory Place-Prefixed Title & Description-Only Series Branding (`publish_gkd_temple_episode.py`)**:
   - Every title MUST start with the actual Tamil temple place name followed by ` | ` (e.g. `திருவெள்ளறை | 1200 ஆண்டு பழமையான ஸ்வஸ்திக் கிணறு & புண்டரீகாட்சப் பெருமாள் வரலாறு!`) so viewers clearly recognize temple history (not a devotional song).
   - Keep `GuruKulaDesam`, `குருகுலதேசம்`, and episode numbers (`Ep 07`, `அத்தியாயம் 07`) strictly out of the title and inside `description` (`assert_temple_title_format()`).
3. **Mandatory YouTube End Screen with 2 Relevant Videos & Zero Subscribe CTA (`set_gkd_endscreen_cdp.py`)**:
   - Every published episode MUST attach **2 specific non-overlapping `@guru-kula-desam` Video cards** (never a Subscribe button, enforcing strict Zero-CTA) in the final 20 seconds via `set_gkd_endscreen_cdp.py` using cloned Chrome `Profile 2` (`--headless=new` + UA override + `@Guru-Kula-Desam` brand switch on `youtube.com`), reload-verified and screenshotted to `work_stickman_v4/endscreen_verified.png` (`read_file` QA gate).
4. **V4 Audio/Visual Architecture & Zero-CTA Narration**:
   - **Narration Hygiene & Dual-Account ElevenLabs Failover (spoken-text rule)**: Never let the narrator read symbols. Convert dashes (`—`, `–`, `-`), colons, semicolons and brackets in `spoken_tamil` into pauses (commas) before TTS and captions (`sanitize_spoken()` in `build_temple_v4_package.py`). Voice for Tamil voiceovers is ElevenLabs `ShishyanTM` (`4Ti6ecav4G1JU5JkCUn5`) at `84%` speed (`0.84x`), with automatic quota failover to the secondary ElevenLabs account (`ELEVENLABS_FALLBACK_API_KEY` in git-ignored `.env`) using the `GuruKulaDesam` voice (`Mu63hpI1uigjGMdYVTDr`) at the same `84%` speed + crisp presence EQ.
   - **Vocal Clarity & Lead-Over-Interlude Loudness Rule**: Apply crisp presence EQ (`highpass=85Hz`, `-2.2dB @ 240Hz`, `+2.5dB @ 2.8kHz`, `+3.8dB @ 4.2kHz`, `+2.8dB @ 7.2kHz` air shelf) + vocal compression (`3:1`) + active-speech RMS leveling (`~ -15.5 dBFS` in mix) to `ShishyanTM @ 84%` (`read_spoken_beat_crisp_44k`), while keeping `Intro.wav` (`0.36`, `~ -22 dB`), `Interlude.wav` (`0.44`, `~ -26 dB`), `Background.wav` (`0.052`), and `Outro.wav` (`0.55`) comfortably **6–10 dB quieter than spoken voice** so music cues never overpower the narrator.
   - Audio timeline (`delta < 0.02s`): `Intro.wav` (`11.500s`) + ElevenLabs `ShishyanTM` (`4Ti6ecav4G1JU5JkCUn5`, `eleven_v4`, `rubberband tempo=0.84`) + `5× Interlude.wav` (`9.700s`) + `Background.wav` (`0.052` ducked under interludes) + closing Tamil gratitude (`B24` `"உங்கள் பொன்னான நேரத்திற்கு மனமார்ந்த நன்றி... சிவாய நம!"`) + full `Outro.wav` (`108.400s`).
   - Visual overlays rendered on Colab GPU (`render_temple_v4_colab.py`): bottom-left oval-headed Yoga Stickman (`8` poses), top-right Google Flow `@Me` circle badge, top-center 50%-transparent white notch pill (`<temple_name_ta>`), centered borderless captions, subtle upward rain, 4-edge golden RTA waves (`spectrum_30fps.bin`), and bottom-right `GuruKulaDesam.png` watermark.


---

## 7. `@karmicgenie` English `ShishyanEN` Colorful Animated Episode & Crisp Vocal Standard (`Utility_Explainer_Studio`)

Canonical standard for all English colorful 2D storybook animated episodes of **The Karmic Genie Show** (`@karmicgenie` / `UCmixCKV4uTv3wIp634IRLXg`):

1. **Mandatory Ultra-Crisp Studio Condenser Vocal Chain (`ShishyanEN` = `Nk3ySQLp8D2ib5z5sqpT` STRICTLY on `eleven_v4`)**:
   - **STRICT `ShishyanEN`-ONLY LOCK**: Never switch or fall back to any other ElevenLabs voice (`GuruKulaDesam`, etc.). If `ShishyanEN` quota runs low, stop and alert the user rather than changing voices.
   - **ZERO Low-Mid Drone Beds**: Never mix a `110–220 Hz` sine pad/drone under `ShishyanEN`—low-mid boosts add chest warmth/mud and soften consonant articulation.
   - Synthesize via `/v1/text-to-speech/Nk3ySQLp8D2ib5z5sqpT/with-timestamps?output_format=mp3_44100_192` (`stability=0.55`, `similarity_boost=0.86`, `style=0.04`, `use_speaker_boost=True`, caching every `BXX.mp3` + `BXX_align.json` on disk).
   - Process spoken voice through the **Ultra-Crisp Studio Condenser EQ + Fast-Attack 3.5:1 Vocal Compressor** (`scripts/synthesize_shishyan_en_episode.py`):
     ```text
     highpass=f=105:poles=2,
     equalizer=f=220:t=q:w=1.2:g=-4.5,
     equalizer=f=400:t=q:w=1.4:g=-2.0,
     equalizer=f=3200:t=q:w=1.1:g=3.8,
     equalizer=f=5200:t=q:w=1.0:g=5.0,
     treble=g=4.5:f=8000,
     acompressor=threshold=-20dB:ratio=3.5:attack=4:release=65:makeup=3.4,
     alimiter=limit=0.95
     ```
   - **Guru-Kula-Desam தல வரலாறு Movie Soundscape (`cinemaMovieMode: True`)**: Use `/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life/{Intro,Interlude,Background,Outro}.wav` so episodes feel like a theatrical movie rather than nonstop wall-to-wall narration:
     - `Intro.wav` (`10.5s` opening flourish before speech begins),
     - `Interlude.wav` (`7.8s` unspoken musical act bridges between major acts),
     - `Background.wav` (seamlessly looped via `acrossfade=d=2.5` with a `-5 dB` vocal-clarity pocket carved at `2.4 kHz` & `4.5 kHz`, ducked to `0.068` under speech and `0.008` during interludes),
     - `Outro.wav` (`atrim=90.0:103.5` pure instrumental sitar/guitar closing resolution, `13.5s`).
2. **Domain-Matched Imagery, Fixed Single-Region Subtitles (`anchorYPercent: 84`), & Zero-Border Sideways Overlays (`src/KarmicGenieCreatorStage.tsx`)**:
   - **Domain-Matched Visual Realism**: Business, AI, economic, and Technological Singularity episodes MUST use **photorealistic Business & World Industrial Revolution IMAX cinematography** (executive boardrooms, semiconductor fabs, automated container ports, robotic gigafactories, sovereign solar megastructures, precision AgTech — never fairy/nursery cartoons!).
   - **Fixed Single-Region Cinema Subtitles (`top: 84%`)**: Subtitles MUST stay anchored in the exact same lower-center cinema region (`anchorYPercent = 84`, non-overlapping phrase windows) throughout the entire film—never jumping between center/top/bottom!
   - **GLOBAL ZERO-BORDER & SIDEWAYS ~50%-TRANSPARENT OVERLAY RULE**: Never draw solid borders (`border: none`, zero stroke rings), and dock supplementary metaphor cards compactly to the upper-left margin (`left: 42px`, `scale(0.76)`, `rgba(10, 14, 26, 0.48)`) so the central visual scene stays 100% open.
   - Generate seamless full-bleed single-scene 16:9 illustrations via `gflow-headless image t2i --project 6903a151-2a18-4f0d-91b0-53303301d460 --aspect 16:9 --model nano-pro` (rejecting any split-panel divider seams or decorative borders during `read_file` contact-sheet QA).
   - Render on Google Colab GPU (`colab`) with Mode-B 3D gold/ivory kinetic phrases, borderless speech-reactive official `@karmicgenie` circular channel emblem (`assets/logo/official_karmic_genie_channel_logo.png`), and 40%-transparent bottom golden RTA bars.
3. **OAuth & Headless Chrome CDP Publishing, Canonical Playlist Buckets & Mandatory SEO Standard (`scripts/publish_kg_2pct.py`, `scripts/publish_karmicgenie_cdp.py`, `scripts/karmicgenie_seo.py` & `scripts/sync_karmicgenie_playlists_and_seo.py`)**:
   - Primary YouTube Data API v3 OAuth token: `/home/shishyan/GitHub/Shishyan/GuruKulaDesam/data/credentials/token_karmicgenie.json` (verified against `UCmixCKV4uTv3wIp634IRLXg`). When OAuth upload quota is capped or tokens expire, fall back to headless Chrome CDP (`http://127.0.0.1:9225`) targeting `https://studio.youtube.com/channel/UCmixCKV4uTv3wIp634IRLXg?authuser=0` using raw `DOM.setFileInputFiles` for zero-overhead `>100 MB` master MP4 attachment + verified `< 2 MB` `16:9` poster thumbnail, clicking **`Publish anyway`** if YouTube Studio's content-checks modal appears.
   - **Canonical `@karmicgenie` YouTube Playlist & Category Buckets** (auto-synced every 12h in GitHub Actions via `.github/workflows/sync-master-playlists.yml` -> `tools/sync_all_to_master_playlists.py`, and deterministically ordered via `scripts/sync_karmicgenie_playlists_and_seo.py`):
     - **`PLL9vX_C3dLxc` (`The Singularity Chronicles (2022–2100) — World Industrial Revolution & Future Timeline`, `categoryId="28"` Science & Technology)**: Complete chronological series (`World Industrial Revolution 2022–2050` `R3Uj4cLeyW4`, `Technological Singularity 2026–2100` `Su7OdsAoqHs`, all 24 Annual Episodes **`Year 2027` -> `Year 2050`**, plus companion specials `5WY5cCYrO-k` & `t6kTW4S97KE`; consolidated on Drive under `gdrive:KarmicGenie/Singularity_Chronicles_2022_2100/`).
     - **`PLTadq3TncTFE` (`The Karmic Genie Show — Purpose, Dharma & Timeless Life Wisdom`, `categoryId="27"` Education)**: All full-length Dharma, conscience, creator calling, and 7D wisdom episodes.
     - **`PLB4tSmh3p9M8` (`Karmic Genie Shorts — 60-Second Dharma, Purpose & Life Wisdom`, `categoryId="27"` Education)**: All `<= 75s` philosophical & Vedic wisdom Shorts.
     - **ASMR & Meditation Buckets**: `PLR3b7ZaAl3tk` (`ASMR Meditation & Focus` + Zero-Credit Botanical Time-Lapses), `PLWS2fI-SQXv0` (`Rain, Forest & Waterfall`), `PLQFflb-RUYC4` (`Ocean Waves`), `PLfj9WvMqgHiQ` (`432Hz Night Sky`), and `PLAj2jnmSYOus` (`60-Second Sleep & ASMR Shorts`).
   - **Mandatory `@karmicgenie` SEO, Tags, Chapters & Hashtags Standard (`scripts/karmicgenie_seo.py`)**:
     - **Strict Zero-CTA (`assert_zero_cta`) & Pioneer Gratitude**: Zero `"subscribe"`, `"bell"`, `"smash that like"`, or `"leave a comment"` anywhere in titles, descriptions, tags, or channel About profile; honor industrial pioneers without villainizing any company, leader, or worker.
     - **Above-the-Fold 2-Line Search Hook**: Every description opens with a natural, high-intent 2-sentence philosophical & search-keyword hook summarizing the core viewer question or prior-year industrial bottleneck.
     - **Playlist Cross-Links, Prev/Next Navigation + `00:00` Key Chapters**: Automatically embed the canonical Playlist URL (`PLL9vX_C3dLxc` / `PLTadq3TncTFE`), Prev/Next chronological episode links, and `>= 4` timestamped `00:00` YouTube Chapters computed directly from `manifest.json` Act breaks.
     - **Targeted & Viral Hashtags (`<= 12–13` per video, strictly `< 15` YouTube hard limit)**: Combine series/year/topic hashtags (`#Singularity #Year20XX #FutureTimeline #IndustrialRevolution #FutureOfBusiness #VedicWisdom`) with `#TheKarmicGenieShow #KarmicGenie #viral #trending`.
     - **20–27 High-Intent Studio `Tags` (`440–485 / 500` chars)**: Populate topic-extracted keywords first (exact technological breakthroughs, year predictions, Vedic/dharma anchors) followed by brand & viral discovery tags (`apply_tags_in_studio_page` / `yt.videos().update`).
