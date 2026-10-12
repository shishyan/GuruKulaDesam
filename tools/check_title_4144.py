import subprocess

ps = """Get-Process -Id 4144 | Select-Object -ExpandProperty MainWindowTitle"""
res = subprocess.run(["powershell", "-Command", ps], capture_output=True, text=True)
print("PID 4144 Title:", repr(res.stdout.strip()))
