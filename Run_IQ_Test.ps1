# NEURO-METRIC Chromium Desktop Launcher
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetFile = Join-Path $scriptDir "index.html"
$fileUrl = "file:///" + ($targetFile -replace '\\', '/')

$chromePaths = @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)

$edgePaths = @(
    "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
)

$browserFound = $null

foreach ($p in $chromePaths) {
    if (Test-Path $p) {
        $browserFound = $p
        break
    }
}

if (-not $browserFound) {
    foreach ($p in $edgePaths) {
        if (Test-Path $p) {
            $browserFound = $p
            break
        }
    }
}

if ($browserFound) {
    Write-Host "[NEURO-METRIC] Starting Chromium Desktop App Mode: $browserFound" -ForegroundColor Cyan
    Start-Process -FilePath $browserFound -ArgumentList @("--app=$fileUrl", "--window-size=1500,950")
} else {
    Write-Host "[NEURO-METRIC] Fallback to default browser" -ForegroundColor Yellow
    Start-Process -FilePath $targetFile
}
