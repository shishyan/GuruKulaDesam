#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/republish_legacy_with_flow.py
Publishes upgraded 9:16 Chorus-clipped Shorts directly from @guru-kula-desam Master Films
across @GuruKulaDesam (4) and @GuruKulaDesam2 (7), while keeping all 11 original public Shorts
untouched (`public` as-is) by default so the creator can review the new Shorts first and switch
the older ones to `Private` manually when desired.
"""

import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.authorize_gurukuladesam2 import get_channel_youtube_service
from tools.tamil_panchangam_engine import IST
from tools.shorts_viral_builder import SHORTS_META_DIR, build_short_for_track
from tools.shorts_autonomous_daemon import (
    load_published_registry,
    save_published_registry,
    upload_short_via_api,
)

QUEUE_FILE = SHORTS_META_DIR / "legacy_republish_queue.json"

DEFAULT_LEGACY_ITEMS = [
    # @GuruKulaDesam (4 Virtuous Shorts)
    {
        "track_id": "02C8glMmetw",
        "old_youtube_id": "FKGB4axuYZk",
        "channel_key": "@gurukuladesam",
        "channel_handle": "@GuruKulaDesam",
        "song_label": "திருக்குறள்: அதிகாரம் 1 - கடவுள் வாழ்த்து",
    },
    {
        "track_id": "--4jzoezBW8",
        "old_youtube_id": "4VjGP9Bbp7s",
        "channel_key": "@gurukuladesam",
        "channel_handle": "@GuruKulaDesam",
        "song_label": "திருக்குறள்: அதிகாரம் 67 - வினைத்திட்பம்",
    },
    {
        "track_id": "-cmB2_XZqs0",
        "old_youtube_id": "4rMDlwiJN5M",
        "channel_key": "@gurukuladesam",
        "channel_handle": "@GuruKulaDesam",
        "song_label": "திருவருட்பா: அபராத விண்ணப்பம் I",
    },
    {
        "track_id": "01g0sJdaL2I",
        "old_youtube_id": "KJKgnfRGPKM",
        "channel_key": "@gurukuladesam",
        "channel_handle": "@GuruKulaDesam",
        "song_label": "திருக்குறள்: அதிகாரம் 56 - கொடுங்கோன்மை",
    },
    # @GuruKulaDesam2 (7 Devotional Shorts)
    {
        "track_id": "2tL-bKjkL18",
        "old_youtube_id": "aMAOsCbGt9Q",
        "channel_key": "@gurukuladesam2",
        "channel_handle": "@GuruKulaDesam2",
        "song_label": "அபிராமி அந்தாதி: தனந்தரும் கல்விதரும்",
    },
    {
        "track_id": "Lki_Y8OSljs",
        "old_youtube_id": "L0Wc1paDzOQ",
        "channel_key": "@gurukuladesam2",
        "channel_handle": "@GuruKulaDesam2",
        "song_label": "விநாயகர் துதி: கண நாதா ஓம்",
    },
    {
        "track_id": "AW4cljBWy2w",
        "old_youtube_id": "EhoFH_-N4lw",
        "channel_key": "@gurukuladesam2",
        "channel_handle": "@GuruKulaDesam2",
        "song_label": "விநாயகர் நான்மணிமாலை: பாலும் தெளிதேனும்",
    },
    {
        "track_id": "DsbMysGdqv8",
        "legacy_track_id": "-L3VXkM2MTY",
        "old_youtube_id": "QWj6z4qXaqU",
        "channel_key": "@gurukuladesam2",
        "channel_handle": "@GuruKulaDesam2",
        "song_label": "கந்தர் அநுபூதி: உருவாய் அருவாய்",
    },
    {
        "track_id": "-unILRjNLHQ",
        "old_youtube_id": "lGTIGx3YMcY",
        "channel_key": "@gurukuladesam2",
        "channel_handle": "@GuruKulaDesam2",
        "song_label": "திருவருட்பா: சிவ சுப்ரமணியர் திருவிருத்தம்",
    },
    {
        "track_id": "B6yVe6HM8Ok",
        "old_youtube_id": "yRmGwie9ZNU",
        "channel_key": "@gurukuladesam2",
        "channel_handle": "@GuruKulaDesam2",
        "song_label": "திருப்புகழ்: ஆறுமுகம் ஆறுமுகம்",
    },
    {
        "track_id": "3oJ2OPG-WCs",
        "old_youtube_id": "-7n4U-4do6U",
        "channel_key": "@gurukuladesam2",
        "channel_handle": "@GuruKulaDesam2",
        "song_label": "திருப்புகழ்: முத்தைத் தரு",
    },
]


def load_queue() -> list[dict]:
    if QUEUE_FILE.exists():
        try:
            return json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    items = []
    for base in DEFAULT_LEGACY_ITEMS:
        it = dict(base)
        it["status"] = "pending_discography"
        it["new_youtube_id"] = None
        it["video_path"] = None
        it["meta_path"] = None
        it["old_marked_private"] = False
        it["updated_at"] = None
        items.append(it)
    save_queue(items)
    return items


def save_queue(items: list[dict]):
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_FILE.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")


def reset_queue_for_discography(items: list[dict]) -> list[dict]:
    by_old = {b["old_youtube_id"]: b for b in DEFAULT_LEGACY_ITEMS}
    updated = []
    for it in items:
        base = by_old.get(it["old_youtube_id"], {})
        new_it = dict(it)
        if base.get("track_id"):
            new_it["track_id"] = base["track_id"]
        if base.get("legacy_track_id"):
            new_it["legacy_track_id"] = base["legacy_track_id"]
        if base.get("song_label"):
            new_it["song_label"] = base["song_label"]
        if new_it.get("status") == "new_flow_marked_private":
            new_it["discarded_flow_youtube_id"] = new_it.get("new_youtube_id")
            new_it["new_youtube_id"] = None
            new_it["video_path"] = None
            new_it["meta_path"] = None
            new_it["status"] = "pending_discography"
            new_it["old_marked_private"] = False
            new_it["updated_at"] = datetime.now(IST).isoformat()
        updated.append(new_it)
    save_queue(updated)
    return updated


def mark_old_video_private(channel_key: str, old_youtube_id: str) -> bool:
    """Marks `old_youtube_id` as `private` on `channel_key` ONLY when explicitly requested."""
    for attempt in range(3):
        try:
            yt, _, cfg = get_channel_youtube_service(channel_key)
            mine = yt.channels().list(part="id", mine=True).execute().get("items", [])
            if not mine or mine[0]["id"] != cfg["channel_id"]:
                raise RuntimeError(f"Channel mismatch on {channel_key}")

            v_res = yt.videos().list(part="status", id=old_youtube_id).execute().get("items", [])
            if not v_res:
                print(f"  ℹ️ Old video {old_youtube_id} not found on {cfg['handle']} (already removed).")
                return True

            status_obj = v_res[0].get("status", {})
            if status_obj.get("privacyStatus") == "private":
                print(f"  ✅ Old video {old_youtube_id} is already marked PRIVATE.")
                return True

            yt.videos().update(
                part="status",
                body={
                    "id": old_youtube_id,
                    "status": {
                        "privacyStatus": "private",
                        "selfDeclaredMadeForKids": bool(status_obj.get("selfDeclaredMadeForKids", False)),
                    },
                },
            ).execute()
            print(f"  🔒 [MARKED PRIVATE] Old Short https://youtube.com/shorts/{old_youtube_id} -> PRIVATE!")
            return True
        except Exception as e:
            print(f"  ⚠️ Attempt {attempt + 1} marking {old_youtube_id} private failed: {e}")
            time.sleep(2)
    return False


def ensure_all_discography_shorts_built(items: list[dict], force_rebuild: bool = False):
    """Clips 9:16 Chorus-aligned Shorts strictly from @guru-kula-desam Master Films (use_flow=False)."""
    for idx, item in enumerate(items, 1):
        if not force_rebuild and item["status"] in ("completed", "ready_to_republish"):
            if item.get("video_path") and (ROOT / item["video_path"]).exists() and item.get("meta_path") and (ROOT / item["meta_path"]).exists():
                m = json.loads((ROOT / item["meta_path"]).read_text(encoding="utf-8"))
                if m.get("visual_source_mode") == "original_master_clip" and m.get("clip_anchor_mode") == "chorus_v1":
                    continue

        tid = item["track_id"]
        ch_hnd = item["channel_handle"]
        print(f"\n[{idx}/{len(items)}] 🎬 Clipping @guru-kula-desam Master Film (Chorus Start) for {tid} ({item['song_label']})...")
        meta = build_short_for_track(tid, force_rebuild=True, brand_handle=ch_hnd, use_flow=False)
        if meta.get("visual_source_mode") != "original_master_clip" or meta.get("clip_anchor_mode") != "chorus_v1":
            raise RuntimeError(f"Guard failed for {tid}: mode={meta.get('visual_source_mode')} anchor={meta.get('clip_anchor_mode')}")

        meta_file = SHORTS_META_DIR / f"short_{meta['deity']}_{tid}.json"
        item["video_path"] = meta["video_path"]
        item["meta_path"] = str(meta_file.relative_to(ROOT))
        item["youtube_film_id"] = meta.get("youtube_film_id")
        item["chorus_start_sec"] = meta.get("peak_start_sec")
        item["duration_sec"] = meta.get("duration_sec")
        if item["status"] != "completed":
            item["status"] = "ready_to_republish"
        item["updated_at"] = datetime.now(IST).isoformat()
        save_queue(items)
        print(
            f"  ✅ Built Discography Chorus Short: {meta['video_path']} "
            f"[{meta.get('peak_start_sec')}s -> {round(meta.get('peak_start_sec', 0) + meta.get('duration_sec', 0), 2)}s] "
            f"(master={meta.get('youtube_film_id')}, replaces {item['old_youtube_id']})"
        )


def publish_ready_replacements(items: list[dict], mark_old_private: bool = False, channel_filter: str = None) -> int:
    """
    Uploads ready @guru-kula-desam Chorus-clipped Shorts as PUBLIC while leaving the 11 original
    public Shorts untouched (`public` as-is) by default unless `mark_old_private=True`.
    """
    reg = load_published_registry()
    pub_map = reg.get("published_shorts", {})
    blocked_channels: set[str] = set()
    replaced_count = 0

    for item in items:
        if channel_filter and item["channel_key"] != channel_filter.lower():
            continue

        if mark_old_private and item.get("new_youtube_id") and not item.get("old_marked_private"):
            if mark_old_video_private(item["channel_key"], item["old_youtube_id"]):
                item["old_marked_private"] = True
                item["status"] = "completed"
                item["updated_at"] = datetime.now(IST).isoformat()
                save_queue(items)
            continue

        if item["status"] != "ready_to_republish":
            continue

        ch_key = item["channel_key"]
        if ch_key in blocked_channels:
            continue

        video_rel = item.get("video_path")
        meta_rel = item.get("meta_path")
        if not video_rel or not (ROOT / video_rel).exists() or not meta_rel or not (ROOT / meta_rel).exists():
            continue

        meta = json.loads((ROOT / meta_rel).read_text(encoding="utf-8"))
        if meta.get("visual_source_mode") != "original_master_clip" or meta.get("clip_anchor_mode") != "chorus_v1":
            print(f"  ❌ Skipping {item['track_id']}: non-chorus/non-discography build.")
            continue

        yt_vid_id = upload_short_via_api(meta, publish_at_dt=None, channel_key=ch_key)

        if yt_vid_id == "CHANNEL_UPLOAD_LIMIT":
            blocked_channels.add(ch_key)
            continue

        if yt_vid_id:
            item["new_youtube_id"] = yt_vid_id
            if mark_old_private:
                priv_ok = mark_old_video_private(ch_key, item["old_youtube_id"])
                item["old_marked_private"] = priv_ok
                item["status"] = "completed" if priv_ok else "uploaded_pending_private"
            else:
                item["old_marked_private"] = False
                item["status"] = "completed"
                print(f"  ✅ Kept existing video https://youtube.com/shorts/{item['old_youtube_id']} PUBLIC as-is (for manual review).")
            item["updated_at"] = datetime.now(IST).isoformat()
            save_queue(items)

            tid = item.get("legacy_track_id") or item["track_id"]
            pub_map[f"{tid}__discography_upgrade"] = {
                "youtube_short_id": yt_vid_id,
                "legacy_track_id": tid,
                "upgraded_from_video_id": item["old_youtube_id"],
                "channel_handle": item["channel_handle"],
                "short_url": f"https://youtube.com/shorts/{yt_vid_id}",
                "title": meta["title"],
                "deity": meta["deity"],
                "visual_source_mode": "original_master_clip",
                "visual_source_file": meta.get("visual_source_file"),
                "youtube_film_id": meta.get("youtube_film_id"),
                "clip_anchor_mode": meta.get("clip_anchor_mode"),
                "peak_start_sec": meta.get("peak_start_sec"),
                "duration_sec": meta.get("duration_sec"),
                "panchangam_occasion": meta.get("panchangam", {}).get("occasion_badge_ta", ""),
                "uploaded_at": datetime.now(IST).isoformat(),
                "scheduled_for": None,
                "status": "public",
            }
            reg["published_shorts"] = pub_map
            save_published_registry(reg)
            replaced_count += 1

    return replaced_count


def print_queue_status():
    items = load_queue()
    print("=" * 100)
    print("🔄 @GURU-KULA-DESAM DISCOGRAPHY CHORUS UPGRADE SHORTS QUEUE (ORIGINAL 11 KEPT PUBLIC AS-IS)")
    print("=" * 100)
    for idx, it in enumerate(items, 1):
        new_str = f"-> NEW: https://youtube.com/shorts/{it['new_youtube_id']}" if it.get("new_youtube_id") else ""
        priv_str = "🔒 OLD=PRIVATE" if it.get("old_marked_private") else "✅ OLD KEPT PUBLIC AS-IS"
        win_str = f"[{it.get('chorus_start_sec')}s +{it.get('duration_sec')}s]" if it.get("chorus_start_sec") is not None else ""
        print(
            f"  {idx:2d}. [{it['channel_handle']:<16}] {it['track_id']:<12} | Old={it['old_youtube_id']} | "
            f"{it['status']:<20} | {win_str:<16} | {priv_str} {new_str}\n      {it['song_label']}"
        )
    print("=" * 100)


def main():
    ap = argparse.ArgumentParser(description="Publish Chorus-clipped @guru-kula-desam Shorts (keeps old videos public as-is)")
    ap.add_argument("--status", action="store_true", help="Print status of all 11 Discography Chorus upgrade Shorts")
    ap.add_argument("--reset-for-discography", action="store_true", help="Reset discarded Flow queue entries to pending_discography")
    ap.add_argument("--build-only", action="store_true", help="Build all 11 Discography Chorus Shorts without uploading")
    ap.add_argument("--force-rebuild", action="store_true", help="Force rebuild all 11 Shorts from @guru-kula-desam Master Films")
    ap.add_argument("--upload-only", action="store_true", help="Only upload already-built Discography Chorus Shorts")
    ap.add_argument("--channel", type=str, default=None, help="Filter upload to @gurukuladesam or @gurukuladesam2")
    ap.add_argument("--mark-old-private", action="store_true", help="Explicitly mark old videos private (disabled by default)")
    ap.add_argument("--sync-git", action="store_true", help="Push updated registry JSON to remote")
    args = ap.parse_args()

    items = load_queue()
    if args.reset_for_discography:
        items = reset_queue_for_discography(items)

    if args.status:
        print_queue_status()
        return

    if not args.upload_only:
        ensure_all_discography_shorts_built(items, force_rebuild=args.force_rebuild)

    if args.build_only:
        print_queue_status()
        return

    replaced = publish_ready_replacements(items, mark_old_private=args.mark_old_private, channel_filter=args.channel)
    if args.sync_git and replaced > 0:
        from tools.shorts_autonomous_daemon import push_registry_to_remote
        push_registry_to_remote()
    print(f"\n🏁 Discography Chorus Upgrade Summary: {replaced} new Shorts published (original 11 kept PUBLIC as-is).")
    print_queue_status()


if __name__ == "__main__":
    main()
