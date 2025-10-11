<#
Setup virtual environment for the project (PowerShell).

Usage (from project root):
    .\scripts\setup_venv.ps1

What it does:
 - Creates a virtual environment in .venv (if not exists)
 - Installs packages from requirements.txt
 - Prints instructions to activate the environment and run the project
#>

Param(
    [string]$VenvPath = ".venv",
    [string]$Requirements = "requirements.txt"
)

Write-Host "Setting up virtual environment at '$VenvPath'..."

if (-not (Test-Path $VenvPath)) {
    python -m venv $VenvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment. Ensure Python is on PATH and version >= 3.8"
        exit 1
    }
    Write-Host "Virtual environment created."
} else {
    Write-Host "Virtual environment already exists. Skipping creation."
}

# Install dependencies
$pip = Join-Path $VenvPath 'Scripts\pip.exe'
if (-not (Test-Path $pip)) {
    Write-Warning "pip not found inside virtualenv. Attempting to use system pip..."
    $pip = "pip"
}

if (Test-Path $Requirements) {
    Write-Host "Installing dependencies from $Requirements..."
    & $pip install -r $Requirements
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install dependencies. See pip output above."
        exit 1
    }
    Write-Host "Dependencies installed."
} else {
    Write-Warning "$Requirements not found. Skipping dependency installation."
}

Write-Host "Done. To activate the virtual environment run:" -ForegroundColor Green
Write-Host "    .\$VenvPath\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "Then run the project with:" -ForegroundColor Green
Write-Host "    python main.py" -ForegroundColor Yellow
