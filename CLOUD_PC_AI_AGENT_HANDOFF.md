# CLOUD PC AI AGENT HANDOFF: THIRUKKURAL 133 CINEMATIC DEVOTIONAL MASTER FILMS

**Date / Timestamp:** 2026-10-16  
**Channel:** [@guru-kula-desam](https://www.youtube.com/@guru-kula-desam) ("குரு குல தேசம்")  
**Target YouTube Playlist:** `PLW7qBZp_Q8Ro`  
**Repository:** `https://github.com/shishyan/GuruKulaDesam.git` (branch: `main`)  
**Mission:** Produce, verify, and publish all 133 Thirukkural chapter master films as **PRIVATE** drafts to YouTube strictly adhering to the **Chapter 3 Gold Master Quality Standard** and the **7-Part Chronological Narrative Progression**.

---

## 1. THE NON-NEGOTIABLE ARTISTIC & CINEMATIC SPECIFICATIONS

Every video produced **MUST** follow these exact rules without exception:

### A. Authentic Dravidian Temple Visuals (Strictly NO Generic / Pastoral Imagery)
- **Settings:** Vivid, newly renovated South Indian Dravidian temples (Maha Kumbabishekam standard).
- **Features:** Towering brightly repainted Gopurams with colourful crisp stucco deities, gleaming gold kalasams, clean whitewashed prakaram walls with red-and-white kavi stripes, polished granite courtyards, brass kuthuvilakku oil lamps, camphor aarti flames, devotees in festive traditional silk sarees / veshtis.
- **Forbidden:** No cows, thatched huts, muddy village lanes, dilapidated/mossy ruins, or generic family portrait slideshows.

### B. Upward Divine Drizzle Mist (100% Upward Floating Only)
- **Asset:** `production/upward_divine_drizzle_loop.mp4` (blended at `0.45` screen opacity).
- **CRITICAL:** **STRICTLY NO DOWNWARD RAIN.** Downward rain was the legacy flaw in older releases. Droplets must float upward like sacred mist/divine grace.
- **Negative Emotion Exception:** Chapters dealing with intense negative emotions or enmity (e.g., Chapters **86, 87, 88, 89, 93, 94**) must **omit drizzle entirely** to preserve sombre mood.

### C. Sacred Dhoopa & Lamp Overlay
- **Asset:** `production/sacred_lamp_dhoopa_overlay_1280x720.png` (auto-healed from embedded base64 in `tools/sacred_overlay_data.py`).
- Placed on the frame with subtle alpha blend.

### D. Native 720p 24fps Broadcast Assembly
- 4-way cinematic camera moves (Pan Left $\to$ Right, Pan Right $\to$ Left, Slow Push, Slow Pull).
- 1.0s smooth cross-dissolve (`xfade=transition=fade:duration=1.0`) between every scene.
- Audio: 256k AAC, 48kHz, with a 2.0s gentle audio fade-out at the tail.

---

## 2. THE 7-PART CHRONOLOGICAL NARRATIVE PROGRESSION (LYRICS-TIED)

Do **NOT** shuffle random images back and forth. Every video must tell a coherent story rooted in the chapter's specific 10 couplets and the song's musical progression:

1. **Part 1 (0:00 - ~0:35): The Worldly Dilemma / Setting**  
   The human problem or circumstance requiring this virtue (e.g. disputes in the marketplace, injustice, carelessness of speech, suffering of greed).
2. **Part 2 (~0:35 - ~1:10): The Core Principle Introduced**  
   The saintly insight / righteous teaching revealed (e.g. the balanced scale of justice, the restraint of the tongue, the debt of gratitude).
3. **Part 3 (~1:10 - ~1:45): The Contrast (Moral Friction)**  
   Wrong action vs. Right action; the consequences of straying vs. the steadfast courage to stand in truth.
4. **Part 4 (~1:45 - ~2:20): Practical Dharma in Action**  
   Living the virtue in family life, community, commerce, and daily duty.
5. **Part 5 (~2:20 - ~3:00): Inner Metamorphosis & Moral Dignity**  
   The spiritual elevation of the character; calm conscience, dignity, resilience in adversity.
6. **Part 6 (~3:00 - ~3:45): Cultural & Generational Fruit**  
   Blessings upon family lineage, thriving community harmony, social honour, and divine providence.
7. **Part 7 (~3:45 - End): Sacred Climax & Eternal Truth**  
   The deep garbhagriha inner sanctum, glowing ghee lamps, camphor flame, and eternal peace.

---

## 3. ASSETS & ENVIRONMENT MAP

### Audio Files (All 133 Chapters Ready)
- Staged in repository: `production/audio_staging/audio_ch001.wav` to `audio_ch133.wav` (7.00 GB).
- Master download mapping: `production/curated_37_waiting_adhigarams.json` and `production/audio_staging_map.json`.
- Cloud/Colab fast CDN releases: `https://github.com/shishyan/GuruKulaDesam/releases/download/v1.0-assets/`

### Visual Assets & Overlays
- Sacred Overlay: `production/sacred_lamp_dhoopa_overlay_1280x720.png`
- Upward Drizzle Loop: `production/upward_divine_drizzle_loop.mp4`
- Existing Curated Dravidian Image Batches: `production/scene_images/` (35 chapters staged).

### Lyrics & Canonical Meanings Database
- Complete database with Tamil lyrics, word-for-word explanations, and English translations:  
  `production/metadata/all_songs_lyrics_and_meanings.json`  
  `production/metadata/all_suno_lyrics_bundle.json`

---

## 4. CURRENT PRODUCTION STATUS

### A. Completed & Uploaded to YouTube (`PLW7qBZp_Q8Ro` as PRIVATE)
All recorded in [`production/youtube_uploaded_private_masters.json`](file:///c:/GitHub/Gurukuladesam/production/youtube_uploaded_private_masters.json):
- **Chapter 3 (*நீத்தார் பெருமை*)**: Video ID `-0vt1SzhZ1A` (Gold standard)
- **Chapter 7 (*புதல்வரைப் பெறுதல்*)**: Video ID `vfFm2G4mU7k` (Rebuilt with temple visuals & upward drizzle)
- **Chapter 9 (*விருந்தோம்பல்*)**: Video ID `bqGLSogcwGs` (Rebuilt with temple visuals & upward drizzle)
- **Chapter 10 (*இனியவை கூறல்*)**: Video ID `gtRJa6_qEjI` (Rebuilt with temple visuals & upward drizzle)
- **Chapter 11 (*செய்ந்நன்றி அறிதல்*)**: Video ID `DjECKZC_0jI` (Rebuilt with temple visuals & upward drizzle)
- **37 Earlier Releases**: All uploaded to YouTube as private drafts. Chapters 4, 5, 8, 12, 13, 14, 15, 17, 18, 19, 25-27, 30-31, 39-40, etc. need narrative script + temple re-renders to replace old village/downward rain versions.

---

## 5. STANDARD COMMANDS FOR CLOUD PC / COLAB EXECUTION

### Step 1: Environment Setup
```bash
git clone -b main https://github.com/shishyan/GuruKulaDesam.git /content/Gurukuladesam
cd /content/Gurukuladesam
pip install -q Pillow numpy tqdm requests mutagen google-api-python-client google-auth-oauthlib google-auth
```

### Step 2: Render Single Chapter (with GPU NVENC on Cloud PC / Colab)
```bash
python tools/build_cinematic_720p_film.py --chapter 12 --gpu nvenc
```
*(On CPU machines, simply omit `--gpu nvenc`).*

### Step 3: Multi-Chapter High-Throughput Batch Render
```bash
python tools/batch_render_all_cinematic.py --gpu nvenc --parallel-chapters 4
```

### Step 4: Upload Master Film to YouTube as Private Draft
```bash
python tools/upload_private_master_to_youtube.py --chapter 12 --video-file renders/releases/thirukkural_ch012_cinematic_720p_master.mp4
```

---

## 6. CLOUD PC AGENT CHECKLIST & INSTRUCTIONS

1. **Pull Latest Main**: Always run `git pull origin main` before starting a batch.
2. **Review Lyrics Before Image Prompting**: For any chapter needing image generation, extract the couplets and meaning from `production/metadata/all_songs_lyrics_and_meanings.json` and formulate the **7-Part Progression** prompt script.
3. **Verify Drizzle Mode**:
   - Upward drizzle (`production/upward_divine_drizzle_loop.mp4`) at 0.45 opacity screen blend for all positive chapters.
   - Omit drizzle for chapters 86, 87, 88, 89, 93, 94.
4. **Zero Overwrite of Gold Standards**: Never re-render Chapter 3.
5. **Always Upload as `private`**: Every single uploaded video must have privacy status `private` and be inserted into playlist `PLW7qBZp_Q8Ro`. Update `production/youtube_uploaded_private_masters.json` after every upload.
