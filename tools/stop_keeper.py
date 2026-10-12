import subprocess

ps = """
Stop-Process -Id 21872 -Force -ErrorAction SilentlyContinue
Get-CimInstance Win32_Process -Filter "Name = 'chrome.exe'" | Where-Object { $_.CommandLine -like "*9225*" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
"""
subprocess.run(["powershell", "-Command", ps], capture_output=True)
print("Stopped keep_chrome_9225 daemon and its Chrome child processes.")
