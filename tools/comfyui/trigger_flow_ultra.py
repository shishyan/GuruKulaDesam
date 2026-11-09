#!/usr/bin/env python3
"""
Autonomous Google Flow Ultra Executor
Sends generation prompts directly to ComfyUI on port 8190, executing via
the native Google Flow Ultra Credits integration.
"""

import sys
import json
import urllib.request
import argparse

COMFYUI_URL = "http://127.0.0.1:8190"

def trigger_generation(prompt: str, model: str = "Veo 3.1", aspect_ratio: str = "16:9"):
    print("=" * 70)
    print(f"Triggering ComfyUI Google Flow (Ultra Credits):")
    print(f"  Model:        {model}")
    print(f"  Aspect Ratio: {aspect_ratio}")
    print(f"  Prompt:       {prompt}")
    print("=" * 70)

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
        result = json.loads(resp.read().decode("utf-8"))
        print(f"SUCCESS: Prompt queued with ID: {result.get('prompt_id')}")
        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trigger Google Flow generation via ComfyUI")
    parser.add_argument("--prompt", type=str, default="Cinematic macro shot of ancient bronze oil lamp flame flickering, warm temple illumination, 4k 24fps", help="Visual prompt")
    parser.add_argument("--model", type=str, default="Veo 3.1", choices=["Veo 3.1", "Veo 3.1 Lite", "Imagen 4"])
    parser.add_argument("--aspect_ratio", type=str, default="16:9", choices=["16:9", "9:16", "1:1"])
    args = parser.parse_args()

    trigger_generation(args.prompt, args.model, args.aspect_ratio)
