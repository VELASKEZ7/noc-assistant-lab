# NOC Assistant Lab

Automatiza el triage inicial de alertas de infraestructura.

## Que hace
- Lee alertas desde `data/alerts.json`
- Clasifica prioridad y accion inicial de runbook
- Estima tiempo de respuesta inicial por severidad
- Genera reporte JSON en `out/triage_report.json`

## Ejecutar
```powershell
cd C:\Users\Administrator\portfolio-redes-projects\noc-assistant-lab
powershell -ExecutionPolicy Bypass -File .\scripts\main.ps1
```

## Probar
```powershell
cd C:\Users\Administrator\portfolio-redes-projects\noc-assistant-lab
python -m unittest tests\test_noc_assistant.py -v
```
