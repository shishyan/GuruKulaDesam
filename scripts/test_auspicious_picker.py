import re
import random
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/home/shishyan/GitHub/Shishyan/GuruKulaDesam')
from tools.tamil_panchangam_engine import IST, get_auspicious_alignment_for_datetime

def parse_time_window(time_str: str, target_date):
    # e.g. "07:45 AM – 08:45 AM"
    parts = [p.strip() for p in re.split(r"[-–—]", time_str)]
    if len(parts) != 2:
        return None
    def parse_one(s):
        dt = datetime.strptime(s.strip(), "%I:%M %p")
        return datetime(target_date.year, target_date.month, target_date.day, dt.hour, dt.minute, tzinfo=IST)
    try:
        return parse_one(parts[0]), parse_one(parts[1])
    except Exception:
        return None

def get_day_auspicious_slots(target_date):
    midday_dt = datetime(target_date.year, target_date.month, target_date.day, 12, 0, tzinfo=IST)
    info = get_auspicious_alignment_for_datetime(midday_dt)
    
    # 4 Authentic Daily Auspicious Muhurtham Windows from Tamil Panchangam:
    # 1. Nalla Neram (காலை நல்ல நேரம்)
    # 2. Gowri Nalla Neram Morning (காலை கௌரி நல்ல நேரம்)
    # 3. Nalla Neram Evening (மாலை நல்ல நேரம்)
    # 4. Gowri Nalla Neram Evening (மாலை கௌரி நல்ல நேரம்)
    windows = []
    for key in ("nalla_neram_am", "gowri_am", "nalla_neram_pm", "gowri_pm"):
        raw = info.get(key)
        if raw:
            win = parse_time_window(raw, target_date)
            if win:
                windows.append((key, win[0], win[1]))
    
    # Sort windows chronologically
    windows.sort(key=lambda x: x[1])
    
    auspicious_slots = []
    for name, st, end in windows:
        # Pick an organic minute within the authentic auspicious muhurtham window
        total_seconds = int((end - st).total_seconds())
        # Divine minute within window, avoiding the very edge seconds
        offset_sec = random.randint(min(180, total_seconds // 4), max(total_seconds - 300, total_seconds // 2))
        slot_dt = st + timedelta(seconds=offset_sec)
        auspicious_slots.append((name, slot_dt, st, end))
        
    return auspicious_slots, info

now = datetime.now(IST)
for d in range(7):
    t_date = (now + timedelta(days=d)).date()
    slots, info = get_day_auspicious_slots(t_date)
    print(f"=== {t_date.strftime('%Y-%m-%d %A')} ({info['tamil_month_ta']} {info['tamil_day']}) ===")
    for name, s_dt, st, end in slots:
        print(f"  {name:16}: {s_dt.strftime('%I:%M %p')} (Window: {st.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')})")
