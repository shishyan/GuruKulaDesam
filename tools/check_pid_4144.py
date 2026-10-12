import subprocess

ps = """Get-CimInstance Win32_Process -Filter "ProcessId = 4144" | Select-Object -ExpandProperty CommandLine"""
res = subprocess.run(["powershell", "-Command", ps], capture_output=True, text=True)
print("PID 4144 commandline:")
print(res.stdout.strip())
