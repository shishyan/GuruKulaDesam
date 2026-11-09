#!/usr/bin/env python3
"""
ComfyUI Google Flow MCP Server
Standard JSON-RPC Model Context Protocol (MCP) server that connects to ComfyUI
and flow.google.com to execute Veo 3.1 & Imagen 4 generations using your Ultra credits.
"""

import sys
import json
import urllib.request

COMFYUI_URL = "http://127.0.0.1:8190"

def queue_flow_prompt(prompt: str, model: str = "Veo 3.1", aspect_ratio: str = "16:9") -> dict:
    workflow = {
        "3": {
            "inputs": {
                "prompt": prompt,
                "model": model,
                "aspect_ratio": aspect_ratio,
                "cdp_port": 9222,
                "timeout_seconds": 300
            },
            "class_type": "GoogleFlowCreditsGenerate",
            "_meta": {
                "title": "Google Flow (Ultra Credits Direct)"
            }
        }
    }
    payload = json.dumps({"prompt": workflow}).encode("utf-8")
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def handle_rpc(line: str):
    try:
        req = json.loads(line)
    except Exception:
        return

    method = req.get("method")
    msg_id = req.get("id")

    if method == "initialize":
        res = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "comfyui-google-flow-mcp", "version": "1.0.0"}
            }
        }
        print(json.dumps(res), flush=True)

    elif method == "tools/list":
        tools = [
            {
                "name": "generate_google_flow_video",
                "description": "Generate a video or scene in Google Flow using your Google Ultra subscription credits via ComfyUI.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Visual prompt describing the cinematic scene"},
                        "model": {"type": "string", "enum": ["Veo 3.1", "Veo 3.1 Lite", "Imagen 4"], "default": "Veo 3.1"},
                        "aspect_ratio": {"type": "string", "enum": ["16:9", "9:16", "1:1"], "default": "16:9"}
                    },
                    "required": ["prompt"]
                }
            }
        ]
        res = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"tools": tools}
        }
        print(json.dumps(res), flush=True)

    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "generate_google_flow_video":
            prompt = args.get("prompt", "")
            model = args.get("model", "Veo 3.1")
            aspect_ratio = args.get("aspect_ratio", "16:9")
            try:
                out = queue_flow_prompt(prompt, model, aspect_ratio)
                content = [{"type": "text", "text": f"Successfully queued in ComfyUI: {json.dumps(out)}"}]
            except Exception as e:
                content = [{"type": "text", "text": f"Error queueing in ComfyUI: {e}"}]

            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"content": content}
            }
            print(json.dumps(res), flush=True)

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line)

if __name__ == "__main__":
    main()
