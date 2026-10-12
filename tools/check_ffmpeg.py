import subprocess

res = subprocess.run(
    ["powershell", "-Command", "Get-CimInstance Win32_Process -Filter 'ProcessId = 32432' | Select-Object -ExpandProperty CommandLine"],
    capture_output=True, text=True, errors="replace"
)
print("COMMAND LINE:")
print(res.stdout)
