# Guru Kula Desam — Agent Operational Handoff Guide

> **Scope**: Autonomous visual production, quality verification, and cinematic storyboard ingestion across 317 Thirukkural and Devotional audio tracks (`/home/nagaraj957/GuruKulaDesam`).

---

## 1. Executive Architecture & Division of Labor

The project pairs a **Local Antigravity Agent** with a concurrent **Gemini Ultra / Argon Session**:

```
                       ┌──────────────────────────────────────────────┐
                       │  Gemini Ultra / Argon Web / Browser Session  │
                       │   - Works Chapter 133 DOWN to Chapter 100+   │
                       │   - Also takes targeted batches (Ch 4, 5, 6) │
                       │   - Saves directly into Google Drive         │
                       └──────────────────────┬───────────────────────┘
                                              │ Deposits folders
                                              ▼
 ┌─────────────────────────────────────────────────────────────────────────────────┐
 │                               Google Drive Storage                              │
 │  - Shared Root ID: `1mXREJzspQdtqgAzwn1YtVLZoc8TpIOFp`                          │
 │  - Master Prompts: `thirukkural_chapters_01_to_50_gemini_ultra_prompts.txt`     │
 │  - Master 317 7-Part Storyboard: `master_317_seven_part_cinematic_prompts.txt`  │
 └────────────────────────────────────┬────────────────────────────────────────────┘
                                      │ rclone copy (high throughput)
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────────────┐
 │                             Local Antigravity Agent                             │
 │  1. Monitors Google Drive for new chapter folders via rclone / Drive API        │
 │  2. Downloads images into `production/google_drive_pull/<folder>`               │
 │  3. Validates quality: 16:9, 8K photorealistic, Tamil Sangam constraints       │
 │  4. Formats & maps into `production/scene_images/<Track_Name>/scene_01..24.jpg`  │
 │  5. Injects 7-part film progression prompts into each album directory           │
 │  6. Commits & pushes atomically to GitHub `main`                                │
 └─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Active Progress & Repository State

- **Repository**: `/home/nagaraj957/GuruKulaDesam` on branch `main`.
- **Latest Commit**: `d8cc2f2` (*"Add 7-part cinematic storyboard prompts for all 317 tracks across varied camera angles"*).
- **Total Master Audio Tracks**: 317 audio tracks in `/home/nagaraj957/Music/` (294 Thirukkural + 23 Sacred Devotional).
- **Scene Ingestion Progress**:
  - **35 Total Album Directories** created under `production/scene_images/`.
  - **33 Albums Fully Completed** with 24 verified photorealistic scenes each (816+ high-resolution scenes pushed to GitHub).
  - **Top-End Chapters Ingested**: Ch 1 (`Kadavul_Vazththu`), Ch 2 (`வான் சிறப்பு`), Ch 3 (`நீத்தார் பெருமை`), Ch 4 (`அறன் வலியுறுத்தல்`), Ch 5 (`இல்வாழ்க்கை`), Ch 6 (`வாழ்க்கைத் துணைநலம்`).
  - **Bottom-End Chapters Ingested from Drive**: Ch 117, Ch 118, Ch 119, Ch 121, Ch 123, Ch 124, Ch 125, Ch 126, Ch 127, Ch 131, Ch 133, Ch 75 (`அரண்`).

---

## 3. Strict Aesthetic & Directorial Rules

All image prompts and ingested assets MUST conform to these exact constraints:

1. **Aspect Ratio & Resolution**: Strict 16:9 composition, 8K photorealistic quality, warm golden natural light (dawn/twilight).
2. **Architecture**:
   - Clean, vibrant, traditionally painted Tamil courtyard homes (*illam*).
   - Fresh ochre and turmeric yellow walls, deep maroon/red base border trims.
   - Intricate white and red rice-flour *kolams* at doorways.
   - Hand-carved teakwood pillars supporting a shaded *thinnai* verandah with terracotta tiled roofs.
   - Pristine surroundings with Kaveri riverbanks, coconut groves, banana trees, and ancient banyan canopies.
3. **Attire & Living Culture**:
   - Traditional clean unbleached cotton and silk *veshtis*, traditional handloom sarees.
   - Authentic South Indian facial features and expressions of quiet dignity, hospitality, marital harmony, and respect for elders.
4. **STRICT NEGATIVE CONSTRAINTS**:
   - 🚫 **NO** temple sanctum idols / inner garbhagriha deities (to preserve universal philosophical sanctity).
   - 🚫 **NO** modern vehicles, roads, wires, or electrical poles.
   - 🚫 **NO** text, subtitles, or watermarks.

---

## 4. The 7-Part Cinematic Storyboard Requirement

Videos must NOT look like one continuous static room with the same characters. Each track requires a 7-stage narrative progression:

```
[1. Town Aerial Wide]  -> [2. Street Level Commons]  -> [3. House Thinnai Verandah]
                                                                     |
                                                                     v
[7. Ground Sunset Horizon] <- [6. Individual Focus] <- [5. Room Chamber] <- [4. Courtyard Family]
```

| Stage | Camera Angle | Scope & Content |
|---|---|---|
| **Part 1** | High-Altitude Drone / Aerial Glide | Entire ancient Tamil town, Kaveri waters, misty hills, terracotta roof clusters, hearth smoke. |
| **Part 2** | Eye-Level Street Tracking Shot | Vibrant village commons/street; elders on pyols, women with brass water pots, bullocks, community gathering. |
| **Part 3** | Medium-Wide Architectural View | Home facade, carved teak thinnai verandah, door toranam, morning threshold hospitality. |
| **Part 4** | Medium Ensemble Shot | Open-air red-oxide mutram courtyard; 3 generations sharing a banana-leaf feast. |
| **Part 5** | Cinematic Medium-Close Interior | Private room lit by brass oil lamps; husband and wife reviewing palm-leaf manuscripts in mutual counsel. |
| **Part 6** | Tight Close-up Portrait (Bokeh) | Single individual in deep ethical dedication (sculpting, writing Tamil script with iron stylus, herb preparation). |
| **Part 7** | Extreme Low-Angle Ground Shot | Dew on paddy shoots/riverbanks looking toward golden sunset; silhouette of sage under banyan tree. |

*Master files for all 317 tracks*:
- Local: [`production/master_317_seven_part_cinematic_prompts.txt`](file:///home/nagaraj957/GuruKulaDesam/production/master_317_seven_part_cinematic_prompts.txt)
- Google Drive: [Open 7-Part Master in Drive](https://drive.google.com/file/d/1rLzr3b9SDxvEIEZMzYlDOZWP9wzgwj31/view?usp=drivesdk) (ID: `1rLzr3b9SDxvEIEZMzYlDOZWP9wzgwj31`)

---

## 5. Google Drive Integration & Rclone Cheatsheet

Drive configuration is authenticated via `/home/nagaraj957/.config/rclone/rclone.conf`.

### Common Commands:
```bash
# Refresh Drive token if needed
rclone about gdrive:

# List chapter folders inside the main parent folder
rclone lsd "gdrive:" --drive-root-folder-id "1mXREJzspQdtqgAzwn1YtVLZoc8TpIOFp"

# Pull a completed chapter folder from Drive (fast multi-threaded)
rclone copy --drive-root-folder-id "<FOLDER_ID>" "gdrive:" "/home/nagaraj957/GuruKulaDesam/production/google_drive_pull/<folder-name>" --transfers 4 -v

# Push new prompt file to Google Drive
rclone copy "/path/to/prompt.txt" "gdrive:" --drive-root-folder-id "1mXREJzspQdtqgAzwn1YtVLZoc8TpIOFp" -v
```

---

## 6. Immediate Next Steps for the Incoming Agent

1. **Check Chapter 116 (`116-pirivaatraamai`)**:
   - Folder ID: `1o6qZ02BK0zWzjMOVRK3j3MKXXIxjOdXq`
   - Check if the 24 images have finished generating in Drive.
   - When ready, pull via rclone, map to `production/scene_images/பிரிவாற்றாமை_Golden/`, verify 24 scenes, and push to GitHub.
2. **Top-End Chapters 7 & 8**:
   - **Chapter 07**: புதல்வரைப் பெறுதல் (`7-puthalvarai-peruthal`)
   - **Chapter 08**: அன்புடைமை (`8-anbudaimai`)
   - Prompts are fully detailed in [`production/thirukkural_chapters_01_to_50_gemini_ultra_prompts.txt`](file:///home/nagaraj957/GuruKulaDesam/production/thirukkural_chapters_01_to_50_gemini_ultra_prompts.txt) and ready for Gemini Ultra generation.
3. **Environment Rules**:
   - ⚠️ **NEVER touch Chrome window/tab `-4525`** (window ID `62914625`), which is the user's personal active window.
   - Use Firefox or headless Drive API/rclone for all automated interactions.
