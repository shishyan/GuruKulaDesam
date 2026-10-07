# -*- coding: utf-8 -*-
"""
Synchronizes higher-studies.html across root, site/, and docs/.
"""

import shutil
import os

def main():
    root_src = 'higher-studies.html'
    if not os.path.exists(root_src):
        print(f"Error: {root_src} not found.")
        return

    targets = ['site/higher-studies.html', 'docs/higher-studies.html']
    for t in targets:
        os.makedirs(os.path.dirname(t), exist_ok=True)
        shutil.copy2(root_src, t)
        print(f"Synchronized {root_src} -> {t}")

if __name__ == '__main__':
    main()

