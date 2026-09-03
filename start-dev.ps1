$projectRoot = $PSScriptRoot
$backendPath = Join-Path $projectRoot "backend"
$frontendPath = Join-Path $projectRoot "frontend"
$venvPython = Join-Path $backendPath "venv\Scripts\python.exe"
$backendPort = 8000
while (Get-NetTCPConnection -LocalPort $backendPort -State Listen -ErrorAction SilentlyContinue) {
    $backendPort++
}
if ($backendPort -ne 8000) {
    Write-Host "El puerto 8000 está ocupado; usando el backend en http://localhost:$backendPort"
}

if (Test-Path $venvPython) {
    $backendCommand = "& '$venvPython' -m uvicorn src.app:app --reload --port $backendPort"
} else {
    $backendCommand = "python -m uvicorn src.app:app --reload --port $backendPort"
}

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-NoLogo",
    "-Command",
    "Set-Location '$backendPath'; $backendCommand"
)

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-NoLogo",
    "-Command",
    "Set-Location '$frontendPath'; `$env:VITE_API_URL='http://localhost:$backendPort'; npm run dev"
)

Write-Host "Backend: http://localhost:$backendPort/docs"
Write-Host "Frontend: revisar la URL mostrada por Vite"