<#
remove_problems_history.ps1
Performs a destructive migration to remove `problems/` from the repository history using git filter-repo.
This script is intentionally conservative: it creates a mirror backup, validates environment, and prompts for explicit confirmation.
#>

param(
    [switch]$WhatIfRun = $false,
    [switch]$DryRun = $false
)

function Assert-CommandExists {
    param([string]$cmd)
    $null = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($LASTEXITCODE -ne 0 -or -not $?) {
        Write-Error "Required command '$cmd' not found in PATH. Please install it and try again."
        exit 2
    }
}

Assert-CommandExists -cmd git
# git-filter-repo may be installed as git-filter-repo or available as python module. Check for binary first.
$filterRepoPresent = $false
if (Get-Command git-filter-repo -ErrorAction SilentlyContinue) {
    $filterRepoPresent = $true
} else {
    try {
        python -c "import git_filter_repo" 2>$null
        $filterRepoPresent = $true
    } catch {
        $filterRepoPresent = $false
    }
}

if (-not $filterRepoPresent) {
    Write-Error "git-filter-repo is required (either the git-filter-repo tool or the python git_filter_repo module). See docs/MIGRATION_TO_LFS.md for installation instructions."
    exit 2
}

$repoPath = (Get-Location).Path
$mirrorPath = Join-Path -Path $repoPath -ChildPath "..\Enzyme-Action-Optimizer-Extended-mirror-backup.git"

Write-Host "Creating a mirror backup at: $mirrorPath"
if (-not (Test-Path $mirrorPath)) {
    git clone --mirror "$repoPath" "$mirrorPath"
} else {
    Write-Host "Mirror backup already exists at $mirrorPath"
}

Write-Host "
This script will run 'git filter-repo --invert-paths --paths problems/' to remove the 'problems/' directory from history.
This is destructive: it rewrites history and requires a forced push. All collaborators must re-clone after the rewrite.
"

if ($WhatIfRun) {
    Write-Host "WhatIf: Showing the git-filter-repo command that would be run:"
    Write-Host "git filter-repo --invert-paths --paths problems/"
    exit 0
}

if ($DryRun) {
    Write-Host "Dry run: previewing the objects that would be removed (first 50):"
    git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(rest)' | sed -n '1,50p'
    exit 0
}

Write-Host "Type the confirmation token PROCEED_REMOVE_PROBLEMS to continue (or press Ctrl+C to cancel):"
$token = Read-Host
if ($token -ne 'PROCEED_REMOVE_PROBLEMS') {
    Write-Error "Confirmation token did not match. Aborting."
    exit 1
}

Write-Host "Running git filter-repo..."
# Run the filter-repo command
git filter-repo --invert-paths --paths problems/

Write-Host "Filter complete. Review the repository, run tests, then push with --force-with-lease when ready."
Write-Host "Example: git push origin main --force-with-lease"
