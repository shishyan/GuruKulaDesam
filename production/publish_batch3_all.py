# -*- coding: utf-8 -*-
"""
Publishes Batch 3 chapters 39, 40, 42, 44, 45, 46 to YouTube sequentially.
"""

import subprocess
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

chapters = [39, 40, 42, 44, 45, 46]

for ch in chapters:
    print(f"\n{'='*75}\nPUBLISHING CHAPTER {ch} TO YOUTUBE\n{'='*75}", flush=True)
    cmd = [sys.executable, "publish_videos_to_youtube.py", "--chapter", str(ch), "--republish"]
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print(f"FAILED to publish Chapter {ch}!", flush=True)
        sys.exit(1)
    print(f"Successfully published Chapter {ch}!\n", flush=True)
    time.sleep(3)

print("🎉 ALL BATCH 3 CHAPTERS PUBLISHED TO YOUTUBE!")

