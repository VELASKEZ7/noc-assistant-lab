# NOC Assistant Lab

## Objetivo
Reducir tiempos de triage operativo con automatizaciones de primera respuesta.

## Stack
n8n, Webhooks, PowerShell

## Arquitectura
Monitoreo -> Webhook -> n8n -> Script -> Notificacion -> Registro

## KPI esperado
-30% en tiempo de triage

## Estructura sugerida
- docs/ diagramas y decisiones tecnicas
- scripts/ automatizaciones
- src/ codigo principal
- 	ests/ pruebas basicas

## Proximos pasos
Integrar con Teams/Slack y runbooks versionados.
