import subprocess

ps = """
Get-CimInstance Win32_Process -Filter "Name = 'chrome.exe'" | Where-Object { $_.CommandLine -like "*9225*" } | Select-Object -ExpandProperty CommandLine
"""
res = subprocess.run(["powershell", "-Command", ps], capture_output=True, text=True)
print("CDP Chrome commandline:")
print(res.stdout.strip())
