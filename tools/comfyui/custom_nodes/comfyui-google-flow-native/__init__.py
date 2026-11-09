"""
ComfyUI Native Google Flow (Credits/Session Bridge) Node
Enables ComfyUI workflows to directly trigger Veo 3.1 generation using your
logged-in Google Flow account (nagaraj957@gmail.com with Ultra Plan credits),
without needing paid 3rd-party API keys or proxy tokens.
"""

import os
import sys
import time
import json
import glob
import urllib.request
from pathlib import Path

# Try importing websocket for CDP communication
try:
    import websocket
except ImportError:
    websocket = None

class GoogleFlowCreditsGenerateNode:
    """
    Triggers Google Flow (flow.google.com) directly using your logged-in Google Ultra
    subscription credits (8,000+ credits pool) connected via Chrome DevTools Protocol (CDP).
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "Cinematic 4k shot of sacred temple lamp flame, cinematic lighting, photorealistic, 24fps"
                }),
                "model": (["Veo 3.1", "Veo 3.1 Lite", "Imagen 4"], {"default": "Veo 3.1"}),
                "aspect_ratio": (["16:9", "9:16", "1:1"], {"default": "16:9"}),
                "cdp_port": ("INT", {"default": 9222, "min": 1024, "max": 65535}),
                "timeout_seconds": ("INT", {"default": 300, "min": 30, "max": 1200}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_path", "status_info")
    FUNCTION = "generate_via_flow"
    OUTPUT_NODE = True
    CATEGORY = "Google Flow (Ultra Credits)"

    def generate_via_flow(self, prompt, model, aspect_ratio, cdp_port, timeout_seconds):
        print(f"\n[Google Flow Native] Starting generation for: {prompt[:80]}...")
        
        # 1. Check CDP availability
        cdp_url = f"http://127.0.0.1:{cdp_port}/json/list"
        try:
            req = urllib.request.Request(cdp_url)
            with urllib.request.urlopen(req, timeout=3) as resp:
                tabs = json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            err_msg = (
                f"Chrome CDP not detected on port {cdp_port}. "
                f"Start Chrome with: google-chrome --remote-debugging-port={cdp_port} "
                f"--user-data-dir=/home/antigravity/shishyan/GuruKulaDesam/production/browser_profile_fresh "
                f"https://flow.google.com"
            )
            print(f"[Google Flow Native] ERROR: {err_msg}")
            return ("", f"ERROR: {err_msg}")

        # 2. Locate Google Flow tab
        flow_tabs = [t for t in tabs if 'flow.google.com' in t.get('url', '')]
        if not flow_tabs:
            return ("", "ERROR: No open tab found for flow.google.com in Chrome.")

        target_tab = flow_tabs[0]
        ws_url = target_tab.get('webSocketDebuggerUrl')
        if not ws_url or not websocket:
            return ("", "ERROR: WebSocket debugger URL not available or websocket-client not installed.")

        # 3. Connect and inject prompt into Flow's ProseMirror editor
        try:
            ws = websocket.create_connection(ws_url, suppress_origin=True)
            
            # Script to focus editor, clear, and paste prompt
            inject_js = f"""
            (() => {{
                const editor = document.querySelector('div.ProseMirror');
                if (!editor) return 'NO_EDITOR';
                editor.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('insertText', false, {json.dumps(prompt)});
                
                // Click the submit arrow button
                setTimeout(() => {{
                    const btn = document.querySelector('button[aria-label*="send" i], button[aria-label*="submit" i], button:has(span.material-icons:contains("arrow_forward"))') ||
                                Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('arrow_forward') || b.getAttribute('aria-label') === 'Submit');
                    if (btn) btn.click();
                    else {{
                        const event = new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', which: 13, keyCode: 13, bubbles: true }});
                        editor.dispatchEvent(event);
                    }}
                }}, 300);
                return 'SUBMITTED';
            }})()
            """
            
            ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': inject_js, 'returnByValue': True}}))
            res = json.loads(ws.recv())
            val = res.get('result', {}).get('result', {}).get('value')
            print(f"[Google Flow Native] Prompt injection status: {val}")

            # 4. Monitor generation status
            start_time = time.time()
            renders_dir = Path("/home/antigravity/shishyan/GuruKulaDesam/production/google_flow_renders")
            renders_dir.mkdir(parents=True, exist_ok=True)
            
            # Record initial files
            before_files = set(glob.glob(str(Path.home() / "Downloads" / "*"))) | set(glob.glob(str(renders_dir / "*")))

            status_text = "Submitted to Google Flow"
            latest_file = ""

            # Poll for completion
            while time.time() - start_time < timeout_seconds:
                time.sleep(4)
                
                # Check for auto-approve dialogs
                approve_js = """
                (() => {
                    const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
                    const approve = btns.find(b => /always approve|approve/i.test(b.innerText));
                    if (approve) {
                        approve.click();
                        return 'APPROVED';
                    }
                    return 'NO_APPROVAL_PROMPT';
                })()
                """
                ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': approve_js, 'returnByValue': True}}))
                _ = ws.recv()

                # Check if new video downloaded or rendered
                current_files = (set(glob.glob(str(Path.home() / "Downloads" / "*.mp4"))) | 
                                 set(glob.glob(str(Path.home() / "Downloads" / "*.zip"))) |
                                 set(glob.glob(str(renders_dir / "**" / "*.mp4"), recursive=True)))
                new_files = list(current_files - before_files)
                if new_files:
                    latest_file = new_files[0]
                    status_text = f"SUCCESS: Generated {os.path.basename(latest_file)}"
                    print(f"[Google Flow Native] {status_text}")
                    break

            ws.close()
            return (latest_file, status_text)

        except Exception as ex:
            return ("", f"ERROR during Flow execution: {ex}")


NODE_CLASS_MAPPINGS = {
    "GoogleFlowCreditsGenerate": GoogleFlowCreditsGenerateNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GoogleFlowCreditsGenerate": "Google Flow (Ultra Credits Direct)"
}
