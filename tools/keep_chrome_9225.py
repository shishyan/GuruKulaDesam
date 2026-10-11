import subprocess, time, urllib.request, pathlib, sys

profile_dir = pathlib.Path.home() / '.antigravity_shishyan'
profile_dir.mkdir(parents=True, exist_ok=True)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
args = [
    chrome_path,
    "--remote-debugging-port=9225",
    f"--user-data-dir={profile_dir}",
    "--remote-allow-origins=*",
    "--no-first-run",
    "--no-default-browser-check",
    "https://studio.youtube.com"
]

while True:
    print("Launching Chrome on port 9225...", flush=True)
    proc = subprocess.Popen(args)
    print(f"Chrome started with PID {proc.pid}. Keeping alive...", flush=True)

    while True:
        time.sleep(2)
        if proc.poll() is not None:
            print(f"Chrome process {proc.pid} exited with code {proc.returncode}! Restarting in 3s...", flush=True)
            time.sleep(3)
            break
