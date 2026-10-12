import subprocess

ps = """Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" | Select-Object ProcessId, CommandLine"""
res = subprocess.run(["powershell", "-Command", ps], capture_output=True, text=True)
for l in res.stdout.splitlines():
    if l.strip():
        print(l)
