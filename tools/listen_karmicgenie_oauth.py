import sys, os, json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from google_auth_oauthlib.flow import InstalledAppFlow

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CLIENT_SECRET = '/home/shishyan/GitHub/Shishyan/GuruKulaDesam/data/credentials/projects/client_secret_472322435541.json'
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube'
]

flow = InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRET,
    scopes=SCOPES,
    redirect_uri='http://localhost:8088/'
)

auth_url, _ = flow.authorization_url(prompt='select_account', access_type='offline')

print("AUTH_LINK_READY:", auth_url)

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        if 'code' in query:
            code = query['code'][0]
            flow.fetch_token(code=code)
            creds = flow.credentials
            token_data = {
                'token': creds.token,
                'refresh_token': creds.refresh_token,
                'token_uri': creds.token_uri,
                'client_id': creds.client_id,
                'client_secret': creds.client_secret,
                'scopes': creds.scopes
            }
            out_file = '/home/shishyan/GitHub/Shishyan/GuruKulaDesam/data/credentials/token_karmicgenie.json'
            with open(out_file, 'w') as f:
                json.dump(token_data, f, indent=2)
            print(f"SUCCESS: Saved token to {out_file}")
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b"<h1>KarmicGenie Authorization Successful!</h1><p>You can close this tab and return to the assistant.</p>")
            # Exit server
            sys.exit(0)
        else:
            self.send_response(400)
            self.end_headers()

server = HTTPServer(('localhost', 8088), OAuthHandler)
print("Listening on http://localhost:8088 for callback...")
server.handle_request()
