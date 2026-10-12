import subprocess

ps = """Get-CimInstance Win32_Process -Filter "ProcessId = 23724" | Select-Object -ExpandProperty CommandLine"""
res = subprocess.run(["powershell", "-Command", ps], capture_output=True, text=True)
print("PID 23724 CommandLine:")
print(res.stdout.strip())
