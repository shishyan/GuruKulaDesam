import sys
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "production"))

from google_flow_engine import get_genai_client

audio_path = ROOT / "source" / "youtube" / "02C8glMmetw.m4a"
with open(ROOT / "production" / "metadata" / "all_songs_lyrics_and_meanings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

kurals = db["02C8glMmetw"]["tamil_lyrics"]

client = get_genai_client()
print("Uploading audio to Gemini API...")
audio_file = client.files.upload(file=str(audio_path))
print(f"File uploaded: {audio_file.name}")

prompt = f"""This audio file is exactly 238.5 seconds long.
It is a devotional Tamil song singing verses from Thirukkural Chapter 1 (கடவுள் வாழ்த்து).

Here is the canonical list of Kurals in Chapter 1:
{kurals}

Listen carefully to the vocals from second 0.0 to 238.5.
Identify the exact timestamps (start_sec and end_sec in floating point seconds) when each Kural or verse is sung.
Do not hallucinate times beyond 238.5 seconds.
Include the intro duration (music only before singing begins) and any instrumental breaks.

Return ONLY a JSON list of objects in this exact structure:
[
  {{
    "kural_num": 1,
    "start_sec": 27.5,
    "end_sec": 48.0,
    "tamil_text": "அகர முதல எழுத்தெல்லாம் ஆதி\\nபகவன் முதற்றே உலகு"
  }}
]
"""

print("Querying Gemini 3.8 Flash...")
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[audio_file, prompt]
)

print("\n--- RESPONSE ---")
print(response.text)

m = re.search(r"\[.*\]", response.text, re.DOTALL)
if m:
    data = json.loads(m.group(0))
    out_file = ROOT / "production" / "aligned_lyrics_02C8glMmetw.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nSuccessfully saved {len(data)} aligned Kurals to {out_file}")
