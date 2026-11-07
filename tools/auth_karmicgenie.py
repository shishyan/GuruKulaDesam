import sys, os, pathlib
from google_auth_oauthlib.flow import InstalledAppFlow

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CLIENT_SECRET = '/home/shishyan/GitHub/Shishyan/GuruKulaDesam/data/credentials/projects/client_secret_472322435541.json'
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube'
]

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, scopes=SCOPES)
# Generate URL with prompt=select_account to let the user pick KarmicGenie brand channel
auth_url, _ = flow.authorization_url(prompt='select_account', access_type='offline', include_granted_scopes='true')

print("\n" + "="*80)
print("🔑 AUTHENTICATE KARMICGENIE BRAND CHANNEL:")
print("="*80)
print("1. Open this URL in your browser:")
print(f"\n{auth_url}\n")
print("2. Sign in with your Google Account, choose the 'KarmicGenie' channel.")
print("3. After consenting, paste the authorization code here:")
print("="*80 + "\n")
