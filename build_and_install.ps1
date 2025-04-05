# Build and install the package locally

# Clean up previous builds
Write-Host "Cleaning up previous builds..." -ForegroundColor Cyan
Remove-Item -Path "dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "src\litprinter.egg-info" -Recurse -Force -ErrorAction SilentlyContinue

# Build the package
Write-Host "Building the package..." -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install --upgrade build
python -m build

# Install the package locally
Write-Host "Installing the package locally..." -ForegroundColor Cyan
$WheelFile = Get-ChildItem -Path "dist" -Filter "*.whl" | Select-Object -First 1
if ($WheelFile) {
    python -m pip install --force-reinstall "$($WheelFile.FullName)"
    Write-Host "Package installed successfully!" -ForegroundColor Green
    Write-Host "You can now import litprinter in your Python scripts." -ForegroundColor Green
} else {
    Write-Host "Failed to find wheel file in dist directory." -ForegroundColor Red
}
