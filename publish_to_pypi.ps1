# Publish the package to PyPI

# Clean up previous builds
Write-Host "Cleaning up previous builds..." -ForegroundColor Cyan
Remove-Item -Path "dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "src\litprinter.egg-info" -Recurse -Force -ErrorAction SilentlyContinue

# Build the package
Write-Host "Building the package..." -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install --upgrade build twine
python -m build

# Check the package
Write-Host "Checking the package..." -ForegroundColor Cyan
python -m twine check dist/*

# Ask for confirmation
$confirmation = Read-Host "Do you want to publish to PyPI? (y/n)"
if ($confirmation -eq 'y') {
    # Publish to PyPI
    Write-Host "Publishing to PyPI..." -ForegroundColor Cyan
    python -m twine upload dist/*
    
    Write-Host "Package published successfully!" -ForegroundColor Green
} else {
    Write-Host "Publication cancelled." -ForegroundColor Yellow
}
