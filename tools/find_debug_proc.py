import subprocess

ps = """Get-CimInstance Win32_Process -Filter "Name = 'chrome.exe'" | Select-Object ProcessId, CommandLine"""
res = subprocess.run(["powershell", "-Command", ps], capture_output=True, text=True)
for l in res.stdout.splitlines():
    if '--remote-debugging-port' in l:
        print(l)
