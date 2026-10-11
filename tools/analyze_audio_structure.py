import soundfile as sf
import numpy as np
import json, sys

sys.stdout.reconfigure(encoding='utf-8')

# Read wav file
data, samplerate = sf.read('scratch/Mata6vtnrjQ.wav')
if len(data.shape) > 1:
    data = data.mean(axis=1) # convert to mono

duration = len(data) / samplerate
print(f"Sample rate: {samplerate}, Samples: {len(data)}, Duration: {duration:.2f}s ({duration/60:.2f} mins)")

# Let's compute RMS energy in 0.5s windows
window_size = int(0.5 * samplerate)
hop_size = int(0.25 * samplerate)

rms = []
times = []
for i in range(0, len(data) - window_size, hop_size):
    chunk = data[i:i+window_size]
    r = np.sqrt(np.mean(chunk**2))
    rms.append(r)
    times.append(i / samplerate)

rms = np.array(rms)
max_rms = np.max(rms)
print(f"Max RMS: {max_rms:.4f}, Mean RMS: {np.mean(rms):.4f}")

# Let's detect silent vs active regions
# What happens in the first 30 seconds? Intro music?
for sec in range(0, int(duration), 10):
    chunk = data[sec*samplerate : min((sec+10)*samplerate, len(data))]
    r = np.sqrt(np.mean(chunk**2))
    print(f"Time {sec:3d}s - {sec+10:3d}s: RMS = {r:.4f}")
