import urllib.request
import json
import websocket

tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9225/json/list').read())
t = [tab for tab in tabs if 'flow.google.com' in tab.get('url', '')][0]
ws = websocket.create_connection(t['webSocketDebuggerUrl'], suppress_origin=True)

# Navigate to Google Accounts sign-in / choose account directly in this tab
ws.send(json.dumps({
    'id': 1,
    'method': 'Page.navigate',
    'params': {'url': 'https://accounts.google.com/AccountChooser?service=labs&continue=https%3A%2F%2Fflow.google.com%2F'}
}))
print("Navigated to AccountChooser:", ws.recv())
ws.close()
