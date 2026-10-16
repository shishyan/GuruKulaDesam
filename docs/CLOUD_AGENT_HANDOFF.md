# Cloud Agent Hand-off: Non-Thirukkural Cinematic Video Pipeline

This document provides a clean, self-contained hand-off specification for autonomous agents running on Cloud PC / Google Colab / remote instances to continue and finish producing broadcast-grade cinema films for all non-Thirukkural devotional audio tracks in the `@guru-kula-desam` catalog.

---

## 1. Core Mandates & Technical Rules

1. **Exactly 24 Unique Thematic Images Per Song ("Double it" Directive):**
   - Every audio track must have **exactly 24 photorealistic, sacred, 16:9 8K thematic scene images**.
   - No looping of fewer scenes. Never render a film with 12 images.
2. **Master Visual Specifications:**
   - **Resolution:** Native 16:9 (`1280x720` for 720p broadcast master).
   - **Framerate:** 24 fps (`-r 24`).
   - **Camera Movements:** Dynamic 4-way cinematic camera motion (Pan Left→Right, Pan Right→Left, Slow Push, Slow Pull, and 3D cosine-eased parabolic panzoom).
   - **Transitions:** 1.0s cross-dissolve (`xfade`) across all 24 scenes.
   - **Divine Overlays:**
     - Upward divine golden drizzle blend (`production/upward_divine_drizzle_loop.mp4` at `0.45` screen opacity).
     - Sacred lamp & dhoopa atmospheric vignette (`production/sacred_lamp_dhoopa_overlay_1280x720.png`).
3. **Lossless Master Audio Remux:**
   - Source 48kHz audio preserved losslessly or high-bitrate AAC 256k stereo.
   - 2.0s smooth tail fade-out matching exact song duration.
4. **Bottom-Up Queue Discipline:**
   - Audio tracks are processed strictly from the bottom-up chronological order of the production audio catalog / Downloads list.

---

## 2. Production Queue Status

### Completed Master Films (7/21):
All 7 master films are rendered and verified in `renders/releases/`:
1. `thirumurugatruppadai_kunram_erinthai_cinematic_720p_master.mp4` (401.7s, 24 scenes)
2. `pazhamai_1f_golden_2026_cinematic_720p_master.mp4` (318.5s, 24 scenes)
3. `pazhamai_1h_golden_pop_1_cinematic_720p_master.mp4` (317.6s, 24 scenes)
4. `pazhamai_clip_cinematic_720p_master.mp4` (88.5s, 24 scenes)
5. `thirupparamkunram_1n_golden_cinematic_720p_master.mp4` (587.0s, 24 scenes)
6. `thirupparamkunram_2b_golden_cinematic_720p_master.mp4` (527.9s, 24 scenes)
7. `thiruavinankudi_1g_golden_2026_cinematic_720p_master.mp4` (470.9s, 24 scenes)

---

### Remaining Active Queue (Tracks 8 to 21 - In Strict Order):

| # | Audio Track Filename | Theme / Subject | Status / Action Needed |
|---|----------------------|-----------------|------------------------|
| **8** | `திருஏரகம் 1H Golden.wav` | Swamimalai (Fourth Arupadai Veedu) | 24 prompts ready in `gen_non_kural_scene_images.py`. Generate 24 scenes & render film. |
| **9** | `குன்றுதோறாடல் 1D Golden.wav` | Thiruthani (Fifth Arupadai Veedu) | Write 24 prompts, generate 24 scenes & render film. |
| **10** | `பழமுதிர் சோலை 1J Golden.wav` | Pazhamudircholai (Sixth Arupadai Veedu) | Write 24 prompts, generate 24 scenes & render film. |
| **11** | `திருச்செந்தூர் 1Q Golden.wav` | Thiruchendur seashore temple (Second Arupadai Veedu) | Write 24 prompts, generate 24 scenes & render film. |
| **12** | `திருச்செந்தூர் 2E Golden 2026.wav` | Thiruchendur Soorasamharam & Murugan victory | Can reuse/expand Thiruchendur 24 scenes. |
| **13** | `தோடு உடைய செவியன் 1M Golden.wav` | Sambandar Thevaram / Sirkazhi Shiva & Murugan | Write 24 prompts, generate 24 scenes & render film. |
| **14** | `பத்தரோடு  1G Golden.wav` | Appar / Sundarar devotional hymns | Write 24 prompts, generate 24 scenes & render film. |
| **15** | `மைம் மரு 1D Golden.wav` | Ancient Sangam devotional classic | Write 24 prompts, generate 24 scenes & render film. |
| **16** | `செய் அருகே 1J2 Golden 2026.wav` | Temple agricultural landscape / devotional hymns | Write 24 prompts, generate 24 scenes & render film. |
| **17** | `அங்கமும் வேதமும் 1N Golden 2026.wav` | Thevaram (Tirumurai) sacred Tamil verses | Write 24 prompts, generate 24 scenes & render film. |
| **18** | `அங்கமும் வேதமும் 1N Golden.wav` | Thevaram alternate master render | Reuse/expand 24 scenes. |
| **19** | `அங்கமும் வேதமும் 1O Golden 2026.wav` | Thevaram alternate master render | Reuse/expand 24 scenes. |
| **20** | `பாடக மெல்லடி 1J Golden.wav` | Ancient Shaivite / Murugan hymnal | Write 24 prompts, generate 24 scenes & render film. |
| **21** | `புண்ணியர் பூதியர் 1H Golden 2026.wav` | Sacred Vibhuti / Lord Shiva / Murugan hymn | Write 24 prompts, generate 24 scenes & render film. |

---

## 3. Tooling & Architecture

### A. Scene Image Generation (`tools/gen_non_kural_scene_images.py`)
- Uses Google GenAI `gemini-2.5-flash-image` (or `imagen-3.0-generate-002`) with 16:9 aspect ratio.
- Each theme contains an array of 24 descriptive Tamil temple prompts (maha kumbabishekam aesthetic, polished granite sanctum, deepams, dhoopam, devotees in traditional silk attire).
- Autocrops any letterbox borders to true 16:9 (`1280x720`).
- Command:
  ```bash
  python tools/gen_non_kural_scene_images.py --theme <theme_name> --out-dir production/scene_images/<theme_name>
  ```

### B. Master Cinema Film Assembly (`tools/build_non_kural_cinematic_film.py`)
- Assembles any 24-image directory and audio file into a master film.
- Supports hardware NVENC (`h264_nvenc` on GPU instances) and CPU (`libx264`).
- Self-heals the sacred overlay PNG if missing or corrupted.
- Command:
  ```bash
  python tools/build_non_kural_cinematic_film.py \
    --audio "<path_to_audio_wav>" \
    --images-dir "production/scene_images/<theme_name>" \
    --output "renders/releases/<output_film_name>.mp4" \
    --title "<Tamil Title> - 24 Scenes Master"
  ```

---

## 4. Cloud PC / Colab Agent Instructions

When picking up this pipeline in a cloud environment:
1. **Pull the latest repository:**
   ```bash
   git pull origin main
   ```
2. **Environment Variable:**
   Ensure a valid `GEMINI_API_KEY` is exported:
   ```bash
   export GEMINI_API_KEY="your-active-api-key"
   ```
3. **Execute Track by Track:**
   - Follow the queue table in Section 2.
   - Verify all 24 scenes are generated before invoking `build_non_kural_cinematic_film.py`.
   - Commit generated scene images and push to `origin main` to keep local and cloud synchronized:
     ```bash
     git add production/scene_images/
     git commit -m "Add 24 generated scenes for <theme>"
     git push origin main
     ```

---

## 5. Colab MCP Server Configuration & Troubleshooting

### Why the Cloud PC Agent Fails to Start Colab MCP:
1. **Prerequisites Missing:** `colab-mcp` is an executable python package distributed via `uv` / `uvx`. It requires `uv` to be installed on the system path (`pip install uv`).
2. **Browser Connection Requirement:** `colab-mcp` is **not** a headless REST client. It is a bridge between the local agent and an **active browser session** running Google Colab. The notebook (`Non-Thirukkural-Videos.ipynb`) must be opened in Chrome on that machine, and the agent must first call `open_colab_browser_connection` to unlock the execution tools (`run_code_cell`, `get_cells`, `update_cell`, etc.).
3. **Client Capability:** The MCP client must support `notifications/tools/list_changed` (standard in Antigravity / Gemini CLI / Windsurf).

### Working Configuration (`mcp_config.json`):
Location:
- Windows: `~/.gemini/config/mcp_config.json` or `.agents/mcp_config.json`
- Linux / Cloud PC: `~/.gemini/config/mcp_config.json` or `~/.config/antigravity/mcp_config.json`

```json
{
  "mcpServers": {
    "colab-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/googlecolab/colab-mcp",
        "colab-mcp"
      ],
      "timeout": 30000
    }
  }
}
```

*Note:* If using Windows with a specific Python/uv install:
```json
{
  "mcpServers": {
    "colab-mcp": {
      "command": "C:\\Python310\\Scripts\\uvx.exe",
      "args": [
        "--from",
        "git+https://github.com/googlecolab/colab-mcp",
        "colab-mcp"
      ]
    }
  }
}
```

### Step-by-Step Activation Sequence for Cloud PC Agents:
1. **Install uv:**
   ```bash
   pip install uv
   ```
2. **Verify CLI runs:**
   ```bash
   uvx --from git+https://github.com/googlecolab/colab-mcp colab-mcp
   ```
3. **Open Colab in Browser:**
   Open Chrome and navigate to the notebook URL:
   `https://colab.research.google.com/drive/1D8TVFR5n9WRrxKNP6kSlODvrlSem0zcB`
4. **Trigger Initial MCP Handshake:**
   The agent must first invoke:
   `open_colab_browser_connection()`
   Once connected, the notebook tools (`run_code_cell`, `get_cells`, `update_cell`) dynamically register.
