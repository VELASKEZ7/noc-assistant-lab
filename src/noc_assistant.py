import argparse
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path


PRIORITY_MAP = {
    "critical": ("P1", 5, "Escalar a on-call y abrir bridge de incidente"),
    "high": ("P2", 15, "Asignar analista N2 y validar impacto en servicio"),
    "medium": ("P3", 30, "Programar revision con checklist operativo"),
    "low": ("P4", 60, "Registrar y monitorear en cola de baja prioridad"),
}

SLA_FIRST_RESPONSE_MIN = {
    "P1": 10,
    "P2": 20,
    "P3": 45,
    "P4": 90,
}


def parse_timestamp(value):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def triage_alert(alert, now_utc):
    severity = str(alert.get("severity", "low")).lower()
    priority, eta_minutes, runbook_action = PRIORITY_MAP.get(severity, PRIORITY_MAP["low"])
    result = dict(alert)
    first_seen = parse_timestamp(alert.get("timestamp"))
    age_minutes = None
    if first_seen:
        age_minutes = max(0, int((now_utc - first_seen).total_seconds() / 60))
    sla_limit = SLA_FIRST_RESPONSE_MIN[priority]
    projected_total_minutes = eta_minutes + (age_minutes or 0)
    result["priority"] = priority
    result["eta_minutes"] = eta_minutes
    result["sla_first_response_limit_minutes"] = sla_limit
    result["age_minutes"] = age_minutes
    result["projected_total_minutes"] = projected_total_minutes
    result["risk_sla_breach"] = projected_total_minutes > sla_limit
    result["runbook_action"] = runbook_action
    return result


def build_report(alerts, now_utc=None):
    now_utc = now_utc or datetime.now(UTC)
    triaged = [triage_alert(alert, now_utc) for alert in alerts]
    severity_counts = {}
    service_counts = Counter()
    total_eta = 0
    p1_or_p2 = 0
    potential_breaches = 0

    for alert in triaged:
        sev = alert["severity"].lower()
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
        service_counts[alert.get("service", "unknown")] += 1
        total_eta += alert["eta_minutes"]
        if alert["priority"] in {"P1", "P2"}:
            p1_or_p2 += 1
        if alert["risk_sla_breach"]:
            potential_breaches += 1

    total = len(triaged)
    avg_eta = round(total_eta / total, 2) if total else 0.0
    high_priority_ratio = round((p1_or_p2 / total) * 100, 2) if total else 0.0
    breach_ratio = round((potential_breaches / total) * 100, 2) if total else 0.0

    return {
        "summary": {
            "total_alerts": total,
            "severity_counts": severity_counts,
            "top_services": service_counts.most_common(5),
            "avg_eta_minutes": avg_eta,
            "high_priority_ratio_percent": high_priority_ratio,
            "potential_sla_breaches": potential_breaches,
            "potential_sla_breach_ratio_percent": breach_ratio,
            "generated_at_utc": now_utc.isoformat(),
        },
        "triaged_alerts": triaged,
    }


def build_markdown_report(report):
    summary = report["summary"]
    lines = [
        "# NOC Triage Report",
        "",
        f"- Total alerts: {summary['total_alerts']}",
        f"- Avg ETA (minutes): {summary['avg_eta_minutes']}",
        f"- High priority ratio (%): {summary['high_priority_ratio_percent']}",
        f"- Potential SLA breaches: {summary['potential_sla_breaches']}",
        "",
        "## Top services",
    ]
    for service, count in summary["top_services"]:
        lines.append(f"- {service}: {count}")
    lines.append("")
    lines.append("## Alerts with potential SLA breach")
    breach_rows = [a for a in report["triaged_alerts"] if a["risk_sla_breach"]]
    if not breach_rows:
        lines.append("- None")
    else:
        for alert in breach_rows:
            lines.append(
                f"- {alert.get('id', 'n/a')} | {alert.get('service', 'unknown')} | "
                f"{alert['priority']} | projected={alert['projected_total_minutes']}m | "
                f"sla={alert['sla_first_response_limit_minutes']}m"
            )
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="NOC assistant triage engine")
    parser.add_argument("--input", required=True, help="Path a alertas JSON")
    parser.add_argument("--output", required=True, help="Path de salida JSON")
    parser.add_argument("--markdown-output", help="Path de salida Markdown")
    parser.add_argument("--now", help="Timestamp UTC fijo en formato ISO8601")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fixed_now = parse_timestamp(args.now) if args.now else None

    alerts = json.loads(input_path.read_text(encoding="utf-8"))
    report = build_report(alerts, now_utc=fixed_now)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Generated triage report: {output_path}")
    if args.markdown_output:
        md_path = Path(args.markdown_output)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(build_markdown_report(report), encoding="utf-8")
        print(f"Generated markdown report: {md_path}")


if __name__ == "__main__":
    main()
