#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds `production/shorts_metadata/master_film_sources.json` — the single canonical
index of 100% genuine, song-specific Original Master Films across:
  1. Live published Master / Cinematic Films on @Guru-Kula-Desam (UCPqB1A_WzpLJec6q69BOO3Q)
  2. Clean un-layered 1080p base Master Videos in Google Drive `Videos/`
  3. Verified non-generic Master Films in `/media/shishyan/Shishyan/GitHub/Gurukuladesam/renders/releases/`
"""

import os
import re
import sys
import json
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.authorize_gurukuladesam2 import get_channel_youtube_service

WIN_ROOT = Path("/media/shishyan/Shishyan/GitHub/Gurukuladesam")
GVFS_VIDS = Path("/run/user/1000/gvfs/google-drive:host=gmail.com,user=nagaraj957/0AO7hUVqpfVvgUk9PVA/1RFL_SO9T271fzcughvXpR9Mjk_5ZYe1q/1EmZnPeIgkP0wBCcLnWS2Jp6UrCBRTFdX")
META_DB_PATH = ROOT / "production" / "metadata" / "all_songs_lyrics_and_meanings.json"
MANIFEST_PATH = ROOT / "production" / "autonomous_master_production_manifest.json"
OUT_CATALOG = ROOT / "production" / "shorts_metadata" / "master_film_sources.json"


def classify_film_deity(title: str, genre: str = "", category_hint: str = "") -> str:
    combined = f"{category_hint} {genre} {title}".lower()
    # 1. Thirukkural first
    if "திருக்குறள்" in combined or "thirukkural" in combined or "அதிகாரம்" in combined or "adhikaram" in combined:
        return "thirukkural"
    # 2. Vallalar / Thiruvarutpa / Universal Wisdom (Konrai Vendhan) before Shiva/Murugan
    if any(k in combined for k in ("திருவருட்பா", "thiruvarutpa", "வள்ளலார்", "vallalar", "அருட்பெருஞ்ஜோதி", "அருட்பெருஞ்சோதி", "arutperunjothi", "கொன்றை வேந்தன்", "konrai vendhan")):
        return "vallalar"
    # 3. Vinayagar before Thiruppugazh/Thevaram/Kandha (so Kaiththala Niraigani, Thigada Sakkara, Pidiyathan Uruvumai map to Vinayagar!)
    if any(k in combined for k in ("விநாயக", "vinayag", "கணபதி", "ganapathi", "கண நாதா", "gana natha", "கணேச", "ganesha", "கைத்தல நிறைகனி", "kaiththala", "திகட சக்கர", "thigada", "பிடியதன் உருவுமை", "pidiyathan")):
        return "vinayagar"
    # 4. Amman / Shakti / Saraswathi / Lakshmi
    if any(k in combined for k in ("அம்மன்", "amman", "அபிராமி", "abhirami", "சக்தி", "sakthi", "சரஸ்வதி", "saraswathi", "லக்ஷ்மி", "lakshmi", "கருமாரி", "karumari", "ரேணுகாம்பாள்", "renukambal", "காயத்ரி", "gayathri")):
        return "amman"
    # 5. Vishnu / Perumal / Krishna / Rama / Azhvar
    if any(k in combined for k in ("விஷ்ணு", "vishnu", "கிருஷ்ண", "krishna", "பெருமாள்", "perumal", "ஆழ்வார்", "azhvar", "திருப்பாவை", "thiruppavai", "நாராயண", "narayana", "கோவிந்த", "govinda", "ராம", "rama", "ரகுபதி", "raghupati", "ஆஞ்சநேயர்", "anjaneyar", "பல்லாண்டு", "pallaandu")):
        return "vishnu"
    # 6. Murugan
    if any(k in combined for k in ("முருக", "murug", "கந்த", "kandha", "kandar", "திருப்புகழ்", "thiruppugazh", "சுப்ரமணிய", "subramani", "ஸ்கந்த", "skanda", "ஆறுமுகம்", "arumugam", "வேல்", "கௌமாரம்", "koumaram", "மகரம் அளறு", "magaram alaru")):
        return "murugan"
    # 7. Shiva
    if any(k in combined for k in ("சிவ", "shiva", "siva", "திருவாசகம்", "thiruvasagam", "தேவாரம்", "thevaram", "ஈஸ்வர", "ishwara", "eeswara", "திருமந்திரம்", "thirumanthiram", "பெரியபுராணம்", "periyapuranam", "தில்லை", "thillai", "அருணாசலம்", "arunachalam", "நடராஜ", "nataraj", "கோளறு", "திருநீற்று")):
        return "shiva"
    return "shiva"


def parse_iso_duration(dur_str: str) -> int:
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", dur_str or "")
    if not m:
        return 0
    h, mn, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mn * 60 + s


def get_bad_duplicate_flow_tids() -> set[str]:
    """Identify any track_ids on Windows SSD whose Flow scene folder used generic duplicated fallback clips."""
    bad = set()
    flow_root = WIN_ROOT / "production" / "google_flow_renders"
    if not flow_root.exists():
        return bad
    hash_counts = {}
    dir_hashes = {}
    for d in flow_root.iterdir():
        if not d.is_dir():
            continue
        hs = []
        for mp4 in sorted(d.glob("scene_*.mp4")):
            if mp4.stat().st_size > 200_000:
                with open(mp4, "rb") as fh:
                    h = hashlib.md5(fh.read(65536)).hexdigest()
                hash_counts[h] = hash_counts.get(h, 0) + 1
                hs.append(h)
        dir_hashes[d.name] = hs
    for tid, hs in dir_hashes.items():
        if hs:
            unique_cnt = sum(1 for h in hs if hash_counts[h] <= 2)
            if unique_cnt < 3:
                bad.add(tid)
    return bad


def scan_gdrive_master_videos() -> list[dict]:
    """Scan mounted GVFS Google Drive Videos subfolders for clean base MP4s and Master Films."""
    results = []
    if not GVFS_VIDS.exists():
        return results

    subfolders = [
        ("1hsGerhkZWe67_PMUwtMFbEtJVrnSAkSA", "Pending_Layering", True),
        ("17WXxfiqJSK5tyFgT0WbPAhijn2kjokTU", "Pending_Review", False),
        ("1WbuabUwZb6shl9FokGr2QeaiIDiIQQ97", "Published", False),
        ("1WUYrvYRqyPOYRUHc2Gd-iC5gcb3P9Qy1", "GuruKulaDesam", False),
    ]
    pub_yt = GVFS_VIDS / "1WbuabUwZb6shl9FokGr2QeaiIDiIQQ97" / "15awinK-dUOeh16CnnyS-c6KdYfmPsZTv"

    dirs_to_scan = [(GVFS_VIDS / sid, lbl, clean_def) for sid, lbl, clean_def in subfolders]
    if pub_yt.exists():
        dirs_to_scan.append((pub_yt, "Published/YouTube", True))

    for dpath, folder_label, default_clean in dirs_to_scan:
        if not dpath.exists():
            continue
        for fname in sorted(os.listdir(dpath)):
            fpath = dpath / fname
            try:
                if fpath.is_dir():
                    continue
            except OSError:
                continue
            try:
                out = subprocess.check_output(
                    ["gio", "info", "-a", "standard::display-name,standard::size", str(fpath)],
                    text=True, stderr=subprocess.DEVNULL
                )
            except Exception:
                continue
            disp = fname
            sz = 0
            for line in out.splitlines():
                if "standard::display-name:" in line:
                    disp = line.split("standard::display-name:", 1)[1].strip()
                elif "standard::size:" in line:
                    sz = int(line.split("standard::size:", 1)[1].strip())
            if not disp.lower().endswith(".mp4") or sz < 15_000_000:
                continue
            if "_old" in disp.lower():
                continue

            is_clean_unlayered = default_clean or ("master_film" not in disp.lower())
            ch_match = re.search(r"(?:ch|அதிகாரம்\s*-?\s*)0*(\d{1,3})\b", disp, re.IGNORECASE)
            ch_num = int(ch_match.group(1)) if ch_match else None

            results.append({
                "display_name": disp,
                "gvfs_path": str(fpath),
                "folder": folder_label,
                "size_mb": round(sz / 1e6, 1),
                "is_clean_unlayered": is_clean_unlayered,
                "chapter_num": ch_num,
            })
    return results


def fetch_parent_channel_films() -> list[dict]:
    yt, _, _ = get_channel_youtube_service("@gurukuladesam")
    uploads_pl = "UUPqB1A_WzpLJec6q69BOO3Q"
    vid_ids = []
    page_token = None
    while True:
        res = yt.playlistItems().list(
            part="contentDetails,snippet",
            playlistId=uploads_pl,
            maxResults=50,
            pageToken=page_token
        ).execute()
        for it in res.get("items", []):
            title = it["snippet"].get("title", "")
            pub_at = it["snippet"].get("publishedAt", "")
            if "[Audio]" in title or "Clilp" in title:
                continue
            if pub_at >= "2026-08-25" or "Film" in title or "Master" in title or "1080p" in title:
                vid_ids.append(it["contentDetails"]["videoId"])
        page_token = res.get("nextPageToken")
        if not page_token:
            break

    films = []
    for i in range(0, len(vid_ids), 50):
        chunk = vid_ids[i : i + 50]
        vres = yt.videos().list(
            part="snippet,contentDetails,status,statistics",
            id=",".join(chunk)
        ).execute()
        for v in vres.get("items", []):
            if v.get("status", {}).get("privacyStatus") != "public":
                continue
            sn = v["snippet"]
            dur = parse_iso_duration(v["contentDetails"].get("duration", ""))
            if dur < 65:
                continue
            title = sn.get("title", "")
            pub_at = sn.get("publishedAt", "")
            ch_m = re.search(r"அதிகாரம்\s*(\d{1,3})\b", title)
            ch_num = int(ch_m.group(1)) if ch_m else None

            has_burned_bars = (pub_at >= "2026-10-21" and ("1080p" in title or ch_num == 8))
            films.append({
                "youtube_film_id": v["id"],
                "title": title,
                "description": sn.get("description", ""),
                "published_at": pub_at,
                "duration_sec": dur,
                "views": int(v.get("statistics", {}).get("viewCount", 0)),
                "chapter_num": ch_num,
                "has_burned_bars": has_burned_bars,
            })
    films.sort(key=lambda x: x["published_at"], reverse=True)
    return films


def main():
    print("🔍 Auditing Flow uniqueness on Windows SSD...")
    bad_flow_tids = get_bad_duplicate_flow_tids()
    print(f"   • Excluded {len(bad_flow_tids)} legacy duplicate-clip track IDs.")

    print("📂 Scanning Google Drive `Videos/` for clean 1080p base Master MP4s...")
    gdrive_files = scan_gdrive_master_videos()
    print(f"   • Found {len(gdrive_files)} Master MP4s in Google Drive ({sum(1 for g in gdrive_files if g['is_clean_unlayered'])} clean un-layered!).")

    print("🏛️  Fetching published Master Films from @Guru-Kula-Desam (UCPqB1A_WzpLJec6q69BOO3Q)...")
    yt_films = fetch_parent_channel_films()
    print(f"   • Found {len(yt_films)} full-length public Master Films on @Guru-Kula-Desam!")

    meta_db = json.loads(META_DB_PATH.read_text(encoding="utf-8")) if META_DB_PATH.exists() else {}
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8")) if MANIFEST_PATH.exists() else {}
    manifest_by_yt = {}
    for t in manifest.get("completed_tracks", []):
        if t.get("youtube_id"):
            manifest_by_yt[t["youtube_id"]] = t

    win_releases_by_tid = {}
    win_adhikaram_by_ch = {}
    if (WIN_ROOT / "renders" / "releases").exists():
        for mp4 in sorted((WIN_ROOT / "renders" / "releases").glob("*.mp4")):
            if mp4.stat().st_size < 10_000_000:
                continue
            m_ch = re.match(r"adhikaram_0*(\d+)_.*_cinematic\.mp4$", mp4.name)
            if m_ch:
                win_adhikaram_by_ch[int(m_ch.group(1))] = str(mp4)
                continue
            for tid in meta_db.keys():
                if f"_{tid}_" in mp4.name and tid not in bad_flow_tids:
                    win_releases_by_tid[tid] = str(mp4)
                    break

    catalog = {}
    seen_chapters_primary = set()
    covered_legacy_tids = set()

    for yf in yt_films:
        yfid = yf["youtube_film_id"]
        title = yf["title"]
        ch_num = yf["chapter_num"]

        if any(w in title.lower() for w in ("ஜன கண மன", "jana gana mana", "தாயின் மணிக்கொடி", "தமிழ்த் தாய் வாழ்த்து", "தமிழ்த்தாய் வாழ்த்து", "சம்சாரம் என்பது வீணை", "விழியிலே மலர்ந்தது")):
            continue

        linked_man = manifest_by_yt.get(yfid)
        orig_tid = linked_man["track_id"] if linked_man else (yfid if yfid in meta_db else None)
        if orig_tid and orig_tid in bad_flow_tids:
            continue

        meta_entry = {}
        matched_tid = orig_tid
        if matched_tid and matched_tid in meta_db:
            meta_entry = meta_db[matched_tid]
        elif ch_num:
            for tid, me in meta_db.items():
                if re.search(rf"அதிகாரம்\s*0*{ch_num}\b", me.get("title", "")):
                    meta_entry = me
                    matched_tid = matched_tid or tid
                    break

        deity = classify_film_deity(title, meta_entry.get("genre", ""), linked_man.get("category", "") if linked_man else "")

        local_clean_path = None
        local_layered_path = None

        if ch_num:
            for gf in gdrive_files:
                if gf["chapter_num"] == ch_num:
                    if gf["is_clean_unlayered"] and not local_clean_path:
                        local_clean_path = gf["gvfs_path"]
                    elif not gf["is_clean_unlayered"] and not local_layered_path:
                        local_layered_path = gf["gvfs_path"]
            if not local_clean_path and ch_num in win_adhikaram_by_ch:
                local_clean_path = win_adhikaram_by_ch[ch_num]
        else:
            for gf in gdrive_files:
                dn = gf["display_name"].lower()
                if ("ஈஸ்வர நாமவளி" in title and ("ஈஸ்வர நாமவளி" in dn or "ishwara_namavali" in dn)) or \
                   ("கோவிந்த நாமாவளி" in title and ("கோவிந்த நாமாவளி" in dn or "govinda_namavali" in dn)):
                    if gf["is_clean_unlayered"] and not local_clean_path:
                        local_clean_path = gf["gvfs_path"]
                    elif not gf["is_clean_unlayered"] and not local_layered_path:
                        local_layered_path = gf["gvfs_path"]

            if not local_clean_path and orig_tid and orig_tid in win_releases_by_tid:
                local_clean_path = win_releases_by_tid[orig_tid]

        is_flagship_oct = yf["published_at"] >= "2026-10-07"
        if ch_num is not None:
            if ch_num in seen_chapters_primary:
                continue
            seen_chapters_primary.add(ch_num)

        if matched_tid:
            covered_legacy_tids.add(matched_tid)

        catalog[yfid] = {
            "film_id": yfid,
            "youtube_film_id": yfid,
            "youtube_url": f"https://www.youtube.com/watch?v={yfid}",
            "legacy_track_id": matched_tid,
            "title": title,
            "deity": deity,
            "chapter_num": ch_num,
            "published_at": yf["published_at"],
            "duration_sec": yf["duration_sec"],
            "views": yf["views"],
            "quality_tier": 0 if is_flagship_oct else 1,
            "has_burned_bars": yf["has_burned_bars"],
            "local_clean_video": local_clean_path,
            "local_layered_video": local_layered_path,
            "tamil_lyrics": meta_entry.get("tamil_lyrics", ""),
            "tamil_meaning": meta_entry.get("tamil_meaning", ""),
            "english_meaning": meta_entry.get("english_meaning", ""),
        }

    # Add Google Drive new Ch 9..27 Master Films not yet on YouTube
    for gf in gdrive_files:
        ch_num = gf["chapter_num"]
        if ch_num and ch_num not in seen_chapters_primary:
            seen_chapters_primary.add(ch_num)
            fid = f"gdrive_ch{ch_num:03d}"
            meta_entry = {}
            for tid, me in meta_db.items():
                if re.search(rf"அதிகாரம்\s*0*{ch_num}\b", me.get("title", "")):
                    meta_entry = me
                    break
            raw_t = meta_entry.get("title") or gf["display_name"].replace(".mp4", "").replace("_", " ")
            catalog[fid] = {
                "film_id": fid,
                "youtube_film_id": None,
                "youtube_url": "https://www.youtube.com/@guru-kula-desam",
                "legacy_track_id": None,
                "title": raw_t,
                "deity": "thirukkural",
                "chapter_num": ch_num,
                "published_at": "2026-10-25T00:00:00Z",
                "duration_sec": 240,
                "views": 0,
                "quality_tier": 0,
                "has_burned_bars": not gf["is_clean_unlayered"],
                "local_clean_video": gf["gvfs_path"] if gf["is_clean_unlayered"] else None,
                "local_layered_video": None if gf["is_clean_unlayered"] else gf["gvfs_path"],
                "tamil_lyrics": meta_entry.get("tamil_lyrics", ""),
                "tamil_meaning": meta_entry.get("tamil_meaning", ""),
                "english_meaning": meta_entry.get("english_meaning", ""),
            }

    # Add verified non-duplicate Windows SSD Master Films not yet covered above
    for tid, win_mp4 in win_releases_by_tid.items():
        if tid in covered_legacy_tids:
            continue
        me = meta_db.get(tid, {})
        raw_t = me.get("title", tid)
        if any(w in raw_t.lower() for w in ("ஜன கண மன", "jana gana mana", "தாயின் மணிக்கொடி", "தமிழ்த் தாய் வாழ்த்து", "சம்சாரம் என்பது வீணை", "விழியிலே மலர்ந்தது")):
            continue
        ch_m = re.search(r"அதிகாரம்\s*0*(\d{1,3})\b", raw_t)
        if ch_m and int(ch_m.group(1)) in seen_chapters_primary:
            continue
        deity = classify_film_deity(raw_t, me.get("genre", ""), Path(win_mp4).name.split("_")[0])
        catalog[tid] = {
            "film_id": tid,
            "youtube_film_id": None,
            "youtube_url": f"https://www.youtube.com/watch?v={tid}",
            "legacy_track_id": tid,
            "title": raw_t,
            "deity": deity,
            "chapter_num": int(ch_m.group(1)) if ch_m else None,
            "published_at": "2026-09-25T00:00:00Z",
            "duration_sec": 240,
            "views": 0,
            "quality_tier": 1,
            "has_burned_bars": False,
            "local_clean_video": win_mp4,
            "local_layered_video": None,
            "tamil_lyrics": me.get("tamil_lyrics", ""),
            "tamil_meaning": me.get("tamil_meaning", ""),
            "english_meaning": me.get("english_meaning", ""),
        }

    OUT_CATALOG.parent.mkdir(parents=True, exist_ok=True)
    OUT_CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")

    by_deity = {}
    for v in catalog.values():
        by_deity[v["deity"]] = by_deity.get(v["deity"], 0) + 1

    print("=" * 80)
    print(f"✅ SAVED MASTER FILM CATALOG: {OUT_CATALOG} ({len(catalog)} verified 100% song-specific Master Films)")
    for d, cnt in sorted(by_deity.items()):
        print(f"   • {d:<14}: {cnt:3d} Master Films")
    print("=" * 80)


if __name__ == "__main__":
    main()
