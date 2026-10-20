@echo off
setlocal
title NEURO-METRIC Cognitive Assessment Engine

echo [NEURO-METRIC] Scanning for Chromium Runtime...

set CHROME_PATH=""
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" set CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
if %CHROME_PATH%=="" if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" set CHROME_PATH="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
if %CHROME_PATH%=="" if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" set CHROME_PATH="%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"

set EDGE_PATH=""
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" set EDGE_PATH="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if %EDGE_PATH%=="" if exist "C:\Program Files\Microsoft\Edge\Application\msedge.exe" set EDGE_PATH="C:\Program Files\Microsoft\Edge\Application\msedge.exe"

set TARGET_FILE="%~dp0index.html"

if not %CHROME_PATH%=="" (
    echo [NEURO-METRIC] Launching via Google Chrome Desktop Engine...
    start "" %CHROME_PATH% --app="file:///%~dp0index.html" --window-size=1500,950
    goto :done
)

if not %EDGE_PATH%=="" (
    echo [NEURO-METRIC] Launching via Chromium Microsoft Edge Desktop Engine...
    start "" %EDGE_PATH% --app="file:///%~dp0index.html" --window-size=1500,950
    goto :done
)

echo [NEURO-METRIC] Fallback: Launching via Default System Browser...
start "" %TARGET_FILE%

:done
echo [NEURO-METRIC] Assessment session active.
exit /b 0
