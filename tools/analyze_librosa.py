import librosa
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load audio
y, sr = librosa.load('scratch/Mata6vtnrjQ.wav', sr=22050)
duration = librosa.get_duration(y=y, sr=sr)
print(f"Loaded audio: {duration:.2f}s")

# Let's detect onset envelope and spectral novelty to see where distinct stanzas start/end
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
print(f"Estimated tempo: {tempo:.1f} BPM")

# Let's check energy profile every 1 second
rms = librosa.feature.rms(y=y)[0]
rms_times = librosa.times_like(rms, sr=sr)

# Find where the audio starts having significant energy (after silence or intro)
# And let's check vocal vs non-vocal: harmonic vs percussive separation
y_harmonic, y_percussive = librosa.effects.hpss(y)
harm_rms = librosa.feature.rms(y=y_harmonic)[0]

# Let's print energy at 5s intervals
print("\nTime (s) | Total RMS | Harm RMS (Vocals/Melody)")
for t in range(0, int(duration), 10):
    idx = int(t * sr / 512)
    idx_end = int((t + 10) * sr / 512)
    tot = np.mean(rms[idx:idx_end]) if idx_end <= len(rms) else 0
    harm = np.mean(harm_rms[idx:idx_end]) if idx_end <= len(harm_rms) else 0
    print(f"{t:3d} - {t+10:3d}s | {tot:.4f}    | {harm:.4f}")
