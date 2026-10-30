#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/republish_legacy_with_flow.py
Publishes upgraded native 9:16 Google Flow Shorts across @GuruKulaDesam (4) and @GuruKulaDesam2 (7)
while keeping all already-published legacy videos untouched (`public` as-is) by default so they can
be reviewed first and switched to `Private` manually when desired (or via explicit `--mark-old-private`).
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
    # @GuruKulaDesam2 (7 Devotional Shorts — ordered highest views / highest impact first!)
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
        "track_id": "-L3VXkM2MTY",
        "old_youtube_id": "QWj6z4qXaqU",
        "channel_key": "@gurukuladesam2",
        "channel_handle": "@GuruKulaDesam2",
        "song_label": "கந்தர் அநுபூதி: உருவாய் அருவாய் II",
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
        it["status"] = "pending_flow"
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


def mark_old_video_private(channel_key: str, old_youtube_id: str) -> bool:
    """Marks `old_youtube_id` as `private` on `channel_key` after verifying channel ownership."""
    for attempt in range(3):
        try:
            yt, pid, cfg = get_channel_youtube_service(channel_key)
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
            print(f"  🔒 [MARKED PRIVATE] Old bad-visual Short https://youtube.com/shorts/{old_youtube_id} -> PRIVATE!")
            return True
        except Exception as e:
            print(f"  ⚠️ Attempt {attempt + 1} marking {old_youtube_id} private failed: {e}")
            time.sleep(2)
    return False


def ensure_all_flow_shorts_built(items: list[dict], scenes_per_short: int = 4):
    """Generates brand-new native 9:16 Google Flow clips and builds 1080x1920 Shorts for all pending items."""
    import subprocess
    from tools.flow_autonomous_generator import CDP_PORT, generate_flow_clips_for_short

    try:
        for idx, item in enumerate(items, 1):
            if item["status"] in ("completed", "ready_to_republish"):
                if item.get("video_path") and (ROOT / item["video_path"]).exists():
                    continue

            tid = item["track_id"]
            ch_hnd = item["channel_handle"]
            print(f"\n[{idx}/{len(items)}] 🎨 Generating New Native 9:16 Flow Video for {tid} ({item['song_label']})...")
            try:
                clips = generate_flow_clips_for_short(tid, scene_count=scenes_per_short)
            except Exception as e:
                print(f"  ⚠️ Flow generation error for {tid}: {e}")
                continue
            if len(clips) < 3:
                print(f"  ❌ Flow returned only {len(clips)} clips for {tid}; will retry.")
                continue

            meta = build_short_for_track(tid, force_rebuild=True, brand_handle=ch_hnd, use_flow=True)
            meta_file = SHORTS_META_DIR / f"short_{meta['deity']}_{tid}.json"
            item["video_path"] = meta["video_path"]
            item["meta_path"] = str(meta_file.relative_to(ROOT))
            item["status"] = "ready_to_republish"
            item["updated_at"] = datetime.now(IST).isoformat()
            save_queue(items)
            print(f"  ✅ Built Flow Replacement Short: {meta['video_path']} (ready to replace {item['old_youtube_id']})")
    finally:
        subprocess.run(["pkill", "-f", f"[r]emote-debugging-port={CDP_PORT}"], check=False)


def publish_ready_replacements(items: list[dict], mark_old_private: bool = False) -> int:
    """
    Uploads ready Flow upgrade Shorts as PUBLIC while leaving already-published videos untouched
    (`public` as-is) by default unless `mark_old_private=True` is explicitly requested.
    Safe to call from cron (`--upload-only`) without needing a display/browser!
    """
    reg = load_published_registry()
    pub_map = reg.get("published_shorts", {})
    blocked_channels: set[str] = set()
    replaced_count = 0

    for item in items:
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

            tid = item["track_id"]
            pub_map[f"{tid}__flow_upgrade"] = {
                "youtube_short_id": yt_vid_id,
                "legacy_track_id": tid,
                "upgraded_from_video_id": item["old_youtube_id"],
                "channel_handle": item["channel_handle"],
                "short_url": f"https://youtube.com/shorts/{yt_vid_id}",
                "title": meta["title"],
                "deity": meta["deity"],
                "visual_source_mode": "google_flow_dedicated",
                "visual_source_file": f"google_flow_renders/{tid}",
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
    print("=" * 95)
    print("🔄 GOOGLE FLOW 9:16 UPGRADE SHORTS QUEUE (EXISTING VIDEOS KEPT PUBLIC AS-IS)")
    print("=" * 95)
    for idx, it in enumerate(items, 1):
        new_str = f"-> NEW: https://youtube.com/shorts/{it['new_youtube_id']}" if it.get("new_youtube_id") else ""
        priv_str = "🔒 OLD=PRIVATE" if it.get("old_marked_private") else "✅ OLD KEPT PUBLIC AS-IS"
        print(
            f"  {idx:2d}. [{it['channel_handle']:<16}] {it['track_id']} | Old={it['old_youtube_id']} | "
            f"{it['status']:<20} | {priv_str} {new_str}\n      {it['song_label']}"
        )
    print("=" * 95)


def main():
    ap = argparse.ArgumentParser(description="Publish upgraded native 9:16 Flow Shorts (keeps old videos public as-is by default)")
    ap.add_argument("--status", action="store_true", help="Print status of all 11 Flow upgrade Shorts")
    ap.add_argument("--upload-only", action="store_true", help="Only upload already-built Flow upgrade Shorts")
    ap.add_argument("--mark-old-private", action="store_true", help="Explicitly mark old videos private (disabled by default)")
    ap.add_argument("--sync-git", action="store_true", help="Push updated queue & registry JSONs to remote")
    ap.add_argument("--scenes", type=int, default=4, help="Number of native 9:16 Flow clips per Short (default: 4)")
    args = ap.parse_args()

    items = load_queue()
    if args.status:
        print_queue_status()
        return

    if not args.upload_only:
        ensure_all_flow_shorts_built(items, scenes_per_short=args.scenes)

    replaced = publish_ready_replacements(items, mark_old_private=args.mark_old_private)
    if args.sync_git and replaced > 0:
        from tools.shorts_autonomous_daemon import push_registry_to_remote
        push_registry_to_remote()
    print(f"\n🏁 Flow Upgrade Pass Summary: {replaced} new Flow Shorts published (existing videos kept PUBLIC as-is).")
    print_queue_status()


if __name__ == "__main__":
    main()
