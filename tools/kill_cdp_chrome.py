import subprocess
import time

ps_kill = """
Get-CimInstance Win32_Process -Filter "Name = 'chrome.exe'" | Where-Object { $_.CommandLine -like "*9225*" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
"""
subprocess.run(["powershell", "-Command", ps_kill], capture_output=True)
print("Stopped port 9225 isolated Chrome processes.")
time.sleep(2)
