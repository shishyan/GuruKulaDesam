import sys
import os
import pathlib
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from google_auth_oauthlib.flow import InstalledAppFlow

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

ROOT = pathlib.Path(__file__).resolve().parent.parent
CRED_DIR = ROOT / 'data' / 'credentials'
SECRET_FILE = ROOT / "client_secret_336846523109-uvh5e4e0209g2p1ojmhpq02uu349pkpt.apps.googleusercontent.com.json"

SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtubepartner'
]

flow = InstalledAppFlow.from_client_secrets_file(str(SECRET_FILE), SCOPES)
flow.redirect_uri = 'http://localhost:8088/'

auth_url, _ = flow.authorization_url(prompt='consent select_account', access_type='offline')

print("\n" + "="*80)
print("AUTH URL:")
print(auth_url)
print("="*80 + "\n", flush=True)

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if 'code' in params:
            code = params['code'][0]
            print(f"Received authorization code! Exchanging for token...", flush=True)
            try:
                flow.fetch_token(code=code)
                creds = flow.credentials
                token_path = CRED_DIR / 'token.json'
                with open(token_path, 'w', encoding='utf-8') as f:
                    f.write(creds.to_json())
                print(f"\nSUCCESS! Token saved cleanly to {token_path}", flush=True)
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(b"<h1>Authorization Successful!</h1><p>You can close this tab and return to the assistant.</p>")
                
                # Signal exit
                sys.exit(0)
            except Exception as e:
                print(f"Error exchanging token: {e}", flush=True)
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error: {e}".encode('utf-8'))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No code parameter found in callback.")

server = HTTPServer(('127.0.0.1', 8088), CallbackHandler)
print("Server listening on http://127.0.0.1:8088/ ...", flush=True)
server.serve_forever()
