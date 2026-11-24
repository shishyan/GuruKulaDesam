#!/usr/bin/env python3
"""
Generate all 1330 Thirukkural verses as 133 Adhikaram posts (10 kurals per post),
categorized by Paal (பால்) -> Iyal (இயல்) -> Adhikaram (அதிகாரம்) for easy searching.
"""
import json
import re
from pathlib import Path

MASTER_JSON = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Tools/thirukkural_master.json")
CATALOG_JSON = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/thirukkural-133-posts/THIRUKKURAL_133_STORIES_MASTER_CATALOG.json")
OUT_ROOT = Path("/home/shishyan/GoogleDrive_GuruKulaDesam/Assets/thirukkural-1330-categorized")


def sanitize_name(name: str) -> str:
    return re.sub(r"[^\w\u0B80-\u0BFF-]+", "_", name.strip()).strip("_")


def main() -> None:
    master_data = json.loads(MASTER_JSON.read_text(encoding="utf-8"))
    kurals = {int(k["Number"]): k for k in master_data["kural"]}
    if len(kurals) != 1330:
        raise RuntimeError(f"Expected 1330 kurals, found {len(kurals)}")

    catalog = {int(c["ch"]): c for c in json.loads(CATALOG_JSON.read_text(encoding="utf-8"))}
    if len(catalog) != 133:
        raise RuntimeError(f"Expected 133 chapters, found {len(catalog)}")

    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    paal_order: dict[str, int] = {}
    iyal_order: dict[str, int] = {}
    index_entries: list[dict] = []

    for ch in range(1, 134):
        meta = catalog[ch]
        paal = meta["paal"].strip()
        iyal = meta["iyal"].strip()
        ch_name = meta["chName"].strip()

        if paal not in paal_order:
            paal_order[paal] = len(paal_order) + 1
        if iyal not in iyal_order:
            iyal_order[iyal] = len(iyal_order) + 1

        paal_dir = f"{paal_order[paal]:02d}_{sanitize_name(paal)}"
        iyal_dir = f"{iyal_order[iyal]:02d}_{sanitize_name(iyal)}"
        target_dir = OUT_ROOT / paal_dir / iyal_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        start_k = (ch - 1) * 10 + 1
        end_k = ch * 10
        filename = f"ch_{ch:03d}_{sanitize_name(ch_name)}_kurals_{start_k:04d}-{end_k:04d}.txt"
        out_path = target_dir / filename

        lines = [
            f"திருக்குறள் | {paal} | {iyal} | அதிகாரம் {ch}: {ch_name} (குறள் {start_k}–{end_k})",
            "",
        ]
        for num in range(start_k, end_k + 1):
            k = kurals[num]
            lines.append(f"குறள் {num}:")
            lines.append(k["Line1"].strip())
            lines.append(k["Line2"].strip())
            lines.append("")

        out_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

        index_entries.append({
            "ch": ch,
            "chName": ch_name,
            "paal": paal,
            "iyal": iyal,
            "kural_start": start_k,
            "kural_end": end_k,
            "rel_path": str(out_path.relative_to(OUT_ROOT)),
        })

    (OUT_ROOT / "THIRUKKURAL_1330_INDEX.json").write_text(
        json.dumps(index_entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    md_lines = [
        "# திருக்குறள் 1330 குறள்கள் — 133 அதிகாரப் பதிவுகள் (வகைப்படுத்தப்பட்ட அட்டவணை)",
        "",
        "| அதிகாரம் | பால் | இயல் | அதிகாரப் பெயர் | குறள் எண்கள் | கோப்பு |",
        "|---:|---|---|---|---:|---|",
    ]
    for e in index_entries:
        md_lines.append(
            f"| {e['ch']} | {e['paal']} | {e['iyal']} | {e['chName']} | {e['kural_start']}–{e['kural_end']} | `{e['rel_path']}` |"
        )
    (OUT_ROOT / "THIRUKKURAL_1330_INDEX.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"Generated {len(index_entries)} Adhikaram posts (1330 kurals) in {OUT_ROOT}")


if __name__ == "__main__":
    main()
