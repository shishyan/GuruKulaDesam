#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/home/shishyan/GitHub/Shishyan/GuruKulaDesam/tools/tdl_women_lifestyle_builder.py
=================================================================================
54-Day Authentic Tamil Women's Lifestyle, Kitchen, Health & Family Harmony
Community Post Builder for @TamilDailyLife Category 3:
  `இல்லறம், சமையல் & மகளிர் நலக் குறிப்புகள்`
Covering Diwali 2026 (`2026-11-08`) through `2026-12-31` (54 unique days).

Guarantees:
1. Connects every day's family harmony reflection to `/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life/YYYY-MM-DD/STORY_METADATA.json`
   and seasonal Tamil calendar progression (`ஐப்பசி` monsoon -> `கார்த்திகை` lamp & rainy chill -> `மார்கழி` winter dawn).
2. 100% Zero-Repetition across all 54 dates:
   - 162 distinct South Indian culinary & time-saving kitchen tips (3/day)
   - 108 distinct women's health, herbal & chemical-free natural care tips (2/day)
   - 108 distinct household micro-savings, screen-free bonding & story-linked family harmony tips (2/day)
   - 54 distinct closing blessings (1/day)
3. Clean, dignified literary Tamil with ZERO emojis/pictographs/decorative Unicode,
   plain `- ` bullets, and `< 3,200` chars per post.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
DATA_JSON_PATH = REPO_ROOT / "data" / "tdl_women_54days_lifestyle.json"
ASSETS_BASE = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/tamil-daily-life")

START_DATE = date(2026, 11, 8)
END_DATE = date(2026, 12, 31)

GREGORIAN_MONTHS_TA = {
    1: "ஜனவரி",
    2: "பிப்ரவரி",
    3: "மார்ச்",
    4: "ஏப்ரல்",
    5: "மே",
    6: "ஜூன்",
    7: "ஜூலை",
    8: "ஆகஸ்ட்",
    9: "செப்டம்பர்",
    10: "அக்டோபர்",
    11: "நவம்பர்",
    12: "டிசம்பர்",
}

_LIFESTYLE_CACHE: dict[str, dict[str, Any]] | None = None


def strip_decorative_unicode(text: str) -> str:
    """
    Strip emojis, pictographs, dingbats, and decorative Unicode symbols.
    Allows standard ASCII printable chars, newlines/tabs, and Tamil Unicode block (U+0B80..U+0BFF).
    """
    cleaned: list[str] = []
    for ch in text:
        cp = ord(ch)
        if (
            ch in ("\n", "\t")
            or (0x20 <= cp <= 0x7E)
            or (0x0B80 <= cp <= 0x0BFF)
            or cp in (0x200C, 0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D)
        ):
            cleaned.append(ch)
    return "".join(cleaned)


def has_forbidden_unicode(text: str) -> list[tuple[str, str]]:
    """Return any character outside clean ASCII + Tamil + standard punctuation."""
    bad: list[tuple[str, str]] = []
    for ch in text:
        cp = ord(ch)
        allowed = (
            ch in ("\n", "\t")
            or (0x20 <= cp <= 0x7E)
            or (0x0B80 <= cp <= 0x0BFF)
            or cp in (0x200C, 0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D)
        )
        if not allowed:
            bad.append((ch, hex(cp)))
    return bad


def load_women_lifestyle_dataset(json_path: Path = DATA_JSON_PATH) -> dict[str, dict[str, Any]]:
    """Load and cache the 54-day women's lifestyle JSON dataset."""
    global _LIFESTYLE_CACHE
    if _LIFESTYLE_CACHE is None or json_path != DATA_JSON_PATH:
        if not json_path.exists():
            raise FileNotFoundError(f"Missing women lifestyle dataset: {json_path}")
        data = json.loads(json_path.read_text(encoding="utf-8"))
        if json_path == DATA_JSON_PATH:
            _LIFESTYLE_CACHE = data
        return data
    return _LIFESTYLE_CACHE


def format_cat3_date_header(date_str: str, entry: dict[str, Any], tamil_date_header: str | None = None) -> str:
    """
    Normalize `tamil_date_header` into `<DD நவம்பர்/டிசம்பர் 2026> (<தமிழ் மாதம்> <நாள்>, <கிழமை>)`.
    Supports:
      - `None` or `""` -> uses canonical `entry["tamil_date_header"]`
      - Full header already containing Gregorian + parenthesized Tamil date -> returned cleanly
      - Inner Tamil calendar string like `ஐப்பசி 22, ஞாயிற்றுக்கிழமை` -> wrapped with Gregorian date
      - Header with `| ` prefix -> strips leading prefix cleanly
    """
    dt = date.fromisoformat(date_str)
    greg_ta = entry.get("gregorian_date_ta") or f"{dt.day:02d} {GREGORIAN_MONTHS_TA[dt.month]} {dt.year}"
    tamil_cal_ta = entry.get("tamil_calendar_ta") or f"{entry['tamil_month']} {entry['tamil_day']}, {entry['weekday_ta']}"
    canonical = f"{greg_ta} ({tamil_cal_ta})"

    if not tamil_date_header or not tamil_date_header.strip():
        return canonical

    hdr = strip_decorative_unicode(tamil_date_header).strip()
    if "|" in hdr:
        hdr = hdr.split("|")[-1].strip()

    if str(dt.year) in hdr and "(" in hdr and ")" in hdr:
        return hdr

    if hdr.startswith("(") and hdr.endswith(")"):
        return f"{greg_ta} {hdr}"

    if str(dt.year) not in hdr:
        return f"{greg_ta} ({hdr})"

    return hdr


def build_cat3_women_lifestyle_post(date_str: str, tamil_date_header: str | None = None) -> str:
    """
    Build Category 3 (`இல்லறம், சமையல் & மகளிர் நலக் குறிப்புகள்`) Community Post for `@TamilDailyLife`.

    Structure:
      - Title: `இல்லறம், சமையல் & மகளிர் நல வழிகாட்டி | <DD நவம்பர்/டிசம்பர் 2026> (<தமிழ் மாதம்> <நாள்>, <கிழமை>)`
      - `சமையலறைக் குறிப்புகள் (சுவையும் நேரச் சேமிப்பும்):` (3 `- ` bullets)
      - `மகளிர் ஆரோக்கியம் & இயற்கை பராமரிப்பு:` (2 `- ` bullets)
      - `குடும்ப நலம், சேமிப்பு & இல்லற மேன்மை:` (2 `- ` bullets)
      - Closing 1-line warm blessing + `வாழ்க வளமுடன். சிவாயநம.`
    """
    dataset = load_women_lifestyle_dataset()
    if date_str not in dataset:
        raise KeyError(
            f"Date {date_str} not found in {DATA_JSON_PATH}. "
            f"Supported range: {START_DATE.isoformat()} to {END_DATE.isoformat()}."
        )

    entry = dataset[date_str]
    header_ta = format_cat3_date_header(date_str, entry, tamil_date_header)

    kitchen_tips = entry["kitchen_tips"]
    wellness_tips = entry["wellness_tips"]
    family_tips = entry["family_harmony_tips"]
    blessing_ta = entry["blessing_ta"].strip()

    assert len(kitchen_tips) == 3, f"Expected 3 kitchen tips on {date_str}, got {len(kitchen_tips)}"
    assert len(wellness_tips) == 2, f"Expected 2 wellness tips on {date_str}, got {len(wellness_tips)}"
    assert len(family_tips) == 2, f"Expected 2 family harmony tips on {date_str}, got {len(family_tips)}"

    lines = [
        f"இல்லறம், சமையல் & மகளிர் நல வழிகாட்டி | {header_ta}",
        "",
        "சமையலறைக் குறிப்புகள் (சுவையும் நேரச் சேமிப்பும்):",
        f"- {kitchen_tips[0]}",
        f"- {kitchen_tips[1]}",
        f"- {kitchen_tips[2]}",
        "",
        "மகளிர் ஆரோக்கியம் & இயற்கை பராமரிப்பு:",
        f"- {wellness_tips[0]}",
        f"- {wellness_tips[1]}",
        "",
        "குடும்ப நலம், சேமிப்பு & இல்லற மேன்மை:",
        f"- {family_tips[0]}",
        f"- {family_tips[1]}",
        "",
        blessing_ta,
        "வாழ்க வளமுடன். சிவாயநம.",
    ]

    raw_post = "\n".join(lines).strip()
    bad = has_forbidden_unicode(raw_post)
    assert not bad, f"Forbidden decorative/emoji Unicode found on {date_str}: {bad}"

    post = strip_decorative_unicode(raw_post).strip()
    assert len(post) < 3200, f"Cat 3 post exceeded 3,200 chars ({len(post)}) on {date_str}"
    return post


def verify_all_54_days(
    verbose_samples: tuple[str, ...] = ("2026-11-08", "2026-12-16"),
) -> dict[str, Any]:
    """
    Verify across all 54 dates (`2026-11-08` through `2026-12-31`) that:
      1. All 54 dates exist in `tdl_women_54days_lifestyle.json` and align with `STORY_METADATA.json`.
      2. 100% uniqueness across all 162 kitchen tips, 108 wellness tips, 108 family tips,
         all 378 combined bullet points, and all 54 closing blessings (zero duplicates).
      3. Zero emojis or non-standard decorative Unicode characters exist anywhere.
      4. Every rendered post is strictly `< 3,200` characters and follows the exact Tamil format.
    """
    dataset = load_women_lifestyle_dataset()

    expected_dates = [
        (START_DATE + timedelta(days=i)).isoformat()
        for i in range((END_DATE - START_DATE).days + 1)
    ]
    assert len(expected_dates) == 54, f"Expected 54 dates, computed {len(expected_dates)}"
    assert set(dataset.keys()) == set(expected_dates), (
        f"Dataset dates mismatch! Missing={set(expected_dates) - set(dataset.keys())}, "
        f"Extra={set(dataset.keys()) - set(expected_dates)}"
    )

    all_kitchen: list[str] = []
    all_wellness: list[str] = []
    all_family: list[str] = []
    all_blessings: list[str] = []
    rendered_posts: dict[str, str] = {}

    for ds in expected_dates:
        entry = dataset[ds]
        meta_path = ASSETS_BASE / ds / "STORY_METADATA.json"
        assert meta_path.exists(), f"Missing STORY_METADATA.json for {ds}: {meta_path}"
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        assert entry["story_title_ta"] == meta["title_ta"], (
            f"Story title mismatch on {ds}: {entry['story_title_ta']} != {meta['title_ta']}"
        )

        kt = [t.strip() for t in entry["kitchen_tips"]]
        wt = [t.strip() for t in entry["wellness_tips"]]
        ft = [t.strip() for t in entry["family_harmony_tips"]]
        bl = entry["blessing_ta"].strip()

        assert len(kt) == 3 and all(kt), f"Invalid kitchen_tips on {ds}"
        assert len(wt) == 2 and all(wt), f"Invalid wellness_tips on {ds}"
        assert len(ft) == 2 and all(ft), f"Invalid family_harmony_tips on {ds}"
        assert bl, f"Empty blessing_ta on {ds}"

        all_kitchen.extend(kt)
        all_wellness.extend(wt)
        all_family.extend(ft)
        all_blessings.append(bl)

        post_default = build_cat3_women_lifestyle_post(ds)
        post_explicit_hdr = build_cat3_women_lifestyle_post(ds, entry["tamil_date_header"])
        post_inner_hdr = build_cat3_women_lifestyle_post(
            ds, f"{entry['tamil_month']} {entry['tamil_day']}, {entry['weekday_ta']}"
        )
        assert post_default == post_explicit_hdr == post_inner_hdr, (
            f"Header normalization mismatch on {ds}"
        )

        # Verify zero emojis / decorative Unicode & strict structure
        assert not has_forbidden_unicode(post_default), f"Forbidden Unicode in rendered post for {ds}"
        assert post_default == strip_decorative_unicode(post_default), f"Strip mismatch on {ds}"
        assert post_default.startswith("இல்லறம், சமையல் & மகளிர் நல வழிகாட்டி | "), f"Bad title on {ds}"
        assert "சமையலறைக் குறிப்புகள் (சுவையும் நேரச் சேமிப்பும்):" in post_default
        assert "மகளிர் ஆரோக்கியம் & இயற்கை பராமரிப்பு:" in post_default
        assert "குடும்ப நலம், சேமிப்பு & இல்லற மேன்மை:" in post_default
        assert post_default.endswith("வாழ்க வளமுடன். சிவாயநம."), f"Bad closing sign-off on {ds}"
        assert post_default.count("\n- ") == 7, f"Expected exactly 7 '- ' bullets on {ds}"
        assert len(post_default) < 3200, f"Post too long ({len(post_default)} chars) on {ds}"

        rendered_posts[ds] = post_default

    # 100% Uniqueness assertions across the entire 54-day corpus
    assert len(all_kitchen) == 162 and len(set(all_kitchen)) == 162, (
        f"Duplicate kitchen tips found: {len(all_kitchen)} total vs {len(set(all_kitchen))} unique"
    )
    assert len(all_wellness) == 108 and len(set(all_wellness)) == 108, (
        f"Duplicate wellness tips found: {len(all_wellness)} total vs {len(set(all_wellness))} unique"
    )
    assert len(all_family) == 108 and len(set(all_family)) == 108, (
        f"Duplicate family tips found: {len(all_family)} total vs {len(set(all_family))} unique"
    )
    combined_bullets = all_kitchen + all_wellness + all_family
    assert len(combined_bullets) == 378 and len(set(combined_bullets)) == 378, (
        f"Cross-category duplicate bullets found: {len(combined_bullets)} total vs {len(set(combined_bullets))} unique"
    )
    assert len(all_blessings) == 54 and len(set(all_blessings)) == 54, (
        f"Duplicate blessings found: {len(all_blessings)} total vs {len(set(all_blessings))} unique"
    )

    lengths = [len(p) for p in rendered_posts.values()]
    stats = {
        "total_days": len(expected_dates),
        "date_range": f"{START_DATE.isoformat()} to {END_DATE.isoformat()}",
        "unique_kitchen_tips": len(set(all_kitchen)),
        "unique_wellness_tips": len(set(all_wellness)),
        "unique_family_harmony_tips": len(set(all_family)),
        "total_unique_bullets": len(set(combined_bullets)),
        "unique_closing_blessings": len(set(all_blessings)),
        "min_post_chars": min(lengths),
        "max_post_chars": max(lengths),
        "avg_post_chars": round(sum(lengths) / len(lengths), 1),
        "forbidden_unicode_count": 0,
    }

    for sample_ds in verbose_samples:
        if sample_ds in rendered_posts:
            p = rendered_posts[sample_ds]
            print("=" * 92)
            print(f"SAMPLE DATE: {sample_ds} | CATEGORY 3 ({len(p)} chars)")
            print("=" * 92)
            print(p)
            print()

    print("=" * 92)
    print(f"VERIFICATION PASSED: {json.dumps(stats, ensure_ascii=False)}")
    print("=" * 92)
    return stats


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

    parser = argparse.ArgumentParser(
        description="Build & verify @TamilDailyLife Category 3 Women's Lifestyle, Kitchen & Family Harmony Posts"
    )
    parser.add_argument(
        "--date",
        default="",
        help="Single YYYY-MM-DD date (2026-11-08..2026-12-31) to render; omit to run full 54-day verification",
    )
    parser.add_argument(
        "--tamil-date-header",
        default="",
        help="Optional custom Tamil date header override",
    )
    args = parser.parse_args()

    if args.date:
        print(build_cat3_women_lifestyle_post(args.date, args.tamil_date_header or None))
    else:
        verify_all_54_days()


if __name__ == "__main__":
    main()
