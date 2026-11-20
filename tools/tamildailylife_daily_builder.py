"""Daily @TamilDailyLife Panchangam script + lyrical-style 1080p video builder."""
import argparse
import datetime
import os
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default="", help="YYYY-MM-DD (defaults to today IST)")
    args = parser.parse_args()

    if args.date:
        dt = datetime.date.fromisoformat(args.date)
    else:
        dt = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).date()

    out_dir = Path("out")
    out_dir.mkdir(parents=True, exist_ok=True)
    date_str = dt.isoformat()

    script_path = out_dir / f"tamildailylife_{date_str}.md"
    audio_path = out_dir / f"tamildailylife_{date_str}.mp3"

    # Weekday-matched temple / deity guidance ("WHERE to go")
    weekday_temples = {
        0: ("திங்கட்கிழமை", "சிவன் கோயில் / அம்மன் சந்நிதி"),
        1: ("செவ்வாய்க்கிழமை", "முருகன் கோயில் / துர்க்கை அம்மன் சந்நிதி"),
        2: ("புதன்கிழமை", "பெருமாள் கோயில் / விநாயகர் சந்நிதி"),
        3: ("வியாழக்கிழமை", "தக்ஷிணாமூர்த்தி / குரு பகவான் சந்நிதி"),
        4: ("வெள்ளிக்கிழமை", "அம்மன் கோயில் / மகாலட்சுமி சந்நிதி"),
        5: ("சனிக்கிழமை", "பெருமாள் / ஆஞ்சநேயர் / சனீஸ்வர பகவான் சந்நிதி"),
        6: ("ஞாயிற்றுக்கிழமை", "சூரிய பகவான் / சிவன் கோயில்"),
    }
    day_ta, temple_ta = weekday_temples[dt.weekday()]

    script_text = (
        f"சிவாயநம! அன்பான சகோதர, சகோதரிகளே! எல்லாரும் எப்படி இருக்கீங்க?\n\n"
        f"இன்னைக்கு {date_str}, {day_ta}. "
        f"இன்னைக்கு வீட்டுல விளக்கேத்தி, எளிய சாத்வீக உணவோட நாளைத் தொடங்குங்க. "
        f"நேரம் கிடைச்சா பக்கத்துல இருக்குற {temple_ta}-க்குப் போயிட்டு வாங்க; மனசுக்கு ரொம்ப நிறைவா இருக்கும்.\n\n"
        f"நாளைக்கு அடுத்த நாளோட கதையோட திரும்பவும் உங்களைப் பார்க்கிறேன்! சிவாயநம!"
    )
    script_path.write_text(script_text, encoding="utf-8")

    subprocess.run(
        [
            "edge-tts",
            "--voice",
            "ta-IN-PallaviNeural",
            "--rate=-12%",
            "--text",
            script_text.replace("\n", " "),
            "--write-media",
            str(audio_path),
        ],
        check=True,
    )
    print(f"Generated {script_path} and {audio_path}")


if __name__ == "__main__":
    main()
