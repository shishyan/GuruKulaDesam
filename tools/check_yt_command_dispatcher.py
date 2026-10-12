import sys
import time
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    # Check if ytd-app or yt.commands exists
    res = page.evaluate('''() => {
        const ytdApp = document.querySelector('ytd-app');
        return {
            hasYtdApp: !!ytdApp,
            hasResolveCommand: !!(ytdApp && ytdApp.resolveCommand),
            hasExecuteCommand: !!(ytdApp && ytdApp.executeCommand),
            hasDispatch: !!(ytdApp && ytdApp.dispatch)
        };
    }''')
    print('Command dispatcher check:', res)
