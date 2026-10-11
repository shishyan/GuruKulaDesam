import time, datetime, subprocess, sys, pathlib
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG_FILE = ROOT / "production" / "auto_sync_runner.log"

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def check_quota():
    cmd = [sys.executable, "tools/check_quota_probe.py"]
    try:
        res = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
        out = res.stdout + res.stderr
        if "QUOTA_OK" in out:
            return True, "Quota is available!"
        if "QUOTA_EXCEEDED" in out or "quotaExceeded" in out or "403" in out:
            return False, "Quota limit active (403 quotaExceeded)"
        return False, f"Waiting... Output: {res.stdout.strip()} {res.stderr.strip()[:100]}"
    except Exception as e:
        return False, f"Exception checking quota: {e}"

def run_sync():
    log("=== QUOTA AVAILABLE! RUNNING MASTER CHANNEL SYNC ===")
    cmd = [sys.executable, "-u", "tools/batch_sync_channel_lyrics_captions.py"]
    try:
        res = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, encoding='utf-8', errors='replace')
        log(f"Batch sync output summary:\n{res.stdout[-400:]}")
        if res.stderr:
            log(f"Stderr: {res.stderr[-200:]}")
    except Exception as e:
        log(f"Error during batch sync execution: {e}")
    log("=== SYNC CYCLE COMPLETED ===")

def main():
    log("Auto-Sync Daemon started. Polling YouTube API quota every 30 minutes...")
    while True:
        available, status = check_quota()
        if available:
            log(f"Status check: {status}. Launching sync...")
            run_sync()
            log("Sync pass finished. Checking next in 30 minutes...")
            time.sleep(1800)
        else:
            log(f"Status check: {status}. Sleeping 30 minutes...")
            time.sleep(1800)

if __name__ == "__main__":
    main()
