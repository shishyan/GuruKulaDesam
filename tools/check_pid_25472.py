import subprocess

ps = """Get-CimInstance Win32_Process -Filter "ProcessId = 25472" | Select-Object -ExpandProperty CommandLine"""
res = subprocess.run(["powershell", "-Command", ps], capture_output=True, text=True)
print("PID 25472 Full CommandLine:")
print(repr(res.stdout))
