import argparse
import json
from pathlib import Path


PRIORITY_MAP = {
    "critical": ("P1", 5, "Escalar a on-call y abrir bridge de incidente"),
    "high": ("P2", 15, "Asignar analista N2 y validar impacto en servicio"),
    "medium": ("P3", 30, "Programar revision con checklist operativo"),
    "low": ("P4", 60, "Registrar y monitorear en cola de baja prioridad"),
}


def triage_alert(alert):
    severity = str(alert.get("severity", "low")).lower()
    priority, eta_minutes, runbook_action = PRIORITY_MAP.get(severity, PRIORITY_MAP["low"])
    result = dict(alert)
    result["priority"] = priority
    result["eta_minutes"] = eta_minutes
    result["runbook_action"] = runbook_action
    return result


def build_report(alerts):
    triaged = [triage_alert(alert) for alert in alerts]
    severity_counts = {}
    total_eta = 0
    p1_or_p2 = 0

    for alert in triaged:
        sev = alert["severity"].lower()
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
        total_eta += alert["eta_minutes"]
        if alert["priority"] in {"P1", "P2"}:
            p1_or_p2 += 1

    total = len(triaged)
    avg_eta = round(total_eta / total, 2) if total else 0.0
    high_priority_ratio = round((p1_or_p2 / total) * 100, 2) if total else 0.0

    return {
        "summary": {
            "total_alerts": total,
            "severity_counts": severity_counts,
            "avg_eta_minutes": avg_eta,
            "high_priority_ratio_percent": high_priority_ratio,
        },
        "triaged_alerts": triaged,
    }


def main():
    parser = argparse.ArgumentParser(description="NOC assistant triage engine")
    parser.add_argument("--input", required=True, help="Path a alertas JSON")
    parser.add_argument("--output", required=True, help="Path de salida JSON")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    alerts = json.loads(input_path.read_text(encoding="utf-8"))
    report = build_report(alerts)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Generated triage report: {output_path}")


if __name__ == "__main__":
    main()
