# Arquitectura

Flujo funcional del laboratorio:

1. Monitoreo emite alerta (simulada con `data/alerts.json`).
2. Motor de triage (`src/noc_assistant.py`) clasifica prioridad.
3. Se asigna accion de runbook y ETA inicial.
4. Se persiste salida en `out/triage_report.json`.

Campos clave por alerta:
- `severity`: critical, high, medium, low
- `priority`: P1, P2, P3, P4
- `runbook_action`: primer paso operativo sugerido
- `eta_minutes`: tiempo estimado a primera accion
