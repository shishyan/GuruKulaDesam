#!/usr/bin/env python3
"""
One-command Custom Thumbnail Backfill for @intelligentian (`UCjVbL7GE3cHLOWRYAxZH65A`).
Run once after enabling YouTube Studio '2. Intermediate features' (Phone Verification) on this brand-new channel
to apply all 10 verified 50/50 3D movie-poster thumbnails (`thumbnail_16x9.jpg`) to the live videos!
"""
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

REPO = Path(__file__).resolve().parent.parent
STUDIO = Path("/home/shishyan/GitHub/Influenzian/Utility_Explainer_Studio/episodes/intelligentian")
NEWS_ARCHIVE_REMOTE = "gdrive:Intelligentian/NewsArchive"
REG = REPO / "production/intelligentian_published_registry.json"
TOKENS_DIR = REPO / "data/credentials/tokens_intelligentian"


def resolve_thumbnail_for_episode(ep_id: str, cache_dir: Path) -> Path | None:
    import subprocess

    for base in (STUDIO / ep_id, Path("/tmp/intelligentian_daily_news") / ep_id, cache_dir / ep_id):
        for name in (f"{ep_id}_thumb_16x9.jpg", "thumbnail_16x9.jpg", "poster_16x9.jpg"):
            cand = base / name
            if cand.exists() and cand.stat().st_size < 2 * 1024 * 1024:
                return cand
    dst = cache_dir / ep_id
    dst.mkdir(parents=True, exist_ok=True)
    for rpath in (
        f"{NEWS_ARCHIVE_REMOTE}/{ep_id}/thumbnail_16x9.jpg",
        f"gdrive:Intelligentian/CurriculumQueue/{ep_id}/thumbnail_16x9.jpg",
        f"gdrive:Intelligentian/Queue/{ep_id}/thumbnail_16x9.jpg",
    ):
        subprocess.run(["rclone", "copy", rpath, str(dst)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        cand = dst / "thumbnail_16x9.jpg"
        if cand.exists() and cand.stat().st_size < 2 * 1024 * 1024:
            return cand
    return None


def main():
    if not REG.exists():
        print(f"[Thumbnail Backfill] Registry not found at {REG}")
        return
    reg = json.loads(REG.read_text(encoding="utf-8"))
    toks = sorted(TOKENS_DIR.glob("token_*.json"))
    fallback_tok = REPO / "data/credentials/token_intelligentian.json"
    if not toks and fallback_tok.exists():
        toks = [fallback_tok]
    clients = []
    for tf in toks:
        try:
            c = Credentials.from_authorized_user_file(str(tf))
            if c.expired and c.refresh_token:
                c.refresh(Request())
                tf.write_text(c.to_json(), encoding="utf-8")
            clients.append((tf.name, build("youtube", "v3", credentials=c)))
        except Exception as exc:
            print(f"[OAuth Skip] {tf.name}: {exc}")

    if not clients:
        print("[Thumbnail Backfill] No active OAuth tokens found; skipping.")
        return

    cache_dir = Path("/tmp/intelligentian_thumb_cache")
    c_idx = 0
    applied = 0
    changed_reg = False
    for ep_id, info in reg.get("published", {}).items():
        if info.get("thumbnailApplied"):
            continue
        vid = info.get("youtubeVideoId", "")
        if not vid:
            continue
        thumb = resolve_thumbnail_for_episode(ep_id, cache_dir)
        if thumb is None or not thumb.exists():
            print(f"[Skip] Missing thumbnail for {ep_id}")
            continue
        while c_idx < len(clients):
            tname, yt = clients[c_idx]
            try:
                yt.thumbnails().set(
                    videoId=vid,
                    media_body=MediaFileUpload(str(thumb), mimetype="image/jpeg", chunksize=1024 * 512, resumable=True),
                ).execute()
                print(f"[Thumbnail Applied] {ep_id} ({vid}) via {tname}")
                info["thumbnailApplied"] = True
                changed_reg = True
                applied += 1
                break
            except Exception as exc:
                msg = str(exc)
                if "quotaExceeded" in msg:
                    c_idx += 1
                elif "forbidden" in msg.lower() or "permissions" in msg.lower() or "403" in msg:
                    print(f"[Notice] Channel custom thumbnails not yet unlocked ({vid}): {msg[:160]}")
                    if changed_reg:
                        REG.write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")
                    return
                else:
                    print(f"[Error] {ep_id} ({vid}): {msg[:180]}")
                    break
    if changed_reg:
        REG.write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Done: applied {applied} new custom thumbnails (total tracked={len(reg.get('published', {}))}).")


if __name__ == "__main__":
    main()
