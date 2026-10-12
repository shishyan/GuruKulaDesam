import sys
import time
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    cfg = page.evaluate('''() => {
        if (typeof ytcfg === 'undefined') return {error: 'no ytcfg'};
        return {
            apiKey: ytcfg.get('INNERTUBE_API_KEY'),
            loggedIn: ytcfg.get('LOGGED_IN'),
            delegatedSessionId: ytcfg.get('DELEGATED_SESSION_ID'),
            clientName: ytcfg.get('INNERTUBE_CLIENT_NAME'),
            clientVersion: ytcfg.get('INNERTUBE_CLIENT_VERSION'),
            hasSapisid: !!document.cookie.match(/SAPISID=([^;]+)/)
        };
    }''')
    print('Innertube config:', json.dumps(cfg, indent=2))
