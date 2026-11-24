#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exports `/tmp/curriculum_324_topics.json` for the parallel `run_workflow` script,
and assembles + validates all 324 complete episode scripts (`Script.md` + `episode_spec.json`)
into both `/home/shishyan/GitHub/Shishyan/GuruKulaDesam/data/women_3pillars_324/` and
`/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/women_3pillars_324/`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from curriculum_324_topics import PILLAR1_TOPICS, PILLAR2_TOPICS, PILLAR3_TOPICS, verify_topics  # noqa: E402
from women_3pillars_catalog import EPISODES as PILOT_EPISODES, SCENE_STYLE_PREFIX  # noqa: E402

DATA_OUT = Path("/home/shishyan/GitHub/Shishyan/GuruKulaDesam/data/women_3pillars_324")
SHARDS_DIR = DATA_OUT / "shards"
DRIVE_LOCAL_OUT = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/women_3pillars_324")

LIVE_PILOTS_YOUTUBE = {
    "P1_001": {
        "pilot_idx": 0,
        "legacy_gkd_unlisted_id": "k5S4-mhe47A",
        "local_mp4": "/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep01_amman_garbarakshambigai/ep01_amman_garbarakshambigai.mp4",
        "local_thumb": "/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep01_amman_garbarakshambigai/ep01_amman_garbarakshambigai_Thumbnail.jpg",
        "gdrive_mp4": "gdrive:GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep01_amman_garbarakshambigai/ep01_amman_garbarakshambigai.mp4",
        "gdrive_thumb": "gdrive:GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep01_amman_garbarakshambigai/ep01_amman_garbarakshambigai_Thumbnail.jpg",
        "drive_mp4_link": "https://drive.google.com/open?id=10TFEv9SlQq-jGQKD_6iS_PA4pQWAZ6lc",
        "drive_thumb_link": "https://drive.google.com/open?id=1-veVfvgYtSPJCJTIW6YcE4pJY6nu4iHp",
    },
    "P2_001": {
        "pilot_idx": 1,
        "legacy_gkd_unlisted_id": "X53iNUO6YC8",
        "local_mp4": "/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep02_patti_vaithiyam_ulundhukali/ep02_patti_vaithiyam_ulundhukali.mp4",
        "local_thumb": "/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep02_patti_vaithiyam_ulundhukali/ep02_patti_vaithiyam_ulundhukali_Thumbnail.jpg",
        "gdrive_mp4": "gdrive:GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep02_patti_vaithiyam_ulundhukali/ep02_patti_vaithiyam_ulundhukali.mp4",
        "gdrive_thumb": "gdrive:GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep02_patti_vaithiyam_ulundhukali/ep02_patti_vaithiyam_ulundhukali_Thumbnail.jpg",
        "drive_mp4_link": "https://drive.google.com/open?id=194kCHZ5YvxGytsRONqKhdZLQNRg-GE6W",
        "drive_thumb_link": "https://drive.google.com/open?id=1ZdomS6dQ0vjF1bL7RLRGCXrgVcQND204",
    },
    "P3_001": {
        "pilot_idx": 2,
        "legacy_gkd_unlisted_id": "BfmH7nQLwjw",
        "local_mp4": "/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep03_pooja_deepa_shastram/ep03_pooja_deepa_shastram.mp4",
        "local_thumb": "/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep03_pooja_deepa_shastram/ep03_pooja_deepa_shastram_Thumbnail.jpg",
        "gdrive_mp4": "gdrive:GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep03_pooja_deepa_shastram/ep03_pooja_deepa_shastram.mp4",
        "gdrive_thumb": "gdrive:GuruKulaDesam/Assets/tamil-daily-life/women_series_pilots/ep03_pooja_deepa_shastram/ep03_pooja_deepa_shastram_Thumbnail.jpg",
        "drive_mp4_link": "https://drive.google.com/open?id=1yRLwWuDHWBHs8SjAsDY8Kex_v0lCCIKt",
        "drive_thumb_link": "https://drive.google.com/open?id=1ypmipCY7Fl8CDHe975GhjoSke3TUhHpN",
    },
}

BANNED_CTA_REGEXES = [
    r"\bsubscribe\b", r"\blike\b", r"\bcomment\b", r"\bshare\b", r"\bnotification\b", r"\bbell\b",
    r"சப்ஸ்கிரைப்", r"(?:^|\s)லைக்(?:\s|$|[,.!?])", r"கமெண்ட்", r"(?:^|\s)ஷேர்(?:\s|$|[,.!?])",
    r"பெல் பட்டன்", r"மறக்காம", r"அடுத்த காணொளி", r"அடுத்த எபிசோட்", r"சேனலை",
]
BANNED_TIMING_REGEXES = [
    r"ராகு\s*காலம்", r"எமகண்டம்", r"குளிகை", r"கௌரி\s*நல்ல\s*நேரம்",
]
BANNED_PROMPT_SUBSTRINGS = ["24K", "24k", "16:9", "completely blank", "empty box"]

TAMIL_NUM_WORDS = {
    "1008": "ஆயிரத்து எட்டு",
    "108": "நூற்று எட்டு",
    "48": "நாற்பத்தி எட்டு",
    "36": "முப்பத்தி ஆறு",
    "32": "முப்பத்தி இரண்டு",
    "30": "முப்பது",
    "28": "இருபத்தி எட்டு",
    "27": "இருபத்தி ஏழு",
    "24": "இருபத்தி நான்கு",
    "21": "இருபத்தி ஒன்று",
    "20": "இருபது",
    "18": "பதினெட்டு",
    "16": "பதினாறு",
    "15": "பதினைந்து",
    "12": "பன்னிரண்டு",
    "11": "பதினோரு",
    "10": "பத்து",
    "9": "ஒன்பது",
    "8": "எட்டு",
    "7": "ஏழு",
    "6": "ஆறு",
    "5": "ஐந்து",
    "4": "நான்கு",
    "3": "மூன்று",
    "2": "இரண்டு",
    "1": "ஒரு",
    "0": "பூஜ்ஜியம்",
}


def clean_spoken_paragraph(p: str) -> str:
    t = p.strip()
    # Replace known integers if any slipped in
    for num_s, word_ta in sorted(TAMIL_NUM_WORDS.items(), key=lambda kv: -len(kv[0])):
        t = re.sub(rf"\b{num_s}\b", word_ta, t)
    # Remove colons, semicolons, hyphens, em/en dashes, parentheses, brackets, quotes
    t = re.sub(r"\s*[—–]\s*", ", ", t)
    t = re.sub(r"\s+-\s+", ", ", t)
    t = re.sub(r"(?<=\S)-(?=\S)", " ", t)
    t = t.replace("-", " ")
    t = re.sub(r"\s*[:;]\s*", ", ", t)
    t = re.sub(r"\s*[()\[\]{}]\s*", " ", t)
    t = t.replace('"', "").replace("'", "").replace("‘", "").replace("’", "").replace("“", "").replace("”", "")
    # Remove banned next-episode phrases if any slipped into closing sentence
    t = re.sub(r"அடுத்த\s+(?:சிறப்புப்\s+)?(?:பதிவில்|காணொளியில்|எபிசோடில்)[^.!?]*[.!?]\s*", "", t)
    t = re.sub(r",\s*(?=[,.!?])", "", t)
    t = re.sub(r"\s+", " ", t).strip(" ,")
    if t and t[-1] not in ".!?":
        t += "."
    return t


def clean_prompt_text(p: str) -> str:
    t = p.strip()
    t = re.sub(r"\b24[Kk]\b", "solid polished", t)
    t = t.replace("16:9", "widescreen")
    t = t.replace("completely blank", "clean open atmospheric space")
    t = t.replace("empty box", "clean space")
    return re.sub(r"\s+", " ", t).strip()


def build_thumbnail_prompt(pillar_code: str, badge_ta: str, main_ta: str, hero_en: str) -> str:
    hero_clean = clean_prompt_text(hero_en)
    genre = "traditional wellness" if pillar_code == "P2" else "devotional theatrical"
    return (
        f"A-grade Tamil {genre} cinema movie-poster artwork, widescreen full-bleed seamless composition "
        f"(pure poster artwork with zero UI buttons or play icons). "
        f"Right side (right half of the frame): Zoomed-in chest-up commanding scene — {hero_clean}, "
        f"illuminated by intense warm golden rim-lighting and glowing brass oil lamps. "
        f"Left side (left half of the frame): Monumental, massive TV-readable Tamil cinema poster typography occupying the left half with grand prominence. "
        f"Top: Distinct dark midnight-indigo pill badge with glowing gold border displaying {badge_ta} (no quotation marks). "
        f"Center/Bottom: Huge, gigantic 3D-extruded solid polished gold Tamil cinema lettering {main_ta} (written once cleanly) "
        f"across a rich royal crimson-maroon velvet banner with sharp metallic bevels, deep drop-shadows, and specular glints, perfectly legible on mobile screens. "
        f"Background: Full-bleed warm South Indian sacred temple or heritage home backdrop with gentle golden mist, zero dead space, "
        f"no text or numbers in the lower-right corner."
    )


def export_curriculum_json() -> None:
    verify_topics()
    SHARDS_DIR.mkdir(parents=True, exist_ok=True)
    pillars = [
        ("P1", "108 அம்மன் தல வரலாறு & விரத மகிமை", PILLAR1_TOPICS),
        ("P2", "108 அஞ்சறைப்பெட்டி & பாட்டி வைத்தியம்", PILLAR2_TOPICS),
        ("P3", "108 பூஜை அறை & தீப சாஸ்திர ரகசியங்கள்", PILLAR3_TOPICS),
    ]
    items = []
    for p_code, p_title, t_list in pillars:
        for idx, (ep_code, short_slug, topic_ta, badge_ta, main_ta, brief) in enumerate(t_list, start=1):
            items.append(
                {
                    "ep_code": ep_code,
                    "pillar_code": p_code,
                    "pillar_title_ta": p_title,
                    "ep_num_in_pillar": idx,
                    "slug": f"{ep_code.lower()}_{short_slug}",
                    "topic_ta": topic_ta,
                    "thumb_badge_ta": badge_ta,
                    "thumb_main_ta": main_ta,
                    "core_focus_brief": brief,
                    "is_live_pilot": ep_code in LIVE_PILOTS_YOUTUBE,
                }
            )
    Path("/tmp/curriculum_324_topics.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Exported {len(items)} curriculum items to /tmp/curriculum_324_topics.json (pending authoring: {sum(not x['is_live_pilot'] for x in items)})")


def convert_pilot_to_spec(meta: dict) -> dict:
    ep_code = meta["ep_code"]
    pinfo = LIVE_PILOTS_YOUTUBE[ep_code]
    src = PILOT_EPISODES[pinfo["pilot_idx"]]
    secs = []
    for s in src["sections"]:
        secs.append(
            {
                "id": s["id"],
                "badge": s["badge"],
                "is_story": s["is_story"],
                "paragraphs": [clean_spoken_paragraph(p) for p in s["paragraphs"]],
            }
        )
    yt_title = src["yt_title"].replace("| Guru Kula Desam", "| @TamilDailyLife").strip()
    yt_desc = src["yt_description"]
    if "#TamilVirtues" not in yt_desc:
        yt_desc = yt_desc.rstrip() + " #TamilVirtues"
    return {
        "ep_code": ep_code,
        "pillar_code": meta["pillar_code"],
        "pillar_title_ta": meta["pillar_title_ta"],
        "ep_num_in_pillar": meta["ep_num_in_pillar"],
        "slug": meta["slug"],
        "title_pill": src["title_pill"],
        "yt_title": yt_title,
        "yt_description": yt_desc,
        "thumb_badge_ta": meta["thumb_badge_ta"],
        "thumb_main_ta": meta["thumb_main_ta"],
        "thumbnail_prompt": src["thumbnail_prompt"],
        "shot_prompts": [clean_prompt_text(sp) for sp in src["shot_prompts"]],
        "sections": secs,
        "status": "RENDERED_READY_FOR_TAMILDAILYLIFE",
        "legacy_gkd_unlisted_id": pinfo["legacy_gkd_unlisted_id"],
        "local_mp4": pinfo["local_mp4"],
        "local_thumb": pinfo["local_thumb"],
        "gdrive_mp4": pinfo["gdrive_mp4"],
        "gdrive_thumb": pinfo["gdrive_thumb"],
        "drive_mp4_link": pinfo["drive_mp4_link"],
        "drive_thumb_link": pinfo["drive_thumb_link"],
        "youtube_video_id": None,
        "youtube_url": None,
    }


def validate_spec(spec: dict) -> None:
    ec = spec["ep_code"]
    assert len(spec["sections"]) == 5, f"{ec}: expected 5 sections, got {len(spec['sections'])}"
    assert len(spec["shot_prompts"]) == 16, f"{ec}: expected 16 shots, got {len(spec['shot_prompts'])}"
    assert len(set(spec["shot_prompts"])) == 16, f"{ec}: duplicate shot prompts!"

    for p in spec["shot_prompts"] + [spec["thumbnail_prompt"]]:
        for bad in BANNED_PROMPT_SUBSTRINGS:
            assert bad not in p, f"{ec}: banned prompt token {bad!r} in {p[:100]}"

    for fld in ("yt_title", "yt_description", "title_pill"):
        for pat in BANNED_CTA_REGEXES:
            assert not re.search(pat, spec[fld], re.IGNORECASE), f"{ec}.{fld} matched CTA {pat}"

    total_words = 0
    for sec in spec["sections"]:
        assert len(sec["paragraphs"]) >= 3, f"{ec}.{sec['id']}: fewer than 3 paragraphs"
        for para in sec["paragraphs"]:
            total_words += len(para.split())
            assert not re.search(r"[0-9]", para), f"{ec}.{sec['id']} has digits: {para}"
            for ch in (":", ";", "-", "(", ")", "[", "]"):
                assert ch not in para, f"{ec}.{sec['id']} has char {ch!r}: {para}"
            for pat in BANNED_CTA_REGEXES:
                assert not re.search(pat, para, re.IGNORECASE), f"{ec}.{sec['id']} matched CTA {pat}: {para}"
            for pat in BANNED_TIMING_REGEXES:
                assert not re.search(pat, para, re.IGNORECASE), f"{ec}.{sec['id']} matched timing {pat}: {para}"
    assert total_words >= 280, f"{ec}: script too short ({total_words} words)"


def assemble_all_324() -> None:
    curriculum = json.loads(Path("/tmp/curriculum_324_topics.json").read_text(encoding="utf-8"))
    by_code = {x["ep_code"]: x for x in curriculum}

    authored_raw = {}
    for sf in sorted(SHARDS_DIR.glob("shard_*.json")):
        arr = json.loads(sf.read_text(encoding="utf-8"))
        for item in arr:
            authored_raw[item["ep_code"]] = item

    pillar_folders = {
        "P1": "pillar1_108_amman_varalaru",
        "P2": "pillar2_108_patti_vaithiyam",
        "P3": "pillar3_108_pooja_deepa_shastram",
    }
    pillar_hashtags = {
        "P1": "#TamilDailyLife #TamilVirtues #AmmanVaralaru #SthalaPuranam #Vratham #TamilDevotional #GuruKulaDesam",
        "P2": "#TamilDailyLife #TamilVirtues #PattiVaithiyam #Anjaraipetti #TamilTraditionalFood #WomenHealthTamil #GuruKulaDesam",
        "P3": "#TamilDailyLife #TamilVirtues #DeepaShastram #PoojaRoomTipsTamil #MangalaIllaram #TamilDevotional #GuruKulaDesam",
    }
    sec_ids = ["s1_intro", "s2_part1", "s3_part2", "s4_practice", "s5_closing"]

    all_specs = []
    by_pillar = {"P1": [], "P2": [], "P3": []}

    for meta in curriculum:
        ec = meta["ep_code"]
        p_code = meta["pillar_code"]
        if meta["is_live_pilot"]:
            spec = convert_pilot_to_spec(meta)
        else:
            assert ec in authored_raw, f"Missing authored episode {ec} in shards!"
            raw = authored_raw[ec]
            secs = []
            for idx, rs in enumerate(raw["sections"]):
                secs.append(
                    {
                        "id": sec_ids[idx],
                        "badge": rs["badge"].strip(),
                        "is_story": idx in (1, 2),
                        "paragraphs": [clean_spoken_paragraph(p) for p in rs["paragraphs"]],
                    }
                )
            bullets = "\n".join(f"- {b.strip().lstrip('- ').strip()}" for b in raw["summary_bullets_ta"])
            yt_title = f"{meta['topic_ta']} | @TamilDailyLife"
            if len(yt_title) > 98:
                yt_title = meta["topic_ta"][:95].rstrip() + "..."
            yt_desc = (
                f"{meta['topic_ta']} — தமிழர் பண்பாடு (வாழ்வியல் நெறி) | @TamilDailyLife வழங்கும் மகளிர் சிறப்புத் தொடர் ({meta['pillar_title_ta']}).\n\n"
                f"இந்தப் பதிவில்:\n{bullets}\n\n"
                f"{pillar_hashtags[p_code]}"
            )
            # Clean any accidental CTA words in bullets
            for pat in BANNED_CTA_REGEXES:
                yt_desc = re.sub(pat, "", yt_desc, flags=re.IGNORECASE)

            shots = [clean_prompt_text(sp) for sp in raw["shot_prompts"]]
            # Guarantee uniqueness if two shots were ever identical
            dedup_shots = []
            seen_s = set()
            for s_i, sp in enumerate(shots):
                if sp in seen_s:
                    sp = f"{sp} (angle variation {s_i + 1})"
                seen_s.add(sp)
                dedup_shots.append(sp)

            spec = {
                "ep_code": ec,
                "pillar_code": p_code,
                "pillar_title_ta": meta["pillar_title_ta"],
                "ep_num_in_pillar": meta["ep_num_in_pillar"],
                "slug": meta["slug"],
                "title_pill": f"{meta['thumb_badge_ta']} • {meta['thumb_main_ta']}",
                "yt_title": yt_title,
                "yt_description": yt_desc,
                "thumb_badge_ta": meta["thumb_badge_ta"],
                "thumb_main_ta": meta["thumb_main_ta"],
                "thumbnail_prompt": build_thumbnail_prompt(p_code, meta["thumb_badge_ta"], meta["thumb_main_ta"], raw["thumb_hero_en"]),
                "shot_prompts": dedup_shots,
                "sections": secs,
                "status": "SCRIPT_READY",
                "youtube_video_id": None,
                "youtube_url": None,
            }

        validate_spec(spec)
        all_specs.append(spec)
        by_pillar[p_code].append(spec)

        # Write per-episode Script.md + episode_spec.json to BOTH GitHub data dir & Local GoogleDrive dir
        p_sub = pillar_folders[p_code]
        md_lines = [
            f"# [{ec}] {meta['topic_ta']}",
            f"> **தொடர்**: {meta['pillar_title_ta']}  ",
            f"> **Thumbnail Badge**: `{spec['thumb_badge_ta']}` | **Main Title**: `{spec['thumb_main_ta']}`  ",
            f"> **Status**: `{spec['status']}`" + (f" ({spec['youtube_url']})" if spec["youtube_url"] else ""),
            "",
        ]
        for s in spec["sections"]:
            md_lines.append(f"## {s['badge']}")
            md_lines.append("")
            for para in s["paragraphs"]:
                md_lines.append(para)
                md_lines.append("")
        md_lines.append("## 16 Widescreen Visual Storyboard Prompts (`nano-pro`, $0 Video Spend)")
        for s_i, sp in enumerate(spec["shot_prompts"], start=1):
            md_lines.append(f"{s_i}. {SCENE_STYLE_PREFIX}{sp}")
        md_txt = "\n".join(md_lines).strip() + "\n"

        for root in (DATA_OUT, DRIVE_LOCAL_OUT):
            ep_folder = root / p_sub / f"{ec}_{meta['slug'].split('_', 1)[1]}"
            ep_folder.mkdir(parents=True, exist_ok=True)
            (ep_folder / "Script.md").write_text(md_txt, encoding="utf-8")
            (ep_folder / "episode_spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")

    # Write Master Pillar JSONs + Master 324 Manifest
    master_manifest = {
        "channel": "@TamilDailyLife",
        "channel_id": "UCDdEZ6CPCr6tIzWdDY9mzxg",
        "voice_name": "GuruKulaDesam",
        "voice_id": "Mu63hpI1uigjGMdYVTDr",
        "total_episodes": len(all_specs),
        "rendered_ready_count": sum(1 for s in all_specs if s["status"] == "RENDERED_READY_FOR_TAMILDAILYLIFE"),
        "published_count": sum(1 for s in all_specs if s["status"] == "PUBLISHED"),
        "script_ready_count": sum(1 for s in all_specs if s["status"] == "SCRIPT_READY"),
        "pillars": {
            "P1": {"folder": pillar_folders["P1"], "count": len(by_pillar["P1"])},
            "P2": {"folder": pillar_folders["P2"], "count": len(by_pillar["P2"])},
            "P3": {"folder": pillar_folders["P3"], "count": len(by_pillar["P3"])},
        },
        "episodes_index": [
            {
                "ep_code": s["ep_code"],
                "pillar_code": s["pillar_code"],
                "slug": s["slug"],
                "yt_title": s["yt_title"],
                "thumb_badge_ta": s["thumb_badge_ta"],
                "thumb_main_ta": s["thumb_main_ta"],
                "word_count": sum(len(p.split()) for sec in s["sections"] for p in sec["paragraphs"]),
                "status": s["status"],
                "youtube_url": s["youtube_url"],
            }
            for s in all_specs
        ],
    }

    for root in (DATA_OUT, DRIVE_LOCAL_OUT):
        root.mkdir(parents=True, exist_ok=True)
        (root / "pillar1_108_amman_varalaru.json").write_text(json.dumps(by_pillar["P1"], ensure_ascii=False, indent=2), encoding="utf-8")
        (root / "pillar2_108_patti_vaithiyam.json").write_text(json.dumps(by_pillar["P2"], ensure_ascii=False, indent=2), encoding="utf-8")
        (root / "pillar3_108_pooja_deepa_shastram.json").write_text(json.dumps(by_pillar["P3"], ensure_ascii=False, indent=2), encoding="utf-8")
        (root / "MASTER_324_WOMEN_SERIES_MANIFEST.json").write_text(json.dumps(master_manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    total_w = sum(x["word_count"] for x in master_manifest["episodes_index"])
    print(f"ASSEMBLED & VALIDATED ALL {len(all_specs)}/324 EPISODES! Total spoken words: {total_w:,} (~{total_w // 82:,} minutes of audio)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", action="store_true")
    ap.add_argument("--assemble", action="store_true")
    args = ap.parse_args()
    if args.export:
        export_curriculum_json()
    if args.assemble:
        assemble_all_324()
