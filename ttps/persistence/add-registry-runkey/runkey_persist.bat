@echo off

cmd.exe /C reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnceEx\0001" /v PurpleTesting /t REG_SZ /d "sshot.exe"

timeout /t 15 /nobreak

exit 0
