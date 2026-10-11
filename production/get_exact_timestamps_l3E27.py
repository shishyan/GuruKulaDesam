import sys
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "production"))

from google_flow_engine import get_genai_client

audio_path = ROOT / "source" / "youtube" / "l3E27q5r-nk.m4a"
client = get_genai_client()

print("Uploading l3E27q5r-nk.m4a to Gemini...")
audio_file = client.files.upload(file=str(audio_path))

prompt = """Listen to this Tamil devotional song.
The lyrics sung are:
அம்பலத்துள் நின்று ஆடல் வல்லானே
தும்பை வன்னியன் சடை முடியவனே
செம்பொன்னே செழும் பவள மாமலையே
திகழும் ஒற்றியூர் சிவபெருமானே

Listen carefully to the vocals.
For each couplet or line sung from the very first vocal entry (around 00:33) until the end of the song:
Identify the EXACT start time (in seconds, e.g. 33.2) and end time (in seconds, e.g. 42.0) when that line is sung.
Group them into 2-line couplets.

Return ONLY a valid JSON list of objects:
[
  {
    "start_sec": 33.0,
    "end_sec": 44.5,
    "tamil_text": "அம்பலத்துள் நின்று ஆடல் வல்லானே\\nதும்பை வன்னியன் சடை முடியவனே"
  }
]
"""

print("Querying Gemini 3.8 Flash for exact timestamps...")
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[audio_file, prompt]
)

print("\n--- TIMESTAMPS ---")
print(response.text)

m = re.search(r"\[.*\]", response.text, re.DOTALL)
if m:
    data = json.loads(m.group(0))
    out_file = ROOT / "production" / "exact_timed_lyrics_l3E27q5r-nk.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(data)} perfectly timed cards to {out_file}")
