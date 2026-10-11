import sys
import time
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    
    # Listen to network responses to see if /youtubei/v1/browse/edit_playlist succeeds
    def on_response(response):
        if 'edit_playlist' in response.url:
            print(f'EDIT_PLAYLIST HTTP {response.status}: {response.url}', flush=True)
            try:
                print('Response body:', response.text()[:200], flush=True)
            except Exception as e:
                print('Error reading response:', e, flush=True)
                
    page.on('response', on_response)
    
    # Test resolving command for setVideoId: 56B44F6D10557CC6 (Row 1)
    print('Testing resolveCommand for Move to top on 56B44F6D10557CC6...', flush=True)
    res = page.evaluate('''() => {
        const endpoint = {
            commandMetadata: {
                webCommandMetadata: {
                    sendPost: true,
                    apiUrl: "/youtubei/v1/browse/edit_playlist"
                }
            },
            playlistEditEndpoint: {
                playlistId: "PLW7qBZp_Q8Ro",
                actions: [
                    {
                        setVideoId: "56B44F6D10557CC6",
                        action: "ACTION_MOVE_VIDEO_AFTER"
                    }
                ],
                params: "CAFAAQ%3D%3D"
            }
        };
        const ytdApp = document.querySelector('ytd-app');
        return ytdApp.resolveCommand(endpoint);
    }''')
    print('resolveCommand returned:', res, flush=True)
    time.sleep(3)
