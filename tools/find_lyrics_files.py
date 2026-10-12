import sys
import os
import glob

sys.stdout.reconfigure(encoding='utf-8')

print("Root files:")
for f in os.listdir('.'):
    if f.endswith(('.json', '.md', '.txt')):
        print(" ", f)

print("\nProduction files:")
for f in os.listdir('production'):
    if f.endswith(('.json', '.md', '.txt')):
        print(" ", f)
