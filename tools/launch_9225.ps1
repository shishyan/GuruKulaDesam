$profileDir = "$env:USERPROFILE\.antigravity_shishyan"
if (!(Test-Path $profileDir)) { New-Item -ItemType Directory -Path $profileDir -Force }
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
Start-Process -FilePath $chromePath -ArgumentList "--remote-debugging-port=9225 --user-data-dir=`"$profileDir`" --remote-allow-origins=* https://studio.youtube.com"
Start-Sleep -Seconds 4
curl.exe -s http://127.0.0.1:9225/json/version
