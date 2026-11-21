from pathlib import Path
from datetime import datetime, timezone
import json

PROJECT = Path("/content/drive/MyDrive/Cehpoint_Hermes_AI_SOC")
REPORTS_DIR = PROJECT / "reports"


def generate_reports(investigation):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    report = {
        "incident_id": investigation.get("incident_id"),
        "status": investigation.get("status", "UNDER_INVESTIGATION"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "severity": investigation.get("assessment", {}).get("severity", "Unknown"),
        "severity_reason": investigation.get("assessment", {}).get("severity_reason", ""),
        "confidence": investigation.get("assessment", {}).get("confidence", "Unknown"),
        "confidence_reason": investigation.get("assessment", {}).get("confidence_reason", ""),
        "affected_entities": investigation.get("affected_entities", {}),
        "timeline": investigation.get("timeline", []),
        "tool_results": investigation.get("tool_results", {}),
        "assessment": investigation.get("assessment", {}),
        "evidence_gaps": investigation.get("evidence_gaps", []),
        "recommendations": investigation.get("recommendations", [])
    }

    json_path = REPORTS_DIR / "incident_report.json"
    markdown_path = REPORTS_DIR / "incident_report.md"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    lines = [
        "# Security Incident Report",
        "",
        f"- **Incident ID:** {report['incident_id']}",
        f"- **Status:** {report['status']}",
        f"- **Generated:** {report['generated_at']}",
        f"- **Severity:** {report['severity']}",
        f"- **Severity rationale:** {report['severity_reason']}",
        f"- **Confidence:** {report['confidence']}",
        f"- **Confidence rationale:** {report['confidence_reason']}",
        "",
        "## Affected entities",
        ""
    ]

    for key, value in report["affected_entities"].items():
        lines.append(f"- **{key.replace('_', ' ').title()}:** {value}")

    lines.extend(["", "## Event timeline", ""])
    if report["timeline"]:
        for event in report["timeline"]:
            lines.append(
                f"- **{event.get('timestamp')}** — "
                f"{event.get('event_type')} "
                f"(Event: {event.get('event_id')}; "
                f"source line: {event.get('evidence_reference')})"
            )
    else:
        lines.append("- No timestamped events were retrieved.")

    lines.extend([
        "",
        "## Assessment",
        "",
        report["assessment"].get("conclusion", "No conclusion available."),
        "",
        "## Evidence gaps and limitations",
        ""
    ])

    if report["evidence_gaps"]:
        lines.extend([f"- {gap}" for gap in report["evidence_gaps"]])
    else:
        lines.append("- No evidence gaps were recorded.")

    lines.extend(["", "## Tool results", ""])
    for tool_name, result in report["tool_results"].items():
        lines.append(f"### {tool_name}")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(result, indent=2, ensure_ascii=False))
        lines.append("```")
        lines.append("")

    lines.extend(["## Recommendations", ""])
    for item in report["recommendations"]:
        lines.extend([
            f"### Priority {item.get('priority', 'N/A')}: {item.get('action', 'Unspecified')}",
            f"- **Expected impact:** {item.get('expected_impact', 'Not specified')}",
            f"- **Approval required:** {item.get('approval_required', 'Not specified')}",
            ""
        ])

    lines.extend([
        "---",
        "",
        "This report is based only on the supplied dataset and recorded tool outputs.",
        "Mock intelligence is not a live threat-intelligence assessment.",
        "No production response action was executed."
    ])

    with markdown_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return {
        "json_report": str(json_path),
        "markdown_report": str(markdown_path),
        "incident_id": report["incident_id"]
    }
