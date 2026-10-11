import subprocess, time, urllib.request, pathlib

profile_dir = pathlib.Path.home() / '.antigravity_shishyan'
profile_dir.mkdir(parents=True, exist_ok=True)

cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--remote-debugging-port=9225',
    f'--user-data-dir={profile_dir}',
    '--remote-allow-origins=*',
    '--no-first-run',
    '--no-default-browser-check',
    'https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro'
]

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

proc = subprocess.Popen(
    cmd,
    creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
    close_fds=True
)

print(f"Launched Chrome PID: {proc.pid}")

# Wait up to 10 seconds for port 9225 to be alive
for i in range(10):
    time.sleep(1)
    try:
        data = urllib.request.urlopen('http://127.0.0.1:9225/json/version', timeout=1).read()
        print("Port 9225 is UP and ready!")
        break
    except Exception:
        print(f"Waiting for 9225... ({i+1}/10)")
