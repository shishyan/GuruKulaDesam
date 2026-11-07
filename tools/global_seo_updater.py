#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/global_seo_updater.py
Updates all videos across @guru-kula-desam, @GuruKulaDesam, and @GuruKulaDesam2:
- Strictly NEVER modifies `snippet.title` (preserves 100% of existing titles).
- Sets `snippet.categoryId = "10"` (Music) so YouTube Music & Global Mixes index every video.
- Populates up to ~490 characters of high-volume Global Music Discovery tags + World/Spiritual/Meditative tags + Song-specific tags.
- Appends a clean Global Music & Meditation SEO footer to `snippet.description` (strictly keeping UTF-8 byte length <= 4850 bytes and removing any `<` or `>` characters).
- Adds multi-language `localizations` (`en`, `es`, `pt`, `de`, `fr`, `ja`, `hi`) for descriptions (while keeping the original `title` identical across localizations as requested).
- Rotates across available OAuth tokens per channel and logs every update to `production/youtube_backup/global_seo_update_log.jsonl`.
"""

import os
import re
import sys
import json
import time
import argparse
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path("/home/shishyan/GitHub/Shishyan/GuruKulaDesam")
BACKUP_DIR = ROOT / "production" / "youtube_backup"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = BACKUP_DIR / "global_seo_update_log.jsonl"
MARKER = "🌍 GLOBAL MUSIC & MEDITATION LISTENERS"

CHANNEL_POOLS = [
    {
        "handle": "@GuruKulaDesam",
        "channel_id": "UCz4dzcjahGaIb5dZCv32AmA",
        "uploads_playlist": "UUz4dzcjahGaIb5dZCv32AmA",
        "tokens": [
            ROOT / "data/credentials/tokens_gurukuladesam/token_839236964216.json",
            ROOT / "data/credentials/tokens_gurukuladesam/token_472322435541.json",
            ROOT / "data/credentials/token_gurukuladesam.json",
        ],
    },
    {
        "handle": "@GuruKulaDesam2",
        "channel_id": "UCGUmNzaV_OUFbsNdHJQtaNQ",
        "uploads_playlist": "UUGUmNzaV_OUFbsNdHJQtaNQ",
        "tokens": [
            ROOT / "data/credentials/tokens_gurukuladesam2/token_839236964216.json",
            ROOT / "data/credentials/tokens_gurukuladesam2/token_472322435541.json",
            ROOT / "data/credentials/token_gurukuladesam2.json",
        ],
    },
    {
        "handle": "@guru-kula-desam",
        "channel_id": "UCPqB1A_WzpLJec6q69BOO3Q",
        "uploads_playlist": "UUPqB1A_WzpLJec6q69BOO3Q",
        "tokens": [
            ROOT / "data/credentials/token.json",
            ROOT / "data/credentials/tokens/token_472322435541.json",
        ],
    },
]

# High-volume Global Top-25 YouTube Search Clusters for Pure Meditative / Instrumental videos
INSTRUMENTAL_GLOBAL_TAGS = [
    "relaxing music", "sleep music", "meditation music", "asmr sleep",
    "deep sleep music", "instrumental music", "flute music", "nature sounds",
    "rain sounds", "zen meditation", "432hz", "528hz", "healing music",
    "calm music", "peaceful music", "study music", "focus music",
    "lofi chill", "background music", "spa music", "yoga music",
    "stress relief", "anxiety relief", "musica relajante", "musique relaxante",
    "musik zum schlafen", "guru kula desam", "song", "music"
]

# High-volume Global Top-25 YouTube Search Clusters for Sacred / World / Devotional / Thirukkural Music
VOCAL_GLOBAL_TAGS = [
    "music", "song", "songs", "relaxing music", "meditation music",
    "world music", "indian music", "spiritual music", "peaceful music",
    "calm music", "healing music", "soulful music", "ambient music",
    "study music", "focus music", "sleep music", "yoga music",
    "sacred music", "ancient wisdom", "acoustic music", "ethereal music",
    "mindfulness music", "guru kula desam", "tamil song", "devotional song"
]

DEITY_SPECIFIC_TAGS = {
    "thirukkural": ["thirukkural", "thiruvalluvar", "ancient tamil wisdom", "ethical music"],
    "murugan": ["murugan songs", "thiruppugazh", "vel muruga", "sacred chants", "karthikeya"],
    "shiva": ["shiva songs", "om namah shivaya", "thiruvasagam", "shiva meditation", "mahadev"],
    "amman": ["amman songs", "abhirami anthathi", "divine mother chants", "devi music"],
    "vinayagar": ["vinayagar songs", "ganesha chants", "vinayagar agaval", "ganapathi"],
    "vishnu": ["perumal songs", "narayana chants", "govinda", "vishnu meditation"],
    "vallalar": ["vallalar songs", "arutperunjothi", "thiruvarutpa", "light meditation"],
}


def detect_video_type_and_deity(title: str, desc: str) -> tuple[bool, str]:
    text = f"{title}\n{desc}".lower()
    is_inst = any(w in text for w in [
        "instrumental", "soundscape", "432hz", "zen garden", "tranquil flow",
        "mountain awakening", "fjord", "ocean of calm", "whispering winds",
        "golden hour harmony", "sacred cascade", "aurora night", "mystic river",
        "oasis of stillness", "floating petals", "sunlit valley", "coastal twilight",
        "terraced sunset", "misty river", "tropical shoreline", "emerald bamboo",
        "glacial summit", "lotus blossom", "highland breeze", "pacific tide",
        "autumn creek", "silent snowfall", "wildflower meadow", "without vocals",
        "deep focus flow", "living focus flow"
    ])
    if "குறள்" in text or "thirukkural" in text or "அதிகாரம்" in text:
        deity = "thirukkural"
    elif "முருக" in text or "திருப்புகழ்" in text or "murug" in text or "கந்த" in text:
        deity = "murugan"
    elif "சிவ" in text or "திருவாசகம்" in text or "shiva" in text or "ஈஸ்வர" in text or "நமச்சிவாய" in text:
        deity = "shiva"
    elif "அம்மன்" in text or "அபிராமி" in text or "amman" in text or "லட்சுமி" in text or "lakshmi" in text:
        deity = "amman"
    elif "விநாயகர்" in text or "vinayag" in text or "கணபதி" in text or "திகட" in text or "சீத களப" in text:
        deity = "vinayagar"
    elif "பெருமாள்" in text or "கோவிந்தா" in text or "நாராயண" in text or "கிருஷ்ண" in text or "vishnu" in text:
        deity = "vishnu"
    elif "அருட்பெருஞ்ஜோதி" in text or "வள்ளலார்" in text or "திருவருட்பா" in text or "vallalar" in text:
        deity = "vallalar"
    else:
        deity = "thirukkural"
    return is_inst, deity


def build_optimal_tags(existing_tags: list[str], title: str, desc: str) -> list[str]:
    is_inst, deity = detect_video_type_and_deity(title, desc)
    candidates = []
    # Keep clean existing tags first if they are specific
    for t in (existing_tags or []):
        t_clean = t.strip().replace("<", "").replace(">", "")
        if t_clean and t_clean.lower() not in [c.lower() for c in candidates]:
            candidates.append(t_clean)

    # Add deity/theme tags
    if not is_inst:
        for t in DEITY_SPECIFIC_TAGS.get(deity, []):
            if t.lower() not in [c.lower() for c in candidates]:
                candidates.append(t)

    # Add global top search cluster tags
    pool = INSTRUMENTAL_GLOBAL_TAGS if is_inst else VOCAL_GLOBAL_TAGS
    for t in pool:
        if t.lower() not in [c.lower() for c in candidates]:
            candidates.append(t)

    # Fit strictly under YouTube's 500-character total tag limit (accounting for quotes/commas YouTube counts)
    final_tags = []
    total_chars = 0
    for t in candidates:
        cost = len(t) + (3 if " " in t else 1)
        if total_chars + cost > 465:
            break
        final_tags.append(t)
        total_chars += cost
    return final_tags


def build_updated_description(desc: str, is_inst: bool, is_short: bool) -> str:
    clean_desc = (desc or "").replace("<", "‹").replace(">", "›").strip()
    if MARKER in clean_desc:
        return clean_desc

    if is_inst:
        footer = (
            "\n\n─────────────────────────────────────────────────────────────────\n"
            f"{MARKER}\n"
            "Pure 48kHz meditative instrumental soundscape (no vocals) crafted for deep sleep, ASMR relaxation, "
            "zen mindfulness, yoga, studying, coding, and anxiety relief across the globe.\n"
            "• Español: Música instrumental relajante para dormir profundamente, meditar y estudiar.\n"
            "• Português: Música instrumental relaxante para dormir, meditação e foco.\n"
            "• Deutsch & Français: Entspannungsmusik zum Schlafen | Musique relaxante pour dormir.\n"
            "• 日本語 & 한국어: 睡眠用BGM・瞑想音楽・リラックス音楽 | 수면 음악 및 명상 음악.\n"
            "#RelaxingMusic #SleepMusic #MeditationMusic #ASMR #Instrumental #DeepSleep #432Hz #NatureSounds #FocusMusic #Zen #GuruKulaDesam"
        )
    else:
        footer = (
            "\n\n─────────────────────────────────────────────────────────────────\n"
            f"{MARKER}\n"
            "Music transcends language. Even if you don't speak Tamil, immerse yourself in the soothing acoustic instruments, "
            "sacred spiritual harmonies, and tranquil rhythm of this original 48kHz composition—ideal for world music lovers, "
            "meditation, yoga, deep focus, and inner peace.\n"
            "• Global Discovery: Sacred Indian World Music | Spiritual & Meditative Song | Peaceful Acoustic Soundtrack.\n"
            "#Music #WorldMusic #MeditationMusic #RelaxingMusic #SpiritualMusic #IndianMusic #PeacefulMusic #HealingMusic #FocusMusic #Song #GuruKulaDesam"
        )

    footer_bytes = len(footer.encode("utf-8"))
    max_base_bytes = 4850 - footer_bytes
    base_bytes = clean_desc.encode("utf-8")
    if len(base_bytes) > max_base_bytes:
        # Trim safely at line boundary
        lines = clean_desc.split("\n")
        kept = []
        cur_b = 0
        for line in lines:
            lb = len((line + "\n").encode("utf-8"))
            if cur_b + lb > max_base_bytes:
                break
            kept.append(line)
            cur_b += lb
        clean_desc = "\n".join(kept).strip()

    return (clean_desc + footer).strip()


def build_localizations(orig_title: str, updated_desc: str, existing_locs: dict, is_inst: bool) -> dict:
    locs = dict(existing_locs or {})
    # Keep the title 100% UNCHANGED in all localizations per user instruction!
    lang_notes = {
        "en": "🌍 Global Music & Meditation: Original 48kHz composition for deep sleep, relaxation, mindfulness, yoga, and focus.\n\n",
        "es": "🌍 Música Relajante del Mundo y Meditación: Composición original en 48kHz para dormir profundamente, meditar, estudiar y relajarse.\n\n",
        "pt": "🌍 Música Relaxante e Meditação: Composição original em 48kHz para dormir, meditar, estudar e relaxar profundamente.\n\n",
        "de": "🌍 Entspannungsmusik & Meditation: Originale 48kHz-Komposition zum Schlafen, Meditieren, Lernen und Entspannen.\n\n",
        "fr": "🌍 Musique Relaxante & Méditation: Composition originale 48kHz pour dormir profondément, méditer, étudier et se détendre.\n\n",
        "ja": "🌍 瞑想・睡眠・リラックス音楽: 深い眠り、ヨガ、勉強、心の平安のための48kHzオリジナル音楽作品。\n\n",
        "hi": "🌍 ध्यान, योग और गहरी नींद के लिए शांत संगीत: मानसिक शांति और एकाग्रता के लिए मूल 48kHz संगीत रचना।\n\n",
    }
    for lang, prefix in lang_notes.items():
        # Fit localized description within 4850 UTF-8 bytes
        p_bytes = len(prefix.encode("utf-8"))
        avail = 4850 - p_bytes
        desc_b = updated_desc.encode("utf-8")[:avail].decode("utf-8", errors="ignore")
        locs[lang] = {
            "title": orig_title,
            "description": (prefix + desc_b).strip(),
        }
    return locs


def load_completed_ids() -> set[str]:
    done = set()
    if LOG_FILE.exists():
        for line in LOG_FILE.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
                if rec.get("ok"):
                    done.add(rec["id"])
            except Exception:
                pass
    return done


def log_record(rec: dict):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def get_working_clients(token_paths: list[Path]):
    clients = []
    seen_projs = set()
    for tp in token_paths:
        if not tp.exists():
            continue
        try:
            raw = json.loads(tp.read_text(encoding="utf-8"))
            proj = raw.get("client_id", "").split("-")[0]
            if proj in seen_projs:
                continue
            creds = Credentials.from_authorized_user_file(str(tp))
            if not creds.valid and creds.refresh_token:
                creds.refresh(Request())
                tp.write_text(creds.to_json(), encoding="utf-8")
            yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
            clients.append((proj, yt))
            seen_projs.add(proj)
        except Exception as e:
            print(f"  [Token skip] {tp.name}: {e}")
    return clients


def fetch_all_channel_video_ids(yt, uploads_playlist_id: str) -> list[str]:
    vids = []
    page_token = None
    while True:
        resp = yt.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=page_token,
        ).execute()
        for it in resp.get("items", []):
            vid = it.get("contentDetails", {}).get("videoId")
            if vid and vid not in vids:
                vids.append(vid)
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return vids


def process_channel(pool_cfg: dict, done_ids: set[str], limit: int = 0) -> tuple[int, int]:
    handle = pool_cfg["handle"]
    print("=" * 80)
    print(f"🚀 PROCESSING CHANNEL: {handle} ({pool_cfg['channel_id']})")
    print("=" * 80)

    clients = get_working_clients(pool_cfg["tokens"])
    if not clients:
        print(f"  ❌ No active OAuth clients available for {handle}")
        return 0, 0

    client_idx = 0
    proj, yt = clients[client_idx]
    print(f"  🔑 Using OAuth Project {proj} to list uploads...")

    all_vids = fetch_all_channel_video_ids(yt, pool_cfg["uploads_playlist"])
    pending_vids = [v for v in all_vids if v not in done_ids]
    print(f"  📹 Total Videos on {handle}: {len(all_vids)} | Already Updated: {len(all_vids) - len(pending_vids)} | Pending: {len(pending_vids)}")

    if not pending_vids:
        return 0, 0

    # Batch-fetch snippet & localizations in chunks of 50 (only 1 quota unit per 50 videos!)
    video_items = []
    for i in range(0, len(pending_vids), 50):
        chunk = pending_vids[i : i + 50]
        resp = yt.videos().list(part="snippet,localizations", id=",".join(chunk)).execute()
        video_items.extend(resp.get("items", []))

    updated_count = 0
    skipped_count = 0

    for idx, item in enumerate(video_items, 1):
        if limit and updated_count >= limit:
            break

        vid = item["id"]
        sn = item["snippet"]
        orig_title = sn["title"]  # Strictly preserved!
        orig_desc = sn.get("description", "")
        orig_tags = sn.get("tags", [])
        orig_cat = sn.get("categoryId", "27")
        orig_locs = item.get("localizations", {})

        is_inst, deity = detect_video_type_and_deity(orig_title, orig_desc)
        is_short = handle.lower() in ("@gurukuladesam", "@gurukuladesam2")

        new_tags = build_optimal_tags(orig_tags, orig_title, orig_desc)
        new_desc = build_updated_description(orig_desc, is_inst=is_inst, is_short=is_short)
        new_locs = build_localizations(orig_title, new_desc, orig_locs, is_inst=is_inst)

        # Build update payload keeping title 100% identical
        new_snippet = {
            "title": orig_title,
            "description": new_desc,
            "tags": new_tags,
            "categoryId": "10",  # Music category globally
        }
        # Set defaultLanguage so localizations work cleanly
        new_snippet["defaultLanguage"] = sn.get("defaultLanguage") or ("en" if is_inst else "ta")
        if "defaultAudioLanguage" in sn:
            new_snippet["defaultAudioLanguage"] = sn["defaultAudioLanguage"]
        else:
            new_snippet["defaultAudioLanguage"] = "en" if is_inst else "ta"

        body = {
            "id": vid,
            "snippet": new_snippet,
            "localizations": new_locs,
        }

        while client_idx < len(clients):
            proj, yt = clients[client_idx]
            try:
                yt.videos().update(part="snippet,localizations", body=body).execute()
                updated_count += 1
                done_ids.add(vid)
                log_record({
                    "id": vid,
                    "channel": handle,
                    "project": proj,
                    "title": orig_title,
                    "is_instrumental": is_inst,
                    "deity": deity,
                    "old_cat": orig_cat,
                    "new_cat": "10",
                    "old_tags_count": len(orig_tags),
                    "new_tags_count": len(new_tags),
                    "ok": True,
                    "ts": time.time(),
                })
                print(
                    f"  ✅ [{updated_count}/{len(video_items)}] {vid} | {orig_title[:45]:45s} | "
                    f"Cat {orig_cat}->10 | Tags {len(orig_tags)}->{len(new_tags)} | Locs: {len(new_locs)} langs"
                )
                break
            except HttpError as e:
                err_str = str(e)
                if "quotaExceeded" in err_str or "dailyLimitExceeded" in err_str or e.resp.status in (403, 429):
                    print(f"  ⚠️ Quota reached on Project {proj} for {handle}. Rotating to next project...")
                    client_idx += 1
                else:
                    print(f"  ❌ API Error on {vid} ({orig_title[:35]}): {err_str[:160]}")
                    log_record({"id": vid, "channel": handle, "ok": False, "error": err_str[:250], "ts": time.time()})
                    skipped_count += 1
                    break

        if client_idx >= len(clients):
            print(f"  🛑 All active OAuth projects for {handle} reached daily quota after {updated_count} updates.")
            break

    return updated_count, skipped_count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="Max updates per channel (0 = unlimited)")
    ap.add_argument("--channel", type=str, default="all", help="Specific channel handle or 'all'")
    args = ap.parse_args()

    done_ids = load_completed_ids()
    print(f"Loaded {len(done_ids)} previously updated video IDs from log.")

    total_updated = 0
    for pool in CHANNEL_POOLS:
        if args.channel != "all" and pool["handle"].lower() != args.channel.lower():
            continue
        u, _ = process_channel(pool, done_ids, limit=args.limit)
        total_updated += u

    print("\n" + "=" * 80)
    print(f"🎉 GLOBAL SEO UPDATE SUMMARY: {total_updated} videos updated in this run (Total completed: {len(done_ids)})")
    print("=" * 80)


if __name__ == "__main__":
    main()
