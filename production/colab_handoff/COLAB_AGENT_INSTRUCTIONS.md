# Guru Kula Desam — Colab Video Generation Handoff & Specifications

This document and the companion file [`pending_batch_prompts.json`](file:///c:/GitHub/Gurukuladesam/production/colab_handoff/pending_batch_prompts.json) provide everything needed for a Google Colab agent / GPU runtime to generate devotional video scenes that seamlessly integrate into the Guru Kula Desam automated master production pipeline.

---

## 1. Technical Video Specifications

All video models (CogVideoX, Wan 2.1, HunyuanVideo, LTX-Video, Mochi, etc.) in Colab must output clips meeting these exact standards:

| Property | Requirement | Rationale |
| :--- | :--- | :--- |
| **Aspect Ratio** | **16:9 Widescreen** | Landscape master films for YouTube standard display |
| **Resolution** | **1280×720 (720p)** or **1920×1080 (1080p)** | Matches our Veo & FFmpeg pipeline dimensions |
| **Frame Rate** | **24 fps** (progressive) | Standard cinematic devotional motion grammar |
| **Duration** | **5 to 10 seconds** per scene | We slow them to 75% devotional speed during master assembly |
| **Video Codec** | **H.264 (avc1)**, pixel format `yuv420p` | Maximum compatibility across all FFmpeg decoders |
| **Audio** | Silent / No audio stream | Local assembly multiplexes the master lossless vocal soundtrack |
| **Text Overlay** | **ABSOLUTELY ZERO BURNED TEXT** | No lyrics, no watermarks, no subtitles, no credits on video |

---

## 2. Sacred Visual Grammar & Authenticity Guidelines

All generated visuals must depict authentic **Sanatana Vedic & Classical Tamil Sangam sacred traditions**:

* **Architecture**: Ancient South Indian Dravidian temples (Chola/Pandya stone vimanas, pillared granite mandapams, carved monolithic sanctums, temple tanks/theppakulams, granite river bathing ghats).
* **Lighting**: Natural golden dawn/dusk amber sunlight, sacred flames from bronze *Kuthuvilakku* / *Agal Vilakku* oil lamps, burning camphor harathi glow, gentle curls of *Sambrani* dhoopam incense.
* **Deities & Vigrahas**: Solid ancient black granite (Krishna Shila) or consecrated bronze panchaloha vigrahas adorned with natural fresh flower garlands (jasmine, marigold, bilva, tulsi, lotus).
* **Devotees & Rishis**: Adorned with sacred white *Tripundra Vibhuti* horizontal stripes, vermilion *Kumkum*, *Rudraksha* malas, unstitched cotton/silk veshtis/dhotis and madisars, bare feet within temple precincts.

### Universal Negative Prompt (Must Append to Every Prompt)
```text
No text, no subtitles, no watermarks, no credits, no modern clothing, no western clothes, no trousers, no shirts, no shoes, no sneakers, no sandals, no eyeglasses, no sunglasses, no electric wires, no lightbulbs, no plastic items, no mobile phones, no cars, no modern roads, no CGI artifacts, no cartoon, no 3D anime, no distorted hands, no extra limbs.
```

---

## 3. Directory Structure & File Naming Conventions

The local Gurukuladesam engine automatically watches for rendered clips in this exact structure:

```
production/google_flow_renders/
└── <TRACK_ID>/
    ├── scene_01.mp4
    ├── scene_02.mp4
    └── scene_03.mp4
```

* Each track folder is named with its canonical 11-character **`TRACK_ID`** (e.g. `1hoVaPwWMes`, `2_rwWlC09I0`).
* Scenes must be numbered with 2 digits: `scene_01.mp4`, `scene_02.mp4`, `scene_03.mp4`.
* Target count: **3 distinct scenes per track** (Anchor Standard).

---

## 4. How the Colab Agent Loads & Iterates Prompts

In Colab, upload or load [`pending_batch_prompts.json`](file:///c:/GitHub/Gurukuladesam/production/colab_handoff/pending_batch_prompts.json):

```python
import json
import os
from pathlib import Path

# Load pre-parsed batch package
with open("pending_batch_prompts.json", "r", encoding="utf-8") as f:
    batch_data = json.load(f)

tracks = batch_data["tracks"]
print(f"Loaded {len(tracks)} pending tracks for generation.")

output_root = Path("generated_clips")

for t in tracks:
    track_id = t["track_id"]
    category = t["category"]
    title = t["title"]
    print(f"\n==========================================")
    print(f"Generating for: {title} ({track_id}) [{category}]")
    print(f"==========================================")
    
    track_dir = output_root / track_id
    track_dir.mkdir(parents=True, exist_ok=True)
    
    for sc in t["scenes"]:
        sc_num = sc["scene_num"]
        out_clip = track_dir / f"scene_{sc_num:02d}.mp4"
        if out_clip.exists():
            print(f"  Scene {sc_num} already exists. Skipping.")
            continue
            
        prompt = sc["prompt"]
        negative_prompt = sc["negative_prompt"]
        
        print(f"  Generating Scene {sc_num}...")
        # >>> CALL YOUR COLAB VIDEO MODEL PIPELINE HERE <<<
        # pipe(prompt=prompt, negative_prompt=negative_prompt, ...).save(out_clip)

# After generation, package for fast download / rsync:
# !zip -r -q devotional_clips_batch.zip generated_clips/
```

---

## 5. Instant Local Assembly & YouTube Publishing

Once the Colab agent completes a batch of clips and places or unzips them into `production/google_flow_renders/<TRACK_ID>/`, the local pipeline runs automatically:

```bash
# To assemble and composite master films for all generated tracks:
python production/google_flow_engine.py --all

# Or to run the autonomous multi-project publisher daemon:
python production/publish_all_masters.py
```

The local engine:
1. Validates 16:9 HD video and detects clip counts.
2. Applies 75% devotional speed retiming.
3. Builds an alternating forward/reverse continuous timeline matching exact audio duration.
4. Composites the sacred temple architectural border and subtle ambient dust/drizzle overlay.
5. Multiplexes the clean audio soundtrack.
6. Writes final release to `renders/releases/<category>_<TRACK_ID>_master.mp4`.
7. Enqueues for YouTube publishing across 8 rotating OAuth projects (80,000 daily quota pool).
