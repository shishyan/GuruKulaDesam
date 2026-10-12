import ctypes

user32 = ctypes.windll.user32
EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = user32.GetWindowTextW
GetWindowTextLength = user32.GetWindowTextLengthW
IsWindowVisible = user32.IsWindowVisible
GetWindowThreadProcessId = user32.GetWindowThreadProcessId

def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            pid = ctypes.c_ulong()
            GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            title = buff.value
            if any(term in title.lower() for term in ['chrome', 'flow', 'google', 'studio', 'youtube']):
                print(f"PID: {pid.value} | Title: {title}")
    return True

EnumWindows(EnumWindowsProc(foreach_window), 0)
