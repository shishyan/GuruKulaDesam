import subprocess

ps = """Get-Process | Where-Object { $_.MainWindowTitle } | Select-Object Id, ProcessName, MainWindowTitle"""
res = subprocess.run(["powershell", "-Command", ps], capture_output=True, text=True)
for line in res.stdout.splitlines():
    if line.strip():
        print(line)
