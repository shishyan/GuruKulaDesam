import subprocess

ps = """Get-Process | Where-Object { $_.MainWindowTitle -ne '' } | Select-Object ProcessName, Id, MainWindowTitle"""
res = subprocess.run(["powershell", "-Command", ps], capture_output=True, text=True)
for l in res.stdout.splitlines():
    if any(k in l.lower() for k in ['chrome', 'edge', 'flow', 'google', 'brave', 'firefox']):
        print(l)
