@echo off
echo Closing lingering Chrome processes...
taskkill /F /IM chrome.exe >nul 2>&1
timeout /t 1 >nul
echo Launching your Google Chrome with automation bridge enabled...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-allow-origins=* "https://studio.youtube.com"
echo Chrome is now running with automation control on port 9222!

