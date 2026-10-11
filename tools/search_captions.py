import sys, json, os, pathlib
ROOT = pathlib.Path('.')
for path in ROOT.glob('**/*'):
    if path.suffix in ['.srt', '.vtt', '.sbv']:
        print('Found subtitle file:', path)
    elif 'caption' in path.name.lower() or 'subtitle' in path.name.lower():
        print('Found caption tool/file:', path)
