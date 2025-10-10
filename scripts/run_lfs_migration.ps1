<#
run_lfs_migration.ps1
Orchestrates a cautious `git lfs migrate import` run in a fresh clone and stops before any push.
Requires an explicit confirmation token to proceed.
#>

param(
    [string]$TargetBranch = 'main'
)

function Assert-CommandExists {
    param([string]$cmd)
    $c = Get-Command $cmd -ErrorAction SilentlyContinue
    if (-not $c) {
        Write-Error "Required command '$cmd' not found in PATH."
        Write-Host "Windows hints:"
        Write-Host "  - Install Git for Windows: https://git-scm.com/download/win"
        Write-Host "  - Install Git LFS: https://github.com/git-lfs/git-lfs/releases or via package manager"
        Write-Host "After installing, restart PowerShell and verify with:`n  git --version`n  git lfs version"
        exit 2
    }
}

Assert-CommandExists -cmd git
Assert-CommandExists -cmd git-lfs

$repoPath = (Get-Location).Path
$workDir = Join-Path -Path (Split-Path -Path $repoPath -Parent) -ChildPath "repo-lfs-migrate"

if (Test-Path $workDir) {
    Write-Host "Working directory $workDir already exists. Please remove or rename it before proceeding." ; exit 1
}

Write-Host "Creating fresh clone at $workDir"
git clone --no-tags "$repoPath" "$workDir"
Set-Location $workDir

Write-Host "Installing Git LFS in the clone..."
git lfs install --local

Write-Host "Preview: top files in 'problems/'"
powershell -NoProfile -Command "& '$PSScriptRoot\preview_problems_size.ps1' -Top 30"

Write-Host "
About to run: git lfs migrate import --include=\"problems/**\" --include-ref=refs/heads/$TargetBranch
This rewrites history in the working clone. It will NOT push changes back to origin.
"

Write-Host "Type the confirmation token PROCEED LFS MIGRATE to run the migration (or press Enter to cancel):"
$token = Read-Host
if ($token -ne 'PROCEED LFS MIGRATE') {
    Write-Host "Token did not match. Aborting. No destructive actions were taken." ; exit 1
}

Write-Host "Running migration..."
git lfs migrate import --include="problems/**" --include-ref=refs/heads/$TargetBranch

Write-Host "Migration finished locally. Run tests and inspect the clone before pushing. Example verification commands:"
Write-Host "  git count-objects -vH"
Write-Host "  pytest -q"
Write-Host "  git lfs ls-files | Select-Object -First 20"

Write-Host "If verified, push with: git push origin $TargetBranch --force-with-lease"

Write-Host "Done."
