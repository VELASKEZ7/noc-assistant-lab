$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$inputFile = Join-Path $root "data\alerts.json"
$outputFile = Join-Path $root "out\triage_report.json"
$entrypoint = Join-Path $root "src\noc_assistant.py"

python $entrypoint --input $inputFile --output $outputFile

Write-Host "Reporte generado en: $outputFile"
