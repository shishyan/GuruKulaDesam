import os
import sys
import json
import sqlite3
import base64
import shutil
import ctypes
from ctypes import wintypes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

sys.stdout.reconfigure(encoding='utf-8')

# Windows DPAPI decrypt helper
class DATA_BLOB(ctypes.Structure):
    _fields_ = [('cbData', wintypes.DWORD),
                ('pbData', ctypes.POINTER(ctypes.c_byte))]

def dpapi_decrypt(encrypted_bytes):
    blob_in = DATA_BLOB(len(encrypted_bytes), ctypes.cast(ctypes.create_string_buffer(encrypted_bytes), ctypes.POINTER(ctypes.c_byte)))
    blob_out = DATA_BLOB()
    
    ret = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blob_in),
        None,
        None,
        None,
        None,
        0,
        ctypes.byref(blob_out)
    )
    if not ret:
        raise Exception("Failed to decrypt DPAPI data")
    
    decrypted = ctypes.string_at(blob_out.pbData, blob_out.cbData)
    ctypes.windll.kernel32.LocalFree(blob_out.pbData)
    return decrypted

def get_edge_master_key():
    local_state_path = os.path.expanduser('~') + r'\AppData\Local\Microsoft\Edge\User Data\Local State'
    with open(local_state_path, 'r', encoding='utf-8') as f:
        local_state = json.load(f)
    encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
    # Remove DPAPI prefix (5 bytes)
    encrypted_key = encrypted_key[5:]
    master_key = dpapi_decrypt(encrypted_key)
    return master_key

def decrypt_cookie_value(encrypted_val, master_key):
    try:
        if encrypted_val.startswith(b'v10') or encrypted_val.startswith(b'v11') or encrypted_val.startswith(b'v20'):
            iv = encrypted_val[3:15]
            ciphertext = encrypted_val[15:]
            aesgcm = AESGCM(master_key)
            decrypted = aesgcm.decrypt(iv, ciphertext, None)
            return decrypted.decode('utf-8', errors='ignore')
        else:
            return dpapi_decrypt(encrypted_val).decode('utf-8', errors='ignore')
    except Exception as e:
        return None

try:
    master_key = get_edge_master_key()
    print("Edge master key extracted successfully!")

    # Copy cookie db to avoid file lock
    edge_cookie_path = os.path.expanduser('~') + r'\AppData\Local\Microsoft\Edge\User Data\Default\Network\Cookies'
    temp_cookie_path = 'production/temp_edge_cookies.db'
    shutil.copyfile(edge_cookie_path, temp_cookie_path)

    conn = sqlite3.connect(temp_cookie_path)
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, encrypted_value, path, is_secure, is_httponly, expires_utc FROM cookies WHERE host_key LIKE '%distrokid%'")
    rows = cursor.fetchall()
    print(f"Found {len(rows)} DistroKid cookies in Edge!")

    cookies_list = []
    for host, name, enc_val, path, secure, httponly, expires in rows:
        val = decrypt_cookie_value(enc_val, master_key)
        if val:
            cookies_list.append({
                'name': name,
                'value': val,
                'domain': host,
                'path': path,
                'secure': bool(secure),
                'httpOnly': bool(httponly)
            })
            print(f"  {name} = {val[:15]}... ({host})")

    with open('production/edge_distrokid_cookies.json', 'w', encoding='utf-8') as f:
        json.dump(cookies_list, f, indent=2)

    conn.close()
    if os.path.exists(temp_cookie_path):
        os.remove(temp_cookie_path)

except Exception as e:
    print("Error extracting Edge cookies:", e)
