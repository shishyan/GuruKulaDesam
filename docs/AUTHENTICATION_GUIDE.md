# Guru Kula Desam & Shishyan Multi-Channel YouTube OAuth & Authentication Guide

> **Author / Channel**: Guru Kula Desam (`@guru-kula-desam` / `shishyan@gmail.com` / `nagaraj957@gmail.com`)  
> **Channel ID**: `UCPqB1A_WzpLJec6q69BOO3Q`  
> **Target Scope**: YouTube Data API v3 publishing, video uploads (Unlisted/Private/Public), caption synchronization, thumbnail attachment, playlist curation, and multi-project quota rotation.

---

## 1. Quick Resolution: Active Working OAuth Token

The active and tested OAuth 2.0 token for `@guru-kula-desam` is backed by GCP Project `472322435541` (`home-manager-2026`).

### 1.1 Local Path (Git-Ignored)
Always place the active token at:
```bash
/home/antigravity/shishyan/GuruKulaDesam/data/credentials/token.json
```
*(Directory `/data/*` is explicitly excluded in `GuruKulaDesam/.gitignore` to prevent credential leaks).*

### 1.2 Google Drive Cloud Backup
If running on a fresh VM or Google Colab instance without local credentials, download the verified token directly:
- **Google Drive File ID**: `1Bt8F9nbr4oJw3d9t7VJ2VvG2GqWaIu7M`
- **File Name**: `token.json`
- **Restore Command**:
  ```bash
  mkdir -p /home/antigravity/shishyan/GuruKulaDesam/data/credentials
  gdrive readonly download 1Bt8F9nbr4oJw3d9t7VJ2VvG2GqWaIu7M --out /home/antigravity/shishyan/GuruKulaDesam/data/credentials/token.json
  ```

---

## 2. Token Details & Diagnostic Findings

During our security and diagnostic scan:
- **`token_backup_guru-kula-desam.json`** (`ID: 11_o61ZLkT5dz0uVclTWF_-rE7F4uDkJ4`) was linked to client ID `440375337189-km8e46cvefo6ccu1k88e99upfg4blh9d`, which has been retired/deleted in GCP (`deleted_client` HTTP 401).
- **`token.json`** (`ID: 1Bt8F9nbr4oJw3d9t7VJ2VvG2GqWaIu7M`) is linked to active GCP client `472322435541-0d035ei...` and refreshed successfully with active access to `@guru-kula-desam`.

---

## 3. Python Verification Script (Headless & Zero-Dependency)

In containerized or remote environments without `google-api-python-client` installed, test or refresh the token using native standard library Python:

```python
import urllib.request, urllib.parse, json
from pathlib import Path

TOKEN_PATH = Path("/home/antigravity/shishyan/GuruKulaDesam/data/credentials/token.json")

def verify_youtube_token():
    with open(TOKEN_PATH) as f:
        d = json.load(f)
    
    # 1. Refresh Access Token
    payload = urllib.parse.urlencode({
        'client_id': d['client_id'],
        'client_secret': d['client_secret'],
        'refresh_token': d['refresh_token'],
        'grant_type': 'refresh_token'
    }).encode('utf-8')

    req = urllib.request.Request('https://oauth2.googleapis.com/token', data=payload)
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        access_token = res['access_token']
        print("✓ Token refreshed successfully.")

    # 2. Check Channel Details
    api_req = urllib.request.Request('https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true')
    api_req.add_header('Authorization', f'Bearer {access_token}')
    with urllib.request.urlopen(api_req) as api_resp:
        data = json.loads(api_resp.read().decode('utf-8'))
        for item in data.get('items', []):
            print(f"Channel Title : {item['snippet']['title']}")
            print(f"Handle        : {item['snippet'].get('customUrl', '')}")
            print(f"Channel ID    : {item['id']}")

if __name__ == "__main__":
    verify_youtube_token()
```

---

## 4. Multi-Project Quota Pool Architecture

YouTube Data API imposes a default quota of 10,000 units/day per Google Cloud project. Video uploads cost 1,600 units each (limiting a single project to ~6 video uploads per day).

To circumvent daily quota exhaustion across the 3 Guru Kula Desam channels, 5 rotating GCP client secret projects are cataloged in Google Drive (`GuruKulaDesam/Tools/Credentials/`):

| Project Number | Project ID | Client ID Prefix | Drive ID (`client_secret`) |
|---|---|---|---|
| **472322435541** | `home-manager-2026` *(Active)* | `472322435541-0d035ei` | `1LQZZyHcUhUsPAILDFassg3wZY5jdauVB` |
| **839236964216** | `guru-kula-desam` | `839236964216-e8s01ds` | `1h5tpg-YTj7jMondlxeozf570Y5xg0ULa` |
| **801831475660** | `gen-lang-client-0601170683` | `801831475660-6672mjf` | `1kn18K3gRZmFmpShydYogtpm25IHouqQo` |
| **942198183044** | `lotusnaga` | `942198183044-l29101d` | `1wX5IH8Es4_zZu5NeIpKW1TBURP2QITRP` |
| **440375337189** | `newton-491915` | `440375337189-km8e46c` | `17yfs7x7AKIVAspPkvPhbbGQs4DWQuwjE` |

### Quota Switching Logic:
When an upload script encounters `quotaExceeded` (HTTP 403), switch the `client_id` and `client_secret` to the next project in the pool while retaining the authorized user refresh token, or switch the credential token file.

---

## 5. Security & Safety Rules

1. **Never Commit Raw Tokens or Secrets to Git**:
   Always verify `.gitignore` contains:
   ```gitignore
   /data/*
   *client_secret*.json
   token.json
   client_secrets.json
   ```
2. **Always Use `gdrive` CLI for Transport**:
   Do not paste raw refresh tokens into chat logs or public repos. Use `gdrive readonly download <ID>` into local `/data/credentials/` or `/tmp`.
