#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/home/shishyan/GitHub/Shishyan/GuruKulaDesam/tools/women_series/stage_women_324_batch.py
========================================================================================
Generalized Cloud-Queue Batch Builder for ANY episodes (`P1_002` .. `P3_108`) in `data/women_3pillars_324/`:
  - Stage 1 (`--audio`): Synthesizes `GuruKulaDesam` (`Mu63hpI1uigjGMdYVTDr`) @ 0.86x + `-14 LUFS` studio mix + `.opus` + 30fps RTA `.bin`
  - Stage 2 (`--visuals`): Generates 16 unique `nano-pro` 16:9 story shots ($0 video credits) + v2 Movie-Poster Thumbnail + QA sheets
  - Stage 3 (`--render-and-stage`): Detached (`nohup`) Colab L4 GPU render (`TamilDailyLifeDynamic` 1080p30) + `256k` AAC mux +
    immediate `colab stop` + `rclone copy` to `gdrive:GuruKulaDesam/Assets/women_3pillars_324/<pillar>/<ep_folder>/` so
    `.github/workflows/tamildailylife-women-3pillars-cloud.yml` publishes them automatically on schedule!
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_women_audio_and_visuals import (  # noqa: E402
    BG_CUE,
    INTER_CUE,
    INTRO_CUE,
    OUTRO_CUE,
    STUDIO_PUB,
    _gen_batch_or_single,
    dur_of,
    extract_spectrum_bin,
    map_sentences_rms_fallback,
    synth_gurukuladesam_voice,
)
from women_3pillars_catalog import SCENE_STYLE_PREFIX  # noqa: E402
import orchestrate_colab_l4 as orch  # noqa: E402
import finish_renders_and_sync as fin  # noqa: E402

REPO_ROOT = SCRIPT_DIR.parents[1]
DATA_ROOT = REPO_ROOT / "data" / "women_3pillars_324"
DRIVE_LOCAL_ROOT = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/women_3pillars_324")
GDRIVE_SERIES_ROOT = "gdrive:GuruKulaDesam/Assets/women_3pillars_324"

PILLAR_FOLDERS = {
    "P1": "pillar1_108_amman_varalaru",
    "P2": "pillar2_108_patti_vaithiyam",
    "P3": "pillar3_108_pooja_deepa_shastram",
}


def load_spec_and_dirs(ep_code: str) -> tuple[dict, Path, str]:
    p_code = ep_code.split("_")[0]
    p_sub = PILLAR_FOLDERS[p_code]
    matches = list((DATA_ROOT / p_sub).glob(f"{ep_code}_*/episode_spec.json"))
    assert matches, f"Could not find episode_spec.json for {ep_code}"
    spec_path = matches[0]
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    ep_folder_name = spec_path.parent.name
    local_out_dir = DRIVE_LOCAL_ROOT / p_sub / ep_folder_name
    local_out_dir.mkdir(parents=True, exist_ok=True)
    remote_dir = f"{GDRIVE_SERIES_ROOT}/{p_sub}/{ep_folder_name}"
    return spec, local_out_dir, remote_dir


def build_audio_for_codes(ep_codes: list[str], api_key: str) -> None:
    shared_work = Path("/tmp/women_series_cues")
    shared_work.mkdir(parents=True, exist_ok=True)
    intro_6s = shared_work / "cue_intro.wav"
    inter_a = shared_work / "cue_inter_a.wav"
    inter_b = shared_work / "cue_inter_b.wav"
    outro_12s = shared_work / "cue_outro.wav"
    bg_unit = shared_work / "bg_unit.wav"

    if not intro_6s.exists():
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", str(INTRO_CUE), "-af", "aresample=48000,aformat=channel_layouts=stereo,atrim=0:6.2,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.4,afade=t=out:st=4.6:d=1.6,loudnorm=I=-20:TP=-2.5:LRA=9", "-c:a", "pcm_s16le", str(intro_6s)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", str(INTER_CUE), "-af", "aresample=48000,aformat=channel_layouts=stereo,atrim=0:5.2,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.5,afade=t=out:st=3.8:d=1.4,loudnorm=I=-21:TP=-2.5:LRA=9", "-c:a", "pcm_s16le", str(inter_a)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", str(INTER_CUE), "-af", "aresample=48000,aformat=channel_layouts=stereo,atrim=2.0:7.2,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.6,afade=t=out:st=3.8:d=1.4,loudnorm=I=-21:TP=-2.5:LRA=9", "-c:a", "pcm_s16le", str(inter_b)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", str(OUTRO_CUE), "-af", "aresample=48000,aformat=channel_layouts=stereo,atrim=90.0:103.5,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=1.2,afade=t=out:st=10.0:d=3.5,loudnorm=I=-19:TP=-2.0:LRA=9", "-c:a", "pcm_s16le", str(outro_12s)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", str(BG_CUE), "-af", "aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-18:TP=-2.5:LRA=9", "-c:a", "pcm_s16le", str(bg_unit)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    for ec in ep_codes:
        spec, out_dir, _ = load_spec_and_dirs(ec)
        slug = spec["slug"]
        work = Path(f"/tmp/women_324_{ec}")
        work.mkdir(parents=True, exist_ok=True)

        print(f"\n=== [Audio] Synthesizing GuruKulaDesam Voice for {ec} ({slug}) ===")
        vo_paths = []
        voiced_with_bg = []
        bg_offsets = [0.0, 12.0, 24.0, 6.0, 18.0]

        for idx, sec in enumerate(spec["sections"]):
            vp = work / f"{sec['id']}.wav"
            if not vp.exists() or vp.stat().st_size < 10_000:
                synth_gurukuladesam_voice("\n\n".join(sec["paragraphs"]), vp, api_key)
            vdur = dur_of(vp)
            print(f"  [{ec}] {sec['id']}: {vdur:.2f}s")
            vo_paths.append(vp)

            v_out = work / f"vo_bedded_{idx+1}.wav"
            off = bg_offsets[idx]
            fc_v = (
                f"[0:a]apad=pad_dur=0.25,atrim=0:{vdur+0.25:.3f},asetpts=PTS-STARTPTS[v];"
                f"[1:a]aloop=loop=-1:size=2e+09,atrim={off}:{off+vdur+0.25:.3f},asetpts=PTS-STARTPTS,"
                f"volume=0.075,afade=t=in:st=0:d=0.4,afade=t=out:st={max(0.1, vdur-0.2):.3f}:d=0.45[b];"
                f"[v][b]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[out]"
            )
            subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", str(vp), "-i", str(bg_unit), "-filter_complex", fc_v, "-map", "[out]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(v_out)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            voiced_with_bg.append(v_out)

        sequence = [
            (intro_6s, 0.90),
            (voiced_with_bg[0], 0.45),
            (inter_a, 0.45),
            (voiced_with_bg[1], 0.45),
            (inter_b, 0.45),
            (voiced_with_bg[2], 0.45),
            (inter_a, 0.45),
            (voiced_with_bg[3], 0.45),
            (inter_b, 0.45),
            (voiced_with_bg[4], 1.10),
            (outro_12s, 0.0),
        ]
        cur_t = 0.0
        sec_starts = []
        for seq_i, (p, xf) in enumerate(sequence):
            if seq_i in (1, 3, 5, 7, 9):
                sec_starts.append(round(cur_t, 3))
            cur_t += dur_of(p) - xf

        inputs = []
        for p, _ in sequence:
            inputs.extend(["-i", str(p)])
        fc_chain = []
        prev = "[0:a]"
        for i in range(1, len(sequence)):
            xf_dur = sequence[i - 1][1]
            out_lbl = f"[m{i}]" if i < len(sequence) - 1 else "[pre_master]"
            fc_chain.append(f"{prev}[{i}:a]acrossfade=d={xf_dur}:c1=tri:c2=tri{out_lbl};")
            prev = out_lbl
        fc_chain.append("[pre_master]loudnorm=I=-14:TP=-1.5:LRA=9[out]")

        master_wav = out_dir / f"{slug}.wav"
        subprocess.run(["ffmpeg", "-nostdin", "-y", *inputs, "-filter_complex", "".join(fc_chain), "-map", "[out]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(master_wav)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        total_dur = dur_of(master_wav)

        opus_rel = f"audio/wom_{ec.lower()}.opus"
        opus_path = STUDIO_PUB / opus_rel
        opus_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", str(master_wav), "-c:a", "libopus", "-b:a", "192k", str(opus_path)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

        spec_name = f"wom_{ec.lower()}_spectrum.bin"
        n_frames = extract_spectrum_bin(master_wav, STUDIO_PUB / spec_name)

        captions = [
            {
                "startSec": 0.4,
                "endSec": round(sec_starts[0] - 0.15, 2),
                "badge": "@TamilDailyLife • மகளிர் சிறப்புத் தொடர்",
                "isDialogue": False,
                "line1": "சிவாயநம! • அன்பான தாய்மார்களே, சகோதரிகளே!",
                "line2": spec["title_pill"],
            }
        ]
        for idx, sec in enumerate(spec["sections"]):
            sec_caps = map_sentences_rms_fallback(vo_paths[idx], sec_starts[idx], sec["paragraphs"], sec["badge"], sec["is_story"])
            captions.extend([{k: v for k, v in c.items() if k != "writtenSentence"} for c in sec_caps])

        captions.append(
            {
                "startSec": round(total_dur - 11.8, 2),
                "endSec": round(total_dur - 1.4, 2),
                "badge": "@TamilDailyLife • ஆசீர்வாதம்",
                "isDialogue": False,
                "line1": "நல்லதே நினைப்போம் • நல்லதே நடக்கும்",
                "line2": "சிவாயநம!",
            }
        )

        alloc = [3, 3, 4, 4, 2]
        sec_spans = [
            (0.0, round(sec_starts[1] - 2.2, 2)),
            (round(sec_starts[1] - 2.2, 2), round(sec_starts[2] - 2.2, 2)),
            (round(sec_starts[2] - 2.2, 2), round(sec_starts[3] - 2.2, 2)),
            (round(sec_starts[3] - 2.2, 2), round(sec_starts[4] - 2.2, 2)),
            (round(sec_starts[4] - 2.2, 2), round(total_dur, 2)),
        ]
        shots = []
        shot_num = 1
        for (sp0, sp1), k in zip(sec_spans, alloc):
            for j in range(k):
                s0 = round(sp0 + (j / k) * (sp1 - sp0), 2)
                s1 = round(sp0 + ((j + 1) / k) * (sp1 - sp0), 2)
                shots.append({"shotNum": shot_num, "startSec": s0, "endSec": s1, "camPreset": ((shot_num - 1) * 3) % 8})
                shot_num += 1

        tl_data = {
            "ep_code": ec,
            "slug": slug,
            "titlePillText": spec["title_pill"],
            "durationSec": round(total_dur, 2),
            "durationInFrames": n_frames,
            "audioFile": opus_rel,
            "spectrumFile": spec_name,
            "shotsFolder": f"wom_{ec.lower()}",
            "shots": shots,
            "captions": captions,
        }
        (work / "episode_timeline.json").write_text(json.dumps(tl_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  => {ec} Audio+Spectrum+Timeline READY: {total_dur:.2f}s ({n_frames} frames)")


def build_visuals_for_codes(ep_codes: list[str]) -> None:
    items: list[tuple[str, Path, str]] = []
    for ec in ep_codes:
        spec, out_dir, _ = load_spec_and_dirs(ec)
        slug = spec["slug"]
        thumb_dst = out_dir / f"{slug}_Thumbnail.jpg"
        shot_dir = STUDIO_PUB / f"wom_{ec.lower()}"
        shot_dir.mkdir(parents=True, exist_ok=True)
        if not (thumb_dst.exists() and thumb_dst.stat().st_size > 45_000):
            items.append((spec["thumbnail_prompt"], thumb_dst, "thumb"))
        for s_idx, sp in enumerate(spec["shot_prompts"]):
            dst = shot_dir / f"shot_{s_idx+1:02d}.jpg"
            if not (dst.exists() and dst.stat().st_size > 45_000):
                items.append((SCENE_STYLE_PREFIX + sp, dst, "shot"))

    print(f"\n=== [Visuals] Generating {len(items)} nano-pro 16:9 items on nagaraj957 ===")
    if items:
        _gen_batch_or_single(items, "nagaraj957")

    qa_dir = Path("/tmp/women_324_qa")
    qa_dir.mkdir(parents=True, exist_ok=True)
    for ec in ep_codes:
        spec, out_dir, _ = load_spec_and_dirs(ec)
        shot_dir = STUDIO_PUB / f"wom_{ec.lower()}"
        hashes = set()
        sheet = Image.new("RGB", (1920, 1080), (12, 16, 28))
        draw = ImageDraw.Draw(sheet)
        shots_backup = out_dir / "shots"
        shots_backup.mkdir(parents=True, exist_ok=True)
        for idx in range(16):
            sp = shot_dir / f"shot_{idx+1:02d}.jpg"
            assert sp.exists() and sp.stat().st_size > 40_000, f"Missing {sp}"
            im_raw = Image.open(sp).convert("RGB")
            w, h = im_raw.size
            arr = np.array(im_raw)
            row_means = arr.mean(axis=(1, 2))
            if row_means[: int(h * 0.06)].mean() < 6.5 or row_means[int(h * 0.94) :].mean() < 6.5:
                valid = np.where(row_means > 8.0)[0]
                if len(valid) > h // 2:
                    y0, y1 = int(valid[0]) + 2, int(valid[-1]) - 1
                    nh = y1 - y0
                    nw = min(w, int(round(nh * 16 / 9)))
                    x0 = (w - nw) // 2
                    im_raw = im_raw.crop((x0, y0, x0 + nw, y0 + nh)).resize((w, h), Image.Resampling.LANCZOS)
                    im_raw.save(sp, format="JPEG", quality=92, optimize=True)
            hashes.add(hashlib.sha256(sp.read_bytes()).hexdigest())
            shutil.copy2(sp, shots_backup / f"shot_{idx+1:02d}.jpg")
            im = im_raw.resize((468, 256), Image.Resampling.LANCZOS)
            cx, cy = (idx % 4) * 480 + 6, (idx // 4) * 270 + 7
            sheet.paste(im, (cx, cy))
            draw.rectangle([cx + 6, cy + 6, cx + 106, cy + 32], fill=(0, 0, 0))
            draw.text((cx + 10, cy + 10), f"{ec} #{idx+1:02d}", fill=(255, 225, 120))
        assert len(hashes) == 16, f"{ec}: duplicate shots!"
        q_out = qa_dir / f"qa_storyboard_{ec}.jpg"
        sheet.save(q_out, format="JPEG", quality=88)
        print(f"  QA Storyboard saved: {q_out} (16/16 unique)")


def render_and_stage_codes(ep_codes: list[str]) -> None:
    ls_out = orch.colab_run(["sessions"], timeout_sec=30).stdout
    print(f"[Snapshot colab sessions]:\n{ls_out.strip()}")
    sid = "wom_batch_bg"
    code_tar = orch.build_lean_studio_tarball()

    try:
        provisioned = False
        for prov_args in (
            ["new", "--gpu", "l4", "-s", sid],
            ["new", "--gpu", "a100", "-s", sid],
            ["new", "--gpu", "t4", "--high-mem", "-s", sid],
            ["new", "--gpu", "t4", "-s", sid],
        ):
            try:
                print(f"Provisioning Colab GPU via: {' '.join(prov_args)} ...")
                r = orch.colab_run(prov_args, timeout_sec=180)
                if r.returncode == 0 or "already exists" in r.stdout:
                    print(f"Provisioned OK: {r.stdout.strip()}")
                    provisioned = True
                    break
                print(f"  -> {prov_args[2]} returned {r.returncode}: {r.stdout[-200:].strip()}")
            except subprocess.TimeoutExpired:
                print(f"  -> {prov_args[2]} timed out at 180s, trying fallback GPU...")
                orch.colab_run(["stop", "-s", sid], timeout_sec=30)
        assert provisioned, f"Could not provision Colab GPU for {sid}"
        time.sleep(5)
        assert orch.colab_run(["upload", "-s", sid, str(code_tar), "/content/women_studio_code.tar.gz"], timeout_sec=180).returncode == 0
        time.sleep(4)

        boot_sh = Path("/tmp/boot_batch_bg.py")
        boot_sh.write_text(
            r"""import pathlib, subprocess
sh = r'''#!/usr/bin/env bash
set -euo pipefail
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq fonts-noto-core fonts-taml fonts-indic fonts-deva fonts-noto-cjk fonts-noto-hinted
fc-cache -f -v >/dev/null
fc-list :lang=ta family | grep -i tamil || { echo "FATAL_NO_TAMIL_FONT"; exit 1; }
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpangocairo-1.0-0 libxshmfence1 libasound2t64
mkdir -p /content/studio && cd /content/studio
tar -xzf /content/women_studio_code.tar.gz
npm ci --prefer-offline || npm install
echo "BOOT_READY_SENTINEL"
'''
pathlib.Path('/content/boot.sh').write_text(sh)
subprocess.run(['bash', '-lc', 'chmod +x /content/boot.sh && nohup /content/boot.sh </dev/null >/content/boot.log 2>&1 & sleep 2'], check=True)
print('BOOT_LAUNCHED', flush=True)
""",
            encoding="utf-8",
        )
        orch.colab_run(["exec", "-s", sid, "--timeout", "45", "-f", str(boot_sh)], timeout_sec=65)
        chk_b = Path("/tmp/chk_boot_bg.py")
        chk_b.write_text("import pathlib; t = pathlib.Path('/content/boot.log').read_text() if pathlib.Path('/content/boot.log').exists() else ''; print(t[-300:])\n")
        for _ in range(30):
            time.sleep(15)
            out_b = orch.colab_run(["exec", "-s", sid, "--timeout", "35", "-f", str(chk_b)], timeout_sec=50).stdout
            if "BOOT_READY_SENTINEL" in out_b:
                print(f"[{sid}] Studio + Tamil fonts READY!")
                break
        else:
            raise RuntimeError(f"Bootstrap timed out on {sid}")

        for ec in ep_codes:
            spec, out_dir, remote_dir = load_spec_and_dirs(ec)
            slug = spec["slug"]
            tl = json.loads(Path(f"/tmp/women_324_{ec}/episode_timeline.json").read_text(encoding="utf-8"))
            props = {
                "titlePillText": tl["titlePillText"],
                "audioFile": tl["audioFile"],
                "spectrumFile": tl["spectrumFile"],
                "shotsFolder": tl["shotsFolder"],
                "fontFamily": "Noto Sans Tamil",
                "shots": tl["shots"],
                "captions": tl["captions"],
            }
            props_p = Path(f"/tmp/props_{ec}.json")
            props_p.write_text(json.dumps(props, ensure_ascii=False, indent=2), encoding="utf-8")
            tar_p = Path(f"/tmp/{ec}_assets.tar.gz")
            shot_dir = STUDIO_PUB / tl["shotsFolder"]
            with tarfile.open(tar_p, "w:gz") as tf:
                tf.add(STUDIO_PUB / tl["audioFile"], arcname=f"public/{tl['audioFile']}")
                tf.add(STUDIO_PUB / tl["spectrumFile"], arcname=f"public/{tl['spectrumFile']}")
                if (STUDIO_PUB / "GuruKulaDesam.png").exists():
                    tf.add(STUDIO_PUB / "GuruKulaDesam.png", arcname="public/GuruKulaDesam.png")
                for i in range(16):
                    tf.add(shot_dir / f"shot_{i+1:02d}.jpg", arcname=f"public/{tl['shotsFolder']}/shot_{i+1:02d}.jpg")

            assert orch.colab_run(["upload", "-s", sid, str(tar_p), f"/content/{ec}_assets.tar.gz"], timeout_sec=240).returncode == 0
            time.sleep(3)
            assert orch.colab_run(["upload", "-s", sid, str(props_p), f"/content/props_{ec}.json"], timeout_sec=90).returncode == 0
            time.sleep(5)

            # Render a proof still on the first episode of the batch per Rule 1.4.2
            if ec == ep_codes[0]:
                still_py = Path(f"/tmp/still_{ec}_bg.py")
                still_py.write_text(
                    f"""import subprocess
cmd = '''
set -e
cd /content/studio
tar -xzf /content/{ec}_assets.tar.gz
./node_modules/.bin/remotion still TamilDailyLifeDynamic /content/{ec}_proof.jpg --frame=450 --props=/content/props_{ec}.json --gl=angle --image-format=jpeg
ls -lh /content/{ec}_proof.jpg
'''
subprocess.run(["bash", "-lc", cmd], check=True)
print("PROOF_STILL_OK", flush=True)
""",
                    encoding="utf-8",
                )
                orch.colab_run(["exec", "-s", sid, "--timeout", "120", "-f", str(still_py)], timeout_sec=140)
                orch.colab_run(["download", "-s", sid, f"/content/{ec}_proof.jpg", f"/tmp/women_324_qa/proof_still_{ec}.jpg"], timeout_sec=90)
                print(f"[{sid}] Proof still downloaded -> /tmp/women_324_qa/proof_still_{ec}.jpg")

            l_py = Path(f"/tmp/launch_{ec}_bg.py")
            l_py.write_text(
                f"""import subprocess
cmd = '''
set -e
cd /content/studio
tar -xzf /content/{ec}_assets.tar.gz
rm -f /content/{ec}_raw.mp4 /content/render_{ec}.log
nohup ./node_modules/.bin/remotion render TamilDailyLifeDynamic /content/{ec}_raw.mp4 --props=/content/props_{ec}.json --gl=angle --concurrency=$(python3 -c 'import os; print(max(1, min(10, os.cpu_count() or 2)))') </dev/null >/content/render_{ec}.log 2>&1 &
sleep 2
'''
subprocess.run(["bash", "-lc", cmd], check=True)
print("LAUNCHED_OK", flush=True)
""",
                encoding="utf-8",
            )
            orch.colab_run(["exec", "-s", sid, "--timeout", "60", "-f", str(l_py)], timeout_sec=80)
            print(f"[{sid}] Rendering {ec} ({slug})...")

            poll_py = Path(f"/tmp/poll_{ec}_bg.py")
            poll_py.write_text(
                f"""import os, pathlib
p = pathlib.Path('/content/render_{ec}.log')
t = p.read_text(errors='ignore') if p.exists() else ''
lines = [x.strip() for x in t.splitlines() if x.strip()]
print('LAST:', lines[-1] if lines else 'waiting...')
if any(err in t for err in ('Error:', 'FATAL', 'status: 404', 'HTTP 404', 'Failed to fetch')):
    print('RENDER_ERROR_SENTINEL')
    print(t[-800:])
if os.path.exists('/content/{ec}_raw.mp4') and os.path.getsize('/content/{ec}_raw.mp4') > 2_000_000 and any('/content/{ec}_raw.mp4' in x for x in lines[-5:]):
    print('RENDER_DONE_SENTINEL')
""",
                encoding="utf-8",
            )
            while True:
                time.sleep(35)
                try:
                    po = orch.colab_run(["exec", "-s", sid, "--timeout", "75", "-f", str(poll_py)], timeout_sec=95).stdout
                except subprocess.TimeoutExpired:
                    continue
                for ln in po.splitlines():
                    if ln.startswith("LAST:"):
                        print(f"  [{sid} / {ec}] {ln}")
                if "RENDER_ERROR_SENTINEL" in po:
                    raise RuntimeError(f"Remotion render error on {ec}:\n{po}")
                if "RENDER_DONE_SENTINEL" in po:
                    break

            raw_mp4 = Path(f"/tmp/{ec}_raw.mp4")
            orch.colab_run(["download", "-s", sid, f"/content/{ec}_raw.mp4", str(raw_mp4)], timeout_sec=360)
            final_mp4 = out_dir / f"{slug}.mp4"
            wav_path = out_dir / f"{slug}.wav"
            subprocess.run(["ffmpeg", "-nostdin", "-y", "-i", str(raw_mp4), "-i", str(wav_path), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", str(final_mp4)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            raw_mp4.unlink(missing_ok=True)
            subprocess.run(["rclone", "copy", str(out_dir), remote_dir, "--transfers", "6"], check=True)
            mp4_link = subprocess.check_output(["rclone", "link", f"{remote_dir}/{slug}.mp4"], text=True).strip()
            thumb_link = subprocess.check_output(["rclone", "link", f"{remote_dir}/{slug}_Thumbnail.jpg"], text=True).strip()
            print(f"[{ec}] STAGED TO CLOUD QUEUE -> MP4: {mp4_link} | THUMB: {thumb_link}")
    finally:
        print(f"Stopping owned Colab session {sid}...")
        orch.colab_run(["stop", "-s", sid], timeout_sec=45)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ep_codes", nargs="+")
    ap.add_argument("--api-key", default=os.environ.get("ELEVENLABS_WOMEN_API_KEY", ""))
    ap.add_argument("--audio", action="store_true")
    ap.add_argument("--visuals", action="store_true")
    ap.add_argument("--render-and-stage", action="store_true")
    args = ap.parse_args()

    if args.audio:
        assert args.api_key
        build_audio_for_codes(args.ep_codes, args.api_key)
    if args.visuals:
        build_visuals_for_codes(args.ep_codes)
    if args.render_and_stage:
        render_and_stage_codes(args.ep_codes)


if __name__ == "__main__":
    main()
