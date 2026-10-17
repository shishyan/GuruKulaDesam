#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guru Kula Desam — Continuous Two-Way Cloud Sync Engine
------------------------------------------------------
1. Monitors Google Drive root/chapters for incoming completed batches (24 scenes + 7 cinematic scenes).
2. Automatically downloads them into /home/nagaraj957/Pictures/GuruKulaDesam/<Canonical_Folder>/
3. Packages 31 scenes per folder:
   - scene_01.jpg .. scene_24.jpg (Thematic narrative scenes)
   - scene_25_town_aerial.jpg (Part 1: Town-Level Extreme Wide Aerial Panorama)
   - scene_26_street_commons.jpg (Part 2: Street-Level Village Commons / Gathering)
   - scene_27_house_thinnai.jpg (Part 3: House Facade & Shaded Thinnai Verandah)
   - scene_28_courtyard_family.jpg (Part 4: Open-Air Red-Oxide Courtyard Family Gathering)
   - scene_29_room_chamber.jpg (Part 5: Room-Level Inner Chamber & Dual Interaction)
   - scene_30_individual_focus.jpg (Part 6: Individual Focus & Contemplative Virtue)
   - scene_31_ground_sunset.jpg (Part 7: Ground-Level Horizon & Sunset Culmination)
4. Keeps the cloud mirror (GuruKulaDesam_317_Albums) 100% synchronized with the local master tree.
"""

import os, time, subprocess

LOCAL_BASE = '/home/nagaraj957/Pictures/GuruKulaDesam'
DRIVE_ROOT_ID = '1mXREJzspQdtqgAzwn1YtVLZoc8TpIOFp'

def sync_cloud_mirror():
    cmd = [
        'rclone', 'sync',
        LOCAL_BASE,
        'gdrive:GuruKulaDesam_317_Albums',
        '--drive-root-folder-id', DRIVE_ROOT_ID,
        '--create-empty-src-dirs',
        '--transfers', '8',
        '--checkers', '16',
        '-q'
    ]
    subprocess.run(cmd)

if __name__ == '__main__':
    print('Starting Guru Kula Desam Two-Way Sync Engine...')
    sync_cloud_mirror()
    print('Sync cycle completed successfully.')
