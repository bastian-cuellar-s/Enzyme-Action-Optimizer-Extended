<#
preview_problems_size.ps1
Lists the largest files under the 'problems/' directory to help decide which patterns to track with Git LFS.
#>

param(
    [int]$Top = 50
)

$problemsPath = Join-Path (Get-Location) 'problems'
if (-not (Test-Path $problemsPath)) {
    Write-Error "Directory 'problems/' not found in the repository root."
    exit 2
}

Write-Host "Listing top $Top largest files under 'problems/':`n"
Get-ChildItem -Path $problemsPath -Recurse -File |
    Select-Object FullName, @{Name='SizeMB';Expression={[math]::Round($_.Length/1MB,3)}} |
    Sort-Object -Property SizeMB -Descending |
    Select-Object -First $Top |
    Format-Table -AutoSize
