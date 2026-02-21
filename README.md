# NOC Assistant Lab

Automatiza el triage inicial de alertas de infraestructura con control de riesgo SLA.

## Que hace
- Lee alertas desde `data/alerts.json`
- Clasifica prioridad y accion inicial de runbook
- Estima tiempo de respuesta por severidad y edad de la alerta
- Detecta potencial incumplimiento de SLA (`risk_sla_breach`)
- Genera reporte JSON en `out/triage_report.json`
- Genera resumen Markdown en `out/triage_report.md`

## Ejecutar
```powershell
cd C:\Users\Administrator\portfolio-redes-projects\noc-assistant-lab
powershell -ExecutionPolicy Bypass -File .\scripts\main.ps1
```

## Ejecucion deterministica (demo)
```powershell
python .\src\noc_assistant.py --input .\data\alerts.json --output .\out\triage_report.json --markdown-output .\out\triage_report.md --now 2026-02-21T04:00:00Z
```

## Probar
```powershell
cd C:\Users\Administrator\portfolio-redes-projects\noc-assistant-lab
python -m unittest tests\test_noc_assistant.py -v
```
