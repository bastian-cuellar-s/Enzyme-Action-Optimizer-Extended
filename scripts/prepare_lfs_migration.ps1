<#
PowerShell helper to prepare and (optionally) run a Git LFS history migration.
This script is conservative: it will create a fresh clone, ensure git-lfs is installed,
create/verify .gitattributes, run the migration locally and show verification steps.
It will NOT push rewritten history; pushing requires explicit manual confirmation and
will be printed as the final command to run.

Usage: run from a machine with git, git-lfs and sufficient disk space.

Important: this script rewrites history locally when running the migrate step.
Do NOT run the migrate step until you've backed up the repo (mirror) and confirmed
that you want to proceed.
#>

param(
    [string]$SourceRepoPath = "C:\\code\\Enzyme-Action-Optimizer-Extended",
    [string]$WorkDir = "C:\\code\\eao-lfs-migrate",
    [string]$Ref = "main",
    [switch]$RunMigrate  # off by default; when provided the script runs 'git lfs migrate import'
)

function Ensure-ExecutableExists([string]$exe) {
    $which = & git --no-pager --version 2>$null
    try {
        $p = Get-Command $exe -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

Write-Host "Preparing LFS migration helper"
Write-Host "Source repo: $SourceRepoPath"
Write-Host "Working directory for migration: $WorkDir"
Write-Host "Target ref: $Ref"

# Ensure required executables are available
if (-not (Ensure-ExecutableExists 'git')) {
    Write-Error "git was not found in PATH. Please install Git before running this script."
    exit 1
}
if (-not (Ensure-ExecutableExists 'git-lfs')) {
    Write-Error "git-lfs was not found in PATH. Please install Git LFS (https://git-lfs.github.com/) before running this script."
    exit 1
}

if (-not (Test-Path $SourceRepoPath)) {
    Write-Error "Source repo path does not exist: $SourceRepoPath"
    exit 1
}

# Create working dir
if (Test-Path $WorkDir) {
    Write-Host "Workdir exists: $WorkDir — removing to start fresh"
    Remove-Item -Recurse -Force $WorkDir
}
New-Item -ItemType Directory -Path $WorkDir | Out-Null

Write-Host "Cloning a fresh working copy into $WorkDir..."
git clone $SourceRepoPath $WorkDir
Push-Location $WorkDir

Write-Host "Initializing Git LFS in the clone..."
git lfs install

if (-not (Test-Path .gitattributes)) {
    Write-Host ".gitattributes not found — creating a conservative default for problems/ and large binaries"
    @"
# Git LFS attributes for large problem datasets
problems/** filter=lfs diff=lfs merge=lfs -text
*.mexw64 filter=lfs diff=lfs merge=lfs -text
*.mat filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
"@ | Out-File -Encoding UTF8 .gitattributes
    git add .gitattributes
    git commit -m "chore: add .gitattributes for Git LFS (problems/**)"
} else {
    Write-Host ".gitattributes exists — please review and adjust before running migration if needed"
}

Write-Host "Suggested include pattern for migration: problems/**"

if (-not $RunMigrate) {
    Write-Host "Dry run complete — migration will not run because -RunMigrate switch was not provided."
    Write-Host "If you intend to run the migration now, re-run this script with -RunMigrate." 
    Write-Host "Example: .\prepare_lfs_migration.ps1 -SourceRepoPath 'C:\\path' -WorkDir 'C:\\temp' -RunMigrate"
    Pop-Location
    exit 0
}

# Confirm destructive step
$confirm = Read-Host "You passed -RunMigrate. THIS WILL REWRITE HISTORY LOCALLY. Type 'YES' to continue"
if ($confirm -ne 'YES') {
    Write-Host "Aborting migration — confirmation not provided."
    Pop-Location
    exit 1
}

Write-Host "Running 'git lfs migrate import' for problems/** (this rewrites history locally)..."
# Use --include-ref to limit to the target branch
git lfs migrate import --include="problems/**" --include-ref=refs/heads/$Ref

Write-Host "Migration complete locally. Verifications:" 
git count-objects -vH
Write-Host "Show LFS-tracked files (sample):"
git lfs ls-files | Select-Object -First 20

Write-Host "Run your test suite now to verify behavior (examples):"
Write-Host "pytest -q"

Write-Host "If everything is correct, push the rewritten branch to remote with --force-with-lease:" 
Write-Host "git remote add origin <remote-url>   # if not present" 
Write-Host "git push origin $Ref --force-with-lease"

Pop-Location

Write-Host "Done. Migration performed locally in: $WorkDir — no push performed by this script."
