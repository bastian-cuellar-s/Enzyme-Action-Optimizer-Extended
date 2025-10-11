<#
Run the project using the project's virtual environment (.venv).

Usage:
    .\scripts\run.ps1            # activates .venv and runs python main.py
    .\scripts\run.ps1 -Test     # runs a quick import test (no interactive prompt)

If .venv does not exist, the script will suggest running setup_venv.ps1
#>

param(
    [switch]$Test
)

$venvPython = Join-Path '.venv' 'Scripts\python.exe'

if (-not (Test-Path $venvPython)) {
    Write-Warning "Virtual environment not found at .venv. Run .\scripts\setup_venv.ps1 first."
    exit 1
}

if ($Test) {
    Write-Host "Running quick import test using .venv python..."
    & $venvPython -c "import main; print('main imported OK')"
    exit $LASTEXITCODE
}

Write-Host "Activating .venv and launching main.py..."
& .\.venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Failed to activate .venv. You can run: .\scripts\setup_venv.ps1"
}

Write-Host "Running: python main.py"
python main.py
