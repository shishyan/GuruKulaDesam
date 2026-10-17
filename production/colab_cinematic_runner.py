# Guru Kula Desam — Google Colab Cinematic Video Generator
# Mounts Google Drive, accesses 31-scene albums, and renders live video motion

from google.colab import drive
import os, glob, subprocess

drive.mount('/content/drive')

DRIVE_SCENES = '/content/drive/MyDrive/1mXREJzspQdtqgAzwn1YtVLZoc8TpIOFp/colab_handoff/scene_images'
OUTPUT_VIDEOS = '/content/drive/MyDrive/1mXREJzspQdtqgAzwn1YtVLZoc8TpIOFp/colab_handoff/rendered_videos'
os.makedirs(OUTPUT_VIDEOS, exist_ok=True)

print(f'Ready! Scanning albums in {DRIVE_SCENES}...')
