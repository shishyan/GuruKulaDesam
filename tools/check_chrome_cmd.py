import subprocess

out = subprocess.check_output(['wmic', 'process', 'where', 'name="chrome.exe"', 'get', 'commandline'], text=True)
for l in out.splitlines():
    if '--remote-debugging-port' in l:
        print("Found debug Chrome:")
        print(l)
        break
else:
    print("No --remote-debugging-port Chrome found.")
