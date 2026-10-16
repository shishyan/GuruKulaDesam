# CLOUD PC AI AGENT HANDOFF: NON-THIRUKKURAL CINEMATIC DEVOTIONAL MASTER FILMS

**Date / Timestamp:** 2026-10-16  
**Channel:** [@guru-kula-desam](https://www.youtube.com/@guru-kula-desam) ("குரு குல தேசம்")  
**Repository:** `https://github.com/shishyan/GuruKulaDesam.git` (branch: `main`)  
**Mission:** Produce, assemble, and render broadcast-grade cinema films for all non-Thirukkural devotional audio tracks from the `@guru-kula-desam` catalog, adhering strictly to the **24-Scene Double-Image Directive**, **4-way cinematic camera panzooms**, **upward divine drizzle**, and **sacred dhoopa lamp overlay**.

---

## 1. THE NON-NEGOTIABLE ARTISTIC & CINEMATIC SPECIFICATIONS

Every non-Thirukkural video produced **MUST** follow these exact specifications:

### A. Strictly 24 Unique Thematic Images Per Song ("Double it" Directive)
- **User Instruction:** *"12 images is not enough per song -- double it"*.
- Every audio track must feature **exactly 24 unique photorealistic 16:9 8K thematic scene images**.
- Never loop or recycle fewer images.
- Images are stored in `production/scene_images/<theme_name>/scene_01.jpg` through `scene_24.jpg`.

### B. Authentic Dravidian Temple Visual Aesthetics
- **Theme Prompts:** Sacred Tamil Nadu temples (Maha Kumbabishekam standard): intricately carved multi-tier gopurams with crisp colourful stucco deities, shining gold kalasams in morning sunlight, polished granite sanctum floors reflecting brass kuthuvilakku deepams, fragrant fresh jasmine & marigold garlands, sacred dhoopam smoke, devotees in traditional festive silk attire.
- **Edge-to-Edge:** Full 16:9 aspect ratio (`1280x720` or higher), no letterbox bars, no watermark, no text.

### C. Upward Divine Drizzle Screen Blend
- **Asset:** `production/upward_divine_drizzle_loop.mp4` (blended at `0.45` screen opacity).
- **Rule:** Drizzle must float upward as divine mist/grace.

### D. Sacred Lamp & Dhoopa Overlay
- **Asset:** `production/sacred_lamp_dhoopa_overlay_1280x720.png` (auto-healed from base64 if missing).
- Subtle atmospheric alpha blend framing the sanctum.

### E. Master Cinematic Camera Motion & Cross-Dissolves
- 4-way cinematic camera moves (Pan Left $\to$ Right, Pan Right $\to$ Left, Slow Push, Slow Pull, and 3D cosine-eased parabolic panzoom).
- 1.0s smooth cross-dissolve (`xfade`) transitions between all 24 scenes.
- Audio: Pristine untouched 48kHz master audio or 256k AAC stereo with a gentle 2.0s fadeout at the tail.

---

## 2. PRODUCTION STATUS & BOTTOM-UP QUEUE

### Completed & Verified Master Films (7/21):
Located in `renders/releases/`:
1. `thirumurugatruppadai_kunram_erinthai_cinematic_720p_master.mp4` (401.7s, 24 scenes)
2. `pazhamai_1f_golden_2026_cinematic_720p_master.mp4` (318.5s, 24 scenes)
3. `pazhamai_1h_golden_pop_1_cinematic_720p_master.mp4` (317.6s, 24 scenes)
4. `pazhamai_clip_cinematic_720p_master.mp4` (88.5s, 24 scenes)
5. `thirupparamkunram_1n_golden_cinematic_720p_master.mp4` (587.0s, 24 scenes)
6. `thirupparamkunram_2b_golden_cinematic_720p_master.mp4` (527.9s, 24 scenes)
7. `thiruavinankudi_1g_golden_2026_cinematic_720p_master.mp4` (470.9s, 24 scenes)

---

### Remaining Active Queue (Strict Bottom-Up Order: Tracks 8 to 21):

| # | Audio Track Filename | Theme / Subject | Status / Action Needed |
|---|---|---|---|
| **8** | `திருஏரகம் 1H Golden.wav` | Swamimalai (Fourth Arupadai Veedu) | 24 prompts written in `gen_non_kural_scene_images.py`. Generate 24 scenes & render film. |
| **9** | `குன்றுதோறாடல் 1D Golden.wav` | Thiruthani (Fifth Arupadai Veedu) | Write 24 prompts, generate 24 scenes & render film. |
| **10** | `பழமுதிர் சோலை 1J Golden.wav` | Pazhamudircholai (Sixth Arupadai Veedu) | Write 24 prompts, generate 24 scenes & render film. |
| **11** | `திருச்செந்தூர் 1Q Golden.wav` | Thiruchendur seashore temple (Second Arupadai Veedu) | Write 24 prompts, generate 24 scenes & render film. |
| **12** | `திருச்செந்தூர் 2E Golden 2026.wav` | Thiruchendur Soorasamharam & divine victory | Reuse / expand Thiruchendur 24 scenes. |
| **13** | `தோடு உடைய செவியன் 1M Golden.wav` | Sambandar Thevaram / Sirkazhi Shiva & Murugan | Write 24 prompts, generate 24 scenes & render film. |
| **14** | `பத்தரோடு  1G Golden.wav` | Appar / Sundarar devotional hymns | Write 24 prompts, generate 24 scenes & render film. |
| **15** | `மைம் மரு 1D Golden.wav` | Ancient Sangam devotional classic | Write 24 prompts, generate 24 scenes & render film. |
| **16** | `செய் அருகே 1J2 Golden 2026.wav` | Temple agricultural landscape / devotional hymns | Write 24 prompts, generate 24 scenes & render film. |
| **17** | `அங்கமும் வேதமும் 1N Golden 2026.wav` | Thevaram (Tirumurai) sacred Tamil verses | Write 24 prompts, generate 24 scenes & render film. |
| **18** | `அங்கமும் வேதமும் 1N Golden.wav` | Thevaram alternate master render | Reuse / expand 24 scenes. |
| **19** | `அங்கமும் வேதமும் 1O Golden 2026.wav` | Thevaram alternate master render | Reuse / expand 24 scenes. |
| **20** | `பாடக மெல்லடி 1J Golden.wav` | Ancient Shaivite / Murugan hymnal | Write 24 prompts, generate 24 scenes & render film. |
| **21** | `புண்ணியர் பூதியர் 1H Golden 2026.wav` | Sacred Vibhuti / Lord Shiva / Murugan hymn | Write 24 prompts, generate 24 scenes & render film. |

---

## 3. SCRIPTS & COMMANDS

### Step 1: Sync Codebase
```bash
git pull origin main
```

### Step 2: Set Valid Gemini API Key
```bash
export GEMINI_API_KEY="your-active-api-key"
```

### Step 3: Generate 24 Thematic Scenes
```bash
python tools/gen_non_kural_scene_images.py --theme <theme_name> --out-dir production/scene_images/<theme_name>
```

### Step 4: Build Master Film
```bash
python tools/build_non_kural_cinematic_film.py \
  --audio "path/to/audio.wav" \
  --images-dir "production/scene_images/<theme_name>" \
  --output "renders/releases/<output_film_name>.mp4" \
  --title "<Song Title> - 24 Scenes Master"
```

### Step 5: Commit and Push Results
```bash
git add production/scene_images/<theme_name>
git commit -m "Add 24 generated scenes for <theme_name>"
git push origin main
```
