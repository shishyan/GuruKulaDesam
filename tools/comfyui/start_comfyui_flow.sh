#!/usr/bin/env bash
# ==============================================================================
# Guru Kula Desam - Autonomous ComfyUI & Google Flow (Ultra Credits) Launcher
# Automatically restores, installs, and launches ComfyUI on any fresh cloud VM.
# ==============================================================================
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMFY_DIR="$HOME/ComfyUI"
PORT=8190

echo "======================================================================"
echo "[ComfyUI + Google Flow Launcher] Checking environment..."
echo "======================================================================"

# 1. Clone ComfyUI if not present on this VM
if [ ! -d "$COMFY_DIR" ]; then
    echo "[1/4] Cloning ComfyUI repository..."
    git clone https://github.com/comfyanonymous/ComfyUI.git "$COMFY_DIR"
fi

# 2. Link persistent custom nodes & MCP server from the repository
echo "[2/4] Linking Google Flow Ultra nodes and MCP server..."
mkdir -p "$COMFY_DIR/custom_nodes"
ln -sfn "$REPO_ROOT/tools/comfyui/custom_nodes/comfyui-google-flow-native" "$COMFY_DIR/custom_nodes/comfyui-google-flow-native"

# 3. Create virtual environment using uv (instant)
if [ ! -d "$COMFY_DIR/.venv" ]; then
    echo "[3/4] Creating virtual environment and installing dependencies via uv..."
    uv venv "$COMFY_DIR/.venv"
    uv pip install --python "$COMFY_DIR/.venv" \
        --extra-index-url https://download.pytorch.org/whl/cpu \
        torch torchvision torchaudio \
        -r "$COMFY_DIR/requirements.txt" \
        requests aiohttp websocket-client
fi

# 4. Free port if busy and start daemon
echo "[4/4] Starting ComfyUI server on port $PORT..."
fuser -k "${PORT}/tcp" 2>/dev/null || true
nohup "$COMFY_DIR/.venv/bin/python3" "$COMFY_DIR/main.py" --cpu --listen 0.0.0.0 --port "$PORT" > "$COMFY_DIR/comfyui.log" 2>&1 &

echo "======================================================================"
echo "[SUCCESS] ComfyUI is running at http://localhost:$PORT"
echo "Log file: $COMFY_DIR/comfyui.log"
echo "======================================================================"
