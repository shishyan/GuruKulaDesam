import subprocess

ps = """Get-CimInstance Win32_Process -Filter "ProcessId = 21992" | Select-Object -ExpandProperty CommandLine"""
res = subprocess.run(["powershell", "-Command", ps], capture_output=True, text=True)
print("PID 21992 Full CommandLine:")
print(repr(res.stdout.strip()))
