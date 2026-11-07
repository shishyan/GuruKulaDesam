import json, os, sys, time
import googleapiclient.discovery
import googleapiclient.http
import google.oauth2.credentials

# Load metadata
meta_file = "/content/drive/MyDrive/Meditative_3Hour_Production/3hour_film_metadata.json"
# Or fallback
video_path = "/content/drive/MyDrive/Meditative_3Hour_Production/Master_3Hour_Meditative_Film_1080p.mp4"

print(f"Checking video file: {video_path}")
if not os.path.exists(video_path):
    print("Video file not found at path!")
    sys.exit(1)

size_gb = os.path.getsize(video_path) / (1024**3)
print(f"Video file ready: {size_gb:.2f} GB")
