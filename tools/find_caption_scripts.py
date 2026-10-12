import sys, json, os, pathlib
ROOT = pathlib.Path('.')
for path in ROOT.glob('**/*caption*'):
    print(path)
