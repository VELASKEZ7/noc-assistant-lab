$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$inputFile = Join-Path $root "data\alerts.json"
$outputFile = Join-Path $root "out\triage_report.json"
$markdownFile = Join-Path $root "out\triage_report.md"
$entrypoint = Join-Path $root "src\noc_assistant.py"

python $entrypoint --input $inputFile --output $outputFile --markdown-output $markdownFile

Write-Host "Reporte generado en: $outputFile"
Write-Host "Resumen markdown en: $markdownFile"
