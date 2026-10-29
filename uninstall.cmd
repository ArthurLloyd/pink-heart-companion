@echo off
setlocal
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\Uninstall.ps1" %*
set "pet_exit_code=%errorlevel%"
if not "%pet_exit_code%"=="0" echo Uninstall did not complete. See the message above.
if /i not "%PINK_HEART_NO_PAUSE%"=="1" pause
exit /b %pet_exit_code%
