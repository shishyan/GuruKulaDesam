import os, sys, json, time
from pathlib import Path

sys.path.insert(0, r"c:\GitHub\Gurukuladesam")
from tools.generate_modern_thumbnail import render_thumbnail

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    meta = json.load(f)

out_dir = Path(r"c:\GitHub\Gurukuladesam\production\thumbnails")
out_dir.mkdir(parents=True, exist_ok=True)

missing = [(vid, item.get('title', '')) for vid, item in meta.items() if not (out_dir / f"{vid}.png").exists()]

print(f"Total videos in catalog: {len(meta)}")
print(f"Already generated: {len(meta) - len(missing)}")
print(f"Generating modern 16:9 thumbnails for {len(missing)} missing tracks...\n")

t0 = time.time()
generated = 0
for idx, (vid, raw_title) in enumerate(missing, 1):
    try:
        render_thumbnail(vid, raw_title)
        generated += 1
    except Exception as e:
        print(f"  ❌ Error on {vid} ({raw_title[:30]}): {e}")
        
    if idx % 25 == 0 or idx == len(missing):
        elapsed = time.time() - t0
        rate = generated / (elapsed if elapsed > 0 else 1)
        print(f"  ⚡ [{idx}/{len(missing)}] Generated {generated} thumbnails ({rate:.1f} thumbs/sec, {elapsed:.1f}s elapsed)...", flush=True)

print(f"\n🎉 Finished! Total thumbnails now in {out_dir}: {len(list(out_dir.glob('*.png')))}")
