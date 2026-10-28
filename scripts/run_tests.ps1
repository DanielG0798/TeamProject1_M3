# Run the Milestone 3 ten-case evaluation and write evaluation_results.csv (Windows PowerShell).
$ErrorActionPreference = "Stop"

Set-Location (Join-Path $PSScriptRoot "..")

if (Test-Path ".venv\Scripts\Activate.ps1") {
    . .\.venv\Scripts\Activate.ps1
}

# Run as a module so the repo root is on sys.path (evaluate_m3 imports src.m3_agent).
python -m scripts.evaluate_m3 @args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
