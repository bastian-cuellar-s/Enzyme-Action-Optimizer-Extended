<#
Build sdist and wheel and zip them into artifacts for release.
Usage:
    .\scripts\build_release.ps1
#>

python -m pip install --upgrade build
python -m build --sdist --wheel
if (Test-Path dist) {
    Compress-Archive -Path dist\* -DestinationPath dist\release_artifacts.zip -Force
    Write-Host "Created dist/release_artifacts.zip"
} else {
    Write-Host "No dist folder created."
}
