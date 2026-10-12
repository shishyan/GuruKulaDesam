import subprocess

ps = """
Get-CimInstance Win32_Process -Filter "Name = 'msedge.exe'" | Select-Object ProcessId, CommandLine
"""
res = subprocess.run(["powershell", "-Command", ps], capture_output=True, text=True)
lines = [l.strip() for l in res.stdout.splitlines() if l.strip()]
roots = [l for l in lines if '--type=' not in l and 'msedge.exe' in l]
print(f"Total Edge Root Processes: {len(roots)}")
for r in roots:
    print(r)
