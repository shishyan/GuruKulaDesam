# Quota resilience & queue watcher
import time, datetime

def handle_quota_limit(err_msg):
    print(f"⚠️ Quota limit detected: {err_msg}")
    print("Scheduling retry when YouTube daily quota resets (midnight Pacific Time)...")
