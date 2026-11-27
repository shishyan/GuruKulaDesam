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

REPO = Path("/home/shishyan/GitHub/Shishyan/GuruKulaDesam")
STUDIO = Path("/home/shishyan/GitHub/Influenzian/Utility_Explainer_Studio/episodes/intelligentian")
REG = REPO / "production/intelligentian_published_registry.json"
TOKENS_DIR = REPO / "data/credentials/tokens_intelligentian"


def main():
    reg = json.loads(REG.read_text(encoding="utf-8"))
    toks = sorted(TOKENS_DIR.glob("token_*.json"))
    clients = []
    for tf in toks:
        c = Credentials.from_authorized_user_file(str(tf))
        if c.expired and c.refresh_token:
            c.refresh(Request())
            tf.write_text(c.to_json(), encoding="utf-8")
        clients.append((tf.name, build("youtube", "v3", credentials=c)))

    c_idx = 0
    applied = 0
    for ep_id, info in reg.get("published", {}).items():
        vid = info["youtubeVideoId"]
        thumb = STUDIO / ep_id / "thumbnail_16x9.jpg"
        if not thumb.exists():
            print(f"[Skip] Missing {thumb}")
            continue
        while c_idx < len(clients):
            tname, yt = clients[c_idx]
            try:
                yt.thumbnails().set(
                    videoId=vid,
                    media_body=MediaFileUpload(str(thumb), mimetype="image/jpeg", chunksize=1024 * 512, resumable=True),
                ).execute()
                print(f"[Thumbnail Applied] {ep_id} ({vid}) via {tname}")
                applied += 1
                break
            except Exception as exc:
                msg = str(exc)
                if "quotaExceeded" in msg:
                    c_idx += 1
                else:
                    print(f"[Error] {ep_id} ({vid}): {msg}")
                    break
    print(f"Done: applied {applied}/{len(reg.get('published', {}))} custom thumbnails.")


if __name__ == "__main__":
    main()
