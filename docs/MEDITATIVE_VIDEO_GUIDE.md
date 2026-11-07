# Meditative Video Guide & Production Pipeline

This guide outlines the production standards, sound-mixing specifications, video layering, and quota-resilient automated publishing pipeline for Guru Kula Desam's global meditative, deep sleep, ASMR, and focus instrumental videos.

---

## 1. Core Principles & Philosophy

1. **100% Original Creations**:
   - Master compositions by the creator (never categorized as remixes or third-party covers).
2. **Global Audience Aesthetic**:
   - Zero regional/religious text overlays or Tamil/Thirukkural typography.
   - Zero artificial visual waveforms (`showwaves`).
   - Clean, grand, natural landscapes (fjords, misty redwoods, waterfalls, rainforest drizzle, bamboo groves, ocean sunsets, Himalayan dawns).
3. **Sound Mixing Ratio**:
   - Master Music Audio: **100% volume (`volume=1.0`)** at 48kHz stereo.
   - Organic Ambient Video Sound: **-75% attenuation (`volume=0.25`, `atempo=0.5`)** to create a subtle acoustic bed underneath the music.
4. **Playback Speed**:
   - **50% Slow-Motion (`setpts=2.0*PTS`)** for all visual footage, transforming standard camera motion into an ethereal, hypnotic meditation.
5. **Quota Resilience**:
   - Automated local master rendering continues unhindered even when YouTube's daily API quota is reached.
   - Upload queue automatically holds and sleeps in 30-minute intervals until quota resets (midnight Pacific Time).

---

## 2. Technical Specifications

- **Resolution**: 1920x1080 (16:9 1080p Full HD)
- **Framerate**: 30 fps constant
- **Speed**: 50% slow motion via `setpts=2.0*PTS`
- **Encoding**: H.264 High Profile, CRF 19, `yuv420p`
- **Container**: MP4 with `-movflags +faststart`
- **Audio Codec**: AAC 320kbps, 48,000 Hz stereo
- **Audio Mix Filter**: `[0:a]atempo=0.5,volume=0.25[a_amb];[1:a][a_amb]amix=inputs=2:duration=first:dropout_transition=3[aout]`

---

## 3. Directory Structure

```
├── /home/shishyan/Downloads/                    # Raw Master WAV Audio Files
├── /home/shishyan/Videos/Instrumentals/         # 42+ 1080p Nature Footage Clips
├── production/nanudaimai_instrumental/
│   ├── autonomous_nature_pipeline.py            # Main Resilient Pipeline Runner
│   └── batch2_masters/                          # Output 1080p Rendered Masters & Results
└── .gemini/config/skills/meditative-video-guide # Global Agent Skill
```
