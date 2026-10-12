import os
import json
import base64
import sqlite3
import shutil
import ctypes
from ctypes import wintypes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class DATA_BLOB(ctypes.Structure):
    _fields_ = [('cbData', wintypes.DWORD), ('pbData', ctypes.POINTER(ctypes.c_byte))]

def decrypt_master_key(local_state_path):
    with open(local_state_path, 'r', encoding='utf-8') as f:
        local_state = json.load(f)
    encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:]
    blob_in = DATA_BLOB(len(encrypted_key), ctypes.cast(ctypes.create_string_buffer(encrypted_key), ctypes.POINTER(ctypes.c_byte)))
    blob_out = DATA_BLOB()
    if ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)):
        key = ctypes.string_at(blob_out.pbData, blob_out.cbData)
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)
        return key
    return None

def decrypt_value(encrypted_val, key):
    try:
        # Chrome/Edge v10+ prefix
        if encrypted_val[:3] == b'v10' or encrypted_val[:3] == b'v11':
            nonce = encrypted_val[3:15]
            ciphertext = encrypted_val[15:]
            aesgcm = AESGCM(key)
            decrypted = aesgcm.decrypt(nonce, ciphertext, None)
            return decrypted.decode('utf-8', errors='ignore')
    except Exception:
        pass
    return None

def check_browser_cookies(name, base_dir):
    local_state = os.path.join(base_dir, 'Local State')
    cookies_db = os.path.join(base_dir, 'Default', 'Network', 'Cookies')
    if not os.path.exists(local_state) or not os.path.exists(cookies_db):
        return f"{name}: Not found"
    try:
        key = decrypt_master_key(local_state)
        if not key:
            return f"{name}: Could not decrypt master key"
        tmp_db = f"temp_{name}_cookies.db"
        shutil.copyfile(cookies_db, tmp_db)
        conn = sqlite3.connect(tmp_db)
        cur = conn.cursor()
        cur.execute("SELECT host_key, name, encrypted_value FROM cookies WHERE host_key LIKE '%google.com' OR host_key LIKE '%youtube.com'")
        rows = cur.fetchall()
        conn.close()
        if os.path.exists(tmp_db):
            os.remove(tmp_db)
            
        auth_cookies = []
        for host, cname, enc_val in rows:
            if cname in ['SAPISID', 'SSID', 'SID', 'LOGIN_INFO']:
                val = decrypt_value(enc_val, key)
                auth_cookies.append((host, cname, bool(val)))
                
        return f"{name}: Total {len(rows)} cookies. Key auth cookies found: {auth_cookies[:6]}"
    except Exception as e:
        return f"{name}: Error: {e}"

if __name__ == '__main__':
    print(check_browser_cookies('Chrome_Default', r'C:\Users\Shishyan\AppData\Local\Google\Chrome\User Data'))
    print(check_browser_cookies('Edge_Default', r'C:\Users\Shishyan\AppData\Local\Microsoft\Edge\User Data'))
