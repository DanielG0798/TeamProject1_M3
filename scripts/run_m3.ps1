param(
    [string]$Course = "physics_101",
    [string]$Question,
    [switch]$Interactive,
    [string]$Model
)

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$python = Join-Path $root ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    Write-Error "Virtual environment not found. Run: python -m venv .venv; .\.venv\Scripts\pip.exe install -r requirements.txt"
    exit 1
}

$arguments = @("-m", "src.m3_agent", "--course", $Course)
if ($Interactive -or -not $Question) {
    $arguments += "--interactive"
} else {
    $arguments += @("--question", $Question)
}
if ($Model) {
    $arguments += @("--model", $Model)
}

& $python @arguments
exit $LASTEXITCODE
