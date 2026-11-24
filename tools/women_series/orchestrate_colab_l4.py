#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/home/shishyan/GitHub/Shishyan/GuruKulaDesam/tools/women_series/orchestrate_colab_l4.py
======================================================================================
Cloud GPU Orchestrator (Colab L4 CLI):
  1. `--prepare-and-whisper`:
     - Builds lean studio code tarball (`/tmp/women_studio_code.tar.gz`) & vocal stems tarball (`/tmp/women_stems.tar.gz`)
     - Provisions `wom_l4_1` & `wom_l4_2` (`--gpu l4`) without touching any pre-existing sessions
     - Installs Tamil fonts in their own dedicated apt call + verifies `fc-list :lang=ta`
     - Installs Chromium libs in a separate apt call + runs `npm ci --prefer-offline`
     - Runs `faster-whisper` (`large-v3`, CUDA) on `wom_l4_1` and downloads `/tmp/aligned_captions_out.json`
  2. `--proof-still`:
     - Packages `ep01` bundle + Whisper-aligned `props_ep01.json`, uploads to `wom_l4_1`,
       renders `remotion still` at frame 540, and downloads `/tmp/women_series_qa/proof_ep01.png` for `read_file` QA!
  3. `--render-and-deliver`:
     - Renders `ep01` & `ep03` on `wom_l4_1` and `ep02` on `wom_l4_2` in parallel (`--gl=angle --concurrency=12`)
     - Verifies zero `status: 404` / `HTTP 404` / `Failed to fetch` / `Error:` in `/content/render.log`
     - Downloads raw MP4s, muxes `256k` AAC audio from `-14 LUFS` master WAVs (`-movflags +faststart`)
     - Immediately stops `wom_l4_1` & `wom_l4_2` (`colab stop`)
     - Syncs all `.mp4`, `.wav`, `_Script.md`, `_Description.txt`, and `_Thumbnail.jpg` to Google Drive via `rclone copy`
       and saves clickable `rclone link` URLs to `/tmp/women_series_links.json`!
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tarfile
import threading
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from women_3pillars_catalog import EPISODES  # noqa: E402

COLAB = "/home/shishyan/GuruKulaDesam_Local/.venv/bin/colab"
STUDIO_DIR = Path("/home/shishyan/GitHub/tamil-lyric-studio")
STUDIO_PUB = STUDIO_DIR / "public"
OUT_ROOT = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots")
GDRIVE_ROOT = "gdrive:GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots"

SESSIONS = ["wom_l4_1", "wom_l4_2"]
colab_lock = threading.Lock()


def colab_run(args: list[str], timeout_sec: int = 240, lock: bool = False) -> subprocess.CompletedProcess:
    if lock:
        with colab_lock:
            return subprocess.run([COLAB, *args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=timeout_sec)
    return subprocess.run([COLAB, *args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=timeout_sec)


def build_lean_studio_tarball() -> Path:
    tar_path = Path("/tmp/women_studio_code.tar.gz")
    with tarfile.open(tar_path, "w:gz") as tf:
        for fname in ("package.json", "package-lock.json", "tsconfig.json", "remotion.config.ts"):
            p = STUDIO_DIR / fname
            if p.exists():
                tf.add(p, arcname=fname)
        tf.add(STUDIO_DIR / "src", arcname="src")
        if (STUDIO_PUB / "fonts").exists():
            tf.add(STUDIO_PUB / "fonts", arcname="public/fonts")
        if (STUDIO_PUB / "GuruKulaDesam.png").exists():
            tf.add(STUDIO_PUB / "GuruKulaDesam.png", arcname="public/GuruKulaDesam.png")
    print(f"Built lean studio tarball: {tar_path} ({tar_path.stat().st_size / 1e6:.2f} MB)")
    return tar_path


def build_stems_tarball() -> Path:
    tar_path = Path("/tmp/women_stems.tar.gz")
    if tar_path.exists() and 5_000_000 < tar_path.stat().st_size < 60_000_000:
        print(f"Reusing slim 16kHz stems tarball: {tar_path} ({tar_path.stat().st_size / 1e6:.2f} MB)")
        return tar_path
    slim_dir = Path("/tmp/stems_16k")
    slim_dir.mkdir(parents=True, exist_ok=True)
    timelines = {}
    with tarfile.open(tar_path, "w:gz") as tf:
        for ep in EPISODES:
            ep_id = ep["id"]
            work = Path(f"/tmp/women_series_{ep_id}")
            tl = json.loads((work / "episode_timeline.json").read_text(encoding="utf-8"))
            timelines[ep_id] = tl
            for sm in tl["stem_manifest"]:
                sec_wav = work / f"{sm['sec_id']}.wav"
                dst = slim_dir / sm["stem_wav"]
                subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", str(sec_wav), "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(dst)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                tf.add(dst, arcname=f"stems/{sm['stem_wav']}")
        tl_in = Path("/tmp/timelines_in.json")
        tl_in.write_text(json.dumps(timelines, ensure_ascii=False, indent=2), encoding="utf-8")
        tf.add(tl_in, arcname="stems/timelines_in.json")
    print(f"Built slim 16kHz vocal stems tarball: {tar_path} ({tar_path.stat().st_size / 1e6:.2f} MB)")
    return tar_path


BOOTSTRAP_PY = """import subprocess

def run_step(title, cmd):
    print(f"=== {title} ===", flush=True)
    p = subprocess.Popen(["bash", "-lc", cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in p.stdout:
        print(line, end="", flush=True)
    rc = p.wait()
    if rc != 0:
        raise RuntimeError(f"{title} failed with exit code {rc}")

# 1. Dedicated Tamil fonts apt call + fc-list verification (Hard Requirement 1.4.2)
run_step("TAMIL_FONTS", '''
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq fonts-noto-core fonts-taml fonts-indic fonts-deva fonts-noto-cjk fonts-noto-hinted
fc-cache -f -v >/dev/null
fc-list :lang=ta family | grep -i tamil || { echo "FATAL: no Tamil font"; exit 1; }
''')

# 2. Separate Chromium system libraries apt call
run_step("CHROMIUM_LIBS", '''
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpangocairo-1.0-0 libxshmfence1 libasound2t64
''')

# 3. Extract lean studio tarball & npm ci
run_step("STUDIO_NPM_CI", '''
set -e
mkdir -p /content/studio
cd /content/studio
tar -xzf /content/women_studio_code.tar.gz
npm ci --prefer-offline || npm install
''')

print("BOOTSTRAP_COMPLETE_SENTINEL", flush=True)
"""


def _provision_and_bootstrap_worker(sid: str, code_tar: Path) -> None:
    probe_f = Path(f"/tmp/probe_{sid}.py")
    probe_f.write_text(
        "import os, subprocess\n"
        "has_rem = os.path.exists('/content/studio/node_modules/.bin/remotion')\n"
        "fc = subprocess.run(['bash', '-lc', 'fc-list :lang=ta family | grep -i tamil'], stdout=subprocess.PIPE, text=True)\n"
        "print('READY_ALREADY' if (has_rem and fc.returncode == 0) else 'NEEDS_SETUP')\n",
        encoding="utf-8",
    )
    chk = colab_run(["exec", "-s", sid, "--timeout", "35", "-f", str(probe_f)], timeout_sec=50)
    if chk.returncode == 0 and "READY_ALREADY" in chk.stdout:
        print(f"[{sid}] Already bootstrapped & Tamil fonts verified — skipping setup!")
        return

    print(f"[{sid}] Provisioning fresh Colab L4 GPU session...")
    colab_run(["stop", "-s", sid], timeout_sec=30, lock=True)
    r_new = colab_run(["new", "--gpu", "l4", "-s", sid], timeout_sec=150, lock=True)
    if r_new.returncode != 0 and "already exists" not in r_new.stdout:
        raise RuntimeError(f"colab new failed for {sid}: {r_new.stdout}")
    time.sleep(3)

    up = colab_run(["upload", "-s", sid, str(code_tar), "/content/women_studio_code.tar.gz"], timeout_sec=180, lock=True)
    assert up.returncode == 0, f"Upload studio code failed on {sid}: {up.stdout}"
    time.sleep(3)  # Settle guard (Rule 1.4.4)

    boot_file = Path(f"/tmp/boot_{sid}.py")
    boot_file.write_text(BOOTSTRAP_PY, encoding="utf-8")
    ex = colab_run(["exec", "-s", sid, "--timeout", "540", "-f", str(boot_file)], timeout_sec=580)
    if "Traceback" in ex.stdout or "BOOTSTRAP_COMPLETE_SENTINEL" not in ex.stdout:
        raise RuntimeError(f"Bootstrap failed on {sid}:\n{ex.stdout[-800:]}")
    print(f"[{sid}] Bootstrap & Tamil font verification PASSED!")


def prepare_and_whisper() -> None:
    ls_out = colab_run(["ls"], timeout_sec=30).stdout
    print(f"[Snapshot colab ls]:\n{ls_out.strip()}")

    code_tar = build_lean_studio_tarball()
    stems_tar = build_stems_tarball()

    errs = []

    def _boot(sid: str):
        try:
            _provision_and_bootstrap_worker(sid, code_tar)
        except Exception as e:
            errs.append((sid, str(e)))

    threads = [threading.Thread(target=_boot, args=(s,)) for s in SESSIONS]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    if errs:
        raise RuntimeError(f"Worker bootstrap errors: {errs}")

    # Run Whisper large-v3 forced alignment on wom_l4_1 in a child python3 process so LD_LIBRARY_PATH applies to dlopen!
    print("[wom_l4_1] Uploading vocal stems & running CUDA faster-whisper large-v3 forced alignment...")
    chk_stems = Path("/tmp/chk_stems.py")
    chk_stems.write_text("import os; print('HAS_STEMS' if os.path.exists('/content/stems/timelines_in.json') else 'NO_STEMS')\n")
    if "HAS_STEMS" not in colab_run(["exec", "-s", "wom_l4_1", "--timeout", "30", "-f", str(chk_stems)], timeout_sec=45).stdout:
        up_s = colab_run(["upload", "-s", "wom_l4_1", str(stems_tar), "/content/women_stems.tar.gz"], timeout_sec=180)
        assert up_s.returncode == 0, up_s.stdout
        time.sleep(3)

    assert colab_run(["upload", "-s", "wom_l4_1", str(SCRIPT_DIR / "colab_whisper_align_remote.py"), "/content/colab_whisper_align_remote.py"], timeout_sec=60).returncode == 0
    time.sleep(2)

    extract_and_run = Path("/tmp/run_whisper_wom.py")
    extract_and_run.write_text(
        """import glob, os, subprocess, sys
if not os.path.exists('/content/stems/timelines_in.json'):
    subprocess.run(['tar', '-xzf', '/content/women_stems.tar.gz', '-C', '/content'], check=True)
subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'faster-whisper', 'nvidia-cublas-cu12', 'nvidia-cudnn-cu12'], check=True)
ld_dirs = set()
for pattern in ('/usr/**/libcublas.so.12*', '/usr/**/libcudnn.so.9*', '/root/**/libcublas.so.12*'):
    for m in glob.glob(pattern, recursive=True):
        ld_dirs.add(os.path.dirname(m))
env = os.environ.copy()
env['LD_LIBRARY_PATH'] = ':'.join(sorted(ld_dirs) + [env.get('LD_LIBRARY_PATH', '')])
print('LD_LIBRARY_PATH dirs:', sorted(ld_dirs), flush=True)
p = subprocess.Popen([sys.executable, '/content/colab_whisper_align_remote.py'], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
for line in p.stdout:
    print(line, end='', flush=True)
rc = p.wait()
if rc != 0:
    raise RuntimeError(f'Whisper subprocess exited with {rc}')
""",
        encoding="utf-8",
    )
    w_res = colab_run(["exec", "-s", "wom_l4_1", "--timeout", "420", "-f", str(extract_and_run)], timeout_sec=460)
    print(w_res.stdout[-1200:])
    if "Traceback" in w_res.stdout or "WHISPER_ALIGNMENT_COMPLETE" not in w_res.stdout:
        raise RuntimeError(f"Whisper alignment failed:\n{w_res.stdout[-800:]}")

    dl = colab_run(["download", "-s", "wom_l4_1", "/content/aligned_captions_out.json", "/tmp/aligned_captions_out.json"], timeout_sec=90)
    assert dl.returncode == 0, dl.stdout

    # Merge Whisper-aligned captions back into episode_timeline.json
    aligned_map = json.loads(Path("/tmp/aligned_captions_out.json").read_text(encoding="utf-8"))
    for ep in EPISODES:
        ep_id = ep["id"]
        tl_p = Path(f"/tmp/women_series_{ep_id}/episode_timeline.json")
        tl = json.loads(tl_p.read_text(encoding="utf-8"))
        if ep_id in aligned_map and len(aligned_map[ep_id]) >= 10:
            tl["captions"] = aligned_map[ep_id]
            tl_p.write_text(json.dumps(tl, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  Updated {ep_id} timeline with {len(tl['captions'])} GPU Whisper-aligned captions!")


def build_episode_bundle(ep_id: str) -> tuple[Path, Path]:
    shot_dir = STUDIO_PUB / f"women_{ep_id}"
    while not all((shot_dir / f"shot_{i+1:02d}.jpg").exists() and (shot_dir / f"shot_{i+1:02d}.jpg").stat().st_size > 45_000 for i in range(16)):
        ready_n = sum(1 for i in range(16) if (shot_dir / f"shot_{i+1:02d}.jpg").exists() and (shot_dir / f"shot_{i+1:02d}.jpg").stat().st_size > 45_000)
        print(f"  [Bundle {ep_id}] Waiting for all 16 shots ({ready_n}/16 ready)...")
        time.sleep(12)

    tl_p = Path(f"/tmp/women_series_{ep_id}/episode_timeline.json")
    tl = json.loads(tl_p.read_text(encoding="utf-8"))
    props = {
        "titlePillText": tl["titlePillText"],
        "audioFile": tl["audioFile"],
        "spectrumFile": tl["spectrumFile"],
        "shotsFolder": tl["shotsFolder"],
        "fontFamily": "Noto Sans Tamil",
        "shots": tl["shots"],
        "captions": tl["captions"],
    }
    props_p = Path(f"/tmp/props_women_{ep_id}.json")
    props_p.write_text(json.dumps(props, ensure_ascii=False, indent=2), encoding="utf-8")

    tar_p = Path(f"/tmp/women_{ep_id}_assets.tar.gz")
    with tarfile.open(tar_p, "w:gz") as tf:
        tf.add(STUDIO_PUB / tl["audioFile"], arcname=f"public/{tl['audioFile']}")
        tf.add(STUDIO_PUB / tl["spectrumFile"], arcname=f"public/{tl['spectrumFile']}")
        if (STUDIO_PUB / "GuruKulaDesam.png").exists():
            tf.add(STUDIO_PUB / "GuruKulaDesam.png", arcname="public/GuruKulaDesam.png")
        for idx in range(16):
            sp = shot_dir / f"shot_{idx+1:02d}.jpg"
            assert sp.exists(), f"Missing {sp}"
            tf.add(sp, arcname=f"public/women_{ep_id}/shot_{idx+1:02d}.jpg")
    return tar_p, props_p


def run_proof_still() -> None:
    tar_p, props_p = build_episode_bundle("ep01")
    assert colab_run(["upload", "-s", "wom_l4_1", str(tar_p), "/content/ep01_assets.tar.gz"], timeout_sec=180).returncode == 0
    assert colab_run(["upload", "-s", "wom_l4_1", str(props_p), "/content/props_ep01.json"], timeout_sec=60).returncode == 0
    time.sleep(3)

    still_py = Path("/tmp/still_wom.py")
    still_py.write_text(
        """import subprocess
cmd = '''
set -e
cd /content/studio
tar -xzf /content/ep01_assets.tar.gz
./node_modules/.bin/remotion still TamilDailyLifeDynamic /content/proof_ep01.png --frame=540 --props=/content/props_ep01.json --gl=angle
'''
p = subprocess.run(["bash", "-lc", cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
print(p.stdout)
if p.returncode != 0:
    raise RuntimeError("remotion still failed")
print("PROOF_STILL_READY", flush=True)
""",
        encoding="utf-8",
    )
    res = colab_run(["exec", "-s", "wom_l4_1", "--timeout", "180", "-f", str(still_py)], timeout_sec=210)
    if "Traceback" in res.stdout or "PROOF_STILL_READY" not in res.stdout:
        raise RuntimeError(f"Proof still failed:\n{res.stdout[-800:]}")

    Path("/tmp/women_series_qa").mkdir(parents=True, exist_ok=True)
    dl = colab_run(["download", "-s", "wom_l4_1", "/content/proof_ep01.png", "/tmp/women_series_qa/proof_ep01.png"], timeout_sec=90)
    assert dl.returncode == 0, dl.stdout
    print("Downloaded Colab proof still -> /tmp/women_series_qa/proof_ep01.png")


def _render_one_on_worker(ep: dict, sid: str) -> dict:
    ep_id = ep["id"]
    slug = ep["slug"]
    tar_p, props_p = build_episode_bundle(ep_id)
    remote_tar = f"/content/{ep_id}_assets.tar.gz"
    remote_props = f"/content/props_{ep_id}.json"
    remote_mp4 = f"/content/{ep_id}_raw.mp4"
    remote_log = f"/content/render_{ep_id}.log"

    print(f"[{sid}] Uploading {slug} bundle ({tar_p.stat().st_size / 1e6:.1f} MB)...")
    assert colab_run(["upload", "-s", sid, str(tar_p), remote_tar], timeout_sec=180, lock=True).returncode == 0
    assert colab_run(["upload", "-s", sid, str(props_p), remote_props], timeout_sec=60, lock=True).returncode == 0
    time.sleep(3)

    launch_py = Path(f"/tmp/launch_{ep_id}.py")
    launch_py.write_text(
        f"""import subprocess
cmd = '''
set -e
cd /content/studio
tar -xzf {remote_tar}
rm -f {remote_mp4} {remote_log}
nohup ./node_modules/.bin/remotion render TamilDailyLifeDynamic {remote_mp4} --props={remote_props} --gl=angle --concurrency=10 </dev/null >{remote_log} 2>&1 &
sleep 2
'''
subprocess.run(["bash", "-lc", cmd], check=True)
print("LAUNCHED_OK", flush=True)
""",
        encoding="utf-8",
    )
    l_res = colab_run(["exec", "-s", sid, "--timeout", "60", "-f", str(launch_py)], timeout_sec=90)
    assert "LAUNCHED_OK" in l_res.stdout, f"Launch failed on {sid}: {l_res.stdout}"

    poll_py = Path(f"/tmp/poll_{ep_id}.py")
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
            p_res = colab_run(["exec", "-s", sid, "--timeout", "75", "-f", str(poll_py)], timeout_sec=95)
            out = p_res.stdout
        except subprocess.TimeoutExpired:
            print(f"  [{sid} / {ep_id}] (kernel busy under 10x render load — continuing poll...)")
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
    dl = colab_run(["download", "-s", sid, remote_mp4, str(local_raw)], timeout_sec=300, lock=True)
    assert dl.returncode == 0 and local_raw.exists(), f"Download failed for {ep_id}: {dl.stdout}"

    ep_dir = OUT_ROOT / slug
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


def render_and_deliver() -> None:
    import queue as _q
    q = _q.Queue()
    for ep in EPISODES:
        q.put(ep)

    results = {}
    errs = []

    def _worker_loop(sid: str):
        try:
            while True:
                try:
                    ep = q.get_nowait()
                except _q.Empty:
                    break
                results[ep["id"]] = _render_one_on_worker(ep, sid)
                q.task_done()
        except Exception as e:
            errs.append((sid, str(e)))
        finally:
            print(f"Stopping Colab session {sid} immediately...")
            colab_run(["stop", "-s", sid], timeout_sec=45)

    t1 = threading.Thread(target=_worker_loop, args=("wom_l4_1",))
    t2 = threading.Thread(target=_worker_loop, args=("wom_l4_2",))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    if errs:
        raise RuntimeError(f"Render lane errors: {errs}")

    # Sync all 3 episode directories to Google Drive & fetch clickable rclone links!
    print("\nSyncing all 3 Women's Series Pilot episodes + thumbnails + scripts to Google Drive...")
    subprocess.run(["rclone", "copy", str(OUT_ROOT), GDRIVE_ROOT, "--transfers", "8"], check=True)
    folder_link = subprocess.check_output(["rclone", "link", GDRIVE_ROOT], text=True).strip()

    deliverables = {"folder_link": folder_link, "episodes": {}}
    for ep in EPISODES:
        ep_id = ep["id"]
        slug = ep["slug"]
        mp4_link = subprocess.check_output(["rclone", "link", f"{GDRIVE_ROOT}/{slug}/{slug}.mp4"], text=True).strip()
        thumb_link = subprocess.check_output(["rclone", "link", f"{GDRIVE_ROOT}/{slug}/{slug}_Thumbnail.jpg"], text=True).strip()
        script_link = subprocess.check_output(["rclone", "link", f"{GDRIVE_ROOT}/{slug}/{slug}_Script.md"], text=True).strip()
        wav_link = subprocess.check_output(["rclone", "link", f"{GDRIVE_ROOT}/{slug}/{slug}.wav"], text=True).strip()
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
    print("\nALL_DELIVERABLES_SYNCED", folder_link)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare-and-whisper", action="store_true")
    ap.add_argument("--proof-still", action="store_true")
    ap.add_argument("--render-and-deliver", action="store_true")
    args = ap.parse_args()

    if args.prepare_and_whisper:
        prepare_and_whisper()
    if args.proof_still:
        run_proof_still()
    if args.render_and_deliver:
        render_and_deliver()


if __name__ == "__main__":
    main()
