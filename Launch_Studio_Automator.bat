@echo off
echo ======================================================================
echo Launching Dedicated YouTube Studio Automation Window (Port 9225)...
echo (Your Google Flow process on Port 9222 will remain completely untouched)
echo ======================================================================
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9225 --user-data-dir="%USERPROFILE%\.antigravity_shishyan" --remote-allow-origins=* "https://studio.youtube.com"
echo.
echo Window launched! You can now let Antigravity run the automation.
