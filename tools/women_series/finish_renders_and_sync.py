#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resilient Multi-Worker Supervisor for the 3 Women's Series 1080p Renders:
  - Attaches seamlessly to `wom_ep02` (already mid-render on ep02!) without restarting it.
  - Attempts to spin up a second isolated worker `wom_ep01` (`--gpu l4`, fallback `--gpu t4 --high-mem`);
    if Colab cap is full (e.g. external session `3e5558` active), gracefully falls back to sequential warm rendering on `wom_ep02`.
  - Never touches external sessions (`3e5558` etc.).
  - Never aborts on transient `colab exec` poll timeouts under heavy Remotion CPU load.
  - Stops ONLY `wom_ep02` / `wom_ep01` once all 3 master MP4s are muxed & verified, then syncs to Google Drive!
"""

from __future__ import annotations

import json
import queue
import subprocess
import sys
import threading
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import orchestrate_colab_l4 as orch  # noqa: E402
from women_3pillars_catalog import EPISODES  # noqa: E402

ep_map = {e["id"]: e for e in EPISODES}
OWNED_SESSIONS = set()


def poll_and_finalize(ep: dict, sid: str) -> dict:
    ep_id = ep["id"]
    slug = ep["slug"]
    remote_mp4 = f"/content/{ep_id}_raw.mp4"
    remote_log = f"/content/render_{ep_id}.log"

    poll_py = Path(f"/tmp/poll_{ep_id}_{sid}.py")
    poll_py.write_text(
        f"""import os, pathlib
log_p = pathlib.Path("{remote_log}")
txt = log_p.read_text(encoding="utf-8", errors="ignore") if log_p.exists() else ""
bad_hits = [s for s in ("status: 404", "HTTP 404", "Failed to fetch", "Error:") if s in txt]
lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
print("LAST:", lines[-1] if lines else "waiting...", flush=True)
if bad_hits:
    print("BAD_LOG_HITS:", bad_hits, flush=True)
    print(txt[-600:], flush=True)
if os.path.exists("{remote_mp4}") and os.path.getsize("{remote_mp4}") > 2_000_000 and any("{remote_mp4}" in ln for ln in lines[-5:]):
    print("RENDER_DONE_SENTINEL", os.path.getsize("{remote_mp4}"), flush=True)
""",
        encoding="utf-8",
    )

    while True:
        time.sleep(35)
        try:
            p_res = orch.colab_run(["exec", "-s", sid, "--timeout", "75", "-f", str(poll_py)], timeout_sec=95)
            out = p_res.stdout
        except subprocess.TimeoutExpired:
            print(f"  [{sid} / {ep_id}] (kernel busy — continuing poll...)")
            continue
        for ln in out.splitlines():
            if ln.startswith("LAST:"):
                print(f"  [{sid} / {ep_id}] {ln}")
        if "BAD_LOG_HITS:" in out:
            raise RuntimeError(f"Render error on {sid} for {ep_id}:\n{out}")
        if "RENDER_DONE_SENTINEL" in out:
            break

    local_raw = Path(f"/tmp/{ep_id}_raw.mp4")
    print(f"[{sid}] Downloading {remote_mp4} -> {local_raw} ...")
    for dl_att in range(3):
        try:
            dl = orch.colab_run(["download", "-s", sid, remote_mp4, str(local_raw)], timeout_sec=360, lock=True)
            if dl.returncode == 0 and local_raw.exists() and local_raw.stat().st_size > 2_000_000:
                break
        except subprocess.TimeoutExpired:
            print(f"  [{sid}] Download retry {dl_att+1}...")
    assert local_raw.exists() and local_raw.stat().st_size > 2_000_000, f"Download failed for {ep_id}"

    ep_dir = orch.OUT_ROOT / slug
    wav_path = ep_dir / f"{slug}.wav"
    final_mp4 = ep_dir / f"{slug}.mp4"

    print(f"[{ep_id}] Muxing 256k AAC master MP4 ({final_mp4.name})...")
    subprocess.run(
        [
            "ffmpeg", "-nostdin", "-y", "-i", str(local_raw), "-i", str(wav_path),
            "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
            "-shortest", "-movflags", "+faststart", str(final_mp4),
        ],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )
    local_raw.unlink(missing_ok=True)
    dur_v = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(final_mp4)], text=True).strip())
    print(f"[{ep_id}] Master MP4 verified: {final_mp4.stat().st_size / 1e6:.1f} MB, {dur_v:.2f}s")
    return {"ep_id": ep_id, "slug": slug, "mp4": str(final_mp4), "duration_sec": round(dur_v, 2), "size_mb": round(final_mp4.stat().st_size / 1e6, 1)}


def launch_fresh_render_on_warm_worker(ep: dict, sid: str, concurrency: int = 10) -> dict:
    ep_id = ep["id"]
    slug = ep["slug"]
    tar_p, props_p = orch.build_episode_bundle(ep_id)
    remote_tar = f"/content/{ep_id}_assets.tar.gz"
    remote_props = f"/content/props_{ep_id}.json"
    remote_mp4 = f"/content/{ep_id}_raw.mp4"
    remote_log = f"/content/render_{ep_id}.log"

    print(f"[{sid}] Uploading {slug} bundle ({tar_p.stat().st_size / 1e6:.1f} MB)...")
    assert orch.colab_run(["upload", "-s", sid, str(tar_p), remote_tar], timeout_sec=240, lock=True).returncode == 0
    assert orch.colab_run(["upload", "-s", sid, str(props_p), remote_props], timeout_sec=90, lock=True).returncode == 0
    time.sleep(3)

    launch_py = Path(f"/tmp/launch_{ep_id}_{sid}.py")
    launch_py.write_text(
        f"""import subprocess
cmd = '''
set -e
cd /content/studio
tar -xzf {remote_tar}
rm -f {remote_mp4} {remote_log}
nohup ./node_modules/.bin/remotion render TamilDailyLifeDynamic {remote_mp4} --props={remote_props} --gl=angle --concurrency={concurrency} </dev/null >{remote_log} 2>&1 &
sleep 2
'''
subprocess.run(["bash", "-lc", cmd], check=True)
print("LAUNCHED_OK", flush=True)
""",
        encoding="utf-8",
    )
    l_res = orch.colab_run(["exec", "-s", sid, "--timeout", "75", "-f", str(launch_py)], timeout_sec=95)
    assert "LAUNCHED_OK" in l_res.stdout, f"Launch failed on {sid}: {l_res.stdout}"
    return poll_and_finalize(ep, sid)


def try_provision_second_worker(sid: str, code_tar: Path) -> tuple[bool, int]:
    for gpu_args, conc in [(["--gpu", "l4"], 10), (["--gpu", "t4", "--high-mem"], 8)]:
        print(f"[{sid}] Trying secondary Colab worker ({' '.join(gpu_args)})...")
        r = orch.colab_run(["new", *gpu_args, "-s", sid], timeout_sec=120, lock=True)
        if r.returncode == 0 or "already exists" in r.stdout:
            OWNED_SESSIONS.add(sid)
            time.sleep(3)
            up = orch.colab_run(["upload", "-s", sid, str(code_tar), "/content/women_studio_code.tar.gz"], timeout_sec=180, lock=True)
            if up.returncode != 0:
                orch.colab_run(["stop", "-s", sid], timeout_sec=30, lock=True)
                OWNED_SESSIONS.discard(sid)
                continue
            time.sleep(3)
            boot_f = Path(f"/tmp/boot_{sid}.py")
            boot_f.write_text(orch.BOOTSTRAP_PY, encoding="utf-8")
            ex = orch.colab_run(["exec", "-s", sid, "--timeout", "540", "-f", str(boot_f)], timeout_sec=580)
            if "BOOTSTRAP_COMPLETE_SENTINEL" in ex.stdout and "Traceback" not in ex.stdout:
                print(f"[{sid}] Secondary worker READY (concurrency={conc})!")
                return True, conc
            orch.colab_run(["stop", "-s", sid], timeout_sec=30, lock=True)
            OWNED_SESSIONS.discard(sid)
    print(f"[{sid}] No extra Colab GPU slot available right now; warm wom_ep02 will handle remaining queue.")
    return False, 0


def main():
    OWNED_SESSIONS.add("wom_ep02")
    code_tar = Path("/tmp/women_studio_code.tar.gz")
    if not code_tar.exists():
        code_tar = orch.build_lean_studio_tarball()

    pending_q: queue.Queue[dict] = queue.Queue()
    pending_q.put(ep_map["ep01"])
    pending_q.put(ep_map["ep03"])

    results: dict[str, dict] = {}
    errs: list[tuple[str, str]] = []

    def worker_wom_ep02():
        try:
            print("[wom_ep02] Attaching to in-progress ep02 render...")
            results["ep02"] = poll_and_finalize(ep_map["ep02"], "wom_ep02")
            while True:
                try:
                    nxt = pending_q.get_nowait()
                except queue.Empty:
                    break
                results[nxt["id"]] = launch_fresh_render_on_warm_worker(nxt, "wom_ep02", concurrency=10)
        except Exception as e:
            errs.append(("wom_ep02", str(e)))
        finally:
            print("Stopping owned Colab session wom_ep02...")
            orch.colab_run(["stop", "-s", "wom_ep02"], timeout_sec=45)

    def worker_secondary():
        ok, conc = try_provision_second_worker("wom_ep01", code_tar)
        if not ok:
            return
        try:
            while True:
                try:
                    nxt = pending_q.get_nowait()
                except queue.Empty:
                    break
                results[nxt["id"]] = launch_fresh_render_on_warm_worker(nxt, "wom_ep01", concurrency=conc)
        except Exception as e:
            errs.append(("wom_ep01", str(e)))
        finally:
            print("Stopping owned Colab session wom_ep01...")
            orch.colab_run(["stop", "-s", "wom_ep01"], timeout_sec=45)

    t_main = threading.Thread(target=worker_wom_ep02)
    t_sec = threading.Thread(target=worker_secondary)
    t_main.start()
    t_sec.start()
    t_main.join()
    t_sec.join()

    if errs or len(results) < 3:
        raise RuntimeError(f"Incomplete renders: got {list(results.keys())}, errs={errs}")

    print("\nSyncing all 3 Women's Series Pilot episodes + thumbnails + scripts to Google Drive...")
    subprocess.run(["rclone", "copy", str(orch.OUT_ROOT), orch.GDRIVE_ROOT, "--transfers", "8"], check=True)
    folder_link = subprocess.check_output(["rclone", "link", orch.GDRIVE_ROOT], text=True).strip()

    deliverables = {"folder_link": folder_link, "episodes": {}}
    for ep in EPISODES:
        ep_id = ep["id"]
        slug = ep["slug"]
        mp4_link = subprocess.check_output(["rclone", "link", f"{orch.GDRIVE_ROOT}/{slug}/{slug}.mp4"], text=True).strip()
        thumb_link = subprocess.check_output(["rclone", "link", f"{orch.GDRIVE_ROOT}/{slug}/{slug}_Thumbnail.jpg"], text=True).strip()
        script_link = subprocess.check_output(["rclone", "link", f"{orch.GDRIVE_ROOT}/{slug}/{slug}_Script.md"], text=True).strip()
        wav_link = subprocess.check_output(["rclone", "link", f"{orch.GDRIVE_ROOT}/{slug}/{slug}.wav"], text=True).strip()
        deliverables["episodes"][ep_id] = {
            **results[ep_id],
            "pillar": ep["pillar"],
            "yt_title": ep["yt_title"],
            "mp4_link": mp4_link,
            "thumb_link": thumb_link,
            "script_link": script_link,
            "wav_link": wav_link,
        }
        print(f"  [{ep_id}] MP4: {mp4_link} | Thumb: {thumb_link}")

    Path("/tmp/women_series_links.json").write_text(json.dumps(deliverables, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nALL_3_PILOTS_DELIVERED", folder_link)


if __name__ == "__main__":
    main()
