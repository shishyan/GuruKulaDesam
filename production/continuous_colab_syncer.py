#!/usr/bin/env python3
# Continuous automated watcher to sync new images between Google Drive and Colab handoff
import subprocess, time, sys

print('Starting continuous Drive <-> Colab 31-scene sync daemon...')
while True:
    try:
        # Sync scene_images to colab_handoff
        cmd = [
            'rclone', 'sync',
            '/home/nagaraj957/GuruKulaDesam/production/scene_images',
            'gdrive:colab_handoff/scene_images',
            '--drive-root-folder-id', '1mXREJzspQdtqgAzwn1YtVLZoc8TpIOFp',
            '--create-empty-src-dirs',
            '--transfers', '8',
            '--checkers', '16',
            '-q'
        ]
        subprocess.run(cmd)
        print('[Daemon] Synced all track directories to Drive colab_handoff')
    except Exception as e:
        print('[Daemon Error]:', e)
    time.sleep(60)
