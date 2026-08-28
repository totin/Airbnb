$projectRoot = $PSScriptRoot
$backendPath = Join-Path $projectRoot "backend"
$frontendPath = Join-Path $projectRoot "frontend"
$venvPython = Join-Path $backendPath "venv\Scripts\python.exe"

if (Test-Path $venvPython) {
    $backendCommand = "& '$venvPython' -m uvicorn src.app:app --reload"
} else {
    $backendCommand = "python -m uvicorn src.app:app --reload"
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
    "Set-Location '$frontendPath'; npm run dev"
)

Write-Host "Backend: http://localhost:8000/docs"
Write-Host "Frontend: revisar la URL mostrada por Vite"