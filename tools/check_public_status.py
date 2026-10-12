import subprocess, json, sys
sys.stdout.reconfigure(encoding='utf-8')

remaining = ['HPP3IG7DWRc', 'cKyT1Cv7zEA', 'ETELjf0OTi4']
for vid in remaining:
    cmd = ['python', '-m', 'yt_dlp', '--dump-json', f'https://www.youtube.com/watch?v={vid}']
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        info = json.loads(res.stdout)
        print(f"{vid}: PUBLIC! title='{info.get('title')}' duration={info.get('duration')}s")
    else:
        err = res.stderr.strip()
        last_line = err.splitlines()[-1] if err else "unknown"
        print(f"{vid}: NOT PUBLIC ({last_line})")
