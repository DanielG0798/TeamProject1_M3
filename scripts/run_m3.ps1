# Run the Milestone 3 agent with example inputs (Windows PowerShell).
$ErrorActionPreference = "Stop"

Set-Location (Join-Path $PSScriptRoot "..")

if (Test-Path ".venv\Scripts\Activate.ps1") {
    . .\.venv\Scripts\Activate.ps1
}

python -m src.m3_agent `
    --course physics_101 `
    --question "I am stuck setting up Newton's second law."
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
