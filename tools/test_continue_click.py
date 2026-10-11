import time
import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]
    cdp = ctx.new_cdp_session(page)
    
    file_chooser_event = []
    
    def on_event(event_name, params):
        if 'fileChooserOpened' in event_name or 'FileChooser' in event_name:
            print(f'EVENT {event_name}: {params}')
            file_chooser_event.append(params)
            
    # Enable Page domain and file chooser interception
    cdp.send('Page.enable')
    cdp.send('Page.setInterceptFileChooserDialog', {'enabled': True})
    
    # Listen to CDP events via cdp.on
    cdp.on('Page.fileChooserOpened', lambda p: on_event('Page.fileChooserOpened', p))
    
    # Click Continue button at (1130, 580)
    print('Clicking Continue at (1130, 580)...')
    cdp.send('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': 1130, 'y': 580})
    cdp.send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': 1130, 'y': 580, 'button': 'left', 'clickCount': 1})
    cdp.send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': 1130, 'y': 580, 'button': 'left', 'clickCount': 1})
    
    time.sleep(2)
    print(f'File chooser events received: {len(file_chooser_event)}')
    
    if file_chooser_event:
        srt_file = os.path.abspath('production/subtitles/31xVgvxoiUA.srt')
        print(f'Handling file chooser with: {srt_file}')
        cdp.send('Page.handleFileChooser', {
            'action': 'accept',
            'files': [srt_file]
        })
        print('Handled file chooser!')
        time.sleep(3)
