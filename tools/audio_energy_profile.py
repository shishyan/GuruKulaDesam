import soundfile as sf
import numpy as np

# Load 6r6TpY-sgbw.wav
data, sr = sf.read('scratch/6r6TpY-sgbw.wav')
duration = len(data) / sr
print(f"Total duration: {duration:.2f}s, sample rate: {sr}")

# Let's inspect energy profile across 5-second intervals to detect vocal boundaries
hop = int(0.5 * sr)
frame_len = int(1.0 * sr)
rms = []
for i in range(0, len(data) - frame_len, hop):
    frame = data[i:i+frame_len]
    rms.append((i/sr, float(np.sqrt(np.mean(frame**2)))))

print("Sample RMS values:")
for t, val in rms[::20][:15]:
    print(f"  {t:5.1f}s: {val:.4f}")
