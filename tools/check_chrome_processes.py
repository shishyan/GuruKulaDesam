import subprocess

out = subprocess.check_output('wmic process where "name=\'chrome.exe\'" get CommandLine,ProcessId', shell=True).decode('utf-8', errors='ignore')
found = False
for line in out.splitlines():
    if '.antigravity_shishyan' in line or '9225' in line:
        found = True
        print('FOUND:', line)
if not found:
    print('NO existing process found for .antigravity_shishyan or 9225')
