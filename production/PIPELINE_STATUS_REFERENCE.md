# Guru Kula Desam — Master Production Pipeline Status & Reference Ledger

Generated: 2026-10-11 | Workspace: `c:\GitHub\Gurukuladesam` | Channel: `@guru-kula-desam`

---

## 1. COMPLETED PIPELINE (Archive & Ready Artifacts)

### A. Live YouTube Channel
* **Total Channel Videos**: **580 live videos**
* **Catalog Coverage**: 598 master devotional songs across 8 deities (Lord Shiva, Murugan, Amman, Krishna, Rama, Vinayagar, Thirukkural, Vallalar).

### B. Master Films Rendered on Disk
* **Total Clean Master Films in `renders/releases/`**: **187 films** (720p HD, 24 fps, zero burned lyrics, sacred architectural framing, lossless audio sync).
* **Catalog Rebuild Queue (`production/rebuild_queue.json`)**: **19 of 19 (100% Completed)**
  * All 19 under-scene legacy tracks rebuilt with **18–24 distinct non-repeating Veo scenes** each:
    1. `FTAB7OBVPPY` (Murugan, 19 scenes, 136.02 MB)
    2. `-yEq62Bu_d8` (Shiva, 21 scenes, 146.49 MB)
    3. `--4jzoezBW8` (Thirukkural, 24 scenes, 217.46 MB)
    4. `Nvx3ObuSndM` (Murugan, 18 scenes, 126.84 MB)
    5. `S4ogw4EfpDY` (Murugan, 21 scenes, 146.73 MB)
    6. `01g0sJdaL2I` (Thirukkural, 24 scenes, 167.95 MB)
    7. `2YzLM0yoBlg` (Krishna, 18 scenes, 30.42 MB)
    8. `0SUn5igNEE0` (Shiva, 24 scenes, 273.99 MB)
    9. `0WurYH-hkNM` (Thirukkural, 24 scenes, 178.91 MB)
    10. `2tL-bKjkL18` (Amman/Krishna, 20 scenes, 143.15 MB)
    11. `0tXyQEAHVNQ` (Shiva, 24 scenes, 217.33 MB)
    12. `meXI3QsNHhE` (Murugan, 21 scenes, 147.74 MB)
    13. `4vZEVROZIx8` (Vishnu/Krishna, 24 scenes, 262.56 MB)
    14. `nuSx1NgiCuo` (Murugan, 24 scenes, 202.51 MB)
    15. `2Qs07DTJvvM` (Thirukkural, 23 scenes, 167.65 MB)
    16. `3CICxCn-4A0` (Thirukkural, 20 scenes, 137.44 MB)
    17. `3yB_oTqh6Jk` (Thirukkural, 24 scenes, 184.73 MB)
    18. `8IAiHMylZJc` (Shiva, 24 scenes, 207.73 MB)
    19. `NeauJSGB2W8` (Krishna, 18 scenes, 33.55 MB)

### C. Completely Novel Chapters Built from Downloads
* **Total Novel Masters Built**: **45 films** (14–26 scenes each, e.g. *அலரறிவுறுத்தல்*, *அவர்வயின்விதும்பல்*, *இகல்*, *இடுக்கணழியாமை*, *இரவச்சம்*, *இரவு*, *உட்பகை*, *உறுப்புநலனழிதல்*, *உழவு*, *ஊடலுவகை*, *கண்விதுப்பழிதல்*, *கனவுநிலையுரைத்தல்*, *கயமை*, *கள்ளுண்ணாமை*, *காதற்சிறப்புரைத்தல்*, *குடிசெயல்வகை*, *குடிமை*, *குற்றங்கடிதல்*, *கூடா நட்பு*, *கொல்லாமை*).

### D. Google Flow Veo Cloud Renders
* **Pre-existing Veo Pool**: **639 clips** across 605 track folders in `production/google_flow_renders/`.
* **Fresh Veo Cloud Clips (Today)**:
  * `scene_01.mp4` (Palani Sivagiri at dawn, 1280x720, 24fps, 7.87 MB).
  * `scene_03.mp4` (Lord Dandayudhapani sanctum, 1280x720, 24fps, 4.78 MB).
  * **Credits Consumed**: 45 Flow credits authorized and deducted.

---

## 2. IN-PROCESS PIPELINE (Live Execution)

| Process | Script / Tool | Current Status |
| :--- | :--- | :--- |
| **YouTube Multi-Project Publisher** | `production/publish_all_masters.py` (`task-18358`) | Monitoring YouTube channel 24-hr velocity rolling window across 8 Google Cloud projects (80k quota). |
| **Google Flow Browser Session** | Port `9225` CDP | Active Chrome session logged in as Guru Kula Desam (`shishyan@gmail.com`). |
| **Master Film Assembly** | `tools/trigger_and_download_scene2.py` | Compositing 24-min film for *Kandha Sashti Kavasam* (`1hoVaPwWMes`). |

---

## 3. PENDING PIPELINE (Queued Tasks)

### A. Downloads Folder Novel Queue (`C:\Users\Shishyan\Downloads`)
* **Total Audio Files Audited**: 297 tracks.
* **Exact YouTube Matches**: **112 tracks** -> **STRICTLY BLOCKED & SKIPPED** (Zero Duplicates).
* **Alt / Variant Cuts**: 30 tracks.
* **Drafts / Scratch**: All files with `Good Intro`, `draft`, `rough`, `test`, `wip` -> **PERMANENTLY EXPUNGED**.
* **Completely Novel Tracks Remaining to Build**: **~109 tracks** (e.g. *சான்றாண்மை*, *சூது*, *செங்கோன்மை*, *செல்வம்*, *நட்பு*, *படைமாட்சி*, *பெரியாரைத் துணைக்கோடல்*, *மானமறிதல்*).
* **Builder Command**: `python -X utf8 tools/build_downloads_videos.py --limit 15`

### B. Colab / GPU Generation Queue
* **Structured Prompts Exported**: [`production/colab_handoff/pending_batch_prompts.json`](file:///c:/GitHub/Gurukuladesam/production/colab_handoff/pending_batch_prompts.json) (60 high-priority devotional tracks with exact scene & negative prompts).
* **Full Blueprint Catalog**: **479 tracks** in `production/pending_google_flow_manifest.json` with 0 rendered clips.
* **Target Output Structure**: `production/google_flow_renders/<TRACK_ID>/scene_01.mp4`, `scene_02.mp4`, `scene_03.mp4`.

### C. YouTube Publishing Queue
* **Verified Clean Masters Ready in `renders/releases/`**: **72+ films** waiting for upload velocity slots.
* **Automatic Ingestion**: Daemon `task-18358` uploads them sequentially as quota and velocity slots open.
