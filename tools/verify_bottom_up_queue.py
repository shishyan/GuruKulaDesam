import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# The exact list from bottom up:
bottom_up_files = [
    # 1. Very bottom:
    "திருமுருகாற்றுப்படை - குன்றம் எறிந்தாய் 1H Golden 2026.wav",
    # 2. Earlier this week:
    "பழைமை Clip .wav",
    "பழைமை 1F Golden 2026.wav",
    "பழைமை 1H Golden Pop (1).wav",
    "திருப்பரங்குன்றம் 1N Golden.wav",
    "திருப்பரங்குன்றம் 2B Golden.wav",
    "திருஆவினன்குடி 1G Golden 2026.wav",
    "திருஏரகம் 1H Golden.wav",
    "குன்றுதோறாடல் 1D Golden.wav",
    "பழமுதிர் சோலை 1J Golden.wav",
    "திருச்செந்தூர் 1Q Golden.wav",
    "திருச்செந்தூர் 2E Golden 2026.wav",
    "தோடு உடைய செவியன் 1M Golden.wav",
    "பத்தரோடு 1G Golden.wav",
    "மைம் மரு 1D Golden.wav",
    "செய் அருகே 1J2 Golden 2026.wav",
    # 3. Yesterday:
    "அங்கமும் வேதமும் 1N Golden 2026.wav",
    "அங்கமும் வேதமும் 1N Golden.wav",
    "அங்கமும் வேதமும் 10 Golden 2026.wav",
    "பாடக மெல்லடி 1J Golden.wav",
    # 4. Today:
    "புண்ணியர் பூதியர் 1E2 Golden 2026.wav",
    "புண்ணியர் பூதியர் 1F Golden 2026.wav"
]

downloads = os.path.expanduser('~/Downloads')
print(f"Total files in queue: {len(bottom_up_files)}")
print("=" * 70)

for idx, f in enumerate(bottom_up_files, 1):
    p = os.path.join(downloads, f)
    if os.path.exists(p):
        sz = os.path.getsize(p) / 1024 / 1024
        print(f"{idx:2d}. [EXISTS] {f:50s} ({sz:5.1f} MB)")
    else:
        print(f"{idx:2d}. [MISSING] {f}")
