#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/gdrive_asset_sync.py
Canonical Google Drive Asset Resolver & Sync Engine for GuruKulaDesam.

Replaces Git LFS with direct Google Drive references (`nagaraj957@gmail.com` — 20 TB Drive)
indexed in `production/gdrive_assets_manifest.json`.

Usage:
  # Check manifest statistics & local/Drive coverage:
  python3 tools/gdrive_asset_sync.py --status

  # Fetch/hydrate specific path(s) or prefix from Google Drive into local working tree:
  python3 tools/gdrive_asset_sync.py --pull production/audio
  python3 tools/gdrive_asset_sync.py --pull production/thumbnails/--4jzoezBW8.png

  # On local workstation (/media/shishyan/Shishyan/GitHub/Gurukuladesam):
  # Upload any remaining local-only renders/videos to Google Drive and update manifest:
  python3 tools/gdrive_asset_sync.py --push-local-missing
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "production" / "gdrive_assets_manifest.json"
GVFS_ROOT = Path("/run/user/1000/gvfs/google-drive:host=gmail.com,user=nagaraj957/0AO7hUVqpfVvgUk9PVA")

GDRIVE_FLOW_RENDERS_FOLDER = "1h56SWy0pqeuU2Q_W2ECk_ZCTqe61ynbA"
GDRIVE_MIGRATION_FOLDER = "1d_OcxMEjcq7MVqMmO9U3u_Mpnwe-hrZk"


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        return {"version": 1, "account": "nagaraj957@gmail.com", "assets": {}}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def save_manifest(data: dict) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def find_gdrive_cli() -> str | None:
    for candidate in ("/tmp/gdrive_fast", "/opt/antigravity/bin/gdrive", shutil.which("gdrive")):
        if candidate and Path(candidate).exists():
            return str(candidate)
    return None


def resolve_asset(rel_path: str, download_if_missing: bool = False) -> Path | None:
    """
    Resolves a repository-relative asset path (e.g. `production/audio/--4jzoezBW8.m4a`):
      1. If local file exists and is a real binary (>300 bytes), returns it immediately.
      2. If Google Drive GVFS mount is active on the workstation and the Drive path exists, returns it.
      3. If `download_if_missing=True` and `gdrive_file_id` is in `gdrive_assets_manifest.json`,
         downloads the file via `gdrive readonly download` into the local path and returns it.
    """
    local_p = ROOT / rel_path
    if local_p.exists() and local_p.stat().st_size > 300:
        return local_p

    manifest = load_manifest()
    entry = manifest.get("assets", {}).get(rel_path)
    if not entry:
        return None

    # Check local GVFS mount if available
    gvfs_rel = entry.get("gdrive_path")
    if gvfs_rel and GVFS_ROOT.exists():
        gvfs_candidate = GVFS_ROOT / gvfs_rel
        if gvfs_candidate.exists() and gvfs_candidate.stat().st_size > 300:
            return gvfs_candidate

    file_id = entry.get("gdrive_file_id")
    if download_if_missing and file_id:
        gdrive_bin = find_gdrive_cli()
        if gdrive_bin:
            local_p.parent.mkdir(parents=True, exist_ok=True)
            res = subprocess.run(
                [gdrive_bin, "readonly", "download", file_id, "--out", str(local_p)],
                capture_output=True, text=True
            )
            if res.returncode == 0 and local_p.exists() and local_p.stat().st_size > 300:
                return local_p

    return None


def cmd_status() -> None:
    manifest = load_manifest()
    assets = manifest.get("assets", {})
    total = len(assets)
    with_id = sum(1 for v in assets.values() if v.get("gdrive_file_id"))
    local_real = sum(1 for k in assets if (ROOT / k).exists() and (ROOT / k).stat().st_size > 300)
    total_mb = sum(v.get("size", 0) for v in assets.values()) / (1024 * 1024)
    id_mb = sum(v.get("size", 0) for v in assets.values() if v.get("gdrive_file_id")) / (1024 * 1024)

    print("═══════════════════════════════════════════════════════════════════════")
    print("  GURUKULADESAM GOOGLE DRIVE ASSET MANIFEST STATUS (LFS REPLACEMENT)")
    print("═══════════════════════════════════════════════════════════════════════")
    print(f"  Google Drive Account : {manifest.get('account', 'nagaraj957@gmail.com')}")
    print(f"  Total Indexed Paths  : {total:,} paths ({total_mb:,.2f} MB)")
    print(f"  Mapped in GDrive     : {with_id:,} / {total:,} paths ({id_mb:,.2f} MB)")
    print(f"  Hydrated Locally     : {local_real:,} paths")
    print("═══════════════════════════════════════════════════════════════════════")


def cmd_pull(prefix: str, workers: int = 8) -> None:
    manifest = load_manifest()
    assets = manifest.get("assets", {})
    targets = [
        (rel, info) for rel, info in assets.items()
        if (rel == prefix or rel.startswith(prefix.rstrip("/") + "/")) and info.get("gdrive_file_id")
    ]
    if not targets:
        print(f"No manifest entries with gdrive_file_id matching '{prefix}'.")
        return

    print(f"Hydrating {len(targets)} file(s) matching '{prefix}' from Google Drive...")
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(resolve_asset, rel, True): rel for rel, _ in targets}
        for fut in as_completed(futs):
            rel = futs[fut]
            res = fut.result()
            if res:
                done += 1
                if done % 25 == 0 or done == len(targets):
                    print(f"  Downloaded {done}/{len(targets)}: {rel}")
            else:
                print(f"  FAILED to download: {rel}")


def cmd_push_local_missing() -> None:
    """
    Uploads any asset in `gdrive_assets_manifest.json` that does not yet have a `gdrive_file_id`
    if its real binary exists on the local machine (e.g., `/media/shishyan/Shishyan/GitHub/Gurukuladesam`).
    """
    gdrive_bin = find_gdrive_cli()
    if not gdrive_bin:
        print("Error: 'gdrive' CLI not found on PATH.")
        sys.exit(1)

    manifest = load_manifest()
    assets = manifest.get("assets", {})
    missing = [
        (rel, info) for rel, info in assets.items()
        if not info.get("gdrive_file_id")
    ]
    if not missing:
        print("All manifest assets already have a Google Drive file_id!")
        return

    print(f"Checking {len(missing)} unmapped manifest paths on local disk...")
    by_oid = {}
    for rel, info in missing:
        p = ROOT / rel
        if p.exists() and p.stat().st_size > 300:
            oid = info.get("sha256")
            if not oid:
                oid = hashlib.sha256(p.read_bytes()).hexdigest()
            by_oid.setdefault(oid, {"local_file": p, "rels": [], "size": p.stat().st_size})["rels"].append(rel)

    if not by_oid:
        print("No local real binaries found for the unmapped entries.")
        return

    print(f"Found {len(by_oid)} unique local binaries ({sum(v['size'] for v in by_oid.values())/1024/1024:.2f} MB) to upload to Google Drive...")
    for oid, item in by_oid.items():
        local_p = item["local_file"]
        res = subprocess.run(
            [gdrive_bin, "mutate", "upload", str(local_p), "--parent", GDRIVE_MIGRATION_FOLDER],
            capture_output=True, text=True
        )
        if res.returncode == 0:
            m = re.search(r"\(ID:\s*([A-Za-z0-9_-]+)\)", res.stdout)
            if m:
                fid = m.group(1)
                for rel in item["rels"]:
                    assets[rel]["gdrive_file_id"] = fid
                    assets[rel]["gdrive_url"] = f"https://drive.google.com/file/d/{fid}/view"
                    assets[rel]["gdrive_path"] = f"GuruKulaDesam/Assets/GitHub_LFS_Migration/{local_p.name}"
                    assets[rel]["status"] = "gdrive_uploaded"
                print(f"  Uploaded {local_p.name} -> {fid} ({len(item['rels'])} paths)")
    save_manifest(manifest)
    print("Updated production/gdrive_assets_manifest.json.")


def main() -> None:
    parser = argparse.ArgumentParser(description="GuruKulaDesam Google Drive Asset Resolver & Sync")
    parser.add_argument("--status", action="store_true", help="Show Google Drive asset manifest status")
    parser.add_argument("--pull", type=str, help="Pull/hydrate a path or directory prefix from Google Drive")
    parser.add_argument("--push-local-missing", action="store_true", help="Upload any remaining local-only binaries to Google Drive")
    args = parser.parse_args()

    if args.pull:
        cmd_pull(args.pull)
    elif args.push_local_missing:
        cmd_push_local_missing()
    else:
        cmd_status()


if __name__ == "__main__":
    main()
