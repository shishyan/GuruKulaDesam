import win32gui
import win32process

def enum_windows_callback(hwnd, extra):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            print(f"PID: {pid} | Title: {title}")

try:
    win32gui.EnumWindows(enum_windows_callback, None)
except Exception as e:
    print("win32gui error:", e)
